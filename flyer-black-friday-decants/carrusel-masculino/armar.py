#!/usr/bin/env python3
"""Carrusel Black Friday de decants MASCULINOS (19 al 30 de noviembre), mismo diseño que
el carrusel femenino (carrusel/armar_carrusel.py): portada, un slide por perfume y cierre,
en formato publicación (1080x1350) y en formato historia (1080x1920, carpeta historias/).

Van los 6 masculinos de diseñador a Gs. 45.000 (5 ml) y Gs. 90.000 (10 ml), lo confirmó la
dueña el 19/11. Los árabes (más baratos que la promo) y el Initio quedan afuera hasta que
pase sus precios.

Uso: python3 flyer-black-friday-decants/carrusel-masculino/armar.py
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "carrusel"))
import armar_carrusel as ac  # noqa: E402

# nombre, marca, tipo, notas, foto (en carrusel/fotos), color del perfume en el decant
ac.FRAGANCIAS = [
    ("Sauvage", "Dior", "Eau de Parfum",
     "Ambroxan fresco con vainilla y pachulí: amaderado y magnético.", "p-sauvage-x4.png", (196, 214, 234)),
    ("Le Male Le Parfum", "Jean Paul Gaultier", "Le Parfum",
     "Cardamomo especiado, lavanda e iris sobre vainilla. Elegante y carismático.",
     "tarjeta-le-male-le-parfum.png", (228, 182, 110)),
    ("Le Beau", "Jean Paul Gaultier", "Eau de Toilette",
     "Fresco y solar, con un toque de coco y haba tonka.", "m-le-beau-recorte.png", (214, 222, 160)),
    ("Eros Parfum", "Versace", "Parfum",
     "Cítricos y menta sobre un fondo intenso y provocador.", "p-eros-parfum-x4.png", (176, 214, 214)),
    ("Stronger With You Parfum", "Emporio Armani", "Parfum",
     "Fougère cálido y especiado: la versión más intensa de la línea.",
     "p-stronger-with-you-x4.png", (204, 112, 92)),
    ("The Most Wanted Parfum", "Azzaro", "Parfum",
     "Jengibre ardiente, maderas cálidas y un fondo dulce de vainilla.",
     "p-most-wanted2-x4.png", (206, 132, 72)),
]
ac.PORTADA = [f[0] for f in ac.FRAGANCIAS]
ac.SALIDA = AQUI

if __name__ == "__main__":
    ac.main()
