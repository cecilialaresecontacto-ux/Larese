import { AbsoluteFill } from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { fuente } from "../fuentes";
import { Abanico } from "./escenas/Escenas";
import { gris, precios, Producto, productos } from "./marca";
import { Encabezado, Fondo, FotoCentral, LogoArriba, Pie, Pildora, POST } from "./Piezas";

const BLANCO = "#ffffff";
const CENTRO_MARCA = 690;

const FilaPrecios: React.FC<{ abajo: number }> = ({ abajo }) => (
  <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: abajo }}>
    <Aparecer desde={18}>
      <div style={{ display: "flex", alignItems: "center", gap: 40, fontFamily: fuente, color: BLANCO, textAlign: "center" }}>
        {precios.map((p, i) => [
          i > 0 ? <div key={`s-${p.ml}`} style={{ width: 3, height: 90, background: "rgba(255, 255, 255, 0.6)" }} /> : null,
          <div key={p.ml}>
            <div style={{ fontSize: 26, fontWeight: 500, letterSpacing: 2 }}>{p.ml} ML</div>
            <div style={{ fontSize: 60, fontWeight: 700, lineHeight: 1.05 }}>{p.precio}</div>
          </div>,
        ])}
      </div>
    </Aparecer>
  </AbsoluteFill>
);

const PildoraAbajo: React.FC<{ texto: string; paleta: typeof gris }> = ({ texto, paleta }) => (
  <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 150 }}>
    <Pildora texto={texto} paleta={paleta} desde={24} m={POST} />
  </AbsoluteFill>
);

const Portada: React.FC = () => (
  <AbsoluteFill>
    <Fondo paleta={gris} centroMarca={CENTRO_MARCA} />
    <LogoArriba m={POST} />
    <Encabezado m={POST} etiqueta="Decants · 100% originales" titulo="Remate de decants" tamano={104} subtitulo="Perfumes árabes premium" />
    <Abanico top={590} ancho={300} separacion={128} />
    <PildoraAbajo texto="Deslizá para ver todos 👉" paleta={gris} />
    <Pie paleta={gris} m={POST} />
  </AbsoluteFill>
);

const SlideFragancia: React.FC<{ producto: Producto }> = ({ producto }) => (
  <AbsoluteFill>
    <Fondo paleta={producto.paleta} centroMarca={CENTRO_MARCA} />
    <LogoArriba m={POST} />
    <Encabezado
      m={POST}
      etiqueta={`Decant original · ${producto.marca}`}
      titulo={producto.nombre}
      subtitulo={producto.publico}
      tamano={producto.nombre.length > 10 ? 80 : 100}
    />
    <FotoCentral imagen={producto.imagen} proporcion={producto.proporcion} ancho={560} top={410} />
    <FilaPrecios abajo={245} />
    <PildoraAbajo texto="¡Pedí el tuyo!" paleta={producto.paleta} />
    <Pie paleta={producto.paleta} m={POST} />
  </AbsoluteFill>
);

const Cierre: React.FC = () => (
  <AbsoluteFill>
    <Fondo paleta={gris} centroMarca={CENTRO_MARCA} />
    <LogoArriba m={POST} />
    <Encabezado m={POST} etiqueta="Remate de decants" titulo="¡Y muchos más!" tamano={100} subtitulo="Hasta agotar stock" />
    <Abanico top={450} ancho={270} separacion={118} />
    <FilaPrecios abajo={245} />
    <PildoraAbajo texto="Escribinos por WhatsApp" paleta={gris} />
    <Pie paleta={gris} m={POST} />
  </AbsoluteFill>
);

// Slides del carrusel de Instagram: portada, una por perfume y cierre
export const slidesCarrusel: React.FC[] = [
  Portada,
  ...productos.map((p) => {
    const Slide: React.FC = () => <SlideFragancia producto={p} />;
    return Slide;
  }),
  Cierre,
];
