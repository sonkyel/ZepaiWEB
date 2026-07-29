"use client";

/**
 * Da vida al contenido inyectado sin recibirlo como prop: lo busca en el DOM.
 * Asi el HTML no se serializa tambien en la carga de hidratacion.
 *
 *  - Traduce los elementos .i18n al cambiar de idioma, igual que hacia el
 *    setLang() de la web original.
 *  - Dispara el scroll-reveal (.reveal -> .v).
 */

import { useEffect } from "react";
import { useLang } from "@/lib/i18n";

export function LegacyEnhancer() {
  const { lang } = useLang();

  useEffect(() => {
    document.querySelectorAll<HTMLElement>("[data-legacy] .i18n").forEach((el) => {
      const txt = el.dataset[lang];
      if (txt !== undefined) el.textContent = txt;
    });
  }, [lang]);

  useEffect(() => {
    const targets = document.querySelectorAll<HTMLElement>("[data-legacy] .reveal");
    if (!targets.length) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      targets.forEach((el) => el.classList.add("v"));
      return;
    }

    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("v");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12 },
    );
    targets.forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, []);

  return null;
}
