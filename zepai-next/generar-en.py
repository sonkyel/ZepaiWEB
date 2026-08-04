# -*- coding: utf-8 -*-
"""Genera las paginas /en/ a partir de las espanolas.

La traduccion ya existe: cada texto lleva data-es y data-en. Lo que faltaba
era darle una URL, porque un idioma que solo vive en atributos que se
intercambian en el navegador no lo indexa nadie.

Se genera en vez de escribirse a mano por una razon concreta: si manana
cambia un parrafo en espanol, se vuelve a lanzar esto y el ingles no se
queda atras. Dos copias escritas a mano se desincronizan siempre.

Que hace con cada pagina:
  - El texto visible pasa a ser el de data-en.
  - Los atributos se conservan TAL CUAL: data-es sigue siendo el castellano.
    Invertirlos rompia la pagina inglesa; el porque esta en a_ingles().
  - El titulo y la descripcion salen del <h1> y del subtitulo en ingles.
  - El canonical apunta a /en/..., y se declara hreflang en las dos
    direcciones.
"""
import io
import json
import os
import re

BASE = r"c:\Users\Sonkyel\Desktop\zepai-landing\zepai-next"
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

# Los articulos del blog traen su propio titulo de buscador, ya medido por
# debajo de 60 caracteres. Derivarlo del <h1> lo pasaba de largo: el titular
# de un articulo es una frase, no una etiqueta.
_arts = os.path.join(BASE, "_fuentes", "blog", "articulos.json")
if os.path.exists(_arts):
    for _a in json.load(io.open(_arts, encoding="utf-8")):
        TITULOS_EN["blog/" + _a["slug"]] = _a["titulo_en"]
        DESC_EN["blog/" + _a["slug"]] = _a["desc_en"]

SALTAR = {"en", "politica-de-cookies", "aviso-legal", "politica-de-privacidad"}


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
    # <tag ... data-es="A" data-en="B" ...>texto</tag>
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


def literal(ruta_tsx):
    s = io.open(ruta_tsx, encoding="utf-8").read()
    m = re.search(r'const HTML = (".*?");\n', s, re.S)
    if m:
        return s, json.loads(m.group(1)), m.span(1)
    m = re.search(r'const HTML = `(.*?)`;\n', s, re.S)
    if m:
        return s, m.group(1), m.span(1)
    return s, None, None


def generar(ruta):
    origen = os.path.join(APP, ruta, "page.tsx") if ruta else os.path.join(APP, "page.tsx")
    s, html, span = literal(origen)
    if html is None:
        return None

    ingles = a_ingles(html)

    if ruta:
        h1_es, h1_en = extrae(html, "sp-h1")
        lead_es, lead_en = extrae(html, "sp-lead")
        titulo = TITULOS_EN.get(
            ruta, "%s | Zepai" % (h1_en or ruta.replace("-", " ").title()))
        desc = DESC_EN.get(ruta) or (lead_en or "")
        if len(desc) > 155:
            # Cortar por palabra, no a hachazos: un "automatiza" a
            # medias en el buscador se lee como una web descuidada.
            desc = desc[:155].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    else:
        titulo, desc = HOME["titulo"], HOME["desc"]

    destino_ruta = "/en" + ("/" + ruta if ruta else "")
    canonico_es = "/" + ruta if ruta else "/"

    cuerpo = '''import type { Metadata } from "next";
import { LegacyContent } from "@/components/site/LegacyContent";

/* GENERADO por generar-en.py desde la pagina en espanol. No editar a mano:
   si cambia el castellano, se vuelve a lanzar el guion y esta se rehace. */

const TITULO = %s;
const DESC = %s;

export const metadata: Metadata = {
  title: TITULO,
  description: DESC,
  alternates: {
    canonical: %s,
    languages: { es: %s, en: %s, "x-default": %s },
  },
  openGraph: {
    title: TITULO,
    description: DESC,
    url: "%s" + %s,
    siteName: "Zepai Agency",
    locale: "en_US",
    type: "website",
    images: ["%s/og-image.png"],
  },
  twitter: { card: "summary_large_image", title: TITULO, description: DESC, images: ["%s/og-image.png"] },
};

const HTML = %s;

export default function Page() {
  return (
    <div lang="en">
      <LegacyContent html={HTML} />
    </div>
  );
}
''' % (json.dumps(titulo, ensure_ascii=False), json.dumps(desc, ensure_ascii=False),
       json.dumps(destino_ruta), json.dumps(canonico_es), json.dumps(destino_ruta), json.dumps(canonico_es),
       URL, json.dumps(destino_ruta), URL, URL,
       json.dumps(ingles, ensure_ascii=False))

    carpeta = os.path.join(APP, "en", ruta) if ruta else os.path.join(APP, "en")
    os.makedirs(carpeta, exist_ok=True)
    io.open(os.path.join(carpeta, "page.tsx"), "w", encoding="utf-8", newline="\n").write(cuerpo)
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

    hechas = []
    for r in rutas:
        res = generar(r)
        if res:
            hechas.append(res)
            print("  %-46s %s" % (res[0], res[1][:52]))
        else:
            print("  SALTADA (sin HTML literal): /%s" % r)
    print("\n%d paginas en ingles" % len(hechas))
    return [h[0] for h in hechas]


if __name__ == "__main__":
    main()
