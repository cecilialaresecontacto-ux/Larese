#!/usr/bin/env python3
"""Anuncio de Meta del Black Friday (pedido de la dueña el 19/11: "más emocionante",
anunciando perfumes enteros y decants). Fondo blanco con la paleta de marca.

Arriba: YA ARRANCÓ EL / BLACK FRIDAY / Perfumes enteros y decants / HASTA EL 30 O AGOTAR STOCK.
Medio: frascos enteros en grupo, con los decants adelante, luz suave y destellos dorados.
Abajo: precios de los decants (los de los frascos enteros no están confirmados: no van),
botón y pie.

Uso: python3 flyer-black-friday-decants/anuncio-meta/crear_anuncio.py
Salida: anuncio-post.png (1080x1350) y anuncio-historia.png (1080x1920)
"""
import math
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
DORADO = (0x99, 0x79, 0x57)
MARFIL = (0xFC, 0xE5, 0xDA)

# frascos enteros, de afuera hacia el centro: (foto, alto relativo)
ENTEROS = [
    ("s-erba-pura.jpg", 0.70),        # izquierda afuera
    ("p-coco-mademoiselle-x4.png", 0.84),
    ("miss-dior-x4.png", 1.00),       # centro
    ("s-jadore.jpg", 0.86),
    ("p-si-passione-x4.png", 0.72),   # derecha afuera
]
# decants adelante: (color, ml)
DECANTS = [((238, 200, 140), 10), ((240, 175, 182), 5), ((205, 165, 222), 10), ((226, 160, 98), 5)]

MEDIDAS = {
    "post": dict(tam=(1080, 1350), logo_y=44, logo_w=180, ya=25, tit=124, cur=56, pill=24,
                 pre=54, ml=20, cta=30, pie=23, pie_y=50),
    "historia": dict(tam=(1080, 1920), logo_y=170, logo_w=230, ya=30, tit=140, cur=66, pill=29,
                     pre=70, ml=25, cta=40, pie=30, pie_y=190),
}


def destello(d, cx, cy, r, color):
    """Brillito de cuatro puntas."""
    k = r * 0.22
    d.polygon([(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k),
               (cx, cy + r), (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k)], fill=color)


def luz(img, cx, cy, rx, ry, desde_y):
    """Resplandor rosa marfil muy suave detrás de los frascos (no sube más allá de desde_y,
    para no lavar los textos de arriba)."""
    capa = Image.new("L", img.size, 0)
    ImageDraw.Draw(capa).ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    capa = capa.filter(ImageFilter.GaussianBlur(min(rx, ry) * 0.45))
    corte = Image.new("L", img.size, 0)
    ImageDraw.Draw(corte).rectangle((0, desde_y, img.width, img.height), fill=255)
    corte = corte.filter(ImageFilter.GaussianBlur(30))
    from PIL import ImageChops
    capa = ImageChops.multiply(capa, corte)
    img.alpha_composite(cp.capa_color(capa, MARFIL, 0.85))


def pegar(img, p, cx, base, alto, sombra=True):
    esc = alto / p.height
    q = p.resize((max(1, int(p.width * esc)), int(alto)), Image.LANCZOS)
    x, y = int(cx - q.width / 2), int(base - q.height)
    if sombra:
        s = Image.new("L", img.size, 0)
        sw = q.width * 0.85
        ImageDraw.Draw(s).ellipse((cx - sw / 2, base - 12, cx + sw / 2, base + 16), fill=170)
        img.alpha_composite(cp.capa_color(s.filter(ImageFilter.GaussianBlur(14)), (60, 20, 22), 0.45))
    img.alpha_composite(q, (x, y))
    return q.width


def heroe(img, caja):
    x0, y0, x1, y1 = caja
    w, h = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2
    luz(img, cx, y0 + h * 0.52, w * 0.55, h * 0.48, y0 + 10)

    # frascos enteros: los de afuera primero, el del centro al final
    alto_max = h * 0.74
    base_ent = y0 + h * 0.78
    fotos = [(producto(f), k) for f, k in ENTEROS]
    anchos = [p.width * alto_max * k / p.height for p, k in fotos]
    solape = 0.18
    total = sum(anchos) - solape * sum(anchos[1:])
    if total > w * 0.98:  # que entren todos
        alto_max *= w * 0.98 / total
        anchos = [a * w * 0.98 / total for a in anchos]
        total = w * 0.98
    xs, x = [], cx - total / 2
    for i, a in enumerate(anchos):
        if i:
            x -= a * solape
        xs.append(x + a / 2)
        x += a
    orden = [0, 4, 1, 3, 2]
    for i in orden:
        p, k = fotos[i]
        pegar(img, p, xs[i], base_ent - (1 - k) * h * 0.05, alto_max * k)

    # decants adelante
    alto_d = h * 0.40
    base_d = y1
    paso = w * 0.15
    for i, (color, ml) in enumerate(DECANTS):
        f = frasco(color, ml, claro=True)
        f10 = frasco(color, 10, claro=True)
        pegar(img, f, cx + (i - 1.5) * paso, base_d, alto_d * f.height / f10.height)

    # destellos dorados
    d = ImageDraw.Draw(img)
    for fx, fy, r in [(0.06, 0.12, 16), (0.93, 0.08, 20), (0.02, 0.45, 10), (0.98, 0.40, 12),
                      (0.50, 0.03, 12), (0.03, 0.80, 9), (0.97, 0.74, 14)]:
        destello(d, x0 + w * fx, y0 + h * fy, r, DORADO)


