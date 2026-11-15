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
  "formato": "historia" | "post",            # opcional, historia por defecto (post = feed 1080x1350)
  "fondo": "blanco" | "bordo",               # opcional, blanco por defecto
  "etiqueta": "Encuesta",                    # Poppins chica en dorado
  "titulo": "¿Dulce o fresco?",              # Cormorant grande, en mayúsculas
  "subtitulo": "Votá y te recomiendo uno",   # opcional, Poppins espaciada en mayúsculas
  "productos": [                              # 0 a 3 productos
     {"imagen": "fuente/scandal.png", "nombre": "Dulce"},
     {"imagen": "fuente/lightblue.jpg", "nombre": "Fresco"}
  ],
  "sticker": "Votá acá abajo",               # texto chico sobre el espacio del sticker
  "alto_sticker": 300,                       # alto del espacio libre
  "borde_blanco": true,                      # opcional: contorno blanco alrededor de cada perfume
  "chips": [{"texto": "Promociones", "x": 0.1, "y": 0.1, "giro": -6}],  # etiquetas tipo sticker;
                                             # x, y relativos a la caja del producto
  "cta": "..."                               # sin sticker: botón y pie
}
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "herramientas", "pieza-marca", "scripts"))
import crear_pieza as pm  # noqa: E402

W = 1080
CX = W / 2
# historia (1080x1920) o post de feed (1080x1350)
MEDIDAS = {
    "historia": dict(H=1920, top=170, logo_w=230, eti=30, tit=(112, 64), sub=28, abajo_sticker=220,
                     limite=520, cta_y=470, cta=36, pie=28, pie_y=190, chip=30),
    "post": dict(H=1350, top=56, logo_w=190, eti=24, tit=(96, 56), sub=22, abajo_sticker=60,
                 limite=290, cta_y=250, cta=30, pie=22, pie_y=52, chip=26),
}


