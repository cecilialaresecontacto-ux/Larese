"""Deja una foto de producto en fondo blanco puro, centrada y con margen parejo.
Uso: python3 fondo_blanco.py entrada salida.jpg
Imprime 'OK' o 'REVISAR <motivo>' si el fondo no es claro (foto real con ambiente)."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

W, H = 1000, 1250          # proporción vertical 4:5, igual que las tarjetas de la tienda
MAX_W, MAX_H = 0.80, 0.78  # cuánto del lienzo ocupa el producto

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src)
if im.mode in ('RGBA', 'LA', 'P'):
    im = im.convert('RGBA')
    base = Image.new('RGBA', im.size, (255, 255, 255, 255))
    base.alpha_composite(im)
    im = base
im = im.convert('RGB')
a = np.asarray(im).astype(np.int16)

# Color del borde: si ya es blanco, no se toca nada del interior (así las cajas blancas no se borran)
perim_px = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
mn = a.min(axis=2); mx = a.max(axis=2)
claro = (mn >= 214) & ((mx - mn) <= 18)
perim = np.concatenate([claro[0], claro[-1], claro[:, 0], claro[:, -1]])
estado = 'OK' if perim.mean() > 0.9 else f'REVISAR borde_claro={perim.mean():.2f}'
out = a.copy()
if np.median(perim_px.min(axis=1)) >= 247:
    casi_blanco = (mn >= 247) & ((mx - mn) <= 6)
    out[casi_blanco] = 255
    fondo = casi_blanco
    producto = ~((mn >= 240) & ((mx - mn) <= 10))
else:
    # fondo gris o de color claro: se reemplaza la zona clara conectada al borde
    lab, _ = ndimage.label(claro)
    borde = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    fondo = np.isin(lab, borde[borde != 0])
    out[fondo] = 255
    cerca = ndimage.binary_dilation(fondo, iterations=1) & ~fondo
    out[cerca] = ((out[cerca] + 255) // 2)
    producto = ~fondo
# ignorar puntitos sueltos al calcular el recorte
producto = ndimage.binary_opening(producto, iterations=2)

ys, xs = np.where(producto)
if len(xs) == 0:
    print('REVISAR vacio'); sys.exit(0)
y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
crop = Image.fromarray(out[y0:y1, x0:x1].astype(np.uint8))
s = min(W * MAX_W / crop.width, H * MAX_H / crop.height)
crop = crop.resize((max(1, round(crop.width * s)), max(1, round(crop.height * s))), Image.LANCZOS)
lienzo = Image.new('RGB', (W, H), (255, 255, 255))
lienzo.paste(crop, ((W - crop.width) // 2, (H - crop.height) // 2))
lienzo.save(dst, quality=92)
print(estado)
