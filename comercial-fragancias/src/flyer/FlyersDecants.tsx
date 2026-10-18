import { linearTiming, TransitionSeries } from "@remotion/transitions";
import { slide } from "@remotion/transitions/slide";
import { flyers } from "./datos";
import { Flyer } from "./Flyer";

export type FlyerProps = {
  usuario: string;
};

export const DURACION_FLYER = 105;
const DURACION_TRANSICION = 15;

export const DURACION_FLYERS = DURACION_FLYER * flyers.length - DURACION_TRANSICION * (flyers.length - 1);

const transicion = linearTiming({ durationInFrames: DURACION_TRANSICION });

export const FlyersDecants: React.FC<FlyerProps> = ({ usuario }) => {
  return (
    <TransitionSeries>
      {flyers.map((f, i) => [
        i > 0 ? (
          <TransitionSeries.Transition
            key={`t-${f.id}`}
            presentation={slide({ direction: "from-right" })}
            timing={transicion}
          />
        ) : null,
        <TransitionSeries.Sequence key={f.id} durationInFrames={DURACION_FLYER}>
          <Flyer fragancia={f} usuario={usuario} />
        </TransitionSeries.Sequence>,
      ])}
    </TransitionSeries>
  );
};
