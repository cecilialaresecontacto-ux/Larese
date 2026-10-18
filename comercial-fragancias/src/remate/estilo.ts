import type { CSSProperties } from "react";

export const dorado = "#d9b25f";

export const textoDorado: CSSProperties = {
  background: "linear-gradient(180deg, #fff1c9 0%, #e6c372 45%, #a8772e 100%)",
  WebkitBackgroundClip: "text",
  backgroundClip: "text",
  color: "transparent",
};

export const fondoOscuro = (acento: string, y = 45) =>
  `radial-gradient(circle at 50% ${y}%, ${acento}40 0%, #141210 45%, #050505 100%)`;
