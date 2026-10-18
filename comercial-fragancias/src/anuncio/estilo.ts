import type { CSSProperties } from "react";

export const negro = "#000000";
export const dorado = "#d9b25f";

// Blanco metálico, como los titulares de los anuncios de Apple
export const textoMetal: CSSProperties = {
  background: "linear-gradient(180deg, #ffffff 0%, #f2f2f2 45%, #a9a9a9 100%)",
  WebkitBackgroundClip: "text",
  backgroundClip: "text",
  color: "transparent",
};

export const textoDorado: CSSProperties = {
  background: "linear-gradient(180deg, #fff1c9 0%, #e6c372 45%, #a8772e 100%)",
  WebkitBackgroundClip: "text",
  backgroundClip: "text",
  color: "transparent",
};

export const resplandor = (opacidad: number) =>
  `radial-gradient(ellipse 70% 40% at 50% 50%, rgba(217, 178, 95, ${opacidad}) 0%, transparent 70%)`;
