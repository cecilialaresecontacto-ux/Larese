import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../../componentes/Aparecer";
import { fuente } from "../../fuentes";
import { marca } from "../../marca";
import { BarraPrecios } from "../componentes/BarraPrecios";
import { LogoStore } from "../componentes/LogoStore";
import { Decant } from "../datos";
import { dorado, fondoOscuro } from "../estilo";

const ANCHO_FOTO = 840;

export const EscenaDecant: React.FC<{ decant: Decant }> = ({ decant }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const entrada = spring({ frame, fps, config: { damping: 14, mass: 0.8 }, durationInFrames: 40 });
  const zoom = interpolate(frame, [0, durationInFrames], [1, 1.05]);
  const flotar = Math.sin(frame / 14) * 8;
  const reflejo = interpolate(frame, [22, 55], [-40, 140], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const altoFoto = ANCHO_FOTO / decant.proporcion;

  return (
    <AbsoluteFill style={{ background: fondoOscuro(decant.acento, 36), fontFamily: fuente, color: marca.blanco }}>
      <AbsoluteFill style={{ alignItems: "center", top: 100 }}>
        <Aparecer desde={4}>
          <LogoStore alto={56} />
        </Aparecer>
      </AbsoluteFill>

      <AbsoluteFill style={{ alignItems: "center", top: 290 }}>
        <div
          style={{
            position: "relative",
            width: ANCHO_FOTO,
            height: altoFoto,
            borderRadius: 44,
            overflow: "hidden",
            background: marca.blanco,
            boxShadow: `0 0 90px ${decant.acento}66, 0 30px 60px rgba(0, 0, 0, 0.5)`,
            opacity: interpolate(entrada, [0, 0.4], [0, 1], { extrapolateRight: "clamp" }),
            transform: `translateY(${interpolate(entrada, [0, 1], [420, 0]) + flotar}px) scale(${interpolate(entrada, [0, 1], [0.85, 1]) * zoom})`,
          }}
        >
          <Img src={staticFile(decant.imagen)} style={{ width: "100%", height: "100%" }} />
          <div
            style={{
              position: "absolute",
              inset: 0,
              background: `linear-gradient(105deg, transparent ${reflejo - 20}%, rgba(255,255,255,0.55) ${reflejo}%, transparent ${reflejo + 20}%)`,
            }}
          />
        </div>
      </AbsoluteFill>

      <AbsoluteFill style={{ alignItems: "center", textAlign: "center", top: 290 + altoFoto + 50 }}>
        <Aparecer desde={14} style={{ fontSize: 32, letterSpacing: 12, fontWeight: 500, color: dorado }}>
          {decant.marca.toUpperCase()}
        </Aparecer>
        <Aparecer desde={20} style={{ fontSize: 104, fontWeight: 700, letterSpacing: -2, lineHeight: 1.05, marginTop: 6 }}>
          {decant.nombre}
        </Aparecer>
        <Aparecer desde={26} style={{ fontSize: 40, fontWeight: 300, marginTop: 8 }}>
          {decant.publico}
        </Aparecer>
      </AbsoluteFill>

      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 130 }}>
        <Aparecer desde={22} style={{ fontSize: 30, letterSpacing: 8, fontWeight: 500, color: dorado, marginBottom: 26 }}>
          DECANTS · HASTA AGOTAR STOCK
        </Aparecer>
        <Aparecer desde={24}>
          <BarraPrecios />
        </Aparecer>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
