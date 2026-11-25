#!/usr/bin/env python3
"""
Pieza "lanzamiento con foto de campaña" para LARESE STORE, con fondo blanco.

Logo de la marca arriba, nombre del perfume, la foto de campaña enmarcada,
un recuadro chico con el frasco y la caja, el tamaño en vertical al costado,
el sello LANZAMIENTO con el isotipo "la", y "Disponible en" + logo larese STORE.

Uso:
    python3 crear_lanzamiento_foto.py spec.json historia salida.png
    python3 crear_lanzamiento_foto.py spec.json post salida.png
    python3 crear_lanzamiento_foto.py spec.json historia-completa salida.png   # foto en toda la pieza
    python3 crear_lanzamiento_foto.py spec.json meta-historia salida.png       # anuncio Meta 9:16
    python3 crear_lanzamiento_foto.py spec.json meta-post salida.png           # anuncio Meta 4:5

Spec (JSON):
{
  "marca_logo": "logo-marca-mascara.png",  # máscara en gris (blanco = tinta)
  "titulo": "Your Devotion EDP Intense",
  "foto": "campana.jpg",
  "foto_recorte": [0, 290, 1320, 1520],     # opcional: (x0, y0, x1, y1) de la foto
  "recuadro": "frasco-caja.png",            # opcional: frasco + caja sobre blanco
  "detalle": "Eau de Parfum Intense · 100 ml",  # sin recuadro: línea abajo de la foto
  "medida": "100 ml.",
  "sello": "LANZAMIENTO",
  "tienda_extra": "Mayorista",              # opcional: logo larese | MAYORISTA en vez de "Disponible en"
  "pie": "WhatsApp 0972 736 002  ·  Envíos a todo Paraguay"
}
"""
import json
import os
import sys

import numpy as np

from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from crear_lanzamiento import PIE, sello  # noqa: E402
from crear_pieza import (  # noqa: E402
    FONDO, GRIS, TEXTO, alto_linea, ancho_txt, capa_color, fuente, logo_mascara, txt,
)

MEDIDAS = {
    "historia": dict(size=(1080, 1920), marca_y=200, marca_w=640, marca_alto=82, titulo_y=300, titulo_t=50,
                     foto=(0, 392, 1080), alto_max=1030, recuadro=310, sello=(960, 500, 100),
                     medida_t=46, pie_y=1700),
    "post": dict(size=(1080, 1350), marca_y=34, marca_w=430, titulo_y=96, titulo_t=34,
                 foto=(0, 148, 1080), alto_max=945, recuadro=265, sello=(985, 238, 78),
                 logo_w=215,
                 medida_t=38, pie_y=1300),
}


def sombra(img, caja, radio=18, opacidad=0.18):
    m = Image.new("L", img.size, 0)
    x0, y0, x1, y1 = caja
    ImageDraw.Draw(m).rectangle((x0 + 4, y0 + 10, x1 + 4, y1 + 10), fill=255)
    img.alpha_composite(capa_color(m.filter(ImageFilter.GaussianBlur(radio)), (0, 0, 0), opacidad))


