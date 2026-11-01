"""Carrusel navideño 'Perfumes para regalar' con precio contado y en 2 cuotas."""
import os, json, sys
from PIL import Image, ImageDraw
import navidad as N

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = "/home/user/Larese/carrusel-navidad-regalos"

# Precios de Shopify (botellas enteras). Agregar acá los que falten.
PERFUMES = [
    {"id": "paradoxe", "marca": "PRADA", "nombre": "Paradoxe", "detalle": "Eau de Parfum  ·  100 ml",
     "contado": 820000, "cuota": 451000, "caja": (760, 560)},
    {"id": "missdior", "marca": "DIOR", "nombre": "Miss Dior", "detalle": "Eau de Parfum  ·  100 ml",
     "contado": 925000, "cuota": 508750, "caja": (620, 600)},
    {"id": "delina", "marca": "PARFUMS DE MARLY", "nombre": "Delina Exclusif", "detalle": "Parfum  ·  75 ml",
     "contado": 1749000, "cuota": 961950, "caja": (520, 610)},
]
extra = os.path.join(AQUI, "perfumes_extra.json")
if os.path.exists(extra):
    PERFUMES += json.load(open(extra))


def cargar(pid):
    return Image.open(os.path.join(AQUI, f"cut/{pid}.png")).convert("RGBA")


def encajar(img, maxw, maxh):
    k = min(maxw / img.width, maxh / img.height)
    return img.resize((int(img.width * k), int(img.height * k)), Image.LANCZOS)


def pegar(img, prod, cx, ybase, maxw, maxh):
    p = encajar(prod, maxw, maxh)
    N.pegar_producto(img, p, cx, ybase, p.height)


def precio(img, y, contado, cuota):
    N.tarjeta(img, (170, y, 910, y + 200), alfa=235, color=N.AZUL_OSC)
    N.texto(img, N.W / 2, y + 16, N.gs(contado), N.poppins("Bold", 68), N.BLANCO, sombra=False)
    N.texto(img, N.W / 2, y + 102, "CONTADO", N.poppins("SemiBold", 22), N.DORADO, esp=6, sombra=False)
    N.texto(img, N.W / 2, y + 138, "o 2 cuotas de " + N.gs(cuota), N.poppins("Medium", 31), N.CREMA, sombra=False)


def portada():
    img, rng = N.escena(101)
    N.oscurecer_arriba(img, 620)
    sel = PERFUMES[:3]
    pos = [(N.W / 2 - 285, 360, 440), (N.W / 2 + 285, 330, 520), (N.W / 2 + 10, 470, 420)]  # izq, der, centro (adelante)
    orden = [1, 2, 0] if len(sel) >= 3 else list(range(len(sel)))
    for (cx, mw, mh), i in zip(pos, orden):
        yb = N.HORIZ + (215 if (cx, mw, mh) == pos[2] else 120)
        pegar(img, cargar(sel[i]["id"]), cx, yb, mw, mh)
    N.bokeh(img, rng); N.nieve(img, rng)
    N.destellos(img, [(140, 640, 22), (950, 600, 26), (540, 520, 16)], rng)
    N.viñeta(img); N.logo(img)
    N.etiqueta(img, 168, "NAVIDAD 2026")
    N.texto(img, N.W / 2, 205, "PERFUMES PARA", N.poppins("ExtraBold", 80), N.BLANCO, esp=3)
    N.texto(img, N.W / 2, 280, "regalar", N.cursiva(140), N.DORADO)
    h = N.pildora(img, N.W / 2, 1218, "Contado o en 2 cuotas       ", N.poppins("SemiBold", 30))
    d = ImageDraw.Draw(img); fp = N.poppins("SemiBold", 30)
    t = "Contado o en 2 cuotas       "
    ax = N.W / 2 - d.textlength(t, font=fp) / 2 + d.textlength("Contado o en 2 cuotas ", font=fp) + 26
    ay = 1218 + h / 2
    d.line([(ax - 22, ay), (ax + 14, ay)], fill=N.BLANCO, width=4)
    d.line([(ax + 2, ay - 12), (ax + 16, ay), (ax + 2, ay + 12)], fill=N.BLANCO, width=4, joint="curve")
    return img


def lamina(p, seed):
    img, rng = N.escena(seed)
    N.oscurecer_arriba(img, 620)
    mw, mh = p["caja"]
    pegar(img, cargar(p["id"]), N.W / 2, N.HORIZ + 110, mw, mh)
    N.bokeh(img, rng); N.nieve(img, rng)
    N.destellos(img, [(200, 620, 20), (880, 680, 24)], rng)
    N.viñeta(img); N.logo(img)
    N.etiqueta(img, 160, p["marca"])
    f = N.cursiva(130)
    while ImageDraw.Draw(img).textlength(p["nombre"], font=f) > 960:
        f = N.cursiva(f.size - 6)
    N.texto(img, N.W / 2, 185, p["nombre"], f, N.BLANCO)
    N.texto(img, N.W / 2, 368, p["detalle"], N.poppins("Medium", 34), N.CREMA, esp=1)
    precio(img, 1095, p["contado"], p["cuota"])
    return img


def cierre():
    img, rng = N.escena(909)
    N.oscurecer_arriba(img, 680, 0.6)
    for (x, yb, w, h) in ((300, N.HORIZ + 175, 190, 160), (560, N.HORIZ + 190, 220, 180), (440, N.HORIZ + 240, 150, 120)):
        N.pegar_con_sombra(img, N.regalo(w, h, (246, 236, 220), N.CELESTE, rng), x, yb)
    N.bokeh(img, rng); N.nieve(img, rng)
    N.destellos(img, [(260, 820, 22), (830, 760, 26)], rng)
    N.viñeta(img); N.logo(img)
    N.etiqueta(img, 160, "TU REGALO, CONTADO O EN CUOTAS")
    N.texto(img, N.W / 2, 198, "PEDÍ EL TUYO", N.poppins("ExtraBold", 86), N.BLANCO, esp=4)
    N.texto(img, N.W / 2, 275, "por WhatsApp", N.cursiva(120), N.DORADO)
    N.pildora(img, N.W / 2, 465, "0972 736 002", N.poppins("Bold", 48), fondo=(37, 158, 92), padx=56, pady=22)
    N.texto(img, N.W / 2, 600, "o en el link de la bio", N.poppins("Medium", 32), N.CREMA)
    N.pie(img, 1262)
    return img


if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    for f in os.listdir(SALIDA):
        os.remove(os.path.join(SALIDA, f))
    slides = [portada()] + [lamina(p, 200 + i) for i, p in enumerate(PERFUMES)] + [cierre()]
    for i, s in enumerate(slides, 1):
        s.convert("RGB").save(f"{SALIDA}/{i}.png")
    print(len(slides), "slides")
