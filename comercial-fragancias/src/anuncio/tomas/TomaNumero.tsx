import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { fuente } from "../../fuentes";
import { negro, resplandor, textoDorado, textoMetal } from "../estilo";

type Props = {
  valor: string;
  detalle: string;
};

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const anillo = "radial-gradient(circle, transparent 14%, black 26%, black 46%, transparent 68%)";

// Número gigante sobre anillos que giran, como "48 MP" en la referencia
export const TomaNumero: React.FC<Props> = ({ valor, detalle }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const entrada = spring({ frame, fps, config: { damping: 200 }, durationInFrames: 12 });
  const salida = interpolate(frame, [durationInFrames - 5, durationInFrames], [0, 1], clamp);
  const giro = frame * 2.2;

  const capa: React.CSSProperties = {
    position: "absolute",
    inset: 0,
    WebkitMaskImage: anillo,
    maskImage: anillo,
  };

  return (
    <AbsoluteFill style={{ background: negro, fontFamily: fuente, opacity: 1 - salida }}>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <div
          style={{
            position: "relative",
            width: 1900,
            height: 1900,
            opacity: entrada,
            transform: `rotate(${giro}deg) scale(${interpolate(frame, [0, durationInFrames], [1.2, 1])})`,
          }}
        >
          <div
            style={{
              ...capa,
              background:
                "repeating-radial-gradient(circle, transparent 0 34px, rgba(255,255,255,0.16) 37px, transparent 44px)",
            }}
          />
          <div
            style={{
              ...capa,
              background:
                "repeating-conic-gradient(rgba(255,255,255,0) 0deg 5deg, rgba(255,255,255,0.4) 6deg, rgba(255,255,255,0) 8deg 13deg)",
              filter: "blur(5px)",
            }}
          />
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: resplandor(0.35) }} />
      <AbsoluteFill
        style={{
          justifyContent: "center",
          alignItems: "center",
          transform: `scale(${interpolate(entrada, [0, 1], [1.3, 1])})`,
          filter: `blur(${interpolate(entrada, [0, 1], [20, 0]) + salida * 16}px)`,
          opacity: entrada,
        }}
      >
        <div style={{ fontSize: 290, fontWeight: 700, letterSpacing: -12, lineHeight: 1, ...textoMetal }}>{valor}</div>
        <div style={{ fontSize: 96, fontWeight: 600, letterSpacing: -2, marginTop: 10, ...textoDorado }}>{detalle}</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
