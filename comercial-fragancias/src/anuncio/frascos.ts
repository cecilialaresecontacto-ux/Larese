export type Frasco = {
  imagen: string;
  // Proporción ancho / alto del recorte sin fondo
  proporcion: number;
};

export const frascos = {
  asad: { imagen: "anuncio/asad.png", proporcion: 313 / 714 },
  yara: { imagen: "anuncio/yara.png", proporcion: 317 / 775 },
  fakharBlack: { imagen: "anuncio/fakhar-black.png", proporcion: 197 / 364 },
  fakharGold: { imagen: "anuncio/fakhar-gold.png", proporcion: 157 / 306 },
  attar: { imagen: "anuncio/attar-al-wesal.png", proporcion: 140 / 317 },
} satisfies Record<string, Frasco>;
