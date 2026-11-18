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

    # [ 01 ]  Nombre  /  marca en cursiva
    izq, y_num = 110, 200
    f_num, f_cor = cc.serif(110, 380), cc.serif(140, 300)
    num = f"{n:02d}"
    cc.escribir(d, izq, y_num - 20, "[", f_cor, PRINCIPAL)
    xb = izq + cc.ancho(d, "[", f_cor) + 14
    cc.escribir(d, xb, y_num, num, f_num, PRINCIPAL)
    xb2 = xb + cc.ancho(d, num, f_num) + 14
    cc.escribir(d, xb2, y_num - 20, "]", f_cor, PRINCIPAL)
    x_tit = xb2 + cc.ancho(d, "]", f_cor) + 36
    tam = 72
    while True:
        f_tit = cc.serif(tam, 450)
        lineas = cc.envolver(d, nombre, f_tit, W - 100 - x_tit)
        if len(lineas) <= 2 or tam <= 48:
            break
        tam -= 4
    alto_l = tam * 1.12
    y_t = y_num + 84 - alto_l * len(lineas) / 2
    for i, l in enumerate(lineas):
        cc.escribir(d, x_tit, y_t + i * alto_l, l, f_tit, PRINCIPAL)
    y_marca = max(y_t + alto_l * len(lineas), y_num + 140) + 4
    cc.escribir(d, W - 100, y_marca, marca, cc.cursiva(60), SUAVE, ancla="ra")

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
