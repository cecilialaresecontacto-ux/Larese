# Arma viales.png (fondo transparente) a partir de los dos renders de render.js:
# render-blanco.png (la escena sobre blanco) y render-mascara.png (silueta blanca sobre negro).
import numpy as np
from PIL import Image, ImageFilter
wr = np.asarray(Image.open('render-blanco.png').convert('RGB')).astype(float) / 255
m = np.asarray(Image.open('render-mascara.png').convert('L').filter(ImageFilter.MaxFilter(3))).astype(float) / 255
sombra = np.clip(1 - wr.mean(axis=2), 0, 1) * (1 - m)
alpha = np.clip(m + sombra, 0, 1)
rgb = np.where(m[..., None] > 0, wr * m[..., None] / np.maximum(alpha[..., None], 1e-4), 0)
im = Image.fromarray((np.dstack([np.clip(rgb, 0, 1), alpha]) * 255).round().astype('uint8'), 'RGBA')
im.crop(im.getchannel('A').point(lambda v: 255 if v > 4 else 0).getbbox()).save('viales.png')
