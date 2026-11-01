"""Carrusel navideño estilo 'cinta roja' para LARESE STORE (1080x1350)."""
import os, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

AQUI = os.path.dirname(os.path.abspath(__file__))
SK = "/root/.claude/skills/synced/5d0982d5-d6b7-4d88-99f1-76c399ea6f7c_6799b8cc-0ae4-4280-9001-08db20837305/larese-anuncios/assets/"
SALIDA = "/home/user/Larese/carrusel-navidad-regalos"
W, H = 1080, 1350
BLANCO = (255, 255, 255)
CREMA = (250, 236, 228)


# ---------------- fuentes ----------------
def serif(tam, peso=500):
    f = ImageFont.truetype(os.path.join(AQUI, "fonts/CormorantGaramond%5Bwght%5D.ttf"), tam)
    f.set_variation_by_axes([peso]); return f


def poppins(peso, tam):
    p = {"Light": os.path.join(AQUI, "fonts/Poppins-Light.ttf"), "Regular": os.path.join(AQUI, "fonts/Poppins-Regular.ttf")}
    return ImageFont.truetype(p.get(peso, SK + f"fonts/Poppins-{peso}.ttf"), tam)


def capa(w=W, h=H):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


# ---------------- fondo ----------------
def fondo(seed, luz=(0.72, 0.30)):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    lx, ly = luz[0] * W, luz[1] * H
    r = np.sqrt(((xx - lx) / W) ** 2 + ((yy - ly) / H) ** 2)
    t = np.clip(r / 0.95, 0, 1)[..., None] ** 0.9
    claro = np.array([206, 52, 62], np.float32); oscuro = np.array([92, 8, 16], np.float32)
    arr = claro * (1 - t) + oscuro * t
    arr += np.random.default_rng(seed).normal(0, 2.2, (H, W, 1))
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")


# ---------------- raso (cinta) ----------------
ROJO_CINTA = np.array([214, 28, 42], np.float32)


