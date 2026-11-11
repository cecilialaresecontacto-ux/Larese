import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

src = Image.open(sys.argv[1]).convert('RGB')
LOGO = sys.argv[3] if len(sys.argv) > 3 else 'logo-negro.png'
ESC = 2
X0, Y0, X1, Y1 = 186, 60, 318, 572                       # caja del frasco en la foto
foto = src.crop((X0, Y0, X1, Y1)).resize(((X1 - X0) * ESC, (Y1 - Y0) * ESC), Image.LANCZOS)
a = np.asarray(foto).astype(float)
W, H = foto.size

# silueta: por fila, de la primera a la última columna con algo que no es blanco
oscuro = a.min(axis=2) < 236
alfa = np.zeros((H, W), np.uint8)
for y in range(H):
    xs = np.where(oscuro[y])[0]
    if len(xs) > 1:
        alfa[y, xs.min():xs.max() + 1] = 255
alfa_im = Image.fromarray(alfa).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))

# hueco interior del vidrio (coordenadas de la foto original)
IX0, IX1, IY_FONDO = 208, 298, 532
def frasco(color, nivel=0.80):
    iy_tope = 243
    y_liq = IY_FONDO - (IY_FONDO - iy_tope) * nivel
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).rounded_rectangle(
        ((IX0 - X0) * ESC, (y_liq - Y0) * ESC, (IX1 - X0) * ESC, (IY_FONDO - Y0) * ESC),
        radius=8 * ESC, fill=255)
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(1.0))).astype(float)[..., None] / 255
    c = np.array(color, float) / 255
    # degradé: un poco más intenso abajo y en los bordes, más claro en el centro (como líquido de verdad)
    yy, xx = np.mgrid[0:H, 0:W]
    cx = ((IX0 + IX1) / 2 - X0) * ESC
    lado = np.clip(np.abs(xx - cx) / ((IX1 - IX0) / 2 * ESC), 0, 1)[..., None]
    alto = np.clip((yy - (y_liq - Y0) * ESC) / ((IY_FONDO - y_liq) * ESC), 0, 1)[..., None]
    fuerza = 0.80 + 0.20 * lado ** 2 + 0.12 * alto
    tinte = 1 - (1 - c) * np.clip(fuerza, 0, 1.1)
    out = a * (1 - m) + a * tinte * m
    # menisco: línea fina más oscura y un brillo justo debajo
    yl = int((y_liq - Y0) * ESC)
    xa, xb = int((IX0 - X0) * ESC) + 6, int((IX1 - X0) * ESC) - 6
    out[yl:yl + 2, xa:xb] *= (0.82 * c + 0.1)
    out[yl + 2:yl + 5, xa:xb] = out[yl + 2:yl + 5, xa:xb] * 0.6 + 255 * 0.4
    # la base gruesa de vidrio refleja un poco el color del líquido
    mb = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mb).rounded_rectangle(
        ((IX0 - X0) * ESC, (IY_FONDO - Y0) * ESC, (IX1 - X0) * ESC, (553 - Y0) * ESC), radius=6 * ESC, fill=255)
    mb = np.asarray(mb.filter(ImageFilter.GaussianBlur(3))).astype(float)[..., None] / 255 * 0.35
    out = out * (1 - mb) + out * (1 - (1 - c) * 0.9) * mb
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert('RGBA')
    im.putalpha(alfa_im)
    # logo larese impreso en el vidrio, centrado en el cuerpo
    logo = Image.open(LOGO).convert('RGBA')
    ancho = int((IX1 - IX0) * ESC * 0.78)
    logo = logo.resize((ancho, round(logo.height * ancho / logo.width)), Image.LANCZOS)
    la = np.asarray(logo).astype(float)
    la[..., 3] *= 0.92
    logo = Image.fromarray(la.astype(np.uint8))
    lx = int(((IX0 + IX1) / 2 - X0) * ESC - ancho / 2)
    ly = int(((y_liq + IY_FONDO) / 2 - Y0) * ESC - logo.height / 2)
    im.alpha_composite(logo, (lx, ly))
    return im

colores = [(140, 182, 234), (238, 196, 112), (240, 170, 196)]   # azul, ámbar, rosa
frascos = [frasco(c) for c in colores]
sep = int(W * 0.18)
lienzo = Image.new('RGBA', (W * 3 + sep * 2, H), (0, 0, 0, 0))
for i, f in enumerate(frascos):
    lienzo.alpha_composite(f, (i * (W + sep), 0))
lienzo.save(sys.argv[2])
fondo = Image.new('RGBA', lienzo.size, (255, 255, 255, 255)); fondo.alpha_composite(lienzo)
fondo.convert('RGB').save('preview.png')
print(lienzo.size)
