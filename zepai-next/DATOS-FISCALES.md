# Datos fiscales pendientes

Cuando la sociedad esté constituida, hay que rellenar **tres datos en dos
ficheros**. Es el único punto de la web que queda incompleto por ley.

## Qué hace falta

| Dato | Ejemplo |
|---|---|
| Razón social | Zepai Agency, S.L. |
| NIF / CIF | B12345678 |
| Domicilio fiscal | Calle Ejemplo 1, 28001 Madrid |

## Dónde va

**1. `src/app/aviso-legal/page.tsx`** — apartado *«1. Datos del prestador del
servicio»*. Añadir tres elementos a la lista, antes del nombre comercial:

```html
<li><strong>Titular:</strong> RAZÓN SOCIAL</li>
<li><strong>NIF / CIF:</strong> NIF</li>
<li><strong>Domicilio:</strong> DOMICILIO</li>
```

Y borrar el párrafo que empieza por *«Zepai Agency se encuentra en proceso de
constitución»*.

**2. `src/app/politica-de-privacidad/page.tsx`** — apartado *«1. Quién trata
tus datos»*. Sustituir el párrafo entero por:

```html
<p>El responsable del tratamiento es <strong>RAZÓN SOCIAL</strong>, con NIF
<strong>NIF</strong> y domicilio en <strong>DOMICILIO</strong>, que opera bajo
el nombre comercial Zepai Agency.</p>
```

## Por qué no se dejaron corchetes

Un `[PENDIENTE]` en una página publicada se lee como un borrador sin
terminar, y esas dos páginas son justo las que un cliente mira para decidir
si la empresa es seria. Se publica lo que existe de verdad — nombre
comercial, correo, teléfono y web — y se dice en una línea que lo demás
llegará al constituirse. Es honesto y no obliga a inventar nada.

## Aviso

Mientras esto siga sin rellenar, el aviso legal **no cumple** el artículo 10
de la LSSI-CE, que exige nombre, NIF y domicilio del prestador. La web
funciona y no hay riesgo inmediato, pero es una infracción leve mientras
dure. Cuanto antes se cierre, mejor.

## De paso, cuando tengas el NIF

Con la sociedad constituida se pueden pedir dos cosas que hoy no puedes:

- **Perfil de Google Business.** Da reseñas verificables, estrellas en el
  buscador y presencia en Maps. Es la señal de confianza más barata que hay.
- **Meta Tech Provider.** Pide datos de empresa, y es la certificación que
  mejor encaja con lo que vendes.
