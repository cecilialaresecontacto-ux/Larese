export type Decant = {
  id: string;
  marca: string;
  nombre: string;
  publico: string;
  imagen: string;
  // Proporción ancho / alto de la foto recortada
  proporcion: number;
  acento: string;
};

export const precios = [
  { ml: 5, precio: "Gs. 15.000" },
  { ml: 10, precio: "Gs. 20.000" },
];

export const decants: Decant[] = [
  {
    id: "asad",
    marca: "Lattafa",
    nombre: "Asad",
    publico: "Para él",
    imagen: "remate/asad.jpg",
    proporcion: 908 / 854,
    acento: "#d9b25f",
  },
  {
    id: "yara",
    marca: "Lattafa",
    nombre: "Yara",
    publico: "Para ella",
    imagen: "remate/yara.jpg",
    proporcion: 991 / 954,
    acento: "#f2a7c3",
  },
  {
    id: "fakhar-black",
    marca: "Lattafa",
    nombre: "Fakhar Black",
    publico: "Para él",
    imagen: "remate/fakhar-black.jpg",
    proporcion: 481 / 440,
    acento: "#c9ccd3",
  },
  {
    id: "fakhar-gold",
    marca: "Lattafa",
    nombre: "Fakhar Gold",
    publico: "Para ella",
    imagen: "remate/fakhar-gold.jpg",
    proporcion: 476 / 462,
    acento: "#e3b48a",
  },
  {
    id: "attar-al-wesal",
    marca: "Al Wataniah",
    nombre: "Attar Al Wesal",
    publico: "Para él",
    imagen: "remate/attar-al-wesal.jpg",
    proporcion: 478 / 432,
    acento: "#c9ccd3",
  },
];
