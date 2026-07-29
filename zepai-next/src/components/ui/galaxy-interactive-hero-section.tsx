"use client";

/**
 * Hero de marca con fondo Vortex.
 *
 * Antes llevaba una escena de Spline: 1.972 KB en cada visita de escritorio,
 * alquilada (alojada en su servidor, imposible de recolorear) y, al moverse,
 * hacia impredecible el contraste del texto. El Vortex logra un efecto
 * equivalente por ~5 KB, con la paleta de Zepai y bajo nuestro control.
 *
 * Tres capas, de abajo a arriba:
 *  1. BrandBackdrop: nebulosa y red de nodos en CSS. Es lo que se ve en movil
 *     y con movimiento reducido, donde el canvas no se anima.
 *  2. El canvas del vortice, con fondo transparente para que la nebulosa siga
 *     viendose por detras de las particulas.
 *  3. El velo, que es lo que garantiza la legibilidad: el vortice dibuja con
 *     mezcla aditiva y puede ponerse muy brillante justo donde esta el texto.
 *     Sus valores estan validados en check-contrast.py.
 */

import { useEffect, useRef } from "react";
import Link from "next/link";
import { T } from "@/lib/i18n";
import { BrandBackdrop } from "@/components/site/BrandBackdrop";
import { Vortex } from "@/components/ui/vortex";

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

  // El contenido se desvanece al hacer scroll, como en el componente original.
  useEffect(() => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) return;

    let raf = 0;
    const onScroll = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const el = contentRef.current;
        if (!el) return;
        const o = 1 - Math.min(window.scrollY / 420, 1);
        el.style.opacity = String(o);
      });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => {
      window.removeEventListener("scroll", onScroll);
      cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <section id="hero" className="galaxy-hero" ref={sectionRef}>
      {/* Debajo siempre: es lo que se ve en movil y si la escena no carga */}
      <BrandBackdrop />

      <div className="galaxy-scene-wrap">
        <Vortex
          particleCount={400}
          baseHue={258}
          rangeHue={40}
          rangeY={340}
          blurPasses={1}
          backgroundColor="transparent"
        />
      </div>

      {/* Encima de la escena: lo que hace predecible el contraste */}
      <div className="galaxy-scrim" aria-hidden="true" />

      <div className="container galaxy-inner" ref={contentRef}>
        <HeroContent />
      </div>
    </section>
  );
}

export default HeroSection;
