# -*- coding: utf-8 -*-
"""Genera carruseles para Instagram con la tipografia y el color de la marca.

Por que no se generan con un modelo de imagen: escriben en un idioma
inventado. Lo vimos en la foto del fundador, donde el rotulo de la pared
tenia debajo letras que no son de ningun alfabeto. Un carrusel es texto, y
el texto tiene que leerse.

Asi que se componen: Satoshi de verdad, el violeta de la web, el robot
recortado con transparencia y las piezas 3D que ya existen.

El contenido va en un fichero aparte -- carruseles/<nombre>.txt -- para que
se puedan hacer mas sin tocar este codigo:

    ---
    Titulo de la diapositiva
    Cuerpo de la diapositiva, opcional.
    @pieza opcional: nombre de un webp de public/tarjetas o public/hero
    ---

Uso:
    python carrusel.py creencias
"""
import io
import os
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FUENTES = os.path.join(BASE, "_fuentes", "tipografia")
SALIDA = os.path.join(BASE, "_fuentes", "carruseles")

# 4:5 es el formato que Instagram muestra mas grande en el feed
ANCHO, ALTO = 1080, 1350
MARGEN = 96

# Los mismos tokens que la web
FONDO = (8, 7, 13)
FONDO_ALT = (21, 18, 31)
VIOLETA = (168, 85, 247)
VIOLETA_CLARO = (192, 132, 252)
BLANCO = (255, 255, 255)
GRIS = (255, 255, 255, 200)


def fuente(peso, tam):
    return ImageFont.truetype(os.path.join(FUENTES, "Satoshi-%d.ttf" % peso), tam)


def ajustar(dibujo, texto, f, ancho_max):
    """Parte el texto en lineas que quepan, midiendo de verdad."""
    palabras, lineas, actual = texto.split(), [], ""
    for p in palabras:
        prueba = (actual + " " + p).strip()
        if dibujo.textlength(prueba, font=f) <= ancho_max:
            actual = prueba
        else:
            if actual:
                lineas.append(actual)
            actual = p
    if actual:
        lineas.append(actual)
    return lineas


def encaja(dibujo, texto, peso, tam_ini, ancho_max, alto_max, tam_min=28):
    """Baja el cuerpo hasta que el bloque cabe. Sin esto, un titular largo
    se sale de la diapositiva y no hay aviso: simplemente se corta."""
    tam = tam_ini
    while tam > tam_min:
        f = fuente(peso, tam)
        lineas = ajustar(dibujo, texto, f, ancho_max)
        alto = len(lineas) * int(tam * 1.14)
        if alto <= alto_max:
            return f, lineas, int(tam * 1.14)
        tam -= 2
    f = fuente(peso, tam_min)
    return f, ajustar(dibujo, texto, f, ancho_max), int(tam_min * 1.14)


def fondo(indice):
    """Alterna el fondo para que el carrusel no sea una pared plana."""
    img = Image.new("RGB", (ANCHO, ALTO), FONDO if indice % 2 == 0 else FONDO_ALT)
    # Resplandor violeta, como el de la web
    halo = Image.new("RGBA", (ANCHO, ALTO), (0, 0, 0, 0))
    d = ImageDraw.Draw(halo)
    cx, cy = (ANCHO * 0.75, ALTO * 0.18) if indice % 2 == 0 else (ANCHO * 0.2, ALTO * 0.8)
    for r in range(520, 0, -20):
        a = int(26 * (1 - r / 520.0))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=VIOLETA + (a,))
    img = Image.alpha_composite(img.convert("RGBA"), halo).convert("RGB")
    return img


def pieza(img, nombre, alto_obj=360, pos=("derecha", "abajo")):
    for carpeta in ("tarjetas", "hero", "paginas", "pasos"):
        ruta = os.path.join(BASE, "public", carpeta, nombre + ".webp")
        if os.path.exists(ruta):
            break
    else:
        return img
    p = Image.open(ruta).convert("RGBA")
    escala = alto_obj / float(p.size[1])
    p = p.resize((int(p.size[0] * escala), alto_obj), Image.LANCZOS)
    x = ANCHO - p.size[0] - MARGEN + 30 if pos[0] == "derecha" else MARGEN - 30
    y = ALTO - p.size[1] - MARGEN - 40
    img.paste(p, (max(0, x), max(0, y)), p)
    return img


