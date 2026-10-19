import { createContext, useContext } from "react";
import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Aparecer } from "../componentes/Aparecer";
import { fuente } from "../fuentes";
import { Decant } from "../remate/componentes/Decant";
import { Paleta } from "../remateMarca/marca";
import { Encabezado, Fondo, HISTORIA, LogoArriba, Medidas, Pie, Pildora, POST } from "../remateMarca/Piezas";

const BLANCO = "#ffffff";
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Rosa empolvado de la categoría perfume, del skill de anuncios de Larese
const rosa: Paleta = { color: "#ce8690", oscuro: "#955a62", centro: "#df9fa8", borde: "#bc7a83" };

type Foto = { imagen: string; proporcion: number };

const fotos: Foto[] = [
  { imagen: "decants/versace-bright-crystal.jpg", proporcion: 375 / 500 },
  { imagen: "decants/coco-mademoiselle.jpg", proporcion: 1 },
  { imagen: "decants/miss-dior.jpg", proporcion: 1 },
];

const vialBlanco = {
  liquido: "linear-gradient(180deg, #ffffff, #fbe9ec)",
  tapa: "linear-gradient(90deg, #6e3f46, #b98089 45%, #6e3f46)",
};

// Versión sin marcas: sin fotos ni nombres de otras marcas, para que Meta no la rechace por propiedad intelectual
const SinMarcas = createContext(false);

