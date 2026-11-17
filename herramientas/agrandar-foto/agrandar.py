#!/usr/bin/env python3
"""
Agranda x4 una foto de producto chica (por ejemplo, una de 500 px bajada de internet)
para que se vea nítida en un post o una historia.

Uso:
    python3 herramientas/agrandar-foto/agrandar.py foto.jpg foto-x4.png

Usa el modelo EDSR de OpenCV (dnn_superres). La primera vez instalá OpenCV con
`pip install opencv-contrib-python-headless` (agregá --break-system-packages si lo
pide); el modelo (38 MB) se baja solo a ~/.cache/larese/. Antes de agrandar limpia
un poco los artefactos del JPEG y al final le da un toque de nitidez.
Tarda alrededor de un minuto y medio por foto.
"""
import os
import sys
import urllib.request

import cv2
from PIL import Image, ImageFilter

MODELO_URL = "https://raw.githubusercontent.com/Saafke/EDSR_Tensorflow/master/models/EDSR_x4.pb"
MODELO = os.path.expanduser("~/.cache/larese/EDSR_x4.pb")


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    entrada, salida = sys.argv[1:3]
    if not os.path.exists(MODELO):
        os.makedirs(os.path.dirname(MODELO), exist_ok=True)
        print("Bajando el modelo EDSR (38 MB)...")
        urllib.request.urlretrieve(MODELO_URL, MODELO)
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(MODELO)
    sr.setModel("edsr", 4)
    im = cv2.imread(entrada, cv2.IMREAD_COLOR)
    if im is None:
        raise SystemExit(f"No pude abrir {entrada}")
    im = cv2.fastNlMeansDenoisingColored(im, None, 3, 3, 7, 21)
    grande = sr.upsample(im)
    rgb = Image.fromarray(cv2.cvtColor(grande, cv2.COLOR_BGR2RGB))
    rgb.filter(ImageFilter.UnsharpMask(radius=3, percent=70, threshold=2)).save(salida)
    print(salida, rgb.size)


if __name__ == "__main__":
    main()
