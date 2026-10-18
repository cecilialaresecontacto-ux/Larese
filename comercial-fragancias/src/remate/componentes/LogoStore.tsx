import { Img, staticFile } from "remotion";
import { fuente } from "../../fuentes";
import { marca } from "../../marca";

// Logo blanco de Larese con "STORE" debajo, para fondos oscuros
export const LogoStore: React.FC<{ alto: number }> = ({ alto }) => {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <Img
        src={staticFile("marca/logo-blanco.png")}
        style={{ height: alto, width: alto * marca.logoProporcion }}
      />
      <div
        style={{
          fontFamily: fuente,
          fontWeight: 500,
          fontSize: alto * 0.3,
          letterSpacing: alto * 0.3,
          // Compensa el espacio que deja la última letra
          marginRight: -alto * 0.3,
          marginTop: alto * 0.18,
          color: marca.blanco,
        }}
      >
        STORE
      </div>
    </div>
  );
};
