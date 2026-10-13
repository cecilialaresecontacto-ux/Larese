import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { Botella } from "../componentes/Botella";
import { Destellos } from "../componentes/Destellos";
import { Fragancia } from "../fragancias";
import { sans, serif } from "../fuentes";

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
        <Destellos cantidad={55} semilla={`${fragancia.id}-atras`} color="#fbe3a6" />
        <AbsoluteFill style={{ alignItems: "center", top: 250 }}>
          <div
            style={{
              opacity: interpolate(entrada, [0, 0.4], [0, 1], { extrapolateRight: "clamp" }),
              transform: `translateY(${interpolate(entrada, [0, 1], [500, 0]) + flotar}px) rotate(${giro}deg) scale(${interpolate(entrada, [0, 1], [0.85, 1])})`,
            }}
          >
            <Botella imagen={fragancia.imagen} alto={1000} proporcion={fragancia.proporcion} inicioReflejo={28} />
          </div>
        </AbsoluteFill>
        <Destellos cantidad={25} semilla={`${fragancia.id}-frente`} color="#fff1c4" />
      </AbsoluteFill>

      <AbsoluteFill
        style={{
          justifyContent: "flex-end",
          alignItems: "center",
          paddingBottom: 170,
          textAlign: "center",
          color: fragancia.texto,
        }}
      >
        <Aparecer desde={18} style={{ fontFamily: sans, fontSize: 28, letterSpacing: 10, fontWeight: 500, opacity: 0.8 }}>
          {`0${numero} · SHIMMER`}
        </Aparecer>
        <Aparecer desde={24} style={{ fontFamily: serif, fontSize: 108, fontWeight: 600, marginTop: 14 }}>
          {fragancia.nombre}
        </Aparecer>
        <Aparecer desde={32} style={{ fontFamily: serif, fontStyle: "italic", fontSize: 52, marginTop: 10 }}>
          {fragancia.notas}
        </Aparecer>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
