# -*- coding: utf-8 -*-
"""Nebulosa de neon: el efecto ASCII de 21st.dev, renderizado a imagen.

Por que un fotograma y no el efecto vivo: a 1920x1080 con celdas de 16 px
son 8.160 celdas por cuadro, y encima los post-efectos son pasadas a
pantalla completa -- solo el grano son 2 millones de pixeles de ruido por
cuadro. Eso es un nucleo al 100 % permanente, un movil caliente, y un fondo
cuyo brillo cambia cada cuadro, con lo que el contraste del texto deja de
ser medible. Renderizado una vez, el aspecto es el mismo y cuesta cero.

Se implementa la receta entera con PIL y numpy, que es una API rasterizada
2D equivalente a Canvas2D y no necesita compilar nada:

  1. Degradado radial animado, con onda y distorsion.
  2. Rejilla de celdas y color medio de cada una.
  3. Una estrella por celda, con tamano y color segun la luminancia.
  4. Brillo, contraste y saturacion.
  5. Post-efectos: scanlines, vineta, bloom, grano, semitonos y pixelado.

    python nebulosa.py
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# ── Parametros, tal cual vienen de la herramienta ────────────────────
ANCHO, ALTO = 1600, 900
CELDA = 16
COBERTURA = 100
BRILLO, CONTRASTE, SATURACION = 12, 115, 100
BG_BLUR, BG_OPACIDAD = 12, 90

GRAD = dict(centro=(0.46, 0.52), escala=0.88, suavidad=0.26,
            onda=0.12, distorsion=0.28, motion=0.86, velocidad=0.50)
# El nucleo va rebajado respecto al preset: #E9CCFF es casi blanco y, con
# el bloom encima, deja una mancha sobre la que no se puede poner texto.
PARADAS = [(0.00, (0xB9, 0x92, 0xE8)),   # Mauve, apagado
           (0.33, (0x8A, 0x2B, 0xE2)),   # Violet
           (0.67, (0x24, 0x00, 0x46)),   # Midnight
           (1.00, (0x03, 0x00, 0x0A))]   # Ink

PFX = dict(scanLines=40, vignette=38, bloom=25, filmGrain=30,
           halftone=20, pixelate=15)

# El fotograma que se congela. La animacion es "wave" y se mueve con el
# tiempo; este valor solo elige en que punto de la onda se para.
T = 0.35


# ── 1. Degradado radial animado ──────────────────────────────────────
def degradado(w, h, t):
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    x = xs / w
    y = ys / h
    cx, cy = GRAD['centro']

    # Deformacion del dominio con varias frecuencias. Con una sola sinusoide
    # el suavizado posterior se la come y queda un circulo limpio; con tres
    # octavas aparecen los brazos y los huecos de una nebulosa.
    fase = t * GRAD['velocidad'] * 6.2831
    amp = GRAD['onda'] * GRAD['motion'] * 3.2
    wx = (np.sin(y * 5.1 + fase) * 0.60 +
          np.sin(y * 11.3 - fase * 1.7) * 0.28 +
          np.sin(y * 23.0 + fase * 0.4) * 0.12)
    wy = (np.cos(x * 4.3 - fase * 0.7) * 0.60 +
          np.cos(x * 9.7 + fase * 1.3) * 0.28 +
          np.cos(x * 19.1 - fase * 0.9) * 0.12)
    x = x + amp * 0.18 * wx
    y = y + amp * 0.18 * wy

    dx = (x - cx) * (w / float(h))     # circular en pantalla ancha
    dy = y - cy
    d = np.sqrt(dx * dx + dy * dy) / GRAD['escala']

    # La distorsion modula el radio segun el angulo: brazos, no anillos.
    ang = np.arctan2(dy, dx)
    d = d * (1 + GRAD['distorsion'] * 0.55 * (
        np.sin(ang * 3.0 + fase * 0.8) * 0.6 +
        np.sin(ang * 7.0 - fase * 0.5) * 0.4))

    # La suavidad aplana la rampa cerca del centro
    d = np.clip(d, 0, 1)
    s = GRAD['suavidad']
    d = d * (1 - s) + (d ** 0.75) * s

    salida = np.zeros((h, w, 3), np.float32)
    for i in range(len(PARADAS) - 1):
        p0, c0 = PARADAS[i]
        p1, c1 = PARADAS[i + 1]
        m = (d >= p0) & (d <= p1)
        k = np.zeros_like(d)
        k[m] = (d[m] - p0) / (p1 - p0)
        k = k * k * (3 - 2 * k)                    # suavizado de Hermite
        for c in range(3):
            salida[..., c][m] = c0[c] + (c1[c] - c0[c]) * k[m]
    return salida


# ── 2 y 3. Rejilla, muestreo y estrellas ─────────────────────────────
def estrellas(fuente):
    h, w, _ = fuente.shape
    cols, filas = w // CELDA, h // CELDA
    # La media por celda es exactamente un redimensionado con filtro caja
    medias = np.asarray(
        Image.fromarray(fuente.astype(np.uint8)).resize((cols, filas), Image.BOX),
        dtype=np.float32)
    lum = (0.2126 * medias[..., 0] + 0.7152 * medias[..., 1] +
           0.0722 * medias[..., 2]) / 255.0

    lienzo = Image.new('RGB', (w, h), (0, 0, 0))
    d = ImageDraw.Draw(lienzo)
    rng = np.random.default_rng(1)
    dibujadas = 0

    for fy in range(filas):
        for fx in range(cols):
            l = float(lum[fy, fx])
            if l < 0.04:
                continue
            if COBERTURA < 100 and rng.random() * 100 > COBERTURA:
                continue
            cxp = fx * CELDA + CELDA / 2.0
            cyp = fy * CELDA + CELDA / 2.0
            r = (CELDA / 2.0) * (0.35 + 0.65 * l)
            col = tuple(int(min(255, v * (0.55 + 0.75 * l))) for v in medias[fy, fx])
            d.polygon(estrella(cxp, cyp, r, r * 0.42), fill=col)
            dibujadas += 1
    return lienzo, dibujadas, cols * filas


def estrella(cx, cy, r, ri, puntas=5, giro=-np.pi / 2):
    pts = []
    for i in range(puntas * 2):
        rad = r if i % 2 == 0 else ri
        a = giro + i * np.pi / puntas
        pts.append((cx + rad * np.cos(a), cy + rad * np.sin(a)))
    return pts


# ── 4. Ajustes de color ──────────────────────────────────────────────
def color(img):
    a = np.asarray(img, np.float32)
    a = a + (BRILLO / 100.0) * 255 * 0.35
    a = (a - 128) * (CONTRASTE / 100.0) + 128
    if SATURACION != 100:
        g = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[..., None]
        a = g + (a - g) * (SATURACION / 100.0)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


# ── 5. Post-efectos, en el orden de la receta ────────────────────────
def scanlines(img, k):
    a = np.asarray(img, np.float32)
    lineas = (np.arange(a.shape[0]) % 3 == 0)[:, None, None]
    return Image.fromarray(np.clip(a * np.where(lineas, 1 - 0.55 * k, 1), 0, 255).astype(np.uint8))


def vineta(img, k):
    h, w = img.size[1], img.size[0]
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xs / w - .5) * 2) ** 2 + ((ys / h - .5) * 2) ** 2) / np.sqrt(2)
    m = np.clip(1 - k * np.clip(d - 0.30, 0, None) ** 1.5 * 2.6, 0, 1)[..., None]
    return Image.fromarray(np.clip(np.asarray(img, np.float32) * m, 0, 255).astype(np.uint8))


def bloom(img, k):
    brillo = np.asarray(img, np.float32)
    umbral = np.clip(brillo - 150, 0, None)
    halo = Image.fromarray(umbral.astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))
    return Image.fromarray(np.clip(brillo + np.asarray(halo, np.float32) * (1.6 * k), 0, 255).astype(np.uint8))


def grano(img, k):
    a = np.asarray(img, np.float32)
    rng = np.random.default_rng(1)
    ruido = rng.normal(0, 255 * 0.09 * k, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a + ruido, 0, 255).astype(np.uint8))


def semitonos(img, k):
    """Rejilla de puntos girada 45 grados, mezclada segun la intensidad."""
    w, h = img.size
    capa = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(capa)
    paso = 6
    gris = np.asarray(img.convert('L'), np.float32) / 255.0
    for y in range(0, h, paso):
        for x in range(0, w, paso):
            despl = (paso // 2) if (y // paso) % 2 else 0
            px, py = min(w - 1, x + despl), y
            r = paso * 0.55 * float(gris[py, px])
            if r > 0.4:
                d.ellipse([px - r, py - r, px + r, py + r], fill=255)
    m = np.asarray(capa, np.float32)[..., None] / 255.0
    a = np.asarray(img, np.float32)
    return Image.fromarray(np.clip(a * (1 - k) + a * m * k * 1.35, 0, 255).astype(np.uint8))


def pixelar(img, k):
    w, h = img.size
    bloque = max(2, int(2 + 6 * k))
    return img.resize((w // bloque, h // bloque), Image.BOX).resize((w, h), Image.NEAREST)


# ── Montaje ──────────────────────────────────────────────────────────
def main():
    fuente = degradado(ANCHO, ALTO, T)

    # Fondo: el propio degradado desenfocado, al 90 %
    fondo = Image.fromarray(fuente.astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(BG_BLUR))
    fondo = Image.blend(Image.new('RGB', (ANCHO, ALTO), (0, 0, 0)),
                        fondo, BG_OPACIDAD / 100.0)

    capa, dibujadas, total = estrellas(fuente)
    img = Image.fromarray(np.clip(
        np.asarray(fondo, np.float32) + np.asarray(capa, np.float32), 0, 255).astype(np.uint8))

    img = color(img)
    img = scanlines(img, PFX['scanLines'] / 100.0)
    img = vineta(img, PFX['vignette'] / 100.0)
    img = bloom(img, PFX['bloom'] / 100.0)
    img = grano(img, PFX['filmGrain'] / 100.0)
    img = semitonos(img, PFX['halftone'] / 100.0)
    img = pixelar(img, PFX['pixelate'] / 100.0)

    os.makedirs('public/fondos', exist_ok=True)
    img.save('public/fondos/nebulosa.webp', 'WEBP', quality=82, method=6)
    img.save('_fuentes/nebulosa-completa.png')
    print('celdas dibujadas: %d de %d' % (dibujadas, total))
    print('salida: %s  %.0f KB' % (img.size, os.path.getsize('public/fondos/nebulosa.webp') / 1024))


if __name__ == '__main__':
    main()
