"""Carrusel navideño Light Blue para LARESE STORE (1080x1350 por slide)."""
import os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

AQUI = os.path.dirname(os.path.abspath(__file__))
SK = "/root/.claude/skills/synced/5d0982d5-d6b7-4d88-99f1-76c399ea6f7c_6799b8cc-0ae4-4280-9001-08db20837305/larese-anuncios/assets/"
FOTO = os.path.join(AQUI, "dl/shop.jpg")
SALIDA = "/home/user/Larese/carrusel-navidad-light-blue"
W, H = 1080, 1350
HORIZ = 930          # línea donde termina la pared y empieza el "piso de azúcar"

BLANCO = (255, 255, 255)
DORADO = (236, 204, 142)
CREMA = (250, 240, 222)
AZUL_OSC = (28, 47, 88)
CELESTE = (150, 201, 233)


# ---------- fuentes ----------
def poppins(peso, tam):
    rutas = {"Light": os.path.join(AQUI, "fonts/Poppins-Light.ttf"),
             "Regular": os.path.join(AQUI, "fonts/Poppins-Regular.ttf")}
    return ImageFont.truetype(rutas.get(peso, SK + f"fonts/Poppins-{peso}.ttf"), tam)


def cursiva(tam, peso=500):
    f = ImageFont.truetype(os.path.join(AQUI, "fonts/PlayfairDisplay-Italic%5Bwght%5D.ttf"), tam)
    f.set_variation_by_axes([peso])
    return f


# ---------- utilidades ----------
def gradiente_v(w, h, c1, c2, curva=1.0):
    t = (np.linspace(0, 1, h) ** curva)[:, None, None]
    arr = np.array(c1, np.float32) * (1 - t) + np.array(c2, np.float32) * t
    return Image.fromarray(np.repeat(arr, w, 1).astype(np.uint8))


def capa():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def brillo_azucar(img, y0, y1, n, rng, tam=(1, 3), alfa=(90, 255), color=(255, 236, 190)):
    """Puntitos brillantes tipo azúcar / glitter."""
    l = capa(); d = ImageDraw.Draw(l)
    for _ in range(n):
        x = rng.uniform(0, W); y = rng.uniform(y0, y1); r = rng.uniform(*tam)
        a = int(rng.uniform(*alfa))
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (a,))
    halo = l.filter(ImageFilter.GaussianBlur(2))
    img.alpha_composite(halo); img.alpha_composite(l)


def destellos(img, puntos, rng):
    """Estrellitas de 4 puntas con halo."""
    l = capa(); d = ImageDraw.Draw(l)
    for (x, y, r) in puntos:
        d.line([x - r, y, x + r, y], fill=(255, 250, 230, 230), width=2)
        d.line([x, y - r, x, y + r], fill=(255, 250, 230, 230), width=2)
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 255, 255, 255))
    img.alpha_composite(l.filter(ImageFilter.GaussianBlur(4)))
    img.alpha_composite(l)


def textura(img, fuerza, rng_seed):
    """Grano fino para que la superficie parezca galleta con azúcar."""
    g = np.random.default_rng(rng_seed).normal(0, fuerza, (H, W, 1))
    arr = np.asarray(img.convert("RGB"), np.float32) + g
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")


