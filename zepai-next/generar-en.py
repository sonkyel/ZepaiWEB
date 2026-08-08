# -*- coding: utf-8 -*-
"""Genera las paginas /en/ a partir de las espanolas.

La traduccion ya existe: cada texto lleva data-es y data-en. Lo que faltaba
era darle una URL, porque un idioma que solo vive en atributos que se
intercambian en el navegador no lo indexa nadie.

Se genera en vez de escribirse a mano por una razon concreta: si manana
cambia un parrafo en espanol, se vuelve a lanzar esto y el ingles no se
queda atras. Dos copias escritas a mano se desincronizan siempre.


COMO SE GENERA, Y POR QUE ASI
-----------------------------
Antes esto emitia una PLANTILLA fija: un page.tsx nuevo que montaba
LegacyContent y nada mas. Servia para las paginas interiores, que son solo
HTML heredado, pero la portada monta ademas <HeroSection /> y
<HomeScripts />, y la plantilla los tiraba. Resultado: en /en no habia hero
-- que es lo que se veia -- y tampoco legacy-home.js, asi que la agenda
salia vacia y los formularios no enviaban. El JSON-LD se perdia en las 21
paginas.

Ahora no hay plantilla. Se parte del fichero espanol y se sustituyen SOLO
las tres piezas que cambian de idioma:

    metadata   ->  titulo, descripcion, canonical /en y hreflang
    HTML       ->  a_ingles()
    JSON_LD    ->  traducido y con las URLs reapuntadas

Los imports y el `export default function Page()` se copian tal cual. Asi el
arbol de componentes coincide POR CONSTRUCCION: si manana una pagina gana un
componente, la inglesa lo hereda sin que este guion se entere.
"""
import io
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(BASE, "src", "app")
URL = "https://zepaiagency.com"

# La home lleva titulo y descripcion escritos a mano: su titular esta en un
# componente React, no en el HTML heredado.
HOME = dict(
    titulo="AI Agency for Business Process Automation | Zepai",
    # Ojo: esto es la fuente de la verdad de /en. Si se corrige a mano en
    # src/app/en/page.tsx, el siguiente lanzamiento del guion lo revierte.
    desc=("We automate your company's processes with artificial intelligence: "
          "customer service, sales, bookings, support and operations. "
          "AI agency and consultancy."),
)

# Titulos de buscador para las paginas inglesas cuyo <h1> pasa de 60
# caracteres con el sufijo de marca. El titular de la pagina se queda como
# esta: es lo que lee la persona, y tiene voz. Esto es solo lo que sale en
# Google, donde por encima de 60 se corta a la mitad.
DESC_EN = {}

TITULOS_EN = {
    "como-trabajamos": "How we work: six beliefs about automation | Zepai",
    "trafico-en-redes": "Social media growth that brings buyers | Zepai",
    "marketing-digital": "Digital marketing measured in customers | Zepai",
    "blog/como-automatizar-la-atencion-al-cliente-con-ia":
        "How to automate customer service with AI | Zepai",
}

SALTAR = {"en", "politica-de-cookies", "aviso-legal", "politica-de-privacidad"}


# ── JSON-LD ────────────────────────────────────────────────────────────────
#
# Clasificacion de claves. Lo que no este en ninguna de las tres listas se
# trata como texto sin traduccion y ABORTA: es la unica forma de que una
# clave nueva no cuele castellano bajo inLanguage:"en" el dia de manana.

CLAVES_TEXTO = {"name", "description", "headline", "text",
                "audienceType", "serviceType"}
CLAVES_URL = {"@id", "item", "url"}
CLAVES_LITERAL = {"@context", "@type", "image", "logo", "sameAs", "position",
                  "datePublished", "dateModified", "priceCurrency",
                  "telephone", "email", "addressCountry", "addressLocality",
                  "contactType", "availableLanguage"}

# Entidades del layout, emitidas en TODAS las paginas y sin idioma. Si se
# reapuntaran a /en, author y publisher quedarian colgando de entidades que
# no existen -- peor que no traducir nada.
GLOBALES = (URL + "/#organization", URL + "/#fundador")

