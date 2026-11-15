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
