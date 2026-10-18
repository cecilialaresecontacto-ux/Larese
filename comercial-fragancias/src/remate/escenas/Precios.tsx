import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../../componentes/Aparecer";
import { fuente } from "../../fuentes";
import { marca } from "../../marca";
import { Decant } from "../componentes/Decant";
import { LogoStore } from "../componentes/LogoStore";
import { precios } from "../datos";
import { dorado, fondoOscuro, textoDorado } from "../estilo";

export const Precios: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ background: fondoOscuro(dorado, 55), fontFamily: fuente, color: marca.blanco }}>
      <AbsoluteFill style={{ alignItems: "center", top: 110 }}>
        <LogoStore alto={56} />
      </AbsoluteFill>

      <AbsoluteFill style={{ alignItems: "center", textAlign: "center", top: 330 }}>
        <Aparecer desde={4} style={{ fontSize: 34, letterSpacing: 12, fontWeight: 500, color: dorado }}>
          PRECIOS DE REMATE
        </Aparecer>
        <Aparecer desde={10} style={{ fontSize: 96, fontWeight: 600, letterSpacing: -2, marginTop: 10 }}>
          Elegí tu tamaño
        </Aparecer>
      </AbsoluteFill>

      <AbsoluteFill style={{ flexDirection: "row", justifyContent: "center", alignItems: "flex-end", gap: 50, paddingBottom: 380 }}>
        {precios.map((p, i) => {
          const entrada = spring({ frame: frame - 14 - i * 8, fps, config: { damping: 13, mass: 0.7 }, durationInFrames: 40 });
          const llenado = interpolate(frame, [24 + i * 8, 60 + i * 8], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });

          return (
            <div
              key={p.ml}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                width: 440,
                padding: "50px 0 44px",
                borderRadius: 40,
                border: `3px solid ${dorado}`,
                background: "rgba(255, 255, 255, 0.06)",
                opacity: interpolate(entrada, [0, 0.4], [0, 1], { extrapolateRight: "clamp" }),
                transform: `translateY(${interpolate(entrada, [0, 1], [500, 0])}px)`,
              }}
            >
              <Decant alto={i === 0 ? 340 : 470} llenado={llenado} />
              <div style={{ fontSize: 90, fontWeight: 700, marginTop: 40, lineHeight: 1 }}>{p.ml} ml</div>
              <div style={{ fontSize: 66, fontWeight: 700, marginTop: 18, ...textoDorado }}>{p.precio}</div>
            </div>
          );
        })}
      </AbsoluteFill>

      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 200 }}>
        <Aparecer desde={46} style={{ fontSize: 40, fontWeight: 500, letterSpacing: 2 }}>
          Precios en guaraníes
        </Aparecer>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
