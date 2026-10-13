import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { Destellos } from "../componentes/Destellos";
import { sans, serif } from "../fuentes";

export const Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const linea = interpolate(frame, [10, 40], [0, 360], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const zoom = interpolate(frame, [0, 90], [1.08, 1]);

  return (
    <AbsoluteFill
      style={{
        background: "radial-gradient(circle at 50% 45%, #fff6ea 0%, #ecd3b6 55%, #b98a5e 100%)",
      }}
    >
      <Destellos cantidad={110} semilla="intro" />
      <AbsoluteFill
        style={{
          justifyContent: "center",
          alignItems: "center",
          textAlign: "center",
          color: "#4a2c1c",
          transform: `scale(${zoom})`,
        }}
      >
        <Aparecer desde={5} style={{ fontFamily: sans, fontSize: 34, letterSpacing: 12, fontWeight: 500 }}>
          SHIMMER FRAGRANCE MIST
        </Aparecer>
        <div style={{ height: 2, width: linea, background: "#b8893f", margin: "40px 0" }} />
        <Aparecer desde={15} style={{ fontFamily: serif, fontSize: 130, lineHeight: 1.05 }}>
          Perfumá
          <br />
          tu piel
        </Aparecer>
        <Aparecer
          desde={28}
          style={{ fontFamily: serif, fontStyle: "italic", fontSize: 92, color: "#a8742f", marginTop: 20 }}
        >
          con brillo dorado
        </Aparecer>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
