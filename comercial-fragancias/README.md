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

- **Nombre de la tienda y texto del botón final:** `src/Root.tsx` (`tienda` y `llamado`).
  También se pueden cambiar desde el panel de props del editor.
- **Nombres, notas y colores de cada fragancia:** `src/fragancias.ts`.
- **Duración de cada escena:** constantes al principio de `src/Comercial.tsx`.
- **Fotos de las botellas (PNG sin fondo):** `public/`.

## Licencia

Remotion requiere licencia de empresa para algunas organizaciones.
[Ver condiciones](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md).
