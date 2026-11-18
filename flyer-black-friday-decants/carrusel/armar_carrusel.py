#!/usr/bin/env python3
"""Carrusel Black Friday de decants (19 al 21 de noviembre), todo en fondo vino.

Slide 1: portada con los decants y los dos precios.
Slides 2 a 7: una fragancia por slide, con el frasco original y al lado sus decants
de 5 y 10 ml (foto real del frasquito, con el color de ese perfume) y el precio de cada uno.
Slide 8: cierre con el WhatsApp.

Estilo editorial de herramientas/carrusel-bordo (estampilla bordó, Playfair, Pinyon Script, Poppins).

Uso: python3 flyer-black-friday-decants/carrusel/armar_carrusel.py
"""
import os
import sys

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..", "..")
sys.path.insert(0, os.path.join(RAIZ, "herramientas", "carrusel-bordo", "scripts"))
sys.path.insert(0, os.path.join(AQUI, "..", "fuente"))
import crear_carrusel as cc  # noqa: E402
from decants_vino import frasco  # noqa: E402

W, H = cc.W, cc.H
FOTOS = os.path.join(AQUI, "fotos")
SALIDA = AQUI

FECHAS = "19 al 21 de noviembre"
PRECIOS = [("5 ml", 45000, 5), ("10 ml", 90000, 10)]

# nombre, marca, tipo, notas, foto, color del perfume en el decant
FRAGANCIAS = [
    ("Libre", "Yves Saint Laurent", "Eau de Parfum",
     "Lavanda francesa y azahar sobre un fondo de vainilla.", "10-libre-x4.png", (238, 200, 140)),
    ("Scandal", "Jean Paul Gaultier", "Eau de Parfum",
     "Miel y gardenia: femenino, empolvado e irresistible.", "13-scandal-x4.png", (234, 168, 150)),
    ("Good Girl Blush", "Carolina Herrera", "Eau de Parfum",
     "La versión empolvada y suave de Good Girl, dulce y floral.", "good-girl-blush-x4.png", (246, 195, 190)),
    ("La Vie Est Belle", "Lancôme", "Eau de Parfum",
     "Iris, praliné y vainilla: el dulce más elegante.", "12-la-vie-est-belle-x4.png", (236, 160, 165)),
    ("J'adore", "Dior", "Eau de Parfum",
     "Un bouquet luminoso de jazmín y nardos. Clásico y sofisticado.", "11-jadore.jpg", (232, 190, 110)),
    ("La Bomba", "Carolina Herrera", "Eau de Parfum",
     "Vibrante y explosiva, con una frescura exótica que seduce.", "07-la-bomba.jpg", (226, 120, 150)),
]

PRINCIPAL = cc.MARFIL
SUAVE = cc.DORADO


def recorte_fino(ruta, umbral):
    """Recorta el fondo blanco con un umbral bajo, para frascos de vidrio casi blanco."""
    import numpy as np
    from PIL import ImageFilter
    im = Image.open(ruta).convert("RGB")
    b = im.copy()
    w, h = b.size
    marca = (1, 254, 3)
    for p in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]:
        if b.getpixel(p) != marca:
            ImageDraw.floodfill(b, p, marca, thresh=umbral)
    fuera = np.all(np.array(b) == marca, axis=-1)
    a = Image.fromarray(np.where(fuera, 0, 255).astype("uint8"))
    a = a.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.5))
    out = im.convert("RGBA")
    out.putalpha(a)
    return out.crop(a.getbbox())


