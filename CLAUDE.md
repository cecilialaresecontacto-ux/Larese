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
