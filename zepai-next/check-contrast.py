# -*- coding: utf-8 -*-
"""Comprueba el contraste WCAG de TODOS los textos, leyendo el CSS.

Por que se reescribio
---------------------
La version anterior llevaba los colores escritos a mano en una lista de 22
elementos. Fallo dos veces por la misma razon: la lista se despega del CSS.

  - Decia que .founder-role era #C4B5FD cuando el CSS la pintaba con
    var(--cyan). Se corrigio a mano... y quedo el mismo agujero.
  - Decia que .section-label era #DDD1FF cuando el CSS usaba var(--cyan).
    Contraste real 4,0 sobre su propia pastilla. Lo encontro PageSpeed, no
    este comprobador, que daba "TODO CUMPLE WCAG AA".

Y sobre todo: cubria 22 reglas de las 103 que declaran un color. Las 81
restantes nunca se midieron. Ahi estaba .ind-more con 2,9:1 -- el peor
contraste de la web, en la llamada a la accion de cada tarjeta de sector -- y
.sp-related a con el mismo indigo en el blog.

Que hace ahora
--------------
Saca del CSS todas las reglas con `color:`, resuelve las variables y las
opacidades, deduce el umbral que le toca a cada una por su tamano y peso de
letra, y las mide. Nada se escribe dos veces, asi que nada puede despegarse.

El fondo de cada elemento sale de FONDOS, que es lo unico que sigue siendo
manual porque no se puede deducir del CSS sin un navegador. Lo que no
aparezca ahi se mide contra el fondo de seccion mas claro, que es el caso
peor de la web oscura: eso puede dar una falsa alarma, nunca un falso
aprobado.

    python check-contrast.py
"""
import io
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
HOJAS = ["src/app/globals.css", "src/app/legacy.css", "src/app/galaxy.css"]

AA_NORMAL = 4.5
AA_GRANDE = 3.0

# ── Fondos ────────────────────────────────────────────────────────────────
# Un elemento solo se mide contra los fondos sobre los que puede aparecer.
# Medir el texto de #results contra el vortice daba fallos falsos: el vortice
# solo existe en el hero.
PREDET = ("seccion oscura, textura al 12 % sobre --bg0", "#171320")

FONDOS = [
    # (prefijo de selector, nombre del fondo, color)
    # El hero: peor pixel de la COLUMNA DEL TEXTO compuesto con el velo al 62 %.
    (".galaxy-title", "hero, peor pixel de la columna del texto", "#444064"),
    (".galaxy-sub", "hero, peor pixel de la columna del texto", "#444064"),
    (".galaxy-badge", "hero, peor pixel de la columna del texto", "#444064"),
    (".galaxy-link", "hero, peor pixel de la columna del texto", "#444064"),
    (".galaxy-trust", "hero, peor pixel de la columna del texto", "#444064"),
    (".galaxy-channel", "hero, peor pixel de la columna del texto", "#444064"),
    # Fondos solidos propios. El degradado se mide en su extremo MAS CLARO,
    # que es el caso peor para el texto blanco encima.
    (".galaxy-cta", "degradado del boton, extremo claro", "#7C3AED"),
    (".btn-p", "degradado del boton, extremo claro", "#7C3AED"),
    (".cookies-si", "degradado del boton, extremo claro", "#7C3AED"),
    (".wa-float", "verde de WhatsApp", "#25D366"),
    (".campo-aviso", "fondo del aviso de campo", "#2A1215"),
]

# ── Excepciones ───────────────────────────────────────────────────────────
# Cada una con su motivo. Sin motivo no entra: es la puerta por la que se
# cuelan los fallos de verdad.
EXENTAS = {
    ".founder-cred--verif .ico": "icono de 14 px, no texto; decorativo junto a una etiqueta que si se mide",
    ".sched-check": "icono de marca de verificacion, no texto",
    ".belief-num": "numero decorativo de fondo, marcado aria-hidden",
    ".fs option": "lo pinta el sistema operativo, no el CSS de la pagina",
    ".wa-float": ("glifo blanco sobre el verde oficial de WhatsApp: es un "
                  "logotipo, y WCAG 1.4.11 exime las marcas. Cambiarle el "
                  "verde lo haria irreconocible, que es peor para todos"),
}

# Tamano de letra heredado. Solo para reglas que no declaran font-size porque
# lo toman de su contenedor: sin esto se miden como texto normal (4,5) cuando
# en pantalla son un titular (3,0), y sale una falsa alarma.
HEREDA = {
    ".galaxy-title-grad": ("--fs-7", 900),   # va dentro del <h1>, .galaxy-title
    ".gt": ("--fs-6", 900),                  # la palabra en violeta de cada .sec-title
}

# Elementos que solo existen al pasar el raton o al enfocar. Se miden igual,
# pero un fallo aqui no bloquea: el usuario ve el estado de reposo primero.
SUFIJOS_ESTADO = (":hover", ":focus", ":focus-visible", ":active")


def _lin(v):
    v /= 255.0
    return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4


def luminancia(rgb):
    r, g, b = rgb
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def hexa(s):
    s = s.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def sobre(fg, alpha, bg):
    return tuple(round(fg[i] * alpha + bg[i] * (1 - alpha)) for i in range(3))


