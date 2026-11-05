#!/usr/bin/env python3
"""Promo 2 x 30.000 de Ahylen Larese Patissier: historia (1080x1920) y post (1080x1350).
Fondo blanco, textos oscuros (marrón del logo) y acento menta del logo."""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES = os.path.join(AQUI, "..", "herramientas", "pieza-fondo-blanco", "assets", "fonts")
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

BLANCO = (255, 255, 255)
MARRON = (104, 66, 36)
GRIS = (120, 110, 100)
MENTA = (178, 220, 214)


def poppins(tam, peso="Bold"):
    return ImageFont.truetype(os.path.join(FUENTES, f"Poppins-{peso}.ttf"), tam)


from PIL import ImageFont  # noqa: E402


def logo(diam):
    cap = Image.open(os.path.join(AQUI, "logo-captura.png")).convert("RGB")
    cx, cy, r = 590, 1137, 384
    rec = cap.crop((cx - r, cy - r, cx + r, cy + r))
    escala = 4
    mask = Image.new("L", (2 * r * escala, 2 * r * escala), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 2 * r * escala - 1, 2 * r * escala - 1), fill=255)
    mask = mask.resize((2 * r, 2 * r), Image.LANCZOS)
    rec.putalpha(mask)
    return rec.resize((diam, diam), Image.LANCZOS)


def tarjeta(ruta, w, h, radio=36):
    foto = ImageOps.fit(Image.open(ruta).convert("RGB"), (w, h), Image.LANCZOS, centering=(0.5, 0.62))
    mask = Image.new("L", (w * 3, h * 3), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w * 3 - 1, h * 3 - 1), radio * 3, fill=255)
    foto.putalpha(mask.resize((w, h), Image.LANCZOS))
    return foto


def sombra(lienzo, x, y, w, h, radio=36):
    capa = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
    ImageDraw.Draw(capa).rounded_rectangle((x, y + 14, x + w, y + h + 14), radio, fill=(60, 40, 20, 60))
    lienzo.alpha_composite(capa.filter(ImageFilter.GaussianBlur(22)))


def centrado(d, y, texto, f, color, ancho=1080):
    w = d.textlength(texto, font=f)
    d.text(((ancho - w) / 2, y), texto, font=f, fill=color)


def pildora(d, y, texto, f, fondo, color, pad_x=44, alto=None):
    w = d.textlength(texto, font=f)
    bb = f.getbbox(texto)
    th = bb[3] - bb[1]
    alto = alto or th + 40
    x0 = (1080 - w) / 2 - pad_x
    d.rounded_rectangle((x0, y, 1080 - x0, y + alto), alto / 2, fill=fondo)
    d.text(((1080 - w) / 2, y + (alto - th) / 2 - bb[1]), texto, font=f, fill=color)
    return y + alto


def pieza(formato, salida):
    W, H = (1080, 1920) if formato == "historia" else (1080, 1350)
    hist = formato == "historia"
    im = Image.new("RGBA", (W, H), BLANCO + (255,))
    d = ImageDraw.Draw(im)

    # Logo
    diam = 260 if hist else 190
    y = 120 if hist else 50
    im.alpha_composite(logo(diam), ((W - diam) // 2, y))
    y += diam + (50 if hist else 30)

    # Titular
    pildora(d, y, "SOLO POR HOY", poppins(34 if hist else 28, "SemiBold"), MENTA, MARRON, alto=70 if hist else 58)
    y += (70 if hist else 58) + (30 if hist else 20)
    f_promo = poppins(118 if hist else 96, "ExtraBold")
    centrado(d, y, "PROMO 2 x", f_promo, MARRON)
    y += (130 if hist else 106)
    centrado(d, y, "Gs. 30.000", f_promo, MARRON)
    y += (170 if hist else 125)

    # Fotos
    gap = 36
    cw = (W - 2 * 72 - gap) // 2
    ch = 560 if hist else 430
    for i, (ruta, nombre) in enumerate([("red-velvet.jpg", "Red Velvet"), ("carrot-cake.jpg", "Carrot Cake")]):
        x = 72 + i * (cw + gap)
        sombra(im, x, y, cw, ch)
        im.alpha_composite(tarjeta(os.path.join(AQUI, ruta), cw, ch), (x, y))
        f_n = ImageFont.truetype(SERIF_IT, 62 if hist else 50)
        tw = d.textlength(nombre, font=f_n)
        d.text((x + (cw - tw) / 2, y + ch + (22 if hist else 14)), nombre, font=f_n, fill=MARRON)
    y += ch + (22 if hist else 14) + (62 if hist else 50) + (52 if hist else 26)

    # Stock + contacto
    centrado(d, y, "Hasta agotar stock", poppins(40 if hist else 32, "Medium"), GRIS)
    y += (40 if hist else 32) + (60 if hist else 24)
    fin = pildora(d, y, "Pedí la tuya: 0984 501 918", poppins(40 if hist else 32, "Bold"), MARRON, BLANCO,
                  alto=96 if hist else 76)
    centrado(d, fin + (30 if hist else 18), "@ahylaresepatissier", poppins(32 if hist else 26, "Medium"), GRIS)

    im.convert("RGB").save(salida, quality=95)
    print(salida, "último y =", fin)


if __name__ == "__main__":
    pieza("historia", os.path.join(AQUI, "historia-promo-tortas.png"))
    pieza("post", os.path.join(AQUI, "post-promo-tortas.png"))
