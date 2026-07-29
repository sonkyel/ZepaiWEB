"use client";

/**
 * Vortex — fondo de partículas sobre canvas.
 *
 * Adaptado del componente original. Ocho correcciones respecto a como venia,
 * cada una por un motivo concreto:
 *
 *  1. "use client": usa hooks, en App Router no arranca sin ella.
 *  2. Sin framer-motion: solo se usaba para un fundido de opacidad 0 -> 1.
 *     Eran 4,8 MB de paquete para tres lineas de CSS.
 *  3. El bucle de animacion guarda su id y SE CANCELA al desmontar. El
 *     original se llamaba a si mismo para siempre: al navegar a otra ruta
 *     seguia consumiendo CPU en segundo plano.
 *  4. El listener de resize se retira; el original usaba una funcion anonima
 *     imposible de quitar.
 *  5. tick, particleProps y el ruido viven en refs. En el original se
 *     redeclaraban en cada render.
 *  6. Se dimensiona por el CONTENEDOR (ResizeObserver) y se escala por
 *     devicePixelRatio; el original usaba window.innerWidth y salia borroso
 *     en pantallas retina.
 *  7. Se pausa cuando el hero sale de pantalla o se cambia de pestana.
 *  8. Respeta prefers-reduced-motion: no anima.
 *
 * Ademas rangeHue y blurPasses son props (estaban fijos), porque el coste por
 * fotograma de los desenfoques a pantalla completa es el grueso del gasto.
 */

import { useEffect, useRef, type ReactNode } from "react";
import { createNoise3D } from "simplex-noise";
import { cn } from "@/lib/utils";

interface VortexProps {
  children?: ReactNode;
  className?: string;
  containerClassName?: string;
  particleCount?: number;
  rangeY?: number;
  baseHue?: number;
  rangeHue?: number;
  baseSpeed?: number;
  rangeSpeed?: number;
  baseRadius?: number;
  rangeRadius?: number;
  backgroundColor?: string;
  /** Pases de desenfoque por fotograma. El original hacia 2; 1 basta. */
  blurPasses?: 0 | 1 | 2;
}

const PROPS_PER_PARTICLE = 9;
const BASE_TTL = 50;
const RANGE_TTL = 150;
const NOISE_STEPS = 3;
const X_OFF = 0.00125;
const Y_OFF = 0.00125;
const Z_OFF = 0.0005;
const TAU = Math.PI * 2;