def raso(ancho, largo, seed=0):
    """Textura de cinta de raso vertical: bordes oscuros, brillo central suave, trama fina."""
    x = np.linspace(-1, 1, ancho)
    perfil = 0.62 + 0.30 * np.exp(-((x - 0.15) / 0.35) ** 2) + 0.18 * np.exp(-((x + 0.55) / 0.12) ** 2)
    perfil = perfil - 0.25 * (np.abs(x) > 0.9)
    y = np.linspace(0, 1, largo)[:, None]
    ondas = 1 + 0.10 * np.sin(y * 9 + seed) * np.cos(x[None, :] * 2)
    k = (perfil[None, :] * ondas)[..., None]
    arr = ROJO_CINTA * k
    # brillo especular
    arr += (np.clip(k - 0.95, 0, 1) * 420)
    trama = (np.sin((np.arange(largo)[:, None] + np.arange(ancho)[None, :]) * 1.7) * 3)[..., None]
    arr = np.clip(arr + trama, 0, 255)
    img = Image.fromarray(arr.astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.line([(1, 0), (1, largo)], fill=(140, 10, 20, 255), width=2)
    d.line([(ancho - 2, 0), (ancho - 2, largo)], fill=(140, 10, 20, 255), width=2)
    return img


def cinta(lienzo, p0, p1, ancho=84, seed=0):
    """Cinta recta desde p0 (arriba) hasta p1."""
    (x0, y0), (x1, y1) = p0, p1
    L = int(math.hypot(x1 - x0, y1 - y0)) + 4
    tex = raso(ancho, L, seed)
    ang = math.degrees(math.atan2(x1 - x0, y1 - y0))
    rot = tex.rotate(ang, resample=Image.BICUBIC, expand=True)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    lienzo.alpha_composite(rot, (int(cx - rot.width / 2), int(cy - rot.height / 2)))


def forma_raso(mascara, seed=0, oscuro_centro=None):
    """Rellena una máscara con raso (para los lazos del moño)."""
    w, h = mascara.size
    tex = raso(max(w, h) * 2, max(w, h) * 2, seed).rotate(35 + seed * 20, resample=Image.BICUBIC)
    tex = tex.crop(((tex.width - w) // 2, (tex.height - h) // 2, (tex.width - w) // 2 + w, (tex.height - h) // 2 + h))
    tex.putalpha(mascara)
    return tex


def tira(ancho, largo, seed, vcut=True):
    t = raso(int(ancho), int(largo), seed)
    if vcut:
        m = Image.new("L", t.size, 255)
        ImageDraw.Draw(m).polygon([(0, largo), (ancho / 2, largo - ancho * 0.45), (ancho, largo)], fill=0)
        t.putalpha(ImageChops.multiply(t.getchannel("A"), m))
    return t


def moño(escala=1.0, seed=0):
    """Moño de raso: dos lazos, dos colas con corte en V y nudo. Devuelve (imagen, punto del nudo)."""
    s = escala
    W2, H2 = int(620 * s), int(560 * s)
    out = capa(W2, H2)
    kx, ky = W2 / 2, H2 * 0.30
    rw = 84 * s
    capas = []
    # colas: tiras de cinta que caen en diagonal
    for lado, ang, largo in ((-1, -24, 300 * s), (1, 30, 270 * s)):
        t = tira(rw * 0.92, largo, seed + (lado > 0))
        r = t.rotate(ang, resample=Image.BICUBIC, expand=True)
        # el extremo superior queda en el nudo
        dx = math.sin(math.radians(ang)) * largo / 2
        dy = math.cos(math.radians(ang)) * largo / 2
        l = capa(W2, H2); l.alpha_composite(r, (int(kx + dx - r.width / 2), int(ky + dy - r.height / 2)))
        capas.append(l)
    # lazos: lágrimas que nacen del nudo, rellenas de raso en sentido horizontal
    for lado in (-1, 1):
        m = Image.new("L", (W2, H2), 0)
        pts = []
        L, A = 250 * s, 128 * s
        for t in np.linspace(0, 2 * math.pi, 120):
            u = (1 - math.cos(t)) / 2              # 0 en el nudo, 1 en la punta
            x = L * u
            y = A / 2 * math.sin(t) * (0.25 + 0.75 * u ** 0.6) - 70 * s * u ** 1.3
            pts.append((kx + lado * (x + 10 * s), ky + y))
        ImageDraw.Draw(m).polygon(pts, fill=255)
        tex = raso(int(A * 1.6), int(L * 2.2), seed + 3 + lado).rotate(90 + lado * 12, resample=Image.BICUBIC, expand=True)
        full = capa(W2, H2); full.alpha_composite(tex, (int(kx + lado * L / 2 - tex.width / 2), int(ky - 35 * s - tex.height / 2)))
        full.putalpha(ImageChops.multiply(full.getchannel("A"), m))
        # sombreado: oscuro cerca del nudo y en el hueco interior, brillo arriba
        yy, xx = np.mgrid[0:H2, 0:W2].astype(np.float32)
        u = np.clip(lado * (xx - kx) / L, 0, 1)
        osc = 0.55 * np.clip(1 - u * 2.2, 0, 1)
        hueco = np.exp(-(((xx - (kx + lado * L * 0.42)) / (L * 0.22)) ** 2 + ((yy - (ky - 40 * s)) / (A * 0.18)) ** 2))
        arr = np.asarray(full, np.float32)
        f = (1 - osc - 0.45 * hueco)[..., None]
        arr[..., :3] = np.clip(arr[..., :3] * f, 0, 255)
        capas.append(Image.fromarray(arr.astype(np.uint8)))
    # sombras internas y armado
    for l in capas:
        sh = Image.new("RGBA", (W2, H2), (40, 0, 5, 255)); sh.putalpha(l.getchannel("A").point(lambda v: int(v * 0.55)))
        out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9 * s)), (int(4 * s), int(9 * s)))
        out.alpha_composite(l)
    # nudo
    m = Image.new("L", (W2, H2), 0)
    ImageDraw.Draw(m).rounded_rectangle([kx - 40 * s, ky - 40 * s, kx + 40 * s, ky + 36 * s], int(18 * s), fill=255)
    nudo = capa(W2, H2); tex = raso(int(90 * s), int(90 * s), seed + 9)
    nudo.alpha_composite(tex, (int(kx - 45 * s), int(ky - 45 * s))); nudo.putalpha(ImageChops.multiply(nudo.getchannel("A"), m))
    sh = Image.new("RGBA", (W2, H2), (40, 0, 5, 255)); sh.putalpha(m.point(lambda v: int(v * 0.6)))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8 * s)), (0, int(5 * s)))
    out.alpha_composite(nudo)
    return out, (kx, ky)


def sombra_pared(lienzo, escena, dx=-190, dy=150, escala=1.12, fuerza=0.55):
    """Sombra proyectada en la pared; repite la fila de arriba para que la cinta no se corte."""
    a = np.asarray(escena.getchannel("A"), np.float32) * fuerza
    PAD = 500
    ext = np.vstack([np.repeat(a[0:1], PAD, 0), a]).astype(np.uint8)
    m = Image.fromarray(ext).resize((int(W * escala), int((H + PAD) * escala)), Image.BICUBIC)
    sh = Image.new("RGBA", m.size, (45, 0, 6, 255)); sh.putalpha(m)
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    ox = int(-(escala - 1) * W / 2 + dx); oy = int(-PAD * escala - (escala - 1) * H / 2 + dy)
    tmp = capa(); tmp.paste(sh, (ox, oy), sh)
    lienzo.alpha_composite(tmp)


