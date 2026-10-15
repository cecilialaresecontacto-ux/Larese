# Comercial de fragancias

Video vertical (1080×1920, 15 s, 30 fps) para Reels y TikTok con los body mist
shimmer Bare Vanilla, Coconut Passion y Pure Seduction. Hecho con [Remotion](https://www.remotion.dev).

## Uso

```console
npm i
npm run dev                                              # editor visual en el navegador
npx remotion render Comercial out/comercial-fragancias.mp4  # exporta el MP4
```

## Qué editar

- **Usuario y texto del botón final:** `src/Root.tsx` (`usuario` y `llamado`).
  También se pueden cambiar desde el panel de props del editor.
- **Nombres, notas y colores de cada fragancia:** `src/fragancias.ts`.
- **Duración de cada escena:** constantes al principio de `src/Comercial.tsx`.
- **Fotos de las botellas (PNG sin fondo):** `public/`.
- **Logo y colores de la marca:** `public/marca/` y `src/marca.ts`.
- **Tipografía (Poppins):** `public/fuentes/` y `src/fuentes.ts`.

## Licencia

Remotion requiere licencia de empresa para algunas organizaciones.
[Ver condiciones](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md).

## Reel "Armando decants de 3 ml"

Composición `Decants` (1080×1920, ~16 s, 30 fps) con los clips reales de
`public/clips` y el logo de Larese.

```console
npx remotion render Decants out/larese-decants-3ml.mp4
```

- **Textos (gancho, frase, usuario, botón):** `src/Root.tsx` (`propsDecants`).
- **Orden, recorte, velocidad y nombre de cada toma:** `src/decants/tomas.ts`.
