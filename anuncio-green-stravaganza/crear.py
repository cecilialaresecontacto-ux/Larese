#!/usr/bin/env python3
"""Anuncio de las notas de Valentino Born in Roma Green Stravaganza (Donna), pedido de la
dueña el 21/11. Mismo estilo que historia-top3 (fondo bordó, líneas en escuadra doradas,
logo arriba, isotipo abajo): el frasco grande al centro y sus tres notas alrededor, cada una
con un ícono dibujado. Notas y precios sacados de la página de la tienda.

Uso: python3 anuncio-green-stravaganza/crear.py
Salida: historia.png (1080x1920) y post.png (1080x1350)
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
from armar_carrusel import recorte_fino  # noqa: E402

BORDO = cp.BORDO
MARFIL = (0xFC, 0xE5, 0xDA)
DORADO = (0xD9, 0xBB, 0x8A)
VERDE = (0xB8, 0xD8, 0x7A)   # el verde del frasco, solo para un brillo suave detrás

# notas de la página: salida, corazón, fondo
NOTAS = [("SALIDA", "Té Lapsang\nSouchong", "te"), ("CORAZÓN", "Jazmín", "jazmin"), ("FONDO", "Vainilla", "vainilla")]
PRECIOS = [("5 ML", 70000), ("10 ML", 115000)]

MEDIDAS = {
    # frasco: (cx, base, alto); notas: (x etiqueta, y etiqueta, lado de la línea)
    "historia": dict(tam=(1080, 1920), logo=(190, 300), tit=96, cur=70, marca=26, y_tit=330,
                     frasco=(540, 1330, 640), notas=[(60, 740, "izq"), (60, 960, "izq"), (60, 1180, "izq")],
                     pre=(1430, 44, 22), iso=1640, glow=(540, 1050, 380, 420)),
    "post": dict(tam=(1080, 1350), logo=(50, 170), tit=78, cur=58, marca=22, y_tit=130,
                 frasco=(540, 1060, 560), notas=[(60, 440, "izq"), (60, 630, "izq"), (60, 820, "izq")],
                 pre=(1110, 38, 19), iso=None, glow=(540, 800, 330, 360)),
}


def icono(d, tipo, cx, cy, r, color):
    """Íconos de línea simples: hoja de té, flor de jazmín y flor/vaina de vainilla."""
    w = max(3, int(r * 0.09))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=2)
    k = r * 0.62
    if tipo == "te":  # hoja con nervadura
        pts = [(cx - k * 0.75, cy + k * 0.75)]
        for t in range(0, 181, 15):
            a = math.radians(t)
            pts.append((cx - k * 0.75 + (k * 1.5) * t / 180 + math.sin(a) * k * 0.45,
                        cy + k * 0.75 - (k * 1.5) * t / 180 + math.sin(a) * k * 0.45))
        for t in range(180, -1, -15):
            a = math.radians(t)
            pts.append((cx - k * 0.75 + (k * 1.5) * t / 180 - math.sin(a) * k * 0.45,
                        cy + k * 0.75 - (k * 1.5) * t / 180 - math.sin(a) * k * 0.45))
        d.line(pts, fill=color, width=w, joint="curve")
        d.line((cx - k * 0.75, cy + k * 0.75, cx + k * 0.75, cy - k * 0.75), fill=color, width=max(2, w - 1))
    elif tipo == "jazmin":  # flor de 5 pétalos
        for i in range(5):
            a = math.radians(-90 + i * 72)
            px, py = cx + math.cos(a) * k * 0.55, cy + math.sin(a) * k * 0.55
            d.ellipse((px - k * 0.38, py - k * 0.38, px + k * 0.38, py + k * 0.38), outline=color, width=w)
        d.ellipse((cx - k * 0.14, cy - k * 0.14, cx + k * 0.14, cy + k * 0.14), fill=color)
    else:  # vainilla: dos vainas cruzadas y una florcita
        for s in (-1, 1):
            d.line((cx - k * 0.8, cy + s * k * 0.15 + k * 0.5, cx + k * 0.8, cy + s * k * 0.15 - k * 0.5),
                   fill=color, width=w + 2)
        d.ellipse((cx + k * 0.25, cy - k * 0.85, cx + k * 0.75, cy - k * 0.35), outline=color, width=w)


def nota(img, x, y, etiqueta, texto, tipo, escala):
    d = ImageDraw.Draw(img)
    f_e = cp.fuente(22 * escala, b"SemiBold")
    f_t = cp.fuente(44 * escala, b"SemiBold")
    r = 34 * escala
    icono(d, tipo, x + r, y + r, r, DORADO)
    tx = x + r * 2 + 18 * escala
    cp_y = y + r * 0.1
    d.text((tx, cp_y - 4), etiqueta, font=f_e, fill=DORADO)
    yy = cp_y + cp.alto_linea(f_e, 1.0)
    fin = tx + d.textlength(etiqueta, font=f_e)
    for i, l in enumerate(texto.split("\n")):
        d.text((tx, yy - 6), l, font=f_t, fill=MARFIL)
        yy += cp.alto_linea(f_t, 0.95)
    return fin


def armar(formato):
    M = MEDIDAS[formato]
    W, H = M["tam"]
    esc = 1.0 if formato == "historia" else 0.85
    img = Image.new("RGBA", (W, H), BORDO + (255,))
    luz = Image.new("L", (W, H), 0)
    ImageDraw.Draw(luz).ellipse((-200, H * 0.15, W + 200, H * 0.9), fill=255)
    img.alpha_composite(cp.capa_color(luz.filter(ImageFilter.GaussianBlur(220)), (0x6A, 0x0E, 0x1A), 0.8))
    # GREEN STRAVAGANZA repetido muy suave
    capa = Image.new("L", (W, H), 0)
    dc = ImageDraw.Draw(capa)
    f = cp.fuente(130 * esc, b"ExtraBold")
    for i, y in enumerate(range(int(H * 0.30), int(H * 0.80), int(140 * esc))):
        dc.text((-150 - (i % 2) * 300, y), "STRAVAGANZA  " * 3, font=f, fill=255)
    img.alpha_composite(cp.capa_color(capa, (0x7A, 0x1A, 0x26), 0.30))

    d = ImageDraw.Draw(img)
    cx = W / 2
    ly, lw = M["logo"]
    logo = cp.logo_mascara("texto", lw)
    img.alpha_composite(cp.capa_color(logo, MARFIL), (int(cx - logo.width / 2), ly))

    # título
    y = M["y_tit"] if formato == "historia" else ly + logo.height + 30
    if formato == "historia":
        y = ly + logo.height + 50
    f_m = cp.fuente(M["marca"], b"SemiBold")
    cp.txt(d, cx, y, "VALENTINO · DONNA", f_m, DORADO, esp=M["marca"] * 0.35)
    y += cp.alto_linea(f_m, 1.3)
    f_t = cp.fuente(M["tit"], b"Bold")
    cp.txt(d, cx, y, "Born in Roma", f_t, MARFIL)
    y += cp.alto_linea(f_t, 0.92)
    f_c = cp.cursiva(M["cur"])
    cp.txt(d, cx, y - M["cur"] * 0.2, "Green Stravaganza", f_c, DORADO)

    # brillo verde suave y frasco
    gx, gy, rx, ry = M["glow"]
    g = Image.new("L", (W, H), 0)
    ImageDraw.Draw(g).ellipse((gx - rx, gy - ry, gx + rx, gy + ry), fill=255)
    img.alpha_composite(cp.capa_color(g.filter(ImageFilter.GaussianBlur(160)), VERDE, 0.28))
    p = recorte_fino(os.path.join(AQUI, "frasco-x4.png"), umbral=8)
    p.putalpha(p.getchannel("A").filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.5)))
    fx, base, alto = M["frasco"]
    q = p.resize((int(p.width * alto / p.height), int(alto)), Image.LANCZOS)
    q = q.rotate(-6, resample=Image.BICUBIC, expand=True)
    x, y0 = int(fx - q.width / 2 + 120 * esc), int(base - q.height)
    s = q.getchannel("A").filter(ImageFilter.GaussianBlur(30))
    img.alpha_composite(cp.capa_color(s, (20, 0, 4), 0.4), (x + 14, y0 + 26))
    img.alpha_composite(q, (x, y0))

    # notas a la izquierda y derecha, con la línea en escuadra que va hacia el frasco
    d = ImageDraw.Draw(img)
    borde_frasco = x + q.width * 0.12
    for (etq, txt, tipo), (nx, ny, _) in zip(NOTAS, M["notas"]):
        fin = nota(img, nx, ny, etq, txt, tipo, esc)
        # línea fina dorada desde la nota hacia el frasco
        yl = ny + 34 * esc
        if borde_frasco - fin > 40:
            d.line((fin + 16, yl, borde_frasco, yl), fill=DORADO, width=2)
            d.ellipse((borde_frasco - 5, yl - 5, borde_frasco + 5, yl + 5), fill=DORADO)

    # precios
    yp, tp, tm = M["pre"]
    d = ImageDraw.Draw(img)
    f_ml = cp.fuente(tm, b"SemiBold")
    f_pr = cp.fuente(tp, b"Bold")
    ancho = max(d.textlength(cp.guaranies(v), font=f_pr) for _, v in PRECIOS)
    for i, (ml, v) in enumerate(PRECIOS):
        px = cx + (i - 0.5) * (ancho + tp * 1.2)
        cp.txt(d, px, yp, "DECANT " + ml, f_ml, DORADO, esp=tm * 0.15)
        cp.txt(d, px, yp + cp.alto_linea(f_ml, 1.1), cp.guaranies(v), f_pr, MARFIL)
    d.line((cx, yp + 6, cx, yp + cp.alto_linea(f_ml, 1.1) + cp.alto_linea(f_pr, 0.9)), fill=DORADO, width=2)

    # botón y pie
    f_b = cp.fuente(34 * esc, b"SemiBold")
    tb = "¡Pedí el tuyo!"
    tw = d.textlength(tb, font=f_b)
    cyb = yp + cp.alto_linea(f_ml, 1.1) + cp.alto_linea(f_pr, 1.0) + 60 * esc
    d.rounded_rectangle((cx - tw / 2 - 50 * esc, cyb - 40 * esc, cx + tw / 2 + 50 * esc, cyb + 40 * esc),
                        radius=40 * esc, fill=MARFIL)
    bb = f_b.getbbox(tb)
    d.text((cx - tw / 2, cyb - (bb[1] + bb[3]) / 2), tb, font=f_b, fill=BORDO)
    f_pie = cp.fuente(24 * esc, b"Medium")
    cp.txt(d, cx, cyb + 70 * esc, "WhatsApp 0972 736 002  ·  Envíos a todo Paraguay", f_pie, DORADO)
    return img.convert("RGB")


if __name__ == "__main__":
    for formato in ("historia", "post"):
        ruta = os.path.join(AQUI, f"{formato}.png")
        armar(formato).save(ruta, optimize=True)
        print(ruta)
