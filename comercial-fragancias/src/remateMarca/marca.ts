// Colores y datos de marca, calculados con las reglas del skill de anuncios de Larese:
// el fondo sale del color del frasco y, si el frasco es negro, va gris.
export type Paleta = {
  color: string;
  oscuro: string;
  centro: string;
  borde: string;
};

export const gris: Paleta = { color: "#8c8e94", oscuro: "#52545b", centro: "#a5a5a5", borde: "#7b7c82" };

export const WHATSAPP = "0972 736 002";
export const ENVIOS = "Envíos a todo Paraguay";

export const precios = [
  { ml: 5, precio: "Gs. 15.000" },
  { ml: 10, precio: "Gs. 20.000" },
];

export type Producto = {
  id: string;
  marca: string;
  nombre: string;
  publico: string;
  // Foto original del producto, con su fondo blanco
  imagen: string;
  // Proporción ancho / alto de la foto
  proporcion: number;
  paleta: Paleta;
};

export const productos: Producto[] = [
  {
    id: "asad",
    marca: "Lattafa",
    nombre: "Asad",
    publico: "Para él",
    imagen: "remate/asad.jpg",
    proporcion: 908 / 854,
    paleta: gris,
  },
  {
    id: "yara",
    marca: "Lattafa",
    nombre: "Yara",
    publico: "Para ella",
    imagen: "remate/yara.jpg",
    proporcion: 991 / 954,
    paleta: { color: "#bc8792", oscuro: "#835861", centro: "#cda0a9", borde: "#aa7a84" },
  },
  {
    id: "fakhar-black",
    marca: "Lattafa",
    nombre: "Fakhar Black",
    publico: "Para él",
    imagen: "remate/fakhar-black.jpg",
    proporcion: 481 / 440,
    paleta: gris,
  },
  {
    id: "fakhar-gold",
    marca: "Lattafa",
    nombre: "Fakhar Gold",
    publico: "Para ella",
    imagen: "remate/fakhar-gold.jpg",
    proporcion: 476 / 462,
    paleta: { color: "#ac967b", oscuro: "#73624d", centro: "#bdaa93", borde: "#9a866e" },
  },
  {
    id: "attar-al-wesal",
    marca: "Al Wataniah",
    nombre: "Attar Al Wesal",
    publico: "Para él",
    imagen: "remate/attar-al-wesal.jpg",
    proporcion: 478 / 432,
    paleta: gris,
  },
];
