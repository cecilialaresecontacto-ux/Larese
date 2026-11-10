"""Sello '+1 decant de 5 ml de REGALO' con REGALO grande.
Uso: python3 sello_regalo.py entrada.png salida.png cx cy radio carpeta_fuentes [tienda|promo] ["línea 1|línea 2|PALABRA GRANDE"]"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
src, out, cx, cy, r, fonts = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
paleta = sys.argv[7] if len(sys.argv) > 7 else "tienda"
l1, l2, l3 = (sys.argv[8] if len(sys.argv) > 8 else "+1 decant|de 5 ml de|REGALO").split("|")
FONDO_SELLO, TEXTO_SELLO = {"tienda": ((238, 210, 226), (9, 49, 141)),
                            "promo": ((255, 66, 0), (255, 255, 255))}[paleta]
img = Image.open(src).convert("RGBA")
sh = Image.new("L", img.size, 0)
ImageDraw.Draw(sh).ellipse((cx-r, cy-r+10, cx+r, cy+r+10), fill=110)
sh = sh.filter(ImageFilter.GaussianBlur(16))
img.alpha_composite(Image.merge("RGBA", [Image.new("L", img.size, 0)]*3 + [sh]))
d = ImageDraw.Draw(img)
d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=FONDO_SELLO)
def fit(text, weight, max_w, start):
    s = start
    while True:
        f = ImageFont.truetype(f"{fonts}/Poppins-{weight}.ttf", s)
        if d.textlength(text, font=f) <= max_w or s < 10: return f
        s -= 1
small1 = fit(l1, "SemiBold", r*1.3, int(r*0.23))
small2 = fit(l2, "SemiBold", r*1.45, small1.size)
small1 = small2 = min(small1, small2, key=lambda f: f.size)
big = fit(l3, "ExtraBold", r*1.5, int(r*0.5))
lines = [(l1, small1), (l2, small2), (l3, big)]
hs = [f.getbbox(t)[3]-f.getbbox(t)[1] for t, f in lines]
gap = r*0.08
y = cy - (sum(hs) + gap*2)/2
for (t, f), h in zip(lines, hs):
    bb = f.getbbox(t)
    d.text((cx - d.textlength(t, font=f)/2, y - bb[1]), t, font=f, fill=TEXTO_SELLO)
    y += h + gap
img.convert("RGB").save(out)
