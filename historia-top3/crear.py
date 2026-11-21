#!/usr/bin/env python3
"""Historia "top 3" (pedido de la dueña el 21/11, con una referencia de otra tienda):
tres frascos grandes e inclinados, cada uno con su nombre y una línea en escuadra,
fondo con "BLACK FRIDAY" repetido muy suave, una cinta curva con "ofertas · ofertas"
en dos esquinas, el logo arriba y el isotipo abajo. Todo con la paleta de marca
(bordó vino, rosa marfil, dorado) y las fuentes de marca.

Uso: python3 historia-top3/crear.py
Salida: historia-top3/historia.png (dama) e historia-caballero.png (1080x1920)
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..")
sys.path.insert(0, os.path.join(RAIZ, "herramientas", "pieza-marca", "scripts"))
sys.path.insert(0, os.path.join(RAIZ, "flyer-black-friday-decants", "carrusel"))
import crear_pieza as cp  # noqa: E402
from armar_carrusel import FOTOS, foto, recorte_fino  # noqa: E402

W, H = 1080, 1920
BORDO = cp.BORDO
MARFIL = (0xFC, 0xE5, 0xDA)
DORADO = (0xD9, 0xBB, 0x8A)
CINTA = (0xC9, 0xA9, 0x7C)

# (nombre en la etiqueta, foto, centro x, base y, alto, giro, etiqueta: x, y)
FRASCOS = [
    ("Born in Roma", "born-in-roma-donna-x4.png", 290, 1440, 500, 12, (120, 780)),
    ("Libre", "10-libre-x4.png", 540, 1250, 590, 0, (590, 580)),
    ("Coco\nMademoiselle", "p-coco-mademoiselle-x4.png", 800, 1440, 540, -12, (770, 720)),
]


def fondo():
    img = Image.new("RGBA", (W, H), BORDO + (255,))
    # leve luz al centro
    luz = Image.new("L", (W, H), 0)
    ImageDraw.Draw(luz).ellipse((-200, 300, W + 200, 1700), fill=255)
    img.alpha_composite(cp.capa_color(luz.filter(ImageFilter.GaussianBlur(220)), (0x6A, 0x0E, 0x1A), 0.8))
    # BLACK FRIDAY repetido, muy suave
    capa = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(capa)
    f = cp.fuente(150, b"ExtraBold")
    for i, y in enumerate(range(-40, 620, 150)):
        t = ("BLACK FRIDAY  " if i % 2 == 0 else "FRIDAY BLACK  ") * 3
        d.text((-180 - (i % 2) * 260, y), t, font=f, fill=255)
    img.alpha_composite(cp.capa_color(capa, (0x7A, 0x1A, 0x26), 0.38))
    return img


def cinta_curva(img, cx, cy, r, a0, a1, ancho, texto, reverso=False):
    """Cinta en arco (centro fuera de la imagen) con texto que sigue la curva."""
    d = ImageDraw.Draw(img)
    d.arc((cx - r, cy - r, cx + r, cy + r), a0, a1, fill=CINTA, width=ancho)
    f = cp.fuente(ancho * 0.52, b"SemiBold")
    rt = r - ancho / 2
    # reverso: el texto avanza en sentido contrario, con la parte de arriba de las letras
    # hacia afuera del arco (para que se lea derecho en la esquina de arriba)
    ang = math.radians(a1 if reverso else a0)
    i = 0
    while (math.radians(a0) < ang) if reverso else (ang < math.radians(a1)):
        ch = texto[i % len(texto)]
        w = d.textlength(ch, font=f)
        x = cx + rt * math.cos(ang)
        y = cy + rt * math.sin(ang)
        letra = Image.new("RGBA", (int(ancho * 1.2), int(ancho * 1.2)), (0, 0, 0, 0))
        ImageDraw.Draw(letra).text((letra.width / 2, letra.height / 2), ch, font=f, fill=BORDO + (255,), anchor="mm")
        giro = 90 - math.degrees(ang) if reverso else -math.degrees(ang) - 90
        letra = letra.rotate(giro, resample=Image.BICUBIC)
        img.alpha_composite(letra, (int(x - letra.width / 2), int(y - letra.height / 2)))
        ang += (-1 if reverso else 1) * (w + ancho * 0.03) / rt
        i += 1


def frasco_girado(img, nombre_foto, cx, base, alto, giro):
    if nombre_foto.startswith("profondo"):  # base de vidrio casi blanca: recorte fino
        p = recorte_fino(os.path.join(FOTOS, nombre_foto), umbral=5)
    else:
        p, ok = foto(os.path.join(FOTOS, nombre_foto))
    # se come el filo blanco del recorte, que sobre bordó se nota
    p.putalpha(p.getchannel("A").filter(ImageFilter.MinFilter(11)).filter(ImageFilter.GaussianBlur(3)))
    esc = alto / p.height
    q = p.resize((max(1, int(p.width * esc)), int(alto)), Image.LANCZOS)
    q = cp.nitido(q, esc)
    q = q.rotate(giro, resample=Image.BICUBIC, expand=True)
    x, y = int(cx - q.width / 2), int(base - q.height)
    s = q.getchannel("A").filter(ImageFilter.GaussianBlur(30))
    img.alpha_composite(cp.capa_color(s, (20, 0, 4), 0.35), (x + 10, y + 22))
    img.alpha_composite(q, (x, y))


def etiqueta(img, texto, x, y):
    """Nombre con una línea en escuadra (horizontal corta arriba y vertical hacia el frasco)."""
    d = ImageDraw.Draw(img)
    f = cp.fuente(42, b"SemiBold")
    lineas = texto.split("\n")
    al = cp.alto_linea(f, 0.95)
    d.line((x - 30, y + 8, x - 6, y + 8), fill=DORADO, width=3)
    d.line((x - 30, y + 8, x - 30, y + al * len(lineas) + 40), fill=DORADO, width=3)
    for i, l in enumerate(lineas):
        d.text((x, y + i * al - 8), l, font=f, fill=DORADO)


def armar():
    img = fondo()
    cinta_curva(img, -40, -20, 330, -5, 100, 64, "ofertas · ", reverso=True)
    cinta_curva(img, W + 40, H - 120, 330, 175, 280, 64, "ofertas · ")

    logo = cp.logo_mascara("texto", 400)
    img.alpha_composite(cp.capa_color(logo, MARFIL), (int(W / 2 - logo.width / 2), 250))
    d = ImageDraw.Draw(img)
    f_c = cp.cursiva(78)
    cp.txt(d, W / 2, 250 + logo.height + 10, "nuestros favoritos", f_c, DORADO)

    # luz rosa suave detrás del grupo
    luz = Image.new("L", (W, H), 0)
    ImageDraw.Draw(luz).ellipse((120, 780, 960, 1480), fill=255)
    img.alpha_composite(cp.capa_color(luz.filter(ImageFilter.GaussianBlur(140)), MARFIL, 0.22))
    # el del medio va atrás
    for i in (1, 0, 2):
        _, archivo, cx, base, alto, giro, _ = FRASCOS[i]
        frasco_girado(img, archivo, cx, base, alto, giro)
    for nombre, *_, (lx, ly) in FRASCOS:
        etiqueta(img, nombre, lx, ly)

    iso = Image.open(os.path.join(RAIZ, "marca", "logos", "isotipo-crema.png")).convert("RGBA")
    iso = iso.resize((150, int(iso.height * 150 / iso.width)), Image.LANCZOS)
    img.alpha_composite(iso, (int(W / 2 - iso.width / 2), 1600))
    return img.convert("RGB")


# versión caballero (pedido de la dueña el 21/11): frascos azules, que resaltan sobre el bordó
FRASCOS_CABALLERO = [
    ("Acqua di Giò\nProfondo", "profondo-frasco-x4.png", 285, 1440, 500, 12, (90, 760)),
    ("Sauvage", "p-sauvage-x4.png", 540, 1250, 600, 0, (590, 580)),
    ("Eros Parfum", "eros-frasco.png", 800, 1440, 500, -12, (760, 760)),
]

if __name__ == "__main__":
    for nombre, frascos in (("historia.png", FRASCOS), ("historia-caballero.png", FRASCOS_CABALLERO)):
        FRASCOS = frascos
        ruta = os.path.join(AQUI, nombre)
        armar().save(ruta, optimize=True)
        print(ruta)
