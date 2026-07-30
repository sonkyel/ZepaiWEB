import type { Metadata } from "next";
import { LegacyContent } from "@/components/site/LegacyContent";
import { SITE, metaSocial } from "@/lib/site";

const TITULO = "Política de Cookies | Zepai Agency";
const DESC =
  "Qué cookies usa zepaiagency.com, para qué sirven y cómo retirar el consentimiento. Meta Pixel y Apollo solo se activan si los aceptas.";

export const metadata: Metadata = {
  title: TITULO,
  description: DESC,
  alternates: { canonical: "/politica-de-cookies" },
  ...metaSocial(TITULO, DESC, "/politica-de-cookies"),
};

const JSON_LD = [
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    name: "Política de Cookies",
    url: `${SITE.url}/politica-de-cookies`,
    inLanguage: "es",
    isPartOf: { "@id": `${SITE.url}/#organization` },
  },
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Inicio", item: `${SITE.url}/` },
      { "@type": "ListItem", position: 2, name: "Política de Cookies", item: `${SITE.url}/politica-de-cookies` },
    ],
  },
];

const HTML = `<section class="sp-hero">
    <div class="container">
      <div class="sp-hero-txt">
      <nav class="sp-crumbs" aria-label="Breadcrumb">
        <a href="/">Inicio</a>
        <span> / </span>
        <span>Política de Cookies</span>
      </nav>
      <h1 class="sp-h1">Política de Cookies</h1>
      <p class="sp-lead">Qué se guarda en tu navegador cuando visitas esta web, para qué sirve y cómo cambiar de opinión.</p>
      </div>
    </div>
  </section>

  <section class="sp-body">
    <div class="container">
      <p>Última actualización: julio de 2026.</p>

      <h2 class="sp-h2">Qué es una cookie</h2>
      <p>Un archivo pequeño que una web guarda en tu navegador para reconocer el dispositivo en visitas posteriores. Algunas las pone esta web y otras las ponen terceros a los que se les cede espacio.</p>

      <h2 class="sp-h2">Qué usamos, exactamente</h2>

      <h3 class="sp-h3">Sin cookies y sin consentimiento</h3>
      <ul class="sp-list">
        <li><strong>Idioma y consentimiento.</strong> El idioma que eliges y tu respuesta al aviso de cookies se guardan en el almacenamiento local del navegador, no en cookies. No se envían a ningún servidor y sirven para no volver a preguntarte lo mismo.</li>
        <li><strong>EmailJS.</strong> Solo interviene cuando envías un formulario, para hacer llegar tu mensaje. Es necesario para prestar el servicio que estás pidiendo, así que no requiere consentimiento previo, y no deja cookies publicitarias.</li>
      </ul>

      <h3 class="sp-h3">Solo si las aceptas</h3>
      <ul class="sp-list">
        <li><strong>Meta Pixel</strong> (Meta Platforms Ireland Ltd.). Mide cuántas visitas llegan desde Instagram y Facebook y permite mostrar anuncios a quien ya ha pasado por aquí. Deja cookies de terceros. Puedes revisar su <a href="https://www.facebook.com/privacy/policy/" target="_blank" rel="noopener">política de privacidad</a>.</li>
        <li><strong>Apollo.io</strong> (Apollo.io Inc.). Registra la visita de empresas para el seguimiento comercial. Deja cookies de terceros. Puedes revisar su <a href="https://www.apollo.io/privacy-policy" target="_blank" rel="noopener">política de privacidad</a>.</li>
      </ul>

      <p>Los dos son de fuera del Espacio Económico Europeo, así que aceptar implica una transferencia internacional de datos amparada en las cláusulas contractuales tipo de la Comisión Europea.</p>

      <h2 class="sp-h2">Mientras no aceptes, no se cargan</h2>
      <p>Ni Meta ni Apollo se descargan al abrir la página. El código solo se pide al servidor si pulsas «Aceptar». Si eliges «Solo lo necesario», o si cierras la web sin responder, no se ejecuta ninguno de los dos y la web funciona igual.</p>

      <h2 class="sp-h2">Cómo cambiar de opinión</h2>
      <p>Borra los datos de sitio de zepaiagency.com desde tu navegador y el aviso volverá a aparecer en la siguiente visita. En Chrome y Edge: candado de la barra de direcciones → Cookies y datos del sitio → Eliminar. En Firefox y Safari, desde la configuración de privacidad. También puedes bloquear las cookies de terceros de forma general desde el navegador.</p>

      <h2 class="sp-h2">Quién responde</h2>
      <p>Zepai Agency. Escríbenos a <a href="mailto:info@zepaiagency.com">info@zepaiagency.com</a> para cualquier duda sobre esta política o sobre tus datos. Si crees que no hemos atendido tu petición como debíamos, puedes reclamar ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es" target="_blank" rel="noopener">aepd.es</a>).</p>

      <section class="sp-related">
        <h2>Sigue explorando</h2>
        <ul>
          <li><a href="/">Inicio</a></li>
          <li><a href="/soluciones">Todas las soluciones</a></li>
          <li><a href="/como-trabajamos">Cómo trabajamos</a></li>
        </ul>
      </section>
    </div>
  </section>`;

export default function Page() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(JSON_LD) }}
      />
      <LegacyContent html={HTML} />
    </>
  );
}
