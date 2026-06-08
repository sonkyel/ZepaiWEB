# Zepai Agency — Contexto del Proyecto (Landing Page)

> Documento de contexto para continuar el trabajo en otra herramienta/IDE (p.ej. Antigravity).
> Archivo principal: `index.html` (sitio estático de una sola página, sin build, sin dependencias npm).
> Carpeta del proyecto: `C:\Users\Sonkyel\Desktop\Creación de página ia ZEPAI\`
> Carpeta lista para deploy (GitHub/Vercel): `C:\Users\Sonkyel\Desktop\zepai-landing\`

---

## 1. Qué es esto

Landing page de **Zepai Agency** (agencia de IA / automatización para negocios). Es un **único archivo HTML** (`index.html`, ~3900 líneas) con:
- CSS embebido (tema "glassmorphism" morado/índigo sobre fondo claro)
- JS embebido (sin frameworks)
- Tres escenas 3D hechas con **Three.js** (CDN `three@0.160.0`)
- Gráficas con **Chart.js** (CDN)
- Notificaciones por correo con **EmailJS** (CDN)
- Soporte bilingüe ES/EN vía atributos `data-es` / `data-en` + clase `.i18n`
- Logo: `logo.png` (letras blancas sobre fondo transparente)

No requiere build ni `package.json`. Para probar localmente se sirvió con:
```
python -m http.server 8000
```
(porque EmailJS rechaza peticiones desde `file://`, necesita un origen `http://`/`https://` real).

---

## 2. Trabajo realizado en esta sesión (cronológico)

### 2.1 Animaciones de scroll-reveal ("stagger con blur")
- Clase `.reveal` (línea ~76-78): cambiada de fade+slide simple a **blur + fade + slide** con `cubic-bezier(.16,1,.3,1)`.
- Ajustado `prefers-reduced-motion` para incluir `filter:none!important`.
- Corregidas clases de retraso escalonado (`rd1`/`rd2`/`rd3`) en pasos de "cómo funciona" y tarjetas de gráficas para que el stagger sea correcto.

### 2.2 Mejora de las 3 escenas 3D (Three.js)
Aplicado un mismo "kit" de mejoras premium a las tres escenas activas:

1. **`#avatarCanvas`** (`initAvatarScene`, ~línea 2996) — robot del hero
2. **`#robotCanvas`** (`initRobot3D`, ~línea 3470) — fondo del hero con planeta
3. **`#endCanvas`** (`initEndScene3D`, ~línea 3271) — escena de cierre orbital

Mejoras aplicadas:
- **Helper compartido `makeGlowSprite(hexColor, worldSize)`** (~línea 2975): genera un `Sprite` con textura de gradiente radial en canvas + `AdditiveBlending` — técnica de "bloom falso" sin coste de post-procesado (`EffectComposer` deliberadamente evitado por rendimiento).
- **Niebla atmosférica** (`THREE.FogExp2`) añadida a las 3 escenas para dar profundidad consistente.
- **Shader de "núcleo de energía"** con ruido `fbm` (fractal Brownian motion) en la esfera central de `endCanvas` (antes era un material plano).
- **Shader de "planeta gigante gaseoso"** (`planetMat`, ~línea 3580) con bandas animadas fbm de 3 octavas, sustituyendo el material plano anterior.
- **Anillo del planeta**: de `TorusGeometry` de color plano a `RingGeometry` + textura de gradiente en canvas con remapeo radial de UVs.
- Glow sprites añadidos en: ojos/antena/LEDs del avatar, satélites de la escena final, luna del planeta (`moonGlow`).
- **Drone compañero** (`droneGroup`, ~línea 3122 dentro de `initAvatarScene`): grupo con icosaedro emissive + shell wireframe + anillo + glow sprite + luz puntual, flotando al lado derecho del robot del hero — agregado porque el usuario sintió que "el lado derecho del robot estaba muy vacío".

### 2.3 Corrección de rendimiento ("se ralentiza al hacer scroll")
El usuario reportó jank/lag al scrollear, causado por las mejoras 3D nuevas (más sprites/shaders/luces corriendo cada frame). Solución — **patrón de throttling cada 2 frames**:
- `initAvatarScene`: contador `avFrame`, actualizaciones de sprites/partículas envueltas en `if(avFrame%2===0){...}`
- `initEndScene3D`: shader del orbe simplificado (5→3 octavas, 64→48 segmentos de esfera), removida una luz extra (`rimPt`)
- `initRobot3D`: contador `rbFrame`, mismo patrón — y se aseguró de **mantener `planetMat.uniforms.uTime.value = t` fuera del throttle** (la animación del shader debe ser fluida) mientras que las opacidades de glow sí se throttlean.

