"use client";

/**
 * i18n ES/EN.
 *
 * Replica el sistema que ya tenia la web estatica (atributos data-es y
 * data-en con un toggle que guardaba el idioma en localStorage), pero en
 * React. Asi el porte de las 12 paginas es mecanico: cada
 * `<span class="i18n" data-es="A" data-en="B">A</span>` pasa a `<T es="A" en="B" />`.
 *
 * Importante para SEO: el servidor renderiza SIEMPRE espanol. El cambio a
 * ingles ocurre despues de montar en el cliente, asi que Google indexa el
 * castellano, que es el idioma objetivo.
 */

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

export type Lang = "es" | "en";

type Ctx = { lang: Lang; setLang: (l: Lang) => void };

const LangContext = createContext<Ctx>({ lang: "es", setLang: () => {} });

export function LangProvider({ children }: { children: ReactNode }) {
  /* El idioma lo decide la URL: /en/... es ingles y el resto castellano.
     Asi el HTML que se genera ya sale en el idioma correcto, que es lo que
     lee Google. Antes se renderizaba siempre en espanol y el cambio ocurria
     despues en el navegador, de modo que /en llegaba medio traducida. */
  const ruta = usePathname() || "/";
  const porRuta: Lang = ruta === "/en" || ruta.startsWith("/en/") ? "en" : "es";
  const [lang, setLangState] = useState<Lang>(porRuta);

  useEffect(() => {
    setLangState(porRuta);
  }, [porRuta]);

  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);

  /* Se conserva por compatibilidad con el codigo heredado, pero ya no es
     la via normal: el idioma se cambia navegando. */
  const setLang = useCallback((l: Lang) => setLangState(l), []);

  return (
    <LangContext.Provider value={{ lang, setLang }}>
      {children}
    </LangContext.Provider>
  );
}

export function useLang() {
  return useContext(LangContext);
}

/** Texto bilingue. Equivalente a la clase .i18n de la web estatica. */
export function T({ es, en }: { es: string; en: string }) {
  const { lang } = useLang();
  return <>{lang === "en" ? en : es}</>;
}

/** Devuelve el texto suelto, para atributos (aria-label, title, alt...). */
export function useT() {
  const { lang } = useLang();
  return useCallback((es: string, en: string) => (lang === "en" ? en : es), [lang]);
}

/* Rutas que solo existen en castellano: son textos de la ley espanola. */
const SOLO_ES = ["/aviso-legal", "/politica-de-privacidad", "/politica-de-cookies"];

/** La pareja de la ruta actual en el otro idioma. */
export function otroIdioma(ruta: string, destino: Lang) {
  const limpia = ruta.replace(/\/$/, "") || "/";
  const esIngles = limpia === "/en" || limpia.startsWith("/en/");
  const base = esIngles ? limpia.slice(3) || "/" : limpia;
  if (SOLO_ES.includes(base)) return destino === "en" ? "/en" : base;
  if (destino === "en") return base === "/" ? "/en" : "/en" + base;
  return base;
}

export function LangToggle({ className = "" }: { className?: string }) {
  const ruta = usePathname() || "/";
  const enIngles = ruta === "/en" || ruta.startsWith("/en/");
  return (
    <div className={`lang-toggle ${className}`.trim()}>
      {/* Enlaces, no botones: antes el idioma cambiaba en memoria y la URL
          seguia siendo la espanola, asi que la version inglesa no se podia
          compartir ni indexar. */}
      <Link
        className={`lang-btn${!enIngles ? " active" : ""}`}
        href={otroIdioma(ruta, "es")}
        hrefLang="es"
        aria-current={!enIngles ? "true" : undefined}
      >
        ES
      </Link>
      <Link
        className={`lang-btn${enIngles ? " active" : ""}`}
        href={otroIdioma(ruta, "en")}
        hrefLang="en"
        aria-current={enIngles ? "true" : undefined}
      >
        EN
      </Link>
    </div>
  );
}
