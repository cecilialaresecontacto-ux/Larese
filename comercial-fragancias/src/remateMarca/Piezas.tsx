import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { fuente } from "../fuentes";
import { ENVIOS, Paleta, WHATSAPP } from "./marca";

const BLANCO = "#ffffff";
const LOGO_PROPORCION = 612 / 133;
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Fondo de marca: degradado de un color y el logo gigante transparente
export const Fondo: React.FC<{ paleta: Paleta; centroMarca?: number }> = ({ paleta, centroMarca = 980 }) => {
  const frame = useCurrentFrame();
  const anchoMarca = 1080 * 1.75;

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse 75% 60% at 50% 50%, ${paleta.centro} 0%, ${paleta.borde} 100%)`,
        overflow: "hidden",
      }}
    >
      <Img
        src={staticFile("marca/logo-store-blanco.png")}
        style={{
          position: "absolute",
          left: -1080 * 0.2 + interpolate(frame, [0, 150], [30, -30]),
          top: centroMarca - anchoMarca / LOGO_PROPORCION / 2,
          width: anchoMarca,
          height: anchoMarca / LOGO_PROPORCION,
          opacity: 0.14,
        }}
      />
    </AbsoluteFill>
  );
};

export const LogoArriba: React.FC = () => (
  <AbsoluteFill style={{ alignItems: "center", top: 170 }}>
    <Aparecer desde={0}>
      <Img src={staticFile("marca/logo-store-blanco.png")} style={{ width: 250, height: 250 / LOGO_PROPORCION }} />
    </Aparecer>
  </AbsoluteFill>
);

// Etiqueta, título y subtítulo centrados, como en las piezas del skill
export const Encabezado: React.FC<{ etiqueta?: string; titulo: string; subtitulo?: string; tamano?: number }> = ({
  etiqueta,
  titulo,
  subtitulo,
  tamano = 116,
}) => (
  <AbsoluteFill style={{ alignItems: "center", top: 300, textAlign: "center", color: BLANCO, fontFamily: fuente, padding: "0 65px" }}>
    {etiqueta ? (
      <Aparecer desde={4} style={{ fontSize: 34, fontWeight: 600, letterSpacing: 34 * 0.06 }}>
        {etiqueta.toUpperCase()}
      </Aparecer>
    ) : null}
    <Aparecer desde={8} style={{ fontSize: tamano, fontWeight: 700, lineHeight: 1.05, marginTop: 6 }}>
      {titulo.toUpperCase()}
    </Aparecer>
    {subtitulo ? (
      <Aparecer desde={12} style={{ fontSize: 32, fontWeight: 500, letterSpacing: 32 * 0.04, marginTop: 14 }}>
        {subtitulo.toUpperCase()}
      </Aparecer>
    ) : null}
  </AbsoluteFill>
);

// Foto del producto como tarjeta redondeada con sombra, que sube y queda flotando
export const FotoCentral: React.FC<{ imagen: string; proporcion: number; ancho: number; top: number; desde?: number }> = ({
  imagen,
  proporcion,
  ancho,
  top,
  desde = 4,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const entrada = spring({ frame: frame - desde, fps, config: { damping: 13, mass: 0.8 }, durationInFrames: 36 });

  return (
    <AbsoluteFill style={{ alignItems: "center", top }}>
      <Img
        src={staticFile(imagen)}
        style={{
          width: ancho,
          height: ancho / proporcion,
          borderRadius: 48,
          boxShadow: "0 30px 60px rgba(0, 0, 0, 0.28)",
          opacity: interpolate(entrada, [0, 0.3], [0, 1], clamp),
          transform: `translateY(${interpolate(entrada, [0, 1], [380, 0]) + Math.sin(frame / 18) * 8}px) scale(${interpolate(entrada, [0, 1], [0.88, 1])})`,
        }}
      />
    </AbsoluteFill>
  );
};

export const Pildora: React.FC<{ texto: string; paleta: Paleta; desde?: number }> = ({ texto, paleta, desde = 26 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame: frame - desde, fps, config: { damping: 10, mass: 0.6 }, durationInFrames: 30 });
  return (
    <div
      style={{
        fontFamily: fuente,
        fontSize: 40,
        fontWeight: 600,
        color: BLANCO,
        padding: "18px 44px",
        borderRadius: 999,
        background: `color-mix(in srgb, ${paleta.oscuro} 84%, transparent)`,
        opacity: interpolate(pop, [0, 0.3], [0, 1], clamp),
        transform: `scale(${interpolate(pop, [0, 1], [0.6, 1])})`,
      }}
    >
      {texto}
    </div>
  );
};

const Circulo: React.FC<{ paleta: Paleta; children: React.ReactNode }> = ({ paleta, children }) => (
  <svg width={63} height={63} viewBox="0 0 64 64">
    <circle cx={32} cy={32} r={32} fill={paleta.oscuro} />
    {children}
  </svg>
);

// Pie con WhatsApp y envíos, como el que agrega el script del skill
export const Pie: React.FC<{ paleta: Paleta; desde?: number }> = ({ paleta, desde = 32 }) => (
  <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 190 }}>
    <Aparecer desde={desde}>
      <div style={{ display: "flex", alignItems: "center", gap: 18, fontFamily: fuente, fontSize: 30, fontWeight: 500, color: BLANCO }}>
        <Circulo paleta={paleta}>
          <g fill="none" stroke={BLANCO} strokeWidth={3.5}>
            <ellipse cx={32} cy={31} rx={14} ry={13.5} />
          </g>
          <path d="M21 37 L17 47 L28 42 Z" fill={BLANCO} />
          {[26, 32, 38].map((x) => (
            <circle key={x} cx={x} cy={31} r={1.8} fill={BLANCO} />
          ))}
        </Circulo>
        <span>{WHATSAPP}</span>
        <div style={{ width: 42 }} />
        <Circulo paleta={paleta}>
          <g fill={BLANCO}>
            <rect x={13} y={22} width={22} height={16} />
            <path d="M37 26 H45 L51 32 V38 H37 Z" />
            <circle cx={21} cy={41} r={4.5} />
            <circle cx={44} cy={41} r={4.5} />
          </g>
        </Circulo>
        <span>{ENVIOS}</span>
      </div>
    </Aparecer>
  </AbsoluteFill>
);
