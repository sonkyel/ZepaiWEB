# -*- coding: utf-8 -*-
"""Genera las variantes de imagen del tamano en que se ven de verdad.

PageSpeed (movil) marco 218 KB de imagenes servidas mas grandes de lo que se
muestran. Los tres casos:

  logo.png      666x375 PNG, 50,3 KB. Se ve a 150x84 en movil y a 178x100 en
                escritorio. Ademas va en la nav: se descarga en las 47
                paginas, no solo en la portada. Es el peor de los tres.
  robot-v2      400x1018, 54,5 KB. Es el elemento LCP, y en movil se pinta a
                97x247.
  tarjetas/*    320x320 cada una, mostradas a 124x124.

Los tamanos de destino salen de multiplicar la medida CSS por la densidad de
pantalla, no de redondear a ojo: una pantalla de movil normal tiene entre 2 y
3 pixeles fisicos por pixel CSS, asi que servir justo la medida CSS se ve
borroso. Se toma DPR 2,625, que es el del Moto G Power con el que mide
PageSpeed.

logo.png NO se borra: es el que declara el JSON-LD como logo de la
organizacion, y ahi Google quiere PNG o JPG.

    python generar-imagenes.py
"""
import io
import os

from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(BASE, "public")

DPR = 2.625


def guarda(im, ruta, calidad=82, lossless=False):
    antes = os.path.getsize(ruta) / 1024 if os.path.exists(ruta) else 0
    im.save(ruta, "WEBP", quality=calidad, method=6, lossless=lossless)
    ahora = os.path.getsize(ruta) / 1024
    rel = os.path.relpath(ruta, BASE).replace("\\", "/")
    if antes:
        print("  %-38s %6.1f -> %6.1f KB  (-%.0f%%)"
              % (rel, antes, ahora, 100 * (1 - ahora / antes)))
    else:
        print("  %-38s %6s    %6.1f KB  %dx%d"
              % (rel, "nuevo", ahora, im.width, im.height))
    return ahora


def redimensiona(origen, ancho):
    im = Image.open(origen)
    if im.mode not in ("RGBA", "RGB"):
        im = im.convert("RGBA")
    alto = round(im.height * ancho / im.width)
    return im.resize((ancho, alto), Image.LANCZOS)


def main():
    total_antes = total_ahora = 0.0

    print("\nLOGO  (nav y pie, en las 47 paginas)")
    # Medida mayor: 178 CSS px de ancho en escritorio, 150 en movil.
    # 178 x 2 (escritorio retina) = 356 ; 150 x 2,625 (movil) = 394.
    # 400 cubre los dos con margen y mantiene la proporcion original.
    src = os.path.join(PUB, "logo.png")
    total_antes += os.path.getsize(src) / 1024
    # Sin perdida: es un logotipo con texto fino sobre negro, y con perdida
    # aparecen halos alrededor de las letras.
    total_ahora += guarda(redimensiona(src, 400), os.path.join(PUB, "logo.webp"),
                          lossless=True)

    print("\nROBOT DEL HERO  (elemento LCP)")
    # Anchos CSS reales segun galaxy.css: 110 px como maximo en movil,
    # 134 hasta 900 px, 220 en escritorio.
    #   movil     110 x 2,625 = 289  -> variante de 300
    #   escritorio 220 x 2     = 440  -> se queda la de 400 que ya existe
    src = os.path.join(PUB, "hero", "robot-v2.webp")
    total_antes += os.path.getsize(src) / 1024
    total_ahora += guarda(redimensiona(src, 300),
                          os.path.join(PUB, "hero", "robot-v2-300.webp"))
    total_ahora += os.path.getsize(src) / 1024  # la de 400 se conserva

    print("\nTARJETAS  (124 CSS px -> 124 x 2,625 = 326... se quedan en 320)")
    # Aqui PageSpeed se queja de 320x320 para 124x124, pero 124 x 2,625 = 326:
    # el fichero YA es del tamano justo para una pantalla retina. Lighthouse
    # calcula con DPR 1 en esta auditoria concreta. Bajarlas a 248 las dejaria
    # borrosas en el movil de verdad para ahorrar unos kilobytes.
    # Lo que si se puede hacer sin tocar el tamano es recomprimir.
    carpeta = os.path.join(PUB, "tarjetas")
    for f in sorted(os.listdir(carpeta)):
        if not f.endswith(".webp"):
            continue
        ruta = os.path.join(carpeta, f)
        antes = os.path.getsize(ruta) / 1024
        im = Image.open(ruta)
        tmp = io.BytesIO()
        im.save(tmp, "WEBP", quality=78, method=6)
        despues = tmp.tell() / 1024
        total_antes += antes
        if despues < antes * 0.92:
            io.open(ruta, "wb").write(tmp.getvalue())
            print("  %-38s %6.1f -> %6.1f KB  (-%.0f%%)"
                  % ("public/tarjetas/" + f, antes, despues,
                     100 * (1 - despues / antes)))
            total_ahora += despues
        else:
            print("  %-38s %6.1f KB  ya esta ajustada" % ("public/tarjetas/" + f, antes))
            total_ahora += antes

    print("\n  TOTAL  %.1f KB -> %.1f KB   (%.1f KB menos)"
          % (total_antes, total_ahora, total_antes - total_ahora))


if __name__ == "__main__":
    main()
