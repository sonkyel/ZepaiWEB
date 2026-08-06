"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { LangToggle, T, useT } from "@/lib/i18n";
import { NAV } from "@/lib/site";

export function Nav() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const t = useT();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Cierra el menu movil al pasar a escritorio
  useEffect(() => {
    const mq = window.matchMedia("(min-width: 901px)");
    const onChange = () => mq.matches && setOpen(false);
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, []);

  return (
    <>
      <nav id="mainNav" className={scrolled ? "scrolled" : undefined}>
        <div className="nav-in">
          <Link className="nav-logo" href="/" aria-label={t("Zepai Agency — Inicio", "Zepai Agency — Home")}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            {/* .webp de 400x225 y no el .png de 666x375: se ve a 178x100 como
                mucho, y el PNG pesaba 50 KB en la nav de las 47 paginas.
                logo.png sigue existiendo porque es el que declara el JSON-LD
                como logo de la organizacion. */}
            <img src="/logo.webp" alt="ZEPAI Agency" className="logo-nav" width={400} height={225} />
          </Link>

          <ul className="nav-links">
            {NAV.map((item) => (
              <li key={item.href + item.es}>
                <Link href={item.href}>
                  <T es={item.es} en={item.en} />
                </Link>
              </li>
            ))}
          </ul>

          <div className="nav-right">
            <LangToggle />
            <a className="btn-p" href="/#contact">
              <T es="Pedir Cotización" en="Get a Quote" />
            </a>
          </div>

          <button
            className={`hamburger${open ? " open" : ""}`}
            onClick={() => setOpen((v) => !v)}
            aria-label={t("Abrir menú", "Open menu")}
            aria-expanded={open}
          >
            <span />
            <span />
            <span />
          </button>
        </div>
      </nav>

      <div className={`mobile-menu${open ? " open" : ""}`}>
        {NAV.map((item) => (
          <Link key={item.href + item.es} href={item.href} onClick={() => setOpen(false)}>
            <T es={item.es} en={item.en} />
          </Link>
        ))}
        <LangToggle className="mt-1" />
        <a className="btn-p" style={{ marginTop: 6 }} href="/#contact" onClick={() => setOpen(false)}>
          <T es="Pedir Cotización" en="Get a Quote" />
        </a>
      </div>
    </>
  );
}