# ---------- escena ----------
def pared(rng):
    img = gradiente_v(W, H, (92, 52, 22), (190, 128, 64), 0.8).convert("RGBA")
    img = textura(img, 9, 1)
    d = ImageDraw.Draw(img)
    # tres paneles tipo galleta de jengibre con glaseado
    paneles = [(-150, 120, 250, 900), (300, 60, 780, 900), (830, 120, 1230, 900)]
    for (x0, y0, x1, y1) in paneles:
        # marco en relieve
        d.rounded_rectangle([x0, y0, x1, y1], 34, fill=(176, 112, 52))
        sombra = capa(); ImageDraw.Draw(sombra).rounded_rectangle([x0 + 34, y0 + 34, x1 - 34, y1 - 34], 22, fill=(0, 0, 0, 120))
        img.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(10)))
        hueco = gradiente_v(x1 - x0 - 76, y1 - y0 - 76, (128, 78, 36), (168, 108, 52))
        m = Image.new("L", hueco.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, hueco.width - 1, hueco.height - 1], 20, fill=255)
        img.paste(hueco, (x0 + 38, y0 + 38), m)
    img = textura(img, 7, 2)
    d = ImageDraw.Draw(img)
    for (x0, y0, x1, y1) in paneles:
        # glaseado: línea de puntitos en el marco y línea fina adentro
        for inset, paso, r in ((16, 21, 5), (48, 0, 0)):
            if paso:
                for xx in np.arange(x0 + inset, x1 - inset, paso):
                    for yy in (y0 + inset, y1 - inset):
                        d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=CREMA)
                for yy in np.arange(y0 + inset, y1 - inset, paso):
                    for xx in (x0 + inset, x1 - inset):
                        d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=CREMA)
            else:
                d.rounded_rectangle([x0 + inset, y0 + inset, x1 - inset, y1 - inset], 18, outline=CREMA, width=4)
        # estrellitas de glaseado en las esquinas
        for (cx, cy) in ((x0 + 48, y0 + 48), (x1 - 48, y0 + 48)):
            d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 246, 228))
    brillo_azucar(img, 0, HORIZ, 2600, rng, (0.6, 1.8), (60, 200))
    # desenfoque de profundidad: la pared queda atrás
    return img.filter(ImageFilter.GaussianBlur(3.2))


def piso(img, rng):
    p = gradiente_v(W, H - HORIZ + 60, (214, 182, 140), (246, 232, 208), 0.6).convert("RGBA")
    m = gradiente_v(W, H - HORIZ + 60, (0, 0, 0), (255, 255, 255), 0.15).convert("L")
    img.paste(p, (0, HORIZ - 60), m)
    brillo_azucar(img, HORIZ - 20, H, 3500, rng, (0.5, 1.6), (90, 255), (255, 255, 245))
    return img


