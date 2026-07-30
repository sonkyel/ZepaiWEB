# -*- coding: utf-8 -*-
"""Mide el CSS con numeros en vez de impresiones.

Dos cosas:
  1) Que selectores no los usa nadie. El CSS arrastra el hero antiguo, un
     splash, una seccion #schedule que no existe y un cursor-glow que
     legacy-home.js busca y recibe null.
  2) El censo de tamanos de fuente, radios, espaciados y !important, que es
     lo que dice si el sistema es un sistema.

    python auditar-css.py            -> informe
    python auditar-css.py --json     -> para comparar antes y despues
"""
import io
import json
import os
import re
import sys
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
CSS = ["src/app/legacy.css", "src/app/galaxy.css", "src/app/globals.css"]
# Donde puede aparecer una clase o un id: el JSX, el string HTML de la home
# y el JS heredado que anade clases a mano.
FUENTES = ["src", "public/legacy-home.js"]


def leer(ruta):
    return io.open(os.path.join(BASE, ruta), encoding="utf-8").read()


def marcado():
    """Todo el texto donde un selector podria estar usado."""
    trozos = []
    for f in FUENTES:
        p = os.path.join(BASE, f)
        if os.path.isfile(p):
            trozos.append(leer(f))
            continue
        for raiz, _, nombres in os.walk(p):
            for n in nombres:
                if n.endswith((".tsx", ".ts", ".js", ".jsx", ".html")):
                    rel = os.path.relpath(os.path.join(raiz, n), BASE)
                    trozos.append(leer(rel.replace("\\", "/")))
    return "\n".join(trozos)


def sin_comentarios(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def bloques(css):
    """(selector, cuerpo) de cada regla, entrando en las @media."""
    css = sin_comentarios(css)
    fuera = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sel, cuerpo = m.group(1).strip(), m.group(2)
        if sel.startswith("@"):
            continue
        fuera.append((sel, cuerpo))
    return fuera


def usado(nombre, html):
    """El nombre aparece como palabra completa (ni prefijo ni sufijo).

    'how' no debe darse por vivo porque exista 'how-more', y 'srv-grid' debe
    darse por vivo aunque venga pegado a una barra invertida.
    """
    return re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(nombre), html) is not None


def nombres_de(sel):
    """Clases e ids que menciona un selector, sin pseudos ni combinadores."""
    clases = set(re.findall(r"\.([A-Za-z0-9_-]+)", sel))
    ids = set(re.findall(r"#([A-Za-z0-9_-]+)", sel))
    return clases, ids


def main():
    html = marcado()
    todo_css = "\n".join(leer(c) for c in CSS)

    # --- 1) selectores muertos ---------------------------------------
    vivos, muertos = 0, []
    vistos = set()
    for ruta in CSS:
        for sel, _ in bloques(leer(ruta)):
            for parte in sel.split(","):
                parte = parte.strip()
                if not parte or parte in vistos:
                    continue
                vistos.add(parte)
                clases, ids = nombres_de(parte)
                if not clases and not ids:
                    continue  # selectores de elemento: siempre "vivos"
                # Frontera por caracter de nombre, no por comilla: en el
                # string HTML de la home las comillas van escapadas
                # (class=\"srv-grid\"), asi que el caracter de al lado es una
                # barra invertida. Buscar comillas daba 196 falsos muertos.
                falta = [n for n in (clases | ids) if not usado(n, html)]
                if falta:
                    muertos.append((ruta, parte, sorted(set(falta))))
                else:
                    vivos += 1

    # --- 2) censo ----------------------------------------------------
    css = sin_comentarios(todo_css)
    fuentes = Counter(m.strip() for m in re.findall(r"font-size\s*:\s*([^;}]+)", css))
    radios = Counter(m.strip() for m in re.findall(r"border-radius\s*:\s*([^;}]+)", css))
    huecos = Counter(m.strip() for m in re.findall(r"[^-]gap\s*:\s*([^;}]+)", css))
    margenes = Counter(m.strip() for m in re.findall(r"margin-bottom\s*:\s*([^;}]+)", css))
    sombras = len(re.findall(r"box-shadow\s*:", css))
    importantes = len(re.findall(r"!important", css))
    keyframes = re.findall(r"@keyframes\s+([A-Za-z0-9_-]+)", css)
    # Un keyframes esta vivo si lo nombra un animation del CSS O del marcado:
    # los robots de seccion llevan style="animation:rb-float 5s ..." incrustado
    # en el string HTML de la home. Mirar solo el CSS daba 12 falsos muertos.
    animaciones = " ".join(re.findall(r"animation[^;}\"]*", css + " " + html))
    kf_muertos = [k for k in keyframes if not re.search(r"\b%s\b" % re.escape(k), animaciones)]
    tokens_muertos = [t for t in re.findall(r"(--[a-z0-9-]+)\s*:", css)
                      if css.count("var(%s)" % t) == 0]

    datos = {
        "selectores_vivos": vivos,
        "selectores_muertos": len(muertos),
        "font_size_declaraciones": sum(fuentes.values()),
        "font_size_valores": len(fuentes),
        "border_radius_declaraciones": sum(radios.values()),
        "border_radius_valores": len(radios),
        "gap_valores": len(huecos),
        "margin_bottom_valores": len(margenes),
        "box_shadow": sombras,
        "importantes": importantes,
        "keyframes": len(keyframes),
        "keyframes_muertos": sorted(kf_muertos),
        "tokens_sin_usar": sorted(tokens_muertos),
    }

    if "--json" in sys.argv:
        print(json.dumps(datos, indent=1, ensure_ascii=False))
        return

    print("=== SELECTORES ===")
    print("  vivos   %d" % vivos)
    print("  muertos %d" % len(muertos))
    for ruta, sel, falta in muertos:
        print("    %-18s %-46s (falta: %s)" % (os.path.basename(ruta), sel[:46], ", ".join(falta)))

    print("\n=== CENSO ===")
    print("  font-size      %3d declaraciones, %2d valores distintos" % (sum(fuentes.values()), len(fuentes)))
    print("  border-radius  %3d declaraciones, %2d valores distintos" % (sum(radios.values()), len(radios)))
    print("  gap            %3d declaraciones, %2d valores distintos" % (sum(huecos.values()), len(huecos)))
    print("  margin-bottom  %3d declaraciones, %2d valores distintos" % (sum(margenes.values()), len(margenes)))
    print("  box-shadow     %3d" % sombras)
    print("  !important     %3d" % importantes)
    print("  @keyframes     %3d (%d sin usar: %s)" % (len(keyframes), len(kf_muertos), ", ".join(sorted(kf_muertos)) or "-"))
    print("  tokens sin usar: %s" % (", ".join(sorted(tokens_muertos)) or "-"))


if __name__ == "__main__":
    main()
