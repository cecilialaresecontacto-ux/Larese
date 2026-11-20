#!/usr/bin/env python3
"""Venta mayorista de decants, hasta 40% OFF por unidad: diseño alternativo (la dueña pidió
"un diseño diferente" el 20/11). Fondo bordó vino con brillo dorado, decants agrupados en
abanico, etiqueta tipo ticket rosa marfil inclinada con el descuento, botón y pie claros.

Uso: python3 anuncio-mayorista/crear_decants_v2.py
Salida: decants-v2-post.png (1080x1350) y decants-v2-historia.png (1080x1920)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..")
sys.path.insert(0, os.path.join(RAIZ, "herramientas", "pieza-marca", "scripts"))
sys.path.insert(0, os.path.join(RAIZ, "flyer-black-friday-decants", "fuente"))
import crear_pieza as cp  # noqa: E402
from decants_vino import frasco  # noqa: E402

BORDO, CUERO = cp.BORDO, (0x2A, 0x0B, 0x0D)
MARFIL = (0xFC, 0xE5, 0xDA)
DORADO = (0x99, 0x79, 0x57)
DORADO_CLARO = (0xC9, 0xA9, 0x7C)

COLORES = [(214, 150, 70), (196, 214, 234), (224, 108, 128), (238, 200, 140), (240, 175, 182),
           (205, 165, 222), (226, 160, 98), (190, 214, 236), (230, 150, 172)]

MEDIDAS = {
    "post": dict(tam=(1080, 1350), top=48, logo=170, tit=104, cur=62, sub=22, alto_dec=420,
                 ticket=(560, 230), cta=32, pie=23, pie_y=48),
    "historia": dict(tam=(1080, 1920), top=175, logo=230, tit=124, cur=78, sub=27, alto_dec=620,
                     ticket=(660, 270), cta=40, pie=29, pie_y=190),
}


def fondo(w, h):
    """Bordó vino con un resplandor más claro al centro y bordes en bordó cuero."""
    img = Image.new("RGBA", (w, h), CUERO + (255,))
    luz = Image.new("L", (w, h), 0)
    ImageDraw.Draw(luz).ellipse((-w * 0.25, h * 0.08, w * 1.25, h * 0.95), fill=255)
    img.alpha_composite(cp.capa_color(luz.filter(ImageFilter.GaussianBlur(w * 0.18)), BORDO, 1.0))
    return img


def brillo(img, cx, cy, rx, ry, color, fuerza):
    capa = Image.new("L", img.size, 0)
    ImageDraw.Draw(capa).ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    img.alpha_composite(cp.capa_color(capa.filter(ImageFilter.GaussianBlur(min(rx, ry) * 0.5)), color, fuerza))


def destello(d, cx, cy, r, color):
    k = r * 0.22
    d.polygon([(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k),
               (cx, cy + r), (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k)], fill=color)


def abanico(img, cx, base, alto):
    """9 decants: el del centro más grande, los de los costados más chicos y un poco más arriba,
    dibujados de afuera hacia adentro para que se superpongan como un abanico."""
    n = len(COLORES)
    mitad = n // 2
    paso = min(alto * 0.30, (img.width - alto * 0.32) / (n - 1))
    orden = sorted(range(n), key=lambda i: -abs(i - mitad))
    for i in orden:
        k = abs(i - mitad)
        ml = 10 if k % 2 == 0 else 5
        f = frasco(COLORES[i], ml)
        f10 = frasco(COLORES[i], 10)
        esc = 1 - 0.085 * k
        h = alto * esc * f.height / f10.height
        q = f.resize((max(1, int(f.width * h / f.height)), int(h)), Image.LANCZOS)
        x = cx + (i - mitad) * paso
        y = base - k * alto * 0.035
        s = Image.new("L", img.size, 0)
        ImageDraw.Draw(s).ellipse((x - q.width * 0.5, y - 10, x + q.width * 0.5, y + 14), fill=200)
        img.alpha_composite(cp.capa_color(s.filter(ImageFilter.GaussianBlur(12)), (0, 0, 0), 0.55))
        img.alpha_composite(q, (int(x - q.width / 2), int(y - q.height)))


def ticket(tw, th, escala):
    """Etiqueta rosa marfil con muescas a los costados y línea punteada, con el descuento."""
    t = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rounded_rectangle((0, 0, tw - 1, th - 1), radius=int(th * 0.12), fill=MARFIL)
    r = th * 0.13
    for x in (0, tw):
        d.ellipse((x - r, th / 2 - r, x + r, th / 2 + r), fill=(0, 0, 0, 0))
    # línea punteada a la izquierda (talón del ticket)
    xl = tw * 0.2
    for y in range(int(th * 0.12), int(th * 0.88), int(th * 0.08)):
        d.line((xl, y, xl, y + th * 0.04), fill=DORADO, width=3)
    # talón: "por unidad" en vertical
    talon = Image.new("RGBA", (th, int(xl)), (0, 0, 0, 0))
    dt = ImageDraw.Draw(talon)
    f_t = cp.fuente(th * 0.11, b"SemiBold")
    cp.txt(dt, th / 2, xl * 0.30, "POR UNIDAD", f_t, BORDO, esp=th * 0.02)
    talon = talon.rotate(90, expand=True)
    t.alpha_composite(talon, (0, 0))
    # cuerpo: HASTA / 40% OFF / en cada decant
    cx = xl + (tw - xl) / 2
    f_h = cp.fuente(th * 0.13, b"SemiBold")
    tam_p = th * 0.50
    while ImageDraw.Draw(t).textlength("40% OFF", font=cp.fuente(tam_p, b"ExtraBold")) > (tw - xl) * 0.84:
        tam_p -= 1
    f_p = cp.fuente(tam_p, b"ExtraBold")
    f_c = cp.cursiva(th * 0.20)
    y = th * 0.07
    cp.txt(d, cx, y, "HASTA", f_h, cp.MALVA, esp=th * 0.04)
    y += cp.alto_linea(f_h, 0.95)
    cp.txt(d, cx, y - th * 0.07, "40% OFF", f_p, BORDO)
    y += cp.alto_linea(f_p, 0.72)
    cp.txt(d, cx, y, "en cada decant", f_c, BORDO)
    return t


def armar(formato):
    M = MEDIDAS[formato]
    W, H = M["tam"]
    img = fondo(W, H)
    d = ImageDraw.Draw(img)
    cx = W / 2

    # ----- arriba -----
    logo = cp.logo_mascara("texto", M["logo"])
    img.alpha_composite(cp.capa_color(logo, cp.CREMA), (int(cx - logo.width / 2), M["top"]))
    y = M["top"] + logo.height + M["tit"] * 0.25
    f_t = cp.fuente(M["tit"], b"ExtraBold")
    tam = M["tit"]
    while cp.ancho_txt(d, "VENTA MAYORISTA", f_t) > W - 80:
        tam -= 2
        f_t = cp.fuente(tam, b"ExtraBold")
    cp.txt(d, cx, y, "VENTA MAYORISTA", f_t, MARFIL)
    y += cp.alto_linea(f_t, 0.92)
    f_c = cp.cursiva(M["cur"])
    cp.txt(d, cx, y - M["cur"] * 0.25, "de decants de perfume", f_c, DORADO_CLARO)
    y += cp.alto_linea(f_c, 0.8)

    # ----- abajo (de abajo hacia arriba) -----
    pie_y = H - M["pie_y"] - M["pie"] * 2.1
    f_cta = cp.fuente(M["cta"], b"SemiBold")
    alto_cta = cp.alto_linea(f_cta) + M["cta"] * 0.9
    y_cta = pie_y - M["pie"] * 1.5 - alto_cta
    f_s = cp.fuente(M["sub"], b"SemiBold")
    y_sub = y_cta - M["cta"] * 0.7 - cp.alto_linea(f_s)
    tw, th = M["ticket"]

    # ----- medio: brillo, abanico de decants y ticket -----
    libre_arriba = y + 10
    base = y_sub - M["sub"] * 1.6 - th * 0.78   # el ticket queda justo encima del texto de abajo
    alto = min(M["alto_dec"], (base - libre_arriba) * 0.97)
    libre_abajo = base + th * 0.6
    brillo(img, cx, base - alto * 0.45, W * 0.42, alto * 0.62, DORADO_CLARO, 0.45)
    abanico(img, cx, base, alto)

    t = ticket(tw, th, 1).rotate(-5, resample=Image.BICUBIC, expand=True)
    sombra = t.getchannel("A").filter(ImageFilter.GaussianBlur(16))
    s = Image.new("RGBA", t.size, (0, 0, 0, 0))
    s.putalpha(sombra.point(lambda v: int(v * 0.5)))
    tx, ty = int(cx - t.width / 2), int(base - th * 0.35)
    img.alpha_composite(s, (tx + 10, ty + 18))
    img.alpha_composite(t, (tx, ty))

    d = ImageDraw.Draw(img)
    for fx, fy, r in [(0.10, 0.30, 14), (0.90, 0.26, 18), (0.06, 0.55, 9), (0.95, 0.52, 11), (0.82, 0.40, 7)]:
        destello(d, W * fx, libre_arriba + (libre_abajo - libre_arriba) * fy, r, DORADO_CLARO)

    # ÁRABES · DISEÑADOR · NICHO
    t_sub = "ÁRABES  ·  DISEÑADOR  ·  NICHO  ·  5 Y 10 ML"
    cp.txt(d, cx, y_sub, t_sub, f_s, DORADO_CLARO, esp=M["sub"] * 0.12)

    # botón y pie en rosa marfil con letras e íconos bordó
    previo = (cp.BLANCO, cp.TEXTO)
    cp.BLANCO, cp.TEXTO = BORDO, MARFIL
    try:
        cp.boton(img, cx, y_cta, "¡Pedí la lista mayorista!", M["cta"], MARFIL)
        cp.pie(img, pie_y, M["pie"], MARFIL)
    finally:
        cp.BLANCO, cp.TEXTO = previo
    return img.convert("RGB")


if __name__ == "__main__":
    for formato, nombre in (("post", "decants-v2-post.png"), ("historia", "decants-v2-historia.png")):
        ruta = os.path.join(AQUI, nombre)
        armar(formato).save(ruta, optimize=True)
        print(ruta)
