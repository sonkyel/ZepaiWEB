"use client";

/**
 * Da vida al contenido inyectado sin recibirlo como prop: lo busca en el DOM.
 * Asi el HTML no se serializa tambien en la carga de hidratacion.
 *
 *  - Traduce los elementos .i18n al cambiar de idioma, igual que hacia el
 *    setLang() de la web original.
 *  - Dispara el scroll-reveal (.reveal -> .v).
 *
 * POR QUE EL REVELADO YA NO USA IntersectionObserver
 * --------------------------------------------------
 * Lo usaba, y dejaba secciones en blanco. Al pulsar "Contacto" en la barra,
 * el navegador salta directo a #contact y sus dos bloques -- que son TODO el
 * contenido de la seccion -- se quedaban en opacity:0 para siempre.
 *
 * El fallo de fondo no era el observador sino el reparto de
 * responsabilidades: 27 bloques de la portada nacian invisibles y dependian
 * de que llegase un callback. Si no llega -- salto a un ancla, restauracion
 * desde el cache de atras/adelante, hidratacion lenta, o un bloque mas alto
 * que la ventana que nunca alcanza el 12 % de umbral -- no hay segunda
 * oportunidad: la seccion se queda vacia y sin un solo aviso en la consola.
 *
 * Ahora:
 *   1. El contenido es visible por defecto. La clase js-reveal la pone este
 *      componente al montarse, y solo entonces el CSS se atreve a ocultar
 *      algo. Sin JS, con JS caido o si este fichero falla, se ve todo.
 *   2. El calculo es directo, con getBoundingClientRect en scroll y resize.
 *      No hay callback que se pueda perder.
 *   3. Y por si acaso, una red de seguridad a los 2,5 s revela lo que quede.
 *      Prefiero perder una animacion que perder una seccion.
 */

import { useEffect } from "react";
import { useLang } from "@/lib/i18n";

/** Se revela un poco antes de que el bloque toque el borde inferior. */
const ANTICIPO = 0.08;

declare global {
  interface Window {
    zepaiAgenda?: () => void;
  }
}

export function LegacyEnhancer() {
  const { lang } = useLang();

  useEffect(() => {
    document.querySelectorAll<HTMLElement>("[data-legacy] .i18n").forEach((el) => {
      const txt = el.dataset[lang];
      if (txt !== undefined) el.textContent = txt;
    });
  }, [lang]);

  /**
   * Reconstruye el selector de fecha.
   *
   * legacy-home.js se ejecuta UNA vez por visita -- Next no reevalua un
   * <Script> con el mismo src -- pero este HTML se repinta cada vez que se
   * monta la pagina: al volver al inicio desde otra pagina, o al cambiar de
   * idioma. El repintado se lleva los botones que el guion habia creado y
   * nadie los volvia a poner, asi que la agenda se quedaba con el texto de
   * respaldo y no se podia reservar.
   *
   * Se reintenta porque el guion carga con lazyOnload y puede llegar despues
   * que este efecto.
   */
  useEffect(() => {
    if (!document.getElementById("datePicker")) return;
    let intentos = 0;
    let temporizador = 0;

    const intentar = () => {
      const hecho = document.querySelector("#datePicker .date-btn");
      if (hecho) return;
      if (window.zepaiAgenda) {
        window.zepaiAgenda();
        return;
      }
      if (++intentos < 40) temporizador = window.setTimeout(intentar, 150);
    };

    intentar();
    return () => clearTimeout(temporizador);
  }, [lang]);

  useEffect(() => {
    const bloques = () =>
      Array.from(document.querySelectorAll<HTMLElement>("[data-legacy] .reveal"));

    if (!bloques().length) return;

    // Sin animacion: no se oculta nada y no hay nada mas que vigilar.
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      bloques().forEach((el) => el.classList.add("v"));
      return;
    }

    document.documentElement.classList.add("js-reveal");

    let cuadro = 0;
    let desmontado = false;

    const desmontar = () => {
      if (desmontado) return;
      desmontado = true;
      sucesos.forEach((n) => window.removeEventListener(n, pedir));
      tardias.forEach(clearTimeout);
      clearTimeout(rescate);
      if (cuadro) cancelAnimationFrame(cuadro);
    };

    const pasada = () => {
      cuadro = 0;
      const limite = window.innerHeight * (1 - ANTICIPO);
      let quedan = 0;
      for (const el of bloques()) {
        if (el.classList.contains("v")) continue;
        const r = el.getBoundingClientRect();
        // Con que el borde superior haya entrado basta, y lo que ya quedo
        // por encima se revela tambien: asi un bloque mas alto que la
        // ventana aparece, cosa que con umbral de ratio no pasaba.
        if (r.bottom <= 0 || r.top < limite) el.classList.add("v");
        else quedan++;
      }
      if (!quedan) desmontar();
    };

    const pedir = () => {
      if (!cuadro) cuadro = requestAnimationFrame(pasada);
    };

    const sucesos = ["scroll", "resize", "hashchange", "pageshow", "load"];
    sucesos.forEach((n) => window.addEventListener(n, pedir, { passive: true }));

    // El salto al ancla puede ocurrir despues de montar: se repasa un par de
    // veces mas antes de dar por hecho que la posicion es la definitiva.
    const tardias = [120, 600].map((ms) => window.setTimeout(pedir, ms));

    // Red de seguridad: si algo impidio revelar, gana el contenido.
    const rescate = window.setTimeout(
      () => bloques().forEach((el) => el.classList.add("v")),
      2500,
    );

    pasada();
    return desmontar;
  }, []);

  return null;
}
