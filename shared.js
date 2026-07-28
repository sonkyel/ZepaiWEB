/* ── SHARED JS ──────────────────────────────────────────────
   Usado por las páginas secundarias (servicios / industrias / blog).
   Contiene solo lo imprescindible: toggle de idioma, nav, menú móvil
   y scroll-reveal. La home tiene su propia copia embebida junto al
   resto de su JS (Three.js, Chart.js, EmailJS).
   ───────────────────────────────────────────────────────── */

/* ── LANGUAGE TOGGLE ── */
let currentLang = localStorage.getItem('zepai-lang') || 'es';

function setLang(lang) {
  currentLang = lang;
  document.querySelectorAll('.i18n').forEach(el => {
    const txt = el.dataset[lang];
    if (txt !== undefined) el.textContent = txt;
  });
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
  });
  document.documentElement.lang = lang;
  localStorage.setItem('zepai-lang', lang);
}

/* ── NAV SCROLL ── */
const mainNav = document.getElementById('mainNav');
if (mainNav) {
  window.addEventListener('scroll', () => {
    mainNav.classList.toggle('scrolled', window.scrollY > 20);
  });
}

/* ── MOBILE MENU ── */
function toggleMenu() {
  const menu = document.getElementById('mobileMenu');
  const ham = document.getElementById('ham');
  if (!menu || !ham) return;
  menu.classList.toggle('open');
  ham.classList.toggle('open');
}
function closeMenu() {
  const menu = document.getElementById('mobileMenu');
  const ham = document.getElementById('ham');
  if (menu) menu.classList.remove('open');
  if (ham) ham.classList.remove('open');
}

/* ── SCROLL REVEAL ── */
const revObs = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('v'); revObs.unobserve(e.target); } });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => revObs.observe(el));

/* Aplicar idioma guardado */
if (currentLang !== 'es') setLang(currentLang);
