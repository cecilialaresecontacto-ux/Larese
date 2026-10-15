// Tomas del reel, en orden. Los clips están en public/clips (1080×1920, 30 fps).
// desde: segundo del clip donde empieza la toma
// velocidad: 1 = normal, 1.5 = 50 % más rápido
// duracion: frames que dura la toma en el reel (30 = 1 s)

export type Toma = {
  clip: string;
  desde: number;
  velocidad: number;
  duracion: number;
  marca?: string;
  nombre?: string;
  frase?: boolean;
};

export const tomas: Toma[] = [
  { clip: "clips/5261.mp4", desde: 0, velocidad: 1, duracion: 60 },
  { clip: "clips/5283.mp4", desde: 1.5, velocidad: 1.1, duracion: 62, marca: "PRADA", nombre: "Paradoxe Intense" },
  { clip: "clips/5281.mp4", desde: 0, velocidad: 1.4, duracion: 85, marca: "DIOR", nombre: "Dior Addict" },
  { clip: "clips/5263.mp4", desde: 0, velocidad: 1.5, duracion: 90, marca: "GIVENCHY", nombre: "L'Interdit" },
  { clip: "clips/5260.mp4", desde: 1.5, velocidad: 1.6, duracion: 60, frase: true },
  // Carga de la jeringa, justo antes del logo
  { clip: "clips/5283.mp4", desde: 0.45, velocidad: 1, duracion: 30 },
];

// Placa final con el logo
export const DURACION_CIERRE = 75;
