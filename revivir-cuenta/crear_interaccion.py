#!/usr/bin/env python3
"""
Historias de interacción de LARESE STORE con la paleta y tipografía de marca, y con espacio
libre para el sticker de Instagram: encuesta, quiz, slider o caja de preguntas.

Usa las fuentes, el logo, los colores y el armado de producto de herramientas/pieza-marca.

Uso:
    python3 crear_interaccion.py historias.json carpeta_salida/

historias.json es una lista de specs:
{
  "archivo": "01-dulce-o-fresco.png",
  "fondo": "crema" | "bordo",                # opcional, crema por defecto
  "etiqueta": "Encuesta",                    # Poppins chica en dorado
  "titulo": "¿Dulce o fresco?",              # Playfair grande
  "subtitulo": "Votá y te recomiendo uno",   # opcional, Playfair italic
  "productos": [                              # 0 a 3 productos
     {"imagen": "fuente/scandal.png", "nombre": "Dulce"},
     {"imagen": "fuente/lightblue.jpg", "nombre": "Fresco"}
  ],
  "sticker": "Votá acá abajo",               # texto chico sobre el espacio del sticker
  "alto_sticker": 300,                       # alto del espacio libre
  "cta": "..."                               # sin sticker: botón y pie
}
"""
import json
import os
import sys

from PIL import ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "herramientas", "pieza-marca", "scripts"))
import crear_pieza as pm  # noqa: E402

W, H = 1080, 1920
CX = W / 2


def armar(spec, base):
    tema = spec.get("fondo", "crema")
    T = pm.TEMAS[tema]
    img = pm.lienzo(W, H, tema)
    d = ImageDraw.Draw(img)

    # --- logo y textos de arriba ---
    logo = pm.logo_mascara("texto", 230)
    y = 170
    img.alpha_composite(pm.capa_color(logo, T["titulo"]), (int(CX - logo.width / 2), y))
    y += logo.height + 44
    if spec.get("etiqueta"):
        fe = pm.poppins(30, "Medium")
        pm.txt(d, CX, y, spec["etiqueta"].upper(), fe, T["acento"], esp=30 * 0.22)
        y += pm.alto_linea(fe, 1.3)
    ft, lt, _ = pm.ajustar(d, spec["titulo"], 116, 66, W - 140, 3, lambda t: pm.playfair(t, 500))
    for l in lt:
        pm.txt(d, CX, y, l, ft, T["titulo"])
        y += pm.alto_linea(ft, 1.0)
    if spec.get("subtitulo"):
        y += 6
        fs, ls, _ = pm.ajustar(d, spec["subtitulo"], 44, 32, W - 200, 2, lambda t: pm.playfair(t, 400, True))
        for l in ls:
            pm.txt(d, CX, y, l, fs, T["sec"])
            y += pm.alto_linea(fs, 1.15)

    # --- zona de abajo: sticker, o botón + pie ---
    con_sticker = bool(spec.get("sticker"))
    if con_sticker:
        y_sticker = H - 220 - spec.get("alto_sticker", 300)   # espacio libre para el sticker
        limite = y_sticker - 70
    else:
        limite = H - 520

    # --- productos ---
    prods = spec.get("productos") or []
    caja_y0 = y + 60
    hay_nombres = any(p.get("nombre") for p in prods)
    n = max(1, len(prods))
    margen = 90 if n > 1 else 150
    hueco = 50 if n > 1 else 0
    ancho = (W - 2 * margen - hueco * (n - 1)) / n
    tam = 44  # el mismo tamaño para todos los nombres, el que entre en la columna
    while tam > 26 and any(d.textlength(p.get("nombre", ""), font=pm.playfair(tam, 500)) > ancho + hueco * 0.6 for p in prods):
        tam -= 2
    fn = pm.playfair(tam, 500)
    caja_y1 = limite - (pm.alto_linea(fn, 1.3) if hay_nombres else 0)
    if prods:
        for i, p in enumerate(prods):
            ruta = p["imagen"] if os.path.isabs(p["imagen"]) else os.path.join(base, p["imagen"])
            im, recortado = pm.cargar_producto(ruta)
            x0 = margen + i * (ancho + hueco)
            ac = pm.poner_producto(img, (x0, caja_y0, x0 + ancho, caja_y1), im, recortado, tema)
            if p.get("nombre"):
                pm.txt(ImageDraw.Draw(img), (ac[0] + ac[2]) / 2, caja_y1 + 22, p["nombre"], fn, T["titulo"])
    else:
        pm.poner_producto(img, (margen, caja_y0, W - margen, caja_y1), None, False, tema)

    d = ImageDraw.Draw(img)
    if con_sticker:
        fsk = pm.playfair(34, 400, True)
        pm.txt(d, CX, y_sticker - 22, spec["sticker"], fsk, T["sec"])
        pm.filete(d, CX, y_sticker + 34, 90, tema)
    else:
        if spec.get("cta"):
            pm.boton(img, CX, H - 470, spec["cta"], 36, tema)
        pm.pie(img, H - 190 - 28 * 2.0, 28, tema)
    return img.convert("RGB")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as fh:
        specs = json.load(fh)
    base = os.path.dirname(os.path.abspath(sys.argv[1]))
    os.makedirs(sys.argv[2], exist_ok=True)
    for s in specs:
        ruta = os.path.join(sys.argv[2], s["archivo"])
        armar(s, base).save(ruta, "PNG")
        print(ruta)


if __name__ == "__main__":
    main()