def regalo(w, h, fondo, cinta, rng):
    """Caja de regalo crema con moño celeste, con tapa en perspectiva."""
    t = int(h * 0.22)
    l = Image.new("RGBA", (w + 40, h + t + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    ox, oy = 20, 60
    cara = gradiente_v(w, h, fondo, tuple(int(c * 0.82) for c in fondo)).convert("RGBA")
    l.paste(cara, (ox, oy + t))
    tapa = [(ox, oy + t), (ox + w, oy + t), (ox + w - w * 0.08, oy), (ox + w * 0.08, oy)]
    d.polygon(tapa, fill=tuple(min(255, int(c * 1.06)) for c in fondo))
    # cintas
    cw = max(10, w // 9)
    cx = ox + w // 2
    d.rectangle([cx - cw // 2, oy + t, cx + cw // 2, oy + t + h], fill=cinta)
    d.polygon([(cx - cw // 2, oy + t), (cx + cw // 2, oy + t), (cx + cw // 2 - 2, oy), (cx - cw // 2 + 2, oy)], fill=cinta)
    d.line([cx - cw // 2 + 3, oy + t, cx - cw // 2 + 3, oy + t + h], fill=(225, 243, 252), width=2)
    # moño
    bw = w * 0.32
    by = oy + 4
    d.ellipse([cx - bw, by - bw * 0.45, cx - 4, by + bw * 0.25], fill=cinta)
    d.ellipse([cx + 4, by - bw * 0.45, cx + bw, by + bw * 0.25], fill=cinta)
    d.ellipse([cx - bw * 0.68, by - bw * 0.3, cx - bw * 0.25, by + bw * 0.08], fill=tuple(int(c * 0.85) for c in cinta))
    d.ellipse([cx + bw * 0.25, by - bw * 0.3, cx + bw * 0.68, by + bw * 0.08], fill=tuple(int(c * 0.85) for c in cinta))
    d.ellipse([cx - cw * 0.7, by - cw * 0.6, cx + cw * 0.7, by + cw * 0.6], fill=cinta)
    # borde dorado de la caja
    d.rectangle([ox, oy + t, ox + w, oy + t + h], outline=(214, 180, 116), width=3)
    return l


def bloque_galleta(w, h):
    """Bloque de galleta de jengibre con glaseado ondulado (como los del ejemplo)."""
    t = int(h * 0.18)
    l = Image.new("RGBA", (w + 20, h + t + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    ox, oy = 10, 10
    cara = gradiente_v(w, h, (164, 98, 46), (118, 66, 28)).convert("RGBA")
    l.paste(cara, (ox, oy + t))
    d.polygon([(ox, oy + t), (ox + w, oy + t), (ox + w - 14, oy), (ox + 14, oy)], fill=(184, 118, 60))
    # glaseado: borde superior y ondas
    d.line([(ox, oy + t), (ox + w, oy + t)], fill=CREMA, width=6)
    n = 4; paso = w / n
    for i in range(n):
        x0 = ox + i * paso
        d.arc([x0 + 6, oy + t + h * 0.45, x0 + paso - 6, oy + t + h * 0.85], 0, 180, fill=CREMA, width=6)
    d.line([(ox + w / 2, oy + t), (ox + w / 2, oy + t + h)], fill=CREMA, width=5)
    lr = l.copy()
    g = np.random.default_rng(w).normal(0, 10, (lr.height, lr.width, 1))
    arr = np.asarray(lr, np.float32); arr[..., :3] = np.clip(arr[..., :3] + g, 0, 255)
    return Image.fromarray(arr.astype(np.uint8))


def pegar_con_sombra(img, obj, x, ybase, blur=0, sombra=0.55):
    """Pega un objeto apoyado en el piso (ybase = donde toca), con sombra de contacto."""
    s = capa(); d = ImageDraw.Draw(s)
    d.ellipse([x + obj.width * 0.04, ybase - 18, x + obj.width * 0.96, ybase + 22], fill=(70, 40, 15, int(255 * sombra)))
    img.alpha_composite(s.filter(ImageFilter.GaussianBlur(14)))
    o = obj.filter(ImageFilter.GaussianBlur(blur)) if blur else obj
    img.alpha_composite(o, (int(x), int(ybase - obj.height)))


def producto():
    """Recorta frasco y caja del fondo blanco (fila por fila, conserva esquinas redondeadas)."""
    src = Image.open(FOTO).convert("RGB")
    a = np.asarray(src).astype(int)
    oscuro = a.min(2) < 246
    mask = np.zeros(oscuro.shape, np.uint8)
    for (x0, x1, y0, y1) in ((300, 770, 260, 1328), (770, 1290, 200, 1328)):
        for y in range(y0, y1):
            cols = np.where(oscuro[y, x0:x1])[0]
            if len(cols):
                mask[y, x0 + cols.min(): x0 + cols.max() + 1] = 255
    m = Image.fromarray(mask).filter(ImageFilter.GaussianBlur(1.2))
    rgba = src.copy(); rgba.putalpha(m)
    rgba = rgba.crop((318, 206, 1266, 1329))
    # tinte cálido suave para integrarlo a la luz dorada
    arr = np.asarray(rgba, np.float32)
    arr[..., 0] *= 1.03; arr[..., 2] *= 0.97
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def pegar_producto(img, prod, cx, ybase, alto):
    p = prod.resize((int(prod.width * alto / prod.height), alto), Image.LANCZOS)
    x = int(cx - p.width / 2)
    # luz dorada detrás
    g = capa(); ImageDraw.Draw(g).ellipse([cx - p.width * 0.9, ybase - alto * 1.05, cx + p.width * 0.9, ybase + 40], fill=(255, 214, 140, 120))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(90)))
    # reflejo en el azúcar
    ref = p.transpose(Image.FLIP_TOP_BOTTOM)
    fade = gradiente_v(ref.width, ref.height, (70,) * 3, (0,) * 3, 0.35).convert("L")
    ref.putalpha(ImageChops.multiply(ref.getchannel("A"), fade))
    img.alpha_composite(ref.filter(ImageFilter.GaussianBlur(3)), (x, ybase))
    pegar_con_sombra(img, p, x, ybase, sombra=0.6)


def bokeh(img, rng, n=14):
    l = capa(); d = ImageDraw.Draw(l)
    for _ in range(n):
        x = rng.choice([rng.uniform(-60, 220), rng.uniform(860, 1140)])
        y = rng.uniform(80, H - 60); r = rng.uniform(18, 60)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 220, 150, int(rng.uniform(40, 100))))
    img.alpha_composite(l.filter(ImageFilter.GaussianBlur(9)))


def nieve(img, rng, n=160):
    l = capa(); d = ImageDraw.Draw(l)
    for _ in range(n):
        x = rng.uniform(0, W); y = rng.uniform(0, H); r = rng.uniform(1.5, 4.5)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, int(rng.uniform(90, 200))))
    img.alpha_composite(l.filter(ImageFilter.GaussianBlur(1.2)))


def oscurecer_arriba(img, hasta=560, fuerza=0.55):
    a = (np.clip(1 - np.arange(H) / hasta, 0, 1) ** 1.3 * fuerza * 255).astype(np.uint8)
    m = Image.fromarray(np.repeat(a[:, None], W, 1))
    negro = Image.new("RGBA", (W, H), (40, 20, 6, 255))
    img.paste(negro, (0, 0), m)


def viñeta(img):
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.75)) ** 2)
    a = (np.clip(r - 0.55, 0, 1) * 1.4 * 255).clip(0, 150).astype(np.uint8)
    img.paste(Image.new("RGBA", (W, H), (30, 14, 4, 255)), (0, 0), Image.fromarray(a))


def escena(seed, regalos=True, galletas=True):
    rng = random.Random(seed)
    img = pared(rng)
    img = piso(img, rng)
    if galletas:
        pegar_con_sombra(img, bloque_galleta(250, 190), -70, HORIZ + 40, blur=2.5)
        pegar_con_sombra(img, bloque_galleta(240, 180), 900, HORIZ + 30, blur=2.5)
    if regalos:
        g1 = regalo(190, 160, (246, 236, 220), CELESTE, rng)
        g2 = regalo(150, 130, (246, 236, 220), CELESTE, rng)
        pegar_con_sombra(img, g1, 30, HORIZ + 175, blur=1.2)
        pegar_con_sombra(img, g2, 880, HORIZ + 190, blur=1.2)
    return img, rng


# ---------- texto ----------
def ancho(d, t, f, esp=0):
    return d.textlength(t, font=f) + esp * max(0, len(t) - 1)


def texto(img, cx, y, t, f, color=BLANCO, esp=0, sombra=True, anchor_left=None):
    l = capa(); d = ImageDraw.Draw(l)
    x = anchor_left if anchor_left is not None else cx - ancho(d, t, f, esp) / 2
    def dibujar(dd, col):
        xx = x
        if esp:
            for ch in t:
                dd.text((xx, y), ch, font=f, fill=col); xx += dd.textlength(ch, font=f) + esp
        else:
            dd.text((xx, y), t, font=f, fill=col)
    if sombra:
        s = capa(); dibujar(ImageDraw.Draw(s), (25, 10, 0, 170))
        img.alpha_composite(s.filter(ImageFilter.GaussianBlur(8)))
    dibujar(d, color + (255,) if len(color) == 3 else color)
    img.alpha_composite(l)


def logo(img, y=58, ancho_logo=230):
    m = Image.open(SK + "logo_texto_mascara.png").convert("L")
    m = m.resize((ancho_logo, int(m.height * ancho_logo / m.width)), Image.LANCZOS)
    img.paste(Image.new("RGBA", m.size, BLANCO + (255,)), ((W - ancho_logo) // 2, y), m)


def etiqueta(img, y, t):
    texto(img, W / 2, y, t, poppins("SemiBold", 25), DORADO, esp=7)


def pildora(img, cx, y, t, f, fondo=AZUL_OSC, color=BLANCO, padx=46, pady=20):
    d = ImageDraw.Draw(img)
    tw = d.textlength(t, font=f); bb = f.getbbox(t)
    h = bb[3] - bb[1] + pady * 2
    s = capa(); ImageDraw.Draw(s).rounded_rectangle([cx - tw / 2 - padx, y + 8, cx + tw / 2 + padx, y + h + 8], h / 2, fill=(30, 12, 0, 120))
    img.alpha_composite(s.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(img).rounded_rectangle([cx - tw / 2 - padx, y, cx + tw / 2 + padx, y + h], h / 2, fill=fondo)
    ImageDraw.Draw(img).text((cx - tw / 2, y + pady - bb[1]), t, font=f, fill=color)
    return h


def tarjeta(img, box, alfa=170, color=(34, 18, 6)):
    x0, y0, x1, y1 = box
    s = capa(); ImageDraw.Draw(s).rounded_rectangle(box, 34, fill=color + (alfa,))
    img.alpha_composite(s)
    ImageDraw.Draw(img).rounded_rectangle(box, 34, outline=DORADO + (160,), width=2)


def gs(v):
    return "Gs. " + f"{v:,}".replace(",", ".")


def flecha_deslizar(img, y):
    texto(img, W / 2, y, "Deslizá  →", poppins("Medium", 30), BLANCO, esp=2)


def pie(img, y=1268):
    texto(img, W / 2, y, "100% original  ·  Envíos a todo Paraguay", poppins("Medium", 27), (90, 52, 20), esp=1, sombra=False)


# ---------- slides ----------
def slide1(prod):
    img, rng = escena(11)
    oscurecer_arriba(img, 600)
    pegar_producto(img, prod, W / 2, HORIZ + 185, 560)
    bokeh(img, rng); nieve(img, rng)
    destellos(img, [(250, 700, 22), (840, 560, 28), (770, 1020, 16)], rng)
    viñeta(img)
    logo(img)
    etiqueta(img, 168, "NAVIDAD 2026")
    texto(img, W / 2, 205, "EL REGALO", poppins("ExtraBold", 92), BLANCO, esp=4)
    texto(img, W / 2, 285, "perfecto", cursiva(150), DORADO)
    h = pildora(img, W / 2, 1218, "Deslizá       ", poppins("SemiBold", 30))
    d = ImageDraw.Draw(img); fp = poppins("SemiBold", 30); ax, ay = W / 2 - d.textlength("Deslizá       ", font=fp) / 2 + d.textlength("Deslizá ", font=fp) + 26, 1218 + h / 2
    d.line([(ax - 22, ay), (ax + 14, ay)], fill=BLANCO, width=4)
    d.line([(ax + 2, ay - 12), (ax + 16, ay), (ax + 2, ay + 12)], fill=BLANCO, width=4, joint="curve")
    return img


def slide2(prod):
    img, rng = escena(22, galletas=True)
    oscurecer_arriba(img, 620)
    pegar_producto(img, prod, W / 2, HORIZ + 120, 520)
    bokeh(img, rng); nieve(img, rng)
    destellos(img, [(230, 640, 20), (860, 700, 24)], rng)
    viñeta(img)
    logo(img)
    etiqueta(img, 160, "DOLCE & GABBANA")
    texto(img, W / 2, 178, "Light Blue", cursiva(140), BLANCO)
    texto(img, W / 2, 372, "Eau de Toilette  ·  100 ml", poppins("Medium", 34), CREMA, esp=1)
    # precio
    tarjeta(img, (200, 1100, 880, 1300), alfa=235, color=AZUL_OSC)
    texto(img, W / 2, 1118, gs(420000), poppins("Bold", 70), BLANCO, sombra=False)
    texto(img, W / 2, 1210, "contado  ·  o 2 cuotas de " + gs(231000), poppins("Regular", 29), CREMA, sombra=False)
    return img


def slide3(prod):
    img, rng = escena(33, regalos=True)
    oscurecer_arriba(img, 700, 0.6)
    pegar_producto(img, prod, W / 2 + 150, HORIZ + 195, 290)
    bokeh(img, rng, 10); nieve(img, rng)
    viñeta(img)
    logo(img)
    etiqueta(img, 160, "LAS NOTAS")
    texto(img, W / 2, 198, "FRESCO PARA UNA", poppins("ExtraBold", 66), BLANCO, esp=3)
    texto(img, W / 2, 262, "Navidad de verano", cursiva(108), DORADO)
    tarjeta(img, (110, 420, 970, 860), alfa=175)
    filas = [("SALIDA", "Limón siciliano, manzana, campanilla"),
             ("CORAZÓN", "Jazmín, rosa blanca, bambú"),
             ("FONDO", "Cedro, ámbar, almizcle")]
    y = 452
    for i, (k, v) in enumerate(filas):
        texto(img, W / 2, y, k, poppins("SemiBold", 25), DORADO, esp=6, sombra=False)
        texto(img, W / 2, y + 40, v, poppins("Regular", 36), BLANCO, sombra=False)
        if i < 2:
            ImageDraw.Draw(img).line([(W / 2 - 60, y + 118), (W / 2 + 60, y + 118)], fill=DORADO + (180,), width=2)
        y += 145
    return img


def slide4(prod):
    img, rng = escena(44)
    # más regalos en el centro: decants como regalo chico
    for (x, yb, w, h) in ((330, HORIZ + 175, 170, 140), (560, HORIZ + 190, 200, 165), (440, HORIZ + 240, 140, 110)):
        pegar_con_sombra(img, regalo(w, h, (246, 236, 220), CELESTE, rng), x, yb)
    oscurecer_arriba(img, 720, 0.6)
    bokeh(img, rng); nieve(img, rng)
    destellos(img, [(300, 940, 18), (800, 900, 22)], rng)
    viñeta(img)
    logo(img)
    etiqueta(img, 160, "¿QUERÉS PROBARLO PRIMERO?")
    texto(img, W / 2, 198, "DECANTS", poppins("ExtraBold", 86), BLANCO, esp=5)
    texto(img, W / 2, 275, "originales", cursiva(120), DORADO)
    texto(img, W / 2, 432, "Light Blue original en frasquitos,", poppins("Regular", 33), CREMA)
    texto(img, W / 2, 476, "ideal para regalar o llevar en la cartera", poppins("Regular", 33), CREMA)
    precios = [("5 ml", 45000), ("10 ml", 70000), ("30 ml", 180000)]
    y = 560
    for ml, p in precios:
        tarjeta(img, (220, y, 860, y + 84), alfa=200, color=AZUL_OSC)
        texto(img, 0, y + 16, ml, poppins("SemiBold", 38), DORADO, sombra=False, anchor_left=270)
        f = poppins("Bold", 38); d = ImageDraw.Draw(img)
        texto(img, 0, y + 16, gs(p), f, BLANCO, sombra=False, anchor_left=810 - d.textlength(gs(p), font=f))
        y += 100
    return img


def slide5(prod):
    img, rng = escena(55)
    oscurecer_arriba(img, 680, 0.6)
    pegar_producto(img, prod, W / 2, HORIZ + 175, 400)
    bokeh(img, rng); nieve(img, rng)
    destellos(img, [(260, 820, 22), (830, 760, 26)], rng)
    viñeta(img)
    logo(img)
    etiqueta(img, 160, "REGALÁ LIGHT BLUE")
    texto(img, W / 2, 198, "PEDÍ EL TUYO", poppins("ExtraBold", 86), BLANCO, esp=4)
    texto(img, W / 2, 275, "por WhatsApp", cursiva(120), DORADO)
    pildora(img, W / 2, 465, "0972 736 002", poppins("Bold", 48), fondo=(37, 158, 92), padx=56, pady=22)
    texto(img, W / 2, 600, "o en el link de la bio", poppins("Medium", 32), CREMA)
    pie(img, 1262)
    return img


if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    prod = producto()
    for i, fn in enumerate((slide1, slide2, slide3, slide4, slide5), 1):
        fn(prod).convert("RGB").save(f"{SALIDA}/{i}.png")
        print("ok", i)
