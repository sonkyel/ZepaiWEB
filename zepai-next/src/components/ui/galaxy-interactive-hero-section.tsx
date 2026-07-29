"use client";

/**
 * Hero a dos columnas: mensaje a la izquierda, mascota a la derecha.
 *
 * Tres capas de fondo a fondo:
 *  1. hero.webp (20 KB): la imagen generada por el cliente. Se ve siempre,
 *     tambien en movil. Es la base.
 *  2. La escena de Spline (1.972 KB): 3D interactivo, solo escritorio y solo
 *     cuando el hero entra en pantalla.
 *  3. Un velo suave, que ahora solo funde con la nav y con la seccion
 *     siguiente.
 *
 * Lo importante de esta composicion: al pasar el texto a SU PROPIA COLUMNA,
 * la escena deja de estar detras de las letras. El problema de contraste que
 * arrastramos toda la sesion -- que obligo a medir pixeles, calcular velos y
 * descartar dos heros -- se resuelve por composicion, no por parches.
 *
 * El robot es lo que le faltaba a la web: la marca es de personaje (todas las
 * publicaciones del feed llevan uno) y aqui no habia ninguno.
 */

import { Suspense, lazy, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { T } from "@/lib/i18n";

const Spline = lazy(() => import("@splinetool/react-spline"));

const SCENE = "https://prod.spline.design/us3ALejTXl6usHZ7/scene.splinecode";

/** Decide si merece la pena descargar 2 MB de escena. */
function useShouldLoadScene(target: React.RefObject<HTMLElement | null>) {
  const [load, setLoad] = useState(false);

  useEffect(() => {
    if (typeof window === "undefined") return;

    const coarse = window.matchMedia("(max-width: 980px)").matches;
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    // @ts-expect-error -- connection es experimental y no esta en los tipos
    const conn = navigator.connection;
    const saveData = Boolean(conn?.saveData);
    const slow = /(^|-)2g$/.test(String(conn?.effectiveType ?? ""));
    if (coarse || reduced || saveData || slow) return;

    const el = target.current;
    if (!el) return;

    const io = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          setLoad(true);
          io.disconnect();
        }
      },
      { rootMargin: "200px" },
    );
    io.observe(el);
    return () => io.disconnect();
  }, [target]);

  return load;
}

function HeroContent() {
  return (
    <div className="galaxy-copy">
      <div className="galaxy-badge">
        <span className="galaxy-badge-dot" />
        <T es="Automatización de Procesos con IA" en="AI Process Automation" />
      </div>

      <h1 className="galaxy-title">
        <T
          es="Deja de perder clientes fuera de horario"
          en="Stop losing customers after hours"
        />
        <br />
        <span className="galaxy-title-grad">
          <T
            es="con agentes de IA que atienden 24/7"
            en="with AI agents that answer 24/7"
          />
        </span>
      </h1>

      <p className="galaxy-sub">
        <T
          es="Somos una agencia y consultora de inteligencia artificial: automatizamos la atención al cliente, las ventas y las reservas de tu empresa."
          en="We are an artificial intelligence agency and consultancy: we automate your company's customer service, sales and bookings."
        />
      </p>

      <div className="galaxy-actions">
        <a className="galaxy-cta" href="#contact">
          <T es="Pedir cotización gratis" en="Get a free quote" />
          <span aria-hidden="true">→</span>
        </a>
        <Link className="galaxy-link" href="/soluciones">
          <T es="o mira qué automatizamos" en="or see what we automate" />
        </Link>
      </div>

      <div className="galaxy-trust">
        <div className="galaxy-trust-label">
          <T
            es="Se integra en los canales que ya usas"
            en="Integrates into the channels you already use"
          />
        </div>
        <div className="galaxy-channels">
          {["WhatsApp", "Instagram", "Messenger", "Tu sitio web", "Teléfono", "Email"].map(
            (c) => (
              <span className="galaxy-channel" key={c}>
                {c}
              </span>
            ),
          )}
        </div>
      </div>
    </div>
  );
}

export function HeroSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const robotRef = useRef<HTMLDivElement>(null);
  const showScene = useShouldLoadScene(sectionRef);

  // Parallax del robot con el raton: unos pocos pixeles, lo justo para dar
  // profundidad. Sin libreria y sin coste apreciable.
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (window.matchMedia("(max-width: 980px)").matches) return;

    let raf = 0;
    const onMove = (e: MouseEvent) => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const el = robotRef.current;
        if (!el) return;
        const x = (e.clientX / window.innerWidth - 0.5) * 18;
        const y = (e.clientY / window.innerHeight - 0.5) * 12;
        el.style.transform = `translate3d(${x}px, ${y}px, 0)`;
      });
    };
    window.addEventListener("mousemove", onMove, { passive: true });
    return () => {
      window.removeEventListener("mousemove", onMove);
      cancelAnimationFrame(raf);
    };
  }, []);

  // El desvanecido va atado a la altura real del hero: con el calculo
  // anterior el titular llegaba a cero con medio hero aun a la vista.
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const INICIO = 0.5;
    const MINIMA = 0.3;
    let raf = 0;
    const onScroll = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const el = contentRef.current;
        const sec = sectionRef.current;
        if (!el || !sec) return;
        const alto = sec.offsetHeight || window.innerHeight;
        const t = Math.min(Math.max((window.scrollY / alto - INICIO) / (1 - INICIO), 0), 1);
        el.style.opacity = String(1 - (1 - MINIMA) * t);
      });
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <section id="hero" className="galaxy-hero" ref={sectionRef}>
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        className="galaxy-bg-img"
        src="/hero/hero.webp"
        alt=""
        aria-hidden="true"
        fetchPriority="high"
        decoding="async"
      />

      {showScene && (
        <Suspense fallback={null}>
          <div className="galaxy-scene-wrap" aria-hidden="true">
            <Spline className="galaxy-scene" scene={SCENE} />
          </div>
        </Suspense>
      )}

      <div className="galaxy-scrim" aria-hidden="true" />

      <div className="container galaxy-grid">
        <div className="galaxy-inner" ref={contentRef}>
          <HeroContent />
        </div>

        <div className="galaxy-mascot" ref={robotRef}>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/hero/robot.webp"
            alt="Agente de IA de Zepai"
            width={400}
            height={1005}
            decoding="async"
          />
        </div>
      </div>
    </section>
  );
}

export default HeroSection;
