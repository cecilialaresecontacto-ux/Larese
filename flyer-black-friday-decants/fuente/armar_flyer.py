#!/usr/bin/env python3
"""Flyer Black Friday de decants (19 al 21 de noviembre), fondo vino: 6 frascos con el
nombre de cada perfume al lado y el precio único (5 ml Gs. 45.000 · 10 ml Gs. 90.000).

Paleta y tipografía de marca (CLAUDE.md): fondo bordó vino, logo crema, títulos y
nombres en Playfair Display (rosa marfil), marcas en Pinyon Script dorado, textos chicos
en Poppins. Los frascos salen de la foto real del decant (decants_vino.py).
Reutiliza las piezas de herramientas/pieza-marca/scripts/crear_pieza.py.

Uso: python3 flyer-black-friday-decants/fuente/armar_flyer.py
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(CARPETA, "..", "herramientas", "pieza-marca", "scripts"))
import crear_pieza as cp  # noqa: E402
from decants_vino import frasco  # noqa: E402

DORADO = (0x99, 0x79, 0x57)
MARFIL = (0xFC, 0xE5, 0xDA)

# Cada frasco de la foto (de izquierda a derecha) con un perfume de color parecido.
# "\n" marca dónde corta el nombre.
# nombre, marca, color del perfume (los mismos que en el carrusel)
PERFUMES = [
    ("Miss Dior", "Dior", (240, 175, 182)),
    ("Libre", "Yves Saint Laurent", (238, 200, 140)),
    ("Addict\nPurple Glow", "Dior", (205, 165, 222)),
    ("Coco\nMademoiselle\nIntense", "Chanel", (226, 160, 98)),
    ("Sì Passione", "Armani", (224, 108, 128)),
    ("Light Blue", "Dolce & Gabbana", (214, 230, 242)),
]
PRECIOS = [("5 ml", 45000), ("10 ml", 90000)]

ETIQUETA = "Decants de perfume"
TITULO = "Black Friday"
SUBTITULO = "19 al 21 de noviembre"
CTA = "¡Pedí los tuyos!"


def frascos():
    return [frasco(color, 10) for _, _, color in PERFUMES]


def celda(img, frasco, nombre, marca, caja, M):
    x0, y0, x1, y1 = caja
    alto = (y1 - y0) * M["alto_frasco"]
    esc = alto / frasco.height
    f = cp.nitido(frasco.resize((int(frasco.width * esc), int(alto)), Image.LANCZOS), esc)
    fx = int(x0)
    fy = int(y0 + (y1 - y0 - f.height) / 2)
    sombra = Image.new("L", img.size, 0)
    sw = f.width * 0.9
    ImageDraw.Draw(sombra).ellipse((fx + (f.width - sw) / 2, fy + f.height - 10,
                                    fx + (f.width + sw) / 2, fy + f.height + 14), fill=150)
    img.alpha_composite(cp.capa_color(sombra.filter(ImageFilter.GaussianBlur(12)), (0, 0, 0), 0.45))
    img.alpha_composite(f, (fx, fy))

    # nombre (Playfair) y marca (Pinyon Script dorado) al lado del frasco
    d = ImageDraw.Draw(img)
    tx = fx + f.width + M["sep"]
    maxw = x1 - tx
    ln = nombre.split("\n")
    tam = M["nom"]
    while tam > M["nom"] * 0.6 and max(d.textlength(l, font=cp.fuente(tam, b"Bold")) for l in ln) > maxw:
        tam -= 1
    fn = cp.fuente(tam, b"Bold")
    tm = M["mar"]
    while tm > M["mar"] * 0.6 and d.textlength(marca, font=cp.cursiva(tm)) > maxw:
        tm -= 1
    fm = cp.cursiva(tm)
    alto_nom = cp.alto_linea(fn, 1.0)
    total = alto_nom * len(ln) + cp.alto_linea(fm, 0.9)
    y = fy + f.height * 0.56 - total / 2
    for l in ln:
        d.text((tx, y), l, font=fn, fill=MARFIL)
        y += alto_nom
    d.text((tx, y - tm * 0.05), marca, font=fm, fill=DORADO)


def bloque_precios(img, cx, y, M):
    """5 ml | 10 ml, cada uno con su precio en Playfair, separados por una línea dorada."""
    d = ImageDraw.Draw(img)
    fl = cp.fuente(M["ml"], b"Medium")
    fp = cp.fuente(M["pre"], b"Bold")
    ancho = max(d.textlength(cp.guaranies(p), font=fp) for _, p in PRECIOS)
    sep = M["pre"] * 1.1
    alto = cp.alto_linea(fl, 1.1) + cp.alto_linea(fp, 1.0)
    for i, (ml, p) in enumerate(PRECIOS):
        px = cx + (i - 0.5) * (ancho + sep)
        cp.txt(d, px, y, ml.upper(), fl, DORADO, esp=M["ml"] * 0.18)
        cp.txt(d, px, y + cp.alto_linea(fl, 1.1), cp.guaranies(p), fp, MARFIL)
    d.line((cx, y + alto * 0.12, cx, y + alto * 0.92), fill=DORADO, width=2)
    return y + alto


MEDIDAS = {
    "post": dict(tam=(1080, 1350), logo_w=200, logo_y=50, eti=54, tit=96, sub=24, cta=30, pie=23, pie_y=52,
                 margen=56, nom=31, mar=34, sep=16, gap_y=26, alto_frasco=0.95, ml=21, pre=50),
    "historia": dict(tam=(1080, 1920), logo_w=250, logo_y=170, eti=62, tit=116, sub=30, cta=40, pie=30, pie_y=190,
                     margen=44, nom=34, mar=38, sep=14, gap_y=60, alto_frasco=0.88, ml=26, pre=66),
}


def armar(formato):
    M = MEDIDAS[formato]
    w, h = M["tam"]
    img = Image.new("RGBA", (w, h), cp.BORDO + (255,))
    d = ImageDraw.Draw(img)
    cx = w / 2

    # arriba: logo bordó, etiqueta en cursiva, título Playfair, subtítulo Poppins
    logo = cp.logo_mascara("texto", M["logo_w"])
    img.alpha_composite(cp.capa_color(logo, cp.CREMA), (int(cx - logo.width / 2), M["logo_y"]))
    y = M["logo_y"] + logo.height + M["eti"] * 0.45
    fe = cp.cursiva(M["eti"])
    cp.txt(d, cx, y, ETIQUETA, fe, DORADO)
    y += cp.alto_linea(fe, 0.85)
    ft = cp.fuente(M["tit"], b"Bold")
    cp.txt(d, cx, y, TITULO, ft, MARFIL)
    y += cp.alto_linea(ft, 0.98)
    fs = cp.fuente(M["sub"], b"Medium")
    t = SUBTITULO.upper()
    cp.txt(d, cx, y, t, fs, DORADO, esp=M["sub"] * 0.12)
    wl = cp.ancho_txt(d, t, fs, M["sub"] * 0.12)
    ly = y + cp.alto_linea(fs) * 0.5
    d.line((cx - wl / 2 - 90, ly, cx - wl / 2 - 22, ly), fill=DORADO, width=1)
    d.line((cx + wl / 2 + 22, ly, cx + wl / 2 + 90, ly), fill=DORADO, width=1)
    arriba = y + cp.alto_linea(fs, 1.15) + h * 0.025

    # abajo: precios, botón y pie
    pie_y = h - M["pie_y"] - M["pie"] * 2.1
    alto_cta = cp.alto_linea(cp.fuente(M["cta"], b"SemiBold")) + M["cta"] * 0.9
    y_cta = pie_y - M["pie"] * 1.4 - alto_cta
    alto_pre = cp.alto_linea(cp.fuente(M["ml"], b"Medium"), 1.1) + cp.alto_linea(cp.fuente(M["pre"], b"Bold"), 1.0)
    y_pre = y_cta - M["cta"] * 0.6 - alto_pre
    abajo = y_pre - h * 0.02

    # medio: grilla de 3 columnas x 2 filas
    ancho_col = (w - 2 * M["margen"]) / 3
    alto_fila = (abajo - arriba - M["gap_y"]) / 2
    for i, (fr, (nombre, marca, _)) in enumerate(zip(frascos(), PERFUMES)):
        c, r = i % 3, i // 3
        x0 = M["margen"] + c * ancho_col
        y0 = arriba + r * (alto_fila + M["gap_y"])
        celda(img, fr, nombre, marca, (x0 + 6, y0, x0 + ancho_col - 8, y0 + alto_fila), M)

    bloque_precios(img, cx, y_pre, M)
    # sobre vino: botón y círculos del pie en rosa marfil, con letras e íconos bordó
    previo = (cp.BLANCO, cp.TEXTO)
    cp.BLANCO, cp.TEXTO = cp.BORDO, MARFIL
    try:
        cp.boton(img, cx, y_cta, CTA, M["cta"], MARFIL)
        cp.pie(img, pie_y, M["pie"], MARFIL)
    finally:
        cp.BLANCO, cp.TEXTO = previo
    return img.convert("RGB")


if __name__ == "__main__":
    for formato, nombre in (("post", "flyer-post.png"), ("historia", "flyer-historia.png")):
        ruta = os.path.join(CARPETA, nombre)
        armar(formato).save(ruta, "PNG")
        print(ruta)
