# Frascos 3D

Render en three.js de los 3 decants de 5 ml (vidrio, líquido de color, virola metálica,
tapa transparente y logo impreso). Para volver a generarlos:

```bash
npm i three@0.180.0
cp ../../../comercial-fragancias/public/marca/logo-negro.png .
cp ../../../herramientas/pieza-fondo-blanco/assets/fonts/Poppins-Bold.ttf .
python3 -m http.server 8765 &
node render.js        # crea render-blanco.png y render-mascara.png
python3 recortar.py   # crea viales.png con fondo transparente
```

Los colores del líquido están en `viales.html` (`colores`).
