import { fuente } from "../../fuentes";
import { marca } from "../../marca";
import { precios } from "../datos";
import { dorado } from "../estilo";

// Los dos precios, siempre visibles al pie de cada fragancia
export const BarraPrecios: React.FC = () => {
  return (
    <div style={{ display: "flex", gap: 24, fontFamily: fuente }}>
      {precios.map((p) => (
        <div
          key={p.ml}
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            width: 400,
            padding: "22px 0",
            borderRadius: 28,
            border: `3px solid ${dorado}`,
            background: "rgba(0, 0, 0, 0.55)",
            color: marca.blanco,
          }}
        >
          <div style={{ fontSize: 36, fontWeight: 500, color: dorado }}>{p.ml} ml</div>
          <div style={{ fontSize: 58, fontWeight: 700, lineHeight: 1.1 }}>{p.precio}</div>
        </div>
      ))}
    </div>
  );
};
