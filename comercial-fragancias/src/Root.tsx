import { Composition } from "remotion";
import { Comercial, ComercialProps, DURACION_TOTAL } from "./Comercial";
import { AnuncioLarese, AnuncioProps, DURACION_ANUNCIO } from "./anuncio/AnuncioLarese";
import { flyers } from "./flyer/datos";
import { Flyer } from "./flyer/Flyer";
import { DURACION_FLYER, DURACION_FLYERS, FlyersDecants } from "./flyer/FlyersDecants";
import { DURACION_REMATE, RemateDecants, RemateProps } from "./remate/RemateDecants";

const props: ComercialProps = {
  usuario: "@larese",
  llamado: "Pedí el tuyo por DM",
};

const propsRemate: RemateProps = {
  usuario: "@larese",
  llamado: "Reservá el tuyo por DM",
};

const propsAnuncio: AnuncioProps = {
  usuario: "@larese",
  llamado: "Pedí el tuyo por DM",
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Comercial"
        component={Comercial}
        durationInFrames={DURACION_TOTAL}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={props}
      />
      <Composition
        id="RemateDecants"
        component={RemateDecants}
        durationInFrames={DURACION_REMATE}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={propsRemate}
      />
      <Composition
        id="AnuncioLarese"
        component={AnuncioLarese}
        durationInFrames={DURACION_ANUNCIO}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={propsAnuncio}
      />
      <Composition
        id="FlyersDecants"
        component={FlyersDecants}
        durationInFrames={DURACION_FLYERS}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{ usuario: "@larese" }}
      />
      {flyers.map((f) => (
        <Composition
          key={f.id}
          id={`Flyer-${f.id}`}
          component={Flyer}
          durationInFrames={DURACION_FLYER}
          fps={30}
          width={1080}
          height={1920}
          defaultProps={{ fragancia: f, usuario: "@larese" }}
        />
      ))}
    </>
  );
};