> **Patrón a seguir si se agregan más efectos 3D**: cualquier actualización de opacidad/intensidad de sprites o luces debe ir dentro de `if(frameCounter%2===0){...}`. Las actualizaciones de uniforms de shaders (`uTime`) NO deben throttlearse (se ven entrecortadas).

### 2.4 Fix: barras de comparación invisibles
`#barChart` (Chart.js, ~línea 2650): el dataset "Antes de Zepai" usaba `rgba(255,255,255,0.12)` (blanco) sobre fondo de tarjeta blanco → invisible. Cambiado a tono slate oscuro: `rgba(15,23,42,0.10)` relleno / `rgba(15,23,42,0.35)` borde.

### 2.5 Política de Privacidad y Seguridad
Agregada para cumplir con buenas prácticas para quienes agendan llamadas o envían correos:
- **Modal** `#privacyOverlay` / `.privacy-modal` (antes de `<footer>`) — 7 secciones bilingües: qué se recopila, cómo se usa, cómo se protege, terceros, retención, derechos del usuario, contacto.
- **Notas de consentimiento** (`.consent-note`) bajo ambos formularios de contacto, con link clicable que abre el modal.
- **Link en el footer**: "Política de Privacidad" en la columna "Empresa".
- **Funciones JS**: `openPrivacyModal(e)` / `closePrivacyModal()` — soporta click en backdrop y tecla Escape, bloquea scroll del body mientras está abierto.

### 2.6 Sistema de notificación por correo (EmailJS)
El sistema anterior solo generaba un link `mailto:` (dependía de que el visitante tuviera cliente de correo configurado — poco confiable). Se reemplazó por **EmailJS**, que envía el correo directo al dueño sin depender del navegador del visitante.

**Configuración actual (ya activa y funcionando)** — constantes en `index.html` ~línea 2790:
```js
const EMAILJS_PUBLIC_KEY  = 'GGgDb2RkPqUEnDFgt';
const EMAILJS_SERVICE_ID  = 'service_8z5p2cv';
const EMAILJS_TEMPLATE_ID = 'template_e96cb38';
```
- SDK cargado vía CDN: `<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>` (línea 17)
- Función compartida `sendNotification(...)`: usa EmailJS si `EMAILJS_READY` es `true`; si no, recurre automáticamente a `mailto:` como respaldo.
- **Toast de confirmación** (`#formToast` / `.form-toast`): aparece tras enviar, muestra éxito (✅) o error (⚠️), se autocierra a los 7s.
- Variables enviadas a la plantilla (cubren varios nombres comunes para máxima compatibilidad con Auto-Reply): `to_email`, `subject`, `message`, `from_name`, `name`, `reply_to`, `email`, `user_email`, `from_email`.
- Log de error detallado en consola: `console.error('[EmailJS] send failed — status:', err.status, '| text:', err.text, ...)`.

**Problemas resueltos durante la integración** (por si reaparecen):
1. *"The recipients address is empty"* (422) → faltaba `to_email` en los parámetros Y configurar el campo **"To Email"** del template en el dashboard de EmailJS como `{{to_email}}`.
2. *"Gmail_API: Request had insufficient authentication scopes"* (412) → la conexión OAuth de Gmail en EmailJS no tenía el permiso "enviar correo en su nombre". Se resolvió reconectando el servicio de Gmail y aceptando todos los permisos solicitados (nuevo Service ID: `service_8z5p2cv`).
3. **Auto-Reply al visitante no llegaba** → causa probable: la plantilla de auto-respuesta espera el correo del visitante bajo un nombre de variable distinto al que se enviaba. Se agregaron alias múltiples (`email`, `user_email`, `from_email`, `reply_to`) para cubrir cualquier configuración. **Pendiente de confirmar si ya llega** — revisar en el dashboard de EmailJS → "Email History" si el auto-reply sale como enviado, y que el campo "To Email" del auto-reply use una de esas variables.

### 2.7 Fix: hora seleccionada invisible (selector de horario de llamada)
Mismo patrón de bug que ya se había corregido para el selector de fechas: `.time-btn{background:rgba(139,92,246,.06)!important}` (lavado morado casi transparente, con `!important`) le ganaba al fondo degradado de `.time-btn.active{background:var(--grad)}` (sin `!important`) → texto blanco sobre fondo casi blanco, invisible.

**Fix** (~línea 1230, junto al fix análogo de `.date-btn.active`):
```css
.time-btn.active{
  background:linear-gradient(135deg,#8B5CF6,#4F46E5)!important;
  border-color:transparent!important;
  box-shadow:0 4px 14px rgba(139,92,246,.4)!important;
  color:#ffffff!important;
  -webkit-text-fill-color:#ffffff!important;
}
```
> **Lección para futuros bugs de "texto/elemento invisible"**: revisar siempre si hay un `!important` en el estado base (`.btn`) que esté ganándole a una declaración sin `!important` en el estado activo (`.btn.active`) — los `!important` siempre ganan sobre no-`!important`, sin importar la especificidad.

