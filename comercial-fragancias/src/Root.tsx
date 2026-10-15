import { Composition } from "remotion";
import { Comercial, ComercialProps, DURACION_TOTAL } from "./Comercial";
import { Decants, DecantsProps, DURACION_DECANTS } from "./decants/Decants";

const props: ComercialProps = {
  usuario: "@larese",
  llamado: "Pedí el tuyo por DM",
};

const propsDecants: DecantsProps = {
  titulo: "ARMANDO",
  subtitulo: "decants de 3 ml",
  frase: "Tu perfume favorito,\nen tamaño cartera",
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
        id="Decants"
        component={Decants}
        durationInFrames={DURACION_DECANTS}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={propsDecants}
      />
    </>
  );
};
