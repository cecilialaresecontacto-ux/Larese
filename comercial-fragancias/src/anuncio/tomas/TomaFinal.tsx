import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../../componentes/Aparecer";
import { fuente } from "../../fuentes";
import { marca } from "../../marca";
import { dorado, negro, resplandor, textoDorado } from "../estilo";

type Props = {
  usuario: string;
  llamado: string;
};

const ALTO_LOGO = 150;

export const TomaFinal: React.FC<Props> = ({ usuario, llamado }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const logo = spring({ frame, fps, config: { damping: 200 }, durationInFrames: 18 });
  const linea = interpolate(frame, [10, 30], [0, 420], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ background: negro, fontFamily: fuente, color: marca.blanco }}>
      <AbsoluteFill style={{ background: resplandor(0.22 * logo) }} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", textAlign: "center" }}>
        <div
          style={{
            opacity: logo,
            filter: `blur(${interpolate(logo, [0, 1], [20, 0])}px)`,
            transform: `scale(${interpolate(logo, [0, 1], [1.2, 1])})`,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Img
            src={staticFile("marca/logo-blanco.png")}
            style={{ height: ALTO_LOGO, width: ALTO_LOGO * marca.logoProporcion }}
          />
          <div style={{ fontSize: 46, fontWeight: 500, letterSpacing: 46, marginRight: -46, marginTop: 24 }}>STORE</div>
        </div>
        <div style={{ height: 3, width: linea, background: dorado, margin: "60px 0 50px" }} />
        <Aparecer desde={16} style={{ fontSize: 64, fontWeight: 600, letterSpacing: -1, ...textoDorado }}>
          Remate de decants.
        </Aparecer>
        <Aparecer desde={22} style={{ fontSize: 42, fontWeight: 400, marginTop: 14 }}>
          5 ml Gs. 15.000 · 10 ml Gs. 20.000
        </Aparecer>
      </AbsoluteFill>
      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 190 }}>
        <Aparecer desde={30} style={{ fontSize: 40, fontWeight: 500 }}>
          {usuario}
        </Aparecer>
        <Aparecer desde={34} style={{ fontSize: 34, fontWeight: 300, marginTop: 8 }}>
          {llamado}
        </Aparecer>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
