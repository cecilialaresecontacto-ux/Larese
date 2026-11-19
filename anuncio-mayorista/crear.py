#!/usr/bin/env python3
"""Anuncio de Meta para VENTA POR MAYOR (pedido de la dueña el 19/11), con el diseño
"clásico" que ella eligió (píldora, título grande, productos en fila con sello redondo,
botón y pie) y la paleta de marca en fondo blanco.

No lleva precios: la dueña no pasó la lista mayorista ni el mínimo de compra. El anuncio
lleva a WhatsApp a pedir la lista. Cuando haya precios, se agregan en BENEFICIOS o como
precio grande.

Uso: python3 anuncio-mayorista/crear.py
Salida: anuncio-post.png (1080x1350) y anuncio-historia.png (1080x1920)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "..", "flyer-black-friday-decants")
sys.path.insert(0, os.path.join(BASE, "..", "herramientas", "pieza-marca", "scripts"))
sys.path.insert(0, os.path.join(BASE, "fuente"))
sys.path.insert(0, os.path.join(BASE, "historia-calendario"))
import crear_pieza as cp  # noqa: E402
from decants_vino import frasco  # noqa: E402
from armar import producto  # noqa: E402  (recorte con margen, de la historia calendario)

BLANCO = (255, 255, 255)
MARFIL = (0xFC, 0xE5, 0xDA)
DORADO = (0x99, 0x79, 0x57)

PILDORA = "PARA REVENDEDORAS Y EMPRENDEDORES"
TITULO = ["VENTA", "MAYORISTA"]
SUBTITULO = "PERFUMES ÁRABES, DE DISEÑADOR Y DECANTS"
SELLO = ("precios", "especiales", "MAYORISTA")
BENEFICIOS = ["Precios especiales por cantidad", "Armá tu propio negocio de perfumes",
              "Variedad de marcas para tu catálogo"]
CTA = "¡Pedí la lista de precios!"

# fila de productos, de izquierda a derecha: (tipo, dato, alto relativo)
FILA = [
    ("foto", "a-khamrah-qahwa.png", 0.80),
    ("decant", ((228, 182, 110), 10), 0.60),
    ("foto", "a-club-de-nuit.png", 1.00),
    ("decant", ((240, 175, 182), 5), 0.60),
    ("foto", "a-asad-elixir.png", 0.76),
]

MEDIDAS = {
    "post": dict(tam=(1080, 1350), logo_y=46, logo_w=190, pil=22, tit=(118, 118), sub=22, sello=104, sello_dy=0.55,
                 ben=27, cta=32, pie=24, pie_y=50),
    "historia": dict(tam=(1080, 1920), logo_y=170, logo_w=250, pil=27, tit=(150, 150), sub=27, sello=120, sello_dy=0.62,
                     ben=34, cta=42, pie=30, pie_y=190),
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
    tam2 = r * 0.36
    while cp.ancho_txt(ImageDraw.Draw(img), SELLO[2], cp.fuente(tam2, b"ExtraBold")) > r * 1.55:
        tam2 -= 1
    f2 = cp.fuente(tam2, b"ExtraBold")
    cp.txt(d, cx, cy - r * 0.62, SELLO[0], f1, cp.BORDO)
    cp.txt(d, cx, cy - r * 0.30, SELLO[1], f1, cp.BORDO)
    cp.txt(d, cx, cy + r * 0.08, SELLO[2], f2, cp.BORDO)


def tilde(d, x, y, r, color):
    d.line([(x - r * 0.55, y), (x - r * 0.12, y + r * 0.45), (x + r * 0.6, y - r * 0.5)], fill=color,
           width=max(3, int(r * 0.22)), joint="curve")


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
    wp = cp.ancho_txt(d, PILDORA, f_p, esp)
    ap = cp.alto_linea(f_p)
    px, py = M["pil"] * 1.0, M["pil"] * 0.38
    d.rounded_rectangle((cx - wp / 2 - px, y, cx + wp / 2 + px, y + ap + 2 * py), radius=(ap + 2 * py) / 2, fill=MARFIL)
    cp.txt(d, cx, y + py - M["pil"] * 0.05, PILDORA, f_p, cp.BORDO, esp=esp)
    y += ap + 2 * py + M["pil"] * 0.5

    for l, tam in zip(TITULO, M["tit"]):
        f_t = cp.fuente(tam, b"ExtraBold")
        while cp.ancho_txt(d, l, f_t) > W - 90:
            tam -= 4
            f_t = cp.fuente(tam, b"ExtraBold")
        cp.txt(d, cx, y - tam * 0.1, l, f_t, cp.TINTA)
        y += cp.alto_linea(f_t, 0.86)
    f_s = cp.fuente(M["sub"], b"Medium")
    cp.txt(d, cx, y + M["sub"] * 0.2, SUBTITULO, f_s, cp.BORDO, esp=M["sub"] * 0.08)
    arriba = y + cp.alto_linea(f_s, 1.2) + H * 0.02

    # abajo: beneficios con tilde, botón y pie
    pie_y = H - M["pie_y"] - M["pie"] * 2.1
    alto_cta = cp.alto_linea(cp.fuente(M["cta"], b"SemiBold")) + M["cta"] * 0.9
    y_cta = pie_y - M["pie"] * 1.5 - alto_cta
    f_b = cp.fuente(M["ben"], b"Medium")
    paso = cp.alto_linea(f_b, 1.45)
    y_ben = y_cta - M["cta"] * 0.7 - paso * len(BENEFICIOS)
    abajo = y_ben - H * 0.03

    cp.marca_de_agua(img, (arriba + abajo) / 2)
    fila_productos(img, (60, arriba + M["sello"] * 0.45, W - 60, abajo))
    r = M["sello"]
    sello(img, W - r - 34, arriba + r * M["sello_dy"], r)

    d = ImageDraw.Draw(img)
    ancho = max(cp.ancho_txt(d, b, f_b) for b in BENEFICIOS)
    rr = M["ben"] * 0.55
    x0 = cx - (ancho + rr * 3) / 2
    yb = y_ben
    for b in BENEFICIOS:
        cy = yb + cp.alto_linea(f_b) * 0.52
        d.ellipse((x0 - rr, cy - rr, x0 + rr, cy + rr), fill=cp.BORDO)
        tilde(d, x0, cy, rr * 0.75, cp.CREMA)
        d.text((x0 + rr * 2, yb), b, font=f_b, fill=cp.TINTA)
        yb += paso

    previo = (cp.BLANCO, cp.TEXTO)
    cp.BLANCO, cp.TEXTO = cp.CREMA, cp.TINTA
    try:
        cp.boton(img, cx, y_cta, CTA, M["cta"], cp.BORDO)
        cp.pie(img, pie_y, M["pie"], cp.BORDO)
    finally:
        cp.BLANCO, cp.TEXTO = previo
    return img.convert("RGB")


if __name__ == "__main__":
    for formato, nombre in (("post", "anuncio-post.png"), ("historia", "anuncio-historia.png")):
        ruta = os.path.join(AQUI, nombre)
        armar(formato).save(ruta, optimize=True)
        print(ruta)
