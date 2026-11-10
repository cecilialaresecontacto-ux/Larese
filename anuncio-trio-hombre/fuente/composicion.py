"""Arma trio.png en fila: frasco de Profondo, Born in Roma Intense (con caja) y Le Beau Le Parfum (con lata)."""
import os
from PIL import Image, ImageDraw, ImageFilter
CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def cargar(nombre, alto, recorte_x=None):
    p = Image.open(os.path.join(CARPETA, "recortes", f"{nombre}.png")).convert("RGBA")
    if recorte_x:
        p = p.crop((recorte_x, 0, p.width, p.height)); p = p.crop(p.getbbox())
    return p.resize((int(p.width * alto / p.height), int(alto)), Image.LANCZOS)

piezas = [cargar("acqua-di-gio-profondo-2", 780),
          cargar("born-in-roma-intense", 760),
          cargar("le-beau-le-parfum", 780)]
sep = 50
W = sum(p.width for p in piezas) + sep * 2
H = max(p.height for p in piezas) + 20
lienzo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
x = 0
for p in piezas:
    s = Image.new("L", (W, H), 0)
    ImageDraw.Draw(s).ellipse((x + p.width * 0.1, H - 34, x + p.width * 0.9, H - 6), fill=120)
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0)); capa.putalpha(s.filter(ImageFilter.GaussianBlur(12)))
    lienzo.alpha_composite(capa)
    lienzo.alpha_composite(p, (x, H - 20 - p.height))
    x += p.width + sep
lienzo = lienzo.crop(lienzo.getbbox())
lienzo.save(os.path.join(CARPETA, "trio.png"))
print(lienzo.size)
