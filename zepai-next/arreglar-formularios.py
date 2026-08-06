# -*- coding: utf-8 -*-
"""Asocia cada <label> del formulario con su control.

PageSpeed senalo un solo fallo -- <select id="sbiz"> sin nombre accesible --
pero al mirarlo resulto que NINGUNA de las 13 etiquetas del formulario tiene
el atributo for. Los <input> se libraban del aviso porque el placeholder les
da un nombre de repuesto; el <select> no tiene placeholder, asi que se quedo
sin nombre y lo canto.

Arreglar solo el select habria subido la puntuacion dejando el problema de
fondo intacto: quien navega con lector de pantalla oye "cuadro de edicion"
en cada campo. Se asocian los trece.

Las dos etiquetas .consent-check no se tocan: envuelven su casilla, que es
una asociacion implicita y valida.

    python arreglar-formularios.py
"""
import importlib.util
import io
import json
import os
import re
import sys

# El modulo se llama editar-home.py, con guion: no es un identificador valido
# de Python, asi que no se puede importar con "import".
_spec = importlib.util.spec_from_file_location(
    "editar_home",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "editar-home.py"))
_eh = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_eh)
Home, esc = _eh.Home, _eh.esc

# <label class="fl ...">texto</label> seguido del control al que describe
PAR = re.compile(
    r'(<label class="fl[^>]*>.*?</label>)(\s*)'
    r'(<(?:input|select|textarea)\b[^>]*?id="([^"]+)"[^>]*>)', re.S)


def pares(html):
    for m in PAR.finditer(html):
        etiqueta, hueco, control, ident = m.groups()
        if 'for=' in etiqueta:
            continue
        nueva = etiqueta.replace('<label class="fl',
                                 '<label for="%s" class="fl' % ident, 1)
        yield m.group(0), nueva + hueco + control, ident


def main(ruta="src/app/page.tsx"):
    h = Home(ruta) if ruta != "src/app/page.tsx" else Home()
    html = json.loads('"' + h.html + '"')

    cambios = list(pares(html))
    if not cambios:
        print("  nada que hacer en %s" % ruta)
        return 0

    for viejo, nuevo, ident in cambios:
        h.cambia(esc(viejo), esc(nuevo), veces=1, nota="for=%s" % ident)

    h.guarda()

    # Comprobacion final sobre el resultado escrito, no sobre lo que creemos
    # haber escrito: cada control visible con id tiene que tener su etiqueta.
    s = io.open(h.ruta, encoding="utf-8").read()
    final = json.loads(re.search(r'const HTML = (".*?");\n', s, re.S).group(1))
    huerfanos = []
    for m in re.finditer(r'<(input|select|textarea)\b([^>]*)>', final):
        attrs = m.group(2)
        mid = re.search(r'id="([^"]+)"', attrs)
        if not mid or 'type="hidden"' in attrs:
            continue
        if 'for="%s"' % mid.group(1) not in final:
            huerfanos.append(mid.group(1))
    if huerfanos:
        raise SystemExit("SIGUEN SIN ETIQUETA: " + ", ".join(huerfanos))
    print("  %d controles visibles, todos con etiqueta asociada"
          % len(re.findall(r'<label for="', final)))
    return len(cambios)


if __name__ == "__main__":
    main(*sys.argv[1:])
