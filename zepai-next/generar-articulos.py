# -*- coding: utf-8 -*-
"""Monta las paginas del blog desde _fuentes/blog/articulos.json.

Se genera y no se escribe a mano por lo de siempre en este repo: el HTML vive
dentro de un literal de UNA sola linea con las comillas escapadas, y editar
eso a mano ya rompio la nav y el pie una vez. Aqui el escapado lo hace
json.dumps, que no se equivoca.

Dos cosas que arregla respecto al articulo que ya existia:

  - Cada articulo lleva un <p class="sp-lead">. No es cosmetica:
    generar-en.py saca la meta description de la version inglesa justamente
    de ahi, y sin sp-lead la pagina /en/blog/... se publicaba con la
    descripcion VACIA. Estaba asi desde el primer dia.

  - El author del schema apunta a la persona (#fundador), no a la empresa.
    El articulo ahora firma "Por Zecuenin Soto" en la pagina, y los datos
    estructurados tienen que decir lo mismo que se lee.

    python generar-articulos.py
"""
import io
import json
import os
import re
import sys
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(BASE, "src", "app")
URL = "https://zepaiagency.com"
FUENTE = os.path.join(BASE, "_fuentes", "blog", "articulos.json")

FECHA = date.today().isoformat()
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
MESES_EN = ["January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"]

# Enlaces del pie de cada articulo. Se eligen por tema para que el enlazado
# interno tenga sentido y no sea el mismo bloque repetido cinco veces.
RELACIONADOS = {
    "chatbot-whatsapp-api-oficial-o-movil": [
        ("/chatbot-whatsapp", "Chatbot de WhatsApp", "WhatsApp chatbot"),
        ("/agentes-de-ia", "Agentes de IA", "AI agents"),
        ("/como-trabajamos", "Cómo trabajamos", "How we work"),
    ],
    "cuanto-cuesta-automatizar-atencion-al-cliente": [
        ("/consultoria-ia", "Consultoría de IA", "AI consultancy"),
        ("/soluciones", "Todas las soluciones", "All solutions"),
        ("/como-trabajamos", "Cómo trabajamos", "How we work"),
    ],
    "agente-de-voz-ia-para-llamadas": [
        ("/automatizacion-de-llamadas", "Automatización de llamadas", "Call automation"),
        ("/agencia-ia-restaurantes", "IA para restaurantes", "AI for restaurants"),
        ("/agentes-de-ia", "Agentes de IA", "AI agents"),
    ],
    "automatizar-reservas-restaurante": [
        ("/agencia-ia-restaurantes", "IA para restaurantes", "AI for restaurants"),
        ("/chatbot-whatsapp", "Chatbot de WhatsApp", "WhatsApp chatbot"),
        ("/automatizacion-de-llamadas", "Automatización de llamadas", "Call automation"),
    ],
    "que-no-deberias-automatizar": [
        ("/como-trabajamos", "Cómo trabajamos", "How we work"),
        ("/consultoria-ia", "Consultoría de IA", "AI consultancy"),
        ("/automatizaciones-n8n-make", "Automatizaciones con n8n y Make", "n8n and Make automations"),
    ],
}


def limpio(t, campo):
    """Ni comillas dobles ni < dentro de un atributo i18n.

    La comilla romperia el atributo, y a_ingles() de generar-en.py usa
    ([^<]*) para el texto visible: un < ahi dejaria el bloque sin traducir.
    """
    if '"' in t:
        raise SystemExit("comilla doble en %s: %r" % (campo, t[:70]))
    if "<" in t or ">" in t:
        raise SystemExit("angulo en %s: %r" % (campo, t[:70]))
    return t


def i18n(etiqueta, clases, es, en, campo, extra=""):
    limpio(es, campo)
    limpio(en, campo)
    cl = (clases + " i18n").strip()
    return '<%s class="%s"%s data-es="%s" data-en="%s">%s</%s>' % (
        etiqueta, cl, extra, es, en, es, etiqueta)


