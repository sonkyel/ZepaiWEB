# -*- coding: utf-8 -*-
"""Recorta la mascota sobre fondo transparente.

El generador ignoro "fondo transparente" y pinto el damero de cuadros que
los editores usan PARA REPRESENTAR transparencia. Es un fallo habitual, y
quitarlo tiene mas miga de la que parece.

Lo que NO funciono, por si se vuelve a intentar:

  - "Borra todo lo gris". Deja un fleco dentado en el contorno: las casillas
    oscuras pegadas al robot estan TENIDAS por su luz violeta -- valores
    tipo (45,36,65), con saturacion de 22 a 45 -- asi que dejan de ser gris
    neutro y sobreviven.
  - Reconstruir la rejilla del damero y comparar cada pixel con el color que
    le tocaria. La fase no es uniforme y sobrevivian columnas enteras.
  - Difuminar el borde. Emborrona el fleco, no lo quita.

Lo que si funciona, y es lo que hace este script:

  1. Dos ramas para detectar el fondo: gris claro y neutro, u oscuro con
     mucho mas margen de tinte. Se puede ser permisivo con los oscuros
     porque la propagacion solo entra desde el borde de la imagen: las
     sombras del interior del robot no se tocan nunca.
  2. Propagacion en 8 direcciones desde los cuatro lados.
  3. Quedarse solo con la isla mas grande, que descarta las motas sueltas.
  4. Contraer la mascara 1 px, que es donde vive la corona de mezcla entre
     robot y fondo.

Y se comprueba el alfa por programa, no mirando: el visor de imagenes dibuja
su propio damero y hace creer que el recorte fallo cuando esta bien.

    python recortar-robot.py
"""
import os
from collections import deque

from PIL import Image, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(BASE, "_fuentes", "robot", "B-brazos-cruzados.png")
DESTINO = os.path.join(BASE, "public", "hero", "robot.webp")
ANCHO = 400


def es_fondo(c):
    r, g, b = c
    alto, sat = max(r, g, b), max(r, g, b) - min(r, g, b)
    if alto <= 175 and sat <= 20:
        return True                       # damero limpio, sus dos tonos
    return alto <= 100 and sat <= 48      # damero oscuro tenido de violeta


def mascara(im):
    w, h = im.size
    px = im.load()
    fondo = bytearray(w * h)
    cola = deque()

    def sembrar(x, y):
        if not fondo[y * w + x] and es_fondo(px[x, y]):
            fondo[y * w + x] = 1
            cola.append((x, y))

    for x in range(w):
        sembrar(x, 0)
        sembrar(x, h - 1)
    for y in range(h):
        sembrar(0, y)
        sembrar(w - 1, y)

    vecinos = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
    while cola:
        x, y = cola.popleft()
        for dx, dy in vecinos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not fondo[ny * w + nx] and es_fondo(px[nx, ny]):
                fondo[ny * w + nx] = 1
                cola.append((nx, ny))

    # Solo la isla mas grande de lo que no es fondo: fuera las motas
    visto = bytearray(w * h)
    mayor, isla_mayor = 0, []
    for sy in range(0, h, 3):
        for sx in range(0, w, 3):
            if fondo[sy * w + sx] or visto[sy * w + sx]:
                continue
            visto[sy * w + sx] = 1
            cola, isla = deque([(sx, sy)]), []
            while cola:
                x, y = cola.popleft()
                isla.append((x, y))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    j = ny * w + nx
                    if 0 <= nx < w and 0 <= ny < h and not fondo[j] and not visto[j]:
                        visto[j] = 1
                        cola.append((nx, ny))
            if len(isla) > mayor:
                mayor, isla_mayor = len(isla), isla

    m = bytearray(w * h)
    for x, y in isla_mayor:
        m[y * w + x] = 255
    a = Image.frombytes("L", (w, h), bytes(m))
    a = a.filter(ImageFilter.MinFilter(3))      # contraer 1 px
    return a.filter(ImageFilter.GaussianBlur(0.5)), mayor / float(w * h)


def main():
    im = Image.open(ORIGEN).convert("RGB")
    alpha, cobertura = mascara(im)
    out = im.convert("RGBA")
    out.putalpha(alpha)
    out = out.crop(out.getbbox())
    out = out.resize((ANCHO, round(ANCHO * out.size[1] / out.size[0])), Image.LANCZOS)
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    out.save(DESTINO, "WEBP", quality=88, method=6)

    a = out.split()[3]
    w, h = out.size
    esquinas = [a.getpixel(p) for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    print("robot: %.1f%% de la imagen original" % (100 * cobertura))
    print("salida: %s  %.0f KB" % (out.size, os.path.getsize(DESTINO) / 1024))
    print("alfa en las esquinas: %s  %s" % (esquinas, "OK" if max(esquinas) == 0 else "REVISAR"))


if __name__ == "__main__":
    main()
