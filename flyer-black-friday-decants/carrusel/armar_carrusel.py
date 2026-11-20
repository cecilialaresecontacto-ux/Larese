#!/usr/bin/env python3
"""Carrusel Black Friday de decants (19 al 30 de noviembre), en fondo blanco (lo pidió la dueña).

Slide 1: portada con los decants y los dos precios.
Slides 2 a 18: los 17 perfumes disponibles, uno por slide, con el frasco original y al lado
sus decants de 5 y 10 ml (foto real del frasquito, con el color de ese perfume) y el precio.
Slide 19: cierre con el WhatsApp. (Instagram acepta hasta 20 slides.)
También guarda cada slide en formato historia (1080x1920) en carrusel/historias/.

Estilo editorial de herramientas/carrusel-bordo (Playfair, Pinyon Script, Poppins) en su versión
"fondo blanco y letra vino": títulos y precios en bordó vino, marcas en cursiva dorada.

Uso: python3 flyer-black-friday-decants/carrusel/armar_carrusel.py
"""
import os
import sys

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..", "..")
sys.path.insert(0, os.path.join(RAIZ, "herramientas", "carrusel-bordo", "scripts"))
sys.path.insert(0, os.path.join(AQUI, "..", "fuente"))
import crear_carrusel as cc  # noqa: E402
from decants_vino import frasco  # noqa: E402

W, H = cc.W, cc.H
FOTOS = os.path.join(AQUI, "fotos")
SALIDA = AQUI

FECHAS = "19 al 30 de noviembre"
PRECIOS = [("5 ml", 45000, 5), ("10 ml", 90000, 10)]
# perfumes con otro precio en la promo (lo confirmó la dueña): nombre -> (5 ml, 10 ml)
PRECIOS_ESPECIALES = {"Light Blue": (25000, 50000), "Bright Crystal": (25000, 50000)}

# Los 17 perfumes disponibles para el Black Friday (lista de la dueña, 18 de noviembre).
# nombre, marca, tipo, notas, foto, color del perfume en el decant
FRAGANCIAS = [
    ("Miss Dior", "Dior", "Eau de Parfum",
     "El floral más romántico de Dior, en su nueva versión.", "miss-dior-x4.png", (240, 175, 182)),
    ("J'adore", "Dior", "Eau de Parfum",
     "Un bouquet luminoso de jazmín y nardos. Clásico y sofisticado.", "s-jadore.jpg", (232, 190, 110)),
    ("Addict Rosy Glow", "Dior", "Eau de Parfum",
     "Lichi, rosa y un fondo cremoso de vainilla.", "p-rosy-glow-x4.png", (240, 160, 186)),
    ("Addict Peachy Glow", "Dior", "Eau de Parfum",
     "Durazno jugoso y jazmín sobre vainilla y crema batida.", "p-peachy-glow-x4.png", (245, 178, 145)),
    ("Addict Purple Glow", "Dior", "Eau de Parfum",
     "Flores confitadas, frambuesa e iris sobre un fondo de vainilla.", "p-purple-glow-x4.png", (205, 165, 222)),
    ("Coco Mademoiselle Intense", "Chanel", "Eau de Parfum Intense",
     "La versión más profunda y sensual del clásico de Chanel.", "p-coco-mademoiselle-x4.png", (226, 160, 98)),
    ("Libre", "Yves Saint Laurent", "Eau de Parfum",
     "Lavanda francesa y azahar sobre un fondo de vainilla.", "10-libre-x4.png", (238, 200, 140)),
    ("Devotion Intense", "Dolce & Gabbana", "Eau de Parfum",
     "Avellana tostada y flores luminosas: cálido y envolvente.", "r-devotion2.png", (238, 150, 96)),
    ("Light Blue", "Dolce & Gabbana", "Eau de Toilette",
     "Limón siciliano y manzana, fresco como un verano en el Mediterráneo.", "s-light-blue.jpg", (214, 230, 242)),
    ("Born in Roma", "Valentino", "Eau de Parfum",
     "Jazmín y vainilla con un fondo amaderado, elegante y moderno.", "born-in-roma-donna-x4.png", (240, 178, 180)),
    ("Divine Couture", "Jean Paul Gaultier", "Eau de Parfum",
     "Notas marinas, flores blancas y un toque dulce de merengue.", "r-divine.webp", (238, 150, 130)),
    ("Scandal Le Parfum", "Jean Paul Gaultier", "Le Parfum",
     "Jazmín radiante y caramelo salado: intenso y adictivo.", "p-scandal-le-parfum-x4.png", (214, 118, 72)),
    ("L'Interdit", "Givenchy", "Eau de Toilette",
     "Flores blancas con un toque cítrico chispeante. Luminoso y vibrante.", "p-linterdit-x4.png", (244, 196, 166)),
    ("Sì Passione", "Armani", "Eau de Parfum",
     "Grosella negra, pera, rosa y jazmín sobre una vainilla intensa.", "p-si-passione-x4.png", (224, 108, 128)),
    ("Bright Crystal", "Versace", "Eau de Toilette",
     "Yuzu y granada sobre un acorde helado, floral y luminoso.", "p-bright-crystal-x4.png", (242, 182, 194)),
    ("Erba Pura", "Xerjoff", "Eau de Parfum · Nicho",
     "Cítricos sicilianos y frutas mediterráneas sobre almizcle blanco.", "s-erba-pura.jpg", (240, 214, 150)),
    ("Naxos", "Xerjoff", "Eau de Parfum · Nicho",
     "Cítricos y lavanda que se vuelven miel especiada con canela.", "p-naxos-x4.png", (210, 150, 80)),
]
# en la portada, 6 decants de colores bien distintos
PORTADA = ["Miss Dior", "Libre", "Addict Purple Glow", "Coco Mademoiselle Intense", "Sì Passione", "Light Blue"]

