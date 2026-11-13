#!/usr/bin/env python3
"""
Pinta el logo de LARESE STORE con cada color de la paleta de marca y arma las opciones
de logo sobre fondo para elegir.

Uso (desde la raíz del repo):
    python3 marca/crear_opciones_logo.py

Genera:
    marca/logos/logo-<color>.png        logo "larese STORE" transparente en cada color
    marca/logos/isotipo-<color>.png     isotipo "la" transparente en cada color
    marca/opciones-logo/opcion-NN.png   cada combinación fondo + logo
    marca/opciones-logo/tablero-fondo-<color>.png   un tablero por fondo, con las opciones numeradas

Solo se arman las combinaciones donde el logo se lee bien (contraste 3:1 o más).
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FUENTES = os.path.join(RAIZ, "herramientas/carrusel-bordo/assets/fonts")
LOGO_ALTA = os.path.join(RAIZ, "comercial-fragancias/public/marca/logo-negro.png")
ISOTIPO = os.path.join(RAIZ, "comercial-fragancias/public/marca/isotipo-negro.png")
MASCARA_STORE = os.path.join(RAIZ, "herramientas/pieza-fondo-blanco/assets/logo_texto_mascara.png")
SALIDA_LOGOS = os.path.join(RAIZ, "marca/logos")
SALIDA_OPCIONES = os.path.join(RAIZ, "marca/opciones-logo")

PALETA = [
    ("Bordó vino", "bordo-vino", "#41030B"),
    ("Bordó cuero", "bordo-cuero", "#2A0B0D"),
    ("Tinta", "tinta", "#321918"),
    ("Malva", "malva", "#7B5B5B"),
    ("Crema", "crema", "#F8F4EB"),
    ("Rosa marfil", "rosa-marfil", "#FCE5DA"),
    ("Dorado antiguo", "dorado", "#997957"),
]


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def luminancia(c):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = map(f, c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = sorted([luminancia(a), luminancia(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def logo_alta():
    """'larese' del archivo de 1200 px + 'STORE' de la máscara, a la misma escala."""
    alta = Image.open(LOGO_ALTA).getchannel("A")
    alta = alta.crop(alta.getbbox())
    m = Image.open(MASCARA_STORE).convert("L")
    a = np.array(m) > 128
    # "larese" baja hasta abajo; "STORE" es chico y queda arriba a la derecha
    fin_larese = int(np.where(a[90:].any(0))[0].max()) + 1
    ys, xs = np.where(a[:, :fin_larese])
    x0, x1, y0 = xs.min(), xs.max(), ys.min()
    esc = alta.width / (x1 - x0 + 1)
    store_m = m.crop((fin_larese, 0, m.width, m.height))
    bb = store_m.getbbox()
    store = store_m.crop(bb)
    store = store.resize((round(store.width * esc), round(store.height * esc)), Image.LANCZOS)
    sx = round((fin_larese + bb[0] - x0) * esc)
    sy = round((bb[1] - y0) * esc)
    lienzo = Image.new("L", (sx + store.width + 2, max(alta.height, sy + store.height)), 0)
    lienzo.paste(alta, (0, 0))
    lienzo.paste(store, (sx, sy), store)
    return lienzo


def pintar(mascara, color):
    capa = Image.new("RGBA", mascara.size, color + (0,))
    capa.putalpha(mascara)
    return capa


def serif(tam, peso=450):
    f = ImageFont.truetype(os.path.join(FUENTES, "PlayfairDisplay.ttf"), tam)
    f.set_variation_by_axes([peso])
    return f


def main():
    os.makedirs(SALIDA_LOGOS, exist_ok=True)
    os.makedirs(SALIDA_OPCIONES, exist_ok=True)
    marca = logo_alta()
    iso = Image.open(ISOTIPO).getchannel("A")
    iso = iso.crop(iso.getbbox())

    for _, slug, h in PALETA:
        pintar(marca, rgb(h)).save(os.path.join(SALIDA_LOGOS, f"logo-{slug}.png"), optimize=True)
        pintar(iso, rgb(h)).save(os.path.join(SALIDA_LOGOS, f"isotipo-{slug}.png"), optimize=True)

    sans = ImageFont.truetype(os.path.join(FUENTES, "Poppins-Medium.ttf"), 22)
    TW, TH, ETIQ = 500, 330, 74

    def muestra(fondo, color):
        t = Image.new("RGBA", (TW, TH), rgb(fondo) + (255,))
        w = 340
        mk = marca.resize((w, round(marca.height * w / marca.width)), Image.LANCZOS)
        t.alpha_composite(pintar(mk, rgb(color)), ((TW - w) // 2, 92))
        s = 72
        ik = iso.resize((round(iso.width * s / iso.height), s), Image.LANCZOS)
        t.alpha_composite(pintar(ik, rgb(color)), ((TW - ik.width) // 2, 205))
        return t.convert("RGB")

    num = 1
    for nombre_f, slug_f, h_f in PALETA:
        grupo = [(n, h) for n, _, h in PALETA if h != h_f and contraste(rgb(h_f), rgb(h)) >= 3.0]
        if not grupo:
            continue
        filas = (len(grupo) + 1) // 2
        BW, BH = 40 + 2 * (TW + 30) + 10, 170 + filas * (TH + ETIQ + 20) + 20
        tablero = Image.new("RGB", (BW, BH), "#EFE7DA" if h_f == "#F8F4EB" else "#F8F4EB")
        d = ImageDraw.Draw(tablero)
        d.text((BW // 2, 40), f"Fondo {nombre_f}", font=serif(54), fill="#321918", anchor="ma")
        d.text((BW // 2, 115), h_f, font=sans, fill="#7B5B5B", anchor="ma")
        for i, (nombre_l, h_l) in enumerate(grupo):
            x, y = 40 + (i % 2) * (TW + 30), 170 + (i // 2) * (TH + ETIQ + 20)
            m = muestra(h_f, h_l)
            tablero.paste(m, (x, y))
            d.rectangle((x - 1, y - 1, x + TW, y + TH), outline="#D9CDBE", width=1)
            d.text((x, y + TH + 12), f"Opción {num}", font=serif(30, 550), fill="#321918")
            d.text((x, y + TH + 48), f"Logo {nombre_l}", font=sans, fill="#7B5B5B")
            m.save(os.path.join(SALIDA_OPCIONES, f"opcion-{num:02d}.png"), optimize=True)
            print(f"{num:2d}  fondo {nombre_f:15s} logo {nombre_l}")
            num += 1
        tablero.save(os.path.join(SALIDA_OPCIONES, f"tablero-fondo-{slug_f}.png"), optimize=True)


if __name__ == "__main__":
    main()
