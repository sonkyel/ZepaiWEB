import type { Metadata } from "next";
import Link from "next/link";
import { T } from "@/lib/i18n";

export const metadata: Metadata = {
  title: "Página no encontrada | Zepai Agency",
  // Una 404 no debe indexarse ni repartir autoridad a los enlaces que lleva.
  robots: { index: false, follow: false },
};

const SALIDAS = [
  { href: "/", es: "Volver al inicio", en: "Back to home" },
  { href: "/soluciones", es: "Todas las soluciones", en: "All solutions" },
  { href: "/agentes-de-ia", es: "Agentes de IA", en: "AI agents" },
  { href: "/blog", es: "Blog", en: "Blog" },
];

export default function NotFound() {
  return (
    <section className="sp-hero e404">
      <div className="container e404-in">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          className="e404-art"
          src="/paginas/error-404.webp"
          width={900}
          height={672}
          alt="Robot de IA con cara de no encontrar la página"
          decoding="async"
        />
        <div>
          <div className="section-label">
            <T es="Error 404" en="Error 404" />
          </div>
          <h1 className="sp-h1">
            <T es="Esta página no existe" en="This page does not exist" />
          </h1>
          <p className="sp-lead">
            <T
              es="O se ha movido, o el enlace venía mal escrito. Lo que buscabas probablemente esté aquí debajo."
              en="Either it moved, or the link was mistyped. What you were looking for is probably below."
            />
          </p>
          <ul className="e404-salidas">
            {SALIDAS.map((s) => (
              <li key={s.href}>
                <Link href={s.href}>
                  <T es={s.es} en={s.en} />
                </Link>
              </li>
            ))}
          </ul>
          <a className="btn-p" href="/#contact">
            <span>
              <T es="Hablar con nosotros" en="Talk to us" />
            </span>
            <span aria-hidden="true">&rarr;</span>
          </a>
        </div>
      </div>
    </section>
  );
}
