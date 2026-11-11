export type Fragancia = {
  id: string;
  etiqueta: string;
  nombre: string;
  marca: string;
  notas: string;
  imagen: string;
  // Proporción ancho / alto de la imagen recortada
  proporcion: number;
  // Alto en pantalla
  alto: number;
};

export const fragancias: Fragancia[] = [
  { id: "azzaro", etiqueta: "DISEÑADOR", nombre: "The Most Wanted Parfum", marca: "Azzaro",
    notas: "Especiado y dulce, para la noche", imagen: "azzaro.png", proporcion: 454 / 435, alto: 780 },
  { id: "bharara", etiqueta: "ÁRABE", nombre: "Bharara King", marca: "Bharara",
    notas: "Cítrico y elegante, día y noche", imagen: "bharara-king.png", proporcion: 192 / 462, alto: 820 },
  { id: "brun", etiqueta: "ÁRABE", nombre: "Liquid Brun", marca: "French Avenue",
    notas: "Cálido y dulce, para la noche", imagen: "liquid-brun.png", proporcion: 410 / 1000, alto: 880 },
  { id: "cdn", etiqueta: "ÁRABE", nombre: "Club de Nuit Intense Man", marca: "Armaf",
    notas: "Amaderado y ahumado, un clásico", imagen: "club-de-nuit.png", proporcion: 391 / 600, alto: 820 },
  { id: "odyssey", etiqueta: "ÁRABE", nombre: "Odyssey Aqua", marca: "Armaf",
    notas: "Fresco y acuático, para el calor", imagen: "odyssey-aqua.png", proporcion: 865 / 739, alto: 760 },
];
