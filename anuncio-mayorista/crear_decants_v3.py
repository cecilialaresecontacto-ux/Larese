#!/usr/bin/env python3
"""Venta mayorista de decants, hasta 40% off por unidad, en fondo NEGRO (lo pidió la dueña
el 20/11): diseño "de cartelera" inspirado en
la referencia que mandó la dueña el 20/11 (cortina de terciopelo, título en cursiva + recto,
producto sobre bandeja en mesa de mármol con reflejo, descuento al costado, recuadro de línea
fina abajo). Todo con la marca LARESE: paleta bordó, rosa marfil y dorado; Playfair, Pinyon y
Poppins; los decants reales del frasquito de la dueña.

Uso: python3 anuncio-mayorista/crear_decants_v3.py
Salida: decants-v3-post.png (1080x1350) y decants-v3-historia.png (1080x1920)
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..")
sys.path.insert(0, os.path.join(RAIZ, "herramientas", "pieza-marca", "scripts"))
sys.path.insert(0, os.path.join(RAIZ, "flyer-black-friday-decants", "fuente"))
import crear_pieza as cp  # noqa: E402
from decants_vino import frasco  # noqa: E402

FUENTES = os.path.join(RAIZ, "herramientas", "pieza-marca", "assets", "fonts")
BORDO = np.array([0x41, 0x03, 0x0B], float)
CUERO = np.array([0x2A, 0x0B, 0x0D], float)
TERCIOPELO = np.array([0x30, 0x2A, 0x2B], float)   # terciopelo negro: brillo gris cálido de los pliegues   # brillo del terciopelo (bordó más claro)
MARFIL = (0xFC, 0xE5, 0xDA)
DORADO = (0xEA, 0xCF, 0xA2)  # dorado claro: sobre el terciopelo rojo el dorado antiguo se pierde
random.seed(40)

# decants sobre la bandeja: (color, ml, dx relativo, fila 0 = atrás / 1 = adelante)
DECANTS = [((240, 175, 182), 10, -0.36, 0), ((205, 165, 222), 10, -0.12, 0), ((238, 200, 140), 10, 0.12, 0),
           ((196, 214, 234), 10, 0.36, 0), ((224, 108, 128), 5, -0.24, 1), ((226, 160, 98), 5, 0.0, 1),
           ((214, 150, 70), 5, 0.24, 1)]

MEDIDAS = {
    "post": dict(tam=(1080, 1350), logo=(72, 96, 170), venta=170, may=118, de=24, pct=104, x_pct=0.79,
                 y_tit=210, mesa=0.79, bandeja=560, alto_dec=300, x_band=0.33, caja=24, caja_y=0.885),
    "historia": dict(tam=(1080, 1920), logo=(72, 230, 200), venta=200, may=134, de=28, pct=118, x_pct=0.74,
                     y_tit=420, mesa=0.79, bandeja=640, alto_dec=400, x_band=0.34, caja=27, caja_y=0.855),
}


def playfair(tam, italica=False, peso=500):
    f = ImageFont.truetype(os.path.join(FUENTES, "PlayfairDisplay-Italic.ttf" if italica else "PlayfairDisplay.ttf"),
                           int(tam))
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f


def cortina(w, h):
    """Terciopelo bordó: pliegues verticales (suma de ondas), luz desde arriba a la derecha
    y viñeta oscura hacia la izquierda y abajo."""
    x = np.linspace(0, 1, w)
    pli = (0.55 * np.sin(x * 2 * math.pi * 5.3 + 0.7) + 0.30 * np.sin(x * 2 * math.pi * 11.1 + 2.1)
           + 0.15 * np.sin(x * 2 * math.pi * 23.7 + 0.3))
    pli = (pli - pli.min()) / (pli.max() - pli.min())
    pli = pli ** 1.8
    yy, xx = np.mgrid[0:h, 0:w] / np.array([h, w])[:, None, None]
    luz = np.exp(-(((xx - 0.68) / 0.55) ** 2 + ((yy - 0.18) / 0.65) ** 2))
    v = (pli[None, :] * 0.75 + 0.25) * (0.45 + 0.85 * luz)
    v = np.clip(v, 0, 1)[..., None]
    rgb = np.array([8, 6, 7], float) * (1 - v) + TERCIOPELO * v
    # viñeta: casi negro a la izquierda y abajo
    vin = np.clip(1.2 - 0.95 * np.sqrt(((xx - 0.55) / 0.8) ** 2 + ((yy - 0.4) / 1.0) ** 2), 0.3, 1)[..., None]
    rgb = rgb * vin
    img = Image.fromarray(rgb.clip(0, 255).astype("uint8"), "RGB")
    ruido = Image.effect_noise((w, h), 14).convert("RGB")
    return Image.blend(img, ruido, 0.025).convert("RGBA")


def marmol(w, h):
    """Mesa de mármol negro con vetas claras muy suaves y un brillo al fondo."""
    yy = np.linspace(0, 1, h)[:, None]
    g = (np.array([20, 17, 18]) * (1 - yy[..., None]) + np.array([3, 3, 3]) * yy[..., None])
    base = np.broadcast_to(g, (h, w, 3)).copy()
    img = Image.fromarray(base.astype("uint8"), "RGB").convert("RGBA")
    vetas = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(vetas)
    for _ in range(9):
        x0, y0 = random.uniform(-0.2, 1.0) * w, random.uniform(0, 1) * h
        pts = [(x0, y0)]
        for _ in range(8):
            x0 += random.uniform(40, 130)
            y0 += random.uniform(-30, 30)
            pts.append((x0, y0))
        d.line(pts, fill=random.randint(40, 90), width=random.randint(1, 3), joint="curve")
    vetas = vetas.filter(ImageFilter.GaussianBlur(1.2))
    img.alpha_composite(cp.capa_color(vetas, (200, 190, 185), 0.35))
    # brillo del borde de la mesa
    borde = Image.new("L", (w, h), 0)
    ImageDraw.Draw(borde).rectangle((0, 0, w, 3), fill=255)
    img.alpha_composite(cp.capa_color(borde.filter(ImageFilter.GaussianBlur(2)), (110, 100, 100), 0.6))
    return img


def aclarar(q):
    """Decant más luminoso sobre fondo oscuro: vidrio como velo claro más visible y
    perfume y tapa un poco más brillantes."""
    a = np.array(q).astype(float)
    alfa = a[..., 3]
    vidrio = (alfa > 8) & (alfa < 140)
    a[..., 3] = np.where(vidrio, np.maximum(alfa, 150), alfa)
    a[..., :3] = np.where(vidrio[..., None], a[..., :3] * 0.5 + 255 * 0.5, a[..., :3] * 1.18)
    return Image.fromarray(a.clip(0, 255).astype("uint8"), "RGBA")


def foco(img, cx, cy, rx, ry, fuerza):
    """Luz de escenario detrás del producto."""
    capa = Image.new("L", img.size, 0)
    ImageDraw.Draw(capa).ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    img.alpha_composite(cp.capa_color(capa.filter(ImageFilter.GaussianBlur(min(rx, ry) * 0.55)), (255, 230, 215), fuerza))


def bandeja_con_decants(ancho, alto_dec):
    """Bandeja dorada (elipse) con los decants arriba. Devuelve la capa y la y del apoyo."""
    W, H = int(ancho * 1.15), int(alto_dec * 1.6)
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    cx = W / 2
    ry = ancho * 0.085
    piso = H - ry * 1.4
    # bandeja: borde dorado, superficie oscura con reflejo
    d.ellipse((cx - ancho / 2, piso - ry, cx + ancho / 2, piso + ry), fill=(110, 82, 52, 255))
    d.ellipse((cx - ancho / 2 + 6, piso - ry + 5, cx + ancho / 2 - 6, piso + ry - 7), fill=(40, 26, 22, 255))
    brillo = Image.new("L", capa.size, 0)
    ImageDraw.Draw(brillo).arc((cx - ancho / 2 + 2, piso - ry + 1, cx + ancho / 2 - 2, piso + ry - 2),
                               200, 340, fill=255, width=3)
    capa.alpha_composite(cp.capa_color(brillo.filter(ImageFilter.GaussianBlur(1)), DORADO, 0.9))
    # canto de la bandeja
    d.rectangle((cx - ancho / 2, piso, cx + ancho / 2, piso + 10), fill=(0, 0, 0, 0))
    d.chord((cx - ancho / 2, piso - ry + 10, cx + ancho / 2, piso + ry + 10), 0, 180, fill=(70, 50, 34, 255))
    d.chord((cx - ancho / 2 + 6, piso - ry + 5, cx + ancho / 2 - 6, piso + ry - 7), 0, 180, fill=(40, 26, 22, 255))
    # decants: primero los de atrás
    for fila in (0, 1):
        for color, ml, dx, f in DECANTS:
            if f != fila:
                continue
            fr = frasco(color, ml)
            f10 = frasco(color, 10)
            h = alto_dec * fr.height / f10.height * (0.93 if fila == 0 else 1.0)
            q = aclarar(fr.resize((max(1, int(fr.width * h / fr.height)), int(h)), Image.LANCZOS))
            x = cx + dx * ancho * 0.92
            base = piso - ry * (0.35 if fila == 0 else -0.05)
            s = Image.new("L", capa.size, 0)
            ImageDraw.Draw(s).ellipse((x - q.width * 0.45, base - 6, x + q.width * 0.45, base + 8), fill=220)
            capa.alpha_composite(cp.capa_color(s.filter(ImageFilter.GaussianBlur(6)), (0, 0, 0), 0.7))
            capa.alpha_composite(q, (int(x - q.width / 2), int(base - q.height)))
    return capa, piso + ry + 10


def armar(formato):
    M = MEDIDAS[formato]
    W, H = M["tam"]
    img = cortina(W, H)
    y_mesa = int(H * M["mesa"])
    img.alpha_composite(marmol(W, H - y_mesa), (0, y_mesa))
    d = ImageDraw.Draw(img)

    # logo arriba a la izquierda, en crema
    lx, ly, lw = M["logo"]
    logo = cp.logo_mascara("texto", lw)
    img.alpha_composite(cp.capa_color(logo, cp.CREMA), (lx, ly))

    # bandeja con decants, apoyada en la mesa, con reflejo
    capa, apoyo = bandeja_con_decants(M["bandeja"], M["alto_dec"])
    bx = int(W * M["x_band"] - capa.width / 2)
    by = int(y_mesa + 30 - apoyo)
    foco(img, bx + capa.width / 2, by + apoyo - M["alto_dec"] * 0.55, M["bandeja"] * 0.62, M["alto_dec"] * 0.85, 0.45)
    sombra = capa.getchannel("A").filter(ImageFilter.GaussianBlur(20))
    img.alpha_composite(cp.capa_color(sombra, (0, 0, 0), 0.5), (bx + 14, by + 22))
    img.alpha_composite(capa, (bx, by))
    refl = capa.transpose(Image.FLIP_TOP_BOTTOM).crop((0, capa.height - int(apoyo), capa.width, capa.height))
    grad = Image.linear_gradient("L").resize(refl.size).point(lambda v: int((255 - v) * 0.22))
    a = Image.fromarray((np.array(refl.getchannel("A"), float) * np.array(grad, float) / 255).astype("uint8"))
    refl.putalpha(a)
    refl = refl.filter(ImageFilter.GaussianBlur(2))
    img.alpha_composite(refl, (bx, by + int(apoyo) - 2))

    # título: "Venta" en cursiva, "Mayorista" recto y corrido a la derecha, "DE DECANTS" chico
    d = ImageDraw.Draw(img)
    f_v = playfair(M["venta"], italica=True, peso=520)
    f_m = playfair(M["may"], peso=430)
    y = M["y_tit"]
    wv = d.textlength("Venta", font=f_v)
    xv = W * 0.18
    d.text((xv, y), "Venta", font=f_v, fill=MARFIL)
    y2 = y + M["venta"] * 0.95
    wm = d.textlength("Mayorista", font=f_m)
    xm = min(W - 60 - wm, xv + wv * 0.55)
    d.text((xm, y2), "Mayorista", font=f_m, fill=MARFIL)
    f_de = cp.fuente(M["de"], b"Medium")
    t_de = "DE DECANTS"
    w_de = cp.ancho_txt(d, t_de, f_de, M["de"] * 0.3)
    cp.txt(d, xm - 30 - w_de / 2, y2 + M["may"] * 0.55, t_de, f_de, MARFIL, esp=M["de"] * 0.3)

    # descuento a la derecha
    xp = W * M["x_pct"]
    yp = y2 + M["may"] * 1.75
    f_h = cp.cursiva(M["pct"] * 0.5)
    cp.txt(d, xp, yp - M["pct"] * 0.42, "hasta", f_h, DORADO)
    f_n = playfair(M["pct"], peso=480)
    f_o = playfair(M["pct"], italica=True, peso=480)
    t1, t2 = "40% ", "off"
    w1, w2 = d.textlength(t1, font=f_n), d.textlength(t2, font=f_o)
    x0 = xp - (w1 + w2) / 2
    d.text((x0, yp), t1, font=f_n, fill=MARFIL)
    d.text((x0 + w1, yp), t2, font=f_o, fill=MARFIL)
    f_u = cp.fuente(M["pct"] * 0.2, b"Medium")
    cp.txt(d, xp, yp + M["pct"] * 1.25, "por unidad, en cada decant", f_u, MARFIL)
    cp.txt(d, xp, yp + M["pct"] * 1.25 + M["pct"] * 0.32, "Árabes · Diseñador · Nicho", f_u, DORADO)

    # recuadro de línea fina con el WhatsApp
    f_c = cp.fuente(M["caja"], b"Medium")
    t_c = "PEDÍ LA LISTA MAYORISTA · WHATSAPP 0972 736 002"
    w_c = cp.ancho_txt(d, t_c, f_c, M["caja"] * 0.04)
    a_c = cp.alto_linea(f_c)
    yc = H * M["caja_y"]
    pad_x, pad_y = M["caja"] * 0.9, M["caja"] * 0.5
    caja = (W / 2 - w_c / 2 - pad_x, yc, W / 2 + w_c / 2 + pad_x, yc + a_c + 2 * pad_y)
    fondo_caja = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(fondo_caja).rectangle(caja, fill=(0, 0, 0, 120))
    img.alpha_composite(fondo_caja)
    d = ImageDraw.Draw(img)
    d.rectangle(caja, outline=MARFIL, width=2)
    cp.txt(d, W / 2, yc + pad_y - M["caja"] * 0.08, t_c, f_c, MARFIL, esp=M["caja"] * 0.04)
    f_e = cp.fuente(M["caja"] * 0.8, b"Medium")
    cp.txt(d, W / 2, caja[3] + M["caja"] * 0.8, "ENVÍOS A TODO PARAGUAY", f_e, DORADO, esp=M["caja"] * 0.25)
    return img.convert("RGB")


if __name__ == "__main__":
    for formato, nombre in (("post", "decants-v3-post.png"), ("historia", "decants-v3-historia.png")):
        ruta = os.path.join(AQUI, nombre)
        armar(formato).save(ruta, optimize=True)
        print(ruta)
