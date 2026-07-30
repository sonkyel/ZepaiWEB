/** Datos del sitio en un solo sitio. Antes vivian duplicados en 12 ficheros. */

export const SITE = {
  name: "Zepai Agency",
  url: "https://zepaiagency.com",
  email: "info@zepaiagency.com",
  tel: "+34604140997",
  telPretty: "+34 604 14 09 97",
  ogImage: "https://zepaiagency.com/og-image.png",
  instagram: "https://www.instagram.com/zepaiagency/",
  fundador: "Zecuenin Soto",
} as const;

export const WHATSAPP =
  "https://wa.me/34604140997?text=Hola,%20me%20gustar%C3%ADa%20saber%20m%C3%A1s%20sobre%20vuestros%20agentes%20de%20IA";

/** Menu principal. 5 elementos: con 7 la barra se partia en tres lineas. */
export const NAV = [
  { href: "/#services", es: "Servicios", en: "Services" },
  { href: "/consultoria-ia", es: "Consultoría IA", en: "AI Consulting" },
  { href: "/#industries", es: "Industrias", en: "Industries" },
  { href: "/soluciones", es: "Soluciones", en: "Solutions" },
  { href: "/#contact", es: "Contacto", en: "Contact" },
] as const;

export const FOOTER_SERVICIOS = [
  { href: "/soluciones", es: "Todas las soluciones", en: "All solutions" },
  { href: "/consultoria-ia", es: "Consultoría de IA", en: "AI Consulting" },
  { href: "/chatbot-whatsapp", es: "Chatbot de WhatsApp", en: "WhatsApp Chatbot" },
  { href: "/automatizacion-de-llamadas", es: "Llamadas con IA", en: "AI Calls" },
  { href: "/automatizaciones-n8n-make", es: "Automatizaciones n8n y Make", en: "n8n and Make automations" },
  { href: "/#services", es: "Marketing Digital", en: "Digital Marketing" },
  { href: "/#services", es: "Clipping de Contenido", en: "Content Clipping" },
  { href: "/#services", es: "Diseño Web", en: "Web Design" },
] as const;

export const FOOTER_INDUSTRIAS = [
  { href: "/agencia-ia-restaurantes", es: "Restaurantes", en: "Restaurants" },
  { href: "/agencia-ia-inmobiliarias", es: "Inmobiliarias", en: "Real Estate" },
  { href: "/agencia-ia-ecommerce", es: "E-Commerce", en: "E-Commerce" },
] as const;

export const FOOTER_EMPRESA = [
  { href: "/", es: "Inicio", en: "Home" },
  { href: "/como-trabajamos", es: "Cómo trabajamos", en: "How we work" },
  { href: "/blog", es: "Blog", en: "Blog" },
  { href: "/#results", es: "Resultados y clientes", en: "Results and clients" },
  { href: "/#contact", es: "Contacto", en: "Contact" },
] as const;

/** Organization + WebSite. Se inyecta una sola vez, en el layout raiz. */
export const ORGANIZATION_LD = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["Organization", "ProfessionalService"],
      "@id": `${SITE.url}/#organization`,
      name: SITE.name,
      url: SITE.url,
      logo: `${SITE.url}/logo.png`,
      image: SITE.ogImage,
      email: SITE.email,
      telephone: SITE.tel,
      description:
        "Agencia y consultora de inteligencia artificial. Automatizamos los procesos de las empresas con IA: atención al cliente, ventas, reservas, soporte y operaciones.",
      additionalType: "https://en.wikipedia.org/wiki/Artificial_intelligence",
      knowsAbout: [
        "Inteligencia artificial",
        "Automatización de procesos",
        "Agentes de IA",
        "Chatbots",
        "Asistentes de voz",
      ],
      areaServed: { "@type": "Place", name: "Worldwide" },
      availableLanguage: ["es", "en"],
      // Una persona con nombre detras de la marca. Google lo usa para el
      // panel de conocimiento y es la senal de "empresa real" que faltaba.
      founder: {
        "@type": "Person",
        "@id": `${SITE.url}/#fundador`,
        name: "Zecuenin Soto",
        jobTitle: "Fundador",
        image: `${SITE.url}/equipo/fundador.webp`,
        worksFor: { "@id": `${SITE.url}/#organization` },
        alumniOf: {
          "@type": "CollegeOrUniversity",
          name: "Universidad Europea de Madrid",
        },
        hasCredential: {
          "@type": "EducationalOccupationalCredential",
          credentialCategory: "degree",
          name: "Grado en Business and Analytics",
          educationalLevel: "Bachelor",
          recognizedBy: {
            "@type": "CollegeOrUniversity",
            name: "Universidad Europea de Madrid",
          },
        },
      },
      sameAs: [SITE.instagram],
      contactPoint: {
        "@type": "ContactPoint",
        contactType: "sales",
        email: SITE.email,
        telephone: SITE.tel,
        areaServed: "Worldwide",
        availableLanguage: ["Spanish", "English"],
      },
    },
    { "@type": "WebSite", name: SITE.name, url: SITE.url },
  ],
};

/**
 * Metadatos sociales de una pagina.
 *
 * Next NO funde el openGraph de la pagina con el del layout: lo sustituye.
 * Cualquier pagina que defina titulo propio pierde la imagen del layout, y
 * asi estuvieron las 12 paginas sin og:image. Este ayudante devuelve el
 * bloque completo para que no pueda volver a pasar.
 */
export function metaSocial(titulo: string, descripcion: string, ruta: string) {
  return {
    openGraph: {
      title: titulo,
      description: descripcion,
      url: `${SITE.url}${ruta}`,
      siteName: SITE.name,
      locale: "es_ES",
      type: "website" as const,
      images: [SITE.ogImage],
    },
    twitter: {
      card: "summary_large_image" as const,
      title: titulo,
      description: descripcion,
      images: [SITE.ogImage],
    },
  };
}
