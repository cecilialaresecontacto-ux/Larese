// Íconos blancos dentro de un círculo, como en la fila de contacto de la referencia
const Circulo: React.FC<{ children: React.ReactNode; color: string }> = ({ children, color }) => (
  <svg width={64} height={64} viewBox="0 0 64 64">
    <circle cx={32} cy={32} r={32} fill="rgba(255, 255, 255, 0.92)" />
    <g fill="none" stroke={color} strokeWidth={3.5} strokeLinecap="round" strokeLinejoin="round">
      {children}
    </g>
  </svg>
);

export const IconoInstagram: React.FC<{ color: string }> = ({ color }) => (
  <Circulo color={color}>
    <rect x={18} y={18} width={28} height={28} rx={8} />
    <circle cx={32} cy={32} r={6.5} />
    <circle cx={40.5} cy={23.5} r={0.8} fill={color} />
  </Circulo>
);

export const IconoReloj: React.FC<{ color: string }> = ({ color }) => (
  <Circulo color={color}>
    <circle cx={32} cy={32} r={14} />
    <path d="M32 24 V32 L38 36" />
  </Circulo>
);
