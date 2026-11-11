"""Recorta las 3 fotos (fondo claro) rellenando el fondo desde los bordes con umbral bajo."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARCA = (1, 254, 3)
for nombre, f, umbral in [("hawas-kobra", "hawas-kobra.jpg", 10), ("supremacy", "supremacy-collectors.jpg", 10),
                          ("hawas-ice", "hawas-ice.webp", 8)]:
    im = Image.open(os.path.join(CARPETA, "fotos", f)).convert("RGB")
    base = im.copy(); w, h = base.size; paso = max(1, w // 120)
    for s in [(x, 0) for x in range(0, w, paso)] + [(x, h - 1) for x in range(0, w, paso)] + \
             [(0, y) for y in range(0, h, paso)] + [(w - 1, y) for y in range(0, h, paso)]:
        if base.getpixel(s) != MARCA and min(base.getpixel(s)) > 215:
            ImageDraw.floodfill(base, s, MARCA, thresh=umbral)
    fondo = np.all(np.asarray(base) == MARCA, axis=-1)
    alfa = Image.fromarray(np.where(fondo, 0, 255).astype(np.uint8))
    alfa = alfa.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1))
    out = im.convert("RGBA"); out.putalpha(alfa)
    out = out.crop(alfa.point(lambda v: 255 if v > 40 else 0).getbbox())
    out.save(os.path.join(CARPETA, "recortes", f"{nombre}.png")); print(nombre, im.size, im.getpixel((2, 2)), "->", out.size)
