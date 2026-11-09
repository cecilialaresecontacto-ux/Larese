"""Arma un reel vertical con el estilo Larese a partir de un plan en JSON.

Uso:
    python armar_reel.py plan.json

Formato del plan (ver SKILL.md para cómo armarlo):
{
  "salida": "reel.mp4",
  "segmentos": [
    {"video": "/ruta/MVI_1040.mov", "ini": 6.2, "fin": 15.0,
     "texto": "Lo que se dice en este tramo, corregido.", "tema_nuevo": false}
  ],
  "titulos": [
    {"segmento": 0, "ancla": "nota de salida", "texto": "Nota de|*salida*"},
    {"segmento": 2, "ancla": "5 a 15", "texto": "de 5 a 15|*minutos*", "pantalla": true}
  ],
  "resaltar": ["salida", "vainilla"],
  "cola": 1.0,          # segundos extra al final (opcional)
  "centro_y": 0.43,     # altura de la cara en el cuadro, 0 arriba 1 abajo (opcional)
  "ding_final": true    # campanita en el último título (opcional)
}

ESTILO "LETRA GIGANTE" (versión del repo): los títulos van en Poppins Black, en
minúscula, con las letras apretadas y en color crema, como en el reel de
referencia ("si sos / fan del / cafe"). En "texto" de un título, "|" separa
renglones y lo que va entre asteriscos sale GIGANTE (la palabra fuerte); el
resto, más chico, alineado a la misma base ("*fan* del"). Un renglón que es solo
una palabra gigante se estira hasta ocupar todo el ancho. Los títulos van
detrás de la persona (la recorta cuadro a cuadro con MediaPipe); con
"pantalla": true, el fondo se desenfoca y el título ocupa toda la pantalla.

Qué hace: corta los silencios (jump cuts), alterna zooms cada ~3 s siempre en
una pausa, agrega logo, subtítulos chicos en Poppins con las palabras clave en
Poppins Black crema, títulos detrás de la persona, sonidos whoosh/pop/ding y normaliza la
voz a -14 LUFS.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import wave

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(AQUI, "..", "assets")
NEGRA = os.path.join(ASSETS, "fonts", "Poppins-Black.ttf")      # títulos y palabras clave
POPM = os.path.join(ASSETS, "fonts", "Poppins-SemiBold.ttf")     # subtítulos
LOGO = os.path.join(ASSETS, "logo_texto_mascara.png")
CACHE = os.path.expanduser("~/.cache/larese-reels")
MODELO_SEG = "https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite"

FPS, W, H = 30, 1080, 1920
ZOOMS = [1.0, 1.16, 1.0, 1.10]
CREMA, BLANCO, NEGRO = (253, 247, 185), (255, 255, 255), (15, 10, 12)
APRIETE = 0.055   # cuánto se juntan las letras de los títulos (fracción del tamaño)
SR = 48000


def sh(*args):
    subprocess.run(list(args), check=True)


def duracion(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                         capture_output=True, text=True).stdout
    return float(out.strip())


# ---------------------------------------------------------------- cortes

def tramos_de_voz(video, a, b, tmp):
    """Tramos con voz entre a y b, con 0.12 s de margen; las pausas largas se cortan.
    Devuelve también la energía del audio (cada 20 ms) para buscar dónde cambiar el zoom."""
    wav = os.path.join(tmp, "v.wav")
    sh("ffmpeg", "-v", "error", "-y", "-ss", f"{a}", "-to", f"{b}", "-i", video, "-vn", "-ac", "1", "-ar", "16000", wav)
    err = subprocess.run(["ffmpeg", "-i", wav, "-af", "silencedetect=noise=-32dB:d=0.32", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    fin = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    d, regs, t = b - a, [], 0.0
    for i, s in enumerate(ini):
        e = fin[i] if i < len(fin) else d
        if s - t > 0.12:
            regs.append([t, s])
        t = e
    if d - t > 0.12:
        regs.append([t, d])
    if not regs:
        regs = [[0, d]]
    with wave.open(wav) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    v = 320  # 20 ms a 16 kHz
    energia = np.sqrt(np.mean(x[: len(x) // v * v].reshape(-1, v) ** 2, axis=1)) if len(x) >= v else np.zeros(1)
    return [[max(0, r[0] - 0.12) + a, min(d, r[1] + 0.12) + a] for r in regs], energia


def puntos_de_zoom(a, b, ini_seg, energia):
    """Dónde cambiar el zoom dentro de un tramo de voz: cada ~3 s, pero siempre en el
    momento más silencioso cercano (una pausa entre palabras), nunca en medio de una."""
    n = max(1, round((b - a) / 3.0))
    cortes = [a]
    for j in range(1, n):
        objetivo = a + j * (b - a) / n
        lo, hi = max(cortes[-1] + 1.2, objetivo - 0.8), min(b - 1.2, objetivo + 0.8)
        if hi <= lo:
            continue
        i0, i1 = int((lo - ini_seg) / 0.02), int((hi - ini_seg) / 0.02)
        tramo = energia[i0:i1]
        if len(tramo) == 0:
            continue
        cortes.append(ini_seg + (i0 + int(np.argmin(tramo))) * 0.02)
    return list(zip(cortes, cortes[1:] + [b]))


def cortar(video, a, d, z, centro_y, destino, fundir_ini=True, fundir_fin=True):
    """Extrae un tramo, lo lleva a 1080x1920 (cubriendo) y aplica el zoom."""
    nf = max(1, round(d * FPS))
    d = nf / FPS
    cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
    cy = int(H * centro_y)
    x, y = (W - cw) // 2, min(max(cy - ch // 2, 0), H - ch)
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"crop={cw}:{ch}:{x}:{y},scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS}")
    # fundido cortito solo en los cortes reales (entre pausas); en los cambios de zoom el audio sigue igual
    af = f"aresample={SR}"
    if fundir_ini:
        af += ",afade=t=in:d=0.015"
    if fundir_fin:
        af += f",afade=t=out:st={max(0, d - 0.025):.3f}:d=0.025"
    sh("ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-i", video, "-frames:v", str(nf), "-t", f"{d:.3f}",
       "-vf", vf, "-af", af, "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-ac", "2", destino)
    return d


# ---------------------------------------------------------------- recorte de persona

class Recorte:
    """Máscara de la persona (MediaPipe selfie multiclass). Si no está disponible,
    los títulos van delante en vez de detrás y el reel se arma igual."""

    def __init__(self):
        self.seg = None
        try:
            import mediapipe as mp
            from mediapipe.tasks import python as mpt
            from mediapipe.tasks.python import vision
            modelo = os.path.join(CACHE, "selfie_multiclass.tflite")
            if not os.path.exists(modelo):
                os.makedirs(CACHE, exist_ok=True)
                urllib.request.urlretrieve(MODELO_SEG, modelo)
            op = vision.ImageSegmenterOptions(base_options=mpt.BaseOptions(model_asset_path=modelo),
                                              output_confidence_masks=True, running_mode=vision.RunningMode.IMAGE)
            self.seg, self.mp = vision.ImageSegmenter.create_from_options(op), mp
        except Exception as e:  # sin mediapipe, sin libEGL o sin red
            print(f"Aviso: sin recorte de persona ({e}). Los títulos van delante.", flush=True)
        self.ultima, self.cuenta = None, 0

    def mascara(self, frame):
        if self.seg is None:
            return None
        # se calcula cada 2 cuadros: la persona se mueve poco y ahorra la mitad del tiempo
        if self.ultima is None or self.cuenta % 2 == 0:
            r = self.seg.segment(self.mp.Image(image_format=self.mp.ImageFormat.SRGB, data=np.ascontiguousarray(frame)))
            m = np.squeeze(np.array(r.confidence_masks[0].numpy_view()))
            m = np.clip((1 - m - 0.35) / 0.4, 0, 1)   # 0 = fondo; se endurece el borde
            img = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))
            self.ultima = img if self.ultima is None else Image.blend(self.ultima, img, 0.7)
        self.cuenta += 1
        return self.ultima

    def cerrar(self):
        if self.seg is not None:
            self.seg.close()
            self.seg = None


# ---------------------------------------------------------------- dibujo

def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def renglones(texto):
    """'Nota de|*salida*' -> [[('Nota de', False)], [('salida', True)]]"""
    out = []
    for r in texto.split("|"):
        partes = re.split(r"(\*[^*]+\*)", r)
        out.append([(p.strip("*"), p.startswith("*")) for p in partes if p.strip()])
    return out


def ancho_apretado(d, txt, f):
    return d.textlength(txt, font=f) - APRIETE * f.size * max(0, len(txt) - 1)


_D = ImageDraw.Draw(Image.new("L", (1, 1)))
_RENGLON = {}


def renglon_mascara(piezas, esp):
    """Máscara (L) de un renglón, letra por letra y apretada, con la base en común.
    Cada letra se dibuja en su propia capa y se combinan con 'lighter' para que donde
    se tocan no queden rayitas. Devuelve (mascara, x_ink, y_tope_ink, y_base)."""
    clave = (tuple((tx, f.size) for tx, f in piezas), round(esp, 1))
    if clave in _RENGLON:
        return _RENGLON[clave]
    grande = max(f.size for _, f in piezas)
    ancho = int(sum(ancho_apretado(_D, tx, f) for tx, f in piezas) + esp * (len(piezas) - 1) + grande)
    alto, base = int(grande * 1.6), int(grande * 1.15)
    m = Image.new("L", (ancho, alto), 0)
    x = grande * 0.5
    for tx, f in piezas:
        for i, ch in enumerate(tx):
            letra = Image.new("L", m.size, 0)
            ImageDraw.Draw(letra).text((x + _D.textlength(tx[:i], font=f) - APRIETE * f.size * i, base), ch,
                                       font=f, fill=255, anchor="ls")
            m = ImageChops.lighter(m, letra)
        x += ancho_apretado(_D, tx, f) + esp
    caja = m.getbbox() or (0, 0, 1, 1)
    res = (m.crop(caja), caja[1], base - caja[1])
    _RENGLON[clave] = res
    return res


def capa_titulo(texto, t, pantalla, cabeza=None):
    """Imagen RGBA del título animado, estilo "letra gigante": Poppins Black en minúscula,
    letras apretadas, color crema plano. Lo que va *entre asteriscos* sale gigante.
    `cabeza` es la fila donde empieza la cabeza; el título se apoya ahí para que ella
    tape solo la parte de abajo del último renglón y la palabra se siga leyendo."""
    chico, grande, maximo = 150, 300, 430
    ANCHO = 1010
    filas = renglones(texto)

    def medir(escala):
        medidas = []
        for fila in filas:
            solo_grande = len(fila) == 1 and fila[0][1]
            piezas = [(txt.lower(), ImageFont.truetype(NEGRA, int((grande if cur else chico) * escala))) for txt, cur in fila]
            esp = lambda ps: 0.22 * min(f.size for _, f in ps)
            ancho = sum(ancho_apretado(_D, tx, f) for tx, f in piezas) + esp(piezas) * (len(piezas) - 1)
            # la palabra gigante sola se estira hasta el ancho; si un renglón no entra, se achica
            if (solo_grande and ancho < ANCHO * escala) or ancho > ANCHO:
                k = ANCHO * (escala if solo_grande and ancho < ANCHO else 1) / ancho
                piezas = [(tx, ImageFont.truetype(NEGRA, max(20, min(int(maximo * escala), int(f.size * k))))) for tx, f in piezas]
            mascara, _, sobre_base = renglon_mascara(piezas, esp(piezas))
            medidas.append((mascara, max(f.size for _, f in piezas)))
        sep = [0.035 * min(a[1], b[1]) for a, b in zip(medidas, medidas[1:])]   # aire entre renglones
        return medidas, sep, sum(m.height for m, _ in medidas) + sum(sep)

    medidas, sep, total = medir(1.0)
    TOPE = 230   # debajo del logo
    if pantalla:
        y = (H - total) / 2 - 80
    elif cabeza is not None:
        # el último renglón se mete ~35% detrás de la cabeza; si la cabeza está muy arriba
        # (por el zoom) y no entra, se achica el título en vez de taparle la palabra
        meter = medidas[-1][0].height * 0.35
        espacio = cabeza + meter - TOPE
        if total > espacio:
            medidas, sep, total = medir(max(0.55, espacio / total))
            meter = medidas[-1][0].height * 0.35
        y = min(max(cabeza - total + meter, TOPE), H * 0.3)
    else:
        y = H * 0.2
    capa = Image.new("L", (W, H), 0)
    for i, (mascara, _) in enumerate(medidas):
        p = ease((t - 0.07 * i) / 0.3)    # cada renglón entra un poquito después
        if p > 0:
            dy = int((1 - p) * 70)
            if p < 1:
                mascara = mascara.point(lambda v, p=p: int(v * p))
            capa.paste(ImageChops.lighter(capa.crop(((W - mascara.width) // 2, int(y) + dy,
                                                     (W - mascara.width) // 2 + mascara.width, int(y) + dy + mascara.height)), mascara),
                       ((W - mascara.width) // 2, int(y) + dy))
        y += mascara.height + (sep[i] if i < len(sep) else 0)
    # sombra muy suave, apenas para que se lea si atrás hay una pared clara
    out = Image.new("RGBA", (W, H), (40, 30, 20, 0))
    out.putalpha(capa.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.30)))
    color = Image.new("RGBA", (W, H), CREMA + (0,))
    color.putalpha(capa)
    out.alpha_composite(color)
    return out


def main():
    plan = json.load(open(sys.argv[1]))
    segs, titulos = plan["segmentos"], plan.get("titulos", [])
    resaltar = {r.lower().strip("¿?¡!.,") for r in plan.get("resaltar", [])}
    centro_y = plan.get("centro_y", 0.43)
    salida = os.path.abspath(plan.get("salida", "reel.mp4"))
    tmp = tempfile.mkdtemp(prefix="reel-")
    try:
        # 1. cortes en silencio y zooms
        lista, mapa, t_out, k = [], [], 0.0, 0
        for si, s in enumerate(segs):
            mapa.append([])
            tramos, energia = tramos_de_voz(s["video"], s["ini"], s["fin"], tmp)
            for a, b in tramos:
                partes = puntos_de_zoom(a, b, s["ini"], energia)
                for j, (c0, c1) in enumerate(partes):
                    p = os.path.join(tmp, f"p{len(lista):03d}.mp4")
                    d = cortar(s["video"], c0, c1 - c0, ZOOMS[k % len(ZOOMS)], centro_y, p,
                               fundir_ini=(j == 0), fundir_fin=(j == len(partes) - 1))
                    lista.append(p)
                    mapa[si].append((t_out, t_out + d))
                    t_out += d
                    k += 1
        habla_fin = t_out
        cola = plan.get("cola", 1.0)
        if cola > 0:   # un poco más del último video (en silencio) para que se lea el cierre
            ult = segs[-1]
            ini_cola = min(ult["fin"] + 0.1, duracion(ult["video"]) - cola)
            p = os.path.join(tmp, f"p{len(lista):03d}.mp4")
            t_out += cortar(ult["video"], max(0, ini_cola), cola, ZOOMS[(k - 1) % len(ZOOMS)], centro_y, p)
            lista.append(p)
        total = t_out
        with open(os.path.join(tmp, "lista.txt"), "w") as f:
            f.write("\n".join(f"file '{p}'" for p in lista))
        base = os.path.join(tmp, "base.mp4")
        sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "lista.txt"), "-c", "copy", base)

        # 2. tiempos (cada palabra en proporción a las letras dentro de la voz del segmento)
        def tiempo_en(si, frac):
            tramos = mapa[si]
            obj = frac * sum(b - a for a, b in tramos)
            for a, b in tramos:
                if obj <= b - a:
                    return a + obj
                obj -= b - a
            return tramos[-1][1]

        subs = []
        for si, s in enumerate(segs):
            pal = s["texto"].split()
            largo_total = sum(len(p) + 1 for p in pal)
            grupos, g = [], []
            for p in pal:
                g.append(p)
                if len(g) == 4 or p[-1] in ".,?!" or sum(len(x) for x in g) > 20:
                    grupos.append(g)
                    g = []
            if g:
                grupos.append(g)
            pos = 0
            for g in grupos:
                lg = sum(len(p) + 1 for p in g)
                subs.append((tiempo_en(si, pos / largo_total), tiempo_en(si, (pos + lg) / largo_total), g))
                pos += lg

        def t_ancla(c):
            txt = segs[c["segmento"]]["texto"]
            idx = max(0, txt.lower().find(c["ancla"].lower()))
            return tiempo_en(c["segmento"], idx / len(txt))

        eventos = []
        for i, c in enumerate(titulos):
            t0 = t_ancla(c)
            ultima = i == len(titulos) - 1
            dur = 1.6 if c.get("pantalla") else 4.5
            sig = t_ancla(titulos[i + 1]) - 0.05 if not ultima else total
            fin = total if ultima else min(sig, t0 + dur, mapa[c["segmento"]][-1][1] + 0.2)
            eventos.append((t0, fin, c["texto"], bool(c.get("pantalla"))))

        # 3. composición cuadro por cuadro: fondo, título (detrás de la persona), persona, subtítulo, logo
        logo = Image.open(LOGO)
        lw = 170
        logo = logo.resize((lw, int(logo.height * lw / logo.width)))
        logo_c = Image.new("RGBA", logo.size, BLANCO + (255,))
        logo_c.putalpha(logo.point(lambda v: int(v * 0.9)))
        fsub, fsub_cur = ImageFont.truetype(POPM, 50), ImageFont.truetype(NEGRA, 56)

        def subtitulo(img, palabras, t):
            d = ImageDraw.Draw(img)
            a = int(255 * ease(t / 0.1))
            piezas = []
            for p in palabras:
                cur = p.lower().strip("¿?¡!.,") in resaltar
                piezas.append((p, cur, fsub_cur if cur else fsub))
            sp = 14
            ancho = sum(d.textlength(p, font=f) for p, c, f in piezas) + sp * (len(piezas) - 1)
            esc = min(1.0, 940 / ancho)
            if esc < 1:
                piezas = [(p, c, ImageFont.truetype(NEGRA if c else POPM, int(f.size * esc))) for p, c, f in piezas]
                ancho = sum(d.textlength(p, font=f) for p, c, f in piezas) + sp * (len(piezas) - 1)
            sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ds = ImageDraw.Draw(sombra)
            x, y = (W - ancho) / 2, 1190
            pos = []
            for p, c, f in piezas:
                dy = -3 if c else 0
                ds.text((x, y + dy), p, font=f, fill=(0, 0, 0, int(a * 0.9)), stroke_width=6, stroke_fill=(0, 0, 0, int(a * 0.9)))
                pos.append((x, y + dy, p, c, f))
                x += d.textlength(p, font=f) + sp
            img.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(7)))
            d = ImageDraw.Draw(img)
            for x, y, p, c, f in pos:
                d.text((x, y), p, font=f, fill=(CREMA if c else BLANCO) + (a,))

        recorte = Recorte()
        lector = subprocess.Popen(["ffmpeg", "-v", "error", "-i", base, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE)
        video_sin_audio = os.path.join(tmp, "video.mp4")
        escritor = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                     "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                                     "-pix_fmt", "yuv420p", video_sin_audio], stdin=subprocess.PIPE)
        def leer_cuadro():
            # un read() sobre un pipe puede devolver menos bytes; se junta hasta tener el cuadro entero
            buf, falta = bytearray(), W * H * 3
            while falta:
                trozo = lector.stdout.read(falta)
                if not trozo:
                    return None
                buf += trozo
                falta -= len(trozo)
            return bytes(buf)

        fi, cabezas = 0, {}
        cortes_plano = sorted(a for tramos in mapa for a, b in tramos)
        while True:
            crudo = leer_cuadro()
            if crudo is None:
                break
            t = fi / FPS
            arr = np.frombuffer(crudo, dtype=np.uint8).reshape(H, W, 3)
            cuadro = Image.fromarray(arr).convert("RGBA")
            activo = next(((a, b, tx, pa) for a, b, tx, pa in eventos if a <= t < b + 0.25), None)
            if activo:
                a, b, tx, pa = activo
                sale = ease((t - b) / 0.25) if t > b else 0.0
                m = None if pa else recorte.mascara(arr)
                # altura de la cabeza: se mide al aparecer el título y otra vez en cada cambio de plano
                # si ella se inclina y la cabeza sube, el título sube suave para no taparse
                clave = (a, sum(1 for c in cortes_plano if c <= t))
                actual = None
                if m is not None:
                    filas = np.where(np.asarray(m)[:, W // 2 - 160: W // 2 + 160].max(axis=1) > 50)[0]   # borde del pelo
                    actual = int(filas[0]) if len(filas) else None
                previa = cabezas.get(clave)
                if previa is None:
                    cabezas[clave] = actual
                elif actual is not None and actual < previa:
                    cabezas[clave] = previa * 0.75 + actual * 0.25
                tit = capa_titulo(tx, t - a, pa, cabezas[clave])
                if sale:
                    tit.putalpha(tit.getchannel("A").point(lambda v: int(v * (1 - sale))))
                if pa:   # pantalla de dato: fondo desenfocado y oscurecido
                    k_pa = ease((t - a) / 0.2) * (1 - sale)
                    borroso = cuadro.filter(ImageFilter.GaussianBlur(28))
                    borroso = Image.blend(borroso, Image.new("RGBA", (W, H), (25, 18, 20, 255)), 0.35)
                    cuadro = Image.blend(cuadro, borroso, k_pa)
                    cuadro.alpha_composite(tit)
                else:    # título detrás de la persona
                    fondo = cuadro.copy()
                    fondo.alpha_composite(tit)
                    cuadro = Image.composite(cuadro, fondo, m) if m is not None else fondo
            if t < habla_fin and not (activo and activo[3]):
                for a, b, g in subs:
                    if a <= t < b:
                        subtitulo(cuadro, g, t - a)
                        break
            cuadro.alpha_composite(logo_c, ((W - lw) // 2, 150))
            escritor.stdin.write(cuadro.convert("RGB").tobytes())
            fi += 1
        escritor.stdin.close()
        escritor.wait()
        lector.wait()
        recorte.cerrar()
        esperado = round(total * FPS)
        if abs(fi - esperado) > 2:
            sys.exit(f"Se procesaron {fi} cuadros y se esperaban {esperado}; revisá los videos de entrada.")

        # 4. sonidos sintetizados
        rng = np.random.default_rng(1)

        def whoosh(d=0.45):
            n = int(SR * d)
            tt = np.arange(n) / SR
            ruido, out, y1, y2 = rng.standard_normal(n), np.zeros(n), 0.0, 0.0
            for i in range(n):   # pasabanda que sube de 300 a 3800 Hz
                th = 2 * np.pi * (300 + 3500 * tt[i] / d) / SR
                y = ruido[i] + 2 * 0.97 * np.cos(th) * y1 - 0.97 ** 2 * y2
                y2, y1, out[i] = y1, y, y
            return out / np.abs(out).max() * np.sin(np.pi * tt / d) ** 2 * 0.35

        def pop(d=0.12):
            tt = np.arange(int(SR * d)) / SR
            return np.sin(2 * np.pi * np.cumsum(900 * np.exp(-tt * 18) + 300) / SR) * np.exp(-tt * 35) * 0.45

        def ding(d=1.2):
            tt = np.arange(int(SR * d)) / SR
            s = sum(a * np.sin(2 * np.pi * f * tt) for f, a in [(1318.5, 1), (2637, 0.4), (3955, 0.2)])
            return s * np.exp(-tt * 4) * 0.25

        pista = np.zeros(int(SR * (total + 2)))

        def poner(son, t):
            i = int(max(0, t) * SR)
            pista[i:i + len(son)] += son[:len(pista) - i]

        for si, s in enumerate(segs):
            if si > 0 and s.get("tema_nuevo"):
                poner(whoosh(), mapa[si][0][0] - 0.22)
        for i, (a, b, tx, pa) in enumerate(eventos):
            if i == len(eventos) - 1 and plan.get("ding_final", True):
                poner(ding(), a)
            else:
                poner(whoosh(0.3) if pa else pop(), a - (0.15 if pa else 0))
        sfx = os.path.join(tmp, "sfx.wav")
        with wave.open(sfx, "w") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((np.clip(pista, -1, 1) * 32767).astype(np.int16).tobytes())

        # 5. mezcla final
        sh("ffmpeg", "-v", "error", "-y", "-i", video_sin_audio, "-i", base, "-i", sfx,
           "-filter_complex",
           # loudnorm sale a 192 kHz: se vuelve a 48 kHz antes de mezclar, si no el reel queda más corto
           "[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[voz];[2:a]aresample=48000,volume=0.8[fx];"
           "[voz][fx]amix=inputs=2:duration=first:normalize=0[a]",
           "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
           "-movflags", "+faststart", salida)
        real = duracion(salida)
        if abs(real - total) > 0.3:
            sys.exit(f"El reel salió de {real:.1f} s y se esperaban {total:.1f} s: algo se cortó en la mezcla.")
        print(f"Reel listo: {salida} ({real:.1f} s)")
    finally:
        if os.environ.get("REEL_DEBUG"):
            print("Archivos intermedios en", tmp)
        else:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
