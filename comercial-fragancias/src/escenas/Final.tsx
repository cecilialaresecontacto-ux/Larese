import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { Botella } from "../componentes/Botella";
import { fragancias } from "../fragancias";
import { fuente } from "../fuentes";
import { marca } from "../marca";

type Props = {
  usuario: string;
  llamado: string;
};

const ALTO_LOGO = 110;

// Coconut a la izquierda, Bare Vanilla al centro, Pure Seduction a la derecha
const orden = [1, 0, 2];

export const Final: React.FC<Props> = ({ usuario, llamado }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const latido = 1 + 0.04 * Math.sin(frame / 5);

  return (
    <AbsoluteFill
      style={{
        background: "radial-gradient(circle at 50% 55%, #fff4e6 0%, #efcfc0 50%, #b9846a 100%)",
        fontFamily: fuente,
        color: marca.negro,
      }}
    >
      <AbsoluteFill style={{ alignItems: "center", textAlign: "center", paddingTop: 160 }}>
        <Aparecer desde={30} style={{ fontSize: 28, letterSpacing: 12, fontWeight: 500 }}>
          BODY MIST · 250 ML
        </Aparecer>
        <Aparecer desde={36} style={{ fontSize: 104, fontWeight: 600, lineHeight: 1.05, letterSpacing: -2, marginTop: 24 }}>
          Elegí tu
          <br />
          <span style={{ fontWeight: 300 }}>brillo favorito</span>
        </Aparecer>
      </AbsoluteFill>

      <AbsoluteFill style={{ flexDirection: "row", justifyContent: "center", alignItems: "flex-end", gap: 30, paddingBottom: 560 }}>
        {orden.map((indice, posicion) => {
          const f = fragancias[indice];
          const entrada = spring({
            frame: frame - posicion * 6,
            fps,
            config: { damping: 13, mass: 0.7 },
            durationInFrames: 40,
          });
          const esCentro = posicion === 1;
          const flotar = Math.sin((frame + posicion * 12) / 15) * 8;

          return (
            <div
              key={f.id}
              style={{
                opacity: interpolate(entrada, [0, 0.4], [0, 1], { extrapolateRight: "clamp" }),
                transform: `translateY(${interpolate(entrada, [0, 1], [700, 0]) + flotar}px)`,
                zIndex: esCentro ? 2 : 1,
              }}
            >
              <Botella
                imagen={f.imagen}
                alto={esCentro ? 720 : 630}
                proporcion={f.proporcion}
                inicioReflejo={45 + posicion * 8}
              />
            </div>
          );
        })}
      </AbsoluteFill>

      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 150, textAlign: "center" }}>
        <Aparecer desde={48}>
          <Img
            src={staticFile(marca.logo)}
            style={{ height: ALTO_LOGO, width: ALTO_LOGO * marca.logoProporcion }}
          />
        </Aparecer>
        <Aparecer desde={54} style={{ fontSize: 40, fontWeight: 500, marginTop: 18, marginBottom: 36 }}>
          {usuario}
        </Aparecer>
        <Aparecer desde={60}>
          <div
            style={{
              fontWeight: 600,
              fontSize: 40,
              letterSpacing: 1,
              color: marca.blanco,
              background: marca.negro,
              padding: "26px 64px",
              borderRadius: 999,
              boxShadow: "0 12px 40px rgba(0, 0, 0, 0.25)",
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
