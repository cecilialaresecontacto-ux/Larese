# Video: combo 5 perfumes para él (Gs. 1.350.000)

Video vertical (1080×1920, 16,5 s, 30 fps) para Meta Ads, Reels e historias: Azzaro The Most Wanted Parfum
+ Bharara King + Liquid Brun + Club de Nuit Intense Man + Odyssey Aqua. Solo blanco y negro.
Hecho con [Remotion](https://www.remotion.dev), a partir de `video-trio-hombre`.

## Uso

```console
npm i
npx remotion render Combo5 out/video.mp4 --browser-executable=/opt/pw-browsers/chromium
python3 musica/generar.py musica/pista.wav 16.5          # música propia, sin derechos de terceros
ffmpeg -i out/video.mp4 -i musica/pista.wav -map 0:v -map 1:a -c:v copy -c:a aac -shortest final.mp4
```

El MP4 terminado con música está en `../anuncio-combo-5-1350/video-combo-5-musica.mp4`.

## Qué editar

- **Precio y botón:** `src/Root.tsx`.
- **Perfumes, marcas y descripciones:** `src/fragancias.ts`.
- **Textos de la intro y el final:** `src/escenas/Intro.tsx` y `src/escenas/Final.tsx`.