def armar(SPEC, formato):
    M = MEDIDAS[formato]
    w, h = M["size"]
    img = Image.new("RGBA", (w, h), FONDO + (255,))
    d = ImageDraw.Draw(img)
    cx = w / 2

    # logo de la marca del perfume
    ml = Image.open(SPEC["marca_logo"]).convert("L")
    mw = M["marca_w"]
    ml = ml.resize((mw, int(ml.height * mw / ml.width)), Image.LANCZOS)
    img.alpha_composite(capa_color(ml, TEXTO), (int(cx - mw / 2), M["marca_y"]))

    # nombre del perfume
    ft = fuente(M["titulo_t"], "Bold")
    txt(d, cx, M["titulo_y"], SPEC["titulo"].upper(), ft, TEXTO, esp=M["titulo_t"] * 0.06)

    # foto de campaña enmarcada
    fx0, fy0, fx1 = M["foto"]
    foto = Image.open(SPEC["foto"]).convert("RGB")
    if SPEC.get("foto_recorte"):
        foto = foto.crop(tuple(SPEC["foto_recorte"]))
    fw = fx1 - fx0
    foto = foto.resize((fw, int(foto.height * fw / foto.width)), Image.LANCZOS)
    sobra = foto.height - M.get("alto_max", foto.height)
    if sobra > 0:  # recorta lo que no entra: un poco arriba y más abajo
        arriba = int(sobra * 0.35)
        foto = foto.crop((0, arriba, fw, arriba + M["alto_max"]))
    fy1 = fy0 + foto.height
    a_lo_ancho = fx0 == 0 and fx1 == w  # foto de borde a borde: sin marco ni sombra
    if not a_lo_ancho:
        sombra(img, (fx0, fy0, fx1, fy1), 22, 0.14)
    img.alpha_composite(foto.convert("RGBA"), (fx0, fy0))
    d = ImageDraw.Draw(img)
    if not a_lo_ancho:
        d.rectangle((fx0, fy0, fx1 - 1, fy1 - 1), outline=(215, 215, 215), width=2)

    # recuadro con frasco y caja, montado sobre la esquina de abajo a la derecha
    R = M["recuadro"]
    rx1 = fx1 - 22
    rx0 = rx1 - R
    ry0 = fy1 - int(R * 0.40)
    ry1 = ry0 + R
    if SPEC.get("recuadro"):
        sombra(img, (rx0, ry0, rx1, ry1), 16, 0.22)
        d = ImageDraw.Draw(img)
        d.rectangle((rx0, ry0, rx1, ry1), fill=FONDO, outline=(200, 200, 200), width=3)
        rec = Image.open(SPEC["recuadro"]).convert("RGB")
        borde = 10
        rec = rec.resize((R - 2 * borde, R - 2 * borde), Image.LANCZOS)
        img.paste(rec, (rx0 + borde, ry0 + borde))

    # sello LANZAMIENTO sobre la esquina de arriba a la derecha de la foto
    if SPEC.get("sello"):
        sx, sy, sr = M["sello"]
        sello(img, sx, sy, sr, SPEC["sello"])

    if not SPEC.get("recuadro"):
        # sin recuadro: detalle + tamaño centrado, y "Disponible en" + logo en una fila
        d = ImageDraw.Draw(img)
        y = fy1 + M["titulo_t"] * 0.8
        detalle = SPEC.get("detalle") or SPEC.get("medida", "")
        if detalle:
            fdet = fuente(M["titulo_t"] * 0.58, "Medium")
            txt(d, cx, y, detalle.upper(), fdet, GRIS, esp=M["titulo_t"] * 0.07)
            y += alto_linea(fdet) + M["titulo_t"] * 0.9
        fdisp = fuente(M["titulo_t"] * 0.8, "Medium")
        logo = logo_mascara("texto", M.get("logo_w", 300))
        gap = 24
        wt = ancho_txt(d, "Disponible en", fdisp)
        xi = cx - (wt + gap + logo.width) / 2
        a, _ = fdisp.getmetrics()
        d.text((xi, y + logo.height * 0.80 - a), "Disponible en", font=fdisp, fill=TEXTO)
        img.alpha_composite(capa_color(logo, TEXTO), (int(xi + wt + gap), int(y)))
    else:
        # tamaño en vertical, pegado al recuadro
        if SPEC.get("medida"):
            fm = fuente(M["medida_t"], "Medium")
            tw = int(ancho_txt(d, SPEC["medida"], fm)) + 10
            th = int(alto_linea(fm, 1.25))
            capa = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
            ImageDraw.Draw(capa).text((4, 0), SPEC["medida"], font=fm, fill=TEXTO)
            capa = capa.rotate(90, expand=True, resample=Image.BICUBIC)
            my = int((fy1 + ry1) / 2 - capa.height / 2)
            img.alpha_composite(capa, (rx0 - capa.width - 6, max(fy1 + 8, my)))

        # "Disponible en" + logo larese STORE, a la izquierda del recuadro
        d = ImageDraw.Draw(img)
        zona_x0, zona_x1 = fx0, rx0 - (M["medida_t"] * 1.4)
        zcx = (zona_x0 + zona_x1) / 2
        fdisp = fuente(M["titulo_t"] * 0.72, "Medium")
        logo = logo_mascara("texto", min(330, (zona_x1 - zona_x0) * 0.82))
        alto_bloque = alto_linea(fdisp, 1.2) + logo.height
        y = (fy1 + ry1) / 2 - alto_bloque / 2 + 6
        txt(d, zcx, y, "Disponible en", fdisp, GRIS)
        y += alto_linea(fdisp, 1.2)
        img.alpha_composite(capa_color(logo, TEXTO), (int(zcx - logo.width / 2), int(y)))

    # pie
    d = ImageDraw.Draw(img)
    fp = fuente(24 if formato == "historia" else 22, "Medium")
    py = M["pie_y"]
    d.line((cx - 260, py - 26, cx + 260, py - 26), fill=(225, 225, 225), width=2)
    txt(d, cx, py, SPEC.get("pie", PIE), fp, GRIS)
    return img.convert("RGB")