def foto(ruta):
    """Recorte del frasco original (algunas fotos traen la caja: se recortan igual)."""
    if not os.path.exists(ruta):  # sin la versión agrandada, la original
        base, _ = os.path.splitext(ruta.replace("-x4", ""))
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            if os.path.exists(base + ext):
                ruta = base + ext
                break
    if os.path.basename(ruta).startswith("11-jadore"):
        # la caja de J'adore es blanca sobre blanco y no se recorta bien: solo el frasco
        im = Image.open(ruta).convert("RGB")
        recorte = os.path.join(FOTOS, "11-jadore-frasco.png")
        im.crop((int(im.width * 0.56), 0, im.width, im.height)).save(recorte)
        ruta = recorte
    if os.path.basename(ruta).startswith("10-libre"):
        # el vidrio de Libre es casi blanco: con el recorte común se come la base
        return recorte_fino(ruta, umbral=6), True
    prod, ok = cc.cargar_producto(ruta)
    if ok:
        # sobre vino se nota el filo blanco del recorte: se come 2 px del borde
        from PIL import ImageFilter
        a = prod.getchannel("A").filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(0.8))
        prod.putalpha(a)
    return prod, ok


def pegar(img, p, cx, base, alto_max, ancho_max):
    esc = min(alto_max / p.height, ancho_max / p.width)
    q = p.resize((max(1, int(p.width * esc)), max(1, int(p.height * esc))), Image.LANCZOS)
    cc.pegar_producto(img, q, (cx - q.width / 2, base - q.height, cx + q.width / 2, base), sombra_color=(0, 0, 0))
    return q.width, q.height


def cinta_fechas(img, y, ancho_linea=70):
    """BLACK FRIDAY · 19 AL 21 DE NOVIEMBRE, con dos líneas finas a los costados."""
    d = ImageDraw.Draw(img)
    f = cc.sans(20, "SemiBold")
    t = f"BLACK FRIDAY  ·  {FECHAS.upper()}"
    w = cc.ancho(d, t, f, 4)
    cc.escribir(d, W / 2, y, t, f, SUAVE, esp=4, ancla="ma")
    cy = y + 15
    d.line((W / 2 - w / 2 - 24 - ancho_linea, cy, W / 2 - w / 2 - 24, cy), fill=SUAVE, width=1)
    d.line((W / 2 + w / 2 + 24, cy, W / 2 + w / 2 + 24 + ancho_linea, cy), fill=SUAVE, width=1)


def slide_fragancia(n, nombre, marca, tipo, notas, archivo, color):
    img = Image.new("RGBA", (W, H), cc.CREMA + (255,))
    cc.estampilla(img)
    d = ImageDraw.Draw(img)
    cc.logo(img, W / 2, 70, 118, cc.CREMA)
    cinta_fechas(img, 128)

    # Nombre centrado (sin número) y la marca en cursiva debajo
    tam = 96
    while tam > 60 and cc.ancho(d, nombre, cc.serif(tam, 450)) > W - 220:
        tam -= 4
    f_tit = cc.serif(tam, 450)
    cc.escribir(d, W / 2, 205, nombre, f_tit, PRINCIPAL, ancla="ma")
    cc.escribir(d, W / 2, 205 + tam * 1.2, marca, cc.cursiva(66), SUAVE, ancla="ma")

    # producto a la izquierda, decants de 5 y 10 ml a la derecha
    base = 960
    prod, ok = foto(os.path.join(FOTOS, archivo))
    if ok:
        pegar(img, prod, 330, base, 470, 400)
    else:
        cc.tarjeta_foto(img, prod, (130, base - 470, 530, base), SUAVE)
    d = ImageDraw.Draw(img)
    d.line((W / 2 + 40, base - 380, W / 2 + 40, base + 90), fill=SUAVE, width=1)

    f_ml = cc.sans(19, "SemiBold")
    f_pr = cc.serif(31, 500)
    for cx, (ml, precio, cap) in zip((690, 900), PRECIOS):
        dec = frasco(color, cap)
        pegar(img, dec, cx, base, 430 * dec.height / frasco(color, 10).height, 200)
        d = ImageDraw.Draw(img)
        cc.escribir(d, cx, base + 22, ml.upper(), f_ml, SUAVE, esp=4, ancla="ma")
        cc.escribir(d, cx, base + 50, cc.guaranies(precio), f_pr, PRINCIPAL, ancla="ma")

    # tipo y notas
    cc.escribir(d, 330, base + 22, f"{tipo.upper()}", f_ml, SUAVE, esp=4, ancla="ma")
    f_notas = cc.serif_it(30, 400)
    y = 1128
    for l in cc.equilibrar(d, notas, f_notas, 780):
        cc.escribir(d, W / 2, y, l, f_notas, PRINCIPAL, ancla="ma")
        y += 40
    cc.pie(img, 1262, SUAVE)
    return img


