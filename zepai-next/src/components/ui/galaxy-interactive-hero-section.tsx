"use client";

/**
 * Hero a dos columnas: mensaje a la izquierda, mascota a la derecha.
 *
 * Dos capas de fondo a fondo: hero.webp (20 KB) y un velo que oscurece la
 * columna del texto. La escena de Spline se ha quitado: hacia caer la
 * pestana del navegador. El 3D lo pone el robot, que es un render -- igual
 * que en el Instagram, donde tampoco hay nada interactivo -- y cuesta 47 KB
 * en vez de 2 MB.
 *
 * Lo importante de esta composicion: al pasar el texto a SU PROPIA COLUMNA,
 * la escena deja de estar detras de las letras. El problema de contraste que
 * arrastramos toda la sesion -- que obligo a medir pixeles, calcular velos y
 * descartar dos heros -- se resuelve por composicion, no por parches.
 *
 * El robot es lo que le faltaba a la web: la marca es de personaje (todas las
 * publicaciones del feed llevan uno) y aqui no habia ninguno.
 */

import { useEffect, useRef } from "react";
import Link from "next/link";
import { T } from "@/lib/i18n";

/* La etiqueta y el titular. En movil, todo lo que va ANTES del robot. */
function HeroArriba() {
  return (
    <div className="galaxy-arriba">
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
    </div>
  );
}

/* Lo que en movil va DESPUES del robot. */
function HeroAbajo() {
  return (
    <div className="galaxy-abajo">
      <p className="galaxy-sub">
        <T
          es="Automatizamos los procesos de tu empresa con inteligencia artificial: atención al cliente, ventas, reservas y las tareas que hoy os quitan horas."
          en="We automate your company's processes with artificial intelligence: customer service, sales, bookings and the tasks that eat your hours today."
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
        {/* Cuatro son nombres de marca y no se traducen; los otros dos si.
            Estaban sueltos en castellano y no se notaba porque /en no
            llegaba a montar el hero: en cuanto volvio, la pagina inglesa
            enseñaba "Tu sitio web" y "Telefono". */}
        <div className="galaxy-channels">
          {[
            { es: "WhatsApp", en: "WhatsApp" },
            { es: "Instagram", en: "Instagram" },
            { es: "Messenger", en: "Messenger" },
            { es: "Tu sitio web", en: "Your website" },
            { es: "Teléfono", en: "Phone" },
            { es: "Email", en: "Email" },
          ].map((c) => (
            <span className="galaxy-channel" key={c.es}>
              <T es={c.es} en={c.en} />
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

export function HeroSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const robotRef = useRef<HTMLDivElement>(null);

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

      <div className="galaxy-scrim" aria-hidden="true" />

      <div className="container galaxy-grid" ref={contentRef}>
        <HeroArriba />

        <div className="galaxy-mascot" ref={robotRef}>
          {/* Este es el elemento LCP de la portada, no el fondo. Le faltaba
              fetchPriority: el navegador se traia primero el hero.webp
              decorativo y el robot llegaba tarde (LCP 3,6 s en movil).

              El srcset esta calculado sobre los anchos CSS reales de
              galaxy.css -- 110 px en movil, 134 hasta 900, 220 en escritorio --
              multiplicados por la densidad de pantalla. En movil basta la
              variante de 300. */}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/hero/robot-v2.webp"
            srcSet="/hero/robot-v2-300.webp 300w, /hero/robot-v2.webp 400w"
            sizes="(max-width: 560px) 110px, (max-width: 900px) 134px, 220px"
            alt="Agente de IA de Zepai"
            width={400}
            height={1018}
            fetchPriority="high"
            decoding="async"
          />
        </div>

        <HeroAbajo />
      </div>
    </section>
  );
}

export default HeroSection;