# Textos del JSON-LD que no tienen pareja en los data-en de su pagina ni en
# articulos.json. Son traducciones del castellano que ya estaba escrito.
TEXTOS_EN = {
    "Worldwide": "Worldwide",

    # Sectores a los que se dirige cada servicio (audienceType)
    "Agencias inmobiliarias y promotoras":
        "Real estate agencies and property developers",
    "Empresas con atención al cliente por chat o teléfono":
        "Businesses with customer service by chat or phone",
    "Empresas con procesos internos repetitivos":
        "Businesses with repetitive internal processes",
    "Empresas de cualquier sector": "Businesses in any industry",
    "Empresas que atienden clientes por WhatsApp":
        "Businesses that serve customers over WhatsApp",
    "Empresas que quieren captar clientes por internet":
        "Businesses looking to win customers online",
    "Empresas que quieren crecer en redes sociales":
        "Businesses looking to grow on social media",
    "Empresas que reciben llamadas de clientes":
        "Businesses that receive customer calls",
    "Empresas y creadores con vídeo largo o directos":
        "Businesses and creators with long-form video or live streams",
    "Restaurantes, bares y cafeterías": "Restaurants, bars and cafes",
    "Tiendas online y e-commerce": "Online shops and e-commerce",

    # Nombres de servicio (serviceType / name)
    "Agentes de IA para atención al cliente":
        "AI agents for customer service",
    "Asistente de voz con IA para restaurantes":
        "AI voice assistant for restaurants",
    "Automatización de llamadas con IA": "AI call automation",
    "Chatbot de IA por WhatsApp para inmobiliarias":
        "WhatsApp AI chatbot for real estate",
    "Clipping de contenido": "Content clipping",
    "Consultoría de IA para empresas": "AI consultancy for business",
    "Crecimiento de audiencia en redes sociales":
        "Social media audience growth",
    "Inteligencia artificial para tiendas online":
        "Artificial intelligence for online shops",
    "Marketing digital": "Digital marketing",

    # Descripciones de servicio
    "Agente de inteligencia artificial en WhatsApp que responde, cualifica y "
    "agenda visitas para agencias inmobiliarias de forma automática.":
        "Artificial intelligence agent on WhatsApp that replies, qualifies "
        "leads and books viewings for real estate agencies automatically.",
    "Agente de voz con inteligencia artificial que atiende llamadas "
    "entrantes, gestiona reservas y citas, filtra y deriva llamadas y "
    "realiza llamadas de salida rutinarias.":
        "Artificial intelligence voice agent that answers incoming calls, "
        "manages bookings and appointments, screens and routes calls, and "
        "makes routine outbound calls.",
    "Agentes de IA para e-commerce: resolución de dudas previas a la compra, "
    "consulta del estado de pedidos, gestión de devoluciones y recuperación "
    "de carritos abandonados.":
        "AI agents for e-commerce: pre-purchase questions, order status "
        "checks, returns handling and abandoned cart recovery.",
    "Agentes de inteligencia artificial de chat y de voz que atienden "
    "consultas, toman reservas y cualifican clientes las 24 horas.":
        "Chat and voice artificial intelligence agents that answer enquiries, "
        "take bookings and qualify customers around the clock.",
    "Asistente de voz con inteligencia artificial que atiende llamadas, "
    "gestiona reservas y responde consultas de clientes en restaurantes, "
    "24 horas al día.":
        "Artificial intelligence voice assistant that answers calls, manages "
        "bookings and handles customer enquiries for restaurants, 24 hours "
        "a day.",
    "Chatbot de inteligencia artificial sobre la API oficial de WhatsApp "
    "Business que atiende consultas, toma reservas y pedidos y cualifica "
    "clientes.":
        "Artificial intelligence chatbot on the official WhatsApp Business "
        "API that answers enquiries, takes bookings and orders, and "
        "qualifies customers.",
    "Consultoría de inteligencia artificial: diagnóstico de procesos, "
    "priorización de oportunidades, prueba piloto e implementación de "
    "automatizaciones a medida.":
        "Artificial intelligence consultancy: process diagnosis, "
        "prioritising opportunities, pilot testing and bespoke automation "
        "rollout.",
    "Diseño, implementación y mantenimiento de flujos de automatización con "
    "n8n y Make para procesos internos empresariales, con integración de "
    "modelos de IA.":
        "Design, rollout and maintenance of n8n and Make automation "
        "workflows for internal business processes, with AI model "
        "integration.",
    "Edición de vídeos largos en clips cortos optimizados para TikTok, "
    "Instagram Reels y YouTube Shorts.":
        "Editing long videos into short clips optimised for TikTok, "
        "Instagram Reels and YouTube Shorts.",
    "Estrategia de contenido, email marketing y campañas pagadas para "
    "empresas, con seguimiento de resultados.":
        "Content strategy, email marketing and paid campaigns for business, "
        "with results tracking.",
    "Estrategia de crecimiento de audiencia orgánica y pagada en redes "
    "sociales para empresas.":
        "Organic and paid social media audience growth strategy for "
        "business.",

    # Paginas indice
    "Artículos sobre automatización de procesos e inteligencia artificial "
    "aplicada a empresas.":
        "Articles on process automation and artificial intelligence applied "
        "to business.",
    "Catálogo de soluciones de inteligencia artificial de Zepai Agency, por "
    "tipo de automatización y por sector.":
        "Zepai Agency's catalogue of artificial intelligence solutions, by "
        "type of automation and by industry.",
    "Seis creencias sobre cómo se automatiza un negocio de verdad: revisar "
    "el proceso antes que la tecnología, cerrar los límites y saber cuándo "
    "no automatizar.":
        "Six beliefs about how a business really gets automated: fix the "
        "process before the technology, set hard limits, and know when not "
        "to automate.",
    "Por dónde empezar a automatizar la atención al cliente, qué no debe "
    "contestar nunca una máquina y qué medir antes de lanzar.":
        "Where to start automating customer service, what a machine should "
        "never answer, and what to measure before launching.",

    # Respuesta del FAQ que no tiene pareja i18n en el HTML
    "Solo se guarda lo necesario para atender la conversación, viaja siempre "
    "por conexión cifrada y no se vende ni se comparte con terceros para "
    "marketing. Puedes pedirnos que eliminemos cualquier dato cuando "
    "quieras. Lo tienes detallado en nuestra Política de Privacidad.":
        "We only store what is needed to handle the conversation, it always "
        "travels over an encrypted connection, and it is never sold or "
        "shared with third parties for marketing. You can ask us to delete "
        "any data whenever you want. It is all set out in our Privacy "
        "Policy.",
}


