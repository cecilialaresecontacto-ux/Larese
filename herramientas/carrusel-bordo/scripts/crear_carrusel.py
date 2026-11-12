#!/usr/bin/env python3
"""
Carrusel de LARESE STORE con la paleta bordó y crema (estilo editorial).

Slides de 1080x1350 que alternan fondo crema y fondo bordó con borde de estampilla,
títulos en Playfair Display, acentos en cursiva (Pinyon Script) y textos chicos en Poppins.

Uso:
    python3 crear_carrusel.py carrusel.json carpeta_salida/

Spec (JSON):
{
  "fotos": "fotos",                 # carpeta de las fotos, relativa al JSON
  "portada": {
    "titulo": "Los más pedidos",
    "cursiva": "del 2026",
    "etiquetas": ["14 favoritos", "de nuestras clientas"],
    "fotos": ["02-good-girl.jpg", "05-miss-dior.jpg", "10-libre.png"],
    "pie": "Deslizá y encontrá el tuyo"
  },
  "productos": [
    {"nombre": "Paradoxe", "marca": "Prada", "tipo": "Eau de Parfum",
     "notas": "Pera y cítricos ...", "precio": 85000, "foto": "01-paradoxe.png"}
  ],
  "cierre": {
    "titulo": "¿Cuál es tu favorito?",
    "cursiva": "contanos en comentarios",
    "texto": "...",
    "boton": "WhatsApp 0972 736 002"
  }
}
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(AQUI, "..", "assets")
FUENTES = os.path.join(ASSETS, "fonts")

W, H = 1080, 1350
BORDO = (92, 18, 32)
BORDO_SUAVE = (130, 62, 72)
CREMA = (244, 238, 229)
CREMA_OSC = (234, 223, 209)
CREMA_SUAVE = (222, 196, 190)
WHATSAPP = "0972 736 002"


# ---------------- tipografías ----------------

def serif(tam, peso=430):
    f = ImageFont.truetype(os.path.join(FUENTES, "PlayfairDisplay.ttf"), int(tam))
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f


def serif_it(tam, peso=420):
    f = ImageFont.truetype(os.path.join(FUENTES, "PlayfairDisplay-Italic.ttf"), int(tam))
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f


def cursiva(tam):
    return ImageFont.truetype(os.path.join(FUENTES, "PinyonScript.ttf"), int(tam))


def sans(tam, peso="Medium"):
    return ImageFont.truetype(os.path.join(FUENTES, f"Poppins-{peso}.ttf"), int(tam))


def guaranies(v):
    return "Gs. " + f"{int(v):,}".replace(",", ".")


# ---------------- texto ----------------

def ancho(d, t, f, esp=0):
    return d.textlength(t, font=f) + esp * max(len(t) - 1, 0)


def escribir(d, x, y, t, f, color, esp=0, ancla="la"):
    """Escribe con espaciado entre letras. ancla: 'la' izquierda, 'ma' centro, 'ra' derecha."""
    w = ancho(d, t, f, esp)
    if ancla == "ma":
        x -= w / 2
    elif ancla == "ra":
        x -= w
    if not esp:
        d.text((x, y), t, font=f, fill=color)
        return
    for c in t:
        d.text((x, y), c, font=f, fill=color)
        x += d.textlength(c, font=f) + esp


def envolver(d, t, f, maxw):
    lineas, actual = [], ""
    for p in t.split():
        prueba = (actual + " " + p).strip()
        if actual and d.textlength(prueba, font=f) > maxw:
            lineas.append(actual)
            actual = p
        else:
            actual = prueba
    if actual:
        lineas.append(actual)
    return lineas


def equilibrar(d, t, f, maxw):
    """Una línea si entra; si no, dos líneas de largo parecido."""
    if d.textlength(t, font=f) <= maxw:
        return [t]
    p = t.split()
    mejor = min(range(1, len(p)), key=lambda i: max(d.textlength(" ".join(p[:i]), font=f),
                                                      d.textlength(" ".join(p[i:]), font=f)))
    return [" ".join(p[:mejor]), " ".join(p[mejor:])]


def alto_bbox(f, muestra="ÁHgjy"):
    a, b = f.getbbox(muestra)[1], f.getbbox(muestra)[3]
    return b - a


# ---------------- elementos ----------------

def logo(img, cx, y, ancho_px, color):
    m = Image.open(os.path.join(ASSETS, "logo_texto_mascara.png")).convert("L")
    m = m.resize((int(ancho_px), int(m.height * ancho_px / m.width)), Image.LANCZOS)
    capa = Image.new("RGBA", m.size, color + (0,))
    capa.putalpha(m)
    img.alpha_composite(capa, (int(cx - m.width / 2), int(y)))
    return m.height


def cargar_producto(ruta):
    """Recorta el producto si la foto tiene fondo liso. Devuelve (RGBA, recortado)."""
    im = ImageOps.exif_transpose(Image.open(ruta)).convert("RGBA")
    a = np.array(im)
    if (a[..., 3] < 250).mean() > 0.02:
        return im.crop(im.getbbox()), True
    rgb = a[..., :3].astype(int)
    borde = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
    if borde.std(axis=0).max() > 22:
        return im, False
    marcador = (1, 254, 3)
    base = im.convert("RGB")
    bw, bh = base.size
    for x, y in [(0, 0), (bw - 1, 0), (0, bh - 1), (bw - 1, bh - 1),
                 (bw // 2, 0), (bw // 2, bh - 1), (0, bh // 2), (bw - 1, bh // 2)]:
        if base.getpixel((x, y)) != marcador:
            ImageDraw.floodfill(base, (x, y), marcador, thresh=34)
    fondo_px = np.all(np.array(base) == marcador, axis=-1)
    alfa = Image.fromarray(np.where(fondo_px, 0, 255).astype("uint8"))
    alfa = alfa.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
    im.putalpha(alfa)
    caja = alfa.point(lambda v: 255 if v > 30 else 0).getbbox()
    return (im.crop(caja), True) if caja else (im, False)


def arco(img, caja, color):
    """Rectángulo con la parte de arriba en semicírculo (arco)."""
    x0, y0, x1, y1 = caja
    r = (x1 - x0) / 2
    d = ImageDraw.Draw(img)
    d.pieslice((x0, y0, x1, y0 + 2 * r), 180, 360, fill=color)
    d.rectangle((x0, y0 + r, x1, y1), fill=color)


def pegar_producto(img, prod, caja, sombra_color=(40, 10, 15)):
    """Pega el producto dentro de la caja, apoyado abajo, con sombra suave."""
    x0, y0, x1, y1 = caja
    p = prod.copy()
    esc = min((x1 - x0) / p.width, (y1 - y0) / p.height)
    p = p.resize((max(1, int(p.width * esc)), max(1, int(p.height * esc))), Image.LANCZOS)
    px = int((x0 + x1) / 2 - p.width / 2)
    py = int(y1 - p.height)
    # sombra de apoyo
    sombra = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sombra)
    ds.ellipse((px + p.width * 0.08, y1 - 16, px + p.width * 0.92, y1 + 16), fill=sombra_color + (70,))
    img.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(14)))
    img.alpha_composite(p, (px, py))


def tarjeta_foto(img, foto, caja, color_borde):
    """Para fotos que no se pueden recortar: tarjeta con borde fino."""
    x0, y0, x1, y1 = caja
    f = foto.convert("RGB")
    esc = min((x1 - x0) / f.width, (y1 - y0) / f.height)
    f = f.resize((int(f.width * esc), int(f.height * esc)), Image.LANCZOS)
    px, py = int((x0 + x1) / 2 - f.width / 2), int((y0 + y1) / 2 - f.height / 2)
    img.paste(f, (px, py))
    ImageDraw.Draw(img).rectangle((px - 1, py - 1, px + f.width, py + f.height), outline=color_borde, width=2)


def estampilla(img, margen=34, r=13, paso=40):
    """Fondo crema con un rectángulo bordó de borde troquelado (como una estampilla)."""
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, H), fill=CREMA)
    x0, y0, x1, y1 = margen, margen, W - margen, H - margen
    d.rectangle((x0, y0, x1, y1), fill=BORDO)
    nx = int((x1 - x0) / paso)
    ny = int((y1 - y0) / paso)
    for i in range(nx + 1):
        x = x0 + (x1 - x0) * i / nx
        d.ellipse((x - r, y0 - r, x + r, y0 + r), fill=CREMA)
        d.ellipse((x - r, y1 - r, x + r, y1 + r), fill=CREMA)
    for j in range(ny + 1):
        y = y0 + (y1 - y0) * j / ny
        d.ellipse((x0 - r, y - r, x0 + r, y + r), fill=CREMA)
        d.ellipse((x1 - r, y - r, x1 + r, y + r), fill=CREMA)


def pie(img, y, color):
    d = ImageDraw.Draw(img)
    f = sans(21)
    t = f"WhatsApp {WHATSAPP}   ·   Envíos a todo Paraguay"
    d.line((W / 2 - 230, y - 22, W / 2 + 230, y - 22), fill=color, width=1)
    escribir(d, W / 2, y, t, f, color, ancla="ma")


# ---------------- slides ----------------

def slide_producto(p, n, fotos_dir, oscuro):
    img = Image.new("RGBA", (W, H), CREMA + (255,))
    if oscuro:
        estampilla(img)
    d = ImageDraw.Draw(img)
    principal = CREMA if oscuro else BORDO
    suave = CREMA_SUAVE if oscuro else BORDO_SUAVE
    fondo_arco = CREMA if oscuro else CREMA_OSC

    logo(img, W / 2, 70, 118, suave)

    # [ 01 ]  Título
    izq = 110
    f_num = serif(118, 380)
    f_cor = serif(150, 300)
    y_num = 150
    num = f"{n:02d}"
    escribir(d, izq, y_num - 22, "[", f_cor, principal)
    xb = izq + ancho(d, "[", f_cor) + 14
    escribir(d, xb, y_num, num, f_num, principal)
    xb2 = xb + ancho(d, num, f_num) + 14
    escribir(d, xb2, y_num - 22, "]", f_cor, principal)
    x_tit = xb2 + ancho(d, "]", f_cor) + 36
    max_tit = W - 100 - x_tit

    tam = 74
    while True:
        f_tit = serif(tam, 450)
        lineas = envolver(d, p["nombre"], f_tit, max_tit)
        if len(lineas) <= 2 or tam <= 48:
            break
        tam -= 4
    alto_l = tam * 1.12
    bloque = alto_l * len(lineas)
    y_t = y_num + 92 - bloque / 2
    for i, l in enumerate(lineas):
        escribir(d, x_tit, y_t + i * alto_l, l, f_tit, principal)
    y_fin_tit = y_t + bloque

    # marca en cursiva, alineada a la derecha
    f_marca = cursiva(64)
    y_marca = max(y_fin_tit, y_num + 150) + 4
    escribir(d, W - 100, y_marca, p["marca"], f_marca, suave, ancla="ra")

    # producto en un arco
    top_arco = y_marca + 100
    caja_arco = (W / 2 - 280, top_arco, W / 2 + 280, 1000)
    arco(img, caja_arco, fondo_arco)
    prod, recortado = cargar_producto(os.path.join(fotos_dir, p["foto"]))
    caja_prod = (caja_arco[0] + 65, top_arco + 120, caja_arco[2] - 65, 1000 - 30)
    if recortado:
        pegar_producto(img, prod, caja_prod)
    else:
        tarjeta_foto(img, prod, caja_prod, suave)
    d = ImageDraw.Draw(img)
    d.line((caja_arco[0] - 40, 1000, caja_arco[2] + 40, 1000), fill=suave, width=2)

    # tipo + notas
    f_tipo = sans(19, "SemiBold")
    escribir(d, W / 2, 1024, p.get("tipo", "").upper(), f_tipo, suave, esp=5, ancla="ma")
    f_notas = serif_it(30, 400)
    lineas = equilibrar(d, p["notas"], f_notas, 760)
    y = 1066 if len(lineas) == 2 else 1084
    for l in lineas:
        escribir(d, W / 2, y, l, f_notas, principal, ancla="ma")
        y += 40

    # precio
    f_desde = cursiva(52)
    f_precio = serif(50, 520)
    t_precio = guaranies(p["precio"])
    w_total = ancho(d, "desde", f_desde) + 22 + ancho(d, t_precio, f_precio)
    x = W / 2 - w_total / 2
    y_p = 1158
    escribir(d, x, y_p - 2, "desde", f_desde, suave)
    escribir(d, x + ancho(d, "desde", f_desde) + 22, y_p, t_precio, f_precio, principal)

    pie(img, 1272, suave)
    return img


def slide_portada(s, fotos_dir):
    img = Image.new("RGBA", (W, H), CREMA + (255,))
    d = ImageDraw.Draw(img)
    logo(img, W / 2, 70, 118, BORDO_SUAVE)

    # ( Los más pedidos )
    f_t = serif(96, 450)
    f_par = serif(170, 280)
    t = s["titulo"]
    wt = ancho(d, t, f_t)
    y_t = 190
    escribir(d, W / 2, y_t, t, f_t, BORDO, ancla="ma")
    escribir(d, W / 2 - wt / 2 - 40, y_t - 46, "(", f_par, BORDO, ancla="ra")
    escribir(d, W / 2 + wt / 2 + 40, y_t - 46, ")", f_par, BORDO)
    escribir(d, W / 2, y_t + 112, s["cursiva"], cursiva(120), BORDO_SUAVE, ancla="ma")

    # arco bordó con productos
    caja_arco = (W / 2 - 360, 470, W / 2 + 360, 1120)
    arco(img, caja_arco, BORDO)
    prods = [cargar_producto(os.path.join(fotos_dir, f)) for f in s["fotos"]]
    prods = [p for p, ok in prods if ok]
    n = len(prods)
    if n:
        anchos = [560 / n * 1.25] * n
        for i, p in enumerate(prods):
            cx = W / 2 + (i - (n - 1) / 2) * 205
            alto = 440 if i == (n - 1) // 2 or n == 1 else 350
            esc = min(anchos[i] / p.width, alto / p.height)
            q = p.resize((int(p.width * esc), int(p.height * esc)), Image.LANCZOS)
            pegar_producto(img, q, (cx - q.width / 2, 1095 - q.height, cx + q.width / 2, 1095))
    d = ImageDraw.Draw(img)

    # etiquetas tipo píldora (como en la referencia)
    for i, (txt, (cx, cy)) in enumerate(zip(s["etiquetas"], [(800, 560), (290, 690)])):
        f = cursiva(66)
        tw = ancho(d, txt, f)
        caja = (cx - tw / 2 - 34, cy - 46, cx + tw / 2 + 34, cy + 46)
        capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
        dc = ImageDraw.Draw(capa)
        dc.rounded_rectangle(caja, radius=46, fill=CREMA if i == 0 else BORDO,
                             outline=BORDO if i == 0 else CREMA, width=3)
        bb = f.getbbox(txt)
        dc.text((cx - tw / 2, cy - (bb[1] + bb[3]) / 2), txt, font=f, fill=BORDO if i == 0 else CREMA)
        img.alpha_composite(capa)
    d = ImageDraw.Draw(img)

    f_pie = sans(21, "SemiBold")
    tp = s["pie"].upper()
    wp = ancho(d, tp, f_pie, 4)
    escribir(d, W / 2 - 30, 1160, tp, f_pie, BORDO_SUAVE, esp=4, ancla="ma")
    xa, ya = W / 2 - 30 + wp / 2 + 22, 1175
    d.line((xa, ya, xa + 44, ya), fill=BORDO_SUAVE, width=2)
    d.line((xa + 34, ya - 8, xa + 44, ya), fill=BORDO_SUAVE, width=2)
    d.line((xa + 34, ya + 8, xa + 44, ya), fill=BORDO_SUAVE, width=2)
    pie(img, 1272, BORDO_SUAVE)
    return img


def slide_cierre(s):
    img = Image.new("RGBA", (W, H), CREMA + (255,))
    estampilla(img)
    d = ImageDraw.Draw(img)
    logo(img, W / 2, 110, 300, CREMA)

    f_t = serif(92, 450)
    y = 330
    for l in envolver(d, s["titulo"], f_t, 820):
        escribir(d, W / 2, y, l, f_t, CREMA, ancla="ma")
        y += 108
    escribir(d, W / 2, y + 6, s["cursiva"], cursiva(78), CREMA_SUAVE, ancla="ma")

    y += 150
    d.line((W / 2 - 60, y, W / 2 + 60, y), fill=CREMA_SUAVE, width=2)
    y += 44
    f_x = sans(30)
    for l in envolver(d, s["texto"], f_x, 720):
        escribir(d, W / 2, y, l, f_x, CREMA, ancla="ma")
        y += 48

    y += 40
    f_x2 = serif_it(34, 420)
    for l in s.get("extras", []):
        escribir(d, W / 2, y, l, f_x2, CREMA_SUAVE, ancla="ma")
        y += 50

    # botón
    f_b = sans(32, "SemiBold")
    tb = s["boton"]
    tw = ancho(d, tb, f_b)
    cy = max(y + 90, 1090)
    d.rounded_rectangle((W / 2 - tw / 2 - 48, cy - 42, W / 2 + tw / 2 + 48, cy + 42), radius=42, fill=CREMA)
    bb = f_b.getbbox(tb)
    d.text((W / 2 - tw / 2, cy - (bb[1] + bb[3]) / 2), tb, font=f_b, fill=BORDO)
    escribir(d, W / 2, cy + 78, s.get("debajo_boton", "o en el link de la bio"), serif_it(30), CREMA_SUAVE, ancla="ma")
    return img


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python3 crear_carrusel.py carrusel.json carpeta_salida/")
    ruta_spec, salida = sys.argv[1], sys.argv[2]
    spec = json.load(open(ruta_spec, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(ruta_spec))
    fotos = os.path.join(base, spec.get("fotos", "."))
    os.makedirs(salida, exist_ok=True)

    slides = [slide_portada(spec["portada"], fotos)]
    for i, p in enumerate(spec["productos"], 1):
        slides.append(slide_producto(p, i, fotos, oscuro=(i % 2 == 0)))
    slides.append(slide_cierre(spec["cierre"]))

    for i, s in enumerate(slides, 1):
        ruta = os.path.join(salida, f"{i:02d}.png")
        s.convert("RGB").save(ruta, optimize=True)
        print(ruta)


if __name__ == "__main__":
    main()