def velo(img, y0, y1, a0, a1):
    """Velo blanco que va de opacidad a0 (en y0) a a1 (en y1); fuera del tramo sigue el borde."""
    w, h = img.size
    col = []
    for y in range(h):
        t = min(1, max(0, (y - y0) / (y1 - y0)))
        t = t * t * (3 - 2 * t)
        col.append(int(255 * (a0 + (a1 - a0) * t)))
    m = Image.new("L", (1, h))
    m.putdata(col)
    img.alpha_composite(capa_color(m.resize((w, h)), FONDO))


# Piezas con la foto en toda la pieza. Las "meta-*" dejan libres las zonas que tapa
# Meta en los anuncios (historia: 14 % arriba y 20 % abajo).
COMPLETA = {
    "historia-completa": dict(size=(1080, 1920), escena_alto=None, escena_y=None,
                              velo_arriba=(300, 470), velo_abajo=(1400, 1580),
                              marca_y=200, marca_w=640, marca_alto=82, titulo_y=300, titulo_t=50, sello=(915, 545, 104),
                              detalle_y=1520, logo_w=300, pie_y=1730),
    "meta-historia": dict(size=(1080, 1920), escena_alto=860, escena_y=440,
                          velo_arriba=(420, 560), velo_abajo=(1200, 1310),
                          marca_y=285, marca_w=560, marca_alto=72, titulo_y=372, titulo_t=44, sello=(880, 560, 92),
                          detalle_y=1300, logo_w=270, pie_y=1490),
    "meta-post": dict(size=(1080, 1350), escena_alto=900, escena_y=160,
                      velo_arriba=(110, 230), velo_abajo=(980, 1085),
                      marca_y=36, marca_w=430, marca_alto=50, titulo_y=100, titulo_t=34, sello=(900, 270, 84),
                      detalle_y=1100, logo_w=240, pie_y=1262),
}