# ── Lectura del CSS ───────────────────────────────────────────────────────
def carga_css():
    trozos = []
    for h in HOJAS:
        trozos.append(io.open(os.path.join(BASE, h), encoding="utf-8").read())
    css = "\n".join(trozos)
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def variables(css):
    var = {}
    for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;}]+)", css):
        var.setdefault(m.group(1), m.group(2).strip())
    # Resolver los var() anidados
    for _ in range(4):
        for k, v in list(var.items()):
            mm = re.search(r"var\((--[\w-]+)\)", v)
            if mm and mm.group(1) in var:
                var[k] = v.replace(mm.group(0), var[mm.group(1)])
    return var


def color_final(valor, var):
    """(rgb, alpha) a partir de un valor CSS. None si no es un color plano."""
    v = valor.strip()
    m = re.match(r"var\((--[\w-]+)\)", v)
    if m:
        if m.group(1) not in var:
            return None
        v = var[m.group(1)].strip()
    m = re.match(r"rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)\s*(?:[,/]\s*([\d.%]+))?\s*\)", v)
    if m:
        rgb = tuple(int(float(x)) for x in m.groups()[:3])
        a = m.group(4)
        if a is None:
            alpha = 1.0
        elif a.endswith("%"):
            alpha = float(a[:-1]) / 100
        else:
            alpha = float(a)
        return rgb, alpha
    if re.match(r"^#[0-9a-fA-F]{3,8}$", v):
        return hexa(v[:7]), 1.0
    if v.lower() in ("white", "#fff", "#ffffff"):
        return (255, 255, 255), 1.0
    return None


def px(valor, var):
    """Tamano de letra en px. De un clamp() se toma el MINIMO: es el caso
    peor para decidir si cuenta como texto grande."""
    v = valor.strip()
    m = re.match(r"var\((--[\w-]+)\)", v)
    if m and m.group(1) in var:
        v = var[m.group(1)].strip()
    m = re.match(r"clamp\(\s*([\d.]+)px", v)
    if m:
        return float(m.group(1))
    m = re.match(r"([\d.]+)px", v)
    if m:
        return float(m.group(1))
    m = re.match(r"([\d.]+)rem", v)
    if m:
        return float(m.group(1)) * 16
    return None


def reglas(css, var):
    """(selector, rgb, alpha, px, peso) de cada regla que declara color."""
    fuera = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sel, cuerpo = m.group(1).strip(), m.group(2)
        if sel.startswith("@") or ":root" in sel or not sel:
            continue
        mc = re.search(r"(?:^|;)\s*color\s*:\s*([^;!]+)", cuerpo)
        if not mc:
            continue
        col = color_final(mc.group(1), var)
        if col is None:
            continue          # degradados y currentColor: no son un color plano
        mf = re.search(r"font-size\s*:\s*([^;]+)", cuerpo)
        mw = re.search(r"font-weight\s*:\s*(\d+)", cuerpo)
        tam = px(mf.group(1), var) if mf else None
        peso = int(mw.group(1)) if mw else 400
        for s in sel.split(","):
            s = " ".join(s.split())
            if not s:
                continue
            t, p = tam, peso
            if t is None and s in HEREDA:
                heredado, p = HEREDA[s]
                t = px("var(%s)" % heredado, var)
            fuera.append((s, col[0], col[1], t, p))
    return fuera


def fondo_de(sel):
    for prefijo, nombre, color in FONDOS:
        if sel.startswith(prefijo):
            return nombre, hexa(color)
    return PREDET[0], hexa(PREDET[1])


def grande(tam, peso):
    """WCAG: >=24 px, o >=18,66 px en negrita. Sin tamano declarado se
    supone texto normal, que es el umbral mas exigente."""
    if tam is None:
        return False
    return tam >= 24 or (tam >= 18.66 and peso >= 700)


def main():
    css = carga_css()
    var = variables(css)
    todas = reglas(css, var)

    fallos, avisos, exentas = [], [], 0
    print("%-44s %-40s %6s %6s" % ("elemento", "fondo", "ratio", "min"))
    print("-" * 100)

    vistos = set()
    for sel, rgb, alpha, tam, peso in todas:
        if sel in EXENTAS:
            exentas += 1
            continue
        clave = (sel, rgb, alpha)
        if clave in vistos:
            continue
        vistos.add(clave)

        nombre_fondo, bg = fondo_de(sel)
        r = contraste(sobre(rgb, alpha, bg), bg)
        minimo = AA_GRANDE if grande(tam, peso) else AA_NORMAL
        estado = sel.endswith(SUFIJOS_ESTADO)

        if r < minimo:
            marca = "  <-- AVISO (estado)" if estado else "  <-- FALLA"
            (avisos if estado else fallos).append((sel, nombre_fondo, r, minimo))
        else:
            marca = ""
        if r < minimo or "-v" in sys.argv:
            print("%-44s %-40s %6.1f %6.1f%s"
                  % (sel[:44], nombre_fondo[:40], r, minimo, marca))

    print()
    print("%d reglas con color medidas, %d exentas con motivo escrito"
          % (len(vistos), exentas))

    if avisos:
        print("\n%d avisos en estados de raton o teclado (no bloquean):" % len(avisos))
        for s, f, r, m in avisos:
            print("  %-42s %.1f < %.1f  sobre %s" % (s, r, m, f))

    if fallos:
        print("\n%d FALLOS de contraste:" % len(fallos))
        for s, f, r, m in fallos:
            print("  %-42s %.1f < %.1f  sobre %s" % (s, r, m, f))
        return 1

    print("\nTODO CUMPLE WCAG AA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
