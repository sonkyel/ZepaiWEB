import type { Metadata, Viewport } from "next";
import { Inter, Nunito } from "next/font/google";

import "./globals.css";
import { LangProvider } from "@/lib/i18n";
import { Nav } from "@/components/site/Nav";
import { Footer } from "@/components/site/Footer";
import { WhatsAppFloat } from "@/components/site/WhatsAppFloat";
import { ORGANIZATION_LD, SITE } from "@/lib/site";

const inter = Inter({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800", "900"],
  variable: "--font-inter",
  display: "swap",
});
const nunito = Nunito({
  subsets: ["latin"],
  weight: ["900"],
  variable: "--font-nunito",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL(SITE.url),
  title:
    "Agencia y Consultora de IA | Automatización de Procesos con IA para Empresas | Zepai",
  description:
    "Agencia y consultora de IA. Automatizamos los procesos de tu empresa con inteligencia artificial: atención al cliente, ventas, reservas, soporte y operaciones. Consultoría e implementación a medida.",
  robots: { index: true, follow: true },
  icons: { icon: "/logo.png" },
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
    <html lang="es" className={`${inter.variable} ${nunito.variable}`}>
      <body>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(ORGANIZATION_LD) }}
        />
        <LangProvider>
          <Nav />
          <main>{children}</main>
          <Footer />
          <WhatsAppFloat />
        </LangProvider>
      </body>
    </html>
  );
}
