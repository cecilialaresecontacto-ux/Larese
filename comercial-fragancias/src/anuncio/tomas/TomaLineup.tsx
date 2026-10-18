import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { fuente } from "../../fuentes";
import { negro, textoMetal } from "../estilo";
import { frascos } from "../frascos";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const ALTO = 400;
const fila = [frascos.asad, frascos.yara, frascos.fakharBlack, frascos.fakharGold, frascos.attar];

// Todos los frascos en fila sobre un escenario, con reflejo en el piso
export const TomaLineup: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const luz = interpolate(frame, [0, 10], [0, 1], clamp);
  const salida = interpolate(frame, [durationInFrames - 5, durationInFrames], [0, 1], clamp);
  const titulo = spring({ frame: frame - 14, fps, config: { damping: 200 }, durationInFrames: 14 });

  return (
    <AbsoluteFill style={{ background: negro, fontFamily: fuente, opacity: 1 - salida }}>
      <AbsoluteFill
        style={{
          opacity: luz,
          background:
            "radial-gradient(ellipse 45% 60% at 50% 0%, rgba(255, 236, 200, 0.22) 0%, transparent 70%), radial-gradient(ellipse 60% 10% at 50% 66%, rgba(217, 178, 95, 0.35) 0%, transparent 70%)",
        }}
      />
      <AbsoluteFill style={{ alignItems: "center", top: 470 }}>
        <div
          style={{
            fontSize: 180,
            fontWeight: 700,
            letterSpacing: -8,
            ...textoMetal,
            opacity: titulo,
            filter: `blur(${interpolate(titulo, [0, 1], [16, 0])}px)`,
            transform: `scale(${interpolate(titulo, [0, 1], [1.15, 1])})`,
          }}
        >
          Decants.
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ flexDirection: "row", justifyContent: "center", alignItems: "flex-end", gap: 18, paddingBottom: 1920 - 1270 }}>
        {fila.map((f, i) => {
          const entrada = spring({ frame: frame - i * 3, fps, config: { damping: 15, mass: 0.6 }, durationInFrames: 24 });
          const ancho = ALTO * f.proporcion;
          return (
            <div
              key={f.imagen}
              style={{
                position: "relative",
                width: ancho,
                height: ALTO,
                opacity: interpolate(entrada, [0, 0.3], [0, 1], clamp),
                transform: `translateY(${interpolate(entrada, [0, 1], [120, 0])}px)`,
              }}
            >
              <Img src={staticFile(f.imagen)} style={{ width: ancho, height: ALTO }} />
              <Img
                src={staticFile(f.imagen)}
                style={{
                  position: "absolute",
                  top: ALTO + 4,
                  left: 0,
                  width: ancho,
                  height: ALTO,
                  transform: "scaleY(-1)",
                  opacity: 0.22,
                  WebkitMaskImage: "linear-gradient(0deg, black 0%, transparent 45%)",
                  maskImage: "linear-gradient(0deg, black 0%, transparent 45%)",
                }}
              />
            </div>
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
