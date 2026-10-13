import { AbsoluteFill, random, useCurrentFrame, useVideoConfig } from "remotion";

type Props = {
  cantidad?: number;
  color?: string;
  semilla?: string;
};

const Estrella: React.FC<{ size: number; color: string }> = ({ size, color }) => (
  <svg width={size} height={size} viewBox="-10 -10 20 20">
    <path
      d="M0 -10 Q1.2 -1.2 10 0 Q1.2 1.2 0 10 Q-1.2 1.2 -10 0 Q-1.2 -1.2 0 -10Z"
      fill={color}
    />
  </svg>
);

// Partículas doradas que suben y titilan, como el brillo del body mist
export const Destellos: React.FC<Props> = ({
  cantidad = 70,
  color = "#f7d58b",
  semilla = "destellos",
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {new Array(cantidad).fill(true).map((_, i) => {
        const r = (k: string) => random(`${semilla}-${i}-${k}`);
        const esEstrella = r("tipo") > 0.75;
        const size = esEstrella ? 22 + r("s") * 34 : 4 + r("s") * 9;
        const velocidad = 0.6 + r("v") * 1.8;
        const recorrido = height + 200;
        const y = (((r("y") * recorrido - frame * velocidad) % recorrido) + recorrido) % recorrido - 100;
        const x = r("x") * width + Math.sin(frame / (20 + r("o") * 30) + r("f") * 6) * 18;
        const titileo = 0.25 + 0.75 * Math.abs(Math.sin(frame / (6 + r("t") * 10) + r("p") * 10));

        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x,
              top: y,
              opacity: titileo,
              filter: `drop-shadow(0 0 ${size / 2}px ${color})`,
            }}
          >
            {esEstrella ? (
              <Estrella size={size} color={color} />
            ) : (
              <div
                style={{
                  width: size,
                  height: size,
                  borderRadius: "50%",
                  background: color,
                }}
              />
            )}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
