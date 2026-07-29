"use client";

/**
 * Carga el JS interactivo de la home: formulario de contacto (EmailJS),
 * agenda de llamadas, acordeon del FAQ, modal de privacidad y contadores.
 *
 * Se carga con strategy="lazyOnload" y EmailJS solo cuando el visitante se
 * acerca al formulario: no tiene sentido descargar el SDK de correo para
 * alguien que solo lee el hero.
 */

import Script from "next/script";
import { useEffect, useState } from "react";

export function HomeScripts() {
  const [needsEmail, setNeedsEmail] = useState(false);

  useEffect(() => {
    const target = document.getElementById("contact");
    if (!target) return;

    const io = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          setNeedsEmail(true);
          io.disconnect();
        }
      },
      { rootMargin: "600px" },
    );
    io.observe(target);
    return () => io.disconnect();
  }, []);

  return (
    <>
      {needsEmail && (
        <Script
          src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"
          strategy="afterInteractive"
        />
      )}
      <Script src="/legacy-home.js" strategy="lazyOnload" />
    </>
  );
}
