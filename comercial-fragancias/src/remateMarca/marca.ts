// Colores y datos de marca, calculados con las reglas del skill de anuncios de Larese:
// el fondo sale del color del frasco y, si el frasco es negro o plateado, se usa el
// rosa empolvado de la categoría perfume.
export type Paleta = {
  color: string;
  oscuro: string;
  centro: string;
  borde: string;
};

export const rosaPerfume: Paleta = { color: "#ce8690", oscuro: "#955a62", centro: "#df9fa8", borde: "#bc7a83" };

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
  imagen: string;
  // Proporción ancho / alto del recorte sin fondo
  proporcion: number;
  paleta: Paleta;
};

export const productos: Producto[] = [
  {
    id: "asad",
    marca: "Lattafa",
    nombre: "Asad",
    publico: "Para él",
    imagen: "flyer/asad.png",
    proporcion: 482 / 1100,
    paleta: { color: "#ac9d74", oscuro: "#736848", centro: "#bdb08b", borde: "#9a8c67" },
  },
  {
    id: "yara",
    marca: "Lattafa",
    nombre: "Yara",
    publico: "Para ella",
    imagen: "flyer/yara.png",
    proporcion: 450 / 1100,
    paleta: { color: "#bc8792", oscuro: "#835861", centro: "#cda0a9", borde: "#aa7a84" },
  },
  {
    id: "fakhar-black",
    marca: "Lattafa",
    nombre: "Fakhar Black",
    publico: "Para él",
    imagen: "flyer/fakhar-black.png",
    proporcion: 595 / 1100,
    paleta: rosaPerfume,
  },
  {
    id: "fakhar-gold",
    marca: "Lattafa",
    nombre: "Fakhar Gold",
    publico: "Para ella",
    imagen: "flyer/fakhar-gold.png",
    proporcion: 564 / 1100,
    paleta: { color: "#ac967b", oscuro: "#73624d", centro: "#bdaa93", borde: "#9a866e" },
  },
  {
    id: "attar-al-wesal",
    marca: "Al Wataniah",
    nombre: "Attar Al Wesal",
    publico: "Para él",
    imagen: "flyer/attar-al-wesal.png",
    proporcion: 486 / 1100,
    paleta: rosaPerfume,
  },
];
