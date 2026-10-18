export type FlyerFragancia = {
  id: string;
  antetitulo: string;
  titulo: string;
  bajada: string;
  imagen: string;
  // Proporción ancho / alto del recorte sin fondo
  proporcion: number;
  color: string;
};

export const precioTexto = "5 ml Gs. 15.000  |  10 ml Gs. 20.000";

export const flyers: FlyerFragancia[] = [
  {
    id: "asad",
    antetitulo: "DECANT · LATTAFA",
    titulo: "ASAD",
    bajada: "INTENSO & ELEGANTE, PARA ÉL",
    imagen: "flyer/asad.png",
    proporcion: 482 / 1100,
    color: "#a8844f",
  },
  {
    id: "yara",
    antetitulo: "DECANT · LATTAFA",
    titulo: "YARA",
    bajada: "DULCE & FEMENINO, PARA ELLA",
    imagen: "flyer/yara.png",
    proporcion: 450 / 1100,
    color: "#d48a9c",
  },
  {
    id: "fakhar-black",
    antetitulo: "DECANT · LATTAFA FAKHAR",
    titulo: "BLACK",
    bajada: "FRESCO & SOFISTICADO, PARA ÉL",
    imagen: "flyer/fakhar-black.png",
    proporcion: 595 / 1100,
    color: "#7d8592",
  },
  {
    id: "fakhar-gold",
    antetitulo: "DECANT · LATTAFA FAKHAR",
    titulo: "GOLD",
    bajada: "CÁLIDO & ELEGANTE, PARA ELLA",
    imagen: "flyer/fakhar-gold.png",
    proporcion: 564 / 1100,
    color: "#c39472",
  },
  {
    id: "attar-al-wesal",
    antetitulo: "DECANT · ATTAR",
    titulo: "AL WESAL",
    bajada: "ÁRABE & SEDUCTOR, PARA ÉL",
    imagen: "flyer/attar-al-wesal.png",
    proporcion: 486 / 1100,
    color: "#6d7783",
  },
];