def armar_completa(SPEC, formato="historia-completa"):
    """Foto ocupando toda la pieza y los textos sobre velos blancos."""
    L = COMPLETA[formato]
    w, h = L["size"]
    cx = w / 2
    foto = Image.open(SPEC["foto"]).convert("RGB")
    if SPEC.get("foto_recorte"):  # escena limpia, sin los textos de la campaña
        foto = foto.crop(tuple(SPEC["foto_recorte"]))

    # fondo: la misma escena agrandada y desenfocada, para cubrir toda la pieza
    esc = max(w / foto.width, h / foto.height)
    fondo_img = foto.resize((int(foto.width * esc) + 1, int(foto.height * esc) + 1), Image.LANCZOS)
    fx = (fondo_img.width - w) // 2
    fy = (fondo_img.height - h) // 2
    fondo_img = fondo_img.crop((fx, fy, fx + w, fy + h)).filter(ImageFilter.GaussianBlur(38))
    img = fondo_img.convert("RGBA")

    # escena nítida, con los bordes fundidos en el fondo desenfocado
    if L["escena_alto"]:
        ph = L["escena_alto"]
        pw = min(w, int(foto.width * ph / foto.height))
    else:
        pw = w
        ph = int(foto.height * w / foto.width)
    nitida = foto.resize((pw, ph), Image.LANCZOS).convert("RGBA")
    fundido = 150
    fundido_x = 90 if pw < w else 0
    ys = np.arange(ph)
    ty = np.clip(np.minimum(ys, ph - 1 - ys) / fundido, 0, 1)
    if fundido_x:
        xs = np.arange(pw)
        tx = np.clip(np.minimum(xs, pw - 1 - xs) / fundido_x, 0, 1)
    else:
        tx = np.ones(pw)
    t = np.minimum(ty[:, None], tx[None, :])
    t = t * t * (3 - 2 * t)
    nitida.putalpha(Image.fromarray((t * 255).astype("uint8")))
    py0 = L["escena_y"] if L["escena_y"] is not None else SPEC.get("foto_completa_y", 400)
    img.alpha_composite(nitida, (int((w - pw) / 2), py0))

    va, vb = L["velo_arriba"], L["velo_abajo"]
    velo(img, va[0], va[1], 0.80, 0.0)   # arriba: logo y título
    velo(img, vb[0], vb[1], 0.0, 0.82)   # abajo: detalle, tienda y pie

    d = ImageDraw.Draw(img)
    ml = Image.open(SPEC["marca_logo"]).convert("L")
    # ancho fijo, pero sin pasar un alto máximo (logos cortos como DIOR no salen gigantes)
    mw = min(L["marca_w"], int(L.get("marca_alto", 999) * ml.width / ml.height))
    mh = int(ml.height * mw / ml.width)
    ml = ml.resize((mw, mh), Image.LANCZOS)
    ajuste = (int(L["marca_w"] * 0.099) - mh) // 2 if mh < L["marca_w"] * 0.099 else 0
    img.alpha_composite(capa_color(ml, TEXTO), (int(cx - mw / 2), L["marca_y"] + max(0, ajuste)))
    tt = L["titulo_t"]
    txt(d, cx, L["titulo_y"], SPEC["titulo"].upper(), fuente(tt, "Bold"), TEXTO, esp=tt * 0.06)

    if SPEC.get("sello"):
        sx, sy, sr = L["sello"]
        sello(img, sx, sy, sr, SPEC["sello"])

    d = ImageDraw.Draw(img)
    k = tt / 50  # escala de los textos de abajo
    y = L["detalle_y"]
    if SPEC.get("detalle"):
        fdet = fuente(29 * k, "Medium")
        txt(d, cx, y, SPEC["detalle"].upper(), fdet, GRIS, esp=3.5 * k)
        y += alto_linea(fdet) + 42 * k
    logo = logo_mascara("texto", L["logo_w"])
    if SPEC.get("tienda_extra"):
        # logo larese STORE | MAYORISTA (o el texto que se pida)
        fx = fuente(44 * k * (L["logo_w"] / 300) / k, "Bold")
        extra = SPEC["tienda_extra"].upper()
        esp = fx.size * 0.14
        we = ancho_txt(d, extra, fx, esp)
        gap = 34 * L["logo_w"] / 300
        xi = cx - (logo.width + 2 * gap + we) / 2
        img.alpha_composite(capa_color(logo, TEXTO), (int(xi), int(y)))
        d = ImageDraw.Draw(img)
        xl = xi + logo.width + gap
        d.line((xl, y + 4, xl, y + logo.height - 2), fill=TEXTO, width=3)
        a, _ = fx.getmetrics()
        txt(d, xl + gap + we / 2, y + logo.height * 0.80 - a, extra, fx, TEXTO, esp=esp)
    else:
        fdisp = fuente(40 * L["logo_w"] / 300, "Medium")
        gap = 24
        wt = ancho_txt(d, "Disponible en", fdisp)
        xi = cx - (wt + gap + logo.width) / 2
        a, _ = fdisp.getmetrics()
        d.text((xi, y + logo.height * 0.80 - a), "Disponible en", font=fdisp, fill=TEXTO)
        img.alpha_composite(capa_color(logo, TEXTO), (int(xi + wt + gap), int(y)))

    d = ImageDraw.Draw(img)
    py = L["pie_y"]
    d.line((cx - 260, py - 26, cx + 260, py - 26), fill=(200, 200, 200), width=2)
    txt(d, cx, py, SPEC.get("pie", PIE), fuente(24 if h > 1500 else 22, "Medium"), GRIS)
    return img.convert("RGB")


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[2] not in list(MEDIDAS) + list(COMPLETA):
        print(__doc__)
        sys.exit(1)
    ruta_spec = os.path.abspath(sys.argv[1])
    with open(ruta_spec, encoding="utf-8") as fh:
        spec = json.load(fh)
    for k in ("foto", "recuadro", "marca_logo"):
        if spec.get(k) and not os.path.isabs(spec[k]):
            spec[k] = os.path.join(os.path.dirname(ruta_spec), spec[k])
    pieza = armar_completa(spec, sys.argv[2]) if sys.argv[2] in COMPLETA else armar(spec, sys.argv[2])
    pieza.save(sys.argv[3], "PNG")
    print(sys.argv[3])
