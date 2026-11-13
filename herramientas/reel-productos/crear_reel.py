#!/usr/bin/env python3
"""
Reel animado de LARESE STORE con fotos de productos (sin video de la dueña),
con la paleta y la tipografía de la marca.

Uso:
    python3 crear_reel.py reel.json salida.mp4

Arma un video vertical 1080x1920 a 30 cuadros por segundo:
  1. Apertura: título en Playfair Display (tinta) y cursiva en Pinyon Script sobre crema.
  2. Un producto por escena, alternando fondo crema y bordó vino: número, nombre,
     marca en cursiva, el frasco con un zoom suave y el precio.
  3. Cierre en bordó vino: logo crema, pregunta, WhatsApp y envíos.
Además guarda la portada del reel (salida-portada.png).

El video sale sin música: la dueña le pone un audio en tendencia desde Instagram.
Los textos importantes quedan entre y=230 y y=1560, fuera de lo que tapan los botones
de Instagram.

Spec (JSON):
{
  "carrusel": "../carrusel-mas-pedidos/carrusel.json",   # toma de ahí los productos y la carpeta de fotos
  "productos": [...],                                     # o la lista directa (mismo formato que el carrusel)
  "fotos": "fotos",                                       # solo si se usa "productos" directo
  "apertura": {"titulo": "Los 18 más pedidos", "cursiva": "del 2026", "bajada": "Mirá hasta el final"},
  "cierre": {"titulo": "¿Cuál es el tuyo?", "cursiva": "contanos en comentarios"},
  "seg_apertura": 2.6, "seg_producto": 0.9, "seg_cierre": 3.0
}
"""
import importlib.util
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "carrusel", os.path.join(AQUI, "..", "carrusel-bordo", "scripts", "crear_carrusel.py"))
cr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cr)

W, H, FPS = 1080, 1920, 30
BORDO, TINTA, MALVA, CREMA, MARFIL, DORADO = cr.BORDO, cr.TINTA, cr.MALVA, cr.CREMA, cr.MARFIL, cr.DORADO
WHATSAPP = "0972 736 002"


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def logo_capa(ancho, color):
    m = Image.open(os.path.join(AQUI, "..", "carrusel-bordo", "assets", "logo_texto_mascara.png")).convert("L")
    m = m.resize((int(ancho), int(m.height * ancho / m.width)), Image.LANCZOS)
    capa = Image.new("RGBA", m.size, color + (0,))
    capa.putalpha(m)
    return capa


def texto_capa(lineas):
    """lineas: [(texto, fuente, color, y)] centrados. Devuelve una capa RGBA transparente."""
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    for t, f, col, y in lineas:
        cr.escribir(d, W / 2, y, t, f, col, ancla="ma")
    return capa


def con_alfa(capa, a, dy=0):
    """La capa con opacidad a (0-1) y corrida dy píxeles hacia abajo."""
    if a >= 1 and dy == 0:
        return capa
    c = capa.copy()
    if a < 1:
        c.putalpha(c.getchannel("A").point(lambda v: int(v * a)))
    if dy:
        out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        out.alpha_composite(c, (0, int(dy)))
        return out
    return c


# ---------------- escenas ----------------