def chip(img, cx, cy, texto, giro, tema, tam=30):
    """Etiqueta tipo sticker: píldora con texto en Poppins espaciada, un poco girada y con sombra.
    Sobre bordó va rosa marfil con texto bordó; sobre blanco, bordó con texto rosa marfil. Filete dorado."""
    fondo_c, texto_c = (pm.MARFIL, pm.BORDO) if tema == "bordo" else (pm.BORDO, pm.MARFIL)
    f = pm.poppins(tam, "Medium")
    t = texto.upper()
    esp = tam * 0.16
    d0 = ImageDraw.Draw(img)
    tw = pm.ancho_txt(d0, t, f, esp)
    th = pm.alto_linea(f)
    px, py = tam * 1.0, tam * 0.55
    w, h = int(tw + 2 * px), int(th + 2 * py)
    k = 3  # se dibuja grande y se achica, para bordes suaves al girar
    capa = Image.new("RGBA", (w * k + 40, h * k + 40), (0, 0, 0, 0))
    dc = ImageDraw.Draw(capa)
    dc.rounded_rectangle((20, 20, 20 + w * k, 20 + h * k), radius=h * k / 2, fill=fondo_c,
                         outline=pm.TEMAS[tema]["acento"], width=2 * k)
    fk = pm.poppins(tam * k, "Medium")
    pm.txt(dc, 20 + w * k / 2, 20 + py * k - tam * k * 0.06, t, fk, texto_c, esp=esp * k)
    capa = capa.rotate(giro, expand=True, resample=Image.BICUBIC)
    capa = capa.resize((capa.width // k, capa.height // k), Image.LANCZOS)
    x, y = int(cx - capa.width / 2), int(cy - capa.height / 2)
    sombra = Image.new("L", img.size, 0)
    sombra.paste(capa.getchannel("A"), (x, y + 8))
    img.alpha_composite(pm.capa_color(sombra.filter(ImageFilter.GaussianBlur(10)), pm.CUERO, 0.55))
    img.alpha_composite(capa, (x, y))


def armar(spec, base):
    tema = spec.get("fondo", "blanco")
    if tema not in pm.TEMAS:
        tema = "blanco"
    T = pm.TEMAS[tema]
    M = MEDIDAS.get(spec.get("formato", "historia"), MEDIDAS["historia"])
    H = M["H"]
    img = pm.lienzo(W, H, tema)
    d = ImageDraw.Draw(img)

    # --- logo y textos de arriba ---
    logo = pm.logo_mascara("texto", M["logo_w"])
    y = M["top"]
    img.alpha_composite(pm.capa_color(logo, T["titulo"]), (int(CX - logo.width / 2), y))
    y += logo.height + M["eti"] * 1.45
    if spec.get("etiqueta"):
        fe = pm.poppins(M["eti"], "Regular")
        pm.txt(d, CX, y, spec["etiqueta"].upper(), fe, T["acento"], esp=M["eti"] * 0.32)
        y += pm.alto_linea(fe, 1.3)
    ft, lt, esp_t = pm.ajustar(d, spec["titulo"].upper(), M["tit"][0], M["tit"][1], W - 140, 3, lambda t: pm.cormorant(t, 600), 0.04)
    for l in lt:
        pm.txt(d, CX, y, l, ft, T["titulo"], esp=esp_t)
        y += pm.alto_linea(ft, 1.0)
    if spec.get("subtitulo"):
        y += 14
        fs, ls, esp_s = pm.ajustar(d, spec["subtitulo"].upper(), M["sub"], M["sub"] * 0.8, W - 180, 2, lambda t: pm.poppins(t, "Regular"), 0.18)
        for l in ls:
            pm.txt(d, CX, y, l, fs, T["sec"], esp=esp_s)
            y += pm.alto_linea(fs, 1.35)

    # --- zona de abajo: sticker, o botón + pie ---
    con_sticker = bool(spec.get("sticker"))
    if con_sticker:
        y_sticker = H - M["abajo_sticker"] - spec.get("alto_sticker", 300)   # espacio libre para el sticker
        limite = y_sticker - 70
    else:
        limite = H - M["limite"]

    # --- productos ---
    prods = spec.get("productos") or []
    caja_y0 = y + (60 if H > 1500 else 40)
    hay_nombres = any(p.get("nombre") for p in prods)
    n = max(1, len(prods))
    margen = 90 if n > 1 else 150
    hueco = 50 if n > 1 else 0
    ancho = (W - 2 * margen - hueco * (n - 1)) / n
    tam = 44  # el mismo tamaño para todos los nombres, el que entre en la columna
    while tam > 26 and any(pm.ancho_txt(d, p.get("nombre", "").upper(), pm.cormorant(tam, 600), tam * 0.06) > ancho + hueco * 0.6 for p in prods):
        tam -= 2
    fn = pm.cormorant(tam, 600)
    caja_y1 = limite - (pm.alto_linea(fn, 1.3) if hay_nombres else 0)
    if prods:
        for i, p in enumerate(prods):
            ruta = p["imagen"] if os.path.isabs(p["imagen"]) else os.path.join(base, p["imagen"])
            im, recortado = pm.cargar_producto(ruta)
            x0 = margen + i * (ancho + hueco)
            ac = pm.poner_producto(img, (x0, caja_y0, x0 + ancho, caja_y1), im, recortado, tema,
                                   borde=12 if spec.get("borde_blanco") else 0)
            if p.get("nombre"):
                pm.txt(ImageDraw.Draw(img), (ac[0] + ac[2]) / 2, caja_y1 + 22, p["nombre"].upper(), fn, T["titulo"], esp=tam * 0.06)
    else:
        ac = pm.poner_producto(img, (margen, caja_y0, W - margen, caja_y1), None, False, tema)

    # --- etiquetas tipo sticker sobre el producto ("Promociones", "Descuentos"...) ---
    for c in spec.get("chips") or []:
        cx_c = ac[0] + (ac[2] - ac[0]) * c.get("x", 0.5)
        cy_c = ac[1] + (ac[3] - ac[1]) * c.get("y", 0.5)
        chip(img, cx_c, cy_c, c["texto"], c.get("giro", 0), tema, c.get("tam", M["chip"]))

    d = ImageDraw.Draw(img)
    if con_sticker:
        fsk = pm.poppins(24, "Regular")
        pm.txt(d, CX, y_sticker - 16, spec["sticker"].upper(), fsk, T["sec"], esp=24 * 0.3)
        pm.filete(d, CX, y_sticker + 34, 90, tema)
    else:
        if spec.get("cta"):
            pm.boton(img, CX, H - M["cta_y"], spec["cta"], M["cta"], tema)
        pm.pie(img, H - M["pie_y"] - M["pie"] * 2.0, M["pie"], tema)
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
