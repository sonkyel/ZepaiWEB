# -*- coding: utf-8 -*-
"""Genera public/sitemap.xml a partir de las rutas que existen de verdad.

El anterior estaba escrito a mano y las 16 entradas inglesas salieron mal:

    https://zepaiagency.comsrc/app/en/chatbot-whatsapp

Falta la barra y se colo el camino del fichero. Nadie lo vio porque un
sitemap no rompe nada visible: simplemente Google no indexa esas paginas y
Search Console acumula errores en silencio.

De ahi que esto se genere y no se escriba. La lista sale de src/app, que es
la unica fuente que no puede mentir sobre que rutas existen.

    python generar-sitemap.py
"""
import io
import os
import re
import sys
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(BASE, "src", "app")
URL = "https://zepaiagency.com"
DESTINO = os.path.join(BASE, "public", "sitemap.xml")

# Prioridad por tipo de pagina. Lo legal se indexa pero no compite.
PRIORIDAD = [
    (re.compile(r"^/$"), "1.0", "weekly"),
    (re.compile(r"^/en$"), "0.9", "weekly"),
    (re.compile(r"^/(aviso-legal|politica-)"), "0.3", "yearly"),
    (re.compile(r"^/blog"), "0.7", "weekly"),
    (re.compile(r"^/en/"), "0.6", "monthly"),
    (re.compile(r".*"), "0.8", "monthly"),
]


def rutas():
    """Toda carpeta de src/app con page.tsx, en su URL publica."""
    fuera = ["/"]
    for raiz, _dirs, ficheros in os.walk(APP):
        if "page.tsx" not in ficheros:
            continue
        rel = os.path.relpath(raiz, APP).replace(os.sep, "/")
        if rel == ".":
            continue
        # Rutas privadas de Next: agrupaciones, dinamicas y privadas.
        if any(t.startswith(("_", "(", "[")) for t in rel.split("/")):
            continue
        fuera.append("/" + rel)
    return sorted(set(fuera), key=lambda r: (r.count("/"), r))


def peso(ruta):
    for patron, prio, frec in PRIORIDAD:
        if patron.match(ruta):
            return prio, frec
    return "0.8", "monthly"


def main():
    hoy = date.today().isoformat()
    lineas = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    todas = rutas()
    for r in todas:
        prio, frec = peso(r)
        # La home lleva barra final; el resto no, porque el sitio va con
        # trailingSlash:false y el canonical de cada pagina es sin barra.
        loc = URL + ("/" if r == "/" else r)
        lineas += ["  <url>",
                   "    <loc>%s</loc>" % loc,
                   "    <lastmod>%s</lastmod>" % hoy,
                   "    <changefreq>%s</changefreq>" % frec,
                   "    <priority>%s</priority>" % prio,
                   "  </url>"]
    lineas.append("</urlset>")
    io.open(DESTINO, "w", encoding="utf-8", newline="\n").write("\n".join(lineas) + "\n")

    # Comprobacion: ninguna URL puede tener el dominio pegado a otra cosa ni
    # rastro de la estructura de ficheros. Es exactamente el fallo anterior.
    malas = [l for l in lineas if "<loc>" in l and
             not re.match(r"    <loc>https://zepaiagency\.com(/[a-z0-9/-]*)?</loc>$", l)]
    if malas:
        print("URLS MAL FORMADAS:")
        for m in malas:
            print("  " + m.strip())
        return 1

    print("%d URLs en public/sitemap.xml" % len(todas))
    print("  espanolas %d, inglesas %d"
          % (len([r for r in todas if not r.startswith("/en")]),
             len([r for r in todas if r.startswith("/en")])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
