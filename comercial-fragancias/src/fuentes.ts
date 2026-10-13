import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Tipografías de Google Fonts (licencia OFL), guardadas en public/fuentes
// para que el render no dependa de internet
export const serif = "Playfair Display";
export const sans = "Montserrat";

loadFont({ family: serif, url: staticFile("fuentes/PlayfairDisplay.woff2"), weight: "400 900" });
loadFont({
  family: serif,
  url: staticFile("fuentes/PlayfairDisplay-Italic.woff2"),
  weight: "400 900",
  style: "italic",
});
loadFont({ family: sans, url: staticFile("fuentes/Montserrat.woff2"), weight: "100 900" });
