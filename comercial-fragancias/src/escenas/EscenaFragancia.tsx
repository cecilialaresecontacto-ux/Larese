import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { Botella } from "../componentes/Botella";
import { Fragancia } from "../fragancias";
import { fuente } from "../fuentes";
import { marca } from "../marca";

const ALTO_LOGO = 56;

export const EscenaFragancia: React.FC<{ fragancia: Fragancia; numero: number }> = ({
  fragancia,
  numero,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const entrada = spring({ frame, fps, config: { damping: 14, mass: 0.8 }, durationInFrames: 45 });
  const zoom = interpolate(frame, [0, durationInFrames], [1, 1.07]);
  const flotar = Math.sin(frame / 16) * 10;
  const giro = interpolate(entrada, [0, 1], [-6, 0]);
  const halo = 0.75 + 0.25 * Math.sin(frame / 10);

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 50% 38%, ${fragancia.fondoCentro} 0%, ${fragancia.fondoBorde} 100%)`,
      }}
    >
      <AbsoluteFill style={{ transform: `scale(${zoom})` }}>
        <div
          style={{
            position: "absolute",
            left: 540 - 420,
            top: 760 - 420,
            width: 840,
            height: 840,
            borderRadius: "50%",
            background: `radial-gradient(circle, ${fragancia.brillo} 0%, transparent 65%)`,
            opacity: halo,
          }}
        />
        <AbsoluteFill style={{ alignItems: "center", top: 270 }}>
          <div
            style={{
              opacity: interpolate(entrada, [0, 0.4], [0, 1], { extrapolateRight: "clamp" }),
              transform: `translateY(${interpolate(entrada, [0, 1], [500, 0]) + flotar}px) rotate(${giro}deg) scale(${interpolate(entrada, [0, 1], [0.85, 1])})`,
            }}
          >
            <Botella imagen={fragancia.imagen} alto={980} proporcion={fragancia.proporcion} inicioReflejo={28} />
          </div>
        </AbsoluteFill>
      </AbsoluteFill>

      <AbsoluteFill style={{ alignItems: "center", top: 110 }}>
        <Aparecer desde={6}>
          <Img
            src={staticFile(marca.logo)}
            style={{ height: ALTO_LOGO, width: ALTO_LOGO * marca.logoProporcion }}
          />
        </Aparecer>
      </AbsoluteFill>

      <AbsoluteFill
        style={{
          justifyContent: "flex-end",
          alignItems: "center",
          paddingBottom: 170,
          textAlign: "center",
          color: marca.negro,
          fontFamily: fuente,
        }}
      >
        <Aparecer desde={18} style={{ fontSize: 26, letterSpacing: 10, fontWeight: 500, opacity: 0.75 }}>
          {`0${numero} · SHIMMER`}
        </Aparecer>
        <Aparecer desde={24} style={{ fontSize: 96, fontWeight: 600, letterSpacing: -2, marginTop: 10 }}>
          {fragancia.nombre}
        </Aparecer>
        <Aparecer desde={32} style={{ fontSize: 44, fontWeight: 300, marginTop: 6 }}>
          {fragancia.notas}
        </Aparecer>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
