import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../../componentes/Aparecer";
import { Decant } from "../../remate/componentes/Decant";
import { fuente } from "../../fuentes";
import { precios, Producto, productos, rosaPerfume } from "../marca";
import { Encabezado, Fondo, LogoArriba, Pie, Pildora, ProductoCentral } from "../Piezas";

const BLANCO = "#ffffff";
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Los 5 frascos en abanico, para la apertura y el cierre
const Abanico: React.FC<{ top: number; alto: number }> = ({ top, alto }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const centro = (productos.length - 1) / 2;
  return (
    <AbsoluteFill style={{ top }}>
      {productos.map((p, i) => {
        const desvio = i - centro;
        const entrada = spring({ frame: frame - 6 - i * 3, fps, config: { damping: 13, mass: 0.7 }, durationInFrames: 34 });
        const altoP = alto * (1 - Math.abs(desvio) * 0.12);
        const ancho = altoP * p.proporcion;
        return (
          <Img
            key={p.id}
            src={staticFile(p.imagen)}
            style={{
              position: "absolute",
              left: 540 - ancho / 2 + desvio * 175,
              top: alto - altoP + Math.abs(desvio) * 14,
              width: ancho,
              height: altoP,
              zIndex: 10 - Math.abs(desvio),
              filter: "drop-shadow(0 26px 26px rgba(0, 0, 0, 0.3))",
              opacity: interpolate(entrada, [0, 0.3], [0, 1], clamp),
              transform: `translateY(${interpolate(entrada, [0, 1], [500, 0]) + Math.sin((frame + i * 9) / 18) * 8}px) rotate(${desvio * 5}deg)`,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

const todas = productos.map((p) => ({ imagen: p.imagen, proporcion: p.proporcion }));

export const Apertura: React.FC = () => (
  <AbsoluteFill>
    <Fondo paleta={rosaPerfume} imagenes={todas} />
    <LogoArriba />
    <Encabezado etiqueta="Decants · 100% originales" titulo="Remate de decants" tamano={120} subtitulo="Perfumes árabes premium" />
    <Abanico top={760} alto={600} />
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 330 }}>
      <Pildora texto="Hasta agotar stock" paleta={rosaPerfume} />
    </AbsoluteFill>
    <Pie paleta={rosaPerfume} />
  </AbsoluteFill>
);

export const Tamanos: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill>
      <Fondo paleta={rosaPerfume} imagenes={[]} />
      <LogoArriba />
      <Encabezado etiqueta="Precios de remate" titulo="Elegí tu tamaño" subtitulo="Decant de perfume original" />
      <AbsoluteFill style={{ flexDirection: "row", justifyContent: "center", alignItems: "flex-end", gap: 120, paddingBottom: 560 }}>
        {precios.map((p, i) => {
          const entrada = spring({ frame: frame - 10 - i * 6, fps, config: { damping: 13, mass: 0.7 }, durationInFrames: 34 });
          const llenado = interpolate(frame, [20 + i * 6, 56 + i * 6], [0, 1], clamp);
          return (
            <div
              key={p.ml}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                fontFamily: fuente,
                color: BLANCO,
                opacity: interpolate(entrada, [0, 0.3], [0, 1], clamp),
                transform: `translateY(${interpolate(entrada, [0, 1], [400, 0])}px)`,
              }}
            >
              <Decant
                alto={i === 0 ? 330 : 460}
                llenado={llenado}
                liquido="linear-gradient(180deg, #ffffff, #fbe9ec)"
                tapa="linear-gradient(90deg, #6e3f46, #b98089 45%, #6e3f46)"
              />
              <div style={{ fontSize: 40, fontWeight: 500, marginTop: 40, letterSpacing: 2 }}>{p.ml} ML</div>
              <div style={{ fontSize: 88, fontWeight: 700, lineHeight: 1.05 }}>{p.precio}</div>
            </div>
          );
        })}
      </AbsoluteFill>
      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 330 }}>
        <Pildora texto="¡Pedí el tuyo!" paleta={rosaPerfume} desde={40} />
      </AbsoluteFill>
      <Pie paleta={rosaPerfume} desde={44} />
    </AbsoluteFill>
  );
};

export const Fragancia: React.FC<{ producto: Producto }> = ({ producto }) => {
  const { paleta } = producto;
  return (
    <AbsoluteFill>
      <Fondo paleta={paleta} imagenes={[producto]} />
      <LogoArriba />
      <Encabezado
        etiqueta={`Decant original · ${producto.marca}`}
        titulo={producto.nombre}
        subtitulo={producto.publico}
        tamano={producto.nombre.length > 10 ? 90 : 116}
      />
      <ProductoCentral imagen={producto.imagen} proporcion={producto.proporcion} alto={640} top={640} />
      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 450 }}>
        <Aparecer desde={18}>
          <div style={{ display: "flex", alignItems: "center", gap: 44, fontFamily: fuente, color: BLANCO, textAlign: "center" }}>
            {precios.map((p, i) => [
              i > 0 ? <div key={`s-${p.ml}`} style={{ width: 3, height: 110, background: "rgba(255, 255, 255, 0.6)" }} /> : null,
              <div key={p.ml}>
                <div style={{ fontSize: 32, fontWeight: 500, letterSpacing: 2 }}>{p.ml} ML</div>
                <div style={{ fontSize: 72, fontWeight: 700, lineHeight: 1.05 }}>{p.precio}</div>
              </div>,
            ])}
          </div>
        </Aparecer>
      </AbsoluteFill>
      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 330 }}>
        <Pildora texto="¡Pedí el tuyo!" paleta={paleta} desde={24} />
      </AbsoluteFill>
      <Pie paleta={paleta} desde={28} />
    </AbsoluteFill>
  );
};

export const Cierre: React.FC = () => (
  <AbsoluteFill>
    <Fondo paleta={rosaPerfume} imagenes={todas} />
    <LogoArriba />
    <Encabezado etiqueta="Remate de decants" titulo="¡Y muchos más!" tamano={120} subtitulo="Hasta agotar stock" />
    <Abanico top={720} alto={540} />
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 430, fontFamily: fuente, color: BLANCO, textAlign: "center" }}>
      <Aparecer desde={20} style={{ fontSize: 88, fontWeight: 700 }}>
        Desde Gs. 15.000
      </Aparecer>
    </AbsoluteFill>
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 330 }}>
      <Pildora texto="Escribinos por WhatsApp" paleta={rosaPerfume} desde={28} />
    </AbsoluteFill>
    <Pie paleta={rosaPerfume} desde={32} />
  </AbsoluteFill>
);
