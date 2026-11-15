#!/usr/bin/env python3
"""Dibuja 6 frasquitos de decant genéricos (sin marcas) para la versión del anuncio que no muestra
frascos de las marcas. Salida: fuente/decants-sin-marca.png (PNG transparente)."""
import os
from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
K = 4  # se dibuja grande y se achica para bordes suaves
VW, VH, GAP = 112, 520, 40  # medidas de cada frasquito (antes de achicar)
LIQUIDOS = [(232, 168, 160), (214, 160, 92), (246, 205, 196), (190, 120, 110), (236, 196, 130), (226, 150, 170)]
DORADO = (196, 163, 122)
VIDRIO = (252, 229, 218)


def frasco(liquido):
    w, h = VW * K, VH * K
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    tapa_h = int(h * 0.22)
    cuello_h = int(h * 0.05)
    cuerpo_y = tapa_h + cuello_h
    r = int(w * 0.18)
    # tapa dorada con brillo
    d.rounded_rectangle((int(w * 0.16), 0, int(w * 0.84), tapa_h), radius=int(w * 0.08), fill=DORADO)
    d.rectangle((int(w * 0.24), int(tapa_h * 0.08), int(w * 0.32), int(tapa_h * 0.92)), fill=(232, 210, 178))
    # cuello
    d.rectangle((int(w * 0.3), tapa_h, int(w * 0.7), cuerpo_y + r), fill=(235, 220, 205))
    # cuerpo de vidrio
    d.rounded_rectangle((0, cuerpo_y, w, h), radius=r, fill=VIDRIO + (90,), outline=VIDRIO + (255,), width=3 * K)
    # perfume
    nivel = cuerpo_y + int((h - cuerpo_y) * 0.18)
    d.rounded_rectangle((int(5 * K), nivel, w - int(5 * K), h - int(5 * K)), radius=r - 5 * K, fill=liquido + (235,))
    # reflejo
    d.rounded_rectangle((int(w * 0.12), cuerpo_y + int(r * 0.6), int(w * 0.22), h - r), radius=int(w * 0.05),
                        fill=(255, 255, 255, 110))
    # etiqueta "5 ml"
    ey = cuerpo_y + int((h - cuerpo_y) * 0.42)
    d.rounded_rectangle((int(w * 0.14), ey, int(w * 0.86), ey + int(h * 0.12)), radius=int(w * 0.04),
                        fill=(255, 255, 255, 235))
    d.line((int(w * 0.26), ey + int(h * 0.06), int(w * 0.74), ey + int(h * 0.06)), fill=DORADO, width=2 * K)
    return im.resize((VW, VH), Image.LANCZOS)


def main():
    n = len(LIQUIDOS)
    W = n * VW + (n - 1) * GAP
    out = Image.new("RGBA", (W, VH + 40), (0, 0, 0, 0))
    for i, liq in enumerate(LIQUIDOS):
        f = frasco(liq)
        # alternar alturas apenas, para que no se vea rígido
        dy = 0 if i % 2 == 0 else 40
        out.alpha_composite(f, (i * (VW + GAP), dy))
    out.save(os.path.join(AQUI, "decants-sin-marca.png"))
    print(os.path.join(AQUI, "decants-sin-marca.png"))


if __name__ == "__main__":
    main()
