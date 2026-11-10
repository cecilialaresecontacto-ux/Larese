"""Genera una pista instrumental propia (sin derechos de terceros) para el video: 14 s,
estilo elegante y moderno (pad suave, bajo, bombo, hi-hat), 100 BPM, en La menor."""
import numpy as np, wave, sys
SR = 44100
DUR = 14.0
BPM = 100
beat = 60 / BPM
n = int(SR * DUR)
t = np.arange(n) / SR
out = np.zeros(n)

def env(length, a=0.01, r=0.3):
    e = np.ones(length)
    na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    nr = min(length, int(r * SR)); e[-nr:] *= np.linspace(1, 0, nr)
    return e

def add(sig, start):
    i = int(start * SR)
    if i >= n: return
    j = min(n, i + len(sig)); out[i:j] += sig[: j - i]

def nota(f): return 440 * 2 ** ((f - 69) / 12)

# acordes: Am - F - C - G (2 compases cada uno = 8 tiempos... aquí 1 compás de 4 tiempos)
acordes = [[57, 60, 64], [53, 57, 60], [48, 52, 55, 60], [55, 59, 62]]
compas = 4 * beat
k = 0
tiempo = 0.0
while tiempo < DUR:
    ac = acordes[k % 4]
    L = int(compas * SR)
    tt = np.arange(L) / SR
    pad = sum(np.sin(2 * np.pi * nota(m) * tt) + 0.3 * np.sin(2 * np.pi * nota(m) * 2.003 * tt) for m in ac)
    pad *= env(L, a=0.4, r=0.6) * 0.06
    add(pad, tiempo)
    # bajo: raíz una octava abajo, en negras
    for b in range(4):
        Lb = int(beat * 0.9 * SR); tb = np.arange(Lb) / SR
        f = nota(ac[0] - 12)
        bajo = (np.sin(2 * np.pi * f * tb) + 0.4 * np.sin(2 * np.pi * 2 * f * tb)) * env(Lb, 0.005, 0.25) * 0.16
        add(bajo, tiempo + b * beat)
    # arpegio suave en corcheas
    for c in range(8):
        Lc = int(beat / 2 * SR); tc = np.arange(Lc) / SR
        m = ac[c % len(ac)] + 12
        arp = np.sin(2 * np.pi * nota(m) * tc) * np.exp(-tc * 9) * 0.05
        add(arp, tiempo + c * beat / 2)
    tiempo += compas; k += 1

# batería desde el segundo 1.5
rng = np.random.default_rng(7)
tb = 1.5
while tb < DUR - 0.5:
    Lk = int(0.35 * SR); tk = np.arange(Lk) / SR
    f = 110 * np.exp(-tk * 18) + 45
    kick = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tk * 9) * 0.5
    add(kick, tb)
    Lh = int(0.06 * SR)
    hat = rng.normal(0, 1, Lh); hat = np.diff(np.concatenate([[0], hat])) * np.exp(-np.arange(Lh) / SR * 70) * 0.05
    add(hat, tb + beat / 2)
    if int(round((tb - 1.5) / beat)) % 2 == 1:
        Ls = int(0.2 * SR); ts = np.arange(Ls) / SR
        clap = rng.normal(0, 1, Ls) * np.exp(-ts * 22) * 0.12
        add(clap, tb)
    tb += beat

# fade in/out y normalizar
fi = int(0.6 * SR); out[:fi] *= np.linspace(0, 1, fi)
fo = int(1.5 * SR); out[-fo:] *= np.linspace(1, 0, fo)
out = out / np.max(np.abs(out)) * 0.85
pcm = (out * 32767).astype(np.int16)
estereo = np.column_stack([pcm, pcm]).ravel()
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(estereo.tobytes())
print("ok", sys.argv[1])
