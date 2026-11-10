import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { fuente } from "../fuentes";
import { marca } from "../marca";

const ALTO_LOGO = 70;

export const Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const golpe = spring({ frame: frame - 10, fps, config: { damping: 10, mass: 0.6 }, durationInFrames: 30 });
  const zoom = interpolate(frame, [0, 90], [1.04, 1]);

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 50% 48%, ${marca.blanco} 0%, ${marca.fondo} 55%, ${marca.halo} 140%)`,
      }}
    >
      <AbsoluteFill style={{ alignItems: "center", top: 170 }}>
        <Aparecer desde={0}>
          <Img src={staticFile(marca.logo)} style={{ height: ALTO_LOGO, width: ALTO_LOGO * marca.logoProporcion }} />
        </Aparecer>
      </AbsoluteFill>
      <AbsoluteFill
        style={{
          justifyContent: "center",
          alignItems: "center",
          textAlign: "center",
          color: marca.negro,
          fontFamily: fuente,
          transform: `scale(${zoom})`,
        }}
      >
        <Aparecer desde={4}>
          <div
            style={{
              fontSize: 34,
              fontWeight: 600,
              letterSpacing: 6,
              background: marca.negro,
              color: marca.blanco,
              padding: "14px 34px",
              borderRadius: 999,
            }}
          >
            TRÍO DE DISEÑADOR · PARA ÉL
          </div>
        </Aparecer>
        <div
          style={{
            fontSize: 150,
            fontWeight: 700,
            lineHeight: 1,
            letterSpacing: -4,
            marginTop: 40,
            opacity: golpe,
            transform: `scale(${interpolate(golpe, [0, 1], [1.6, 1])})`,
          }}
        >
          3 DECANTS
        </div>
        <Aparecer desde={26} style={{ fontSize: 60, fontWeight: 300, marginTop: 30 }}>
          de 5 ml cada uno
        </Aparecer>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
