import { linearTiming, TransitionSeries } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { Final } from "./escenas/Final";
import { EscenaFragancia } from "./escenas/EscenaFragancia";
import { Intro } from "./escenas/Intro";
import { fragancias } from "./fragancias";

export type ComercialProps = {
  tienda: string;
  llamado: string;
};

export const DURACION_INTRO = 75;
export const DURACION_FRAGANCIA = 105;
export const DURACION_FINAL = 120;
export const DURACION_TRANSICION = 15;

export const DURACION_TOTAL =
  DURACION_INTRO +
  DURACION_FRAGANCIA * fragancias.length +
  DURACION_FINAL -
  DURACION_TRANSICION * (fragancias.length + 1);

const transicion = linearTiming({ durationInFrames: DURACION_TRANSICION });

export const Comercial: React.FC<ComercialProps> = ({ tienda, llamado }) => {
  return (
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={DURACION_INTRO}>
        <Intro />
      </TransitionSeries.Sequence>
      {fragancias.map((f, i) => [
        <TransitionSeries.Transition
          key={`t-${f.id}`}
          presentation={i === 0 ? fade() : slide({ direction: "from-right" })}
          timing={transicion}
        />,
        <TransitionSeries.Sequence key={f.id} durationInFrames={DURACION_FRAGANCIA}>
          <EscenaFragancia fragancia={f} numero={i + 1} />
        </TransitionSeries.Sequence>,
      ])}
      <TransitionSeries.Transition presentation={fade()} timing={transicion} />
      <TransitionSeries.Sequence durationInFrames={DURACION_FINAL}>
        <Final tienda={tienda} llamado={llamado} />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
