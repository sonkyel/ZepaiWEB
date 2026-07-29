/**
 * Fondo de marca del hero.
 *
 * Sustituye a la escena de Spline, que era alquilada (alojada en su
 * servidor, imposible de recolorear y 2 MB por visita). Esto es nuestro:
 * paleta exacta de Zepai y, sobre todo, un fondo DETERMINISTA. El problema
 * de legibilidad anterior venia de no saber que habia detras del texto
 * porque la escena se movia; aqui la zona tras la copia nunca supera
 * #241A4A, que es el fondo contra el que se valida el contraste en
 * check-contrast.py.
 *
 * El motivo no es espacio generico: son nodos conectados por aristas, una
 * red de automatizacion. Todo SVG y CSS, sin JS ni canvas.
 */

const NODOS = [
  { x: 118, y: 128, r: 5.5 },
  { x: 232, y: 74, r: 4 },
  { x: 300, y: 186, r: 6.5 },
  { x: 186, y: 246, r: 4.5 },
  { x: 402, y: 108, r: 5 },
  { x: 470, y: 232, r: 4 },
  { x: 356, y: 320, r: 5.5 },
  { x: 552, y: 148, r: 4.5 },
  { x: 620, y: 268, r: 6 },
  { x: 500, y: 372, r: 4 },
  { x: 700, y: 96, r: 4.5 },
  { x: 742, y: 214, r: 5 },
];

const ARISTAS: [number, number][] = [
  [0, 1], [1, 2], [0, 3], [2, 3], [1, 4], [2, 5], [3, 6],
  [4, 7], [5, 8], [6, 9], [7, 10], [8, 11], [5, 6], [7, 8],
];

export function BrandBackdrop() {
  return (
    <div className="brand-bg" aria-hidden="true">
      {/* 1. Base y nebulosa en la paleta de marca */}
      <div className="brand-nebula" />

      {/* 2. Campo de estrellas, tres capas con parpadeo desfasado */}
      <div className="brand-stars" />

      {/* 3. Red de nodos: el motivo que dice "automatizacion", no "espacio" */}
      <svg
        className="brand-net"
        viewBox="0 0 800 440"
        preserveAspectRatio="xMidYMid slice"
        role="presentation"
      >
        <defs>
          <linearGradient id="netLine" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#8B5CF6" stopOpacity="0.55" />
            <stop offset="100%" stopColor="#4F46E5" stopOpacity="0.2" />
          </linearGradient>
          <radialGradient id="netDot">
            <stop offset="0%" stopColor="#DDD1FF" />
            <stop offset="100%" stopColor="#8B5CF6" />
          </radialGradient>
        </defs>

        <g stroke="url(#netLine)" strokeWidth="1.2" fill="none">
          {ARISTAS.map(([a, b], i) => (
            <line
              key={i}
              x1={NODOS[a].x}
              y1={NODOS[a].y}
              x2={NODOS[b].x}
              y2={NODOS[b].y}
              className="brand-edge"
              style={{ animationDelay: `${(i % 7) * 0.9}s` }}
            />
          ))}
        </g>

        <g>
          {NODOS.map((n, i) => (
            <circle
              key={i}
              cx={n.x}
              cy={n.y}
              r={n.r}
              fill="url(#netDot)"
              className="brand-node"
              style={{ animationDelay: `${(i % 5) * 1.1}s` }}
            />
          ))}
        </g>
      </svg>

      {/* 4. Velo: garantiza el fondo detras del texto pase lo que pase */}
      <div className="brand-scrim" />
    </div>
  );
}
