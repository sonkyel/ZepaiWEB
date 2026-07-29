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

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

export type Lang = "es" | "en";

const STORAGE_KEY = "zepai-lang";

type Ctx = { lang: Lang; setLang: (l: Lang) => void };

const LangContext = createContext<Ctx>({ lang: "es", setLang: () => {} });

export function LangProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>("es");

  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(STORAGE_KEY);
      if (saved === "en" || saved === "es") setLangState(saved);
    } catch {
      /* localStorage bloqueado: nos quedamos en espanol */
    }
  }, []);

  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);

  const setLang = useCallback((l: Lang) => {
    setLangState(l);
    try {
      window.localStorage.setItem(STORAGE_KEY, l);
    } catch {
      /* sin persistencia, pero el cambio sigue funcionando en la sesion */
    }
  }, []);

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

export function LangToggle({ className = "" }: { className?: string }) {
  const { lang, setLang } = useLang();
  return (
    <div className={`lang-toggle ${className}`.trim()}>
      <button
        className={`lang-btn${lang === "es" ? " active" : ""}`}
        onClick={() => setLang("es")}
        aria-pressed={lang === "es"}
      >
        ES
      </button>
      <button
        className={`lang-btn${lang === "en" ? " active" : ""}`}
        onClick={() => setLang("en")}
        aria-pressed={lang === "en"}
      >
        EN
      </button>
    </div>
  );
}
