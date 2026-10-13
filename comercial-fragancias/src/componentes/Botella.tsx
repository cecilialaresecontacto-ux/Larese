import { Img, interpolate, staticFile, useCurrentFrame } from "remotion";

type Props = {
  imagen: string;
  alto: number;
  proporcion: number;
  // Frame en el que pasa el reflejo de luz por la botella
  inicioReflejo?: number;
};

export const Botella: React.FC<Props> = ({
  imagen,
  alto,
  proporcion,
  inicioReflejo = 30,
}) => {
  const frame = useCurrentFrame();
  const ancho = alto * proporcion;
  const src = staticFile(imagen);

  const reflejo = interpolate(frame, [inicioReflejo, inicioReflejo + 35], [-60, 160], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div style={{ position: "relative", width: ancho, height: alto }}>
      <div
        style={{
          position: "absolute",
          left: "-10%",
          right: "-10%",
          bottom: -alto * 0.03,
          height: alto * 0.06,
          borderRadius: "50%",
          background: "rgba(60, 30, 20, 0.35)",
          filter: "blur(18px)",
        }}
      />
      <Img src={src} style={{ width: ancho, height: alto, position: "absolute" }} />
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: `linear-gradient(105deg, transparent ${reflejo - 25}%, rgba(255,255,255,0.75) ${reflejo}%, transparent ${reflejo + 25}%)`,
          mixBlendMode: "screen",
          WebkitMaskImage: `url(${src})`,
          WebkitMaskSize: "100% 100%",
          maskImage: `url(${src})`,
          maskSize: "100% 100%",
        }}
      />
    </div>
  );
};
