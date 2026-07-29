"use client";

/**
 * Hero de marca con escena Spline.
 *
 * La escena es la que le gusta al cliente, asi que se queda. Lo que NO se
 * queda es el problema que traia: al moverse hacia impredecible el contraste
 * y la segunda linea del titular llegaba a 1,2 (WCAG AA pide 4,5).
 *
 * La solucion no es quitar la escena, es garantizar el fondo tras el texto:
 *  - BrandBackdrop debajo, siempre. Es lo que se ve en movil y mientras (o
 *    si) la escena no carga, con la paleta de Zepai y su red de nodos.
 *  - Un velo centrado encima de la escena que asegura que detras de las
 *    letras nunca haya nada mas claro que #241A4A, que es el fondo contra el
 *    que se valida en check-contrast.py.
 *
 * La escena pesa ~2 MB: no se descarga en movil, ni con ahorro de datos, ni
 * en 2G, ni si se pidio reducir movimiento, ni hasta que el hero entra en
 * pantalla.
 */

import { Suspense, lazy, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { T } from "@/lib/i18n";
import { BrandBackdrop } from "@/components/site/BrandBackdrop";

const Spline = lazy(() => import("@splinetool/react-spline"));

const SCENE = "https://prod.spline.design/us3ALejTXl6usHZ7/scene.splinecode";

/** Decide si merece la pena descargar 2 MB de escena. */
function useShouldLoadScene(target: React.RefObject<HTMLElement | null>) {
  const [load, setLoad] = useState(false);

  useEffect(() => {
    if (typeof window === "undefined") return;

    const coarse = window.matchMedia("(max-width: 900px)").matches;
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
  const showScene = useShouldLoadScene(sectionRef);

  // Desvanecido del contenido al hacer scroll.
  //
  // Antes usaba `1 - scrollY / 420`: con un hero de una pantalla completa el
  // titular llegaba a opacidad 0 con medio hero todavia a la vista, y parecia
  // que el texto faltaba. Ahora se ata a la ALTURA REAL del hero: no empieza
  // hasta haber recorrido el 45 % y nunca baja de 0,25, asi que el titular
  // sigue legible mientras el hero este en pantalla.
  useEffect(() => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) return;

    const INICIO = 0.45; // no se desvanece hasta este % del hero recorrido
    const MINIMA = 0.25; // nunca desaparece del todo

    let raf = 0;
    const onScroll = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const el = contentRef.current;
        const sec = sectionRef.current;
        if (!el || !sec) return;

        const alto = sec.offsetHeight || window.innerHeight;
        const avance = window.scrollY / alto; // 0 arriba, 1 al final del hero
        const t = Math.min(Math.max((avance - INICIO) / (1 - INICIO), 0), 1);
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
      {/* Debajo siempre: es lo que se ve en movil y si la escena no carga */}
      <BrandBackdrop />

      {showScene && (
        <Suspense fallback={null}>
          <div className="galaxy-scene-wrap">
            <Spline
              className="galaxy-scene"
              scene={SCENE}
              style={{ width: "100%", height: "100%", pointerEvents: "auto" }}
            />
          </div>
        </Suspense>
      )}

      {/* Encima de la escena: lo que hace predecible el contraste */}
      <div className="galaxy-scrim" aria-hidden="true" />

      <div className="container galaxy-inner" ref={contentRef}>
        <HeroContent />
      </div>
    </section>
  );
}

export default HeroSection;
