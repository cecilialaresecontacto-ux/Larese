#!/usr/bin/env python3
"""Historia Black Friday estilo "calendario" (referencia que mandó la dueña el 18/11):
fondo blanco con la grilla de un calendario inclinada, tarjeta oscura con textura de
plástico, el día 19 marcado con fibra, los días 20 y 21 en la grilla y productos
inclinados alrededor. En lugar de un "% de descuento", los precios reales de los decants.

Paleta y tipografía de marca: bordó vino / bordó cuero, rosa marfil, dorado, tinta;
Playfair Display, Pinyon Script y Poppins.

Uso: python3 flyer-black-friday-decants/historia-calendario/armar.py
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..", "..")
sys.path.insert(0, os.path.join(RAIZ, "herramientas", "carrusel-bordo", "scripts"))
sys.path.insert(0, os.path.join(AQUI, "..", "fuente"))
sys.path.insert(0, os.path.join(AQUI, "..", "carrusel"))
import crear_carrusel as cc  # noqa: E402
from decants_vino import frasco  # noqa: E402
from armar_carrusel import FOTOS  # noqa: E402

W, H = 1080, 1920
BLANCO = (255, 255, 255)
GIRO = -8  # grados de inclinación de la grilla y la tarjeta
random.seed(19)


def girado(capa, grados):
    return capa.rotate(grados, resample=Image.BICUBIC, expand=True)


def grilla(img):
    """Líneas del calendario: celdas grandes, inclinadas."""
    capa = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    cx, cy = W, H
    for x in range(-6, 7):
        xx = cx + 140 + x * 420
        d.line((xx, 0, xx, H * 2), fill=cc.TINTA + (255,), width=3)
    for y in range(-6, 7):
        yy = cy + 90 + y * 600
        d.line((0, yy, W * 2, yy), fill=cc.TINTA + (255,), width=3)
    capa = capa.rotate(GIRO, resample=Image.BICUBIC, center=(cx, cy))
    img.alpha_composite(capa.crop((W - W // 2, H - H // 2, W + W // 2, H + H // 2)))


def textura_plastico(w, h, base):
    """Fondo de la tarjeta con brillos suaves, como un plástico arrugado."""
    t = Image.new("RGBA", (w, h), base + (255,))
    luz = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(luz)
    for _ in range(26):
        x0, y0 = random.uniform(-0.2, 1.1) * w, random.uniform(-0.1, 1.1) * h
        ang = random.uniform(0.6, 1.3)
        largo = random.uniform(0.25, 0.7) * w
        x1, y1 = x0 + math.cos(ang) * largo, y0 + math.sin(ang) * largo
        d.line((x0, y0, x1, y1), fill=random.randint(40, 120), width=random.randint(2, 9))
    luz = luz.filter(ImageFilter.GaussianBlur(6))
    brillo = Image.new("RGBA", (w, h), (255, 236, 236, 0))
    brillo.putalpha(luz.point(lambda v: int(v * 0.55)))
    t.alpha_composite(brillo)
    sombra = Image.new("L", (w, h), 0)
    ds = ImageDraw.Draw(sombra)
    for _ in range(14):
        x0, y0 = random.uniform(0, 1) * w, random.uniform(0, 1) * h
        ang = random.uniform(0.5, 1.4)
        largo = random.uniform(0.2, 0.5) * w
        ds.line((x0, y0, x0 + math.cos(ang) * largo, y0 + math.sin(ang) * largo), fill=110, width=random.randint(6, 16))
    sombra = sombra.filter(ImageFilter.GaussianBlur(10))
    osc = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    osc.putalpha(sombra.point(lambda v: int(v * 0.5)))
    t.alpha_composite(osc)
    return t


def circulo_fibra(d, caja, color, vueltas=3, ancho=7):
    """Círculo hecho a mano con fibra: varias vueltas un poco desparejas."""
    x0, y0, x1, y1 = caja
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    pts = []
    pasos = 140
    for i in range(int(pasos * (vueltas - 0.15))):
        t = i / pasos * 2 * math.pi - 0.4
        k = 1 + 0.05 * math.sin(t * 1.5 + 1) + 0.035 * (i / pasos)
        pts.append((cx + rx * k * math.cos(t), cy + ry * k * math.sin(t) - 6 * math.sin(t * 0.5)))
    d.line(pts, fill=color, width=ancho, joint="curve")


def tarjeta():
    w, h = 820, 780
    t = textura_plastico(w, h, cc.BORDO_CUERO)
    d = ImageDraw.Draw(t)
    # BLACK / FRIDAY
    f = cc.serif(122, 700)
    cc.escribir(d, 90, 80, "BLACK", f, cc.MARFIL)
    cc.escribir(d, 90, 205, "FRIDAY", f, cc.MARFIL)
    # el 19 marcado con fibra
    f19 = cc.sans(92, "SemiBold")
    x19 = 610
    cc.escribir(d, x19, 78, "19", f19, cc.MARFIL)
    w19 = cc.ancho(d, "19", f19)
    circulo_fibra(d, (x19 - 44, 72, x19 + w19 + 44, 204), cc.MARFIL, vueltas=2.6, ancho=6)
    cc.escribir(d, 92, 360, "al 21 de noviembre", cc.cursiva(70), cc.DORADO)

    # precios en lugar del porcentaje: etiqueta blanca chica + precio grande
    f_tag = cc.sans(30, "SemiBold")
    f_pr = cc.serif(82, 600)
    y = 490
    for ml, precio in (("5 ml", "45.000"), ("10 ml", "90.000")):
        tw = cc.ancho(d, ml, f_tag)
        d.rectangle((90, y + 34, 90 + tw + 32, y + 86), fill=BLANCO)
        cc.escribir(d, 106, y + 39, ml, f_tag, cc.BORDO_CUERO)
        cc.escribir(d, 90 + tw + 56, y, "Gs. " + precio, f_pr, BLANCO)
        y += 112
    return t


def producto(nombre):
    """Recorta el frasco de la foto. Antes le agrega un margen blanco: si el frasco toca el
    borde de la foto, el recorte empieza desde el frasco y deja una caja blanca."""
    import tempfile
    from PIL import ImageOps
    im = Image.open(os.path.join(FOTOS, nombre)).convert("RGB")
    if "jadore" in nombre:  # solo el frasco, sin la caja blanca
        im = im.crop((int(im.width * 0.56), 0, im.width, im.height))
    im = ImageOps.expand(im, border=max(im.size) // 12, fill=BLANCO)
    with tempfile.TemporaryDirectory() as tmp:
        ruta = os.path.join(tmp, "foto.png")
        im.save(ruta)
        p, _ = cc.cargar_producto(ruta)
        p.load()
    return p


def pegar_girado(img, p, cx, cy, alto, grados, sombra=True):
    esc = alto / p.height
    q = p.resize((max(1, int(p.width * esc)), int(alto)), Image.LANCZOS)
    q = girado(q, grados)
    x, y = int(cx - q.width / 2), int(cy - q.height / 2)
    if sombra:
        a = q.getchannel("A").filter(ImageFilter.GaussianBlur(18))
        s = Image.new("RGBA", q.size, (40, 10, 12, 0))
        s.putalpha(a.point(lambda v: int(v * 0.35)))
        img.alpha_composite(s, (x + 18, y + 26))
    img.alpha_composite(q, (x, y))


def armar():
    img = Image.new("RGBA", (W, H), BLANCO + (255,))
    grilla(img)
    d = ImageDraw.Draw(img)

    # días de la grilla
    f_dia = cc.sans(118, "Medium")
    cc.escribir(d, 80, 1500, "20", f_dia, cc.TINTA)
    cc.escribir(d, 830, 1470, "21", f_dia, cc.TINTA)

    # tarjeta inclinada
    t = girado(tarjeta(), -GIRO * -1)  # mismo giro que la grilla
    sombra = t.getchannel("A").filter(ImageFilter.GaussianBlur(24))
    s = Image.new("RGBA", t.size, (40, 10, 12, 0))
    s.putalpha(sombra.point(lambda v: int(v * 0.35)))
    tx, ty = int(W / 2 - t.width / 2 + 40), 540
    img.alpha_composite(s, (tx + 16, ty + 28))
    img.alpha_composite(t, (tx, ty))

    # logo
    cc.logo(img, W / 2, 230, 300, cc.BORDO)

    # productos alrededor
    coco = producto("p-coco-mademoiselle-x4.png")
    pegar_girado(img, coco, 125, 470, 440, 14)
    jadore = producto("s-jadore.jpg")
    pegar_girado(img, jadore, 965, 1215, 430, -16)
    d10 = frasco((240, 175, 182), 10, claro=True)
    d5 = frasco((226, 160, 98), 5, claro=True)
    pegar_girado(img, d10, 360, 1480, 340, 10)
    pegar_girado(img, d5, 520, 1525, 340 * d5.height / d10.height, -6)

    # píldora con el WhatsApp
    d = ImageDraw.Draw(img)
    f_p = cc.sans(34, "Medium")
    tp = "WhatsApp 0972 736 002"
    tw = cc.ancho(d, tp, f_p)
    cy = 1712
    d.rounded_rectangle((W / 2 - tw / 2 - 56, cy - 40, W / 2 + tw / 2 + 56, cy + 40), radius=40, fill=cc.MARFIL)
    bb = f_p.getbbox(tp)
    d.text((W / 2 - tw / 2, cy - (bb[1] + bb[3]) / 2), tp, font=f_p, fill=cc.BORDO)
    f_e = cc.serif_it(32)
    te = "Envíos a todo Paraguay"
    we = cc.ancho(d, te, f_e)
    d.rectangle((W / 2 - we / 2 - 16, cy + 54, W / 2 + we / 2 + 16, cy + 104), fill=BLANCO)
    cc.escribir(d, W / 2, cy + 58, te, f_e, cc.MALVA, ancla="ma")
    return img.convert("RGB")


if __name__ == "__main__":
    ruta = os.path.join(AQUI, "historia-calendario.png")
    armar().save(ruta, optimize=True)
    print(ruta)
