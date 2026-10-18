import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { fuenteFlyer } from "../fuentes";
import { marca } from "../marca";
import { FlyerFragancia, precioTexto } from "./datos";
import { IconoInstagram, IconoReloj } from "./Iconos";

type Props = {
  fragancia: FlyerFragancia;
  usuario: string;
};

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const ALTO_PRODUCTO = 740;
const ALTO_LOGO = 46;

// Frascos desenfocados en las esquinas, como las frambuesas de la referencia
const flotantes = [
  { x: 70, y: 70, alto: 300, giro: -22, desenfoque: 5, desde: { x: -300, y: 0 } },
  { x: 700, y: -90, alto: 600, giro: 18, desenfoque: 12, desde: { x: 400, y: 0 } },
  { x: -130, y: 1240, alto: 560, giro: -14, desenfoque: 10, desde: { x: -400, y: 0 } },
];

export const Flyer: React.FC<Props> = ({ fragancia, usuario }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { color } = fragancia;
  const src = staticFile(fragancia.imagen);

  const producto = spring({ frame: frame - 6, fps, config: { damping: 12, mass: 0.8 }, durationInFrames: 40 });
  const flotar = Math.sin(frame / 18) * 12;
  const fondo = spring({ frame, fps, config: { damping: 200 }, durationInFrames: 30 });
  const pastilla = spring({ frame: frame - 30, fps, config: { damping: 10, mass: 0.6 }, durationInFrames: 30 });
  const tamanoTitulo = Math.min(190, 880 / (fragancia.titulo.length * 0.8));

  return (
    <AbsoluteFill
      style={{
        fontFamily: fuenteFlyer,
        color: marca.blanco,
        overflow: "hidden",
        background: `radial-gradient(circle at 78% 22%, color-mix(in srgb, ${color}, white 28%) 0%, ${color} 50%, color-mix(in srgb, ${color}, black 12%) 100%)`,
      }}
    >
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <div
          style={{
            fontSize: 600,
            fontWeight: 800,
            letterSpacing: -20,
            whiteSpace: "nowrap",
            color: "rgba(255, 255, 255, 0.2)",
            opacity: fondo,
            transform: `translate(${interpolate(frame, [0, 150], [90, -60])}px, 120px) rotate(-14deg)`,
          }}
        >
          {fragancia.titulo.toLowerCase()}
        </div>
      </AbsoluteFill>

      {flotantes.map((f, i) => {
        const entrada = spring({ frame: frame - i * 4, fps, config: { damping: 200 }, durationInFrames: 30 });
        const vaiven = Math.sin((frame + i * 25) / 22) * 14;
        return (
          <Img
            key={i}
            src={src}
            style={{
              position: "absolute",
              left: f.x + interpolate(entrada, [0, 1], [f.desde.x, 0]),
              top: f.y + vaiven,
              height: f.alto,
              width: f.alto * fragancia.proporcion,
              filter: `blur(${f.desenfoque}px)`,
              opacity: 0.85 * entrada,
              transform: `rotate(${f.giro + Math.sin(frame / 30 + i) * 3}deg)`,
            }}
          />
        );
      })}

      <AbsoluteFill style={{ alignItems: "center", top: 70 }}>
        <Aparecer desde={2}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <Img
              src={staticFile("marca/logo-blanco.png")}
              style={{ height: ALTO_LOGO, width: ALTO_LOGO * marca.logoProporcion }}
            />
            <div style={{ fontSize: 15, fontWeight: 600, letterSpacing: 14, marginRight: -14, marginTop: 8 }}>STORE</div>
          </div>
        </Aparecer>
      </AbsoluteFill>

      <AbsoluteFill style={{ top: 380, left: 110, right: 60, textShadow: "0 4px 24px rgba(0, 0, 0, 0.12)" }}>
        <Aparecer desde={8} style={{ fontSize: 44, fontWeight: 600, letterSpacing: 1 }}>
          {fragancia.antetitulo}
        </Aparecer>
        <Aparecer desde={12} style={{ fontSize: tamanoTitulo, fontWeight: 800, lineHeight: 0.95, letterSpacing: 2, marginTop: 4 }}>
          {fragancia.titulo}
        </Aparecer>
        <Aparecer desde={16} style={{ fontSize: 36, fontWeight: 600, letterSpacing: 1, marginTop: 14 }}>
          {fragancia.bajada}
        </Aparecer>
      </AbsoluteFill>

      <AbsoluteFill style={{ alignItems: "center", top: 690 }}>
        <div
          style={{
            opacity: interpolate(producto, [0, 0.3], [0, 1], clamp),
            transform: `translateY(${interpolate(producto, [0, 1], [400, 0]) + flotar}px) scale(${interpolate(producto, [0, 1], [0.85, 1])})`,
            filter: "drop-shadow(0 40px 40px rgba(0, 0, 0, 0.28))",
          }}
        >
          <Img src={src} style={{ height: ALTO_PRODUCTO, width: ALTO_PRODUCTO * fragancia.proporcion }} />
        </div>
      </AbsoluteFill>

      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 110 }}>
        <div
          style={{
            fontSize: 44,
            fontWeight: 600,
            whiteSpace: "pre",
            padding: "20px 48px",
            borderRadius: 999,
            background: `color-mix(in srgb, ${color}, black 30%)`,
            opacity: interpolate(pastilla, [0, 0.3], [0, 1], clamp),
            transform: `scale(${interpolate(pastilla, [0, 1], [0.6, 1])})`,
          }}
        >
          {precioTexto}
        </div>
        <Aparecer desde={38}>
          <div style={{ display: "flex", alignItems: "center", gap: 22, marginTop: 70, fontSize: 36, fontWeight: 500 }}>
            <IconoInstagram color={color} />
            <span>{usuario}</span>
            <div style={{ width: 40 }} />
            <IconoReloj color={color} />
            <span>Hasta agotar stock</span>
          </div>
        </Aparecer>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
