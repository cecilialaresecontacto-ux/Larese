import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { fuente } from "../fuentes";
import { marca } from "../marca";

type Props = {
  precio: string;
  llamado: string;
};

const ALTO_LOGO = 64;
const PROPORCION_TRIO = 2009 / 800;

export const Final: React.FC<Props> = ({ precio, llamado }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const latido = 1 + 0.035 * Math.sin(frame / 5);
  const trio = spring({ frame, fps, config: { damping: 13, mass: 0.7 }, durationInFrames: 40 });
  const precioIn = spring({ frame: frame - 30, fps, config: { damping: 9, mass: 0.6 }, durationInFrames: 30 });
  const anchoTrio = 1020;

  return (
    <AbsoluteFill style={{ background: marca.fondo, fontFamily: fuente, color: marca.negro }}>
      <AbsoluteFill style={{ alignItems: "center", textAlign: "center", paddingTop: 170 }}>
        <Aparecer desde={0}>
          <Img src={staticFile(marca.logo)} style={{ height: ALTO_LOGO, width: ALTO_LOGO * marca.logoProporcion }} />
        </Aparecer>
        <Aparecer desde={6} style={{ fontSize: 120, fontWeight: 700, letterSpacing: -3, marginTop: 50, lineHeight: 1 }}>
          3 DECANTS
        </Aparecer>
        <Aparecer desde={10} style={{ fontSize: 34, fontWeight: 500, color: marca.gris, marginTop: 14, letterSpacing: 2 }}>
          PROFONDO · BORN IN ROMA INTENSE · LE BEAU
        </Aparecer>
      </AbsoluteFill>

      <AbsoluteFill style={{ alignItems: "center", top: 700 }}>
        <div
          style={{
            opacity: interpolate(trio, [0, 0.4], [0, 1], { extrapolateRight: "clamp" }),
            transform: `translateY(${interpolate(trio, [0, 1], [400, 0])}px)`,
          }}
        >
          <Img src={staticFile("trio.png")} style={{ width: anchoTrio, height: anchoTrio / PROPORCION_TRIO }} />
        </div>
      </AbsoluteFill>

      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 200, textAlign: "center" }}>
        <Aparecer desde={24} style={{ fontSize: 44, fontWeight: 400, color: marca.gris }}>
          Los 3 a tan solo
        </Aparecer>
        <div
          style={{
            fontSize: 140,
            fontWeight: 700,
            letterSpacing: -3,
            lineHeight: 1.05,
            opacity: precioIn,
            transform: `scale(${interpolate(precioIn, [0, 1], [1.5, 1])})`,
          }}
        >
          {precio}
        </div>
        <Aparecer desde={44} style={{ marginTop: 30 }}>
          <div
            style={{
              fontWeight: 600,
              fontSize: 44,
              color: marca.blanco,
              background: marca.negro,
              padding: "26px 60px",
              borderRadius: 999,
              boxShadow: "0 12px 40px rgba(0, 0, 0, 0.2)",
              transform: `scale(${latido})`,
            }}
          >
            {llamado}
          </div>
        </Aparecer>
        <Aparecer desde={52} style={{ fontSize: 38, fontWeight: 500, marginTop: 34 }}>
          0972 736 002 · Envíos a todo Paraguay
        </Aparecer>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
