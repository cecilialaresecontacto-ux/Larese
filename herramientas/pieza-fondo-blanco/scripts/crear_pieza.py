#!/usr/bin/env python3
"""
Genera piezas visuales de LARESE STORE como PNG.

Estilo: fondo blanco, textos en Deep Blue (#09318D) y detalles en Ballerina (#EED2E2), producto recortado y grande
en el centro, copias desenfocadas del producto en las esquinas para dar profundidad,
el logo "larese" gigante y transparente detrás, texto blanco en Poppins
(títulos en mayúsculas y gruesos), botón tipo píldora y pie con íconos.

Uso:
    python crear_pieza.py spec.json salida.png
    python crear_pieza.py spec.json carpeta_salida/      # para carruseles

Spec (JSON). Solo "formato" y "titulo" son obligatorios:

{
  "formato": "post" | "cuadrado" | "historia" | "portada" | "carrusel",
  "etiqueta": "Decant original",          # línea chica arriba del título
  "titulo": "Good Girl Blush",            # grande, va en mayúsculas
  "subtitulo": "Carolina Herrera · 3, 5 y 10 ml",
  "precio": 40000,                        # número en guaraníes -> "Gs. 40.000"
  "precio_prefijo": "Desde",              # opcional
  "precio_anterior": 50000,               # opcional, se muestra tachado
  "descuento": "-20%",                    # opcional, sello blanco
  "imagen": "producto.png",               # foto del producto (ideal: fondo blanco o PNG recortado)
  "elementos": ["flor.png"],              # opcional: imágenes extra para las esquinas desenfocadas
  "color": "#D4848C",                     # opcional: fuerza el color de fondo
  "categoria": "perfume",                 # perfume | joya | maquillaje | cosmetico | electronica
  "cta": "¡Pedí el tuyo!",                # texto del botón
  "gancho": "...",                        # solo portada: frase grande en lugar del título
  "slides": [ {...}, {...} ]              # solo carrusel: un spec de post por slide
}

El pie (WhatsApp y envíos) se agrega solo. Si no hay "color", sale de la foto del producto;
si no hay foto, de la categoría.
"""
import colorsys
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(AQUI, "..", "assets")
FUENTES = os.path.join(ASSETS, "fonts")

WHATSAPP = "0972 736 002"
ENVIOS = "Envíos a todo Paraguay"
BLANCO = (255, 255, 255)
# Fondo SIEMPRE blanco. Paleta de la tienda: Deep Blue #09318D (textos, botón, íconos)
# y Ballerina #EED2E2 (detalles: etiqueta y sello). Blanco de la paleta: #FCFFFF (se usa blanco puro).
FONDO = (255, 255, 255)
TEXTO = (9, 49, 141)       # Deep Blue #09318D
GRIS = (84, 104, 160)      # Deep Blue suavizado, para textos secundarios
ACENTO = (9, 49, 141)      # Deep Blue
ROSA = (238, 210, 226)     # Ballerina #EED2E2

TAMANOS = {
    "post": (1080, 1350),
    "cuadrado": (1080, 1080),
    "historia": (1080, 1920),
    "portada": (1080, 1920),
}

COLOR_CATEGORIA = {
    "perfume": (206, 134, 144),     # rosa empolvado
    "joya": (168, 140, 118),        # champagne / taupe
    "maquillaje": (196, 136, 124),  # nude rosado
    "cosmetico": (150, 160, 140),   # verde salvia
    "electronica": (92, 106, 126),  # gris azulado
}
COLOR_DEFECTO = (190, 138, 146)


# ---------------- utilidades ----------------

def fuente(tam, peso=b"Bold"):
    """Poppins en el peso pedido (Medium, SemiBold, Bold o ExtraBold)."""
    nombre = peso.decode() if isinstance(peso, bytes) else peso
    if nombre not in ("Medium", "SemiBold", "Bold", "ExtraBold"):
        nombre = "Bold"
    return ImageFont.truetype(os.path.join(FUENTES, f"Poppins-{nombre}.ttf"), int(tam))