### 2.8 Fix: letras blancas del logo de splash invisibles
`.logo-splash` (línea 927) usaba `mix-blend-mode:screen` — diseñado para logos blancos sobre fondos **oscuros** (como el nav, que es `#0A0A14`). Pero el fondo del splash es `#F5F4FF` (casi blanco) → blanco sobre casi-blanco con "screen" = invisible.

**Fix**: se reemplazó por el mismo filtro de corrección de color que ya usaba `.logo-footer` (que también está sobre fondo claro):
```css
.logo-splash{height:70px;width:auto;display:block;filter:invert(1) hue-rotate(240deg) saturate(0.9) brightness(0.38)}
```
Esto convierte las letras blancas en un tono morado oscuro, visible sobre el fondo claro.

> **Nota**: `.logo-nav` (línea 926) SÍ debe seguir usando `mix-blend-mode:screen`, porque el nav tiene fondo oscuro permanente (`#0A0A14`, ver línea 1067 `/* NAV OSCURA PERMANENTE */`).

### 2.9 Carpeta de despliegue (GitHub → Vercel)
Creada en `C:\Users\Sonkyel\Desktop\zepai-landing\` con SOLO lo necesario:
- `index.html` + `logo.png` (copias sincronizadas del proyecto principal)
- `vercel.json` — cabeceras de cache (`logo.png`: 1 año inmutable; `index.html`: siempre revalida)
- `.gitignore` — ignora `.vercel`, `.DS_Store`, `Thumbs.db`
- `README.md` — instrucciones de `git init`/push y de importar en Vercel

Se agregó también `<link rel="icon" type="image/png" href="logo.png">` (línea 7) — el sitio no tenía favicon.

> **Nota importante**: cuando se editó `index.html` después de crear esta carpeta (fix del logo splash), se sincronizó manualmente con `cp`. **Si sigues editando `index.html` en el proyecto principal, recuerda copiar los cambios a `zepai-landing/index.html` antes de hacer commit/push**, o mejor aún, trabaja directamente sobre la copia de `zepai-landing/` y descarta la carpeta original para evitar desincronización.

---

## 3. Pendientes / siguientes pasos sugeridos

1. **Confirmar que el Auto-Reply de EmailJS ya llega al visitante** (sección 2.6, punto 3) — si sigue sin llegar, revisar en el dashboard qué variable usa el campo "To Email" de la plantilla de auto-respuesta y ajustar el nombre en el JS si hace falta.
2. **Decidir si se inicializa el repo Git** en `zepai-landing/` y se sube a GitHub (se ofreció pero no se ha hecho).
3. **Revisar "Allowed origins" en EmailJS** una vez el sitio tenga su dominio final de Vercel — por defecto EmailJS puede tener restricciones de origen que bloqueen el dominio nuevo (mismo problema que causó errores al probar desde `file://`).
4. Mantener sincronizadas las dos copias de `index.html` (proyecto principal vs. carpeta de deploy) o consolidar en una sola ubicación.

---

## 4. Datos de contacto / cuentas usadas

- Correo de notificaciones: `zecuenin@gmail.com`
- EmailJS — Public Key: `GGgDb2RkPqUEnDFgt` · Service ID: `service_8z5p2cv` · Template ID: `template_e96cb38`

---

## 5. Convenciones del proyecto (para mantener consistencia)

- **i18n**: todo texto visible debe ir en `<span class="i18n" data-es="..." data-en="...">texto en español</span>` — el JS usa `el.textContent = txt`, así que **no se puede meter HTML dentro de los atributos `data-es`/`data-en`** (links, negritas, etc. deben ir como elementos hermanos fuera del span).
- **Colores de marca**: morado `#8B5CF6`, índigo `#4F46E5`, gradiente `var(--grad)` = `linear-gradient(135deg,#8B5CF6 0%,#4F46E5 100%)`.
- **Texto sobre fondo claro**: usar tonos oscuros tipo `rgba(10,10,20,.65)` / `#0A0A14` (la sección "LIGHT MODE TEXT FIXES" ~línea 844 centraliza muchos de estos ajustes).
- **Glow/bloom**: usar `makeGlowSprite()` en vez de post-procesado pesado — más barato en rendimiento, especialmente importante porque las escenas 3D corren simultáneamente con scroll/animaciones.
- **Throttling de animaciones 3D**: cualquier actualización de opacidad/intensidad debe ir cada 2 frames (`if(frameCounter%2===0)`) para evitar jank en scroll — los uniforms de shaders (`uTime`) no se throttlean.
