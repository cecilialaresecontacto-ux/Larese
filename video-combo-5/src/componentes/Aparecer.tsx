import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

type Props = {
  desde: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
};

// Texto que sube y aparece suavemente
export const Aparecer: React.FC<Props> = ({ desde, children, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - desde, fps, config: { damping: 200 }, durationInFrames: 25 });

  return (
    <div
      style={{
        ...style,
        opacity: p,
        transform: `translateY(${interpolate(p, [0, 1], [40, 0])}px)`,
        filter: `blur(${interpolate(p, [0, 1], [8, 0])}px)`,
      }}
    >
      {children}
    </div>
  );
};
