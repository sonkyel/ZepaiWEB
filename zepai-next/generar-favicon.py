# -*- coding: utf-8 -*-
"""Dibuja el icono de la marca y escribe favicon.ico y apple-touch-icon.

Dos problemas que arregla:

  1. src/app/favicon.ico era el que trae create-next-app: el triangulo de
     Vercel. Next da prioridad a ese fichero por convencion de nombre, asi
     que ganaba al icons.icon declarado en el layout y salia en la pestana
     de todo el que entraba.

  2. apple-touch-icon.png era el logotipo COMPLETO -- "ZEPAI AGENCY" con su
     tipografia -- metido en 180x180. A ese tamano no se lee, y a 16 px es
     una mancha gris.

Un icono de pestana no es un logotipo pequeno: es una marca. Aqui se usa el
robot que hace de "A" en el logotipo, que ya es el simbolo de la casa.

Se redibuja en vez de recortarse del PNG porque en el logotipo mide 62x60
pixeles: ampliado a 256 sale borroso. Las proporciones estan medidas del
original, no inventadas.

    python generar-favicon.py
"""
import io
import os

from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))

FONDO = (14, 12, 22)        # --bg1, el mismo de las tarjetas
BLANCO = (255, 255, 255)
VIOLETA = (168, 85, 247)    # --cyan, el violeta de marca

# Medidas tomadas del logotipo (marca de 62x60):
#   bola     12 de diametro, centro en x 30,5   y 7,5
#   cabeza   58x35, de y 25 a 59
#   ojos     7x12 cada uno, en x 16-22 y 39-45, y 36-47 (absolutos)
# Se pasan a fraccion del lado para poder dibujar a cualquier tamano.
L = 62.0
BOLA_R = 6 / L
BOLA_CX, BOLA_CY = 30.5 / L, 7.5 / L
TALLO_W = 2.4 / L
CAB_X0, CAB_X1 = 2 / L, 60 / L
CAB_Y0, CAB_Y1 = 25 / L, 60 / L
OJO_W, OJO_H = 7 / L, 12 / L
OJO1_X, OJO2_X = 16 / L, 39 / L
OJO_Y = 36 / L


def icono(lado, con_fondo=True, margen=0.13):
    """El robot, centrado, con aire alrededor.

    El margen no es estetico: sin el, a 16 px la cabeza toca el borde y en
    una pestana se lee como un rectangulo, no como una cara.
    """
    ss = 8  # se dibuja 8 veces mas grande y se reduce: bordes limpios
    n = lado * ss
    img = Image.new("RGBA", (n, n), FONDO + (255,) if con_fondo else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if con_fondo:
        # Esquinas redondeadas, del mismo aire que las tarjetas de la web
        mascara = Image.new("L", (n, n), 0)
        ImageDraw.Draw(mascara).rounded_rectangle([0, 0, n - 1, n - 1],
                                                  radius=int(n * 0.22), fill=255)
        img.putalpha(mascara)

    util = n * (1 - margen * 2)
    o = n * margen

    def X(v):
        return o + v * util

    # Tallo de la antena
    d.rounded_rectangle([X(BOLA_CX - TALLO_W / 2), X(BOLA_CY),
                         X(BOLA_CX + TALLO_W / 2), X(CAB_Y0 + 0.02)],
                        radius=util * TALLO_W / 2, fill=BLANCO)
    # Cabeza
    d.rounded_rectangle([X(CAB_X0), X(CAB_Y0), X(CAB_X1), X(CAB_Y1)],
                        radius=util * 0.145, fill=BLANCO)
    # Ojos, vaciados
    for ox in (OJO1_X, OJO2_X):
        d.rounded_rectangle([X(ox), X(OJO_Y), X(ox + OJO_W), X(OJO_Y + OJO_H)],
                            radius=util * OJO_W / 2, fill=FONDO if con_fondo else (10, 8, 16))
    # Bola de la antena, lo unico violeta
    d.ellipse([X(BOLA_CX - BOLA_R), X(BOLA_CY - BOLA_R),
               X(BOLA_CX + BOLA_R), X(BOLA_CY + BOLA_R)], fill=VIOLETA)

    return img.resize((lado, lado), Image.LANCZOS)


def main():
    # favicon.ico con los cuatro tamanos que piden los navegadores
    tamanos = [16, 32, 48, 64, 128, 256]
    capas = [icono(t) for t in tamanos]
    destino = os.path.join(BASE, "src", "app", "favicon.ico")
    capas[-1].save(destino, format="ICO",
                   sizes=[(t, t) for t in tamanos])
    print("  src/app/favicon.ico        %d tamanos, %.1f KB"
          % (len(tamanos), os.path.getsize(destino) / 1024))

    # apple-touch-icon: sin esquinas redondeadas, iOS ya las pone
    ios = icono(180, margen=0.16)
    ios = ios.convert("RGB")
    ruta_ios = os.path.join(BASE, "public", "apple-touch-icon.png")
    ios.save(ruta_ios, optimize=True)
    print("  public/apple-touch-icon.png 180x180, %.1f KB" % (os.path.getsize(ruta_ios) / 1024))

    # Hoja de contactos para mirarlo a tamano real antes de publicarlo
    hoja = Image.new("RGB", (430, 90), (58, 58, 66))
    x = 12
    for t in (16, 32, 48, 64, 128):
        i = icono(t)
        hoja.paste(i, (x, (90 - t) // 2), i)
        x += t + 14
    hoja.save(os.path.join(BASE, "_fuentes", "favicon-prueba.png"))
    print("  _fuentes/favicon-prueba.png a tamano real")


if __name__ == "__main__":
    main()
