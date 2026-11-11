"""Arma cinco.png: los 4 árabes atrás (Liquid Brun · Odyssey Aqua · Bharara King · Club de Nuit)
y el Azzaro The Most Wanted Parfum adelante, al centro y más grande (es el gancho del combo)."""
import os
from PIL import Image, ImageDraw, ImageFilter
CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = 1000

def cargar(nombre, alto):
    p = Image.open(os.path.join(CARPETA, "recortes", f"{nombre}.png")).convert("RGBA")
    return p.resize((int(p.width * alto / p.height), int(alto)), Image.LANCZOS)

atras = [cargar("liquid-brun", 700), cargar("odyssey-aqua", 600), cargar("bharara-king", 680), cargar("club-de-nuit", 640)]
heroe = cargar("azzaro", 640)
sep = 14
W = sum(p.width for p in atras) + sep * (len(atras) - 1)
base_atras = 700
alto_total = base_atras + 380
lienzo = Image.new("RGBA", (W, alto_total), (0, 0, 0, 0))

def poner(p, x, base, sombra=110):
    s = Image.new("L", lienzo.size, 0)
    ImageDraw.Draw(s).ellipse((x + p.width * .1, base - 12, x + p.width * .9, base + 16), fill=sombra)
    capa = Image.new("RGBA", lienzo.size, (0, 0, 0, 0)); capa.putalpha(s.filter(ImageFilter.GaussianBlur(14)))
    lienzo.alpha_composite(capa)
    lienzo.alpha_composite(p, (int(x), int(base - p.height)))

x = 0
for p in atras:
    poner(p, x, base_atras); x += p.width + sep
poner(heroe, (W - heroe.width) / 2, alto_total - 20, sombra=150)
lienzo = lienzo.crop(lienzo.getbbox())
lienzo.save(os.path.join(CARPETA, "cinco.png")); print(lienzo.size)
