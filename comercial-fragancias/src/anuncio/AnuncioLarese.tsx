import { Series } from "remotion";
import { fuente } from "../fuentes";
import { dorado } from "./estilo";
import { frascos } from "./frascos";
import { TomaFinal } from "./tomas/TomaFinal";
import { TomaLineup } from "./tomas/TomaLineup";
import { TomaNumero } from "./tomas/TomaNumero";
import { TomaPalabra } from "./tomas/TomaPalabra";

export type AnuncioProps = {
  usuario: string;
  llamado: string;
};

const marcaDebajo = (texto: string) => (
  <div style={{ fontFamily: fuente, fontSize: 34, fontWeight: 500, letterSpacing: 14, color: dorado }}>{texto}</div>
);

// Cortes secos y rápidos, una idea por toma
const tomas = (props: AnuncioProps) => [
  { duracion: 40, contenido: <TomaPalabra partes={["Remate."]} tamano={240} explotar /> },
  { duracion: 36, contenido: <TomaPalabra partes={["As", frascos.asad, "d."]} debajo={marcaDebajo("LATTAFA")} /> },
  { duracion: 36, contenido: <TomaPalabra partes={["Y", frascos.yara, "ra."]} debajo={marcaDebajo("LATTAFA")} /> },
  {
    duracion: 40,
    contenido: (
      <TomaPalabra
        partes={["F", frascos.fakharBlack, "kh", frascos.fakharGold, "r."]}
        tamano={180}
        debajo={marcaDebajo("BLACK · GOLD")}
      />
    ),
  },
  { duracion: 36, contenido: <TomaPalabra partes={["Att", frascos.attar, "r."]} debajo={marcaDebajo("AL WESAL")} /> },
  { duracion: 42, contenido: <TomaNumero valor="5 ml" detalle="Gs. 15.000" /> },
  { duracion: 42, contenido: <TomaNumero valor="10 ml" detalle="Gs. 20.000" /> },
  { duracion: 54, contenido: <TomaLineup /> },
  { duracion: 36, contenido: <TomaPalabra partes={["Y más."]} tamano={230} /> },
  { duracion: 40, contenido: <TomaPalabra partes={["Hasta agotar"]} tamano={130} debajo={<TomaStock />} /> },
  { duracion: 80, contenido: <TomaFinal {...props} /> },
];

const TomaStock: React.FC = () => (
  <div style={{ fontFamily: fuente, fontSize: 200, fontWeight: 700, letterSpacing: -8, lineHeight: 1, marginTop: -40, color: dorado }}>
    stock.
  </div>
);

export const DURACION_ANUNCIO = tomas({ usuario: "", llamado: "" }).reduce((total, t) => total + t.duracion, 0);

export const AnuncioLarese: React.FC<AnuncioProps> = (props) => {
  return (
    <Series>
      {tomas(props).map((t, i) => (
        <Series.Sequence key={i} durationInFrames={t.duracion}>
          {t.contenido}
        </Series.Sequence>
      ))}
    </Series>
  );
};
