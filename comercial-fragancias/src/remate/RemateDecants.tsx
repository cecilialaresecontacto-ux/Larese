import { linearTiming, TransitionSeries } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { decants } from "./datos";
import { EscenaDecant } from "./escenas/EscenaDecant";
import { FinalRemate } from "./escenas/FinalRemate";
import { IntroRemate } from "./escenas/IntroRemate";
import { Precios } from "./escenas/Precios";

export type RemateProps = {
  usuario: string;
  llamado: string;
};

export const DURACION_INTRO = 80;
export const DURACION_PRECIOS = 95;
export const DURACION_DECANT = 75;
export const DURACION_FINAL = 120;
export const DURACION_TRANSICION = 12;

export const DURACION_REMATE =
  DURACION_INTRO +
  DURACION_PRECIOS +
  DURACION_DECANT * decants.length +
  DURACION_FINAL -
  DURACION_TRANSICION * (decants.length + 2);

const transicion = linearTiming({ durationInFrames: DURACION_TRANSICION });

export const RemateDecants: React.FC<RemateProps> = ({ usuario, llamado }) => {
  return (
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={DURACION_INTRO}>
        <IntroRemate />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition presentation={fade()} timing={transicion} />
      <TransitionSeries.Sequence durationInFrames={DURACION_PRECIOS}>
        <Precios />
      </TransitionSeries.Sequence>
      {decants.map((d) => [
        <TransitionSeries.Transition
          key={`t-${d.id}`}
          presentation={slide({ direction: "from-right" })}
          timing={transicion}
        />,
        <TransitionSeries.Sequence key={d.id} durationInFrames={DURACION_DECANT}>
          <EscenaDecant decant={d} />
        </TransitionSeries.Sequence>,
      ])}
      <TransitionSeries.Transition presentation={fade()} timing={transicion} />
      <TransitionSeries.Sequence durationInFrames={DURACION_FINAL}>
        <FinalRemate usuario={usuario} llamado={llamado} />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
