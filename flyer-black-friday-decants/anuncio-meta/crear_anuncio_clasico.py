#!/usr/bin/env python3
"""Anuncio de Meta del Black Friday con el diseño "clásico" que eligió la dueña (el del
Kit 3 Momentos: píldora arriba, título grande, línea de subtítulo, productos en fila con
sello redondo, precio grande, botón y pie), pasado a la paleta y tipografía de marca:
fondo blanco, bordó vino, rosa marfil, dorado; Playfair Display, Pinyon Script y Poppins.

Uso: python3 flyer-black-friday-decants/anuncio-meta/crear_anuncio_clasico.py
Salida: clasico-post.png (1080x1350) y clasico-historia.png (1080x1920)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "..")
sys.path.insert(0, os.path.join(BASE, "..", "herramientas", "pieza-marca", "scripts"))
sys.path.insert(0, os.path.join(BASE, "fuente"))
sys.path.insert(0, os.path.join(BASE, "historia-calendario"))
import crear_pieza as cp  # noqa: E402
from decants_vino import frasco  # noqa: E402
from armar import producto  # noqa: E402  (recorte con margen, de la historia calendario)

BLANCO = (255, 255, 255)
MARFIL = (0xFC, 0xE5, 0xDA)
DORADO = (0x99, 0x79, 0x57)

PILDORA = "YA ARRANCÓ · HASTA EL 30"
SUBTITULO = "PERFUMES ENTEROS Y DECANTS"
SELLO = ("hasta", "agotar", "STOCK")
CTA = "¡Pedí el tuyo!"

# fila de productos, de izquierda a derecha: (tipo, dato, alto relativo)
FILA = [
    ("foto", "p-coco-mademoiselle-x4.png", 0.84),
    ("decant", ((238, 200, 140), 10), 0.56),
    ("foto", "miss-dior-x4.png", 1.00),
    ("decant", ((205, 165, 222), 5), 0.56),
    ("foto", "s-jadore.jpg", 0.74),
]

MEDIDAS = {
    "post": dict(tam=(1080, 1350), logo_y=46, logo_w=190, pil=24, tit=(126,), sub=24, sello=112, sello_dy=0.75,
                 ml=21, pre=58, cta=32, pie=24, pie_y=50),
    "historia": dict(tam=(1080, 1920), logo_y=170, logo_w=250, pil=32, tit=(150, 150), sub=29, sello=140, sello_dy=0.25,
                     ml=26, pre=74, cta=42, pie=30, pie_y=190),
}


def imagen(tipo, dato):
    if tipo == "foto":
        return producto(dato)
    color, ml = dato
    return frasco(color, ml, claro=True)


def fila_productos(img, caja):
    """Productos en fila, apoyados en el mismo piso, con sombra suave."""
    x0, y0, x1, y1 = caja
    w, h = x1 - x0, y1 - y0
    imgs = [(imagen(t, d), k) for t, d, k in FILA]
    # el decant de 5 ml es más bajo que el de 10: se respeta la proporción
    altos = []
    for (t, d, k), (p, _) in zip(FILA, imgs):
        if t == "decant" and d[1] == 5:
            altos.append(h * k * p.height / frasco(d[0], 10, claro=True).height)
        else:
            altos.append(h * k)
    anchos = [p.width * a / p.height for (p, _), a in zip(imgs, altos)]
    sep = w * 0.012
    total = sum(anchos) + sep * (len(anchos) - 1)
    esc = min(1.0, w / total)
    x = (x0 + x1) / 2 - total * esc / 2
    base = y1
    for (p, _), a, an in zip(imgs, altos, anchos):
        q = p.resize((max(1, int(an * esc)), max(1, int(a * esc))), Image.LANCZOS)
        cx = x + q.width / 2
        s = Image.new("L", img.size, 0)
        sw = q.width * 0.9
        ImageDraw.Draw(s).ellipse((cx - sw / 2, base - 14, cx + sw / 2, base + 18), fill=170)
        img.alpha_composite(cp.capa_color(s.filter(ImageFilter.GaussianBlur(16)), (60, 20, 22), 0.4))
        img.alpha_composite(q, (int(x), int(base - q.height)))
        x += q.width + sep * esc


def sello(img, cx, cy, r):
    """Sello redondo rosa marfil con letras bordó (como el de REGALO de la referencia)."""
    s = Image.new("L", img.size, 0)
    ImageDraw.Draw(s).ellipse((cx - r, cy - r + 10, cx + r, cy + r + 10), fill=140)
    img.alpha_composite(cp.capa_color(s.filter(ImageFilter.GaussianBlur(16)), (60, 20, 22), 0.35))
    d = ImageDraw.Draw(img)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=MARFIL)
    f1 = cp.cursiva(r * 0.42)
    f2 = cp.fuente(r * 0.36, b"ExtraBold")
    cp.txt(d, cx, cy - r * 0.62, SELLO[0], f1, cp.BORDO)
    cp.txt(d, cx, cy - r * 0.30, SELLO[1], f1, cp.BORDO)
    cp.txt(d, cx, cy + r * 0.08, SELLO[2], f2, cp.BORDO)


def armar(formato):
    M = MEDIDAS[formato]
    W, H = M["tam"]
    img = Image.new("RGBA", (W, H), BLANCO + (255,))
    d = ImageDraw.Draw(img)
    cx = W / 2

    # logo
    logo = cp.logo_mascara("texto", M["logo_w"])
    img.alpha_composite(cp.capa_color(logo, cp.BORDO), (int(cx - logo.width / 2), M["logo_y"]))
    y = M["logo_y"] + logo.height + M["pil"] * 1.0

    # píldora rosa marfil
    f_p = cp.fuente(M["pil"], b"SemiBold")
    esp = M["pil"] * 0.1
    wp = cp.ancho_txt(d, PILDORA, f_p, esp)
    ap = cp.alto_linea(f_p)
    px, py = M["pil"] * 1.0, M["pil"] * 0.35
    d.rounded_rectangle((cx - wp / 2 - px, y, cx + wp / 2 + px, y + ap + 2 * py), radius=(ap + 2 * py) / 2, fill=MARFIL)
    cp.txt(d, cx, y + py - M["pil"] * 0.05, PILDORA, f_p, cp.BORDO, esp=esp)
    y += ap + 2 * py + M["pil"] * 0.5

    # título: BLACK FRIDAY en una línea (post) o en dos (historia)
    lineas = ["BLACK FRIDAY"] if len(M["tit"]) == 1 else ["BLACK", "FRIDAY"]
    for l, tam in zip(lineas, M["tit"]):
        f_t = cp.fuente(tam, b"ExtraBold")
        while cp.ancho_txt(d, l, f_t) > W - 90:
            tam -= 4
            f_t = cp.fuente(tam, b"ExtraBold")
        cp.txt(d, cx, y - tam * 0.1, l, f_t, cp.TINTA)
        y += cp.alto_linea(f_t, 0.86)
    f_s = cp.fuente(M["sub"], b"Medium")
    cp.txt(d, cx, y + M["sub"] * 0.2, SUBTITULO, f_s, cp.BORDO, esp=M["sub"] * 0.08)
    arriba = y + cp.alto_linea(f_s, 1.2) + H * 0.03

    # abajo: precios, botón y pie
    pie_y = H - M["pie_y"] - M["pie"] * 2.1
    alto_cta = cp.alto_linea(cp.fuente(M["cta"], b"SemiBold")) + M["cta"] * 0.9
    y_cta = pie_y - M["pie"] * 1.5 - alto_cta
    f_ml = cp.fuente(M["ml"], b"SemiBold")
    f_pr = cp.fuente(M["pre"], b"ExtraBold")
    alto_pre = cp.alto_linea(f_ml, 1.15) + cp.alto_linea(f_pr, 1.0)
    y_pre = y_cta - M["cta"] * 0.6 - alto_pre
    abajo = y_pre - H * 0.035

    # productos y sello
    cp.marca_de_agua(img, (arriba + abajo) / 2)
    fila_productos(img, (60, arriba + M["sello"] * 0.5, W - 60, abajo))
    r = M["sello"]
    sello(img, W - r - 34, arriba + r * M["sello_dy"], r)

    # precios
    d = ImageDraw.Draw(img)
    precios = [("DECANT 5 ML", 45000), ("DECANT 10 ML", 90000)]
    ancho = max(d.textlength(cp.guaranies(p), font=f_pr) for _, p in precios)
    sep = M["pre"] * 1.0
    for i, (ml, p) in enumerate(precios):
        x = cx + (i - 0.5) * (ancho + sep)
        cp.txt(d, x, y_pre, ml, f_ml, cp.MALVA, esp=M["ml"] * 0.15)
        cp.txt(d, x, y_pre + cp.alto_linea(f_ml, 1.15), cp.guaranies(p), f_pr, cp.TINTA)
    d.line((cx, y_pre + alto_pre * 0.1, cx, y_pre + alto_pre * 0.92), fill=DORADO, width=2)

    previo = (cp.BLANCO, cp.TEXTO)
    cp.BLANCO, cp.TEXTO = cp.CREMA, cp.TINTA
    try:
        cp.boton(img, cx, y_cta, CTA, M["cta"], cp.BORDO)
        cp.pie(img, pie_y, M["pie"], cp.BORDO)
    finally:
        cp.BLANCO, cp.TEXTO = previo
    return img.convert("RGB")


if __name__ == "__main__":
    for formato, nombre in (("post", "clasico-post.png"), ("historia", "clasico-historia.png")):
        ruta = os.path.join(AQUI, nombre)
        armar(formato).save(ruta, optimize=True)
        print(ruta)
