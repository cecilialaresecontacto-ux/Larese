#!/usr/bin/env python3
"""Arma 6 decants llenos a partir de la foto del frasquito vacío (fuente/decant-vacio.webp):
recorta el frasco (sin el texto de abajo), le pinta perfume de distintos colores adentro
y lo pasa a PNG transparente para que sirva sobre fondo blanco o bordó.
Salida: fuente/decants-foto.png"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
# medidas medidas sobre la foto original (595x892)
RECORTE = (214, 76, 384, 684)                 # el frasco entero, sin el cartel de abajo
INTERIOR = (248, 335, 352, 631)               # donde va el perfume (deja aire arriba)
LIQUIDOS = [(236, 170, 160), (222, 160, 88), (246, 200, 190), (196, 122, 112), (238, 196, 122), (230, 150, 172)]


def lleno(base, color):
    im = base.copy()
    a = np.array(im).astype(float)
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle(INTERIOR, radius=8, fill=255)
    m = np.array(m.filter(ImageFilter.GaussianBlur(1.5))).astype(float)[..., None] / 255
    tinte = a * (np.array(color) / 255.0)          # multiplicar: el vidrio y el tubito siguen viéndose
    a = a * (1 - m * 0.9) + tinte * (m * 0.9)
    return Image.fromarray(a.clip(0, 255).astype("uint8"))


def a_transparente(im):
    """Pasa la foto sobre blanco a RGBA: el blanco queda transparente y el vidrio semitransparente."""
    c = np.array(im).astype(float)
    alfa = (255 - c.min(axis=2)) / 255.0
    alfa = np.clip(alfa * 1.15, 0, 1)
    k = np.where(alfa[..., None] > 0.01, (c - (1 - alfa[..., None]) * 255) / np.maximum(alfa[..., None], 0.01), 0)
    out = np.dstack([k.clip(0, 255), alfa * 255]).astype("uint8")
    return Image.fromarray(out, "RGBA")


def main():
    base = Image.open(os.path.join(AQUI, "decant-vacio.webp")).convert("RGB")
    frascos = [a_transparente(lleno(base, c).crop(RECORTE)) for c in LIQUIDOS]
    fw, fh = frascos[0].size
    gap = 18
    out = Image.new("RGBA", (len(frascos) * fw + (len(frascos) - 1) * gap, fh + 40), (0, 0, 0, 0))
    for i, f in enumerate(frascos):
        out.alpha_composite(f, (i * (fw + gap), 0 if i % 2 == 0 else 40))
    ruta = os.path.join(AQUI, "decants-foto.png")
    out.save(ruta)
    print(ruta, out.size)


if __name__ == "__main__":
    main()
