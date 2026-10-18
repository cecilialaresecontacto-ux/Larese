import { AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Botella } from "../../componentes/Botella";
import { fuente } from "../../fuentes";
import { Frasco } from "../frascos";
import { negro, resplandor, textoDorado, textoMetal } from "../estilo";

// Cada parte es texto o un frasco que ocupa el lugar de una letra
export type Parte = string | Frasco;

type Props = {
  partes: Parte[];
  tamano?: number;
  dorada?: boolean;
  // Las letras salen volando al final de la toma
  explotar?: boolean;
  debajo?: React.ReactNode;
};

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export const TomaPalabra: React.FC<Props> = ({ partes, tamano = 210, dorada = false, explotar = false, debajo }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const entrada = spring({ frame, fps, config: { damping: 200 }, durationInFrames: 12 });
  const salida = explotar
    ? interpolate(frame, [durationInFrames - 12, durationInFrames], [0, 1], clamp)
    : interpolate(frame, [durationInFrames - 5, durationInFrames], [0, 1], clamp);
  const zoom = interpolate(frame, [0, durationInFrames], [1, 1.06]);
  const altoFrasco = tamano * 1.9;

  const letra = (ch: string, indice: number, key: string) => {
    const dx = (random(`x${indice}`) - 0.5) * 1600 * salida;
    const dy = (random(`y${indice}`) - 0.5) * 1600 * salida;
    const giro = (random(`r${indice}`) - 0.5) * 200 * salida;
    return (
      <span
        key={key}
        style={{
          display: "inline-block",
          fontSize: tamano,
          fontWeight: 700,
          lineHeight: 1,
          letterSpacing: -tamano * 0.045,
          ...(dorada ? textoDorado : textoMetal),
          transform: explotar ? `translate(${dx}px, ${dy}px) rotate(${giro}deg) scale(${1 + salida})` : undefined,
          opacity: explotar ? 1 - salida : 1,
          filter: explotar ? `blur(${salida * 14}px)` : undefined,
        }}
      >
        {ch === " " ? "\u00a0" : ch}
      </span>
    );
  };

  let indice = 0;
  const contenido = partes.flatMap((p, i) => {
    if (typeof p === "string") {
      return p.split("").map((ch, j) => letra(ch, indice++, `${i}-${j}`));
    }
    const subida = spring({ frame: frame - 3, fps, config: { damping: 14, mass: 0.7 }, durationInFrames: 22 });
    return [
      <div
        key={`f-${i}`}
        style={{
          margin: `0 ${tamano * 0.1}px`,
          transform: `translateY(${interpolate(subida, [0, 1], [500, 0])}px)`,
          opacity: interpolate(subida, [0, 0.3], [0, 1], clamp),
        }}
      >
        <Botella imagen={p.imagen} alto={altoFrasco} proporcion={p.proporcion} inicioReflejo={10 + i * 3} />
      </div>,
    ];
  });

  return (
    <AbsoluteFill style={{ background: negro, fontFamily: fuente }}>
      <AbsoluteFill style={{ background: resplandor(0.18 * entrada) }} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            transform: `scale(${interpolate(entrada, [0, 1], [1.25, 1]) * zoom})`,
            filter: `blur(${interpolate(entrada, [0, 1], [24, 0]) + (explotar ? 0 : salida * 16)}px)`,
            opacity: entrada * (explotar ? 1 : 1 - salida),
          }}
        >
          {contenido}
        </div>
      </AbsoluteFill>
      {debajo ? (
        <AbsoluteFill
          style={{
            alignItems: "center",
            top: 960 + Math.max(tamano, altoFrasco) / 2 + 40,
            opacity: interpolate(frame, [8, 16], [0, 1], clamp) * (1 - salida),
          }}
        >
          {debajo}
        </AbsoluteFill>
      ) : null}
    </AbsoluteFill>
  );
};
