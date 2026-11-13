# LARESE STORE: reglas de diseño

## Fondos permitidos: blanco puro o bordó y crema

Las piezas para redes (posts, historias, carruseles, portadas) usan **solo uno de estos dos estilos**. Nunca el fondo con el color del producto ni otros colores. La dueña lo pidió así.

### 1. Fondo blanco puro (estilo de siempre)

- No uses el script de la skill `larese-anuncios` tal cual: arma el fondo con el color del producto y el texto en blanco.
- Usá la versión de fondo blanco del repo, que tiene el mismo estilo pero con texto negro y grises:

  ```bash
  python3 herramientas/pieza-fondo-blanco/scripts/crear_pieza.py spec.json salida.png
  ```

  El spec es el mismo que el de la skill. Los campos `color` y `categoria` se ignoran, porque el fondo siempre es blanco.

### 2. Bordó y crema (estilo editorial, aprobado en noviembre de 2026)

La dueña eligió esta paleta a partir de una referencia de carrusel editorial. Los colores se sacaron de esa referencia y son la **paleta oficial de la marca**. La muestra está en `marca/paleta.png`.

| Color | Hex | Uso |
|---|---|---|
| Bordó vino | `#41030B` | Fondos oscuros, píldoras, botones |
| Bordó cuero | `#2A0B0D` | Sombras y fondos profundos |
| Tinta | `#321918` | Títulos y textos sobre crema |
| Malva | `#7B5B5B` | Textos secundarios sobre crema |
| Crema | `#F8F4EB` | Fondo claro principal |
| Rosa marfil | `#FCE5DA` | Textos sobre bordó, arcos sobre crema |
| Dorado antiguo | `#997957` | Acentos, líneas finas y textos secundarios sobre bordó |

- Usá solo estos colores. Las slides alternan fondo crema y fondo bordó vino con borde de estampilla.
- Tipografías: títulos en Playfair Display, acentos en cursiva Pinyon Script y textos chicos en Poppins. Están en `herramientas/carrusel-bordo/assets/fonts/`.
- Para carruseles de productos:

  ```bash
  python3 herramientas/carrusel-bordo/scripts/crear_carrusel.py carrusel.json carpeta_salida/
  ```

  Ejemplo de spec: `carrusel-mas-pedidos/carrusel.json`.

### En los dos estilos

- Si armás una pieza a mano o con otra herramienta, usá uno de los dos estilos: fondo blanco con textos oscuros, o bordó y crema.
- Precios y nombres sacados de Shopify, nunca inventados.
