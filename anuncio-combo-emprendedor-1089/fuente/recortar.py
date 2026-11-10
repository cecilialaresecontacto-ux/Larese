"""Recorta los 5 perfumes del combo de Gs. 976.300.
Liquid Brun sale de la composición del combo del 9 de noviembre (cinco.png); los demás, de sus fotos."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARCA = (1, 254, 3)

def recortar(im, umbral=8, oscuro=False):
    base = im.copy(); w, h = base.size; paso = max(1, w // 120)
    semillas = [(x, 0) for x in range(0, w, paso)] + [(x, h - 1) for x in range(0, w, paso)] \
             + [(0, y) for y in range(0, h, paso)] + [(w - 1, y) for y in range(0, h, paso)]
    for s in semillas:
        px = base.getpixel(s)
        if px != MARCA and (oscuro or min(px) > 225):
            ImageDraw.floodfill(base, s, MARCA, thresh=umbral)
    return np.all(np.asarray(base) == MARCA, axis=-1)

def guardar(im, fondo, nombre):
    alfa = Image.fromarray(np.where(fondo, 0, 255).astype(np.uint8))
    alfa = alfa.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1))
    out = im.convert("RGBA"); out.putalpha(alfa)
    out = out.crop(alfa.point(lambda v: 255 if v > 40 else 0).getbbox())
    out.save(os.path.join(CARPETA, "recortes", f"{nombre}.png")); print(nombre, out.size)

for nombre, f in [("hawas-ice", "hawas-ice.jpg"), ("hawas-verde", "hawas-verde.webp"),
                  ("amber-oud", "amber-oud-aqua-dubai.jpg"), ("odyssey-aqua", "odyssey-aqua.webp")]:
    im = Image.open(os.path.join(CARPETA, "fotos", f)).convert("RGB")
    guardar(im, recortar(im), nombre)

# Liquid Brun: está entre Amber Oud (cian) y Club de Nuit (negro) en cinco.png
cinco = Image.open(os.path.join(CARPETA, "..", "anuncio-combo-emprendedor-masculino", "cinco.png")).convert("RGB")
im = cinco.crop((1110, 0, 1520, 1020))
a = np.asarray(im).astype(int)
fondo = recortar(im, umbral=10)
cian = (a[..., 2] - a[..., 0] > 70)
negro = (a.max(-1) < 70)
x = np.arange(a.shape[1])[None, :].repeat(a.shape[0], 0)
fondo |= cian | (negro & ((x < 60) | (x > 300)))
guardar(im, fondo, "liquid-brun")