BLANCO = (255, 255, 255)
PRINCIPAL = cc.BORDO     # títulos, nombres y precios
SUAVE = cc.DORADO        # marcas, líneas finas y etiquetas
TEXTO = cc.TINTA         # notas
CHICO = cc.MALVA         # pie y textos chicos


def lienzo(alto=None):
    return Image.new("RGBA", (W, alto or H), BLANCO + (255,))


def recorte_fino(ruta, umbral):
    """Recorta el fondo blanco con un umbral bajo, para frascos de vidrio casi blanco."""
    import numpy as np
    from PIL import ImageFilter
    im = Image.open(ruta).convert("RGB")
    b = im.copy()
    w, h = b.size
    marca = (1, 254, 3)
    for p in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]:
        if b.getpixel(p) != marca:
            ImageDraw.floodfill(b, p, marca, thresh=umbral)
    fuera = np.all(np.array(b) == marca, axis=-1)
    a = Image.fromarray(np.where(fuera, 0, 255).astype("uint8"))
    a = a.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.5))
    out = im.convert("RGBA")
    out.putalpha(a)
    return out.crop(a.getbbox())


def foto(ruta):
    """Recorte del frasco original (algunas fotos traen la caja: se recortan igual)."""
    if not os.path.exists(ruta):  # sin la versión agrandada, la original
        base, _ = os.path.splitext(ruta.replace("-x4", ""))
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            if os.path.exists(base + ext):
                ruta = base + ext
                break
    if os.path.basename(ruta).startswith("tarjeta-"):
        # foto con fondo oscuro que no se puede recortar: va como tarjeta
        return Image.open(ruta).convert("RGBA"), False
    if "jadore" in os.path.basename(ruta):
        # la caja de J'adore es blanca sobre blanco y no se recorta bien: solo el frasco
        im = Image.open(ruta).convert("RGB")
        recorte = os.path.join(FOTOS, "jadore-frasco.png")
        im.crop((int(im.width * 0.56), 0, im.width, im.height)).save(recorte)
        ruta = recorte
    if os.path.basename(ruta).startswith("10-libre"):
        # el vidrio de Libre es casi blanco: con el recorte común se come la base
        return recorte_fino(ruta, umbral=6), True
    return cc.cargar_producto(ruta)


def pegar(img, p, cx, base, alto_max, ancho_max):
    esc = min(alto_max / p.height, ancho_max / p.width)
    q = p.resize((max(1, int(p.width * esc)), max(1, int(p.height * esc))), Image.LANCZOS)
    cc.pegar_producto(img, q, (cx - q.width / 2, base - q.height, cx + q.width / 2, base), sombra_color=(90, 60, 60))
    return q.width, q.height


def cinta_fechas(img, y, ancho_linea=70):
    """BLACK FRIDAY · 19 AL 30 DE NOVIEMBRE, con dos líneas finas a los costados."""
    d = ImageDraw.Draw(img)
    f = cc.sans(20, "SemiBold")
    t = f"BLACK FRIDAY  ·  {FECHAS.upper()}"
    w = cc.ancho(d, t, f, 4)
    cc.escribir(d, W / 2, y, t, f, SUAVE, esp=4, ancla="ma")
    cy = y + 15
    d.line((W / 2 - w / 2 - 24 - ancho_linea, cy, W / 2 - w / 2 - 24, cy), fill=SUAVE, width=1)
    d.line((W / 2 + w / 2 + 24, cy, W / 2 + w / 2 + 24 + ancho_linea, cy), fill=SUAVE, width=1)


