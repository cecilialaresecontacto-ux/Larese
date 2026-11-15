#!/usr/bin/env python3
"""
Piezas para redes de LARESE STORE con la paleta y la tipografía de marca.

Paleta:
    Crema        #F8F4EB  fondo claro principal
    Bordó vino   #41030B  fondo oscuro, píldoras, botones
    Bordó cuero  #2A0B0D  sombras y fondos profundos
    Tinta        #321918  títulos y textos sobre crema
    Malva        #7B5B5B  textos secundarios sobre crema
    Rosa marfil  #FCE5DA  textos sobre bordó, arcos
    Dorado       #997957  acentos y detalles finos

Tipografía:
    Playfair Display         títulos, nombres de perfume, precios
    Playfair Display Italic  notas y frases cortas
    Pinyon Script            acentos: marcas, "Desde", frases
    Poppins                  textos chicos, etiquetas, botones

Uso:
    python3 crear_pieza.py spec.json salida.png
    python3 crear_pieza.py spec.json carpeta_salida/      # para carruseles

Spec (JSON). Solo "formato" y "titulo" son obligatorios:

{
  "formato": "post" | "cuadrado" | "historia" | "portada" | "carrusel",
  "fondo": "crema" | "bordo",             # opcional, crema por defecto
  "etiqueta": "Decant original",          # Poppins chica en dorado, arriba
  "titulo": "Good Girl Blush",            # Playfair grande (no se pasa a mayúsculas)
  "marca": "Carolina Herrera",            # Pinyon Script, debajo del título
  "subtitulo": "Eau de Parfum · 3, 5 y 10 ml",   # Poppins espaciada en mayúsculas
  "nota": "Almendra, café y rosa",        # Playfair italic, frase corta
  "precio": 40000,                        # número en guaraníes -> "Gs. 40.000"
  "precio_prefijo": "Desde",              # va en Pinyon Script
  "precio_anterior": 50000,               # tachado
  "descuento": "-20%",                    # sello bordó
  "imagen": "producto.png",               # foto (fondo liso o PNG recortado)
  "cta": "¡Pedí el tuyo!",                # botón píldora bordó
  "gancho": "...",                        # solo portada: frase grande en lugar del título
  "slides": [ {...}, {...} ]              # solo carrusel: un spec por slide
}

Los campos "color" y "categoria" de la skill se ignoran. El pie (WhatsApp y envíos) se agrega solo.
El producto va directo sobre el fondo, sin arcos ni franjas (las fotos con fondo van como tarjeta redondeada).
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(AQUI, "..", "assets")
FUENTES = os.path.join(ASSETS, "fonts")

WHATSAPP = "0972 736 002"
ENVIOS = "Envíos a todo Paraguay"

CREMA = (248, 244, 235)
BORDO = (65, 3, 11)
CUERO = (42, 11, 13)
TINTA = (50, 25, 24)
MALVA = (123, 91, 91)
MARFIL = (252, 229, 218)
DORADO = (153, 121, 87)

TEMAS = {
    # fondo, título, secundario, acento, botón, texto del botón
    "crema": dict(fondo=CREMA, titulo=TINTA, sec=MALVA, acento=DORADO, boton=BORDO, boton_txt=MARFIL),
    "bordo": dict(fondo=BORDO, titulo=MARFIL, sec=(222, 196, 186), acento=(196, 163, 122),
                  boton=MARFIL, boton_txt=BORDO),
}

TAMANOS = {
    "post": (1080, 1350),
    "cuadrado": (1080, 1080),
    "historia": (1080, 1920),
    "portada": (1080, 1920),
}


# ---------------- tipografía ----------------

def playfair(tam, peso=500, italic=False):
    f = ImageFont.truetype(os.path.join(FUENTES, "PlayfairDisplay-Italic.ttf" if italic else "PlayfairDisplay.ttf"), int(tam))
    f.set_variation_by_axes([peso])
    return f


def script(tam):
    return ImageFont.truetype(os.path.join(FUENTES, "PinyonScript-Regular.ttf"), int(tam))


def poppins(tam, peso="Regular"):
    if peso not in ("Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold"):
        peso = "Regular"
    return ImageFont.truetype(os.path.join(FUENTES, f"Poppins-{peso}.ttf"), int(tam))


def guaranies(valor):
    if valor in (None, ""):
        return None
    if isinstance(valor, str):
        dig = "".join(c for c in valor if c.isdigit())
        if not dig:
            return valor
        valor = int(dig)
    return "Gs. " + f"{int(valor):,}".replace(",", ".")


def alto_linea(f, k=1.0):
    a, b = f.getmetrics()
    return (a + b) * k


def ancho_txt(d, t, f, esp=0):
    return d.textlength(t, font=f) + esp * max(0, len(t) - 1) if t else 0


def txt(d, cx, y, t, f, color, esp=0):
    """Texto centrado en cx, con espaciado entre letras opcional."""
    x = cx - ancho_txt(d, t, f, esp) / 2
    if not esp:
        d.text((x, y), t, font=f, fill=color)
        return
    for ch in t:
        d.text((x, y), ch, font=f, fill=color)
        x += d.textlength(ch, font=f) + esp


def envolver(d, t, f, maxw, esp=0):
    lineas, act = [], ""
    for p in t.split():
        prueba = (act + " " + p).strip()
        if ancho_txt(d, prueba, f, esp) <= maxw:
            act = prueba
        else:
            if act:
                lineas.append(act)
            act = p
    if act:
        lineas.append(act)
    return lineas


def ajustar(d, t, tmax, tmin, maxw, maxl, hacer_fuente, esp_rel=0.0):
    """Tamaño de letra más grande con el que el texto entra en maxl líneas."""
    tam = tmax
    while True:
        f = hacer_fuente(tam)
        esp = tam * esp_rel
        ls = envolver(d, t, f, maxw, esp)
        if (len(ls) <= maxl and all(ancho_txt(d, l, f, esp) <= maxw for l in ls)) or tam <= tmin:
            return f, ls, esp
        tam -= 2


# ---------------- producto ----------------

def cargar_producto(ruta):
    """Devuelve (imagen RGBA, se_pudo_recortar). Recorta solo si el fondo es liso o ya es PNG transparente."""
    if not ruta or not os.path.exists(ruta):
        return None, False
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
    W, H = base.size
    for x, y in [(0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1),
                 (W // 2, 0), (W // 2, H - 1), (0, H // 2), (W - 1, H // 2)]:
        if base.getpixel((x, y)) != marcador:
            ImageDraw.floodfill(base, (x, y), marcador, thresh=34)
    fondo_px = np.all(np.array(base) == marcador, axis=-1)
    alfa = Image.fromarray(np.where(fondo_px, 0, 255).astype("uint8"))
    alfa = alfa.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    im.putalpha(alfa)
    caja = alfa.point(lambda v: 255 if v > 30 else 0).getbbox()
    if not caja:
        return im, False
    return im.crop(caja), True


# ---------------- capas ----------------

def lienzo(w, h, tema):
    T = TEMAS[tema]
    if tema == "crema":
        return Image.new("RGBA", (w, h), T["fondo"] + (255,))
    # bordó con una luz suave al centro que cae a bordó cuero en los bordes
    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.clip(np.sqrt(((xx - w / 2) / (w * 0.8)) ** 2 + ((yy - h * 0.48) / (h * 0.65)) ** 2), 0, 1)[..., None]
    arr = np.array(BORDO) * (1 - dist) + np.array(CUERO) * dist
    return Image.fromarray(arr.astype("uint8"), "RGB").convert("RGBA")


def capa_color(mascara, color, opacidad=1.0):
    capa = Image.new("RGBA", mascara.size, color + (0,))
    capa.putalpha(mascara.point(lambda v: int(v * opacidad)))
    return capa


def logo_mascara(nombre, ancho):
    m = Image.open(os.path.join(ASSETS, f"logo_{nombre}_mascara.png")).convert("L")
    return m.resize((int(ancho), int(m.height * ancho / m.width)), Image.LANCZOS)


def poner_producto(img, caja, prod, recortado, tema, abajo=True):
    """Pone el producto lo más grande posible dentro de caja (apoyado abajo o centrado), directo sobre el fondo
    y con una sombra suave. Sin arcos ni franjas detrás (la dueña no los quiere).
    Si la foto no se puede recortar, va como tarjeta con esquinas redondeadas. Devuelve su caja."""
    T = TEMAS[tema]
    x0, y0, x1, y1 = (int(v) for v in caja)
    bw, bh = x1 - x0, y1 - y0
    if prod is None:
        mono = logo_mascara("monograma", min(bw, bh) * 0.6)
        mx, my = int(x0 + (bw - mono.width) / 2), int(y0 + (bh - mono.height) / 2)
        img.alpha_composite(capa_color(mono, T["acento"], 0.35), (mx, my))
        return (mx, my, mx + mono.width, my + mono.height)
    sombra = Image.new("L", img.size, 0)
    sd = ImageDraw.Draw(sombra)
    if recortado:
        esc = min(bw * 0.94 / prod.width, bh * 0.96 / prod.height)
        p = prod.resize((max(1, int(prod.width * esc)), max(1, int(prod.height * esc))), Image.LANCZOS)
        px, py = int(x0 + (bw - p.width) / 2), (int(y1 - p.height) if abajo else int(y0 + (bh - p.height) / 2))
        sw = p.width * 0.8
        sd.ellipse((px + (p.width - sw) / 2, py + p.height - 18, px + (p.width + sw) / 2, py + p.height + 18), fill=140)
        img.alpha_composite(capa_color(sombra.filter(ImageFilter.GaussianBlur(18)), CUERO, 0.5))
    else:
        cw = int(min(bw, bh * 0.8))
        p = ImageOps.fit(prod.convert("RGB"), (cw, bh), Image.LANCZOS).convert("RGBA")
        m = Image.new("L", p.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, p.width, p.height), radius=int(cw * 0.08), fill=255)
        p.putalpha(m)
        px, py = int(x0 + (bw - p.width) / 2), (int(y1 - p.height) if abajo else int(y0 + (bh - p.height) / 2))
        sd.rounded_rectangle((px + 8, py + 18, px + p.width - 8, py + p.height + 18), radius=int(cw * 0.08), fill=120)
        img.alpha_composite(capa_color(sombra.filter(ImageFilter.GaussianBlur(26)), CUERO, 0.35 if tema == "crema" else 0.6))
    img.alpha_composite(p, (px, py))
    return (px, py, px + p.width, py + p.height)


def sello(img, cx, cy, texto, r, tema):
    T = TEMAS[tema]
    fondo_s, txt_s = (BORDO, MARFIL) if tema == "crema" else (MARFIL, BORDO)
    s = Image.new("L", img.size, 0)
    ImageDraw.Draw(s).ellipse((cx - r, cy - r + 8, cx + r, cy + r + 8), fill=120)
    img.alpha_composite(capa_color(s.filter(ImageFilter.GaussianBlur(14)), CUERO, 0.45))
    d = ImageDraw.Draw(img)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fondo_s, outline=T["acento"], width=3)
    f, ls, _ = ajustar(d, texto, int(r * 0.7), 20, r * 1.5, 2, lambda t: playfair(t, 600))
    y = cy - alto_linea(f) * len(ls) / 2 - r * 0.05
    for l in ls:
        txt(d, cx, y, l, f, txt_s)
        y += alto_linea(f)


def boton(img, cx, y, texto, tam, tema):
    T = TEMAS[tema]
    f = poppins(tam, "Medium")
    d = ImageDraw.Draw(img)
    w = d.textlength(texto, font=f)
    h = alto_linea(f)
    px, py = tam * 1.2, tam * 0.5
    caja = (cx - w / 2 - px, y, cx + w / 2 + px, y + h + 2 * py)
    d.rounded_rectangle(caja, radius=(h + 2 * py) / 2, fill=T["boton"])
    txt(d, cx, y + py - tam * 0.05, texto, f, T["boton_txt"])
    return caja[3]


def icono_chat(d, cx, cy, r, c):
    d.ellipse((cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.58), outline=c, width=max(2, int(r * 0.13)))
    d.polygon([(cx - r * 0.52, cy + r * 0.30), (cx - r * 0.74, cy + r * 0.74), (cx - r * 0.16, cy + r * 0.52)], fill=c)
    for dx in (-0.25, 0, 0.25):
        d.ellipse((cx + r * dx - r * 0.07, cy - r * 0.07, cx + r * dx + r * 0.07, cy + r * 0.07), fill=c)


def icono_camion(d, cx, cy, r, c):
    s = r * 0.95
    d.rectangle((cx - s * 0.64, cy - s * 0.34, cx + s * 0.10, cy + s * 0.20), fill=c)
    d.polygon([(cx + s * 0.15, cy - s * 0.14), (cx + s * 0.42, cy - s * 0.14), (cx + s * 0.62, cy + s * 0.04),
               (cx + s * 0.62, cy + s * 0.20), (cx + s * 0.15, cy + s * 0.20)], fill=c)
    for wx in (cx - s * 0.38, cx + s * 0.38):
        d.ellipse((wx - s * 0.15, cy + s * 0.12, wx + s * 0.15, cy + s * 0.42), fill=c)


def pie(img, y, tam, tema):
    T = TEMAS[tema]
    w = img.size[0]
    d = ImageDraw.Draw(img)
    f = poppins(tam, "Regular")
    r = tam * 1.0
    items = [("chat", WHATSAPP), ("camion", ENVIOS)]
    sep = tam * 2.0
    anchos = [2 * r + tam * 0.55 + d.textlength(t, font=f) for _, t in items]
    x = w / 2 - (sum(anchos) + sep) / 2
    cy = y + r
    c_circ, c_ico = (BORDO, MARFIL) if tema == "crema" else (MARFIL, BORDO)
    for (ic, t), aw in zip(items, anchos):
        d.ellipse((x, cy - r, x + 2 * r, cy + r), fill=c_circ)
        (icono_chat if ic == "chat" else icono_camion)(d, x + r, cy, r * 0.82, c_ico)
        d.text((x + 2 * r + tam * 0.55, cy - alto_linea(f) / 2 - tam * 0.02), t, font=f, fill=T["titulo"])
        x += aw + sep


def filete(d, cx, y, largo, tema):
    d.line((cx - largo / 2, y, cx + largo / 2, y), fill=TEMAS[tema]["acento"], width=2)


def medir_precio(spec, tam):
    al = 0
    if spec.get("precio_anterior"):
        al += alto_linea(poppins(tam * 0.36), 1.1)
    if spec.get("precio"):
        al += alto_linea(playfair(tam, 500), 1.0)
    return al


def precio(img, cx, y, spec, tam, tema):
    T = TEMAS[tema]
    d = ImageDraw.Draw(img)
    anterior = guaranies(spec.get("precio_anterior"))
    if anterior:
        f2 = poppins(tam * 0.36)
        w2 = d.textlength(anterior, font=f2)
        d.text((cx - w2 / 2, y), anterior, font=f2, fill=T["sec"])
        a, _ = f2.getmetrics()
        d.line((cx - w2 / 2 - 4, y + a * 0.62, cx + w2 / 2 + 4, y + a * 0.62), fill=T["sec"], width=2)
        y += alto_linea(f2, 1.1)
    actual = guaranies(spec.get("precio"))
    if actual:
        f = playfair(tam, 500)
        pref = spec.get("precio_prefijo")
        fp = script(tam * 0.85)
        wp = d.textlength(pref + " ", font=fp) if pref else 0
        wa = d.textlength(actual, font=f)
        x = cx - (wp + wa) / 2
        if pref:
            # el script se alinea a la línea de base del precio
            d.text((x, y + f.getmetrics()[0] - fp.getmetrics()[0]), pref, font=fp, fill=T["acento"])
        d.text((x + wp, y), actual, font=f, fill=T["titulo"])
        y += alto_linea(f, 1.0)
    return y


# ---------------- armado ----------------

MEDIDAS = {
    "post":     dict(logo_w=190, logo_y=56, eti=24, tit=(100, 60), marca=64, sub=22, nota=32, pre=64, cta=28, pie=22, pie_y=52, lineas=2),
    "cuadrado": dict(logo_w=170, logo_y=46, eti=22, tit=(84, 52), marca=54, sub=20, nota=28, pre=56, cta=26, pie=20, pie_y=44, lineas=2),
    "historia": dict(logo_w=230, logo_y=170, eti=30, tit=(124, 72), marca=84, sub=28, nota=40, pre=84, cta=36, pie=28, pie_y=190, lineas=2),
    "portada":  dict(logo_w=230, logo_y=300, eti=32, tit=(116, 70), marca=84, sub=30, nota=42, pre=80, cta=36, pie=28, pie_y=0, lineas=4),
}


def armar(spec):
    formato = spec.get("formato", "post")
    if formato not in TAMANOS:
        raise SystemExit(f"Formato desconocido: {formato}. Usá: {', '.join(list(TAMANOS) + ['carrusel'])}")
    tema = spec.get("fondo", "crema")
    if tema not in TEMAS:
        tema = "crema"
    T = TEMAS[tema]
    w, h = TAMANOS[formato]
    M = MEDIDAS[formato]
    cx = w / 2

    prod, recortado = cargar_producto(spec.get("imagen"))
    img = lienzo(w, h, tema)
    d = ImageDraw.Draw(img)

    # --- bloque de arriba (medición) ---
    titulo = spec.get("gancho") if (formato == "portada" and spec.get("gancho")) else spec.get("titulo", "")
    ft, lt, _ = ajustar(d, titulo, M["tit"][0], M["tit"][1], w - 140, M["lineas"], lambda t: playfair(t, 500))
    logo_m = logo_mascara("texto", M["logo_w"])
    y = M["logo_y"] + logo_m.height + M["eti"] * 1.4
    bloques = []  # (tipo, alto)
    if spec.get("etiqueta"):
        fe = poppins(M["eti"], "Medium")
        bloques.append(("eti", fe, [spec["etiqueta"].upper()], alto_linea(fe, 1.2)))
    bloques.append(("tit", ft, lt, alto_linea(ft, 1.0)))
    if spec.get("marca"):
        fm = script(M["marca"])
        bloques.append(("marca", fm, [spec["marca"]], alto_linea(fm, 0.82)))
    if spec.get("subtitulo"):
        fs, ls, _ = ajustar(d, spec["subtitulo"].upper(), M["sub"], M["sub"] * 0.75, w - 200, 2,
                            lambda t: poppins(t, "Medium"), 0.12)
        bloques.append(("sub", fs, ls, alto_linea(fs, 1.25)))
    if spec.get("nota"):
        fn, ln, _ = ajustar(d, spec["nota"], M["nota"], M["nota"] * 0.75, w - 200, 2, lambda t: playfair(t, 400, True))
        bloques.append(("nota", fn, ln, alto_linea(fn, 1.15)))
    arriba = y + sum(al * len(ls) for _, _, ls, al in bloques) + (16 if spec.get("subtitulo") else 0)

    # --- bloque de abajo (medición) ---
    pie_y = h - M["pie_y"] - M["pie"] * 2.0 if M["pie_y"] else h
    abajo = pie_y - M["pie"] * 1.3
    if spec.get("cta") and formato != "portada":
        abajo -= alto_linea(poppins(M["cta"], "Medium")) + M["cta"] * 1.6
    abajo -= medir_precio(spec, M["pre"]) + M["pre"] * 0.3

    if formato == "portada":
        caja = (w * 0.12, arriba + 60, w * 0.88, h - 400)
    else:
        caja = (w * 0.1, arriba + h * 0.03, w * 0.9, abajo - h * 0.015)

    # --- producto ---
    acaja = poner_producto(img, caja, prod, recortado, tema, abajo=False)
    if spec.get("descuento"):
        r = w * 0.095
        sello(img, min(w - r - 40, acaja[2] - r * 0.2), acaja[1] + r * 1.3, spec["descuento"], r, tema)

    # --- textos de arriba ---
    d = ImageDraw.Draw(img)
    img.alpha_composite(capa_color(logo_m, T["titulo"]), (int(cx - logo_m.width / 2), M["logo_y"]))
    for tipo, f, ls, al in bloques:
        if tipo == "sub":
            y += 16
        for l in ls:
            if tipo == "eti":
                txt(d, cx, y, l, f, T["acento"], esp=M["eti"] * 0.22)
            elif tipo == "tit":
                txt(d, cx, y, l, f, T["titulo"])
            elif tipo == "marca":
                txt(d, cx, y - al * 0.12, l, f, T["acento"])
            elif tipo == "sub":
                txt(d, cx, y, l, f, T["sec"], esp=M["sub"] * 0.12)
            else:
                txt(d, cx, y, l, f, T["sec"])
            y += al

    # --- bloque de abajo ---
    if formato == "portada":
        if spec.get("precio"):
            precio(img, cx, h - 360, spec, M["pre"] * 0.8, tema)
        return img.convert("RGB")
    yb = precio(img, cx, abajo + M["pre"] * 0.3, spec, M["pre"], tema)
    if spec.get("cta"):
        boton(img, cx, yb + M["cta"] * 0.5, spec["cta"], M["cta"], tema)
    if M["pie_y"]:
        pie(img, pie_y, M["pie"], tema)
    return img.convert("RGB")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as fh:
        spec = json.load(fh)
    salida = sys.argv[2]
    base = os.path.dirname(os.path.abspath(sys.argv[1]))

    def resolver(s):
        if s.get("imagen") and not os.path.isabs(s["imagen"]):
            s["imagen"] = os.path.join(base, s["imagen"])
        return s

    if spec.get("formato") == "carrusel":
        os.makedirs(salida, exist_ok=True)
        comunes = {k: spec[k] for k in ("fondo",) if k in spec}
        for i, s in enumerate(spec.get("slides", []), 1):
            s = resolver({**comunes, **s})
            s.setdefault("formato", "post")
            ruta = os.path.join(salida, f"slide_{i:02d}.png")
            armar(s).save(ruta, "PNG")
            print(ruta)
        return
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    armar(resolver(spec)).save(salida, "PNG")
    print(salida)


if __name__ == "__main__":
    main()