def marca(img, d, indice, total):
    """Pie de diapositiva: la marca y el numero. Sin esto, un carrusel que
    alguien reenvia no lleva a ninguna parte."""
    f = fuente(700, 26)
    d.text((MARGEN, ALTO - 60), "@zepaiagency", font=f, fill=VIOLETA_CLARO)
    if indice:
        n = "%d/%d" % (indice, total - 1)
        d.text((ANCHO - MARGEN - d.textlength(n, font=f), ALTO - 60), n, font=f, fill=(255, 255, 255, 120))


def portada(datos, total):
    img = fondo(0)
    d = ImageDraw.Draw(img)
    ancho = ANCHO - MARGEN * 2

    etiqueta = fuente(700, 28)
    d.text((MARGEN, MARGEN + 10), datos.get("etiqueta", "").upper(), font=etiqueta, fill=VIOLETA_CLARO)

    f, lineas, salto = encaja(d, datos["titulo"], 900, 96, ancho, 520)
    y = MARGEN + 110
    for l in lineas:
        d.text((MARGEN, y), l, font=f, fill=BLANCO)
        y += salto

    if datos.get("cuerpo"):
        f2, l2, s2 = encaja(d, datos["cuerpo"], 500, 40, ancho - 120, 240)
        y += 30
        for l in l2:
            d.text((MARGEN, y), l, font=f2, fill=(255, 255, 255, 190))
            y += s2

    img = pieza(img, datos.get("pieza", "robot-v2"), alto_obj=520)
    marca(img, ImageDraw.Draw(img), 0, total)
    return img


def diapositiva(datos, indice, total):
    img = fondo(indice)
    d = ImageDraw.Draw(img)
    ancho = ANCHO - MARGEN * 2

    num = fuente(900, 120)
    d.text((MARGEN, MARGEN - 20), "%02d" % indice, font=num, fill=VIOLETA + (70,))

    f, lineas, salto = encaja(d, datos["titulo"], 900, 72, ancho, 380)
    y = MARGEN + 150
    for l in lineas:
        d.text((MARGEN, y), l, font=f, fill=BLANCO)
        y += salto

    if datos.get("cuerpo"):
        f2, l2, s2 = encaja(d, datos["cuerpo"], 500, 38, ancho, 520)
        y += 40
        for l in l2:
            d.text((MARGEN, y), l, font=f2, fill=(255, 255, 255, 195))
            y += s2

    if datos.get("pieza"):
        img = pieza(img, datos["pieza"], alto_obj=300)
    marca(img, ImageDraw.Draw(img), indice, total)
    return img


def leer(nombre):
    ruta = os.path.join(BASE, "carruseles", nombre + ".txt")
    bruto = io.open(ruta, encoding="utf-8").read()
    bloques = [b.strip() for b in bruto.split("---") if b.strip()]
    fuera = []
    for b in bloques:
        datos, cuerpo = {}, []
        for linea in b.split("\n"):
            if linea.startswith("@"):
                clave, _, valor = linea[1:].partition(":")
                datos[clave.strip()] = valor.strip()
            elif not datos.get("titulo"):
                datos["titulo"] = linea.strip()
            else:
                cuerpo.append(linea.strip())
        datos["cuerpo"] = " ".join(x for x in cuerpo if x)
        fuera.append(datos)
    return fuera


def main():
    nombre = sys.argv[1] if len(sys.argv) > 1 else "creencias"
    hojas = leer(nombre)
    destino = os.path.join(SALIDA, nombre)
    os.makedirs(destino, exist_ok=True)

    # La ultima con etiqueta es el cierre: se compone como la portada y no
    # lleva numero. Si no, la llamada a la accion parece un punto mas de la
    # lista y la cuenta sale descuadrada.
    cierre = len(hojas) > 2 and "etiqueta" in hojas[-1]
    numeradas = len(hojas) - 1 - (1 if cierre else 0)

    for i, h in enumerate(hojas):
        if i == 0:
            img = portada(h, numeradas + 1)
        elif cierre and i == len(hojas) - 1:
            img = portada(h, numeradas + 1)
        else:
            img = diapositiva(h, i, numeradas + 1)
        ruta = os.path.join(destino, "%02d.jpg" % i)
        img.save(ruta, "JPEG", quality=92, subsampling=0)
    print("%d diapositivas (%d numeradas) en _fuentes/carruseles/%s/" % (len(hojas), numeradas, nombre))
    print("%.0f KB en total" % (sum(os.path.getsize(os.path.join(destino, f))
                                   for f in os.listdir(destino)) / 1024))


if __name__ == "__main__":
    main()
