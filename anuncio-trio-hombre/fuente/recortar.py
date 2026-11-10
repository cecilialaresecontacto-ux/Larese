"""Recorta las 3 fotos (fondo blanco) y agranda las chicas, sin comerse las cajas."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# nombre: (archivo, recorte previo, escala)
fotos = {
    "acqua-di-gio-profondo": ("acqua-di-gio-profondo.webp", (109, 212, 428, 510), 3),
    "le-beau": ("le-beau.webp", (183, 231, 356, 451), 4),
    "born-in-roma-intense": ("born-in-roma-intense.webp", None, 1),
}
MARCA = (1, 254, 3)
os.makedirs(os.path.join(CARPETA, "recortes"), exist_ok=True)
for nombre, (f, caja, escala) in fotos.items():
    im = Image.open(os.path.join(CARPETA, "fotos", f)).convert("RGB")
    if caja:
        im = im.crop(caja)
    if escala > 1:
        im = im.resize((im.width * escala, im.height * escala), Image.LANCZOS)
    base = im.copy()
    w, h = base.size
    paso = max(1, w // 80)
    semillas = [(x, 0) for x in range(0, w, paso)] + [(x, h - 1) for x in range(0, w, paso)] \
             + [(0, y) for y in range(0, h, paso)] + [(w - 1, y) for y in range(0, h, paso)]
    for s in semillas:
        if base.getpixel(s) != MARCA and min(base.getpixel(s)) > 225:
            ImageDraw.floodfill(base, s, MARCA, thresh=10)
    fondo = np.all(np.asarray(base) == MARCA, axis=-1)
    alfa = Image.fromarray(np.where(fondo, 0, 255).astype(np.uint8))
    alfa = alfa.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1))
    out = im.convert("RGBA"); out.putalpha(alfa)
    out = out.crop(alfa.point(lambda v: 255 if v > 40 else 0).getbbox())
    out.save(os.path.join(CARPETA, "recortes", f"{nombre}.png"))
    print(nombre, out.size)
