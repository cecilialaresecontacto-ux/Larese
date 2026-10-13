import { Composition } from "remotion";
import { Comercial, ComercialProps, DURACION_TOTAL } from "./Comercial";

const props: ComercialProps = {
  tienda: "",
  llamado: "Pedí el tuyo por DM",
};

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Comercial"
      component={Comercial}
      durationInFrames={DURACION_TOTAL}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={props}
    />
  );
};
