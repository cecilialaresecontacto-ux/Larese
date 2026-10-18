import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { fuente } from "../fuentes";
import { ENVIOS, Paleta, WHATSAPP } from "./marca";

const BLANCO = "#ffffff";
const LOGO_PROPORCION = 612 / 133;
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

type Imagen = { imagen: string; proporcion: number };

// Copias grandes y desenfocadas en las esquinas: x, y y ancho relativos, giro, desenfoque
const esquinas = [
  { x: -0.1, y: 0.05, ancho: 0.32, giro: 18, desenfoque: 10 },
  { x: 0.74, y: -0.03, ancho: 0.42, giro: -22, desenfoque: 18 },
  { x: -0.14, y: 0.7, ancho: 0.38, giro: -14, desenfoque: 14 },
  { x: 0.8, y: 0.8, ancho: 0.3, giro: 25, desenfoque: 9 },
];

// Fondo de marca: degradado de un color, logo gigante transparente y frascos desenfocados
export const Fondo: React.FC<{ paleta: Paleta; imagenes: Imagen[]; centroMarca?: number }> = ({
  paleta,
  imagenes,
  centroMarca = 980,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
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
      {imagenes.length > 0
        ? esquinas.map((e, i) => {
            const im = imagenes[i % imagenes.length];
            const entrada = spring({ frame: frame - i * 3, fps, config: { damping: 200 }, durationInFrames: 30 });
            const ancho = 1080 * e.ancho;
            const alto = Math.min(ancho * 1.6, ancho / im.proporcion);
            return (
              <Img
                key={i}
                src={staticFile(im.imagen)}
                style={{
                  position: "absolute",
                  left: 1080 * e.x + interpolate(entrada, [0, 1], [e.x < 0.5 ? -200 : 200, 0]),
                  top: 1920 * e.y + Math.sin((frame + i * 20) / 24) * 14,
                  width: alto * im.proporcion,
                  height: alto,
                  filter: `blur(${e.desenfoque}px)`,
                  opacity: entrada,
                  transform: `rotate(${-e.giro + Math.sin(frame / 30 + i) * 3}deg)`,
                }}
              />
            );
          })
        : null}
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

// Producto recortado con sombra suave, que sube y queda flotando
export const ProductoCentral: React.FC<Imagen & { alto: number; top: number; desde?: number }> = ({
  imagen,
  proporcion,
  alto,
  top,
  desde = 4,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const entrada = spring({ frame: frame - desde, fps, config: { damping: 13, mass: 0.8 }, durationInFrames: 36 });
  const ancho = alto * proporcion;

  return (
    <AbsoluteFill style={{ alignItems: "center", top }}>
      <div
        style={{
          position: "relative",
          width: ancho,
          height: alto,
          opacity: interpolate(entrada, [0, 0.3], [0, 1], clamp),
          transform: `translateY(${interpolate(entrada, [0, 1], [380, 0])}px) scale(${interpolate(entrada, [0, 1], [0.88, 1])})`,
        }}
      >
        <div
          style={{
            position: "absolute",
            left: ancho * 0.125,
            width: ancho * 0.75,
            bottom: -26,
            height: 52,
            borderRadius: "50%",
            background: "rgba(0, 0, 0, 0.32)",
            filter: "blur(22px)",
          }}
        />
        <Img
          src={staticFile(imagen)}
          style={{ position: "absolute", width: ancho, height: alto, transform: `translateY(${Math.sin(frame / 18) * 10}px)` }}
        />
      </div>
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
