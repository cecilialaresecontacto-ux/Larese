import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { Botella } from "../componentes/Botella";
import { Destellos } from "../componentes/Destellos";
import { fragancias } from "../fragancias";
import { sans, serif } from "../fuentes";

type Props = {
  tienda: string;
  llamado: string;
};

// Coconut a la izquierda, Bare Vanilla al centro, Pure Seduction a la derecha
const orden = [1, 0, 2];

export const Final: React.FC<Props> = ({ tienda, llamado }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const latido = 1 + 0.04 * Math.sin(frame / 5);

  return (
    <AbsoluteFill
      style={{
        background: "radial-gradient(circle at 50% 55%, #fff4e6 0%, #efcfc0 50%, #b9846a 100%)",
      }}
    >
      <Destellos cantidad={90} semilla="final" />
      <AbsoluteFill style={{ alignItems: "center", textAlign: "center", color: "#4a2c1c", paddingTop: 170 }}>
        <Aparecer desde={30} style={{ fontFamily: sans, fontSize: 30, letterSpacing: 12, fontWeight: 500 }}>
          BODY MIST · 250 ML
        </Aparecer>
        <Aparecer desde={36} style={{ fontFamily: serif, fontSize: 112, lineHeight: 1.05, marginTop: 24 }}>
          Elegí tu
          <br />
          <span style={{ fontStyle: "italic", color: "#a8742f" }}>brillo favorito</span>
        </Aparecer>
      </AbsoluteFill>

      <AbsoluteFill style={{ flexDirection: "row", justifyContent: "center", alignItems: "flex-end", gap: 30, paddingBottom: 430 }}>
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
                alto={esCentro ? 820 : 720}
                proporcion={f.proporcion}
                inicioReflejo={45 + posicion * 8}
              />
            </div>
          );
        })}
      </AbsoluteFill>

      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 170, textAlign: "center" }}>
        {tienda ? (
          <Aparecer desde={50} style={{ fontFamily: serif, fontSize: 64, color: "#4a2c1c", marginBottom: 30 }}>
            {tienda}
          </Aparecer>
        ) : null}
        <Aparecer desde={58}>
          <div
            style={{
              fontFamily: sans,
              fontWeight: 600,
              fontSize: 44,
              letterSpacing: 3,
              color: "#fff8ee",
              background: "linear-gradient(135deg, #c99a4f, #8f5f2a)",
              padding: "28px 64px",
              borderRadius: 999,
              boxShadow: "0 12px 40px rgba(120, 70, 30, 0.35)",
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
