import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
src, out, cx, cy, r, fonts = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
img = Image.open(src).convert("RGBA")
sh = Image.new("L", img.size, 0)
ImageDraw.Draw(sh).ellipse((cx-r, cy-r+10, cx+r, cy+r+10), fill=110)
sh = sh.filter(ImageFilter.GaussianBlur(16))
img.alpha_composite(Image.merge("RGBA", [Image.new("L", img.size, 0)]*3 + [sh]))
d = ImageDraw.Draw(img)
d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=(22,22,22))
def fit(text, weight, max_w, start):
    s = start
    while True:
        f = ImageFont.truetype(f"{fonts}/Poppins-{weight}.ttf", s)
        if d.textlength(text, font=f) <= max_w or s < 10: return f
        s -= 1
small1 = fit("+1 decant", "SemiBold", r*1.25, int(r*0.23))
small2 = fit("de 5 ml de", "SemiBold", r*1.35, small1.size)
big = fit("REGALO", "ExtraBold", r*1.5, int(r*0.5))
lines = [("+1 decant", small1), ("de 5 ml de", small2), ("REGALO", big)]
hs = [f.getbbox(t)[3]-f.getbbox(t)[1] for t, f in lines]
gap = r*0.08
total = sum(hs) + gap*2
y = cy - total/2
for (t, f), h in zip(lines, hs):
    bb = f.getbbox(t)
    d.text((cx - d.textlength(t, font=f)/2, y - bb[1]), t, font=f, fill=(255,255,255))
    y += h + gap
img.convert("RGB").save(out)
