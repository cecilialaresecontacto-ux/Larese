"""Arma trio.png para la historia de apertura: J'adore atrás al centro, Omnia y Romance adelante."""
import os
from PIL import Image
CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def cargar(nombre, alto):
    p = Image.open(os.path.join(CARPETA, "recortes", f"{nombre}.png")).convert("RGBA")
    return p.resize((int(p.width * alto / p.height), alto), Image.LANCZOS)

jadore = cargar("jadore", 1000)
omnia = cargar("omnia", 470)
romance = cargar("romance", 560)
W = omnia.width + romance.width - 60
H = 1000 + 330
lienzo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
lienzo.alpha_composite(jadore, ((W - jadore.width) // 2, 0))
lienzo.alpha_composite(omnia, (0, H - omnia.height))
lienzo.alpha_composite(romance, (W - romance.width, H - romance.height))
lienzo.save(os.path.join(CARPETA, "trio.png"))
print(lienzo.size)
