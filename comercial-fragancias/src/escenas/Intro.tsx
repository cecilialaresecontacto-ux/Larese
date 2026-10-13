import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { fuente } from "../fuentes";
import { marca } from "../marca";

export const Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const logo = spring({ frame, fps, config: { damping: 12, mass: 0.7 }, durationInFrames: 35 });
  const linea = interpolate(frame, [18, 45], [0, 320], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const zoom = interpolate(frame, [0, 90], [1.06, 1]);

  return (
    <AbsoluteFill
      style={{
        background: "radial-gradient(circle at 50% 45%, #fff6ea 0%, #ecd3b6 55%, #b98a5e 100%)",
      }}
    >
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
        <Img
          src={staticFile(marca.isotipo)}
          style={{
            width: 220,
            height: 220,
            marginBottom: 60,
            opacity: logo,
            transform: `scale(${interpolate(logo, [0, 1], [0.6, 1])})`,
          }}
        />
        <Aparecer desde={12} style={{ fontSize: 30, letterSpacing: 12, fontWeight: 500 }}>
          SHIMMER FRAGRANCE MIST
        </Aparecer>
        <div style={{ height: 3, width: linea, background: marca.negro, margin: "40px 0" }} />
        <Aparecer desde={22} style={{ fontSize: 120, fontWeight: 600, lineHeight: 1.05, letterSpacing: -2 }}>
          Perfumá
          <br />
          tu piel
        </Aparecer>
        <Aparecer desde={32} style={{ fontSize: 64, fontWeight: 300, marginTop: 24 }}>
          con brillo dorado
        </Aparecer>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
