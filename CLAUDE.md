# LARESE STORE: reglas de diseño

## Fondo blanco SIEMPRE

Todas las piezas para redes (posts, historias, carruseles, portadas) van con **fondo blanco puro**, sin excepción. La dueña lo pidió así.

- No uses el script de la skill `larese-anuncios` tal cual: arma el fondo con el color del producto y el texto en blanco.
- Usá la versión de fondo blanco del repo, que tiene el mismo estilo pero con texto negro y grises:

  ```bash
  python3 herramientas/pieza-fondo-blanco/scripts/crear_pieza.py spec.json salida.png
  ```

  El spec es el mismo que el de la skill. Los campos `color` y `categoria` se ignoran, porque el fondo siempre es blanco.
- Si armás una pieza a mano o con otra herramienta, también va con fondo blanco y textos oscuros.

## Reels: tipografía "letra gigante" con Poppins

En los reels que edites (skill `larese-reels`), los títulos grandes van con el estilo del reel de referencia que mandó la dueña ("si sos / fan del / cafe"): **Poppins Black en minúscula, letras apretadas, color crema `#FDF7B9`, sin brillo**, con renglones de distinto tamaño y la palabra fuerte gigante ocupando todo el ancho, pasando detrás de ella.

- No uses el `armar_reel.py` de la skill tal cual: tiene la cursiva dorada con brillo. Usá la versión del repo, que hace todo lo demás igual (cortes en silencio, zooms, recorte de la persona, sonidos, logo):

  ```bash
  python3 herramientas/reels-tipografia/scripts/armar_reel.py plan.json
  ```

  La transcripción sigue siendo con el `transcribir.py` de la skill.
- El plan es el mismo que el de la skill. En `texto` de un título, `|` separa renglones y lo que va `*entre asteriscos*` sale **gigante**; el resto sale más chico, apoyado en la misma base. Patrones que funcionan: `"si sos|*fan* del|*cafe*"`, `"nota de|*salida*"`, `"¿tenés|*dudas?*"`. Una palabra gigante sola en su renglón se estira hasta el ancho de la pantalla, así que conviene que sea corta (4-8 letras).
- Subtítulos chicos en Poppins SemiBold blanco; las palabras de `resaltar` salen en Poppins Black crema (ya no en cursiva).
