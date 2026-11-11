import { Composition } from "remotion";
import { Comercial, ComercialProps, DURACION_TOTAL } from "./Comercial";

const props: ComercialProps = {
  precio: "Gs. 1.350.000",
  llamado: "Pedí tu combo por WhatsApp",
};

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Combo5"
      component={Comercial}
      durationInFrames={DURACION_TOTAL}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={props}
    />
  );
};
