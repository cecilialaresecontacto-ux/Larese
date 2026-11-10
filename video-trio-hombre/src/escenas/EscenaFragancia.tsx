import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { Botella } from "../componentes/Botella";
import { Fragancia } from "../fragancias";
import { fuente } from "../fuentes";
import { marca } from "../marca";

const ALTO_LOGO = 56;

export const EscenaFragancia: React.FC<{ fragancia: Fragancia; numero: number }> = ({ fragancia, numero }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const entrada = spring({ frame, fps, config: { damping: 14, mass: 0.8 }, durationInFrames: 45 });
  const zoom = interpolate(frame, [0, durationInFrames], [1, 1.06]);
  const flotar = Math.sin(frame / 16) * 10;
  const giro = interpolate(entrada, [0, 1], [-5, 0]);
  const halo = 0.8 + 0.2 * Math.sin(frame / 10);
  const centroY = 330 + fragancia.alto / 2;

  return (
    <AbsoluteFill style={{ background: marca.fondo }}>
      <AbsoluteFill style={{ transform: `scale(${zoom})` }}>
        <div
          style={{
            position: "absolute",
            left: 540 - 430,
            top: centroY - 430,
            width: 860,
            height: 860,
            borderRadius: "50%",
            background: `radial-gradient(circle, ${marca.halo} 0%, transparent 66%)`,
            opacity: halo,
          }}
        />
        <AbsoluteFill style={{ alignItems: "center", top: 330 }}>
          <div
            style={{
              opacity: interpolate(entrada, [0, 0.4], [0, 1], { extrapolateRight: "clamp" }),
              transform: `translateY(${interpolate(entrada, [0, 1], [500, 0]) + flotar}px) rotate(${giro}deg) scale(${interpolate(entrada, [0, 1], [0.85, 1])})`,
            }}
          >
            <Botella imagen={fragancia.imagen} alto={fragancia.alto} proporcion={fragancia.proporcion} inicioReflejo={28} />
          </div>
        </AbsoluteFill>
      </AbsoluteFill>

      <AbsoluteFill style={{ alignItems: "center", top: 170 }}>
        <Aparecer desde={6}>
          <Img src={staticFile(marca.logo)} style={{ height: ALTO_LOGO, width: ALTO_LOGO * marca.logoProporcion }} />
        </Aparecer>
      </AbsoluteFill>

      <AbsoluteFill
        style={{
          justifyContent: "flex-end",
          alignItems: "center",
          paddingBottom: 230,
          textAlign: "center",
          color: marca.negro,
          fontFamily: fuente,
        }}
      >
        <Aparecer desde={14}>
          <div
            style={{
              fontSize: 28,
              letterSpacing: 6,
              fontWeight: 600,
              background: marca.negro,
              color: marca.blanco,
              padding: "10px 28px",
              borderRadius: 999,
            }}
          >
            {`0${numero} · DECANT 5 ML`}
          </div>
        </Aparecer>
        <Aparecer desde={20} style={{ fontSize: 36, fontWeight: 500, color: marca.gris, marginTop: 24, letterSpacing: 2 }}>
          {fragancia.marca.toUpperCase()}
        </Aparecer>
        <Aparecer desde={24} style={{ fontSize: 84, fontWeight: 700, letterSpacing: -2, lineHeight: 1.05, marginTop: 6, maxWidth: 980 }}>
          {fragancia.nombre}
        </Aparecer>
        <Aparecer desde={32} style={{ fontSize: 44, fontWeight: 300, marginTop: 12 }}>
          {fragancia.notas}
        </Aparecer>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