def html_articulo(a):
    fecha_es = "%d de %s de %s" % (int(FECHA[8:10]), MESES[int(FECHA[5:7]) - 1], FECHA[:4])
    fecha_en = "%d %s %s" % (int(FECHA[8:10]), MESES_EN[int(FECHA[5:7]) - 1], FECHA[:4])

    p = []
    p.append('<section class="sp-hero">')
    p.append('    <div class="container">')
    p.append('      <div class="sp-hero-txt" style="max-width:760px">')
    p.append('      <nav class="sp-crumbs" aria-label="Breadcrumb">')
    p.append('        <a href="/" class="i18n" data-es="Inicio" data-en="Home">Inicio</a>')
    p.append('        <span> / </span>')
    p.append('        <a href="/blog" class="i18n" data-es="Blog" data-en="Blog">Blog</a>')
    p.append('        <span> / </span>')
    p.append('        ' + i18n("span", "", a["migaja_es"], a["migaja_en"], "migaja"))
    p.append('      </nav>')
    p.append('      ' + i18n("h1", "sp-h1", a["h1_es"], a["h1_en"], "h1"))
    p.append('      ' + i18n("p", "sp-lead", a["lead_es"], a["lead_en"], "lead"))
    p.append('      <p class="sp-meta">')
    p.append('        ' + i18n("time", "", fecha_es, fecha_en, "fecha",
                               extra=' datetime="%s"' % FECHA))
    p.append('        <span aria-hidden="true"> &middot; </span>')
    p.append('        <span class="i18n" data-es="Por Zecuenin Soto" data-en="By Zecuenin Soto">Por Zecuenin Soto</span>')
    p.append('      </p>')
    p.append('      </div>')
    p.append('    </div>')
    p.append('  </section>')
    p.append('')
    p.append('  <section class="sp-body">')
    p.append('    <div class="container">')
    for s in a["secciones"]:
        p.append('      ' + i18n("h2", "sp-h2", s["h2_es"], s["h2_en"], "h2"))
        for par in s["parrafos"]:
            p.append('      ' + i18n("p", "", par["es"], par["en"], "parrafo"))
    p.append('')
    p.append('      <section class="sp-cta reveal">')
    p.append('        ' + i18n("h2", "", "¿Lo quieres montar en tu empresa?",
                               "Want to build this in your company?", "cta-h2"))
    p.append('        ' + i18n("p", "",
                               "Media hora, sin discurso comercial. Y si vemos que no te compensa, te lo decimos.",
                               "Half an hour, no sales pitch. And if we think it is not worth it for you, we will say so.",
                               "cta-p"))
    p.append('        <a class="btn-p" href="/#contact">')
    p.append('          <span class="i18n" data-es="Pedir cotización gratis" data-en="Get a free quote">Pedir cotización gratis</span>')
    p.append('          <span>&rarr;</span>')
    p.append('        </a>')
    p.append('      </section>')
    p.append('      <section class="sp-related">')
    p.append('        <h2 class="i18n" data-es="Sigue explorando" data-en="Keep exploring">Sigue explorando</h2>')
    p.append('        <ul>')
    for ruta, es, en in RELACIONADOS[a["slug"]]:
        p.append('        <li>' + i18n("a", "", es, en, "relacionado",
                                       extra=' href="%s"' % ruta) + '</li>')
    p.append('        <li><a href="/blog" class="i18n" data-es="Volver al blog" data-en="Back to the blog">Volver al blog</a></li>')
    p.append('        </ul>')
    p.append('      </section>')
    p.append('    </div>')
    p.append('  </section>')
    return "\n".join(p)


def json_ld(a):
    u = "%s/blog/%s" % (URL, a["slug"])
    return [
        {"@context": "https://schema.org", "@type": "BlogPosting",
         "headline": a["h1_es"], "description": a["desc_es"], "url": u,
         "mainEntityOfPage": {"@type": "WebPage", "@id": u},
         "inLanguage": "es", "datePublished": FECHA, "dateModified": FECHA,
         "image": "%s/og-image.png" % URL,
         # La persona, no la empresa: la pagina firma "Por Zecuenin Soto".
         "author": {"@id": "%s/#fundador" % URL},
         "publisher": {"@id": "%s/#organization" % URL}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList",
         "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Inicio", "item": URL + "/"},
             {"@type": "ListItem", "position": 2, "name": "Blog", "item": URL + "/blog"},
             {"@type": "ListItem", "position": 3, "name": a["h1_es"], "item": u}]},
    ]


