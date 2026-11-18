# LARESE STORE: reglas de diseño

## Paleta y tipografía de marca en TODO

Todas las piezas de la tienda (posts, historias, carruseles, portadas, reels y anuncios de Meta) usan la **paleta y la tipografía de marca**. La dueña lo pidió en noviembre de 2026, lo confirmó el 17 de noviembre ("usá siempre eso") y lo volvió a pedir el 18 para el flyer de Black Friday. Las láminas están en `marca/paleta.png` y `marca/tipografia.png`.

El fondo blanco puro (estilo anterior) se usa **solo si la dueña lo pide** para una pieza puntual. Nunca uses el fondo con el color del producto ni colores fuera de la paleta.

### Paleta

| Color | Hex | Uso |
|---|---|---|
| Bordó vino | `#41030B` | Fondos oscuros, píldoras, botones, logo sobre fondo claro |
| Bordó cuero | `#2A0B0D` | Sombras y fondos profundos |
| Tinta | `#321918` | Títulos y textos sobre crema |
| Malva | `#7B5B5B` | Textos secundarios sobre crema |
| Crema | `#F8F4EB` | Fondo claro principal |
| Rosa marfil | `#FCE5DA` | Textos sobre bordó, acentos claros |
| Dorado antiguo | `#997957` | Acentos, líneas finas y marcas de perfume en cursiva |

### Tipografía

- **Playfair Display:** títulos, nombres de perfume y precios.
- **Pinyon Script:** acentos en cursiva (marcas de perfume, "desde", etiquetas). No la uses en tamaños chicos.
- **Poppins:** textos chicos, etiquetas, botones, subtítulos y pie.

Los archivos están en `herramientas/pieza-marca/assets/fonts/`. Los logos en todos los colores están en `marca/logos/` (sobre fondo claro, bordó vino).

## Qué herramienta usar

No uses el script de la skill `larese-anuncios` tal cual: tiene los colores y las letras viejas.

| Pieza | Herramienta |
|---|---|
| Post, cuadrado, historia, portada o carrusel simple | `python3 herramientas/pieza-marca/scripts/crear_pieza.py spec.json salida.png` (mismo spec que `larese-anuncios`; `color` y `categoria` se ignoran; `"fondo": "blanco"` y `"letra": "vino"` solo si la dueña lo pide) |
| Carrusel de productos estilo editorial (slides crema y bordó con estampilla) | `python3 herramientas/carrusel-bordo/scripts/crear_carrusel.py carrusel.json carpeta/` (para un carrusel a medida, importá sus funciones, como `flyer-black-friday-decants/carrusel/armar_carrusel.py`) |
| Decants de 5 y 10 ml con la foto real del frasquito, para fondo vino | `flyer-black-friday-decants/fuente/decants_vino.py` (función `frasco(color, ml)`) |
| Foto de producto chica (menos de ~1000 px) | `python3 herramientas/agrandar-foto/agrandar.py foto.jpg foto-x4.png` (necesita `opencv-contrib-python-headless<5`; con OpenCV 5 no abre el modelo) |
| Fondo blanco, solo si lo pide | `python3 herramientas/pieza-fondo-blanco/scripts/crear_pieza.py spec.json salida.png` |

Si armás una pieza a mano o con otra herramienta, respetá la paleta y la tipografía de arriba. Podés importar las funciones de `herramientas/pieza-marca/scripts/crear_pieza.py` (logo, botón, pie, fuentes), como hace `flyer-black-friday-decants/fuente/armar_flyer.py`.

## Datos

- Precios y nombres sacados de Shopify o confirmados por la dueña, nunca inventados.
- Meta rechazó un anuncio por la palabra "originales": en piezas pautadas, sacala.
