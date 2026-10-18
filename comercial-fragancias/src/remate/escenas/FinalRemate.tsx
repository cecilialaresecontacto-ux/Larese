import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../../componentes/Aparecer";
import { fuente } from "../../fuentes";
import { marca } from "../../marca";
import { LogoStore } from "../componentes/LogoStore";
import { decants, precios } from "../datos";
import { dorado, fondoOscuro, textoDorado } from "../estilo";

type Props = {
  usuario: string;
  llamado: string;
};

const ANCHO_MINI = 300;

export const FinalRemate: React.FC<Props> = ({ usuario, llamado }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const latido = 1 + 0.04 * Math.sin(frame / 5);
  const centro = (decants.length - 1) / 2;

  return (
    <AbsoluteFill style={{ background: fondoOscuro(dorado, 40), fontFamily: fuente, color: marca.blanco }}>
      <AbsoluteFill style={{ alignItems: "center", textAlign: "center", paddingTop: 170 }}>
        <Aparecer desde={0} style={{ fontSize: 34, letterSpacing: 12, fontWeight: 500, color: dorado }}>
          REMATE DE DECANTS
        </Aparecer>
        <Aparecer desde={6} style={{ fontSize: 120, fontWeight: 700, letterSpacing: -3, lineHeight: 1.05, marginTop: 14, ...textoDorado }}>
          ¡Hasta agotar
          <br />
          stock!
        </Aparecer>
        <Aparecer desde={12} style={{ fontSize: 44, fontWeight: 500, marginTop: 30 }}>
          {precios.map((p) => `${p.ml} ml ${p.precio}`).join("  ·  ")}
        </Aparecer>
      </AbsoluteFill>

      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", top: 120 }}>
        <div style={{ position: "relative", width: 1080, height: 320 }}>
          {decants.map((d, i) => {
            const entrada = spring({ frame: frame - 10 - i * 4, fps, config: { damping: 13, mass: 0.7 }, durationInFrames: 40 });
            const desvio = i - centro;
            const alto = ANCHO_MINI / d.proporcion;
            return (
              <Img
                key={d.id}
                src={staticFile(d.imagen)}
                style={{
                  position: "absolute",
                  left: 540 - ANCHO_MINI / 2 + desvio * 190,
                  top: (320 - alto) / 2 + Math.abs(desvio) * 30,
                  width: ANCHO_MINI,
                  height: alto,
                  borderRadius: 28,
                  border: `3px solid ${dorado}`,
                  boxShadow: "0 20px 40px rgba(0, 0, 0, 0.6)",
                  zIndex: 10 - Math.abs(desvio),
                  opacity: interpolate(entrada, [0, 0.4], [0, 1], { extrapolateRight: "clamp" }),
                  transform: `translateY(${interpolate(entrada, [0, 1], [600, 0])}px) rotate(${desvio * 6}deg)`,
                }}
              />
            );
          })}
        </div>
      </AbsoluteFill>

      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 150, textAlign: "center" }}>
        <Aparecer desde={30}>
          <LogoStore alto={100} />
        </Aparecer>
        <Aparecer desde={36} style={{ fontSize: 40, fontWeight: 500, marginTop: 20, marginBottom: 36 }}>
          {usuario}
        </Aparecer>
        <Aparecer desde={42}>
          <div
            style={{
              fontWeight: 600,
              fontSize: 42,
              color: marca.negro,
              background: dorado,
              padding: "26px 64px",
              borderRadius: 999,
              boxShadow: "0 12px 40px rgba(0, 0, 0, 0.4)",
              transform: `scale(${latido})`,
            }}
          >
            {llamado}
          </div>
        </Aparecer>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
