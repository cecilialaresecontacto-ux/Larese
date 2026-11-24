#!/usr/bin/env python3
"""
Anuncio del GRUPO MAYORISTA de LARESE STORE con 3 perfumes, fondo blanco.

Uso:
    python3 crear_mayorista.py spec.json historia salida.png        # 1080x1920, historia común de Instagram
    python3 crear_mayorista.py spec.json meta-historia salida.png   # 1080x1920, zonas seguras de Meta
    python3 crear_mayorista.py spec.json meta-post salida.png       # 1080x1350

Spec (JSON):
{
  "antetitulo": "Sumate a nuestro",
  "titulo": "Grupo Mayorista",
  "subtitulo": "Perfumes de marca a precio mayorista",
  "productos": [
    {"imagen": "fotos/a.jpg", "nombre": "Good Girl", "marca": "Carolina Herrera"},
    {"imagen": "fotos/b.png", "nombre": "La Vie Est Belle", "marca": "Lancôme", "solo_frasco": true},
    {"imagen": "fotos/c.webp", "nombre": "Miss Dior", "marca": "Dior"}
  ],
  "boton": "Sumate por WhatsApp",
  "pie": "WhatsApp 0972 736 002"
}
"solo_frasco": si la foto trae frasco y caja separados, se queda con el de la izquierda.
Con 4 productos se arma un grupo (orden: adelante-izq, atrás-izq, atrás-der, adelante-der)
y no se muestran nombres. Con "mostrar_nombres": false tampoco en fila.
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "herramientas", "pieza-fondo-blanco", "scripts"))
from crear_pieza import (  # noqa: E402
    FONDO, GRIS, TEXTO, alto_linea, ancho_txt, capa_color, cargar_producto, fuente,
    logo_mascara, txt,
)

# posiciones (y) de cada bloque; la historia deja libre el 14 % de arriba y el 20 % de abajo
FORMATOS = {
    "historia": dict(size=(1080, 1920), k=1.0, ante_y=190, titulo_y=232, sub_y=360,
                     prod=(440, 1250), prod_sin_nombres=(450, 1360), nombres_y=1275,
                     boton_y=1440, tienda_y=1575, pie_y=1680),
    "meta-historia": dict(size=(1080, 1920), k=1.0, ante_y=300, titulo_y=342, sub_y=470,
                          prod=(545, 1105), prod_sin_nombres=(560, 1205), nombres_y=1130, boton_y=1245, tienda_y=1370, pie_y=1470),
    "meta-post": dict(size=(1080, 1350), k=0.82, ante_y=46, titulo_y=82, sub_y=186,
                      prod=(250, 860), prod_sin_nombres=(255, 950), nombres_y=880, boton_y=990, tienda_y=1105, pie_y=1210),
}


def solo_frasco(prod):
    """Separa frasco y caja por la columna vacía más ancha y devuelve la parte izquierda."""
    a = np.array(prod.getchannel("A")) > 40
    cols = a.any(axis=0)
    mejor, inicio, largo = None, None, 0
    for x, ocupada in enumerate(list(cols) + [True]):
        if not ocupada and inicio is None:
            inicio = x
        elif ocupada and inicio is not None:
            if x - inicio > largo and inicio > 0 and x < len(cols):
                mejor, largo = (inicio, x), x - inicio
            inicio = None
    if not mejor:
        return prod
    izq = prod.crop((0, 0, mejor[0], prod.height))
    return izq.crop(izq.getbbox())


def sin_borde_blanco(p):
    """Achica un poco el recorte y borra el halo blanco que queda del fondo original."""
    a = p.getchannel("A").filter(ImageFilter.MinFilter(5))
    arr = np.array(p.convert("RGB")).astype(int)
    blanco = (arr.min(axis=2) > 232)
    borde = np.array(a.filter(ImageFilter.MinFilter(9))) < 255  # solo cerca del contorno
    alfa = np.array(a)
    alfa[blanco & borde] = 0
    p = p.copy()
    p.putalpha(Image.fromarray(alfa).filter(ImageFilter.GaussianBlur(0.8)))
    return p


def pegar(img, p, cx, base, ancho_max, alto_max):
    esc = min(ancho_max / p.width, alto_max / p.height)
    p = p.resize((int(p.width * esc), int(p.height * esc)), Image.LANCZOS)
    p = sin_borde_blanco(p)
    x, y = int(cx - p.width / 2), int(base - p.height)
    # sombra de contacto
    s = Image.new("L", img.size, 0)
    sw = p.width * 0.8
    ImageDraw.Draw(s).ellipse((cx - sw / 2, base - 12, cx + sw / 2, base + 14), fill=150)
    img.alpha_composite(capa_color(s.filter(ImageFilter.GaussianBlur(14)), (0, 0, 0), 0.40))
    img.alpha_composite(p, (x, y))


def armar(SPEC, formato):
    F = FORMATOS[formato]
    w, h = F["size"]
    k = F["k"]
    cx = w / 2
    img = Image.new("RGBA", (w, h), FONDO + (255,))
    d = ImageDraw.Draw(img)

    # encabezado
    fa = fuente(34 * k, "Medium")
    txt(d, cx, F["ante_y"], SPEC["antetitulo"].upper(), fa, GRIS, esp=34 * k * 0.22)
    ft = fuente(96 * k, "ExtraBold")
    titulo = SPEC["titulo"].upper()
    while ancho_txt(d, titulo, ft, 2) > w - 100:
        ft = fuente(ft.size - 4, "ExtraBold")
    txt(d, cx, F["titulo_y"], titulo, ft, TEXTO, esp=2)
    fs = fuente(32 * k, "Medium")
    txt(d, cx, F["sub_y"], SPEC["subtitulo"], fs, GRIS)

    sin_nombres = len(SPEC["productos"]) == 4 or not SPEC.get("mostrar_nombres", True)
    y0, y1 = F["prod_sin_nombres"] if sin_nombres else F["prod"]

    prods = SPEC["productos"]
    cargados = []
    for pr in prods:
        p, ok = cargar_producto(pr["imagen"])
        if not ok:
            raise SystemExit(f"No se pudo recortar {pr['imagen']}")
        cargados.append(solo_frasco(p) if pr.get("solo_frasco") else p)
    alto_zona = y1 - y0

    if len(prods) == 4:
        # grupo: los 2 del medio atrás y más grandes, los 2 de las puntas adelante
        # (centro x relativo, base relativa en la zona, alto relativo, ancho máx relativo)
        lugares = [(0.22, 1.00, 0.46, 0.40), (0.35, 0.76, 0.74, 0.36),
                   (0.70, 0.76, 0.74, 0.30), (0.79, 1.00, 0.46, 0.38)]
        for i in (1, 2, 0, 3):  # primero los de atrás
            rx, rb, rh, rw = lugares[i]
            pegar(img, cargados[i], w * rx, y0 + alto_zona * rb, w * rw, alto_zona * rh)
    else:
        # en fila, sobre una misma base (el del medio un poco más grande)
        n = len(prods)
        margen = 24
        pesos = [0.95, 1.10, 0.95] if n == 3 else [1.0] * n
        anchos = [(w - 2 * margen) * pe / sum(pesos) for pe in pesos]
        for i, pr in enumerate(prods):
            slot = anchos[i]
            pcx = margen + sum(anchos[:i]) + slot / 2
            pegar(img, cargados[i], pcx, y1, slot * 0.98, alto_zona * (1.0 if i == n // 2 else 0.90))
            if SPEC.get("mostrar_nombres", True) and pr.get("nombre"):
                d = ImageDraw.Draw(img)
                fn = fuente(31 * k, "Bold")
                nombre = pr["nombre"].upper()
                while ancho_txt(d, nombre, fn, 1.5) > slot - 16:
                    fn = fuente(fn.size - 2, "Bold")
                y = F["nombres_y"]
                txt(d, pcx, y, nombre, fn, TEXTO, esp=1.5)
                txt(d, pcx, y + alto_linea(fn, 1.05), pr.get("marca", ""), fuente(24 * k, "Medium"), GRIS)

    # botón
    d = ImageDraw.Draw(img)
    fb = fuente(38 * k, "SemiBold")
    bw = ancho_txt(d, SPEC["boton"], fb) + 120 * k
    bh = 86 * k
    by = F["boton_y"]
    d.rounded_rectangle((cx - bw / 2, by, cx + bw / 2, by + bh), radius=bh / 2, fill=TEXTO)
    a, b = fb.getmetrics()
    d.text((cx - ancho_txt(d, SPEC["boton"], fb) / 2, by + (bh - a - b) / 2 + 2), SPEC["boton"], font=fb, fill=FONDO)

    # larese STORE | MAYORISTA
    logo = logo_mascara("texto", 270 * k)
    fx = fuente(40 * k, "Bold")
    extra = "MAYORISTA"
    esp = fx.size * 0.14
    we = ancho_txt(d, extra, fx, esp)
    gap = 30 * k
    y = F["tienda_y"]
    xi = cx - (logo.width + 2 * gap + we) / 2
    img.alpha_composite(capa_color(logo, TEXTO), (int(xi), int(y)))
    d = ImageDraw.Draw(img)
    xl = xi + logo.width + gap
    d.line((xl, y + 4, xl, y + logo.height - 2), fill=TEXTO, width=3)
    a, _ = fx.getmetrics()
    txt(d, xl + gap + we / 2, y + logo.height * 0.80 - a, extra, fx, TEXTO, esp=esp)

    # pie
    txt(d, cx, F["pie_y"], SPEC["pie"], fuente(28 * k, "Medium"), GRIS)
    return img.convert("RGB")


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[2] not in FORMATOS:
        print(__doc__)
        sys.exit(1)
    ruta_spec = os.path.abspath(sys.argv[1])
    with open(ruta_spec, encoding="utf-8") as fh:
        spec = json.load(fh)
    for pr in spec["productos"]:
        if not os.path.isabs(pr["imagen"]):
            pr["imagen"] = os.path.join(os.path.dirname(ruta_spec), pr["imagen"])
    armar(spec, sys.argv[2]).save(sys.argv[3], "PNG")
    print(sys.argv[3])
