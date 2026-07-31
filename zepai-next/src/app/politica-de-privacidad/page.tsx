import type { Metadata } from "next";
import { LegacyContent } from "@/components/site/LegacyContent";
import { SITE, metaSocial } from "@/lib/site";

const TITULO = "Política de Privacidad | Zepai Agency";
const DESC =
  "Qué datos recogemos cuando escribes o agendas una llamada, para qué los usamos, cuánto los conservamos y cómo ejercer tus derechos.";

export const metadata: Metadata = {
  title: TITULO,
  description: DESC,
  alternates: { canonical: "/politica-de-privacidad" },
  ...metaSocial(TITULO, DESC, "/politica-de-privacidad"),
};

const JSON_LD = [
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    name: "Política de Privacidad",
    url: `${SITE.url}/politica-de-privacidad`,
    inLanguage: "es",
    isPartOf: { "@id": `${SITE.url}/#organization` },
  },
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Inicio", item: `${SITE.url}/` },
      { "@type": "ListItem", position: 2, name: "Política de Privacidad", item: `${SITE.url}/politica-de-privacidad` },
    ],
  },
];

const HTML = `<section class="sp-hero">
    <div class="container">
      <div class="sp-hero-txt">
      <nav class="sp-crumbs" aria-label="Breadcrumb">
        <a href="/">Inicio</a>
        <span> / </span>
        <span>Política de Privacidad</span>
      </nav>
      <h1 class="sp-h1">Política de Privacidad</h1>
      <p class="sp-lead">Qué datos nos das, qué hacemos con ellos y cómo recuperarlos o borrarlos cuando quieras.</p>
      </div>
    </div>
  </section>

  <section class="sp-body">
    <div class="container">
      <p>Última actualización: julio de 2026.</p>

      <h2 class="sp-h2">1. Quién trata tus datos</h2>
      <p>El responsable del tratamiento es <strong>Zepai Agency</strong>, con domicilio en España. La sociedad está en proceso de constitución: la razón social, el NIF y el domicilio completos se publicarán aquí y en el <a href="/aviso-legal">Aviso Legal</a> en cuanto se complete el trámite.</p>
      <p>Para cualquier asunto relacionado con tus datos: <a href="mailto:info@zepaiagency.com">info@zepaiagency.com</a>.</p>

      <h2 class="sp-h2">2. Qué datos recogemos</h2>
      <p>Solo los que nos das tú, al rellenar uno de los dos formularios de la web:</p>
      <ul class="sp-list">
        <li><strong>Agendar una llamada:</strong> nombre, correo electrónico, teléfono o WhatsApp (opcional), tipo de negocio, fecha y horario preferidos, y lo que quieras contarnos.</li>
        <li><strong>Pedir cotización:</strong> nombre, empresa (opcional), correo electrónico, tipo de negocio, servicio de interés y tu mensaje.</li>
      </ul>
      <p>No pedimos datos de categorías especiales —salud, ideología, origen— ni datos de pago. Si nos los envías por tu cuenta en el campo de texto libre, los eliminaremos.</p>

      <h2 class="sp-h2">3. Para qué los usamos y con qué base legal</h2>
      <ul class="sp-list">
        <li><strong>Responder a tu solicitud y preparar la conversación comercial.</strong> Base jurídica: tu consentimiento, que das marcando la casilla del formulario (art. 6.1.a del RGPD), y la aplicación de medidas precontractuales a petición tuya (art. 6.1.b).</li>
        <li><strong>Medir de dónde llegan las visitas</strong>, mediante Meta Pixel y Apollo. Base jurídica: tu consentimiento, que das aceptando en el aviso de cookies. Si no lo aceptas, esas herramientas no se cargan. Se detalla en la <a href="/politica-de-cookies">Política de Cookies</a>.</li>
      </ul>
      <p>No usamos tus datos para decisiones automatizadas con efectos jurídicos, ni elaboramos perfiles con ellos.</p>

      <h2 class="sp-h2">4. Quién más los ve</h2>
      <p>No vendemos ni cedemos tus datos. Solo los tratan los proveedores estrictamente necesarios para que la web funcione:</p>
      <ul class="sp-list">
        <li><strong>EmailJS</strong> (EmailJS Inc., Estados Unidos): entrega a nuestro correo el contenido de los formularios. Es el encargado que hace posible que tu mensaje nos llegue.</li>
        <li><strong>Vercel</strong> (Vercel Inc., Estados Unidos): alojamiento del sitio. Registra datos técnicos de conexión, como la dirección IP, con fines de seguridad y funcionamiento.</li>
        <li><strong>Meta</strong> (Meta Platforms Ireland Ltd.) y <strong>Apollo.io</strong> (Apollo.io Inc., Estados Unidos): medición, y solo si aceptas las cookies.</li>
      </ul>
      <p>Algunos están fuera del Espacio Económico Europeo. Esas transferencias internacionales se amparan en las cláusulas contractuales tipo aprobadas por la Comisión Europea.</p>

      <h2 class="sp-h2">5. Cuánto tiempo los guardamos</h2>
      <p>Los datos de una solicitud se conservan mientras dure la conversación comercial y, después, durante un año, por si retomas el contacto. Si llegamos a trabajar juntos, se conservan durante la relación y los plazos de prescripción legal que correspondan. Puedes pedirnos que los borremos antes.</p>

      <h2 class="sp-h2">6. Cómo protegemos la información</h2>
      <p>Todo el sitio se sirve por conexión cifrada (HTTPS), con las cabeceras de seguridad activadas para evitar que la página se incruste en otros sitios o que el navegador ejecute código no previsto. El acceso al buzón donde llegan las solicitudes está limitado a Zepai Agency.</p>
      <p>Ningún sistema es infalible. Si se produjera una brecha que afecte a tus datos, lo notificaremos a la Agencia Española de Protección de Datos y, cuando proceda, a ti, en los plazos que marca el RGPD.</p>

      <h2 class="sp-h2">7. Tus derechos</h2>
      <p>Puedes pedirnos en cualquier momento:</p>
      <ul class="sp-list">
        <li><strong>Acceso:</strong> saber qué datos tuyos tenemos.</li>
        <li><strong>Rectificación:</strong> corregir los que sean inexactos.</li>
        <li><strong>Supresión:</strong> que los borremos.</li>
        <li><strong>Limitación y oposición:</strong> que dejemos de tratarlos o que restrinjamos su uso.</li>
        <li><strong>Portabilidad:</strong> recibirlos en un formato que puedas llevarte.</li>
        <li><strong>Retirar el consentimiento</strong> en cualquier momento, sin que eso afecte a lo hecho antes.</li>
      </ul>
      <p>Escríbenos a <a href="mailto:info@zepaiagency.com">info@zepaiagency.com</a> indicando qué derecho quieres ejercer. Responderemos en el plazo de un mes.</p>
      <p>Si crees que no hemos atendido tu petición como debíamos, puedes reclamar ante la <strong>Agencia Española de Protección de Datos</strong>, en <a href="https://www.aepd.es" target="_blank" rel="noopener noreferrer">aepd.es</a>.</p>

      <h2 class="sp-h2">8. Cambios en esta política</h2>
      <p>Si cambia lo que hacemos con los datos, actualizaremos esta página y la fecha del encabezado. Los cambios relevantes se avisarán en la propia web.</p>

      <section class="sp-related">
        <h2>Sigue explorando</h2>
        <ul>
          <li><a href="/aviso-legal">Aviso Legal</a></li>
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