def pagina(a):
    ruta = "/blog/%s" % a["slug"]
    j = json.dumps
    return '''import type { Metadata } from "next";
import { metaSocial } from "@/lib/site";
import { LegacyContent } from "@/components/site/LegacyContent";

/* GENERADO por generar-articulos.py desde _fuentes/blog/articulos.json.
   No editar a mano: se pierde al regenerar. */

export const metadata: Metadata = {
  title: %s,
  description: %s,
  alternates: {
    canonical: %s,
    languages: { es: %s, en: %s, "x-default": %s },
  },
  ...metaSocial(
    %s,
    %s,
    %s,
  ),
};

const JSON_LD = %s;

const HTML = %s;

export default function Page() {
  return (
    <>
      {JSON_LD.map((d, i) => (
        <script
          key={i}
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(d) }}
        />
      ))}
      <LegacyContent html={HTML} />
    </>
  );
}
''' % (j(a["titulo_es"], ensure_ascii=False), j(a["desc_es"], ensure_ascii=False),
       j(ruta), j(ruta), j("/en" + ruta), j(ruta),
       j(a["titulo_es"], ensure_ascii=False), j(a["desc_es"], ensure_ascii=False), j(ruta),
       j(json_ld(a), ensure_ascii=False),
       j(html_articulo(a), ensure_ascii=False))


def tarjeta(a):
    return ('      <a class="sp-post" href="/blog/%s">\n'
            '        %s\n'
            '        %s\n'
            '        <span class="ind-more i18n" data-es="Leer el artículo &rarr;" data-en="Read the article &rarr;">Leer el artículo &rarr;</span>\n'
            '      </a>' % (a["slug"],
                            i18n("h3", "", a["h1_es"], a["h1_en"], "tarjeta-h3"),
                            i18n("p", "", a["lead_es"], a["lead_en"], "tarjeta-p")))


def main():
    arts = json.load(io.open(FUENTE, encoding="utf-8"))

    # 1) Las paginas
    for a in arts:
        carpeta = os.path.join(APP, "blog", a["slug"])
        os.makedirs(carpeta, exist_ok=True)
        cuerpo = pagina(a)
        # El literal tiene que seguir siendo un string valido y quedar en una
        # sola linea acabada en ";
        m = re.search(r'const HTML = (".*?");\n', cuerpo, re.S)
        if not m:
            raise SystemExit("%s: el literal no cuadra" % a["slug"])
        html = json.loads(m.group(1))
        if html.count("data-es=") != html.count("data-en="):
            raise SystemExit("%s: %d data-es y %d data-en"
                             % (a["slug"], html.count("data-es="), html.count("data-en=")))
        io.open(os.path.join(carpeta, "page.tsx"), "w", encoding="utf-8",
                newline="\n").write(cuerpo)
        print("  %-46s %d pares i18n, %d palabras"
              % ("/blog/" + a["slug"], html.count("data-es="),
                 len(re.sub(r"<[^>]+>", " ", html).split())))

    # 2) El indice: las tarjetas nuevas primero
    ruta_indice = os.path.join(APP, "blog", "page.tsx")
    s = io.open(ruta_indice, encoding="utf-8").read()
    m = re.search(r'const HTML = (".*?");\n', s, re.S)
    indice = json.loads(m.group(1))
    ancla = '<h2 class="sp-h2 i18n" data-es="Artículos" data-en="Articles">Artículos</h2>\n'
    if ancla not in indice:
        raise SystemExit("no encuentro donde insertar las tarjetas")
    nuevas = "\n\n".join(tarjeta(a) for a in arts)
    # Idempotente: primero se quitan las tarjetas de estos slugs si ya estan
    for a in arts:
        indice = re.sub(r'\n?      <a class="sp-post" href="/blog/%s">.*?</a>' % re.escape(a["slug"]),
                        "", indice, flags=re.S)
    indice = indice.replace(ancla, ancla + "\n" + nuevas + "\n", 1)
    if indice.count("data-es=") != indice.count("data-en="):
        raise SystemExit("indice descuadrado: %d data-es, %d data-en"
                         % (indice.count("data-es="), indice.count("data-en=")))
    io.open(ruta_indice, "w", encoding="utf-8", newline="\n").write(
        s[:m.start(1)] + json.dumps(indice, ensure_ascii=False) + s[m.end(1):])
    print("\n  indice: %d tarjetas" % indice.count('class="sp-post"'))
    return 0


if __name__ == "__main__":
    sys.exit(main())