def slide_portada():
    img = Image.new("RGBA", (W, H), cc.CREMA + (255,))
    cc.estampilla(img)
    d = ImageDraw.Draw(img)
    cc.logo(img, W / 2, 84, 230, cc.CREMA)

    cc.escribir(d, W / 2, 196, "Decants de perfume", cc.cursiva(76), SUAVE, ancla="ma")
    cc.escribir(d, W / 2, 268, "Black Friday", cc.serif(128, 450), PRINCIPAL, ancla="ma")
    f_f = cc.sans(24, "SemiBold")
    t = FECHAS.upper()
    w = cc.ancho(d, t, f_f, 6)
    cc.escribir(d, W / 2, 442, t, f_f, SUAVE, esp=6, ancla="ma")
    cy = 458
    d.line((W / 2 - w / 2 - 110, cy, W / 2 - w / 2 - 26, cy), fill=SUAVE, width=1)
    d.line((W / 2 + w / 2 + 26, cy, W / 2 + w / 2 + 110, cy), fill=SUAVE, width=1)

    # fila de decants, uno por fragancia, alternando 10 y 5 ml
    base = 930
    paso = 128
    for i, fr in enumerate(FRAGANCIAS):
        cap = 10 if i % 2 == 0 else 5
        dec = frasco(fr[5], cap)
        alto = 400 * dec.height / frasco(fr[5], 10).height
        pegar(img, dec, W / 2 + (i - 2.5) * paso, base, alto, 140)
    d = ImageDraw.Draw(img)

    # precios
    f_ml = cc.sans(22, "SemiBold")
    f_pr = cc.serif(60, 500)
    y = 990
    for k, (ml, precio, _) in enumerate(PRECIOS):
        cx = W / 2 + (k - 0.5) * 380
        cc.escribir(d, cx, y, ml.upper(), f_ml, SUAVE, esp=5, ancla="ma")
        cc.escribir(d, cx, y + 36, cc.guaranies(precio), f_pr, PRINCIPAL, ancla="ma")
    d.line((W / 2, y + 6, W / 2, y + 110), fill=SUAVE, width=1)

    f_pie = cc.sans(21, "SemiBold")
    tp = "DESLIZÁ Y ELEGÍ EL TUYO"
    wp = cc.ancho(d, tp, f_pie, 4)
    cc.escribir(d, W / 2 - 30, 1172, tp, f_pie, SUAVE, esp=4, ancla="ma")
    xa, ya = W / 2 - 30 + wp / 2 + 22, 1187
    d.line((xa, ya, xa + 44, ya), fill=SUAVE, width=2)
    d.line((xa + 34, ya - 8, xa + 44, ya), fill=SUAVE, width=2)
    d.line((xa + 34, ya + 8, xa + 44, ya), fill=SUAVE, width=2)
    cc.pie(img, 1262, SUAVE)
    return img


def slide_cierre():
    return cc.slide_cierre({
        "titulo": "Solo del 19 al 21",
        "cursiva": "de noviembre",
        "texto": "Todos los decants a un solo precio. Elegí tus favoritos:",
        "extras": ["5 ml · Gs. 45.000", "10 ml · Gs. 90.000", "Envíos a todo Paraguay"],
        "boton": "WhatsApp 0972 736 002",
        "debajo_boton": "o en el link de la bio",
    })


def main():
    slides = [slide_portada()]
    slides += [slide_fragancia(i, *fr) for i, fr in enumerate(FRAGANCIAS, 1)]
    slides.append(slide_cierre())
    for i, s in enumerate(slides, 1):
        ruta = os.path.join(SALIDA, f"{i:02d}.png")
        s.convert("RGB").save(ruta, optimize=True)
        print(ruta)


if __name__ == "__main__":
    main()
