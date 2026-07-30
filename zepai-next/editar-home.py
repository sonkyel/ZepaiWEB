# -*- coding: utf-8 -*-
"""Edicion segura del HTML de la home.

El marcado de la home es una constante `HTML` dentro de page.tsx: una sola
linea de 72 KB con las comillas escapadas. Editarla con expresiones
regulares ya rompio la nav y el pie en esta sesion, y un validador laxo dijo
"TODO OK" dos veces con la web visiblemente rota.

De ahi este modulo. Toda edicion pasa por aqui y por las mismas
comprobaciones:

  - el texto a sustituir aparece EXACTAMENTE el numero de veces esperado;
  - el literal sigue siendo un string valido despues (se valida con
    json.loads: el escapado de JS que usa este fichero -- \\" y \\n -- es
    compatible con JSON);
  - el balance de <div>, <section> y <svg> cambia justo lo previsto;
  - hay tantos data-es como data-en (los dos idiomas siguen emparejados).

Uso:

    from editar_home import Home
    h = Home()
    h.cambia('<div class=\\"x\\">', '<div class=\\"y\\">')
    h.guarda(divs=0, svgs=-2)      # deltas esperados
"""
import io
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
RUTA = os.path.join(BASE, "src", "app", "page.tsx")


def esc(html):
    """Convierte HTML legible al escapado que lleva el literal.

    Escribir a mano \\" y \\n dentro de un string de Python es exactamente la
    fuente de errores que este modulo existe para evitar: json.dumps hace la
    misma conversion que necesita el literal y no se equivoca.

        esc('<div class="x">\\n  hola\\n</div>')  ->  '<div class=\\"x\\">\\n  hola\\n</div>'
    """
    return json.dumps(html, ensure_ascii=False)[1:-1]


def _contar(s):
    return {
        "div": len(re.findall(r"<div\b", s)),
        "/div": s.count("</div>"),
        "section": len(re.findall(r"<section\b", s)),
        "/section": s.count("</section>"),
        "svg": len(re.findall(r"<svg\b", s)),
        "/svg": s.count("</svg>"),
        "data-es": s.count("data-es="),
        "data-en": s.count("data-en="),
    }


class Home(object):
    def __init__(self, ruta=RUTA):
        self.ruta = ruta
        self.s = io.open(ruta, encoding="utf-8").read()
        # inicio apunta a la comilla de apertura; fin, a la de cierre. Las dos
        # se calculan siempre con este metodo: cuando cambia() lo hacia de otra
        # forma, una de las dos se colaba dentro del corte y json.loads fallaba
        # con un error que no tenia nada que ver.
        self.inicio = self.s.index('const HTML = "') + len('const HTML = ')
        self.fin = self._fin()
        self.antes = _contar(self.html)
        self.cambios = []

    def _fin(self):
        fin = self.s.index("\n", self.inicio)
        assert self.s[fin - 2:fin] == '";', repr(self.s[fin - 8:fin])
        return fin - 2

    @property
    def html(self):
        """El contenido, sin las comillas que lo envuelven."""
        return self.s[self.inicio + 1:self.fin]

    def cambia(self, viejo, nuevo, veces=1, nota=""):
        n = self.html.count(viejo)
        if n != veces:
            raise SystemExit("esperaba %d de %r y hay %d" % (veces, viejo[:80], n))
        self.s = (self.s[:self.inicio + 1] + self.html.replace(viejo, nuevo)
                  + self.s[self.fin:])
        self.fin = self._fin()
        self.cambios.append(nota or (viejo[:56] + " -> " + nuevo[:40]))
        return self

    def guarda(self, **deltas):
        # 1) el literal sigue siendo un string valido, comillas incluidas
        json.loads(self.s[self.inicio:self.fin + 1])

        # 2) las etiquetas cuadran
        ahora = _contar(self.html)
        fallos = []
        for clave, antes in self.antes.items():
            esperado = antes + deltas.get(clave.replace("/", "cierre_"), deltas.get(clave, 0))
            if ahora[clave] != esperado:
                fallos.append("%s: %d -> %d (esperaba %d)" % (clave, antes, ahora[clave], esperado))
        if ahora["div"] != ahora["/div"]:
            fallos.append("div sin cerrar: %d abren, %d cierran" % (ahora["div"], ahora["/div"]))
        if ahora["section"] != ahora["/section"]:
            fallos.append("section sin cerrar: %d abren, %d cierran" % (ahora["section"], ahora["/section"]))
        if ahora["data-es"] != ahora["data-en"]:
            fallos.append("i18n descuadrado: %d data-es, %d data-en" % (ahora["data-es"], ahora["data-en"]))
        if fallos:
            raise SystemExit("NO SE GUARDA:\n  " + "\n  ".join(fallos))

        io.open(self.ruta, "w", encoding="utf-8", newline="\n").write(self.s)
        for c in self.cambios:
            print("  " + c)
        print("OK  div %d  section %d  svg %d  i18n %d pares" % (
            ahora["div"], ahora["section"], ahora["svg"], ahora["data-es"]))