# ---------------- producto colgado ----------------
def colgar(lienzo, prod, cx, cy, alto, ang=-7, con_moño=True, x_cinta=None, seed=0, ancla_y=0.0, escala_moño=0.85):
    """Cuelga el producto: cinta desde arriba hasta su parte superior, moño en el cuello y sombra en la pared."""
    p = prod.resize((int(prod.width * alto / prod.height), alto), Image.LANCZOS)
    p = p.rotate(ang, resample=Image.BICUBIC, expand=True)
    px, py = int(cx - p.width / 2), int(cy - p.height / 2)
    a = np.asarray(p.getchannel("A"))
    filas = np.where(a.max(1) > 120)[0]
    ytop = filas[0] + int(ancla_y * p.height)
    cols = np.where(a[min(ytop + 6, a.shape[0] - 1)] > 120)[0]
    xtop = px + (cols.mean() if len(cols) else p.width / 2)
    ytop = py + ytop
    xc = x_cinta if x_cinta is not None else xtop + 30
    escena = capa()
    cinta(escena, (xc, -420), (xtop, ytop + 20), seed=seed)
    escena.alpha_composite(p, (px, py))
    if con_moño:
        m, (kx, ky) = moño(escala_moño * alto / 560, seed)
        escena.alpha_composite(m, (int(xtop - kx), int(ytop + 10 - ky)))
    # sombra proyectada en la pared (abajo a la izquierda, grande y suave)
    sombra_pared(lienzo, escena)
    # sombra de contacto suave detrás del frasco
    lienzo.alpha_composite(escena)


# ---------------- texto ----------------
def texto(img, cx, y, t, f, color=BLANCO, esp=0, alfa=255, sombra=True):
    ft = ["lnum"]
    d0 = ImageDraw.Draw(img)
    tw = sum(d0.textlength(ch, font=f, features=ft) for ch in t) + esp * (len(t) - 1) if esp else d0.textlength(t, font=f, features=ft)
    x0 = cx - tw / 2
    def dib(dd, col):
        x = x0
        if esp:
            for ch in t:
                dd.text((x, y), ch, font=f, fill=col, features=ft); x += dd.textlength(ch, font=f, features=ft) + esp
        else:
            dd.text((x, y), t, font=f, fill=col, features=ft)
    if sombra:
        s = capa(); dib(ImageDraw.Draw(s), (50, 0, 6, 120)); img.alpha_composite(s.filter(ImageFilter.GaussianBlur(6)))
    l = capa(); dib(ImageDraw.Draw(l), color + (alfa,)); img.alpha_composite(l)
    return tw


def ajustar_serif(img, t, tam, maxw, peso=500, esp_rel=0.04):
    d = ImageDraw.Draw(img)
    while True:
        f = serif(tam, peso); esp = tam * esp_rel
        tw = sum(d.textlength(ch, font=f) for ch in t) + esp * (len(t) - 1)
        if tw <= maxw or tam < 40: return f, esp
        tam -= 4


