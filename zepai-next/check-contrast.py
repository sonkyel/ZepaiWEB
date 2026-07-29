# -*- coding: utf-8 -*-
"""Comprueba el contraste WCAG de los textos sobre fondo oscuro.

Es el criterio que decide si el diseño vale, no la impresión visual: el hero
anterior "se veía bien" y tenía la segunda línea del titular en 1,2 sobre las
zonas claras de la escena.

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


# Fondos que puede haber detrás del texto. Ahora que el fondo es nuestro,
# el rango es acotado y conocido: no depende de una escena que se mueve.
FONDOS = {
    "base del hero": hexa("#06050F"),
    "escena a través del velo aclarado (peor caso)": hexa("#594887"),
    "sección #results en oscuro": hexa("#0B0A18"),
}

# (elemento, color, opacidad, ¿texto grande?)
TEXTOS = [
    (".galaxy-title", "#FFFFFF", 1.00, True),
    (".galaxy-title-grad (inicio)", "#F3E8FF", 1.00, True),
    (".galaxy-title-grad (final)", "#C4B5FD", 1.00, True),
    (".galaxy-sub", "#FFFFFF", 0.92, False),
    (".galaxy-trust-label", "#FFFFFF", 0.80, False),
    (".galaxy-channel", "#FFFFFF", 0.94, False),
    (".galaxy-link", "#FFFFFF", 0.94, False),
    (".galaxy-badge", "#EDE4FF", 1.00, False),
    (".galaxy-cta (texto del botón)", "#FFFFFF", 1.00, False),
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


def main() -> int:
    fallos = []
    for nombre_fondo, bg in FONDOS.items():
        print("\n=== sobre %s (#%02X%02X%02X) ===" % (nombre_fondo, *bg))
        print("%-34s %8s %8s" % ("elemento", "ratio", "mínimo"))
        for nombre, col, alpha, grande in TEXTOS:
            # El botón lleva su propio fondo sólido: se mide contra él.
            # el peor caso del boton es su tono MAS claro, no el medio
            fondo = hexa("#7C3AED") if "cta" in nombre else bg
            r = contraste(sobre(hexa(col), alpha, fondo), fondo)
            minimo = AA_GRANDE if grande else AA_NORMAL
            mal = r < minimo
            if mal:
                fallos.append((nombre_fondo, nombre, r, minimo))
            print("%-34s %8.1f %8.1f%s" % (nombre, r, minimo, "  <-- FALLA" if mal else ""))

    print()
    if fallos:
        print("%d FALLOS de contraste:" % len(fallos))
        for f, n, r, m in fallos:
            print("  %-30s %-24s %.1f < %.1f" % (n, f, r, m))
        return 1
    print("TODO CUMPLE WCAG AA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
