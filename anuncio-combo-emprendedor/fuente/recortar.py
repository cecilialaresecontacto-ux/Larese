"""Recorta las 5 fotos del combo (rellenando el fondo desde los bordes con umbral bajo)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# nombre: (archivo, umbral, fondo oscuro)
fotos = {
    "asad-elixir": ("asad-elixir.png", 10, False),
    "bharara-king": ("bharara-king.jpg", 10, False),
    "9pm-rebel": ("9pm-rebel.jpg", 22, True),
    "khamrah-qahwa": ("khamrah-qahwa.jpg", 6, False),
    "club-de-nuit": ("club-de-nuit.jpg", 10, False),
}
MARCA = (1, 254, 3)
for nombre, (f, umbral, oscuro) in fotos.items():
    im = Image.open(os.path.join(CARPETA, "fotos", f)).convert("RGB")
    if nombre == "asad-elixir":  # solo el frasco, sin la caja
        im = im.crop((570, 0, im.width, im.height))
    base = im.copy()
    w, h = base.size
    paso = max(1, w // 80)
    semillas = [(x, 0) for x in range(0, w, paso)] + [(x, h - 1) for x in range(0, w, paso)] \
             + [(0, y) for y in range(0, h, paso)] + [(w - 1, y) for y in range(0, h, paso)]
    for s in semillas:
        px = base.getpixel(s)
        fondo_ok = max(px) < 30 if oscuro else min(px) > 225
        if px != MARCA and fondo_ok:
            ImageDraw.floodfill(base, s, MARCA, thresh=umbral)
    fondo = np.all(np.asarray(base) == MARCA, axis=-1)
    alfa = Image.fromarray(np.where(fondo, 0, 255).astype(np.uint8))
    alfa = alfa.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1))
    out = im.convert("RGBA"); out.putalpha(alfa)
    out = out.crop(alfa.point(lambda v: 255 if v > 40 else 0).getbbox())
    out.save(os.path.join(CARPETA, "recortes", f"{nombre}.png"))
    print(nombre, out.size)