def _articulos():
    """Traducciones de los articulos del blog, ya escritas y revisadas."""
    dic = {}
    ruta = os.path.join(BASE, "_fuentes", "blog", "articulos.json")
    if not os.path.exists(ruta):
        return dic
    for a in json.load(io.open(ruta, encoding="utf-8")):
        for par in ("titulo", "desc", "h1", "lead", "migaja"):
            es, en = a.get(par + "_es"), a.get(par + "_en")
            if es and en:
                dic[es] = en
        TITULOS_EN["blog/" + a["slug"]] = a["titulo_en"]
        DESC_EN["blog/" + a["slug"]] = a["desc_en"]
    return dic


ARTICULOS = _articulos()


def reapunta(v):
    """Mete /en en las URLs propias. Las globales y las externas, intactas."""
    if v in GLOBALES or not v.startswith(URL):
        return v
    resto = v[len(URL):]
    return URL + "/en" + ("" if resto == "/" else resto)


def traduce_ld(nodo, pares, faltan, camino="JSON_LD"):
    if isinstance(nodo, list):
        return [traduce_ld(x, pares, faltan, "%s[%d]" % (camino, i))
                for i, x in enumerate(nodo)]
    if not isinstance(nodo, dict):
        return nodo

    salida = {}
    for k, v in nodo.items():
        sub = camino + "." + k
        if k == "inLanguage":
            salida[k] = "en"
        elif isinstance(v, str) and k in CLAVES_URL:
            salida[k] = reapunta(v)
        elif isinstance(v, str) and k in CLAVES_LITERAL:
            salida[k] = v
        elif isinstance(v, str) and k in CLAVES_TEXTO:
            en = pares.get(v) or ARTICULOS.get(v) or TEXTOS_EN.get(v)
            if en is None:
                faltan.append((sub, v))
                salida[k] = v
            else:
                salida[k] = en
        elif isinstance(v, str):
            # Clave desconocida con texto dentro: no se deja pasar.
            faltan.append((sub + "  (clave sin clasificar)", v))
            salida[k] = v
        else:
            salida[k] = traduce_ld(v, pares, faltan, sub)
    return salida


# ── Corte de literales dentro del page.tsx ─────────────────────────────────

