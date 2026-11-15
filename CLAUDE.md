# LARESE STORE: reglas de diseño

## Paleta y tipografía de marca SIEMPRE

Todas las piezas para redes (posts, historias, carruseles, portadas) van con la **paleta y la tipografía de marca**, sin excepción. La dueña lo pidió así (reemplaza a la regla anterior de fondo blanco). Las referencias que mandó están en `herramientas/pieza-marca/paleta-de-marca.png` y `herramientas/pieza-marca/tipografia-de-marca.png`.

### Paleta

| Color | Hex | Uso |
|---|---|---|
| Crema | `#F8F4EB` | Fondo claro principal |
| Bordó vino | `#41030B` | Fondos oscuros, píldoras, botones |
| Bordó cuero | `#2A0B0D` | Sombras y fondos profundos |
| Tinta | `#321918` | Títulos y textos sobre crema |
| Malva | `#7B5B5B` | Textos secundarios sobre crema |
| Rosa marfil | `#FCE5DA` | Textos sobre bordó, arcos |
| Dorado antiguo | `#997957` | Acentos y detalles finos |

### Tipografía

| Fuente | Uso |
|---|---|
| Playfair Display | Títulos, nombres de perfume, precios |
| Playfair Display Italic | Notas y frases cortas |
| Pinyon Script | Acentos: marcas, "Desde", frases |
| Poppins | Textos chicos, etiquetas, botones |

### Cómo generar las piezas

- No uses el script de la skill `larese-anuncios` tal cual (fondo del color del producto y texto blanco), ni el viejo `herramientas/pieza-fondo-blanco`.
- Usá la herramienta de marca del repo:

  ```bash
  python3 herramientas/pieza-marca/scripts/crear_pieza.py spec.json salida.png
  ```

  El spec es el mismo que el de la skill, con estos cambios:
  - `"fondo": "crema"` (por defecto) o `"bordo"` para la versión oscura.
  - `"marca"`: la marca del perfume, va en Pinyon Script (por ejemplo "Carolina Herrera").
  - `"nota"`: frase corta en Playfair italic (por ejemplo "Dulce y seductor").
  - El título no se pasa a mayúsculas: escribilo como querés que se lea.
  - `color` y `categoria` se ignoran.
- **Nada de franjas ni arcos rellenos de rosa detrás del producto:** a la dueña no le gustan. El producto va sobre el fondo, enmarcado solo por un arco de línea dorada fina.
- Para historias con sticker de Instagram (encuesta, quiz, slider, preguntas) usá `revivir-cuenta/crear_interaccion.py`, que tiene el mismo estilo.
- Si armás una pieza a mano o con otra herramienta (Remotion, HTML, etc.), también va con esta paleta y estas fuentes. Están en `herramientas/pieza-marca/assets/fonts`.
