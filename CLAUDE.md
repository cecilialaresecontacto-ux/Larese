# LARESE STORE: reglas de diseño

## Paleta y tipografía de marca en TODO

Todas las piezas de la tienda usan la **paleta y la tipografía de marca**: posts, historias, carruseles, portadas, reels, videos y anuncios de Meta. La dueña lo pidió así en noviembre de 2026 y lo confirmó el 17 de noviembre: "usá siempre eso". Las láminas están en `marca/paleta.png` y `marca/tipografia.png`.

El fondo blanco puro (estilo anterior) se usa **solo si la dueña lo pide** para una pieza puntual. Nunca uses el fondo con el color del producto ni colores fuera de la paleta.

### Paleta

| Color | Hex | Uso |
|---|---|---|
| Bordó vino | `#41030B` | Fondos oscuros, píldoras, botones |
| Bordó cuero | `#2A0B0D` | Sombras y fondos profundos |
| Tinta | `#321918` | Títulos y textos sobre crema |
| Malva | `#7B5B5B` | Textos secundarios sobre crema |
| Crema | `#F8F4EB` | Fondo claro principal |
| Rosa marfil | `#FCE5DA` | Textos sobre bordó, acentos claros |
| Dorado antiguo | `#997957` | Acentos, líneas finas, brillos y textos secundarios sobre bordó |

### Tipografía

- **Playfair Display:** títulos, nombres de perfume y precios. La itálica, para notas y frases cortas.
- **Pinyon Script:** acentos en cursiva (marcas, "desde", la palabra fuerte de un título). No la uses en tamaños chicos.
- **Poppins:** textos chicos, etiquetas, botones y subtítulos.

Los archivos están en `herramientas/carrusel-bordo/assets/fonts/` y, para pasárselos a la dueña, en `marca/tipografias-larese.zip`.

### Logo oficial: crema sobre bordó vino

- Versión principal: logo **crema** `#F8F4EB` sobre fondo **bordó vino** `#41030B`. Archivos con fondo transparente: `marca/logos/logo-crema.png` y `marca/logos/isotipo-crema.png`.
- Sobre fondos claros (crema, rosa marfil o blanco) usá la versión bordó vino: `marca/logos/logo-bordo-vino.png` y `marca/logos/isotipo-bordo-vino.png`.
- Foto de perfil de Instagram: `marca/perfil/perfil-instagram.png`.
- Para regenerar los logos en todos los colores: `python3 marca/crear_opciones_logo.py`.

## Qué herramienta usar

No uses los scripts de las skills `larese-anuncios` ni `larese-reels` tal cual: tienen los colores y las letras viejas. Usá las versiones del repo, que aceptan el mismo spec o plan.

| Pieza | Herramienta |
|---|---|
| Post, cuadrado, historia, portada de reel o carrusel simple | `python3 herramientas/pieza-marca/scripts/crear_pieza.py spec.json salida.png` (mismo spec que `larese-anuncios`; `color` y `categoria` se ignoran) |
| Carrusel de productos estilo editorial (slides crema y bordó con estampilla) | `python3 herramientas/carrusel-bordo/scripts/crear_carrusel.py carrusel.json carpeta/` (ejemplo: `carrusel-mas-pedidos/carrusel.json`) |
| Reel con los videos de la dueña hablando a cámara | `python3 herramientas/reels-marca/scripts/armar_reel.py plan.json` (mismo plan que `larese-reels`; seguí las instrucciones de esa skill para armarlo) |
| Reel animado con fotos de productos (sin video de ella) | `python3 herramientas/reel-productos/crear_reel.py reel.json salida.mp4` (ejemplo: `reel-mas-pedidos/reel.json`; sale sin música, la dueña le pone un audio en tendencia desde Instagram) |
| Fondo blanco, solo si lo pide | `python3 herramientas/pieza-fondo-blanco/scripts/crear_pieza.py spec.json salida.png` |
| Foto de producto chica o borrosa (menos de ~1000 px) | `python3 herramientas/agrandar-foto/agrandar.py foto.jpg foto-x4.png` antes de armar la pieza, y usá `foto-x4.png` en el spec (ejemplo: `anuncio-odyssey-aqua/`) |

Si armás una pieza a mano o con otra herramienta, respetá la paleta y la tipografía de arriba.

### Que se vea nítido

- La dueña pide que las piezas se vean nítidas. Las fotos que manda suelen ser chicas (500 a 600 px): agrandalas con `agrandar-foto` antes de usarlas. `pieza-marca` igual le da un toque de nitidez a cualquier foto que tenga que estirar.
- En `pieza-marca`, el botón va en bordó vino sólido, el precio tachado en malva y los títulos de dos renglones llevan aire para que no toquen el subtítulo.
- Para que un nombre no se corte en dos renglones, uní sus palabras con espacio duro (U+00A0) en el spec: `"9 PM Rebel"`.

## Datos

- Precios y nombres sacados de Shopify, nunca inventados. Si el conector de Shopify no responde, la tienda pública sirve: `https://lareseparfums.com.py/search/suggest.json?q=...&resources[type]=product` y `https://lareseparfums.com.py/products/<handle>.js` (los precios del `.js` vienen multiplicados por 100).
- Meta rechazó un anuncio por la palabra "originales": en piezas pautadas, sacala.
- Instagram acepta hasta 20 slides por carrusel.
