"""Arma cinco-historia.png en dos filas (para la historia, que tiene más alto):
atrás Hawas Ice · Amber Oud · Odyssey Aqua; adelante Liquid Brun y Hawas Verde."""
import os
from PIL import Image, ImageDraw, ImageFilter
CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def cargar(nombre, alto):
    p = Image.open(os.path.join(CARPETA, "recortes", f"{nombre}.png")).convert("RGBA")
    return p.resize((int(p.width * alto / p.height), int(alto)), Image.LANCZOS)

atras = [cargar("hawas-ice", 560), cargar("amber-oud", 600), cargar("odyssey-aqua", 580)]
adelante = [cargar("liquid-brun", 760), cargar("hawas-verde", 640)]
sep = 10
W = sum(p.width for p in atras) + sep * 2
base_atras = 600
H = base_atras + 330
lienzo = Image.new("RGBA", (W, H), (0, 0, 0, 0))

def poner(p, x, base):
    s = Image.new("L", lienzo.size, 0)
    ImageDraw.Draw(s).ellipse((x + p.width * .1, base - 12, x + p.width * .9, base + 14), fill=110)
    capa = Image.new("RGBA", lienzo.size, (0, 0, 0, 0)); capa.putalpha(s.filter(ImageFilter.GaussianBlur(12)))
    lienzo.alpha_composite(capa)
    lienzo.alpha_composite(p, (int(x), int(base - p.height)))

x, bordes = 0, []
for p in atras:
    poner(p, x, base_atras); x += p.width + sep; bordes.append(x - sep / 2)
# adelante, cada uno centrado en el límite entre dos de atrás, así el del medio se ve entero
for p, c in zip(adelante, bordes[:2]):
    poner(p, c - p.width / 2, H - 16)
lienzo = lienzo.crop(lienzo.getbbox())
lienzo.save(os.path.join(CARPETA, "cinco-historia.png")); print(lienzo.size)
