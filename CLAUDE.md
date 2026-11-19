# LARESE STORE: reglas de diseño

## Paleta y tipografía de marca SIEMPRE

Todas las piezas para redes (posts, historias, carruseles, portadas) van con la **paleta y la tipografía de marca**, sin excepción. La dueña lo pidió así (reemplaza a la regla anterior de fondo blanco). Las referencias que mandó están en `herramientas/pieza-marca/paleta-de-marca.png` y `herramientas/pieza-marca/tipografia-de-marca.png`.

### Paleta

| Color | Hex | Uso |
|---|---|---|
| Blanco | `#FFFFFF` | Fondo claro principal (la dueña lo prefiere a la crema `#F8F4EB` de la paleta) |
| Bordó vino | `#41030B` | Fondos oscuros, píldoras, botones |
| Bordó cuero | `#2A0B0D` | Sombras y fondos profundos |
| Tinta | `#321918` | Títulos y textos sobre blanco |
| Malva | `#7B5B5B` | Textos secundarios sobre blanco |
| Rosa marfil | `#FCE5DA` | Textos sobre bordó, arcos |
| Dorado antiguo | `#997957` | Acentos y detalles finos |

### Tipografía

La dueña eligió el estilo del carrusel de Navidad para los títulos (reemplaza a Playfair Display).

| Fuente | Uso |
|---|---|
| Cormorant Garamond | Títulos, nombres de perfume y precios, en MAYÚSCULAS con las letras espaciadas |
| Poppins (Regular) | Etiquetas, frases cortas y textos chicos en MAYÚSCULAS bien espaciadas; botones y pie |
| Pinyon Script | Acentos: marcas, "Desde", frases |

### Lo que más le gusta a la dueña (usalo siempre que se pueda)

- **La marca del perfume en cursiva dorada** (Pinyon Script) debajo del nombre, seguida del detalle en Poppins espaciada: `"marca": "Versace"` + `"nota": "Decant EDT · 5 y 10 ml"`.
- **El precio con "Desde" en cursiva dorada** delante: `"precio_prefijo": "Desde"` cuando hay varios tamaños.
- Ejemplo de referencia: historia de Bright Crystal en fondo bordó, con etiqueta "Fresco y floral", título "Bright Crystal", marca "Versace", nota "Decant EDT · 5 y 10 ml" y "Desde Gs. 45.000".

### Cómo generar las piezas

- No uses el script de la skill `larese-anuncios` tal cual (fondo del color del producto y texto blanco), ni el viejo `herramientas/pieza-fondo-blanco`.
- Usá la herramienta de marca del repo:

  ```bash
  python3 herramientas/pieza-marca/scripts/crear_pieza.py spec.json salida.png
  ```

  El spec es el mismo que el de la skill, con estos cambios:
  - `"fondo": "blanco"` (por defecto) o `"bordo"` (bordó vino) para la versión oscura. **Nunca crema:** la dueña pidió blanco puro en lugar de crema.
  - `"marca"`: la marca del perfume, va en Pinyon Script (por ejemplo "Carolina Herrera").
  - `"nota"`: frase corta, sale en Poppins espaciada en mayúsculas (por ejemplo "Dulce y seductor").
  - El título se pasa solo a mayúsculas en Cormorant Garamond. `"titulos": "playfair"` vuelve al estilo viejo, pero no lo uses salvo que la dueña lo pida.
  - `color` y `categoria` se ignoran.
- **Nada de arcos, franjas ni marcos detrás del producto** (ni rellenos de rosa ni de línea dorada): a la dueña no le gustan. El producto va directo sobre el fondo (blanco o bordó), con una sombra suave. Las fotos que no se pueden recortar van como tarjeta con esquinas redondeadas.
- Para historias con sticker de Instagram (encuesta, quiz, slider, preguntas) usá `revivir-cuenta/crear_interaccion.py`, que tiene el mismo estilo.
- Si armás una pieza a mano o con otra herramienta (Remotion, HTML, etc.), también va con esta paleta y estas fuentes. Están en `herramientas/pieza-marca/assets/fonts`.

## Edición de videos (reels y TikTok)

La dueña eligió un estilo de edición nuevo para **todos** sus videos. Está descrito en `herramientas/estilo-video/README.md`: cortes rápidos que ilustran lo que se dice, texto en el centro palabra por palabra con letras mezcladas (gruesa, a mano, cursiva con serifa) y un color de acento en recuadros, círculos y franjas. Reemplaza al estilo de la skill `larese-reels` (letra blanca + cursiva dorada con brillo neón). Con la paleta de marca, salvo que ella pida otra cosa. Nunca usar cortes de películas o series: solo material propio de la dueña.
