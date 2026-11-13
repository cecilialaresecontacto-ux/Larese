"""Transcribe videos en español con Whisper (sherpa-onnx), local y sin cuentas.

Uso:
    python transcribir.py salida.json video1.mov video2.mov ...

Por cada video guarda la duración, el texto completo y las frases con su
tiempo de inicio y fin (separadas por las pausas del audio). Esas frases son
las que después se eligen para armar el reel.

La primera vez instala sherpa-onnx con pip y baja el modelo whisper-small
(~640 MB) desde GitHub a ~/.cache/larese-reels. Si GitHub no está disponible,
el script lo avisa y hay que transcribir de otra forma (ver SKILL.md).
"""
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import wave

CACHE = os.path.expanduser("~/.cache/larese-reels")
MODELO = "sherpa-onnx-whisper-small"
URL = f"https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/{MODELO}.tar.bz2"


def preparar_modelo():
    carpeta = os.path.join(CACHE, MODELO)
    if os.path.exists(os.path.join(carpeta, "small-tokens.txt")):
        return carpeta
    os.makedirs(CACHE, exist_ok=True)
    destino = os.path.join(CACHE, MODELO + ".tar.bz2")
    print(f"Bajando modelo de voz ({URL})...", flush=True)
    try:
        urllib.request.urlretrieve(URL, destino)
    except Exception as e:
        sys.exit(f"No se pudo bajar el modelo: {e}. Revisá que github.com esté permitido en la red.")
    with tarfile.open(destino) as t:
        t.extractall(CACHE)
    os.remove(destino)
    return carpeta


def cargar_sherpa():
    try:
        import sherpa_onnx  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "sherpa-onnx", "numpy"], check=True)
    import sherpa_onnx
    return sherpa_onnx


def audio_16k(video, carpeta):
    wav = os.path.join(carpeta, os.path.basename(video) + ".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    return wav


def regiones_de_voz(wav, dur):
    """Complemento de los silencios: tramos donde se habla."""
    err = subprocess.run(["ffmpeg", "-i", wav, "-af", "silencedetect=noise=-32dB:d=0.22", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    fin = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    regs, t = [], 0.0
    for i, s in enumerate(ini):
        if s - t > 0.15:
            regs.append([t, s])
        t = fin[i] if i < len(fin) else dur
    if dur - t > 0.15:
        regs.append([t, dur])
    # junta pausas muy cortas y tramos sueltos de menos de medio segundo
    out = []
    for r in regs:
        if out and (r[0] - out[-1][1] < 0.3 or r[1] - r[0] < 0.5):
            out[-1][1] = r[1]
        else:
            out.append(r)
    return out


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    salida, videos = sys.argv[1], sys.argv[2:]
    import numpy as np
    sherpa_onnx = cargar_sherpa()
    m = preparar_modelo()
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=f"{m}/small-encoder.int8.onnx", decoder=f"{m}/small-decoder.int8.onnx",
        tokens=f"{m}/small-tokens.txt", language="es", task="transcribe", num_threads=4)

    def reconocer(muestras, sr):
        s = rec.create_stream()
        s.accept_waveform(sr, muestras)
        rec.decode_stream(s)
        return s.result.text.strip()

    resultado = []
    with tempfile.TemporaryDirectory() as tmp:
        for v in videos:
            wav = audio_16k(v, tmp)
            with wave.open(wav) as w:
                sr = w.getframerate()
                a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
            dur = len(a) / sr
            frases = []
            for s, e in regiones_de_voz(wav, dur):
                trozo = a[int(max(0, s - 0.08) * sr): int(min(dur, e + 0.08) * sr)]
                frases.append({"ini": round(s, 2), "fin": round(e, 2), "texto": reconocer(trozo, sr)})
            resultado.append({"video": os.path.abspath(v), "duracion": round(dur, 2),
                              "texto": reconocer(a, sr) if dur <= 30 else " ".join(f["texto"] for f in frases),
                              "frases": frases})
            print(f"{os.path.basename(v)} ({dur:.1f}s): {resultado[-1]['texto']}", flush=True)
    with open(salida, "w") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=1)
    print(f"Transcripción guardada en {salida}")


if __name__ == "__main__":
    main()
