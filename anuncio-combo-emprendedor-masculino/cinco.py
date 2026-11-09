import sys
from PIL import Image, ImageDraw
import numpy as np
d, out = sys.argv[1], sys.argv[2]
def trim(im, thr=238):
    a = np.asarray(im).astype(int); ys, xs = np.where(a.min(axis=2) < thr)
    im = im.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1))
    a = np.asarray(im).copy(); a[a.min(axis=2) >= 246] = 255
    return Image.fromarray(a)
def load(f, box=None, flood=False):
    im = Image.open(f"{d}/{f}").convert("RGB")
    if box: im = im.crop(box)
    if flood:
        w, h = im.size
        for p in [(0,0),(w-1,0),(0,h-1),(w-1,h-1),(w//2,0),(w//2,h-1),(0,h//2),(w-1,h//2)]:
            ImageDraw.floodfill(im, p, (255,255,255), thresh=28)
    return trim(im)
hawas = load("6.jpg", (0, 0, 800, 880))
aqua = load("8.jpg", flood=True)
_a = np.asarray(aqua).astype(int); _sat = _a.max(axis=2) - _a.min(axis=2)
_ys, _xs = np.where(_sat > 60)
aqua = aqua.crop((_xs.min(), _ys.min(), _xs.max()+1, _ys.max()+1))
brun = load("5.jpg")
cdn = load("4.jpg")
tur = load("7.jpg", (568, 0, 900, 900))
H = 1000
def sc(im, h): return im.resize((max(1, round(im.width*h/im.height)), h), Image.LANCZOS)
items = [sc(hawas, int(H*.78)), sc(aqua, int(H*.84)), sc(brun, H), sc(cdn, int(H*.84)), sc(tur, int(H*.78))]
gap = -10
W = sum(i.width for i in items) + gap*(len(items)-1) + 40
canvas = Image.new("RGB", (W, H+20), "white")
x = 20
# draw outer first, center last so it overlaps on top
pos = []
for im in items:
    pos.append(x); x += im.width + gap
order = [0, 4, 1, 3, 2]
for k in order:
    im = items[k]
    a = np.asarray(im); mask = Image.fromarray(((a.min(axis=2) < 250) * 255).astype("uint8"))
    canvas.paste(im, (pos[k], H+10-im.height), mask)
canvas.save(out); print(canvas.size, [i.size for i in items])
