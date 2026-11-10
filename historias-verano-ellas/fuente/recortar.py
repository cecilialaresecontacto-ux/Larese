"""Recorta los perfumes (fondo blanco) sin comerse las cajas blancas.

El script de la herramienta usa un umbral alto y se mete dentro de las cajas blancas;
acá el fondo se rellena desde los bordes con un umbral bajo, así que solo sale el blanco
de afuera y la caja queda entera.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fotos = {"jadore": ("jadore.jpg", 8), "omnia": ("omnia.jpg", 8), "romance": ("romance.jpg", 10)}
os.makedirs(os.path.join(CARPETA, "recortes"), exist_ok=True)
MARCA = (1, 254, 3)
for nombre, (f, umbral) in fotos.items():
    im = Image.open(os.path.join(CARPETA, f)).convert("RGB")
    if nombre == "romance":  # foto chica con mucho margen: se acerca y se agranda x3
        im = im.crop((185, 396, 612, 728)); im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS)
    base = im.copy()
    w, h = base.size
    paso = max(1, w // 80)
    semillas = [(x, 0) for x in range(0, w, paso)] + [(x, h - 1) for x in range(0, w, paso)] \
             + [(0, y) for y in range(0, h, paso)] + [(w - 1, y) for y in range(0, h, paso)]
    for s in semillas:
        if base.getpixel(s) != MARCA and min(base.getpixel(s)) > 225:
            ImageDraw.floodfill(base, s, MARCA, thresh=umbral)
    fondo = np.all(np.asarray(base) == MARCA, axis=-1)
    alfa = Image.fromarray(np.where(fondo, 0, 255).astype(np.uint8))
    alfa = alfa.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1))
    out = im.convert("RGBA"); out.putalpha(alfa)
    out = out.crop(alfa.point(lambda v: 255 if v > 40 else 0).getbbox())
    out.save(os.path.join(CARPETA, "recortes", f"{nombre}.png"))
    print(nombre, out.size)
