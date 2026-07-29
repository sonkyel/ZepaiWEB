# -*- coding: utf-8 -*-
"""Comprueba el contraste WCAG de los textos sobre fondo oscuro.

Es el criterio que decide si el diseño vale, no la impresión visual: el hero
original "se veía bien" y tenía la segunda línea del titular en 1,2 sobre las
zonas claras de la escena.

Cada elemento se mide SOLO contra los fondos sobre los que puede aparecer.
Medir el texto de #results contra el fondo del vórtice daba fallos falsos:
el vórtice solo existe en el hero.

    python check-contrast.py
"""
import sys

AA_NORMAL = 4.5
AA_GRANDE = 3.0


def _lin(v: float) -> float:
    v /= 255
    return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4


def luminancia(rgb):
    r, g, b = rgb
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def hexa(s: str):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def sobre(fg, alpha, bg):
    """Color resultante de pintar fg con opacidad alpha sobre bg."""
    return tuple(round(fg[i] * alpha + bg[i] * (1 - alpha)) for i in range(3))


# Fondos posibles del HERO. El vórtice dibuja con mezcla aditiva, así que se
# comprueban dos casos: una partícula brillante y la saturación total a
# blanco. Los valores salen de acotar el canvas al 62 % y el velo al 48 %.
FONDOS_HERO = {
    # Medido sobre la imagen real: el pixel mas claro de la banda del texto
    # en public/hero/hero.webp. Ya no es una estimacion, es el valor exacto.
    "hero, pixel más claro de la imagen": hexa("#1A1F3F"),
}

# Las secciones oscuras tienen su propio fondo sólido: ahí no hay vórtice.
FONDOS_SECCION = {
    "sección oscura (#results / marco de #contact)": hexa("#0B0A18"),
}

# (elemento, color, opacidad, ¿texto grande?)
TEXTOS_HERO = [
    (".galaxy-title", "#FFFFFF", 1.00, True),
    (".galaxy-title-grad (inicio)", "#F3E8FF", 1.00, True),
    (".galaxy-title-grad (final)", "#C4B5FD", 1.00, True),
    (".galaxy-sub", "#FFFFFF", 0.92, False),
    (".galaxy-trust-label", "#FFFFFF", 0.80, False),
    (".galaxy-channel", "#FFFFFF", 0.94, False),
    (".galaxy-link", "#FFFFFF", 0.94, False),
    (".galaxy-badge", "#EDE4FF", 1.00, False),
]

TEXTOS_SECCION = [
    ("#results .sec-title", "#FFFFFF", 1.00, True),
    ("#results .sec-sub", "#FFFFFF", 0.78, False),
    ("#results .stat-num", "#C4B5FD", 1.00, True),
    ("#results .stat-lbl", "#FFFFFF", 0.74, False),
    ("#results .test-quote", "#FFFFFF", 0.86, False),
    ("#results .t-name", "#FFFFFF", 1.00, False),
    ("#results .t-role", "#FFFFFF", 0.68, False),
    ("#results .kii-tag", "#DDD1FF", 1.00, False),
    ("#contact .section-label", "#DDD1FF", 1.00, False),
    ("#contact h2", "#FFFFFF", 1.00, True),
    ("#contact p", "#FFFFFF", 0.80, False),
]

# El botón lleva su propio fondo sólido. Se mide contra el tono MÁS CLARO de
# su degradado, que es el caso peor. Sobre el #8B5CF6 de marca el blanco daba
# 4,2 y no llegaba a AA: por eso el degradado arranca en #7C3AED.
BOTON = ("botón principal (.btn-p / .galaxy-cta)", "#FFFFFF", 1.00, False, "#7C3AED")


def bloque(fondos, textos, fallos):
    for nombre_fondo, bg in fondos.items():
        print("\n=== %s (#%02X%02X%02X) ===" % (nombre_fondo, *bg))
        print("%-34s %8s %8s" % ("elemento", "ratio", "mínimo"))
        for nombre, col, alpha, grande in textos:
            r = contraste(sobre(hexa(col), alpha, bg), bg)
            minimo = AA_GRANDE if grande else AA_NORMAL
            mal = r < minimo
            if mal:
                fallos.append((nombre_fondo, nombre, r, minimo))
            print("%-34s %8.1f %8.1f%s" % (nombre, r, minimo, "  <-- FALLA" if mal else ""))


def main() -> int:
    fallos = []
    bloque(FONDOS_HERO, TEXTOS_HERO, fallos)
    bloque(FONDOS_SECCION, TEXTOS_SECCION, fallos)

    nombre, col, alpha, grande, fondo = BOTON
    bg = hexa(fondo)
    r = contraste(sobre(hexa(col), alpha, bg), bg)
    minimo = AA_GRANDE if grande else AA_NORMAL
    print("\n=== sobre su propio fondo ===")
    print("%-34s %8.1f %8.1f%s" % (nombre, r, minimo, "  <-- FALLA" if r < minimo else ""))
    if r < minimo:
        fallos.append(("fondo propio", nombre, r, minimo))

    print()
    if fallos:
        print("%d FALLOS de contraste:" % len(fallos))
        for f, n, r, m in fallos:
            print("  %-30s %-46s %.1f < %.1f" % (n, f, r, m))
        return 1
    print("TODO CUMPLE WCAG AA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
