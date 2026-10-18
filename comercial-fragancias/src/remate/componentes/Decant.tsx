import { interpolate } from "remotion";
import { dorado } from "../estilo";

type Props = {
  alto: number;
  // De 0 a 1: cuánto líquido se ve
  llenado: number;
};

// Frasquito de decant dibujado con CSS
export const Decant: React.FC<Props> = ({ alto, llenado }) => {
  const ancho = alto * 0.3;
  const altoTapa = alto * 0.22;
  const altoVidrio = alto - altoTapa;
  const liquido = interpolate(llenado, [0, 1], [0, altoVidrio * 0.88]);

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <div
        style={{
          width: ancho * 0.7,
          height: altoTapa,
          borderRadius: "10px 10px 4px 4px",
          background: "linear-gradient(90deg, #8a6424, #f3d78c 45%, #9c7230)",
        }}
      />
      <div
        style={{
          position: "relative",
          width: ancho,
          height: altoVidrio,
          borderRadius: `8px 8px ${ancho / 2}px ${ancho / 2}px`,
          border: "4px solid rgba(255, 255, 255, 0.7)",
          background: "rgba(255, 255, 255, 0.08)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            bottom: 0,
            height: liquido,
            background: `linear-gradient(180deg, #f6dd9a, ${dorado} 50%, #9c6a22)`,
          }}
        />
        <div
          style={{
            position: "absolute",
            top: "8%",
            bottom: "12%",
            left: "16%",
            width: "14%",
            borderRadius: 999,
            background: "rgba(255, 255, 255, 0.45)",
          }}
        />
      </div>
    </div>
  );
};
