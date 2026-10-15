import {
  AbsoluteFill,
  Img,
  interpolate,
  OffthreadVideo,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { fuente } from "../fuentes";
import { marca } from "../marca";
import { DURACION_CIERRE, DURACION_FOTO, fotoFinal, Toma, tomas } from "./tomas";

export type DecantsProps = {
  titulo: string;
  subtitulo: string;
  frase: string;
  usuario: string;
  llamado: string;
};

export const DURACION_DECANTS =
  tomas.reduce((total, t) => total + t.duracion, 0) + DURACION_FOTO + DURACION_CIERRE;

const sombra = "0 4px 24px rgba(0, 0, 0, 0.45), 0 2px 6px rgba(0, 0, 0, 0.35)";

// Golpe de zoom y destello blanco al entrar a cada toma
const Corte: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const golpe = spring({ frame, fps, config: { damping: 18, mass: 0.6 }, durationInFrames: 12 });

  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ transform: `scale(${interpolate(golpe, [0, 1], [1.12, 1.02]) + frame * 0.0006})` }}>
        {children}
      </AbsoluteFill>
      <AbsoluteFill
        style={{
          backgroundColor: marca.blanco,
          opacity: interpolate(frame, [0, 5], [0.55, 0], { extrapolateRight: "clamp" }),
        }}
      />
    </AbsoluteFill>
  );
};

const Clip: React.FC<{ toma: Toma }> = ({ toma }) => {
  const { fps } = useVideoConfig();
  const fin = toma.duracion;

  return (
    <OffthreadVideo
      src={staticFile(toma.clip)}
      trimBefore={Math.round(toma.desde * fps)}
      playbackRate={toma.velocidad}
      // Fundido corto del sonido ambiente para que no haga "clic" en los cortes
      volume={(f) => interpolate(f, [0, 3, fin - 3, fin], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}
      style={{ width: "100%", height: "100%", objectFit: "cover" }}
    />
  );
};

// Nombre del perfume en el tercio superior (fuera de los botones de Instagram y TikTok)
const Rotulo: React.FC<{ marcaPerfume: string; nombre: string }> = ({ marcaPerfume, nombre }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const entrada = spring({ frame: frame - 4, fps, config: { damping: 14 }, durationInFrames: 18 });

  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 330, fontFamily: fuente, color: marca.blanco, textAlign: "center" }}>
      <div
        style={{
          fontSize: 30,
          fontWeight: 600,
          letterSpacing: 12,
          paddingLeft: 12,
          textShadow: sombra,
          opacity: entrada,
          transform: `translateY(${interpolate(entrada, [0, 1], [-30, 0])}px)`,
        }}
      >
        {marcaPerfume}
      </div>
      <div
        style={{
          fontSize: 92,
          fontWeight: 700,
          letterSpacing: -2,
          lineHeight: 1.05,
          marginTop: 8,
          textShadow: sombra,
          opacity: entrada,
          transform: `scale(${interpolate(entrada, [0, 1], [0.7, 1])})`,
        }}
      >
        {nombre}
      </div>
      <div
        style={{
          marginTop: 22,
          fontSize: 30,
          fontWeight: 600,
          letterSpacing: 4,
          color: marca.negro,
          background: marca.blanco,
          padding: "10px 26px",
          borderRadius: 999,
          transform: `scale(${spring({ frame: frame - 12, fps, config: { damping: 10 }, durationInFrames: 16 })})`,
        }}
      >
        3 ML
      </div>
    </AbsoluteFill>
  );
};

