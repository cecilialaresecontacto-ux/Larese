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

## Anuncio estilo Apple

Tercera composición, `AnuncioLarese` (1080×1920, ~16 s): palabras gigantes con
cortes rápidos, el frasco reemplaza una letra ("As▯d.", "Y▯ra."), precios sobre
anillos giratorios, fila de frascos y cierre con el logo.

```console
npx remotion render AnuncioLarese out/anuncio-larese.mp4
```

- **Tomas, palabras y duración de cada una:** `tomas` en `src/anuncio/AnuncioLarese.tsx`.
- **Frascos sin fondo (PNG):** `public/anuncio/` y `src/anuncio/frascos.ts`.

## Flyers estilo pastelería

Un flyer por fragancia (`Flyer-asad`, `Flyer-yara`, …) y un video que los pasa
todos (`FlyersDecants`, ~15 s): fondo pastel de un color, frascos desenfocados
flotando, nombre gigante de fondo y tipografía Montserrat SemiBold con esquinas redondeadas (como "FRAMBUESA" en la referencia).

```console
npx remotion still Flyer-asad out/flyers/flyer-asad.png --frame=95   # imagen
npx remotion render FlyersDecants out/flyers-decants.mp4             # video
```

- **Textos, colores y fotos de cada flyer:** `src/flyer/datos.ts`.

## Remate con el estilo de marca

`RemateLarese` (1080×1920, ~20 s): el anuncio del remate de decants rehecho con el
estilo del skill de anuncios de Larese (Poppins centrada, fondo del color del frasco o gris si es negro, fotos originales,
logo "larese STORE" gigante de fondo, píldora y pie con WhatsApp y envíos).

```console
npx remotion render RemateLarese out/remate-larese.mp4
```

- **Productos, precios y colores:** `src/remateMarca/marca.ts`.

## Licencia

Remotion requiere licencia de empresa para algunas organizaciones.
[Ver condiciones](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md).
