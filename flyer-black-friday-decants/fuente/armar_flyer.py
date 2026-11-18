#!/usr/bin/env python3
"""Flyer Black Friday de decants: 6 frascos con el nombre de cada perfume al lado.

Usa el mismo estilo (fondo blanco, Poppins, logo, botón y pie) que
herramientas/pieza-fondo-blanco/scripts/crear_pieza.py.

Uso: python3 fuente/armar_flyer.py   (desde flyer-black-friday-decants/)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(CARPETA, "..", "herramientas", "pieza-fondo-blanco", "scripts"))
import crear_pieza as cp  # noqa: E402

# Cada frasco de la foto (de izquierda a derecha) con un perfume de color parecido
PERFUMES = [
    ("Libre", "Yves Saint Laurent"),
    ("Scandal\nLe Parfum", "Jean Paul Gaultier"),
    ("Good Girl\nBlush", "Carolina Herrera"),
    ("La Vie\nEst Belle", "Lancôme"),
    ("J'adore", "Dior"),
    ("La Bomba", "Carolina Herrera"),
]

ETIQUETA = "Decants · 3, 5 y 10 ml"
TITULO = "Black Friday"
SUBTITULO = "Precios especiales en decants"
CTA = "¡Pedí los tuyos!"


def frascos():
    foto = Image.open(os.path.join(CARPETA, "decants.png")).convert("RGBA")
    alfa = foto.getchannel("A").point(lambda v: 255 if v > 20 else 0)
    cols, dentro = [], False
    for x in range(foto.width):
        hay = alfa.crop((x, 0, x + 1, foto.height)).getbbox() is not None
        if hay and not dentro:
            ini, dentro = x, True
        elif not hay and dentro:
            cols.append((ini, x)); dentro = False
    if dentro:
        cols.append((ini, foto.width))
    out = []
    for x0, x1 in cols:
        p = foto.crop((x0, 0, x1, foto.height))
        out.append(p.crop(p.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox()))
    assert len(out) == 6, len(out)
    return out


def celda(img, frasco, nombre, marca, caja, M):
    x0, y0, x1, y1 = caja
    alto = (y1 - y0) * M.get("alto_frasco", 0.94)
    esc = alto / frasco.height
    f = frasco.resize((int(frasco.width * esc), int(alto)), Image.LANCZOS)
    fx = int(x0)
    fy = int(y0 + (y1 - y0 - f.height) / 2)
    # sombra suave bajo el frasco
    sombra = Image.new("L", img.size, 0)
    sw = f.width * 0.9
    ImageDraw.Draw(sombra).ellipse((fx + (f.width - sw) / 2, fy + f.height - 10,
                                    fx + (f.width + sw) / 2, fy + f.height + 14), fill=150)
    img.alpha_composite(cp.capa_color(sombra.filter(ImageFilter.GaussianBlur(12)), (0, 0, 0), 0.5))
    img.alpha_composite(f, (fx, fy))

    # texto al lado del frasco
    d = ImageDraw.Draw(img)
    tx = fx + f.width + M["sep"]
    maxw = x1 - tx
    # el nombre corta donde dice "\n"; la letra se achica hasta que cada renglón entre
    ln = nombre.upper().split("\n")
    tam = M["nom"]
    while tam > M["nom"] * 0.6 and max(d.textlength(l, font=cp.fuente(tam, b"Bold")) for l in ln) > maxw:
        tam -= 1
    fn = cp.fuente(tam, b"Bold")
    fm, lm, _ = cp.ajustar(d, marca, M["mar"], M["mar"] * 0.6, maxw, 1, b"Medium")
    raya = M["nom"] * 0.9
    total = cp.alto_linea(fn, 0.95) * len(ln) + raya + cp.alto_linea(fm, 1.05) * len(lm)
    y = fy + f.height * 0.56 - total / 2
    for l in ln:
        d.text((tx, y), l, font=fn, fill=cp.TEXTO)
        y += cp.alto_linea(fn, 0.95)
    ry = y + raya * 0.42
    d.line((tx + 2, ry, tx + M["nom"] * 1.4, ry), fill=cp.TEXTO, width=3)
    y += raya
    for l in lm:
        d.text((tx, y), l, font=fm, fill=cp.GRIS)
        y += cp.alto_linea(fm, 1.05)


MEDIDAS = {
    "post": dict(tam=(1080, 1350), logo_w=210, logo_y=56, eti=30, tit=104, sub=28, cta=32, pie=24, pie_y=60,
                 margen=56, nom=28, mar=21, sep=16, gap_y=40),
    "historia": dict(tam=(1080, 1920), logo_w=250, logo_y=170, eti=34, tit=116, sub=32, cta=40, pie=30, pie_y=190,
                     margen=44, nom=30, mar=21, sep=14, gap_y=80, alto_frasco=0.86),
}


def armar(formato):
    M = MEDIDAS[formato]
    w, h = M["tam"]
    img = cp.fondo(w, h, cp.FONDO)
    d = ImageDraw.Draw(img)
    cx = w / 2

    # arriba: logo, etiqueta, título y subtítulo
    logo = cp.logo_mascara("texto", M["logo_w"])
    img.alpha_composite(cp.capa_color(logo, cp.TEXTO), (int(cx - logo.width / 2), M["logo_y"]))
    y = M["logo_y"] + logo.height + M["eti"] * 1.3
    fe = cp.fuente(M["eti"], b"SemiBold")
    cp.txt(d, cx, y, ETIQUETA.upper(), fe, cp.GRIS, esp=M["eti"] * 0.06)
    y += cp.alto_linea(fe, 1.05)
    ft, lt, _ = cp.ajustar(d, TITULO.upper(), M["tit"], 60, w - 130, 1, b"Bold")
    for l in lt:
        cp.txt(d, cx, y, l, ft, cp.TEXTO)
        y += cp.alto_linea(ft, 0.86)
    fs = cp.fuente(M["sub"], b"Medium")
    y += 6
    cp.txt(d, cx, y, SUBTITULO.upper(), fs, cp.GRIS, esp=M["sub"] * 0.04)
    arriba = y + cp.alto_linea(fs, 1.15) + h * 0.03

    # abajo: botón y pie
    pie_y = h - M["pie_y"] - M["pie"] * 2.1
    alto_cta = cp.alto_linea(cp.fuente(M["cta"], b"SemiBold")) + M["cta"] * 0.9
    y_cta = pie_y - M["pie"] * 1.6 - alto_cta
    abajo = y_cta - h * 0.035

    # medio: grilla de 3 columnas x 2 filas
    cp.marca_de_agua(img, (arriba + abajo) / 2)
    ancho_col = (w - 2 * M["margen"]) / 3
    alto_fila = (abajo - arriba - M["gap_y"]) / 2
    for i, (frasco, (nombre, marca)) in enumerate(zip(frascos(), PERFUMES)):
        c, r = i % 3, i // 3
        x0 = M["margen"] + c * ancho_col
        y0 = arriba + r * (alto_fila + M["gap_y"])
        celda(img, frasco, nombre, marca, (x0 + 6, y0, x0 + ancho_col - 10, y0 + alto_fila), M)

    cp.boton(img, cx, y_cta, CTA, M["cta"], cp.ACENTO)
    cp.pie(img, pie_y, M["pie"], cp.ACENTO)
    return img.convert("RGB")


if __name__ == "__main__":
    for formato, nombre in (("post", "flyer-post.png"), ("historia", "flyer-historia.png")):
        ruta = os.path.join(CARPETA, nombre)
        armar(formato).save(ruta, "PNG")
        print(ruta)
