import { LegacyEnhancer } from "./LegacyEnhancer";

/**
 * Inyecta el contenido de la web original tal cual.
 *
 * El HTML, las clases y los atributos data-es/data-en son exactamente los
 * mismos que ya estaban indexados: no se pierde ni una palabra ni una regla
 * de estilo, y el SEO se mantiene identico.
 *
 * IMPORTANTE: esto es un componente de SERVIDOR y no recibe el HTML como
 * prop de ningun componente de cliente. Si lo fuera, el contenido viajaria
 * dos veces (una en el HTML y otra en la carga de hidratacion): en la home
 * eran 80 KB de mas. El comportamiento interactivo lo aporta LegacyEnhancer,
 * que no recibe props y busca los elementos en el DOM.
 */
export function LegacyContent({ html }: { html: string }) {
  return (
    <>
      <div data-legacy="" dangerouslySetInnerHTML={{ __html: html }} />
      <LegacyEnhancer />
    </>
  );
}
