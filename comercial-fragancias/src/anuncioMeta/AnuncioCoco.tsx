import { AbsoluteFill } from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { fuente } from "../fuentes";
import { Paleta } from "../remateMarca/marca";
import { Encabezado, Fondo, FotoCentral, HISTORIA, LogoArriba, Medidas, Pie, Pildora, POST } from "../remateMarca/Piezas";

const BLANCO = "#ffffff";

// Color sacado del frasco con las reglas del skill de anuncios de Larese
const durazno: Paleta = { color: "#bc9684", oscuro: "#836456", centro: "#cdac9c", borde: "#aa8777" };

const precios = [
  { ml: 5, precio: "Gs. 95.000" },
  { ml: 10, precio: "Gs. 160.000" },
];

type Diseno = {
  m: Medidas;
  centroMarca: number;
  titulo: number;
  foto: { ancho: number; top: number };
  precios: { abajo: number; ml: number; precio: number };
  pildoraAbajo: number;
};

const disenos: Record<"post" | "historia", Diseno> = {
  post: {
    m: POST,
    centroMarca: 690,
    titulo: 84,
    foto: { ancho: 540, top: 400 },
    precios: { abajo: 245, ml: 26, precio: 60 },
    pildoraAbajo: 150,
  },
  historia: {
    m: HISTORIA,
    centroMarca: 980,
    titulo: 88,
    foto: { ancho: 620, top: 680 },
    precios: { abajo: 450, ml: 32, precio: 72 },
    pildoraAbajo: 330,
  },
};

// Anuncio pago de Meta para el decant de Coco Mademoiselle Intense, con el estilo de marca
export const AnuncioCoco: React.FC<{ formato: "post" | "historia" }> = ({ formato }) => {
  const d = disenos[formato];
  return (
    <AbsoluteFill>
      <Fondo paleta={durazno} centroMarca={d.centroMarca} />
      <LogoArriba m={d.m} />
      <Encabezado
        m={d.m}
        etiqueta="Decant original · Chanel"
        titulo="Coco Mademoiselle"
        subtitulo="Eau de Parfum Intense"
        tamano={d.titulo}
      />
      <FotoCentral imagen="meta/coco-mademoiselle.jpg" proporcion={1} ancho={d.foto.ancho} top={d.foto.top} />
      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: d.precios.abajo }}>
        <Aparecer desde={18}>
          <div style={{ display: "flex", alignItems: "center", gap: 40, fontFamily: fuente, color: BLANCO, textAlign: "center" }}>
            {precios.map((p, i) => [
              i > 0 ? (
                <div key={`s-${p.ml}`} style={{ width: 3, height: d.precios.precio * 1.5, background: "rgba(255, 255, 255, 0.6)" }} />
              ) : null,
              <div key={p.ml}>
                <div style={{ fontSize: d.precios.ml, fontWeight: 500, letterSpacing: 2 }}>{p.ml} ML</div>
                <div style={{ fontSize: d.precios.precio, fontWeight: 700, lineHeight: 1.05 }}>{p.precio}</div>
              </div>,
            ])}
          </div>
        </Aparecer>
      </AbsoluteFill>
      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: d.pildoraAbajo }}>
        <Pildora texto="¡Pedí el tuyo!" paleta={durazno} desde={24} m={d.m} />
      </AbsoluteFill>
      <Pie paleta={durazno} m={d.m} />
    </AbsoluteFill>
  );
};