def guaranies(valor):
    if valor in (None, ""):
        return None
    if isinstance(valor, str):
        dig = "".join(c for c in valor if c.isdigit())
        if not dig:
            return valor
        valor = int(dig)
    return "Gs. " + f"{int(valor):,}".replace(",", ".")


def hex_a_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminancia(rgb):
    def c(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (c(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ajustar_color(rgb, dv=0.0, ds=0.0):
    h, s, v = colorsys.rgb_to_hsv(*(x / 255 for x in rgb))
    s = min(1, max(0, s + ds))
    v = min(1, max(0, v + dv))
    return tuple(int(x * 255) for x in colorsys.hsv_to_rgb(h, s, v))


def legible(rgb):
    """Oscurece el color hasta que el texto blanco se lea bien encima."""
    while (1.05 / (luminancia(rgb) + 0.05)) < 2.6:
        rgb = ajustar_color(rgb, dv=-0.03)
    return rgb


def ancho_txt(d, t, f, esp=0):
    return d.textlength(t, font=f) + esp * max(0, len(t) - 1) if t else 0


def txt(d, cx, y, t, f, color=TEXTO, esp=0):
    """Texto centrado en cx, con espaciado entre letras opcional."""
    w = ancho_txt(d, t, f, esp)
    x = cx - w / 2
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


def ajustar(d, t, tmax, tmin, maxw, maxl, peso, esp_rel=0.0):
    """Tamaño de letra más grande con el que el texto entra en maxl líneas."""
    tam = tmax
    while True:
        f = fuente(tam, peso)
        esp = tam * esp_rel
        ls = envolver(d, t, f, maxw, esp)
        if (len(ls) <= maxl and all(ancho_txt(d, l, f, esp) <= maxw for l in ls)) or tam <= tmin:
            return f, ls, esp
        tam -= 4


def alto_linea(f, k=1.0):
    a, b = f.getmetrics()
    return (a + b) * k


# ---------------- producto: recorte y color ----------------

def cargar_producto(ruta):
    """Devuelve (imagen RGBA, se_pudo_recortar). Recorta solo si el fondo es liso o ya es PNG transparente."""
    if not ruta or not os.path.exists(ruta):
        return None, False
    im = ImageOps.exif_transpose(Image.open(ruta)).convert("RGBA")
    a = np.array(im)
    if (a[..., 3] < 250).mean() > 0.02:              # ya viene con transparencia
        return im.crop(im.getbbox()), True
    rgb = a[..., :3].astype(int)
    borde = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
    if borde.std(axis=0).max() > 22:                  # fondo con detalles: no se recorta
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


def color_del_producto(prod):
    """Color de fondo a partir de los tonos del producto (promedio pesado por saturación)."""
    p = prod.copy()
    p.thumbnail((160, 160))
    a = np.array(p).reshape(-1, 4) / 255.0
    a = a[a[:, 3] > 0.8][:, :3]
    if len(a) < 50:
        return None
    hsv = np.array([colorsys.rgb_to_hsv(*px) for px in a])
    peso = hsv[:, 1] * hsv[:, 2]
    peso[(hsv[:, 2] < 0.15) | (hsv[:, 2] > 0.97)] = 0
    if peso.sum() < len(a) * 0.06:                    # producto casi sin color (negro, blanco, plata)
        return None
    ang = hsv[:, 0] * 2 * math.pi
    h = (math.atan2((np.sin(ang) * peso).sum(), (np.cos(ang) * peso).sum()) / (2 * math.pi)) % 1
    s = min(0.48, max(0.28, float((hsv[:, 1] * peso).sum() / peso.sum()) * 0.7))
    return tuple(int(x * 255) for x in colorsys.hsv_to_rgb(h, s, 0.74))


# ---------------- capas ----------------

def fondo(w, h, color):
    if color == FONDO:  # blanco puro, sin degradé
        return Image.new("RGBA", (w, h), FONDO + (255,))
    centro = ajustar_color(color, dv=0.07, ds=-0.06)
    borde = ajustar_color(color, dv=-0.07)
    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.sqrt(((xx - w / 2) / (w * 0.75)) ** 2 + ((yy - h * 0.5) / (h * 0.6)) ** 2)
    t = np.clip(dist, 0, 1)[..., None]
    arr = np.array(centro) * (1 - t) + np.array(borde) * t
    img = Image.fromarray(arr.astype("uint8"), "RGB")
    ruido = Image.effect_noise((w, h), 12).convert("RGB")
    return Image.blend(img, ruido, 0.02).convert("RGBA")


def capa_color(mascara, color, opacidad=1.0):
    capa = Image.new("RGBA", mascara.size, color + (0,))
    capa.putalpha(mascara.point(lambda v: int(v * opacidad)))
    return capa


def logo_mascara(nombre, ancho):
    m = Image.open(os.path.join(ASSETS, f"logo_{nombre}_mascara.png")).convert("L")
    return m.resize((int(ancho), int(m.height * ancho / m.width)), Image.LANCZOS)


def marca_de_agua(img, cy):
    """El logo 'larese' gigante, blanco y muy transparente, cortado por los bordes."""
    w, _ = img.size
    m = logo_mascara("texto", w * 1.75)
    img.alpha_composite(capa_color(m, TEXTO, 0.04), (int(-w * 0.2), int(cy - m.height / 2)))


def esquinas_desenfocadas(img, fuentes_img, zona_libre):
    """Copias grandes y desenfocadas en las esquinas (como las frambuesas del ejemplo)."""
    if not fuentes_img:
        return
    w, h = img.size
    lugares = [  # (x, y, ancho relativo, giro, desenfoque)
        (-0.10, 0.05, 0.32, 18, 10),
        (0.74, -0.03, 0.42, -22, 18),
        (-0.14, 0.70, 0.38, -14, 14),
        (0.80, 0.80, 0.30, 25, 9),
    ]
    x0, y0, x1, y1 = zona_libre
    for i, (rx, ry, rw, giro, blur) in enumerate(lugares):
        copia = fuentes_img[i % len(fuentes_img)].copy()
        ancho = w * rw
        copia.thumbnail((int(ancho), int(ancho * 1.6)), Image.LANCZOS)
        copia = copia.rotate(giro, expand=True, resample=Image.BICUBIC)
        copia = copia.filter(ImageFilter.GaussianBlur(blur))
        x, y = int(w * rx), int(h * ry)
        if x < x1 and x + copia.width > x0 and y < y1 and y + copia.height > y0:
            # si se cruza con el producto principal, más transparente
            copia.putalpha(copia.getchannel("A").point(lambda v: int(v * 0.55)))
        img.alpha_composite(copia, (x, y))


def pegar_producto(img, prod, recortado, caja):
    """Pone el producto lo más grande posible dentro de caja, con sombra suave."""
    x0, y0, x1, y1 = (int(v) for v in caja)
    bw, bh = x1 - x0, y1 - y0
    if recortado:
        esc = min(bw / prod.width, bh / prod.height)
        p = prod.resize((max(1, int(prod.width * esc)), max(1, int(prod.height * esc))), Image.LANCZOS)
    else:
        # foto con fondo: va como tarjeta redondeada
        p = ImageOps.fit(prod.convert("RGB"), (int(bw * 0.78), int(bh * 0.94)), Image.LANCZOS).convert("RGBA")
        m = Image.new("L", p.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, p.width, p.height), radius=48, fill=255)
        p.putalpha(m)
    px = int(x0 + (bw - p.width) / 2)
    py = int(y0 + (bh - p.height) / 2)
    sombra = Image.new("L", img.size, 0)
    sd = ImageDraw.Draw(sombra)
    if recortado:
        sw = p.width * 0.75
        sd.ellipse((px + (p.width - sw) / 2, py + p.height - 26, px + (p.width + sw) / 2, py + p.height + 26), fill=150)
        sombra = sombra.filter(ImageFilter.GaussianBlur(22))
    else:
        sd.rounded_rectangle((px + 10, py + 24, px + p.width - 10, py + p.height + 24), radius=48, fill=110)
        sombra = sombra.filter(ImageFilter.GaussianBlur(30))
    img.alpha_composite(capa_color(sombra, (0, 0, 0), 0.55))
    img.alpha_composite(p, (px, py))
    return (px, py, px + p.width, py + p.height)


def monograma_grande(img, caja):
    """Sin foto: el monograma 'la' grande y translúcido en el lugar del producto."""
    x0, y0, x1, y1 = caja
    ancho = min(x1 - x0, (y1 - y0) * 1.07) * 0.62
    m = logo_mascara("monograma", ancho)
    img.alpha_composite(capa_color(m, TEXTO, 0.10),
                        (int((x0 + x1 - m.width) / 2), int((y0 + y1 - m.height) / 2)))


def sello(img, cx, cy, texto, r, color_texto):
    sombra = Image.new("L", img.size, 0)
    ImageDraw.Draw(sombra).ellipse((cx - r, cy - r + 8, cx + r, cy + r + 8), fill=120)
    img.alpha_composite(capa_color(sombra.filter(ImageFilter.GaussianBlur(14)), (0, 0, 0), 0.5))
    d = ImageDraw.Draw(img)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ROSA)
    f, ls, _ = ajustar(d, texto, int(r * 0.62), 20, r * 1.55, 2, b"ExtraBold")
    y = cy - alto_linea(f) * len(ls) / 2 - r * 0.04
    for l in ls:
        txt(d, cx, y, l, f, color_texto)
        y += alto_linea(f)


def boton(img, cx, y, texto, tam, color_fondo):
    f = fuente(tam, b"SemiBold")
    d = ImageDraw.Draw(img)
    w = d.textlength(texto, font=f)
    h = alto_linea(f)
    px, py = tam * 1.1, tam * 0.45
    caja = (cx - w / 2 - px, y, cx + w / 2 + px, y + h + 2 * py)
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(capa).rounded_rectangle(caja, radius=(h + 2 * py) / 2, fill=color_fondo + (255,))
    img.alpha_composite(capa)
    txt(ImageDraw.Draw(img), cx, y + py - tam * 0.05, texto, f, BLANCO)
    return caja[3]


def icono_chat(d, cx, cy, r):
    d.ellipse((cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.58), outline=BLANCO, width=max(2, int(r * 0.13)))
    d.polygon([(cx - r * 0.52, cy + r * 0.30), (cx - r * 0.74, cy + r * 0.74), (cx - r * 0.16, cy + r * 0.52)], fill=BLANCO)
    for dx in (-0.25, 0, 0.25):
        d.ellipse((cx + r * dx - r * 0.07, cy - r * 0.07, cx + r * dx + r * 0.07, cy + r * 0.07), fill=BLANCO)


def icono_camion(d, cx, cy, r):
    s = r * 0.95
    d.rectangle((cx - s * 0.64, cy - s * 0.34, cx + s * 0.10, cy + s * 0.20), fill=BLANCO)
    d.polygon([(cx + s * 0.15, cy - s * 0.14), (cx + s * 0.42, cy - s * 0.14), (cx + s * 0.62, cy + s * 0.04),
               (cx + s * 0.62, cy + s * 0.20), (cx + s * 0.15, cy + s * 0.20)], fill=BLANCO)
    for wx in (cx - s * 0.38, cx + s * 0.38):
        d.ellipse((wx - s * 0.15, cy + s * 0.12, wx + s * 0.15, cy + s * 0.42), fill=BLANCO)


def pie(img, y, tam, color_circulo):
    w = img.size[0]
    d = ImageDraw.Draw(img)
    f = fuente(tam, b"Medium")
    r = tam * 1.05
    items = [("chat", WHATSAPP), ("camion", ENVIOS)]
    sep = tam * 2.0
    anchos = [2 * r + tam * 0.6 + d.textlength(t, font=f) for _, t in items]
    x = w / 2 - (sum(anchos) + sep) / 2
    cy = y + r
    for (ic, t), aw in zip(items, anchos):
        d.ellipse((x, cy - r, x + 2 * r, cy + r), fill=color_circulo)
        (icono_chat if ic == "chat" else icono_camion)(d, x + r, cy, r * 0.82)
        d.text((x + 2 * r + tam * 0.6, cy - alto_linea(f) / 2 - tam * 0.05), t, font=f, fill=TEXTO)
        x += aw + sep


def precio(img, cx, y, spec, tam):
    d = ImageDraw.Draw(img)
    actual = guaranies(spec.get("precio"))
    if actual and spec.get("precio_prefijo"):
        actual = f'{spec["precio_prefijo"]} {actual}'
    anterior = guaranies(spec.get("precio_anterior"))
    if anterior:
        f2 = fuente(tam * 0.46, b"Medium")
        w2 = d.textlength(anterior, font=f2)
        claro = GRIS + (255,)
        d.text((cx - w2 / 2, y), anterior, font=f2, fill=claro)
        a, _ = f2.getmetrics()
        d.line((cx - w2 / 2 - 4, y + a * 0.62, cx + w2 / 2 + 4, y + a * 0.62), fill=claro, width=3)
        y += alto_linea(f2, 1.05)
    if actual:
        f = fuente(tam, b"Bold")
        txt(ImageDraw.Draw(img), cx, y, actual, f)
        y += alto_linea(f, 1.05)
    return y


def alto_precio(spec, tam):
    al = 0
    if spec.get("precio_anterior"):
        al += alto_linea(fuente(tam * 0.46, b"Medium"), 1.05)
    if spec.get("precio"):
        al += alto_linea(fuente(tam, b"Bold"), 1.05)
    return al


# ---------------- armado ----------------

MEDIDAS = {
    # pie_y = espacio libre bajo el pie (zona tapada por la app); 0 = sin pie
    "post":     dict(logo_w=210, logo_y=56, eti=30, tit=(104, 60), sub=28, pre=70, cta=32, pie=24, pie_y=60, lineas=2),
    "cuadrado": dict(logo_w=190, logo_y=48, eti=26, tit=(88, 52), sub=24, pre=60, cta=28, pie=22, pie_y=50, lineas=2),
    "historia": dict(logo_w=250, logo_y=170, eti=34, tit=(116, 70), sub=32, pre=88, cta=40, pie=30, pie_y=190, lineas=2),
    "portada":  dict(logo_w=250, logo_y=300, eti=40, tit=(120, 70), sub=34, pre=84, cta=40, pie=30, pie_y=0, lineas=4),
}


def armar(spec):
    formato = spec.get("formato", "post")
    if formato not in TAMANOS:
        raise SystemExit(f"Formato desconocido: {formato}. Usá: {', '.join(list(TAMANOS) + ['carrusel'])}")
    w, h = TAMANOS[formato]
    M = MEDIDAS[formato]

    prod, recortado = cargar_producto(spec.get("imagen"))
    if spec.get("color"):
        color = hex_a_rgb(spec["color"])
    else:
        color = (color_del_producto(prod) if (prod is not None and recortado) else None) \
            or COLOR_CATEGORIA.get(spec.get("categoria", ""), COLOR_DEFECTO)
    # fondo SIEMPRE blanco (se ignora el color de la foto o de la categoría)
    oscuro = ACENTO

    img = fondo(w, h, FONDO)
    d = ImageDraw.Draw(img)
    cx = w / 2

    # --- bloque de arriba (medición) ---
    titulo = spec.get("gancho") if (formato == "portada" and spec.get("gancho")) else spec.get("titulo", "")
    ft, lt, esp_t = ajustar(d, titulo.upper(), M["tit"][0], M["tit"][1], w - 130, M["lineas"], b"Bold", 0.0)
    logo_m = logo_mascara("texto", M["logo_w"])
    y_texto = M["logo_y"] + logo_m.height + M["eti"] * 1.3
    arriba = y_texto
    if spec.get("etiqueta"):
        arriba += alto_linea(fuente(M["eti"], b"SemiBold"), 1.05) + M["eti"] * 0.35
    arriba += alto_linea(ft, 0.86) * len(lt)
    fs, ls = None, []
    if spec.get("subtitulo"):
        fs, ls, _ = ajustar(d, spec["subtitulo"].upper(), M["sub"], M["sub"] * 0.7, w - 180, 2, b"Medium", 0.04)
        arriba += alto_linea(fs, 1.15) * len(ls) + 6

    # --- bloque de abajo (medición) ---
    pie_y = h - M["pie_y"] - M["pie"] * 2.1 if M["pie_y"] else h
    abajo = pie_y - M["pie"] * 1.2
    if spec.get("cta") and formato != "portada":
        abajo -= alto_linea(fuente(M["cta"], b"SemiBold")) + M["cta"] * 1.4
    abajo -= alto_precio(spec, M["pre"]) + M["pre"] * 0.25

    margen_x = w * (0.09 if formato in ("historia", "portada") else 0.13)
    if formato == "portada":
        caja = (margen_x, arriba + 40, w - margen_x, h - 380)
    else:
        caja = (margen_x, arriba + h * 0.015, w - margen_x, abajo - h * 0.01)

    # --- fondo: marca de agua y esquinas ---
    if prod is not None:  # sin foto, el monograma ocupa ese lugar y no se mezclan
        marca_de_agua(img, (caja[1] + caja[3]) / 2)
    esquinas = []
    for ruta in spec.get("elementos") or []:
        e, ok = cargar_producto(ruta)
        if e is not None and ok:
            esquinas.append(e)
    # con fondo blanco no se usan copias desenfocadas del producto (ensucian el blanco)
    esquinas_desenfocadas(img, esquinas, caja)

    # --- producto ---
    if prod is not None:
        pcaja = pegar_producto(img, prod, recortado, caja)
    else:
        monograma_grande(img, caja)
        ancho_c = caja[2] - caja[0]
        pcaja = (caja[0] + ancho_c * 0.2, caja[1], caja[2] - ancho_c * 0.2, caja[3])
    if spec.get("descuento"):
        r = w * (0.105 if formato in ("historia", "portada") else 0.095)
        sx = min(w - r - 44, pcaja[2] + r * 0.5)
        sello(img, sx, pcaja[1] + r * 1.15, spec["descuento"], r, TEXTO)

    # --- textos de arriba ---
    d = ImageDraw.Draw(img)
    img.alpha_composite(capa_color(logo_m, TEXTO), (int(cx - logo_m.width / 2), M["logo_y"]))
    y = y_texto
    if spec.get("etiqueta"):
        fe = fuente(M["eti"], b"SemiBold")
        et = spec["etiqueta"].upper()
        esp_e = M["eti"] * 0.06
        we = ancho_txt(d, et, fe, esp_e)
        bb = fe.getbbox(et)
        px, py = M["eti"] * 0.9, M["eti"] * 0.38
        d.rounded_rectangle((cx - we / 2 - px, y + bb[1] - py, cx + we / 2 + px, y + bb[3] + py),
                            radius=(bb[3] - bb[1]) / 2 + py, fill=ROSA)
        txt(d, cx, y, et, fe, TEXTO, esp=esp_e)
        y += alto_linea(fe, 1.05) + M["eti"] * 0.35
    for l in lt:
        txt(d, cx, y, l, ft, TEXTO, esp=esp_t)
        y += alto_linea(ft, 0.86)
    if ls:
        y += 6
        for l in ls:
            txt(d, cx, y, l, fs, GRIS, esp=M["sub"] * 0.04)
            y += alto_linea(fs, 1.15)

    # --- bloque de abajo ---
    if formato == "portada":
        if spec.get("precio"):
            precio(img, cx, h - 360, spec, M["pre"] * 0.8)
        return img.convert("RGB")
    yb = precio(img, cx, abajo + M["pre"] * 0.25, spec, M["pre"])
    if spec.get("cta"):
        boton(img, cx, yb + M["cta"] * 0.45, spec["cta"], M["cta"], oscuro)
    if M["pie_y"]:
        pie(img, pie_y, M["pie"], oscuro)
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
        if s.get("elementos"):
            s["elementos"] = [e if os.path.isabs(e) else os.path.join(base, e) for e in s["elementos"]]
        return s

    if spec.get("formato") == "carrusel":
        os.makedirs(salida, exist_ok=True)
        # el color se comparte entre slides para que el carrusel se vea parejo
        comunes = {k: spec[k] for k in ("color", "categoria", "elementos") if k in spec}
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
