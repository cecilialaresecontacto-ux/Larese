"""Arma tres.png: Hawas Ice · Hawas Kobra (con caja, al centro) · Supremacy Collector's Edition."""
import os
from PIL import Image, ImageDraw, ImageFilter
CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def cargar(nombre, alto):
    p = Image.open(os.path.join(CARPETA, "recortes", f"{nombre}.png")).convert("RGBA")
    return p.resize((int(p.width * alto / p.height), int(alto)), Image.LANCZOS)

piezas = [cargar("hawas-ice", 820), cargar("hawas-kobra", 760), cargar("supremacy", 860)]
sep = 40
W = sum(p.width for p in piezas) + sep * 2
H = max(p.height for p in piezas) + 30
lienzo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
x = 0
for p in piezas:
    s = Image.new("L", lienzo.size, 0)
    ImageDraw.Draw(s).ellipse((x + p.width * .1, H - 40, x + p.width * .9, H - 10), fill=120)
    capa = Image.new("RGBA", lienzo.size, (0, 0, 0, 0)); capa.putalpha(s.filter(ImageFilter.GaussianBlur(12)))
    lienzo.alpha_composite(capa)
    lienzo.alpha_composite(p, (x, H - 25 - p.height)); x += p.width + sep
lienzo = lienzo.crop(lienzo.getbbox())
lienzo.save(os.path.join(CARPETA, "tres.png")); print(lienzo.size)
