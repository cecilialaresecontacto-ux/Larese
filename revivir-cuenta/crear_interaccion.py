#!/usr/bin/env python3
"""
Historias de interacción de LARESE STORE (fondo blanco) con espacio libre para el sticker
de Instagram: encuesta, quiz, slider o caja de preguntas.

Usa las fuentes, el logo y el recorte de producto de herramientas/pieza-fondo-blanco.

Uso:
    python3 crear_interaccion.py historias.json carpeta_salida/

historias.json es una lista de specs:
{
  "archivo": "01-dulce-o-fresco.png",
  "etiqueta": "Encuesta",                    # línea chica arriba
  "titulo": "¿Dulce o fresco?",              # pregunta grande
  "subtitulo": "Votá y te recomiendo uno",   # opcional
  "productos": [                              # 0 a 3 productos, cada uno con nombre opcional
     {"imagen": "fuente/scandal.png", "nombre": "Dulce"},
     {"imagen": "fuente/lightblue.jpg", "nombre": "Fresco"}
  ],
  "sticker": "Votá acá abajo",               # texto chico gris sobre el espacio del sticker
  "cta": "...", "pie": true                  # opcional: botón y pie (para historias sin sticker)
}
"""
import json
import os
import sys

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "herramientas", "pieza-fondo-blanco", "scripts"))
import crear_pieza as cp  # noqa: E402

W, H = 1080, 1920
CX = W / 2


def armar(spec, base):
    img = Image.new("RGBA", (W, H), cp.FONDO + (255,))
    d = ImageDraw.Draw(img)

    # --- logo y textos de arriba ---
    logo = cp.logo_mascara("texto", 250)
    y = 170
    img.alpha_composite(cp.capa_color(logo, cp.TEXTO), (int(CX - logo.width / 2), y))
    y += logo.height + 44
    if spec.get("etiqueta"):
        fe = cp.fuente(34, b"SemiBold")
        cp.txt(d, CX, y, spec["etiqueta"].upper(), fe, cp.GRIS, esp=2)
        y += cp.alto_linea(fe, 1.1)
    ft, lt, _ = cp.ajustar(d, spec["titulo"].upper(), 112, 64, W - 130, 3, b"Bold")
    for l in lt:
        cp.txt(d, CX, y, l, ft, cp.TEXTO)
        y += cp.alto_linea(ft, 0.86)
    if spec.get("subtitulo"):
        y += 14
        fs, ls, _ = cp.ajustar(d, spec["subtitulo"], 40, 30, W - 200, 2, b"Medium")
        for l in ls:
            cp.txt(d, CX, y, l, fs, cp.GRIS)
            y += cp.alto_linea(fs, 1.15)

    # --- zona de abajo: sticker, o botón + pie ---
    con_sticker = bool(spec.get("sticker"))
    if con_sticker:
        alto_sticker = spec.get("alto_sticker", 300)
        fondo_zona = H - 220                      # lo de abajo lo tapa la barra de respuesta
        y_sticker = fondo_zona - alto_sticker     # espacio blanco libre para el sticker
        limite = y_sticker - 60
    else:
        limite = H - 520

    # --- productos ---
    prods = spec.get("productos") or []
    caja_y0 = y + 50
    nombre_f = cp.fuente(36, b"SemiBold")
    alto_nombre = cp.alto_linea(nombre_f, 1.2) if any(p.get("nombre") for p in prods) else 0
    caja_y1 = limite - alto_nombre
    if prods:
        n = len(prods)
        margen = 80
        hueco = 40 if n > 1 else 0
        ancho = (W - 2 * margen - hueco * (n - 1)) / n
        tam = 36  # el mismo tamaño para todos los nombres, el que entre en la columna
        while tam > 22 and any(d.textlength(p.get("nombre", "").upper(), font=cp.fuente(tam, b"SemiBold")) + 2 * len(p.get("nombre", "")) > ancho for p in prods):
            tam -= 2
        nombre_f = cp.fuente(tam, b"SemiBold")
        for i, p in enumerate(prods):
            ruta = p["imagen"] if os.path.isabs(p["imagen"]) else os.path.join(base, p["imagen"])
            im, recortado = cp.cargar_producto(ruta)
            x0 = margen + i * (ancho + hueco)
            caja = (x0, caja_y0, x0 + ancho, caja_y1)
            pc = cp.pegar_producto(img, im, recortado, caja)
            if p.get("nombre"):
                d = ImageDraw.Draw(img)
                cp.txt(d, (pc[0] + pc[2]) / 2, caja_y1 + 18, p["nombre"].upper(), nombre_f, cp.TEXTO, esp=2)
    else:
        cp.monograma_grande(img, (120, caja_y0, W - 120, caja_y1))

    d = ImageDraw.Draw(img)
    if con_sticker:
        fsk = cp.fuente(30, b"Medium")
        cp.txt(d, CX, y_sticker - 10, spec["sticker"], fsk, (150, 150, 150))
    else:
        yb = H - 470
        if spec.get("cta"):
            cp.boton(img, CX, yb, spec["cta"], 40, cp.ACENTO)
        if spec.get("pie", True):
            cp.pie(img, H - 190 - 30 * 2.1, 30, cp.ACENTO)
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
