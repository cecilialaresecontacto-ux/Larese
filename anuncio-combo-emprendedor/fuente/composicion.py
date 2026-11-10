"""Arma combo.png con los 5 perfumes: 3 atrás separados y 2 adelante en los huecos."""
import os
from PIL import Image, ImageDraw, ImageFilter
CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = 900  # alto de referencia

def cargar(nombre, alto):
    p = Image.open(os.path.join(CARPETA, "recortes", f"{nombre}.png")).convert("RGBA")
    return p.resize((int(p.width * alto / p.height), int(alto)), Image.LANCZOS)

atras = [cargar("9pm-rebel", U * 0.80), cargar("asad-elixir", U * 0.92), cargar("bharara-king", U * 0.90)]
adelante = [cargar("club-de-nuit", U * 0.62), cargar("khamrah-qahwa", U * 0.62)]
hueco = int(adelante[0].width * 0.80)
W = sum(p.width for p in atras) + hueco * 2
base_atras = int(U * 0.92)
H = base_atras + int(U * 0.22)
lienzo = Image.new("RGBA", (W, H), (0, 0, 0, 0))

def sombra(x, y, ancho):
    s = Image.new("L", (W, H), 0)
    ImageDraw.Draw(s).ellipse((x + ancho * 0.1, y - 14, x + ancho * 0.9, y + 14), fill=120)
    s = s.filter(ImageFilter.GaussianBlur(14))
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0)); capa.putalpha(s)
    lienzo.alpha_composite(capa)

x, xs = 0, []
for p in atras:
    sombra(x, base_atras, p.width)
    lienzo.alpha_composite(p, (x, base_atras - p.height))
    xs.append(x); x += p.width + hueco
for i, p in enumerate(adelante):
    c = xs[i] + atras[i].width + hueco / 2
    px = int(c - p.width / 2)
    sombra(px, H - 16, p.width)
    lienzo.alpha_composite(p, (px, H - 16 - p.height))
lienzo = lienzo.crop(lienzo.getbbox())
lienzo.save(os.path.join(CARPETA, "combo.png"))
print(lienzo.size)
