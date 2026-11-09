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

## Colores de la tienda

Sobre el fondo blanco se usan los colores que eligió la dueña:

- **Negro**: títulos, precio y textos del pie.
- **Deep Blue `#09318D`**: logo, subtítulos, botón e íconos del pie.
- **Ballerina `#EED2E2`**: detalles, como la píldora de la etiqueta y los sellos (texto en Deep Blue encima).
- **White `#FCFFFF`**: el blanco de la paleta. El fondo se deja en blanco puro.

Esta es la paleta **de la tienda** y la herramienta `herramientas/pieza-fondo-blanco` la usa por defecto (`"paleta": "tienda"`).

### Paleta de promos

Para promos, liquidaciones y fechas con urgencia (Black Friday, "últimas horas"), la dueña eligió una segunda paleta. Se activa con `"paleta": "promo"` en el spec:

- **Matte Black `#28282B`**: logo, títulos, precio, botón e íconos.
- **Red Orange `#FF4200`**: píldora de la etiqueta y sellos (texto blanco encima).
- **Off-White `#F9F9F9`** de fondo: la dueña lo aprobó para la paleta de promos. Es un blanco apenas grisado; la paleta de la tienda sigue en blanco puro.
