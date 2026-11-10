# Video: trío de diseñador para él

Video vertical (1080×1920, 14 s, 30 fps) para Reels, historias y anuncios: 3 decants de 5 ml
(Acqua di Giò Profondo, Born in Roma Intense y Le Beau) a Gs. 180.000. Colores: solo blanco y negro
(solo blanco y negro). Hecho con [Remotion](https://www.remotion.dev), a partir de `comercial-fragancias`.

## Uso

```console
npm i
npm run dev                                                   # editor visual
npx remotion render TrioHombre out/video-trio-hombre.mp4 \
  --browser-executable=/opt/pw-browsers/chromium            # exporta el MP4
```

El MP4 terminado está en `../anuncio-trio-hombre/video-trio-hombre.mp4`.

## Qué editar

- **Precio y texto del botón:** `src/Root.tsx`.
- **Perfumes, marcas y descripciones:** `src/fragancias.ts`.
- **Colores:** `src/marca.ts`.
- **Duración de cada escena:** constantes al principio de `src/Comercial.tsx`.