def corta(s, marcador, abre, parsear=True):
    """(inicio, fin, valor) del literal que sigue a `marcador`.

    Cuenta delimitadores ignorando los que van dentro de una cadena: el
    aviso legal tiene un corchete en el texto y un contador ingenuo se
    descuadraba justo ahi.

    Con parsear=False solo devuelve el tramo. Hace falta para el bloque
    metadata, que es TypeScript -- lleva `...metaSocial(...)` dentro -- y no
    hay nada que interpretar: se sustituye entero.
    """
    i = s.find(marcador)
    if i < 0:
        return None
    j = s.index(abre, i)
    cierra = {"[": "]", "{": "}", '"': '"'}[abre]
    lee = (lambda t: json.loads(t)) if parsear else (lambda t: None)

    if abre == '"':
        k = j + 1
        while True:
            if s[k] == "\\":
                k += 2
                continue
            if s[k] == '"':
                return j, k + 1, lee(s[j:k + 1])
            k += 1

    hondo = 0
    dentro = False
    escapa = False
    for k in range(j, len(s)):
        c = s[k]
        if escapa:
            escapa = False
            continue
        if c == "\\":
            escapa = True
            continue
        if c == '"':
            dentro = not dentro
            continue
        if dentro:
            continue
        if c == abre:
            hondo += 1
        elif c == cierra:
            hondo -= 1
            if hondo == 0:
                return j, k + 1, lee(s[j:k + 1])
    return None


def a_ingles(html):
    """Pone el texto visible en ingles. Los atributos NO se tocan.

    Antes se invertian -- data-es pasaba a contener el ingles -- porque el
    conmutador de idioma intercambiaba los textos dentro de la misma pagina y
    hacia falta que siguiera funcionando en la inglesa.

    Eso dejo de ser cierto cuando el conmutador paso a ser dos enlaces a
    /es y /en, y la inversion se quedo haciendo dano en silencio:
    LegacyEnhancer escribe el.textContent = el.dataset[lang], y en /en el
    idioma es "en", asi que leia el data-en invertido... que contenia el
    castellano. Resultado: /en llegaba en ingles y React la volvia a poner en
    espanol al hidratar.

    Es el peor de los dos mundos. Google indexaba una version en ingles que
    ninguna persona llegaba a ver -- que es la definicion de contenido
    encubierto, y eso Google lo penaliza.
    """
    patron = re.compile(
        r'(<(?:span|p|h1|h2|h3|h4|div|a|li|button|time)\b[^>]*?)'
        r'data-es="([^"]*)"\s+data-en="([^"]*)"'
        r'([^>]*)>([^<]*)(</)', re.S)

    def rep(m):
        antes, es, en, despues, _texto, cierre = m.groups()
        return '%sdata-es="%s" data-en="%s"%s>%s%s' % (antes, es, en, despues, en, cierre)

    return patron.sub(rep, html)


def extrae(html, clase):
    m = re.search(r'class="%s[^"]*"[^>]*data-es="([^"]*)"\s+data-en="([^"]*)"' % clase, html)
    return m.groups() if m else (None, None)


AVISO = """/* GENERADO por generar-en.py desde la pagina en espanol. No editar a mano:
   si cambia el castellano, se vuelve a lanzar el guion y esta se rehace.
   Los imports y el componente son los del fichero espanol, copiados tal
   cual: asi /en monta exactamente los mismos componentes que /. */
"""


def metadata_en(titulo, desc, destino, canonico_es):
    return (
        'export const metadata: Metadata = {\n'
        '  title: %s,\n'
        '  description: %s,\n'
        '  alternates: {\n'
        '    canonical: %s,\n'
        '    languages: { es: %s, en: %s, "x-default": %s },\n'
        '  },\n'
        '  ...metaSocial(%s, %s, %s, "en_US"),\n'
        '};'
        % (json.dumps(titulo, ensure_ascii=False), json.dumps(desc, ensure_ascii=False),
           json.dumps(destino), json.dumps(canonico_es), json.dumps(destino),
           json.dumps(canonico_es),
           json.dumps(titulo, ensure_ascii=False), json.dumps(desc, ensure_ascii=False),
           json.dumps(destino))
    )


