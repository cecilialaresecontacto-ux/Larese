import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../../componentes/Aparecer";
import { fuente } from "../../fuentes";
import { marca } from "../../marca";
import { LogoStore } from "../componentes/LogoStore";
import { dorado, fondoOscuro, textoDorado } from "../estilo";

export const IntroRemate: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const golpe = spring({ frame: frame - 14, fps, config: { damping: 9, mass: 0.6 }, durationInFrames: 30 });
  const linea = interpolate(frame, [26, 50], [0, 520], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const zoom = interpolate(frame, [0, 90], [1.05, 1]);
  const latido = 1 + 0.035 * Math.sin(frame / 4);

  return (
    <AbsoluteFill style={{ background: fondoOscuro(dorado), fontFamily: fuente, color: marca.blanco }}>
      <AbsoluteFill
        style={{ justifyContent: "center", alignItems: "center", textAlign: "center", transform: `scale(${zoom})` }}
      >
        <Aparecer desde={0}>
          <LogoStore alto={120} />
        </Aparecer>
        <div style={{ height: 3, width: linea, background: dorado, margin: "70px 0 50px" }} />
        <div
          style={{
            fontSize: 210,
            fontWeight: 700,
            letterSpacing: -4,
            lineHeight: 1,
            opacity: interpolate(golpe, [0, 0.3], [0, 1], { extrapolateRight: "clamp" }),
            transform: `scale(${interpolate(golpe, [0, 1], [1.8, 1])})`,
            ...textoDorado,
          }}
        >
          REMATE
        </div>
        <Aparecer desde={26} style={{ fontSize: 92, fontWeight: 300, letterSpacing: 6, marginTop: 10 }}>
          de decants
        </Aparecer>
        <Aparecer desde={40}>
          <div
            style={{
              marginTop: 70,
              padding: "18px 48px",
              borderRadius: 999,
              background: dorado,
              color: marca.negro,
              fontSize: 40,
              fontWeight: 600,
              letterSpacing: 2,
              transform: `scale(${latido})`,
            }}
          >
            ¡HASTA AGOTAR STOCK!
          </div>
        </Aparecer>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