def slide_fragancia(n, nombre, marca, tipo, notas, archivo, color):
    img = lienzo()
    d = ImageDraw.Draw(img)
    cc.logo(img, W / 2, 70, 118, cc.BORDO)
    cinta_fechas(img, 128)

    # Nombre centrado (sin número) y la marca en cursiva debajo
    tam = 96
    while tam > 60 and cc.ancho(d, nombre, cc.serif(tam, 450)) > W - 220:
        tam -= 4
    f_tit = cc.serif(tam, 450)
    cc.escribir(d, W / 2, 205, nombre, f_tit, PRINCIPAL, ancla="ma")
    cc.escribir(d, W / 2, 205 + tam * 1.2, marca, cc.cursiva(66), SUAVE, ancla="ma")

    # producto a la izquierda, decants de 5 y 10 ml a la derecha
    base = 960
    prod, ok = foto(os.path.join(FOTOS, archivo))
    if ok:
        pegar(img, prod, 330, base, 470, 400)
    else:
        cc.tarjeta_foto(img, prod, (130, base - 470, 530, base), SUAVE)
    d = ImageDraw.Draw(img)
    d.line((W / 2 + 40, base - 380, W / 2 + 40, base + 90), fill=SUAVE, width=1)

    f_ml = cc.sans(19, "SemiBold")
    f_pr = cc.serif(31, 500)
    especial = PRECIOS_ESPECIALES.get(nombre)
    precios = [(ml, especial[i] if especial else p, cap) for i, (ml, p, cap) in enumerate(PRECIOS)]
    for cx, (ml, precio, cap) in zip((690, 900), precios):
        dec = frasco(color, cap, claro=True)
        pegar(img, dec, cx, base, 430 * dec.height / frasco(color, 10, claro=True).height, 200)
        d = ImageDraw.Draw(img)
        cc.escribir(d, cx, base + 22, ml.upper(), f_ml, SUAVE, esp=4, ancla="ma")
        cc.escribir(d, cx, base + 50, cc.guaranies(precio), f_pr, PRINCIPAL, ancla="ma")

    # tipo y notas
    cc.escribir(d, 330, base + 22, f"{tipo.upper()}", f_ml, SUAVE, esp=4, ancla="ma")
    f_notas = cc.serif_it(30, 400)
    y = 1128
    for l in cc.equilibrar(d, notas, f_notas, 780):
        cc.escribir(d, W / 2, y, l, f_notas, TEXTO, ancla="ma")
        y += 40
    cc.pie(img, 1262, CHICO)
    return img


def slide_fragancia_historia(nombre, marca, tipo, notas, archivo, color):
    """Lo mismo que slide_fragancia, pero armado para historia (1080x1920): logo, fechas,
    nombre, frasco y decants más grandes, botón y pie dentro de la zona segura."""
    HH = 1920
    img = lienzo(HH)
    d = ImageDraw.Draw(img)
    cc.logo(img, W / 2, 175, 190, cc.BORDO)
    cinta_fechas(img, 270)

    tam = 112
    while tam > 64 and cc.ancho(d, nombre, cc.serif(tam, 450)) > W - 160:
        tam -= 4
    f_tit = cc.serif(tam, 450)
    cc.escribir(d, W / 2, 345, nombre, f_tit, PRINCIPAL, ancla="ma")
    cc.escribir(d, W / 2, 345 + tam * 1.2, marca, cc.cursiva(76), SUAVE, ancla="ma")

    base = 1240
    prod, ok = foto(os.path.join(FOTOS, archivo))
    if ok:
        pegar(img, prod, 300, base, 600, 470)
    else:
        cc.tarjeta_foto(img, prod, (70, base - 600, 530, base), SUAVE)
    d = ImageDraw.Draw(img)
    d.line((W / 2 + 40, base - 480, W / 2 + 40, base + 120), fill=SUAVE, width=1)

    f_ml = cc.sans(24, "SemiBold")
    f_pr = cc.serif(40, 500)
    especial = PRECIOS_ESPECIALES.get(nombre)
    precios = [(ml, especial[i] if especial else p, cap) for i, (ml, p, cap) in enumerate(PRECIOS)]
    for cx, (ml, precio, cap) in zip((700, 925), precios):
        dec = frasco(color, cap, claro=True)
        pegar(img, dec, cx, base, 540 * dec.height / frasco(color, 10, claro=True).height, 230)
        d = ImageDraw.Draw(img)
        cc.escribir(d, cx, base + 28, ml.upper(), f_ml, SUAVE, esp=5, ancla="ma")
        cc.escribir(d, cx, base + 64, cc.guaranies(precio), f_pr, PRINCIPAL, ancla="ma")
    cc.escribir(d, 300, base + 28, tipo.upper(), f_ml, SUAVE, esp=5, ancla="ma")

    f_notas = cc.serif_it(36, 400)
    y = 1420
    for l in cc.equilibrar(d, notas, f_notas, 860):
        cc.escribir(d, W / 2, y, l, f_notas, TEXTO, ancla="ma")
        y += 48

    # botón
    f_b = cc.sans(34, "SemiBold")
    tb = "¡Pedí el tuyo!"
    tw = cc.ancho(d, tb, f_b)
    cy = max(1560, y + 88)  # con notas de dos renglones, el botón baja un poco
    d.rounded_rectangle((W / 2 - tw / 2 - 52, cy - 42, W / 2 + tw / 2 + 52, cy + 42), radius=42, fill=cc.BORDO)
    bb = f_b.getbbox(tb)
    d.text((W / 2 - tw / 2, cy - (bb[1] + bb[3]) / 2), tb, font=f_b, fill=cc.CREMA)
    cc.pie(img, cy + 100, CHICO)
    return img


