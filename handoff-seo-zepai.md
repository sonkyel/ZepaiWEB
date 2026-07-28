# Handoff SEO — ZEPAI Agency (para Patrick)

> **Para el Claude de Patrick:** este documento es un encargo de trabajo. Patrick tiene los accesos (Google Search Console, Perfil de Negocio de Google, hosting/dominio). Jordan no los tiene. Tu trabajo es ayudar a Patrick a ejecutar el checklist SEO de abajo, pedirle solo lo que necesites y dejar cada punto hecho o con su guía paso a paso. Trabaja "de la mano" — Patrick no es técnico.

---

## Contexto

- **Web:** https://zepaiagency.com (también responde `www.zepaiagency.com`)
- **Qué es:** agencia de IA — agentes IA, marketing digital, clipping, tráfico en redes y diseño web. Industrias: restaurantes, inmobiliarias, e-commerce, blockchain/Web3. Servicio para toda Latinoamérica.
- **Estructura actual:** la web es **one-page** (una sola URL). Lo que parecen secciones (Servicios, Industrias, Contacto) son anclas dentro de la misma página, no páginas separadas.
- **Tecnología:** es una **SPA** (carga con "Cargando experiencia…" y renderiza todo por JavaScript). Esto es importante para la indexación (ver punto 1).
- **Contacto del negocio:** info@zepaiagency.com

El origen de este encargo es un reel de Instagram con un checklist de SEO local ("¿estás haciendo esto para que Google te encuentre?"). Abajo está cada punto + el estado verificado desde la web.

---

## Checklist de trabajo

### 1. Google Search Console — ¿Google encuentra las páginas?
**Estado:** no verificado (requiere acceso de Patrick).

Pasos:
1. Entrar a https://search.google.com/search-console
2. Añadir la propiedad `zepaiagency.com` y verificar (por DNS o etiqueta HTML).
3. Revisar **Páginas → Indexadas**. Confirmar que `zepaiagency.com` aparece indexada.
4. Usar **Inspección de URL** sobre la home y pulsar "Solicitar indexación".

⚠️ **Riesgo crítico a comprobar:** como la web es una SPA (todo por JavaScript), Google puede **no renderizar el contenido** y dejarla mal indexada. En la Inspección de URL, usar "Ver página renderizada" / "Probar URL publicada" y confirmar que Google ve el texto real (servicios, industrias, testimonios). Si ve la página casi vacía → hay que añadir prerender / SSR o meta-contenido estático. **Este es el punto más importante.**

### 2. Perfil de Negocio de Google (Google Business Profile) — fotos y reviews
**Estado:** no verificado (requiere acceso de Patrick).

Pasos:
1. Buscar "Zepai Agency" en Google Maps. ¿Existe el perfil?
   - **Si no existe:** crearlo en https://business.google.com
   - **Si existe:** completarlo al 100%.
2. Subir: logo, fotos del trabajo / capturas de los agentes IA, categoría correcta ("Agencia de marketing" o "Servicio de software").
3. Conseguir **reviews**: pedir reseñas a los clientes reales (los testimonios de la web: Carlos Mendoza – El Rincón Gourmet, María González – Horizonte Plus, Andrés Vargas – Roast & Co, Laura Jiménez – TiendaFit.co).
4. Nota: ZEPAI es agencia remota (no local físico). El perfil ayuda menos que para un negocio con local, pero suma autoridad y reviews.

### 3. Nombre de servicio + negocio en cada título de página
**Estado:** ✅ cumple parcialmente — verificado desde la web.

- Título actual: **"Zepai Agency — Agentes IA para tu Negocio"** → tiene negocio + servicio. Correcto.
- **Limitación:** al ser one-page solo hay **un título para todo**. El reel dice "en *cada* página" y ZEPAI no tiene varias.
- **Oportunidad (recomendado):** crear páginas separadas por servicio/industria, cada una con su propio título optimizado. Ejemplos:
  - `/agentes-ia-restaurantes` → *"Agente IA para Restaurantes | Zepai Agency"*
  - `/agentes-ia-inmobiliarias` → *"Agente IA para Inmobiliarias | Zepai Agency"*
  - `/diseno-web` → *"Diseño Web para Negocios | Zepai Agency"*
- Esto multiplica las búsquedas por las que la web puede aparecer en Google.

### 4. (Pendiente — el reel se cortó)
La transcripción del reel quedó incompleta en *"Ahora, ¿continúas…"*. Falta capturar el último punto. Cuando Jordan lo tenga, se añade aquí.

> Checklist típico de SEO local — probables puntos que seguían en el reel (revisar y aplicar si aplican):
> - ¿Tienes la web enlazada desde tu Perfil de Negocio de Google?
> - ¿Pides reviews de forma activa y respondes a todas?
> - ¿Tienes NAP consistente (Nombre, Dirección, Teléfono) en todos lados?
> - ¿Tu web carga rápido en móvil?
> - ¿Tienes contenido/blog con palabras clave que busca tu cliente?

---

## Hallazgo extra (no es del reel, pero hay que arreglarlo)

En la sección **"Resultados Reales"** de la web, los contadores muestran:
- **"0+ Proyectos completados"**
- **"0% Satisfacción de clientes"**

Están en cero (animación que no carga o dato sin rellenar). **Choca con los testimonios** que dicen +65% ventas y 420% ROI. Da mala imagen. Hay que poner números reales o quitar los contadores.

---

## Resumen para Patrick (lo accionable ya)

1. **Search Console** → verificar dominio + confirmar que Google ve el contenido real (riesgo SPA). *Lo más urgente.*
2. **Perfil de Negocio de Google** → crear/completar + conseguir reviews de los clientes.
3. **Títulos / páginas** → la home está OK; valorar crear páginas por servicio.
4. **Arreglar contadores en 0** de la sección Resultados.

*Preparado por el asistente de Jordan · ZEPAI Agency.*
