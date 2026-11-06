#!/usr/bin/env python3
"""
Pieza estilo "lanzamiento" para LARESE STORE, con fondo blanco.

Marca del perfume arriba, frasco grande al centro con reflejo, sello circular
con texto alrededor del isotipo "la", y abajo "Disponible en" + logo larese STORE.

Uso:
    python3 crear_lanzamiento.py spec.json post salida.png
    python3 crear_lanzamiento.py spec.json historia salida.png

Spec (JSON):
{
  "marca": "YVES SAINT LAURENT",          # arriba, en texto (nunca el logo oficial)
  "nombre": "Y Iced Cologne",             # grande, abajo del frasco
  "detalle": "Eau de Toilette Intense · 60 ml",
  "imagen": "foto.jpg",                    # ideal: fondo blanco liso
  "sello": "LANZAMIENTO",                  # texto alrededor del isotipo
  "sello_rel": [0.98, 0.42],               # opcional: centro del sello relativo al producto (x, y)
  "pie": "WhatsApp 0972 736 002  ·  Envíos a todo Paraguay"
}
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "herramientas", "pieza-fondo-blanco", "scripts"))
from crear_pieza import (  # noqa: E402
    ASSETS, FONDO, GRIS, TEXTO, alto_linea, ancho_txt, capa_color, cargar_producto,
    fuente, logo_mascara, txt,
)

ISOTIPO = os.path.join(AQUI, "..", "comercial-fragancias", "public", "marca", "isotipo-negro.png")

PIE = "WhatsApp 0972 736 002  ·  Envíos a todo Paraguay"

MEDIDAS = {
    "post": dict(size=(1080, 1350), marca_y=70, marca_t=46, prod=(185, 925), sello=(835, 440, 118),
                 nombre_y=965, disp_y=1110, pie_y=1268),
    "historia": dict(size=(1080, 1920), marca_y=230, marca_t=50, prod=(420, 1260), sello=(830, 690, 128),
                     nombre_y=1330, disp_y=1480, pie_y=1660),
}


def texto_circular(img, cx, cy, r, texto, f, color):
    """Escribe el texto alrededor de un círculo, letra por letra, empezando arriba."""
    d = ImageDraw.Draw(img)
    anchos = [d.textlength(ch, font=f) for ch in texto]
    total = sum(anchos)
    escala = (2 * math.pi * r) / total  # reparte el texto en toda la vuelta
    ang = -math.pi / 2
    alto = alto_linea(f)
    for ch, a in zip(texto, anchos):
        paso = a * escala / r
        medio = ang + paso / 2
        lado = int(max(a, alto) * 2.2)
        letra = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
        ImageDraw.Draw(letra).text(((lado - a) / 2, (lado - alto) / 2), ch, font=f, fill=color)
        letra = letra.rotate(-math.degrees(medio) - 90, resample=Image.BICUBIC)
        x = cx + r * math.cos(medio) - lado / 2
        y = cy + r * math.sin(medio) - lado / 2
        img.alpha_composite(letra, (int(x), int(y)))
        ang += paso


def sello(img, cx, cy, R, texto):
    d = ImageDraw.Draw(img)
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=FONDO + (255,), outline=TEXTO, width=4)
    f = fuente(R * 0.17, "SemiBold")
    vuelta = f"{texto}  •  {texto}  •  "
    texto_circular(img, cx, cy, R * 0.74, vuelta, f, TEXTO)
    iso = Image.open(ISOTIPO).convert("RGBA")
    iso = iso.crop(iso.getbbox())
    lado = int(R * 0.72)
    iso.thumbnail((lado, lado), Image.LANCZOS)
    img.alpha_composite(iso, (int(cx - iso.width / 2), int(cy - iso.height / 2)))


def producto_con_reflejo(img, prod, x0, y0, y1, ancho_max):
    """Frasco escalado al alto disponible, centrado en x, con reflejo suave abajo."""
    esc = min((y1 - y0) * 0.78 / prod.height, ancho_max / prod.width)
    alto = int(prod.height * esc)
    p = prod.resize((int(prod.width * esc), alto), Image.LANCZOS)
    p = p.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    px = int(x0 - p.width / 2)
    base = y0 + alto

    # reflejo: frasco invertido, desvanecido hacia abajo
    ref = p.transpose(Image.FLIP_TOP_BOTTOM)
    hr = int((y1 - base) * 0.95)
    ref = ref.crop((0, 0, ref.width, min(hr, ref.height)))
    grad = Image.linear_gradient("L").resize(ref.size).point(lambda v: int((255 - v) * 0.22))
    a = ref.getchannel("A")
    ref.putalpha(Image.composite(grad, Image.new("L", ref.size, 0), a))
    ref = ref.filter(ImageFilter.GaussianBlur(1.5))
    img.alpha_composite(ref, (px, base + 4))

    # sombra de contacto
    sombra = Image.new("L", img.size, 0)
    sw = p.width * 0.9
    ImageDraw.Draw(sombra).ellipse((x0 - sw / 2, base - 10, x0 + sw / 2, base + 14), fill=140)
    img.alpha_composite(capa_color(sombra.filter(ImageFilter.GaussianBlur(12)), (0, 0, 0), 0.45))

    img.alpha_composite(p, (px, y0))
    return px, y0, px + p.width, base


def armar(SPEC, formato):
    M = MEDIDAS[formato]
    w, h = M["size"]
    img = Image.new("RGBA", (w, h), FONDO + (255,))
    d = ImageDraw.Draw(img)
    cx = w / 2

    # línea de horizonte muy suave (como el agua del ejemplo, pero en gris claro)
    y0, y1 = M["prod"]
    horizonte = y0 + int((y1 - y0) * 0.78)
    banda = Image.new("L", img.size, 0)
    ImageDraw.Draw(banda).rectangle((0, horizonte - 1, w, horizonte + 1), fill=255)
    img.alpha_composite(capa_color(banda.filter(ImageFilter.GaussianBlur(3)), (0, 0, 0), 0.10))

    # marca del perfume arriba (en texto, sin logo oficial)
    fm = fuente(M["marca_t"], "Medium")
    esp = M["marca_t"] * 0.32
    txt(d, cx, M["marca_y"], SPEC["marca"], fm, TEXTO, esp=esp)
    yl = M["marca_y"] + alto_linea(fm) + 22
    lw = 60
    d.line((cx - lw / 2, yl, cx + lw / 2, yl), fill=TEXTO, width=2)

    # marca de agua "la" gigante detrás del frasco
    m = logo_mascara("monograma", w * 0.95)
    img.alpha_composite(capa_color(m, TEXTO, 0.035),
                        (int(cx - m.width / 2), int((y0 + horizonte) / 2 - m.height / 2)))

    prod, ok = cargar_producto(SPEC["imagen"])
    if not ok:
        raise SystemExit("No se pudo recortar la foto del producto")
    bx0, by0, bx1, by1 = producto_con_reflejo(img, prod, cx, y0, y1, w * 0.80)

    sx, sy, sr = M["sello"]
    if SPEC.get("sello_rel"):
        rx, ry = SPEC["sello_rel"]
        sx, sy = bx0 + (bx1 - bx0) * rx, by0 + (by1 - by0) * ry
        sx = min(sx, w - sr - 30)
    sello(img, sx, sy, sr, SPEC["sello"])

    # nombre del perfume
    d = ImageDraw.Draw(img)
    y = M["nombre_y"]
    fn = fuente(64, "Bold")
    while ancho_txt(d, SPEC["nombre"].upper(), fn, 6) > w - 140:
        fn = fuente(fn.size - 4, "Bold")
    txt(d, cx, y, SPEC["nombre"].upper(), fn, TEXTO, esp=6)
    y += alto_linea(fn, 0.95)
    fd = fuente(28, "Medium")
    txt(d, cx, y, SPEC["detalle"].upper(), fd, GRIS, esp=28 * 0.12)

    # "Disponible en" + logo larese STORE en una fila
    y = M["disp_y"]
    fdisp = fuente(40, "Medium")
    logo = logo_mascara("texto", 300)
    gap = 26
    wt = ancho_txt(d, "Disponible en", fdisp)
    total = wt + gap + logo.width
    xi = cx - total / 2
    a, b = fdisp.getmetrics()
    ly = int(y)
    ty = ly + logo.height * 0.80 - a  # alinea la base del texto con la base del logo
    d.text((xi, ty), "Disponible en", font=fdisp, fill=TEXTO)
    img.alpha_composite(capa_color(logo, TEXTO), (int(xi + wt + gap), ly))

    # pie
    fp = fuente(24, "Medium")
    d = ImageDraw.Draw(img)
    d.line((cx - 260, M["pie_y"] - 26, cx + 260, M["pie_y"] - 26), fill=(225, 225, 225), width=2)
    txt(d, cx, M["pie_y"], SPEC.get("pie", PIE), fp, GRIS)
    return img.convert("RGB")


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[2] not in MEDIDAS:
        print(__doc__)
        sys.exit(1)
    ruta_spec = os.path.abspath(sys.argv[1])
    with open(ruta_spec, encoding="utf-8") as fh:
        spec = json.load(fh)
    if not os.path.isabs(spec["imagen"]):
        spec["imagen"] = os.path.join(os.path.dirname(ruta_spec), spec["imagen"])
    armar(spec, sys.argv[2]).save(sys.argv[3], "PNG")
    print(sys.argv[3])
