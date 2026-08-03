# -*- coding: utf-8 -*-
"""Busca contenido que solo se ve si el JavaScript coopera.

Nace de un fallo real: al pulsar "Contacto" en la barra, la seccion aparecia
vacia. La causa no era el enlace sino que los 27 bloques de la portada
nacian en opacity:0 y dependian de que un IntersectionObserver disparase. Si
no disparaba -- salto a un ancla, vuelta atras desde el cache, hidratacion
lenta -- no habia segunda oportunidad y la seccion se quedaba en blanco sin
un solo aviso en la consola.

La regla que comprueba esto es simple de enunciar y dificil de recordar:

    ninguna regla de CSS puede dejar contenido invisible salvo que este
    debajo de un interruptor que solo enciende el propio JavaScript.

Se admite un unico interruptor, html.js-reveal, porque lo pone el mismo
componente que luego revela, y ademas lleva red de seguridad.

    python comprobar-visible.py
"""
import glob
import io
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(BASE, "out")

# El interruptor aceptado: si oculta, tiene que estar detras de esto.
INTERRUPTOR = "html.js-reveal"

# Estados de interfaz que se ocultan a proposito y tienen su pareja visible
# comprobada. No son contenido: nadie se pierde nada si nunca se abren.
# Cada entrada lleva por que, para que anadir una cueste pensarlo.
PERMITIDOS = {
    ".hamburger":
        "solo se ve en movil; .hamburger{display:flex} en <=768px",
    ".hamburger.open span:nth-child(2)":
        "la barra del medio al pasar a aspa",
    ".mobile-menu":
        "menu cerrado; se abre con .mobile-menu.open{display:flex}",
    ".test-anchor":
        "ancla de salto sin contenido: visibility:hidden y alto 0 a proposito",
    ".form-toast":
        "aviso de envio; aparece con .form-toast.show{opacity:1}",
    ".privacy-overlay":
        "modal de privacidad; se abre con .privacy-overlay.open{display:flex}",
}

# Propiedades con las que se puede dejar algo invisible.
OCULTA = re.compile(
    r"(?:^|;|\{)\s*(?:opacity\s*:\s*0(?:\.0*)?\s*(?:;|\}|$)"
    r"|visibility\s*:\s*hidden"
    r"|display\s*:\s*none)", re.I)


def reglas(css):
    """(selector, cuerpo) de cada regla, ignorando lo que hay en @media."""
    fuera, prof, i, ini = [], 0, 0, 0
    sel = ""
    while i < len(css):
        c = css[i]
        if c == "{":
            if prof == 0:
                sel = css[ini:i].strip()
            prof += 1
        elif c == "}":
            prof -= 1
            if prof == 0:
                fuera.append((sel, css[css.index("{", ini) + 1:i]))
                ini = i + 1
        i += 1
    return fuera


def clases_de(selector):
    return set(re.findall(r"\.([A-Za-z0-9_-]+)", selector))


def main():
    hojas = glob.glob(os.path.join(SALIDA, "_next", "static", "**", "*.css"),
                      recursive=True)
    if not hojas:
        raise SystemExit("no hay CSS compilado en out/: lanza antes npm run build")

    paginas = glob.glob(os.path.join(SALIDA, "**", "*.html"), recursive=True)
    if not paginas:
        raise SystemExit("no hay HTML en out/")

    # Clases que aparecen de verdad en el marcado publicado.
    usadas = set()
    for p in paginas:
        s = io.open(p, encoding="utf-8").read()
        for m in re.finditer(r'class="([^"]*)"', s):
            usadas.update(m.group(1).split())

    fallos = []
    for hoja in hojas:
        css = io.open(hoja, encoding="utf-8").read()
        # Se descartan los bloques @media y @keyframes: ocultar en un tamano
        # de pantalla o dentro de una animacion es normal y deliberado.
        css_plano = re.sub(r"@(?:media|keyframes|supports)[^{]*\{(?:[^{}]|\{[^{}]*\})*\}",
                           "", css)
        for selector, cuerpo in reglas(css_plano):
            if not OCULTA.search(cuerpo):
                continue
            if selector.startswith("@"):
                continue
            for parte in selector.split(","):
                parte = parte.strip()
                if not parte or INTERRUPTOR in parte:
                    continue
                # :hover, :focus, ::before y compania esconden estados, no
                # contenido: si el elemento base se ve, no hay perdida.
                if re.search(r"::?(hover|focus|active|before|after|placeholder|"
                             r"backdrop|selection|marker|first-line)", parte):
                    continue
                if parte in PERMITIDOS:
                    continue
                cls = clases_de(parte)
                # Solo importa si esas clases estan puestas en alguna pagina.
                if cls and not (cls & usadas):
                    continue
                fallos.append((os.path.basename(hoja), parte,
                               re.sub(r"\s+", " ", cuerpo.strip())[:70]))

    print("=== CONTENIDO QUE PODRIA QUEDAR INVISIBLE ===")
    if not fallos:
        print("  ninguna regla oculta contenido fuera de %s" % INTERRUPTOR)
        print("  (%d estados de interfaz declarados y comprobados)\n"
              % len(PERMITIDOS))
    else:
        for hoja, sel, cuerpo in fallos:
            print("  %-46s { %s }" % (sel[:46], cuerpo))
        print("\n  %d reglas ocultan sin interruptor de JS.\n" % len(fallos))

    # Segunda comprobacion: el conjunto que oculta el CSS y el que revela el
    # JS tienen que ser el mismo. Si el CSS oculta de mas, sobra invisible.
    enh = io.open(os.path.join(BASE, "src", "components", "site",
                               "LegacyEnhancer.tsx"), encoding="utf-8").read()
    ambito_js = re.search(r'querySelectorAll<HTMLElement>\("([^"]*\.reveal)"\)', enh)
    print("=== AMBITOS ===")
    print("  el JS revela  : %s" % (ambito_js.group(1) if ambito_js else "?"))
    css_todo = "\n".join(io.open(h, encoding="utf-8").read() for h in hojas)
    ambito_css = re.findall(r"html\.js-reveal\s+([^\s{,]+)\s+\.reveal", css_todo)
    print("  el CSS oculta : %s .reveal" % (ambito_css[0] if ambito_css else "?"))
    descuadre = (ambito_js and ambito_css
                 and ambito_css[0] not in ambito_js.group(1))
    if descuadre:
        print("  <-- NO COINCIDEN: lo que oculte de mas queda invisible")

    return 1 if (fallos or descuadre) else 0


if __name__ == "__main__":
    sys.exit(main())
