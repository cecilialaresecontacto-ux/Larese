#!/usr/bin/env python3
"""Anuncio de Meta: VENTA MAYORISTA DE DECANTS, hasta 40% de descuento por unidad
(lo pidió la dueña el 20/11, con ese porcentaje). Mismo diseño que crear.py (píldora,
título grande, fila de productos con sello, botón y pie), con una fila de decants de
colores y el descuento grande en lugar de la lista de beneficios.

Uso: python3 anuncio-mayorista/crear_decants.py
Salida: decants-post.png (1080x1350) y decants-historia.png (1080x1920)
"""
import os
import sys

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import crear as base  # noqa: E402
from crear import cp, fila_productos, sello, tilde  # noqa: E402

BLANCO, MARFIL, DORADO = base.BLANCO, base.MARFIL, base.DORADO

base.PILDORA = "PARA REVENDEDORAS Y EMPRENDEDORES"
TITULO = ["VENTA", "MAYORISTA"]
base.SUBTITULO = "DE DECANTS DE PERFUME · 5 Y 10 ML"
base.SELLO = ("precios", "especiales", "MAYORISTA")
# fila de decants de colores, alternando 10 y 5 ml
base.FILA = [("decant", (c, ml), 1.0) for c, ml in [
    ((240, 175, 182), 5), ((238, 200, 140), 10), ((205, 165, 222), 5), ((226, 160, 98), 10),
    ((224, 108, 128), 5), ((196, 214, 234), 10), ((214, 150, 70), 5),
]]
BENEFICIOS = ["Árabes, de diseñador y nicho", "Ideal para revender"]
CTA = "¡Pedí la lista mayorista!"

MEDIDAS = {
    "post": dict(tam=(1080, 1350), logo_y=46, logo_w=190, pil=22, tit=(112, 112), sub=21, sello=96, sello_dy=0.5,
                 hasta=30, pct=150, xun=40, ben=24, cta=32, pie=24, pie_y=50),
    "historia": dict(tam=(1080, 1920), logo_y=170, logo_w=250, pil=27, tit=(146, 146), sub=26, sello=118, sello_dy=0.5,
                     hasta=38, pct=200, xun=52, ben=30, cta=42, pie=30, pie_y=190),
}


def armar(formato):
    M = MEDIDAS[formato]
    W, H = M["tam"]
    img = Image.new("RGBA", (W, H), BLANCO + (255,))
    d = ImageDraw.Draw(img)
    cx = W / 2

    logo = cp.logo_mascara("texto", M["logo_w"])
    img.alpha_composite(cp.capa_color(logo, cp.BORDO), (int(cx - logo.width / 2), M["logo_y"]))
    y = M["logo_y"] + logo.height + M["pil"] * 1.0

    f_p = cp.fuente(M["pil"], b"SemiBold")
    esp = M["pil"] * 0.08
    wp = cp.ancho_txt(d, base.PILDORA, f_p, esp)
    ap = cp.alto_linea(f_p)
    px, py = M["pil"] * 1.0, M["pil"] * 0.38
    d.rounded_rectangle((cx - wp / 2 - px, y, cx + wp / 2 + px, y + ap + 2 * py), radius=(ap + 2 * py) / 2, fill=MARFIL)
    cp.txt(d, cx, y + py - M["pil"] * 0.05, base.PILDORA, f_p, cp.BORDO, esp=esp)
    y += ap + 2 * py + M["pil"] * 0.5

    for l, tam in zip(TITULO, M["tit"]):
        f_t = cp.fuente(tam, b"ExtraBold")
        while cp.ancho_txt(d, l, f_t) > W - 90:
            tam -= 4
            f_t = cp.fuente(tam, b"ExtraBold")
        cp.txt(d, cx, y - tam * 0.1, l, f_t, cp.TINTA)
        y += cp.alto_linea(f_t, 0.86)
    f_s = cp.fuente(M["sub"], b"Medium")
    cp.txt(d, cx, y + M["sub"] * 0.2, base.SUBTITULO, f_s, cp.BORDO, esp=M["sub"] * 0.08)
    arriba = y + cp.alto_linea(f_s, 1.2) + H * 0.02

    # ----- abajo: pie, botón, beneficios y el descuento grande -----
    pie_y = H - M["pie_y"] - M["pie"] * 2.1
    alto_cta = cp.alto_linea(cp.fuente(M["cta"], b"SemiBold")) + M["cta"] * 0.9
    y_cta = pie_y - M["pie"] * 1.5 - alto_cta
    f_b = cp.fuente(M["ben"], b"Medium")
    y_ben = y_cta - M["cta"] * 0.6 - cp.alto_linea(f_b, 1.3)
    f_h = cp.fuente(M["hasta"], b"SemiBold")
    f_pct = cp.fuente(M["pct"], b"ExtraBold")
    f_x = cp.cursiva(M["xun"])
    alto_desc = cp.alto_linea(f_h, 1.0) + cp.alto_linea(f_pct, 0.78) + M["xun"] * 0.2 + cp.alto_linea(f_x, 0.9)
    y_desc = y_ben - M["ben"] * 0.6 - alto_desc
    abajo = y_desc - H * 0.025

    cp.marca_de_agua(img, (arriba + abajo) / 2)
    fila_productos(img, (70, arriba + M["sello"] * 0.4, W - 70, abajo))
    r = M["sello"]
    sello(img, W - r - 34, arriba + r * M["sello_dy"], r)

    d = ImageDraw.Draw(img)
    # HASTA / 40% OFF / por unidad
    y = y_desc
    cp.txt(d, cx, y, "HASTA", f_h, cp.MALVA, esp=M["hasta"] * 0.4)
    y += cp.alto_linea(f_h, 1.0)
    cp.txt(d, cx, y - M["pct"] * 0.12, "40% OFF", f_pct, cp.BORDO)
    y += cp.alto_linea(f_pct, 0.78) + M["xun"] * 0.2
    cp.txt(d, cx, y, "por unidad, en cada decant", f_x, DORADO)

    # beneficios en una línea, con tildes
    rr = M["ben"] * 0.5
    sep = M["ben"] * 1.6
    anchos = [rr * 2.6 + cp.ancho_txt(d, b, f_b) for b in BENEFICIOS]
    x = cx - (sum(anchos) + sep * (len(anchos) - 1)) / 2
    cy = y_ben + cp.alto_linea(f_b) * 0.52
    for b, a in zip(BENEFICIOS, anchos):
        d.ellipse((x, cy - rr, x + 2 * rr, cy + rr), fill=cp.BORDO)
        tilde(d, x + rr, cy, rr * 0.75, cp.CREMA)
        d.text((x + rr * 2.6, y_ben), b, font=f_b, fill=cp.TINTA)
        x += a + sep

    previo = (cp.BLANCO, cp.TEXTO)
    cp.BLANCO, cp.TEXTO = cp.CREMA, cp.TINTA
    try:
        cp.boton(img, cx, y_cta, CTA, M["cta"], cp.BORDO)
        cp.pie(img, pie_y, M["pie"], cp.BORDO)
    finally:
        cp.BLANCO, cp.TEXTO = previo
    return img.convert("RGB")


if __name__ == "__main__":
    for formato, nombre in (("post", "decants-post.png"), ("historia", "decants-historia.png")):
        ruta = os.path.join(AQUI, nombre)
        armar(formato).save(ruta, optimize=True)
        print(ruta)