export function Vortex({
  children,
  className,
  containerClassName,
  particleCount = 400,
  rangeY = 320,
  baseHue = 258,
  rangeHue = 40,
  baseSpeed = 0,
  rangeSpeed = 1.5,
  baseRadius = 1,
  rangeRadius = 2,
  backgroundColor = "#06050F",
  blurPasses = 1,
}: VortexProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wrapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const wrap = wrapRef.current;
    if (!canvas || !wrap) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const len = particleCount * PROPS_PER_PARTICLE;
    const noise3D = createNoise3D();
    const props = new Float32Array(len);
    const center: [number, number] = [0, 0];
    let tick = 0;
    let raf = 0;
    let visible = true;
    let running = false;

    const rand = (n: number) => n * Math.random();
    const randRange = (n: number) => n - rand(2 * n);
    const fadeInOut = (t: number, m: number) => {
      const hm = 0.5 * m;
      return Math.abs(((t + hm) % m) - hm) / hm;
    };
    const lerp = (a: number, b: number, s: number) => (1 - s) * a + s * b;

    function initParticle(i: number) {
      props.set(
        [
          rand(canvas!.width),
          center[1] + randRange(rangeY),
          0,
          0,
          0,
          BASE_TTL + rand(RANGE_TTL),
          baseSpeed + rand(rangeSpeed),
          baseRadius + rand(rangeRadius),
          baseHue + rand(rangeHue),
        ],
        i,
      );
    }

    function resize() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const { width, height } = wrap!.getBoundingClientRect();
      canvas!.width = Math.max(1, Math.floor(width * dpr));
      canvas!.height = Math.max(1, Math.floor(height * dpr));
      canvas!.style.width = `${width}px`;
      canvas!.style.height = `${height}px`;
      center[0] = 0.5 * canvas!.width;
      center[1] = 0.5 * canvas!.height;
    }

    function drawParticle(
      x: number, y: number, x2: number, y2: number,
      life: number, ttl: number, radius: number, hue: number,
    ) {
      ctx!.save();
      ctx!.lineCap = "round";
      ctx!.lineWidth = radius;
      ctx!.strokeStyle = `hsla(${hue},95%,62%,${fadeInOut(life, ttl)})`;
      ctx!.beginPath();
      ctx!.moveTo(x, y);
      ctx!.lineTo(x2, y2);
      ctx!.stroke();
      ctx!.closePath();
      ctx!.restore();
    }

    function step() {
      tick++;
      ctx!.clearRect(0, 0, canvas!.width, canvas!.height);
      ctx!.fillStyle = backgroundColor;
      ctx!.fillRect(0, 0, canvas!.width, canvas!.height);

      for (let i = 0; i < len; i += PROPS_PER_PARTICLE) {
        const x = props[i];
        const y = props[i + 1];
        const n = noise3D(x * X_OFF, y * Y_OFF, tick * Z_OFF) * NOISE_STEPS * TAU;
        const vx = lerp(props[i + 2], Math.cos(n), 0.5);
        const vy = lerp(props[i + 3], Math.sin(n), 0.5);
        const life = props[i + 4];
        const ttl = props[i + 5];
        const speed = props[i + 6];
        const x2 = x + vx * speed;
        const y2 = y + vy * speed;

        drawParticle(x, y, x2, y2, life, ttl, props[i + 7], props[i + 8]);

        props[i] = x2;
        props[i + 1] = y2;
        props[i + 2] = vx;
        props[i + 3] = vy;
        props[i + 4] = life + 1;

        const fuera =
          x > canvas!.width || x < 0 || y > canvas!.height || y < 0 || life > ttl;
        if (fuera) initParticle(i);
      }

      // El resplandor es lo que mas cuesta por fotograma: un pase, no dos.
      for (let p = 0; p < blurPasses; p++) {
        ctx!.save();
        ctx!.filter = "blur(8px) brightness(180%)";
        ctx!.globalCompositeOperation = "lighter";
        ctx!.drawImage(canvas!, 0, 0);
        ctx!.restore();
      }

      if (running) raf = requestAnimationFrame(step);
    }

    function start() {
      if (running || reduced) return;
      running = true;
      raf = requestAnimationFrame(step);
    }
    function stop() {
      running = false;
      cancelAnimationFrame(raf);
    }

    resize();
    for (let i = 0; i < len; i += PROPS_PER_PARTICLE) initParticle(i);
    // Un fotograma siempre, para que con movimiento reducido no quede vacio
    running = false;
    step();

    const ro = new ResizeObserver(() => {
      resize();
      for (let i = 0; i < len; i += PROPS_PER_PARTICLE) initParticle(i);
    });
    ro.observe(wrap);

    const io = new IntersectionObserver(
      (entries) => {
        visible = entries.some((e) => e.isIntersecting);
        if (visible && !document.hidden) start();
        else stop();
      },
      { threshold: 0.01 },
    );
    io.observe(wrap);

    const onVisibility = () => {
      if (document.hidden || !visible) stop();
      else start();
    };
    document.addEventListener("visibilitychange", onVisibility);

    // Esto es lo que faltaba en el original: sin este return, la animacion
    // y los listeners sobreviven a la navegacion.
    return () => {
      stop();
      ro.disconnect();
      io.disconnect();
      document.removeEventListener("visibilitychange", onVisibility);
    };
  }, [
    particleCount, rangeY, baseHue, rangeHue, baseSpeed,
    rangeSpeed, baseRadius, rangeRadius, backgroundColor, blurPasses,
  ]);

  return (
    <div className={cn("vortex-root", containerClassName)}>
      <div ref={wrapRef} className="vortex-canvas-wrap">
        <canvas ref={canvasRef} className="vortex-canvas" />
      </div>
      {children ? <div className={cn("vortex-content", className)}>{children}</div> : null}
    </div>
  );
}

export default Vortex;