// Gancho de los primeros 2 segundos
const Gancho: React.FC<{ titulo: string; subtitulo: string }> = ({ titulo, subtitulo }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const palabras = subtitulo.split(" ");

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        paddingBottom: 380,
        fontFamily: fuente,
        color: marca.blanco,
        textAlign: "center",
        textShadow: sombra,
      }}
    >
      <Aparecer desde={0} style={{ fontSize: 40, fontWeight: 600, letterSpacing: 14, paddingLeft: 14 }}>
        {titulo}
      </Aparecer>
      <div style={{ display: "flex", gap: 24, marginTop: 6 }}>
        {palabras.map((p, i) => {
          const s = spring({ frame: frame - 6 - i * 5, fps, config: { damping: 9, mass: 0.6 }, durationInFrames: 18 });
          return (
            <span key={i} style={{ fontSize: 116, fontWeight: 700, letterSpacing: -3, display: "inline-block", transform: `scale(${s})` }}>
              {p}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const FraseIntermedia: React.FC<{ frase: string }> = ({ frase }) => (
  <AbsoluteFill
    style={{
      justifyContent: "center",
      alignItems: "center",
      paddingBottom: 300,
      paddingLeft: 90,
      paddingRight: 90,
      fontFamily: fuente,
      color: marca.blanco,
      textAlign: "center",
      textShadow: sombra,
    }}
  >
    <Aparecer desde={3} style={{ fontSize: 76, fontWeight: 700, lineHeight: 1.1, letterSpacing: -1, whiteSpace: "pre-line" }}>
      {frase}
    </Aparecer>
  </AbsoluteFill>
);

// Foto de los decants listos, con zoom lento
const Resultado: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const zoom = interpolate(frame, [0, DURACION_FOTO], [1.0, 1.14]);
  const sello = spring({ frame: frame - 10, fps, config: { damping: 10 }, durationInFrames: 20 });

  return (
    <Corte>
      <AbsoluteFill style={{ transform: `scale(${zoom})`, transformOrigin: "50% 70%" }}>
        <Img src={staticFile(fotoFinal)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </AbsoluteFill>
      <AbsoluteFill style={{ alignItems: "center", paddingTop: 330, fontFamily: fuente, textAlign: "center" }}>
        <div
          style={{
            fontSize: 110,
            fontWeight: 700,
            letterSpacing: -3,
            color: marca.blanco,
            textShadow: sombra,
            transform: `scale(${sello}) rotate(${interpolate(sello, [0, 1], [-8, -3])}deg)`,
          }}
        >
          ¡Listos! ✨
        </div>
      </AbsoluteFill>
    </Corte>
  );
};

const Cierre: React.FC<{ usuario: string; llamado: string }> = ({ usuario, llamado }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const logo = spring({ frame, fps, config: { damping: 12, mass: 0.7 }, durationInFrames: 22 });
  const latido = 1 + 0.035 * Math.sin(frame / 4);
  const ancho = 720;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: marca.blanco,
        justifyContent: "center",
        alignItems: "center",
        paddingBottom: 200,
        fontFamily: fuente,
        color: marca.negro,
        textAlign: "center",
      }}
    >
      <Img
        src={staticFile(marca.logo)}
        style={{
          width: ancho,
          height: ancho / marca.logoProporcion,
          transform: `scale(${interpolate(logo, [0, 1], [0.6, 1])})`,
          opacity: logo,
        }}
      />
      <Aparecer desde={8} style={{ fontSize: 34, fontWeight: 500, letterSpacing: 10, paddingLeft: 10, marginTop: 40 }}>
        DECANTS · 3 ML
      </Aparecer>
      <Aparecer desde={14} style={{ fontSize: 44, fontWeight: 600, marginTop: 70 }}>
        {usuario}
      </Aparecer>
      <Aparecer desde={20} style={{ marginTop: 30 }}>
        <div
          style={{
            fontWeight: 600,
            fontSize: 42,
            letterSpacing: 1,
            color: marca.blanco,
            background: marca.negro,
            padding: "26px 64px",
            borderRadius: 999,
            transform: `scale(${latido})`,
          }}
        >
          {llamado}
        </div>
      </Aparecer>
    </AbsoluteFill>
  );
};

// Logo chico arriba a la izquierda durante las tomas
const MarcaDeAgua: React.FC = () => (
  <AbsoluteFill style={{ padding: "120px 0 0 70px" }}>
    <Img
      src={staticFile(marca.logo)}
      style={{
        width: 230,
        height: 230 / marca.logoProporcion,
        filter: "invert(1) drop-shadow(0 2px 8px rgba(0, 0, 0, 0.5))",
        opacity: 0.92,
      }}
    />
  </AbsoluteFill>
);

export const Decants: React.FC<DecantsProps> = ({ titulo, subtitulo, frase, usuario, llamado }) => {
  let inicio = 0;
  const secuencias = tomas.map((toma, i) => {
    const desde = inicio;
    inicio += toma.duracion;
    const esPrimera = i === 0;
    const esUltima = i === tomas.length - 1;

    return (
      <Sequence key={toma.clip} from={desde} durationInFrames={toma.duracion}>
        <Corte>
          <Clip toma={toma} />
        </Corte>
        {esPrimera ? <Gancho titulo={titulo} subtitulo={subtitulo} /> : null}
        {toma.marca && toma.nombre ? <Rotulo marcaPerfume={toma.marca} nombre={toma.nombre} /> : null}
        {esUltima ? <FraseIntermedia frase={frase} /> : null}
      </Sequence>
    );
  });
  const finTomas = inicio;

  return (
    <AbsoluteFill style={{ backgroundColor: marca.negro }}>
      {secuencias}
      <Sequence from={finTomas} durationInFrames={DURACION_FOTO}>
        <Resultado />
      </Sequence>
      <Sequence durationInFrames={finTomas + DURACION_FOTO}>
        <MarcaDeAgua />
      </Sequence>
      <Sequence from={finTomas + DURACION_FOTO} durationInFrames={DURACION_CIERRE}>
        <Cierre usuario={usuario} llamado={llamado} />
      </Sequence>
    </AbsoluteFill>
  );
};
