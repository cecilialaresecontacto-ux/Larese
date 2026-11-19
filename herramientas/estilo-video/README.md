# Estilo de edición de videos (reels y TikTok)

La dueña mandó un video de referencia (frase de Anthony Bourdain, editado por otra cuenta de TikTok) y pidió que **de ahora en más sus videos se editen así**. Cuadros de referencia: `referencia-cuadros.png`. El video original no se guarda en el repo porque es de otra cuenta.

## El estilo

- **Una voz que cuenta algo** (frase, idea, recomendación) y una música suave de fondo, sin cortes bruscos.
- **Cortes rápidos**: una toma nueva cada 1 a 1,5 segundos, y cada toma ilustra lo que se está diciendo en ese momento.
- **Mezcla de tomas en blanco y negro y en color**, con grano de película y algunas tomas con movimiento o desenfoque.
- **Texto en el centro, palabra por palabra o de a 2-3 palabras**, apareciendo justo cuando se dicen. Nunca subtítulos largos abajo.
- **Cada frase con su propia letra**, mezclando:
  - palabra chica fina arriba + palabra grande gruesa abajo ("tan lejos / COMO PUEDAS");
  - letra gruesa sin serifa para casi todo;
  - letra a mano (marcador) para las palabras más emocionales;
  - cursiva con serifa para palabras sueltas ("río", "océano", "alguien nuevo");
  - mayúsculas dibujadas con brillo para un verbo fuerte ("MUEVETE").
- **Un color de acento** para remarcar:
  - recuadro de color detrás de la palabra clave ("muy simple", "nuevo");
  - círculo dibujado a mano alrededor de una frase;
  - franja vertical de color con texto adentro.
- **Cierre** con una toma tranquila y el logo.

## Cómo se adapta a Larese

- **Colores:** en la referencia el acento es azul eléctrico. Para Larese va con la paleta de marca: recuadro **bordó vino** con letra **rosa marfil**, círculos y franjas en **dorado antiguo** (salvo que la dueña pida el azul).
- **Letras:** gruesa = Poppins Bold/SemiBold; cursiva con serifa = Cormorant Garamond Italic; a mano = una letra tipo marcador de Google Fonts (por ejemplo Gochi Hand o Caveat), que se descarga del repo `google/fonts` en GitHub; marca y acentos = Pinyon Script.
- **Tomas:** solo videos y fotos de la dueña (perfumes, decants, envíos, ella hablando). **No** usar cortes de películas, series ni documentales: tienen derechos de autor y Instagram/TikTok bajan el video o silencian el audio.
- **Formato:** 1080×1920, 25 a 30 cuadros por segundo, texto dentro de la zona segura (lejos de los bordes de arriba y abajo).

## Herramientas

- Transcripción con tiempos por palabra: WhisperAI (la dueña sube el audio con el botón de carga). HuggingFace está bloqueado en este entorno, así que no hay Whisper local.
- Armado del video: Remotion (como `comercial-fragancias/`) o ffmpeg + Pillow.
