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
const satoshi = localFont({
  src: [
    { path: "./fonts/Satoshi-500.woff2", weight: "500", style: "normal" },
    { path: "./fonts/Satoshi-700.woff2", weight: "700", style: "normal" },
    { path: "./fonts/Satoshi-900.woff2", weight: "900", style: "normal" },
  ],
  variable: "--font-satoshi",
  display: "swap",
});

const inter = Inter({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800", "900"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL(SITE.url),
  title:
    "Agencia y Consultora de IA | Automatización de Procesos con IA para Empresas | Zepai",
  description:
    "Agencia y consultora de IA. Automatizamos los procesos de tu empresa con inteligencia artificial: atención al cliente, ventas, reservas, soporte y operaciones. Consultoría e implementación a medida.",
  robots: { index: true, follow: true },
  icons: { icon: "/logo.png", apple: "/apple-touch-icon.png" },
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