def logo(img, y, ancho=170, alfa=235):
    m = Image.open(SK + "logo_texto_mascara.png").convert("L")
    m = m.resize((ancho, int(m.height * ancho / m.width)), Image.LANCZOS).point(lambda v: int(v * alfa / 255))
    img.paste(Image.new("RGBA", m.size, BLANCO + (255,)), ((W - ancho) // 2, y), m)


def gs(v):
    return "Gs. " + f"{v:,}".replace(",", ".")


def linea(img, y, ancho=60):
    ImageDraw.Draw(img).line([(W / 2 - ancho, y), (W / 2 + ancho, y)], fill=(255, 255, 255, 170), width=2)


def encabezado(img, chico, grande, y=118):
    texto(img, W / 2, y, chico, poppins("Regular", 27), BLANCO, esp=9)
    f, esp = ajustar_serif(img, grande, 118, 940)
    texto(img, W / 2, y + 30, grande, f, BLANCO, esp=esp)


def precio(img, contado, cuota, y=1090):
    texto(img, W / 2, y, gs(contado), serif(76, 600), BLANCO, esp=2)
    texto(img, W / 2, y + 92, "CONTADO", poppins("Regular", 21), CREMA, esp=8, alfa=220)
    linea(img, y + 136, 40)
    texto(img, W / 2, y + 152, "O 2 CUOTAS DE " + gs(cuota).upper(), poppins("Regular", 27), BLANCO, esp=4)


# ---------------- datos ----------------
PERFUMES = [
    {"id": "paradoxe", "marca": "PRADA", "nombre": "PARADOXE", "detalle": "EAU DE PARFUM · 100 ML",
     "contado": 820000, "cuota": 451000, "alto": 470, "ang": -4, "moño": True},
    {"id": "missdior", "marca": "DIOR", "nombre": "MISS DIOR", "detalle": "EAU DE PARFUM · 100 ML",
     "contado": 925000, "cuota": 508750, "alto": 540, "ang": -6, "moño": False},
    {"id": "delina", "marca": "PARFUMS DE MARLY", "nombre": "DELINA EXCLUSIF", "detalle": "PARFUM · 75 ML",
     "contado": 1749000, "cuota": 961950, "alto": 530, "cy": 720, "ang": -6, "moño": True},
]
extra = os.path.join(AQUI, "perfumes_extra.json")
if os.path.exists(extra):
    PERFUMES += json.load(open(extra))


def cargar(pid):
    return Image.open(os.path.join(AQUI, f"cut/{pid}.png")).convert("RGBA")


# ---------------- láminas ----------------
def portada():
    img = fondo(1)
    sel = PERFUMES[:3]
    pos = [(215, 640, 330, -8), (865, 700, 360, 6), (535, 830, 390, -4)]
    orden = [1, 2, 0]
    for (cx, cy, alto, ang), i in zip(pos, orden):
        pr = sel[i]
        colgar(img, cargar(pr["id"]), cx, cy, int(alto * pr["alto"] / 560), ang=ang, con_moño=pr["moño"], x_cinta=cx + 10, seed=i, escala_moño=0.95)
    encabezado(img, "NAVIDAD 2026", "PARA REGALAR")
    texto(img, W / 2, 1150, "PRECIOS AL CONTADO Y EN 2 CUOTAS", poppins("Regular", 27), BLANCO, esp=5)
    tw = texto(img, W / 2 - 30, 1210, "DESLIZÁ", poppins("Regular", 23), CREMA, esp=8, alfa=220)
    d = ImageDraw.Draw(img); ax = W / 2 - 30 + tw / 2 + 22; ay = 1226
    d.line([(ax, ay), (ax + 40, ay)], fill=CREMA + (220,), width=2)
    d.line([(ax + 30, ay - 8), (ax + 40, ay), (ax + 30, ay + 8)], fill=CREMA + (220,), width=2)
    logo(img, 1268, 150)
    return img


def lamina(p, seed):
    img = fondo(seed, luz=(0.7 if seed % 2 else 0.32, 0.3))
    colgar(img, cargar(p["id"]), W / 2 + 10, p.get("cy", 650), p["alto"], ang=p["ang"], con_moño=p["moño"], x_cinta=W / 2 + 40, seed=seed)
    encabezado(img, p["marca"], p["nombre"])
    texto(img, W / 2, 290, p["detalle"], poppins("Regular", 23), CREMA, esp=6, alfa=220)
    precio(img, p["contado"], p["cuota"], y=1040)
    logo(img, 1276, 140)
    return img


def cierre():
    img = fondo(77, luz=(0.5, 0.35))
    # solo la cinta con el moño, como un regalo esperando
    escena = capa()
    cinta(escena, (W / 2 + 30, -420), (W / 2, 600), seed=3)
    m, (kx, ky) = moño(1.25, 3)
    escena.alpha_composite(m, (int(W / 2 - kx), int(600 - ky)))
    sombra_pared(img, escena, dx=-170, dy=140, escala=1.0, fuerza=0.5)
    img.alpha_composite(escena)
    texto(img, W / 2, 118, "TU REGALO TE ESPERA", poppins("Regular", 27), BLANCO, esp=9)
    f, esp = ajustar_serif(img, "PEDÍ EL TUYO", 118, 940)
    texto(img, W / 2, 148, "PEDÍ EL TUYO", f, BLANCO, esp=esp)
    texto(img, W / 2, 960, "WHATSAPP", poppins("Regular", 23), CREMA, esp=8, alfa=220)
    texto(img, W / 2, 995, "0972 736 002", serif(84, 600), BLANCO, esp=3)
    linea(img, 1108, 40)
    texto(img, W / 2, 1130, "O EN EL LINK DE LA BIO", poppins("Regular", 27), BLANCO, esp=5)
    texto(img, W / 2, 1190, "100% ORIGINAL  ·  ENVÍOS A TODO PARAGUAY", poppins("Regular", 21), CREMA, esp=4, alfa=220)
    logo(img, 1268, 150)
    return img


if __name__ == "__main__":
    import sys
    os.makedirs(SALIDA, exist_ok=True)
    for f in os.listdir(SALIDA):
        os.remove(os.path.join(SALIDA, f))
    slides = [portada()] + [lamina(p, 200 + i) for i, p in enumerate(PERFUMES)] + [cierre()]
    for i, s in enumerate(slides, 1):
        s.convert("RGB").save(f"{SALIDA}/{i}.png")
    print(len(slides), "slides")
