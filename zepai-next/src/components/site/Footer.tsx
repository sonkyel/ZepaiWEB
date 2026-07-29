import Link from "next/link";
import { T } from "@/lib/i18n";
import {
  FOOTER_EMPRESA,
  FOOTER_INDUSTRIAS,
  FOOTER_SERVICIOS,
  SITE,
  WHATSAPP,
} from "@/lib/site";

function Col({
  es,
  en,
  items,
}: {
  es: string;
  en: string;
  items: readonly { href: string; es: string; en: string }[];
}) {
  return (
    <div className="fcol">
      <h4>
        <T es={es} en={en} />
      </h4>
      <ul>
        {items.map((i) => (
          <li key={i.href + i.es}>
            <Link href={i.href}>
              <T es={i.es} en={i.en} />
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function Footer() {
  return (
    <footer>
      <div className="container">
        <div className="footer-grid">
          <div>
            <div className="f-logo">
              <div className="f-logo-badge">
                <Link href="/">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src="/logo.png" alt="ZEPAI Agency" className="logo-footer" />
                </Link>
              </div>
            </div>
            <p className="f-tag">
              <T
                es="Automatizamos negocios con inteligencia artificial para que crezcas sin límites."
                en="We automate businesses with artificial intelligence so you can grow without limits."
              />
            </p>
            <div className="f-contact">
              <a className="f-contact-link" href={WHATSAPP} target="_blank" rel="noopener">
                <span className="f-ci">💬</span>
                <span>WhatsApp {SITE.telPretty}</span>
              </a>
              <a className="f-contact-link" href={`tel:${SITE.tel}`}>
                <span className="f-ci">📞</span>
                <span>{SITE.telPretty}</span>
              </a>
              <a className="f-contact-link" href={`mailto:${SITE.email}`}>
                <span className="f-ci">📧</span>
                <span>{SITE.email}</span>
              </a>
            </div>
          </div>

          <Col es="Servicios" en="Services" items={FOOTER_SERVICIOS} />
          <Col es="Industrias" en="Industries" items={FOOTER_INDUSTRIAS} />
          <Col es="Empresa" en="Company" items={FOOTER_EMPRESA} />
        </div>

        <div className="footer-bot">
          <span className="f-copy">
            <T
              es="© 2026 Zepai Agency. Todos los derechos reservados."
              en="© 2026 Zepai Agency. All rights reserved."
            />
          </span>
          <a className="f-copy" href={`mailto:${SITE.email}`}>
            {SITE.email}
          </a>
        </div>
      </div>
    </footer>
  );
}
