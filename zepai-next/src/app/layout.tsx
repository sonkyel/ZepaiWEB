import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import localFont from "next/font/local";

import "./globals.css";
import { LangProvider } from "@/lib/i18n";
import { Nav } from "@/components/site/Nav";
import { Footer } from "@/components/site/Footer";
import { WhatsAppFloat } from "@/components/site/WhatsAppFloat";
import { Consent } from "@/components/site/Consent";
import { ORGANIZATION_LD, SITE } from "@/lib/site";

// Satoshi (Fontshare, libre para uso comercial) autoalojada: una peticion
// externa menos y sin salto de texto. Sustituye a Nunito, que se descargaba
// y no se usaba en ninguna parte.
// Satoshi solo se usa en titulares, y ningun titular baja de 700: los pesos
// declarados en el CSS son 700, 800 y 900. El fichero de 500 se precargaba en
// cada visita -- 25 KB, uno de los cuatro preloads que compiten con la imagen
// del hero -- y no pintaba un solo glifo. Comprobado ademas por captura: la
// web se ve identica pixel a pixel sin el.
const satoshi = localFont({
  src: [
    { path: "./fonts/Satoshi-700.woff2", weight: "700", style: "normal" },
    { path: "./fonts/Satoshi-900.woff2", weight: "900", style: "normal" },
  ],
  variable: "--font-satoshi",
  display: "swap",
});

// Sin lista de pesos: Inter se sirve como fuente variable, asi que los siete
// pesos apuntaban al MISMO fichero. Declararlos no descargaba nada de mas,
// pero generaba 49 reglas @font-face en vez de 7.
const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL(SITE.url),
  // 55 caracteres. El anterior tenia 84 y Google lo cortaba por la mitad:
  // en el buscador se leia "...Automatizacion de Procesos con IA para..." y
  // la marca, que es lo unico que no puede faltar, se perdia.
  title: "Automatización de Procesos con IA para Empresas | Zepai",
  description:
    "Automatizamos los procesos de tu empresa con IA: atención al cliente, ventas, reservas y soporte. Consultoría e implementación a medida.",
  robots: { index: true, follow: true },
  // x-default: le dice a Google que servir a quien no encaje en ningun
  // idioma declarado. Sin el, elige por su cuenta.
  alternates: {
    canonical: "/",
    languages: { es: "/", en: "/en", "x-default": "/" },
  },
  // Sin icon: lo pone src/app/favicon.ico por convencion de fichero, y ahi
  // esta la marca en seis tamanos. Declarar ademas /logo.png metia un
  // segundo <link rel=icon> con el logotipo entero, de 666x375: el navegador
  // podia elegir ese y aplastarlo en un cuadrado de 16 px.
  icons: { apple: "/apple-touch-icon.png" },
  openGraph: {
    type: "website",
    siteName: SITE.name,
    locale: "es_ES",
    alternateLocale: ["en_US"],
    images: [SITE.ogImage],
  },
  twitter: { card: "summary_large_image", images: [SITE.ogImage] },
};

// themeColor va aqui: dentro de metadata quedo deprecado desde Next 14.
export const viewport: Viewport = {
  themeColor: "#0a0a0a",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" className={`${inter.variable} ${satoshi.variable}`}>
      <body>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(ORGANIZATION_LD) }}
        />
        <LangProvider>
          {/* Sin esto, con teclado hay que recorrer toda la nav en cada
              pagina antes de llegar al contenido. */}
          <a className="saltar" href="#contenido">
            Saltar al contenido
          </a>
          <Nav />
          <main id="contenido">{children}</main>
          <Footer />
          <WhatsAppFloat />
          <Consent />
        </LangProvider>
      </body>
    </html>
  );
}