def armar(formato):
    M = MEDIDAS[formato]
    W, H = M["tam"]
    img = Image.new("RGBA", (W, H), BLANCO + (255,))
    d = ImageDraw.Draw(img)
    cx = W / 2

    # ----- arriba -----
    logo = cp.logo_mascara("texto", M["logo_w"])
    img.alpha_composite(cp.capa_color(logo, cp.BORDO), (int(cx - logo.width / 2), M["logo_y"]))
    y = M["logo_y"] + logo.height + M["ya"] * 1.2
    f_ya = cp.fuente(M["ya"], b"SemiBold")
    cp.txt(d, cx, y, "YA ARRANCÓ EL", f_ya, cp.BORDO, esp=M["ya"] * 0.3)
    y += cp.alto_linea(f_ya, 1.0)
    f_t = cp.fuente(M["tit"], b"ExtraBold")
    tam = M["tit"]
    while cp.ancho_txt(d, "BLACK FRIDAY", f_t) > W - 90:
        tam -= 4
        f_t = cp.fuente(tam, b"ExtraBold")
    cp.txt(d, cx, y - tam * 0.12, "BLACK FRIDAY", f_t, cp.BORDO)
    y += cp.alto_linea(f_t, 0.92)
    f_c = cp.cursiva(M["cur"])
    cp.txt(d, cx, y - M["cur"] * 0.2, "Perfumes enteros y decants", f_c, DORADO)
    y += cp.alto_linea(f_c, 0.8) + M["pill"] * 0.4
    # píldora bordó llena: HASTA EL 30 O AGOTAR STOCK
    f_p = cp.fuente(M["pill"], b"SemiBold")
    t = "HASTA EL 30 O AGOTAR STOCK"
    esp = M["pill"] * 0.14
    wp = cp.ancho_txt(d, t, f_p, esp)
    ap = cp.alto_linea(f_p)
    px, py = M["pill"] * 1.2, M["pill"] * 0.5
    d.rounded_rectangle((cx - wp / 2 - px, y, cx + wp / 2 + px, y + ap + 2 * py), radius=(ap + 2 * py) / 2, fill=cp.BORDO)
    cp.txt(d, cx, y + py - M["pill"] * 0.05, t, f_p, MARFIL, esp=esp)
    arriba = y + ap + 2 * py + H * 0.02

    # ----- abajo -----
    pie_y = H - M["pie_y"] - M["pie"] * 2.1
    alto_cta = cp.alto_linea(cp.fuente(M["cta"], b"SemiBold")) + M["cta"] * 0.9
    y_cta = pie_y - M["pie"] * 1.4 - alto_cta
    f_ml = cp.fuente(M["ml"], b"SemiBold")
    f_pr = cp.fuente(M["pre"], b"Bold")
    alto_pre = cp.alto_linea(f_ml, 1.1) + cp.alto_linea(f_pr, 1.0)
    y_pre = y_cta - M["cta"] * 0.55 - alto_pre
    abajo = y_pre - H * 0.025

    heroe(img, (40, arriba, W - 40, abajo))

    # precios de los decants
    d = ImageDraw.Draw(img)
    precios = [("DECANT 5 ML", 45000), ("DECANT 10 ML", 90000)]
    ancho = max(d.textlength(cp.guaranies(p), font=f_pr) for _, p in precios)
    sep = M["pre"] * 1.1
    for i, (ml, p) in enumerate(precios):
        x = cx + (i - 0.5) * (ancho + sep)
        cp.txt(d, x, y_pre, ml, f_ml, cp.MALVA, esp=M["ml"] * 0.18)
        cp.txt(d, x, y_pre + cp.alto_linea(f_ml, 1.1), cp.guaranies(p), f_pr, cp.BORDO)
    d.line((cx, y_pre + alto_pre * 0.12, cx, y_pre + alto_pre * 0.92), fill=DORADO, width=2)

    previo = (cp.BLANCO, cp.TEXTO)
    cp.BLANCO, cp.TEXTO = cp.CREMA, cp.BORDO
    try:
        cp.boton(img, cx, y_cta, "¡Escribinos y reservá el tuyo!", M["cta"], cp.BORDO)
        cp.pie(img, pie_y, M["pie"], cp.BORDO)
    finally:
        cp.BLANCO, cp.TEXTO = previo
    return img.convert("RGB")


if __name__ == "__main__":
    for formato, nombre in (("post", "anuncio-post.png"), ("historia", "anuncio-historia.png")):
        ruta = os.path.join(AQUI, nombre)
        armar(formato).save(ruta, optimize=True)
        print(ruta)
