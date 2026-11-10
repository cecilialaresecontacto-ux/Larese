"""Arma cinco.png: Hawas Ice · Amber Oud · Liquid Brun (centro) · Hawas Verde · Odyssey Aqua."""
import os
from PIL import Image, ImageDraw, ImageFilter
CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = 1000

def cargar(nombre, rel):
    p = Image.open(os.path.join(CARPETA, "recortes", f"{nombre}.png")).convert("RGBA")
    return p.resize((int(p.width * H * rel / p.height), int(H * rel)), Image.LANCZOS)

items = [cargar("hawas-ice", .74), cargar("amber-oud", .80), cargar("liquid-brun", 1.0),
         cargar("hawas-verde", .86), cargar("odyssey-aqua", .76)]
gap = -40
W = sum(i.width for i in items) + gap * 4
lienzo = Image.new("RGBA", (W, H + 30), (0, 0, 0, 0))
pos, x = [], 0
for i in items:
    pos.append(x); x += i.width + gap
for k in [0, 4, 1, 3, 2]:          # los de afuera primero, el del centro arriba
    s = Image.new("L", lienzo.size, 0)
    ImageDraw.Draw(s).ellipse((pos[k] + items[k].width * .1, H - 6, pos[k] + items[k].width * .9, H + 22), fill=110)
    capa = Image.new("RGBA", lienzo.size, (0, 0, 0, 0)); capa.putalpha(s.filter(ImageFilter.GaussianBlur(12)))
    lienzo.alpha_composite(capa)
    lienzo.alpha_composite(items[k], (pos[k], H + 8 - items[k].height))
lienzo = lienzo.crop(lienzo.getbbox())
lienzo.save(os.path.join(CARPETA, "cinco.png")); print(lienzo.size)