def slide_portada():
    img = lienzo()
    d = ImageDraw.Draw(img)
    cc.logo(img, W / 2, 84, 230, cc.BORDO)

    cc.escribir(d, W / 2, 196, "Todos los decants", cc.cursiva(76), SUAVE, ancla="ma")
    cc.escribir(d, W / 2, 268, "Black Friday", cc.serif(128, 450), PRINCIPAL, ancla="ma")
    f_f = cc.sans(24, "SemiBold")
    t = FECHAS.upper()
    w = cc.ancho(d, t, f_f, 6)
    cc.escribir(d, W / 2, 442, t, f_f, SUAVE, esp=6, ancla="ma")
    cy = 458
    d.line((W / 2 - w / 2 - 110, cy, W / 2 - w / 2 - 26, cy), fill=SUAVE, width=1)
    d.line((W / 2 + w / 2 + 26, cy, W / 2 + w / 2 + 110, cy), fill=SUAVE, width=1)

    # fila de decants, uno por fragancia, alternando 10 y 5 ml
    base = 930
    paso = 128
    elegidas = [fr for nombre in PORTADA for fr in FRAGANCIAS if fr[0] == nombre]
    for i, fr in enumerate(elegidas):
        cap = 10 if i % 2 == 0 else 5
        dec = frasco(fr[5], cap, claro=True)
        alto = 400 * dec.height / frasco(fr[5], 10, claro=True).height
        pegar(img, dec, W / 2 + (i - 2.5) * paso, base, alto, 140)
    d = ImageDraw.Draw(img)

    # precios
    f_ml = cc.sans(22, "SemiBold")
    f_pr = cc.serif(60, 500)
    y = 990
    for k, (ml, precio, _) in enumerate(PRECIOS):
        cx = W / 2 + (k - 0.5) * 380
        cc.escribir(d, cx, y, ml.upper(), f_ml, SUAVE, esp=5, ancla="ma")
        cc.escribir(d, cx, y + 36, cc.guaranies(precio), f_pr, PRINCIPAL, ancla="ma")
    d.line((W / 2, y + 6, W / 2, y + 110), fill=SUAVE, width=1)

    f_pie = cc.sans(21, "SemiBold")
    tp = "DESLIZÁ Y ELEGÍ EL TUYO"
    wp = cc.ancho(d, tp, f_pie, 4)
    cc.escribir(d, W / 2 - 30, 1172, tp, f_pie, SUAVE, esp=4, ancla="ma")
    xa, ya = W / 2 - 30 + wp / 2 + 22, 1187
    d.line((xa, ya, xa + 44, ya), fill=SUAVE, width=2)
    d.line((xa + 34, ya - 8, xa + 44, ya), fill=SUAVE, width=2)
    d.line((xa + 34, ya + 8, xa + 44, ya), fill=SUAVE, width=2)
    cc.pie(img, 1262, CHICO)
    return img