// Tres frasquitos de decant, en lugar de las fotos de marcas
const Viales: React.FC<{ top: number; alto: number }> = ({ top, alto }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ top, flexDirection: "row", justifyContent: "center", alignItems: "flex-start", gap: alto * 0.28 }}>
      {[0.72, 1, 0.84].map((escala, i) => {
        const entrada = spring({ frame: frame - 6 - i * 3, fps, config: { damping: 13, mass: 0.7 }, durationInFrames: 34 });
        return (
          <div
            key={i}
            style={{
              marginTop: alto * (1 - escala),
              opacity: interpolate(entrada, [0, 0.3], [0, 1], clamp),
              transform: `translateY(${interpolate(entrada, [0, 1], [300, 0])}px)`,
            }}
          >
            <Decant alto={alto * escala} llenado={interpolate(frame, [16 + i * 5, 52 + i * 5], [0, 1], clamp)} {...vialBlanco} />
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// Fotos originales como tarjetas en abanico
const Tarjetas: React.FC<{ top: number; alto: number; separacion: number }> = ({ top, alto, separacion }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (useContext(SinMarcas)) {
    return <Viales top={top} alto={alto} />;
  }
  return (
    <AbsoluteFill style={{ top }}>
      {fotos.map((f, i) => {
        const desvio = i - 1;
        const entrada = spring({ frame: frame - 6 - i * 3, fps, config: { damping: 13, mass: 0.7 }, durationInFrames: 34 });
        const ancho = alto * f.proporcion;
        return (
          <Img
            key={f.imagen}
            src={staticFile(f.imagen)}
            style={{
              position: "absolute",
              left: 540 - ancho / 2 + desvio * separacion,
              top: Math.abs(desvio) * 30,
              width: ancho,
              height: alto,
              borderRadius: 32,
              zIndex: desvio === 0 ? 2 : 1,
              boxShadow: "0 24px 50px rgba(0, 0, 0, 0.25)",
              opacity: interpolate(entrada, [0, 0.3], [0, 1], clamp),
              transform: `translateY(${interpolate(entrada, [0, 1], [400, 0])}px) rotate(${desvio * 7}deg)`,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

const Texto: React.FC<{ top: number; children: React.ReactNode; tamano?: number }> = ({ top, children, tamano = 36 }) => (
  <AbsoluteFill style={{ top, alignItems: "center" }}>
    <Aparecer
      desde={14}
      style={{ maxWidth: 860, textAlign: "center", fontFamily: fuente, fontSize: tamano, fontWeight: 500, lineHeight: 1.4, color: BLANCO }}
    >
      {children}
    </Aparecer>
  </AbsoluteFill>
);

const Base: React.FC<{
  m: Medidas;
  centroMarca: number;
  etiqueta: string;
  titulo: string;
  subtitulo?: string;
  tamano?: number;
  cta: string;
  ctaAbajo: number;
  children: React.ReactNode;
}> = ({ m, centroMarca, etiqueta, titulo, subtitulo, tamano = 92, cta, ctaAbajo, children }) => (
  <AbsoluteFill>
    <Fondo paleta={rosa} centroMarca={centroMarca} />
    <LogoArriba m={m} />
    <Encabezado m={m} etiqueta={etiqueta} titulo={titulo} subtitulo={subtitulo} tamano={tamano} />
    {children}
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: ctaAbajo }}>
      <Pildora texto={cta} paleta={rosa} desde={24} m={m} />
    </AbsoluteFill>
    <Pie paleta={rosa} m={m} />
  </AbsoluteFill>
);

const Slide: React.FC<Omit<React.ComponentProps<typeof Base>, "m" | "centroMarca" | "ctaAbajo">> = (props) => (
  <Base m={POST} centroMarca={690} ctaAbajo={150} {...props} />
);

const Portada: React.FC = () => (
  <Slide etiqueta="Guía Larese" titulo="¿Decant o frasco entero?" subtitulo="5 razones para empezar por un decant" cta="Deslizá para verlas 👉">
    <Tarjetas top={540} alto={380} separacion={250} />
  </Slide>
);

const Razon1: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Slide etiqueta="Razón 01" titulo="Probalo en tu piel" tamano={78} cta="¡Pedí el tuyo!">
      <Texto top={350}>
        Un perfume cambia en cada piel. Con un decant lo usás varios días antes de invertir en el frasco completo.
      </Texto>
      <AbsoluteFill style={{ top: 600, alignItems: "center" }}>
        <Decant alto={400} llenado={interpolate(frame, [14, 50], [0, 1], clamp)} {...vialBlanco} />
      </AbsoluteFill>
    </Slide>
  );
};

const Razon2: React.FC = () => {
  const sinMarcas = useContext(SinMarcas);
  return (
    <Slide etiqueta="Razón 02" titulo="Pagás mucho menos" tamano={78} cta="¡Pedí el tuyo!">
      <Texto top={350}>Perfumes de lujo 100% originales, sin gastar de una el precio de un frasco completo.</Texto>
      <AbsoluteFill style={{ top: 640, alignItems: "center", textAlign: "center", fontFamily: fuente, color: BLANCO }}>
        <Aparecer desde={20} style={{ fontSize: 30, fontWeight: 500, letterSpacing: 2 }}>
          {sinMarcas ? "DECANTS DE 5 Y 10 ML" : "POR EJEMPLO, VERSACE BRIGHT CRYSTAL 5 ML"}
        </Aparecer>
        <Aparecer desde={24} style={{ fontSize: sinMarcas ? 96 : 120, fontWeight: 700, lineHeight: 1.1, marginTop: 10 }}>
          {sinMarcas ? "Una fracción del precio" : "Gs. 45.000"}
        </Aparecer>
      </AbsoluteFill>
    </Slide>
  );
};

const Razon3: React.FC = () => (
  <Slide etiqueta="Razón 03" titulo="Armá tu colección" tamano={78} cta="¡Pedí el tuyo!">
    <Texto top={350}>Con lo que cuesta un frasco tenés varios perfumes: uno para el día, otro para la noche y otro para salir.</Texto>
    <Tarjetas top={630} alto={330} separacion={230} />
  </Slide>
);

const Razon4: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Slide etiqueta="Razón 04" titulo="Llevalo a todos lados" tamano={78} cta="¡Pedí el tuyo!">
      <Texto top={430}>Entra en la cartera, en el auto o en la valija. Retocás tu perfume cuando quieras.</Texto>
      <AbsoluteFill style={{ flexDirection: "row", justifyContent: "center", alignItems: "flex-end", gap: 110, paddingBottom: 320 }}>
        {[
          { ml: 5, alto: 260 },
          { ml: 10, alto: 360 },
        ].map((v, i) => (
          <div key={v.ml} style={{ display: "flex", flexDirection: "column", alignItems: "center", fontFamily: fuente, color: BLANCO }}>
            <Decant alto={v.alto} llenado={interpolate(frame, [14 + i * 6, 50 + i * 6], [0, 1], clamp)} {...vialBlanco} />
            <div style={{ fontSize: 40, fontWeight: 700, marginTop: 20 }}>{v.ml} ML</div>
          </div>
        ))}
      </AbsoluteFill>
    </Slide>
  );
};

const Razon5: React.FC = () => (
  <Slide etiqueta="Razón 05" titulo="El mismo perfume original" tamano={78} cta="¡Pedí el tuyo!">
    <Texto top={440}>Es perfume 100% original, pasado de su frasco a uno de 5 o 10 ml. El mismo aroma, en un tamaño más práctico.</Texto>
    <AbsoluteFill style={{ top: 700, alignItems: "center" }}>
      <Aparecer desde={20}>
        <div style={{ position: "relative" }}>
          {useContext(SinMarcas) ? (
            <div style={{ width: 360, height: 360, display: "flex", justifyContent: "center", alignItems: "center" }}>
              <Decant alto={340} llenado={1} {...vialBlanco} />
            </div>
          ) : (
            <Img
              src={staticFile("decants/coco-mademoiselle.jpg")}
              style={{ width: 360, height: 360, borderRadius: 32, boxShadow: "0 24px 50px rgba(0, 0, 0, 0.25)" }}
            />
          )}
          <div
            style={{
              position: "absolute",
              right: -70,
              top: -30,
              width: 150,
              height: 150,
              borderRadius: "50%",
              background: BLANCO,
              color: rosa.oscuro,
              fontFamily: fuente,
              fontWeight: 800,
              fontSize: 30,
              lineHeight: 1.05,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              textAlign: "center",
              boxShadow: "0 12px 30px rgba(0, 0, 0, 0.25)",
            }}
          >
            100%
            <br />
            ORIGINAL
          </div>
        </div>
      </Aparecer>
    </AbsoluteFill>
  </Slide>
);

const Cierre: React.FC = () => (
  <Slide etiqueta="Larese Store" titulo="Empezá por un decant" subtitulo="Perfumes originales en 5 y 10 ml" cta="Escribinos por WhatsApp">
    <Tarjetas top={540} alto={380} separacion={250} />
  </Slide>
);

export const slidesDecants: React.FC[] = [Portada, Razon1, Razon2, Razon3, Razon4, Razon5, Cierre];

export const slidesDecantsSinMarcas: React.FC[] = slidesDecants.map((S) => {
  const SinMarca: React.FC = () => (
    <SinMarcas.Provider value>
      <S />
    </SinMarcas.Provider>
  );
  return SinMarca;
});

const razones = [
  "Lo probás en tu piel antes de comprar el frasco",
  "Pagás mucho menos por un perfume de lujo",
  "Armás tu colección con varios aromas",
  "Lo llevás en la cartera a todos lados",
  "Es el mismo perfume, 100% original",
];

const Check: React.FC = () => (
  <svg width={46} height={46} viewBox="0 0 46 46" style={{ flexShrink: 0 }}>
    <circle cx={23} cy={23} r={23} fill={BLANCO} />
    <path d="M13 24 L20 31 L33 16" fill="none" stroke={rosa.oscuro} strokeWidth={4.5} strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export const HistoriaDecantsSinMarcas: React.FC = () => (
  <SinMarcas.Provider value>
    <HistoriaDecants />
  </SinMarcas.Provider>
);

// Historia con las cinco razones en lista
export const HistoriaDecants: React.FC = () => (
  <Base
    m={HISTORIA}
    centroMarca={980}
    etiqueta="Guía Larese"
    titulo="¿Por qué elegir decants?"
    tamano={96}
    cta="¡Pedí el tuyo!"
    ctaAbajo={330}
  >
    <AbsoluteFill style={{ top: 620, alignItems: "center" }}>
      <div style={{ display: "flex", flexDirection: "column", gap: 34 }}>
        {razones.map((r, i) => (
          <Aparecer key={r} desde={12 + i * 4}>
            <div style={{ display: "flex", alignItems: "center", gap: 24, fontFamily: fuente, fontSize: 38, fontWeight: 500, color: BLANCO, maxWidth: 880 }}>
              <Check />
              <span>{r}</span>
            </div>
          </Aparecer>
        ))}
      </div>
    </AbsoluteFill>
    <Tarjetas top={1150} alto={250} separacion={190} />
  </Base>
);
