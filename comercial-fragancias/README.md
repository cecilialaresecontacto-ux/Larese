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

## Remate de decants

Segunda composición, `RemateDecants` (1080×1920, ~20 s): intro "Remate de decants",
precios (5 ml Gs. 15.000 · 10 ml Gs. 20.000), una escena por fragancia y cierre
"¡Hasta agotar stock!" con el logo de Larese Store.

```console
npx remotion render RemateDecants out/remate-decants.mp4
```

- **Fragancias y precios:** `src/remate/datos.ts`.
- **Fotos:** `public/remate/`.
- **Usuario y texto del botón final:** `propsRemate` en `src/Root.tsx`.

## Licencia

Remotion requiere licencia de empresa para algunas organizaciones.
[Ver condiciones](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md).
