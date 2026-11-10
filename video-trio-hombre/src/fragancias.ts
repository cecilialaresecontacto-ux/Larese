export type Fragancia = {
  id: string;
  nombre: string;
  marca: string;
  notas: string;
  imagen: string;
  // Proporción ancho / alto de la imagen recortada
  proporcion: number;
  // Alto en pantalla (las fotos con caja son más anchas)
  alto: number;
};

export const fragancias: Fragancia[] = [
  {
    id: "profondo",
    nombre: "Acqua di Giò Profondo",
    marca: "Giorgio Armani",
    notas: "Fresco y marino, para el día",
    imagen: "profondo.png",
    proporcion: 280 / 536,
    alto: 900,
  },
  {
    id: "born-in-roma",
    nombre: "Born in Roma Intense",
    marca: "Valentino",
    notas: "Dulce y avainillado, para la noche",
    imagen: "born-in-roma.png",
    proporcion: 600 / 508,
    alto: 760,
  },
  {
    id: "le-beau",
    nombre: "Le Beau Le Parfum",
    marca: "Jean Paul Gaultier",
    notas: "Amaderado y seductor, para la noche",
    imagen: "le-beau.png",
    proporcion: 429 / 560,
    alto: 860,
  },
];
