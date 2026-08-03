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
      {/* afterInteractive, no lazyOnload.

          lazyOnload espera al evento load de la ventana. Si el visitante
          entra por otra pagina y llega al inicio navegando, ese evento ya
          paso hace rato y este <Script> se monta despues: medido con el
          guion de prueba, a los 11 segundos seguia sin cargarse y la agenda
          se quedaba sin fechas.

          Son 18 KB y de aqui salen el formulario, la agenda y el acordeon
          del FAQ. No es decoracion que pueda esperar a que el navegador este
          ocioso: es la mitad de lo que un visitante puede querer pulsar. */}
      <Script src="/legacy-home.js" strategy="afterInteractive" />
    </>
  );
}