def slide_cierre():
    img = lienzo()
    d = ImageDraw.Draw(img)
    cc.logo(img, W / 2, 110, 300, cc.BORDO)
    y = 330
    cc.escribir(d, W / 2, y, "Del 19 al 30", cc.serif(92, 450), PRINCIPAL, ancla="ma")
    cc.escribir(d, W / 2, y + 114, "de noviembre", cc.cursiva(78), SUAVE, ancla="ma")
    y += 264
    d.line((W / 2 - 60, y, W / 2 + 60, y), fill=SUAVE, width=2)
    y += 44
    cc.escribir(d, W / 2, y, "Todos los decants", cc.sans(30), TEXTO, ancla="ma")
    y += 80
    f_ml, f_pr = cc.sans(22, "SemiBold"), cc.serif(60, 500)
    for k, (ml, precio, _) in enumerate(PRECIOS):
        cx = W / 2 + (k - 0.5) * 380
        cc.escribir(d, cx, y, ml.upper(), f_ml, CHICO, esp=5, ancla="ma")
        cc.escribir(d, cx, y + 36, cc.guaranies(precio), f_pr, PRINCIPAL, ancla="ma")
    d.line((W / 2, y + 6, W / 2, y + 110), fill=SUAVE, width=1)
    y += 170
    # los perfumes con otro precio, agrupados por precio ("Light Blue y Bright Crystal: ...")
    grupos = {}
    for nombre, precios in PRECIOS_ESPECIALES.items():
        grupos.setdefault(precios, []).append(nombre)
    for (p5, p10), nombres in grupos.items():
        quienes = " y ".join([", ".join(nombres[:-1]), nombres[-1]]) if len(nombres) > 1 else nombres[0]
        cc.escribir(d, W / 2, y - 18, f"{quienes}:", cc.sans(26, "Medium"), PRINCIPAL, ancla="ma")
        cc.escribir(d, W / 2, y + 20, f"5 ml {cc.guaranies(p5)} · 10 ml {cc.guaranies(p10)}",
                    cc.sans(26, "Medium"), PRINCIPAL, ancla="ma")
        y += 92
    cc.escribir(d, W / 2, y, "Envíos a todo Paraguay", cc.serif_it(34, 420), CHICO, ancla="ma")

    f_b = cc.sans(32, "SemiBold")
    tb = "WhatsApp 0972 736 002"
    tw = cc.ancho(d, tb, f_b)
    cy = 1120
    d.rounded_rectangle((W / 2 - tw / 2 - 48, cy - 42, W / 2 + tw / 2 + 48, cy + 42), radius=42, fill=cc.BORDO)
    bb = f_b.getbbox(tb)
    d.text((W / 2 - tw / 2, cy - (bb[1] + bb[3]) / 2), tb, font=f_b, fill=cc.CREMA)
    cc.escribir(d, W / 2, cy + 78, "o en el link de la bio", cc.serif_it(30), CHICO, ancla="ma")
    return img


def main():
    slides = [slide_portada()]
    slides += [slide_fragancia(i, *fr) for i, fr in enumerate(FRAGANCIAS, 1)]
    slides.append(slide_cierre())
    # versión historia (1080x1920) en carrusel/historias/: los perfumes con su propio diseño;
    # portada y cierre, el mismo slide centrado (Instagram tapa ~250 px arriba y abajo)
    carpeta_hist = os.path.join(SALIDA, "historias")
    os.makedirs(carpeta_hist, exist_ok=True)
    nombres = ["portada"] + [slug(fr[0]) for fr in FRAGANCIAS] + ["cierre"]
    for i, (s, nombre) in enumerate(zip(slides, nombres), 1):
        ruta = os.path.join(SALIDA, f"{i:02d}.png")
        s.convert("RGB").save(ruta, optimize=True)
        print(ruta)
        if 1 < i < len(slides):  # perfumes: diseño propio de historia
            hist = slide_fragancia_historia(*FRAGANCIAS[i - 2]).convert("RGB")
        else:  # portada y cierre: el mismo slide centrado
            hist = Image.new("RGB", (1080, 1920), BLANCO)
            hist.paste(s.convert("RGB"), (0, (1920 - H) // 2))
        ruta_h = os.path.join(carpeta_hist, f"{i:02d}-{nombre}.png")
        hist.save(ruta_h, optimize=True)
        print(ruta_h)


def slug(nombre):
    import unicodedata
    t = unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode().lower()
    return "".join(c if c.isalnum() else "-" for c in t).strip("-").replace("--", "-")


if __name__ == "__main__":
    main()
