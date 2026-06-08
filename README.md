# Zepai Agency — Landing Page

Sitio estático de una sola página (`index.html` + `logo.png`). No requiere build ni dependencias — usa CDNs para Three.js, Chart.js y EmailJS.

## Subir a GitHub

```bash
git init
git add .
git commit -m "Zepai Agency landing page"
git branch -M main
git remote add origin https://github.com/<tu-usuario>/<tu-repo>.git
git push -u origin main
```

## Desplegar en Vercel

1. Entra a [vercel.com](https://vercel.com) → **Add New Project** → importa el repositorio de GitHub.
2. Vercel detecta automáticamente que es un sitio estático ("Other" / sin framework) — no hace falta configurar build command ni output directory.
3. Click en **Deploy**.

`vercel.json` ya incluye cabeceras de cache para `logo.png` (1 año, inmutable) y `index.html` (siempre revalida, para que tus cambios se reflejen al instante).

## Notas

- El formulario de contacto/agendamiento envía notificaciones por correo vía **EmailJS** (claves configuradas directamente en `index.html`).
- Si cambias de dominio, recuerda revisar en tu cuenta de EmailJS que no haya restricciones de "Allowed origins" que bloqueen el dominio nuevo.