def escena_apertura(sp, n):
    fondo = Image.new("RGBA", (W, H), CREMA + (255,))
    lg = logo_capa(260, BORDO)
    titulo = sp.get("titulo", "Los más pedidos")
    f_t = cr.serif(118, 450)
    d = ImageDraw.Draw(fondo)
    lineas_t = cr.envolver(d, titulo, f_t, 920)
    y = 640
    capas = []
    for l in lineas_t:
        capas.append(texto_capa([(l, f_t, TINTA, y)]))
        y += 138
    cur = texto_capa([(sp.get("cursiva", ""), cr.cursiva(150), MALVA, y + 10)])
    raya_y = y + 250
    baj = texto_capa([(sp.get("bajada", "").upper(), cr.sans(30, "SemiBold"), DORADO, raya_y + 50)])

    def cuadro(i):
        t = i / FPS
        img = fondo.copy()
        img.alpha_composite(con_alfa(lg, ease(t / 0.4)), ((W - lg.width) // 2, 260))
        for k, c in enumerate(capas):
            p = ease((t - 0.15 - 0.12 * k) / 0.45)
            img.alpha_composite(con_alfa(c, p, (1 - p) * 40))
        p = ease((t - 0.55) / 0.5)
        img.alpha_composite(con_alfa(cur, p, (1 - p) * 30))
        p = ease((t - 0.9) / 0.4)
        ImageDraw.Draw(img).line((W / 2 - 90 * p, raya_y, W / 2 + 90 * p, raya_y), fill=DORADO, width=3)
        img.alpha_composite(con_alfa(baj, ease((t - 1.1) / 0.4)))
        return img
    return [cuadro(i) for i in range(n)]


def escena_producto(p, num, fotos, oscuro, n):
    fondo = Image.new("RGBA", (W, H), (BORDO if oscuro else CREMA) + (255,))
    principal = MARFIL if oscuro else TINTA
    suave = DORADO if oscuro else MALVA
    d = ImageDraw.Draw(fondo)

    # arriba: número, nombre y marca
    lg = logo_capa(150, CREMA if oscuro else BORDO)
    fondo.alpha_composite(lg, ((W - lg.width) // 2, 150))
    cr.escribir(d, W / 2, 250, f"N.º {num:02d}", cr.sans(30, "SemiBold"), suave, esp=6, ancla="ma")
    tam = 104
    while True:
        f_n = cr.serif(tam, 450)
        lineas = cr.envolver(d, p["nombre"], f_n, 940)
        if len(lineas) <= 2 or tam <= 60:
            break
        tam -= 6
    y = 310
    for l in lineas:
        cr.escribir(d, W / 2, y, l, f_n, principal, ancla="ma")
        y += tam * 1.12
    cr.escribir(d, W / 2, y + 4, p["marca"], cr.cursiva(84), suave, ancla="ma")
    top_prod = y + 150

    # abajo: tipo y precio
    cr.escribir(d, W / 2, 1400, p.get("tipo", "").upper(), cr.sans(26, "SemiBold"), suave, esp=6, ancla="ma")
    prefijo = p.get("prefijo", "desde")
    f_pre, f_pr = cr.cursiva(82), cr.serif(86, 520)
    t_pr = cr.guaranies(p["precio"])
    sep = 26 if prefijo else 0
    w_pre = cr.ancho(d, prefijo, f_pre) if prefijo else 0
    x = W / 2 - (w_pre + sep + cr.ancho(d, t_pr, f_pr)) / 2
    if prefijo:
        cr.escribir(d, x, 1452, prefijo, f_pre, suave)
    cr.escribir(d, x + w_pre + sep, 1458, t_pr, f_pr, principal)

    # producto
    ruta = os.path.join(fotos, p["foto"])
    caja = (W / 2 - 400, top_prod, W / 2 + 400, 1360)
    prod, ok = cr.cargar_producto(ruta)
    if p.get("recorte") is False or not ok:
        prod = Image.open(ruta).convert("RGBA")
    esc = min((caja[2] - caja[0]) / prod.width, (caja[3] - caja[1]) / prod.height)
    prod = prod.resize((int(prod.width * esc), int(prod.height * esc)), Image.LANCZOS)
    plano = p.get("recorte") is False or not ok
    if plano and not oscuro:
        # foto con fondo blanco: se funde con el crema (multiplicar), como en el carrusel
        zona = Image.new("RGB", prod.size, CREMA)
        from PIL import ImageChops
        prod = ImageChops.multiply(zona, prod.convert("RGB")).convert("RGBA")
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).ellipse((W / 2 - prod.width * 0.42, caja[3] - 18, W / 2 + prod.width * 0.42, caja[3] + 18),
                                   fill=cr.BORDO_CUERO + (90,))
    fondo.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(16)))

    def cuadro(i):
        t = i / FPS
        img = fondo.copy()
        z = 1.07 - 0.07 * ease(t / (n / FPS))         # zoom suave hacia adentro
        a = ease(t / 0.15)
        q = prod.resize((int(prod.width * z), int(prod.height * z)), Image.BILINEAR)
        if a < 1:
            q.putalpha(q.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(q, (int(W / 2 - q.width / 2), int(caja[3] - q.height)))
        return img
    return [cuadro(i) for i in range(n)]


def escena_cierre(sp, n):
    fondo = Image.new("RGBA", (W, H), BORDO + (255,))
    lg = logo_capa(380, CREMA)
    d = ImageDraw.Draw(fondo)
    f_t = cr.serif(124, 450)
    y = 640
    capas = []
    for l in cr.envolver(d, sp.get("titulo", "¿Cuál es el tuyo?"), f_t, 900):
        capas.append(texto_capa([(l, f_t, MARFIL, y)]))
        y += 142
    cur = texto_capa([(sp.get("cursiva", "contanos en comentarios"), cr.cursiva(92), DORADO, y + 10)])
    yb = y + 230
    boton = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    db = ImageDraw.Draw(boton)
    f_b = cr.sans(44, "SemiBold")
    tb = f"WhatsApp {WHATSAPP}"
    tw = cr.ancho(db, tb, f_b)
    db.rounded_rectangle((W / 2 - tw / 2 - 60, yb, W / 2 + tw / 2 + 60, yb + 110), radius=55, fill=MARFIL)
    bb = f_b.getbbox(tb)
    db.text((W / 2 - tw / 2, yb + 55 - (bb[1] + bb[3]) / 2), tb, font=f_b, fill=BORDO)
    pie = texto_capa([("Envíos a todo Paraguay", cr.serif_it(46), DORADO, yb + 160)])

    def cuadro(i):
        t = i / FPS
        img = fondo.copy()
        img.alpha_composite(con_alfa(lg, ease(t / 0.4)), ((W - lg.width) // 2, 300))
        for k, c in enumerate(capas):
            p = ease((t - 0.1 - 0.12 * k) / 0.45)
            img.alpha_composite(con_alfa(c, p, (1 - p) * 40))
        p = ease((t - 0.5) / 0.45)
        img.alpha_composite(con_alfa(cur, p, (1 - p) * 30))
        p = ease((t - 0.8) / 0.4)
        img.alpha_composite(con_alfa(boton, p, (1 - p) * 30))
        img.alpha_composite(con_alfa(pie, ease((t - 1.0) / 0.4)))
        return img
    return [cuadro(i) for i in range(n)]


# ---------------- armado ----------------

def main():
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python3 crear_reel.py reel.json salida.mp4")
    ruta_spec, salida = sys.argv[1], sys.argv[2]
    spec = json.load(open(ruta_spec, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(ruta_spec))
    if spec.get("carrusel"):
        ruta_c = os.path.join(base, spec["carrusel"])
        c = json.load(open(ruta_c, encoding="utf-8"))
        productos = c["productos"]
        fotos = os.path.join(os.path.dirname(ruta_c), c.get("fotos", "."))
    else:
        productos = spec["productos"]
        fotos = os.path.join(base, spec.get("fotos", "."))

    n_ap = int(spec.get("seg_apertura", 2.6) * FPS)
    n_pr = int(spec.get("seg_producto", 0.9) * FPS)
    n_ci = int(spec.get("seg_cierre", 3.0) * FPS)

    ffmpeg = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
         "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", salida],
        stdin=subprocess.PIPE)

    def enviar(cuadros):
        for c in cuadros:
            ffmpeg.stdin.write(c.convert("RGB").tobytes())

    apertura = escena_apertura(spec.get("apertura", {}), n_ap)
    apertura[-1].convert("RGB").save(os.path.splitext(salida)[0] + "-portada.png", optimize=True)
    enviar(apertura)
    for i, p in enumerate(productos, 1):
        enviar(escena_producto(p, i, fotos, oscuro=(i % 2 == 0), n=n_pr))
        print(f"  {i:02d} {p['nombre']}", flush=True)
    enviar(escena_cierre(spec.get("cierre", {}), n_ci))
    ffmpeg.stdin.close()
    if ffmpeg.wait() != 0:
        raise SystemExit("ffmpeg falló")
    print(salida)


if __name__ == "__main__":
    main()
