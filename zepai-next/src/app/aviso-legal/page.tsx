import type { Metadata } from "next";
import { LegacyContent } from "@/components/site/LegacyContent";
import { SITE, metaSocial } from "@/lib/site";

const TITULO = "Aviso Legal | Zepai Agency";
const DESC =
  "Datos identificativos del prestador del servicio, condiciones de uso de zepaiagency.com, propiedad intelectual y legislación aplicable.";

export const metadata: Metadata = {
  title: TITULO,
  description: DESC,
  alternates: { canonical: "/aviso-legal" },
  ...metaSocial(TITULO, DESC, "/aviso-legal"),
};

const JSON_LD = [
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    name: "Aviso Legal",
    url: `${SITE.url}/aviso-legal`,
    inLanguage: "es",
    isPartOf: { "@id": `${SITE.url}/#organization` },
  },
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Inicio", item: `${SITE.url}/` },
      { "@type": "ListItem", position: 2, name: "Aviso Legal", item: `${SITE.url}/aviso-legal` },
    ],
  },
];

const HTML = `<section class="sp-hero">
    <div class="container">
      <div class="sp-hero-txt">
      <nav class="sp-crumbs" aria-label="Breadcrumb">
        <a href="/">Inicio</a>
        <span> / </span>
        <span>Aviso Legal</span>
      </nav>
      <h1 class="sp-h1">Aviso Legal</h1>
      <p class="sp-lead">Quién está detrás de esta web, en qué condiciones se usa y a qué te comprometes al usarla.</p>
      </div>
    </div>
  </section>

  <section class="sp-body">
    <div class="container">
      <p>Última actualización: julio de 2026.</p>

      <h2 class="sp-h2">1. Datos del prestador del servicio</h2>
      <p>En cumplimiento del artículo 10 de la Ley 34/2002 de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se hacen constar los siguientes datos:</p>
      <ul class="sp-list">
        <li><strong>Titular:</strong> [PENDIENTE — razón social o nombre y apellidos]</li>
        <li><strong>NIF / CIF:</strong> [PENDIENTE]</li>
        <li><strong>Domicilio:</strong> [PENDIENTE]</li>
        <li><strong>Correo electrónico:</strong> <a href="mailto:info@zepaiagency.com">info@zepaiagency.com</a></li>
        <li><strong>Teléfono:</strong> <a href="tel:+34604140997">+34 604 14 09 97</a></li>
        <li><strong>Nombre comercial:</strong> Zepai Agency</li>
        <li><strong>Sitio web:</strong> zepaiagency.com</li>
      </ul>
      <p>Actividad: agencia y consultora de inteligencia artificial. Diseño e implantación de agentes de IA para atención al cliente, automatización de procesos y servicios de marketing digital.</p>

      <h2 class="sp-h2">2. Condiciones de uso</h2>
      <p>El acceso a este sitio es gratuito y no exige registro. Al navegar por él aceptas estas condiciones. Te comprometes a hacer un uso conforme a la ley y a no emplear la web para actividades ilícitas, ni a intentar dañar, sobrecargar o acceder sin autorización a sus sistemas.</p>
      <p>La información publicada tiene finalidad informativa y comercial. No constituye una oferta contractual vinculante: cualquier servicio se formaliza mediante presupuesto aceptado por escrito.</p>

      <h2 class="sp-h2">3. Propiedad intelectual e industrial</h2>
      <p>Los textos, el diseño, el código, las ilustraciones y la marca Zepai Agency son titularidad del prestador o se usan con autorización. No se permite su reproducción, distribución ni transformación sin permiso escrito, salvo el uso privado.</p>
      <p>Las marcas de terceros que aparecen citadas —WhatsApp, Instagram, Meta, TikTok, Make, n8n y cualesquiera otras— pertenecen a sus respectivos titulares y se mencionan únicamente a efectos identificativos y descriptivos. Su mención no implica asociación, patrocinio ni certificación por parte de esas empresas.</p>

      <h2 class="sp-h2">4. Enlaces a otros sitios</h2>
      <p>Esta web enlaza a sitios de terceros, como el de nuestros clientes o nuestro perfil de Instagram. No respondemos de sus contenidos ni de sus políticas de privacidad: al seguir esos enlaces sales de nuestro ámbito de responsabilidad.</p>

      <h2 class="sp-h2">5. Responsabilidad</h2>
      <p>Procuramos que la información esté actualizada y libre de errores, pero no podemos garantizarlo en todo momento. Tampoco garantizamos la disponibilidad ininterrumpida del sitio, que depende de proveedores de alojamiento y de la propia red.</p>
      <p>No respondemos de los daños derivados del uso de la información publicada cuando ese uso se haga sin la valoración profesional previa que cada caso requiere.</p>

      <h2 class="sp-h2">6. Protección de datos</h2>
      <p>El tratamiento de los datos personales que nos facilitas se describe en la <a href="/politica-de-privacidad">Política de Privacidad</a>. El uso de cookies se detalla en la <a href="/politica-de-cookies">Política de Cookies</a>.</p>

      <h2 class="sp-h2">7. Legislación aplicable</h2>
      <p>Estas condiciones se rigen por la legislación española. Para cualquier controversia, las partes se someten a los juzgados y tribunales del domicilio del titular, salvo que la normativa de consumo establezca otro fuero imperativo.</p>

      <section class="sp-related">
        <h2>Sigue explorando</h2>
        <ul>
          <li><a href="/politica-de-privacidad">Política de Privacidad</a></li>
          <li><a href="/politica-de-cookies">Política de Cookies</a></li>
          <li><a href="/">Inicio</a></li>
        </ul>
      </section>
    </div>
  </section>`;

export default function Page() {
  return (
    <>
      {JSON_LD.map((ld, i) => (
        <script
          key={i}
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(ld) }}
        />
      ))}
      <LegacyContent html={HTML} />
    </>
  );
}
