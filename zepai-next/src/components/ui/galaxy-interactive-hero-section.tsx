"use client";

/**
 * Hero de marca.
 *
 * Historia corta de por que es una imagen y no otra cosa:
 *  - Escena Spline: 1.972 KB por visita, alquilada (alojada en su servidor,
 *    imposible de recolorear) y, al moverse, hacia impredecible el contraste.
 *  - Vortex sobre canvas: ligero, pero animacion constante y el brillo
 *    aditivo volvia a comprometer la legibilidad. Se conserva en vortex.tsx.
 *  - Imagen generada por el cliente: 20 KB, es suya, y sobre todo es FIJA,
 *    asi que el contraste se puede medir leyendo sus pixeles en vez de
 *    estimarlo. El pixel mas claro de la banda del texto es #1A1F3F, que da
 *    16,0 con texto blanco. Por eso el velo aqui es minimo.
 *
 * Tambien se probo el video (200 KB, contraste 8,8): descartado porque a
 * 720p se notaba la falta de definicion.
 */

import { useEffect, useRef } from "react";
import Link from "next/link";
import { T } from "@/lib/i18n";

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

  // Desvanecido atado a la ALTURA REAL del hero. Con el calculo anterior
  // (1 - scrollY/420) el titular llegaba a cero con medio hero aun visible y
  // parecia que el texto faltaba.
  useEffect(() => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) return;

    const INICIO = 0.45;
    const MINIMA = 0.25;

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

      <div className="container galaxy-inner" ref={contentRef}>
        <HeroContent />
      </div>
    </section>
  );
}

export default HeroSection;
