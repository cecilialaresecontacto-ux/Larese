export type Fragancia = {
  id: string;
  nombre: string;
  notas: string;
  imagen: string;
  // Proporción ancho / alto de la imagen recortada
  proporcion: number;
  fondoCentro: string;
  fondoBorde: string;
  brillo: string;
  texto: string;
};

export const fragancias: Fragancia[] = [
  {
    id: "bare-vanilla",
    nombre: "Bare Vanilla",
    notas: "Vainilla batida y cachemira",
    imagen: "bare-vanilla.png",
    proporcion: 344 / 1136,
    fondoCentro: "#fbeee0",
    fondoBorde: "#c8956c",
    brillo: "#ffd9a8",
    texto: "#4a2c1c",
  },
  {
    id: "coconut-passion",
    nombre: "Coconut Passion",
    notas: "Coco cremoso y vainilla al sol",
    imagen: "coconut-passion.png",
    proporcion: 171 / 572,
    fondoCentro: "#fbf5e2",
    fondoBorde: "#c3a35f",
    brillo: "#fff0b8",
    texto: "#4a3a17",
  },
  {
    id: "pure-seduction",
    nombre: "Pure Seduction",
    notas: "Ciruela roja y fresia",
    imagen: "pure-seduction.png",
    proporcion: 168 / 561,
    fondoCentro: "#fbe4ee",
    fondoBorde: "#b0567f",
    brillo: "#ffc8de",
    texto: "#561a38",
  },
];