def generar(ruta, problemas):
    origen = os.path.join(APP, ruta, "page.tsx") if ruta else os.path.join(APP, "page.tsx")
    s = io.open(origen, encoding="utf-8").read()

    trozo_html = corta(s, "const HTML = ", '"')
    if trozo_html is None:
        return None
    ini_h, fin_h, html = trozo_html

    destino_ruta = "/en" + ("/" + ruta if ruta else "")
    canonico_es = "/" + ruta if ruta else "/"

    if ruta:
        _, h1_en = extrae(html, "sp-h1")
        _, lead_en = extrae(html, "sp-lead")
        titulo = TITULOS_EN.get(
            ruta, "%s | Zepai" % (h1_en or ruta.replace("-", " ").title()))
        desc = DESC_EN.get(ruta) or (lead_en or "")
        if len(desc) > 155:
            # Cortar por palabra, no a hachazos: un "automatiza" a
            # medias en el buscador se lee como una web descuidada.
            desc = desc[:155].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    else:
        titulo, desc = HOME["titulo"], HOME["desc"]

    # Las sustituciones se aplican de atras hacia delante para que los
    # indices de las anteriores sigan siendo validos.
    piezas = [(ini_h, fin_h, json.dumps(a_ingles(html), ensure_ascii=False))]

    trozo_ld = corta(s, "const JSON_LD = ", "[")
    if trozo_ld:
        ini_l, fin_l, ld = trozo_ld
        pares = dict(re.findall(r'data-es="([^"]*)"\s+data-en="([^"]*)"', html))
        faltan = []
        ld_en = traduce_ld(ld, pares, faltan)
        for donde, texto in faltan:
            problemas.append("%s  %s\n      %s" % (destino_ruta, donde, texto))
        piezas.append((ini_l, fin_l, json.dumps(ld_en, ensure_ascii=False)))

    MARCA = "export const metadata: Metadata = "
    trozo_meta = corta(s, MARCA, "{", parsear=False)
    if trozo_meta is None:
        problemas.append("%s  sin bloque metadata" % destino_ruta)
        return None
    _, fin_m, _ = trozo_meta
    # Desde el principio de la declaracion, no desde la llave: el texto nuevo
    # ya trae el "export const metadata", y sustituir solo el bloque dejaba
    # la declaracion escrita dos veces.
    # fin_m+1 se come ademas el ';' de cierre, que el nuevo tambien trae.
    piezas.append((s.index(MARCA), fin_m + 1,
                   metadata_en(titulo, desc, destino_ruta, canonico_es)))
    salida = s
    for ini, fin, nuevo in sorted(piezas, reverse=True):
        salida = salida[:ini] + nuevo + salida[fin:]
    salida = AVISO + salida

    # El layout emite <html lang="es"> para todo el sitio, asi que sin esto
    # /en se sirve declarando castellano con el contenido en ingles. Se
    # envuelve el componente entero en vez de tocar su JSX: el cuerpo se
    # copia tal cual y no hay nada que un cambio en la pagina espanola pueda
    # romper aqui.
    VIEJO = "export default function Page() {"
    if salida.count(VIEJO) != 1:
        problemas.append("%s  no encuentro el componente para marcar el idioma"
                         % destino_ruta)
        return None
    salida = salida.replace(VIEJO, "function Contenido() {")
    salida = salida.rstrip() + """

export default function Page() {
  return (
    <div lang="en">
      <Contenido />
    </div>
  );
}
"""

    if "metaSocial" not in salida:
        problemas.append("%s  la pagina espanola no importa metaSocial" % destino_ruta)
        return None

    carpeta = os.path.join(APP, "en", ruta) if ruta else os.path.join(APP, "en")
    os.makedirs(carpeta, exist_ok=True)
    io.open(os.path.join(carpeta, "page.tsx"), "w", encoding="utf-8", newline="\n").write(salida)
    return destino_ruta, titulo


def main():
    rutas = [""]
    for d in sorted(os.listdir(APP)):
        p = os.path.join(APP, d)
        if not os.path.isdir(p) or d in SALTAR or d.startswith(("_", "[")):
            continue
        if os.path.exists(os.path.join(p, "page.tsx")):
            rutas.append(d)
        for sub in sorted(os.listdir(p)):
            if os.path.exists(os.path.join(p, sub, "page.tsx")):
                rutas.append("%s/%s" % (d, sub))

    problemas = []
    hechas = []
    for r in rutas:
        res = generar(r, problemas)
        if res:
            hechas.append(res)
            print("  %-46s %s" % (res[0], res[1][:52]))
        else:
            print("  SALTADA (sin HTML literal): /%s" % r)

    if problemas:
        # Publicar castellano bajo inLanguage:"en" le dice a Google una cosa
        # y le ensena otra. Antes que eso, no se genera nada.
        raise SystemExit(
            "\nNO SE GENERA. %d textos del JSON-LD sin traduccion:\n\n  %s\n"
            % (len(problemas), "\n  ".join(problemas)))

    print("\n%d paginas en ingles" % len(hechas))
    return [h[0] for h in hechas]


if __name__ == "__main__":
    main()
