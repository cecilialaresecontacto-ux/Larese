#!/usr/bin/env python3
"""
Arma plan-revivir-instagram.pdf a partir de PLAN.md, con la paleta y las letras de marca
y una página con las piezas en miniatura.

Uso:
    python3 crear_pdf.py

Necesita: pip install markdown, y Playwright con Chromium (ya instalado en el entorno).
"""
import os
import subprocess
import tempfile

import markdown
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES = os.path.join(AQUI, "..", "herramientas", "pieza-marca", "assets", "fonts")
LOGO = os.path.join(AQUI, "..", "herramientas", "pieza-marca", "assets", "logo_texto_mascara.png")
SALIDA = os.path.join(AQUI, "plan-revivir-instagram.pdf")

PIEZAS = [
    ("h01-libre-o-coco.png", "h01 · Encuesta"),
    ("h02-miss-dior-o-born-in-roma.png", "h02 · Encuesta"),
    ("h03-devotion-o-divine.png", "h03 · Encuesta"),
    ("h04-quiz-lavanda.png", "h04 · Quiz"),
    ("h05-slider-dulces.png", "h05 · Slider"),
    ("h06-preguntas.png", "h06 · Preguntas"),
    ("h07-notificaciones.png", "h07 · Notificaciones"),
    ("h08-mejores-amigos.png", "h08 · Mejores Amigos"),
    ("h09-comunidad.png", "h09 · Comunidad"),
    ("post-comenta-perfume.png", "Post · Comentá"),
    ("post-comunidad.png", "Post · Comunidad"),
    ("portada-reel-3-perfumes.png", "Portada del reel 1"),
]


def main():
    # logo en color tinta (el archivo de la marca es una máscara en grises)
    m = Image.open(LOGO).convert("L")
    logo = Image.new("RGBA", m.size, (50, 25, 24, 0))
    logo.putalpha(m)
    logo_png = os.path.join(tempfile.gettempdir(), "larese-logo-tinta.png")
    logo.save(logo_png)

    texto = open(os.path.join(AQUI, "PLAN.md"), encoding="utf-8").read()
    # la parte técnica (cómo regenerar) no va en el PDF
    texto = texto.split("## Para volver a generar las piezas")[0].rstrip().rstrip("-").rstrip()
    titulo, cuerpo = texto.split("\n", 1)
    html_cuerpo = markdown.markdown(cuerpo, extensions=["tables", "fenced_code"])

    piezas = "".join(
        f'<figure><img src="file://{os.path.join(AQUI, "piezas", f)}"><figcaption>{c}</figcaption></figure>'
        for f, c in PIEZAS if os.path.exists(os.path.join(AQUI, "piezas", f))
    )

    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><style>
@font-face {{ font-family: Cormorant; src: url(file://{FUENTES}/CormorantGaramond.ttf); font-weight: 300 700; }}
@font-face {{ font-family: Poppins; src: url(file://{FUENTES}/Poppins-Regular.ttf); font-weight: 400; }}
@font-face {{ font-family: Poppins; src: url(file://{FUENTES}/Poppins-Medium.ttf); font-weight: 500; }}
@font-face {{ font-family: Poppins; src: url(file://{FUENTES}/Poppins-SemiBold.ttf); font-weight: 600; }}
@font-face {{ font-family: Pinyon; src: url(file://{FUENTES}/PinyonScript-Regular.ttf); }}
@page {{ size: A4; margin: 18mm 16mm; }}
:root {{ --tinta:#321918; --malva:#7B5B5B; --dorado:#997957; --bordo:#41030B; --marfil:#FCE5DA; }}
body {{ background:#fff; color:var(--tinta); font-family:Poppins; font-size:10.5pt; line-height:1.55; margin:0; }}
.portada {{ text-align:center; padding:8mm 0 4mm; }}
.logo {{ width:52mm; margin:0 auto 6mm; display:block; }}
.portada .eti {{ color:var(--dorado); letter-spacing:.32em; font-size:9pt; text-transform:uppercase; }}
h1 {{ font-family:Cormorant; font-weight:600; text-transform:uppercase; letter-spacing:.06em;
      font-size:28pt; line-height:1.1; margin:3mm 0 1mm; }}
.portada .firma {{ font-family:Pinyon; color:var(--dorado); font-size:22pt; }}
h2 {{ font-family:Cormorant; font-weight:600; text-transform:uppercase; letter-spacing:.06em;
      font-size:17pt; margin:9mm 0 3mm; padding-bottom:2mm; border-bottom:1px solid var(--dorado); break-after:avoid; }}
hr {{ border:0; margin:0; }}
strong {{ font-weight:600; }}
code {{ font-family:Poppins; font-size:8.5pt; color:var(--bordo); background:var(--marfil);
        padding:.3mm 1.6mm; border-radius:2mm; white-space:nowrap; }}
pre {{ background:#faf7f4; border-left:2px solid var(--dorado); padding:3mm 4mm; white-space:pre-wrap;
       font-family:Poppins; font-size:9.5pt; break-inside:avoid; }}
pre code {{ background:none; padding:0; color:var(--tinta); white-space:pre-wrap; }}
table {{ width:100%; border-collapse:collapse; font-size:9.5pt; margin:2mm 0 4mm; }}
th {{ text-align:left; font-weight:500; color:var(--dorado); text-transform:uppercase; letter-spacing:.14em;
      font-size:8pt; border-bottom:1px solid var(--dorado); padding:2mm 2mm; }}
td {{ border-bottom:1px solid #eadfd6; padding:2.2mm 2mm; vertical-align:top; }}
tr {{ break-inside:avoid; }}
blockquote {{ margin:2mm 0 4mm; padding:2mm 4mm; border-left:2px solid var(--dorado); color:var(--malva);
              font-style:normal; break-inside:avoid; }}
ol, ul {{ padding-left:6mm; }}
li {{ margin:1mm 0; }}
.piezas {{ break-before:page; }}
.grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:4mm; }}
figure {{ margin:0; text-align:center; break-inside:avoid; }}
figure img {{ width:100%; border:1px solid #eadfd6; }}
figcaption {{ font-size:7.5pt; color:var(--malva); margin-top:1mm; letter-spacing:.05em; }}
</style></head><body>
<div class="portada">
  <img class="logo" src="file://{logo_png}">
  <div class="eti">Instagram · 16 al 29 de noviembre</div>
  <h1>{titulo.lstrip('# ').strip()}</h1>
  <div class="firma">Larese Store</div>
</div>
{html_cuerpo}
<section class="piezas"><h2>Las piezas</h2><div class="grid">{piezas}</div></section>
</body></html>"""

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as fh:
        fh.write(html)
        ruta_html = fh.name
    js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://{ruta_html}', {{ waitUntil: 'load' }});
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({{ path: {SALIDA!r}, format: 'A4', printBackground: true,
                margin: {{ top: '18mm', bottom: '18mm', left: '16mm', right: '16mm' }} }});
  await b.close();
}})();"""
    subprocess.run(["node", "-e", js], check=True)
    os.unlink(ruta_html)
    print(SALIDA)


if __name__ == "__main__":
    main()
