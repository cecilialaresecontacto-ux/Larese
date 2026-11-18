#!/usr/bin/env python3
"""Decants de 5 y 10 ml para fondo bordó, a partir de la foto real del frasquito vacío
(fuente/decant-vacio.webp, la que mandó la dueña).

- Les pinta el perfume adentro con el color de cada fragancia.
- El de 5 ml es el mismo frasco con el cuerpo más corto (misma tapa y mismo ancho).
- Sobre bordó el vidrio transparente se vería oscuro: el vidrio queda como un velo claro
  semitransparente y el perfume casi opaco, así se lee bien sobre el vino.
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
RECORTE = (214, 76, 384, 684)       # el frasco entero en la foto original (595x892)
INTERIOR = (248, 335, 352, 631)     # donde va el perfume
CORTE_5ML = (380, 505)              # franja del cuerpo que se saca para el de 5 ml (coordenadas originales)
FIN_TAPA = 262                      # hasta acá (en y) es la tapa dorada: va opaca


def _base():
    return Image.open(os.path.join(AQUI, "decant-vacio.webp")).convert("RGB")


def _silueta(im):
    """Máscara del frasco: todo lo que no es el fondo blanco conectado a los bordes."""
    marcador = (1, 254, 3)
    b = im.copy()
    w, h = b.size
    for p in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (0, h // 2), (w - 1, h // 2)]:
        if b.getpixel(p) != marcador:
            ImageDraw.floodfill(b, p, marcador, thresh=18)
    fuera = np.all(np.array(b) == marcador, axis=-1)
    m = Image.fromarray(np.where(fuera, 0, 255).astype("uint8"))
    return m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))


def frasco(color, ml=10):
    im = _base()
    a = np.array(im).astype(float)
    liq = Image.new("L", im.size, 0)
    ImageDraw.Draw(liq).rounded_rectangle(INTERIOR, radius=8, fill=255)
    liq = np.array(liq.filter(ImageFilter.GaussianBlur(1.5))).astype(float) / 255
    sil = np.array(_silueta(im)).astype(float) / 255

    # color: perfume teñido (multiplicar, se siguen viendo el tubito y los reflejos)
    tinte = a * (np.array(color) / 255.0)
    rgb = a * (1 - liq[..., None] * 0.92) + tinte * (liq[..., None] * 0.92)
    # alfa: lo oscuro (tapa, bordes) opaco; el vidrio, un velo claro; el perfume casi opaco
    oscuridad = np.clip((255 - a.min(axis=2)) / 255 * 1.6, 0, 1)
    alfa = np.maximum(oscuridad, 0.30) * sil
    alfa = np.maximum(alfa, liq * 0.94 * sil)
    alfa[:FIN_TAPA] = sil[:FIN_TAPA]
    out = np.dstack([rgb.clip(0, 255), alfa * 255]).astype("uint8")
    img = Image.fromarray(out, "RGBA")

    if ml == 5:
        y0, y1 = CORTE_5ML
        arriba = img.crop((0, 0, img.width, y0))
        abajo = img.crop((0, y1, img.width, img.height))
        nuevo = Image.new("RGBA", (img.width, img.height - (y1 - y0)), (0, 0, 0, 0))
        nuevo.paste(arriba, (0, 0))
        nuevo.paste(abajo, (0, y0))
        img = nuevo
        x0, t, x1, b = RECORTE
        return img.crop((x0, t, x1, b - (y1 - y0)))
    return img.crop(RECORTE)


if __name__ == "__main__":
    import sys
    fondo = Image.new("RGBA", (520, 760), (0x41, 0x03, 0x0B, 255))
    for i, (c, ml) in enumerate([((236, 170, 160), 5), ((236, 170, 160), 10), ((222, 160, 88), 5), ((222, 160, 88), 10)]):
        f = frasco(c, ml)
        fondo.alpha_composite(f, (5 + i * 130, 700 - f.height))
    fondo.save(sys.argv[1] if len(sys.argv) > 1 else "prueba.png")
