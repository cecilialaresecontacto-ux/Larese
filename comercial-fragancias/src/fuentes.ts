import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Poppins (Google Fonts, licencia OFL), guardada en public/fuentes
// para que el render no dependa de internet
export const fuente = "Poppins";

for (const peso of ["300", "400", "500", "600", "700"]) {
  loadFont({ family: fuente, url: staticFile(`fuentes/Poppins-${peso}.woff2`), weight: peso });
}

// Montserrat (licencia OFL) para los flyers estilo pastelería
export const fuenteFlyer = "Montserrat";

for (const peso of ["500", "600", "700", "800"]) {
  loadFont({ family: fuenteFlyer, url: staticFile(`fuentes/Montserrat-${peso}.woff2`), weight: peso });
}
