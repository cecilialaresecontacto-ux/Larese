import { linearTiming, TransitionSeries } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { productos } from "./marca";
import { Apertura, Cierre, Fragancia, Tamanos } from "./escenas/Escenas";

const DURACION_APERTURA = 85;
const DURACION_TAMANOS = 95;
const DURACION_FRAGANCIA = 80;
const DURACION_CIERRE = 120;
const DURACION_TRANSICION = 12;

export const DURACION_REMATE_LARESE =
  DURACION_APERTURA +
  DURACION_TAMANOS +
  DURACION_FRAGANCIA * productos.length +
  DURACION_CIERRE -
  DURACION_TRANSICION * (productos.length + 2);

const transicion = linearTiming({ durationInFrames: DURACION_TRANSICION });

// El primer anuncio del remate, rehecho con el estilo del skill de anuncios de Larese
export const RemateLarese: React.FC = () => {
  return (
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={DURACION_APERTURA}>
        <Apertura />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition presentation={fade()} timing={transicion} />
      <TransitionSeries.Sequence durationInFrames={DURACION_TAMANOS}>
        <Tamanos />
      </TransitionSeries.Sequence>
      {productos.map((p) => [
        <TransitionSeries.Transition
          key={`t-${p.id}`}
          presentation={slide({ direction: "from-right" })}
          timing={transicion}
        />,
        <TransitionSeries.Sequence key={p.id} durationInFrames={DURACION_FRAGANCIA}>
          <Fragancia producto={p} />
        </TransitionSeries.Sequence>,
      ])}
      <TransitionSeries.Transition presentation={fade()} timing={transicion} />
      <TransitionSeries.Sequence durationInFrames={DURACION_CIERRE}>
        <Cierre />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
