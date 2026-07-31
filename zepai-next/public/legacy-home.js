/* Contenido interactivo de la home: FAQ, modal de privacidad, contadores,
   agenda de llamadas y envio de formularios (EmailJS).
   El idioma, el nav, el menu movil y el scroll-reveal los gestiona React. */

/* Espejo del idioma que guarda el contexto de React, para los textos que
   este fichero genera en tiempo de ejecucion (fechas, horas, avisos). */
var currentLang = (function () {
  try { return localStorage.getItem('zepai-lang') || 'es'; } catch (e) { return 'es'; }
})();
window.addEventListener('storage', function (e) {
  if (e.key === 'zepai-lang' && e.newValue) currentLang = e.newValue;
});

/* ── SCROLL TO SECTION ── */
function scrollToSection(id) {
  const el = document.getElementById(id);
  if (!el) return;
  const offset = el.getBoundingClientRect().top + window.pageYOffset - 80;
  window.scrollTo({ top: offset, behavior: 'smooth' });
}

/* El tilt 3D se retiro con el rediseno sobrio: pintaba un degradado y una
   sombra violetas al mover el raton, y solo lo llevaba una de las tres
   tarjetas de cifras. */

/* ── FAQ ACCORDION ── */
function toggleFaq(qEl) {
  const item = qEl.closest('.faq-item');
  const isOpen = item.classList.contains('open');
  document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
  if (!isOpen) item.classList.add('open');
}

/* ── PRIVACY POLICY MODAL ── */
function openPrivacyModal(e) {
  if (e) e.preventDefault();
  const ov = document.getElementById('privacyOverlay');
  if (!ov) return;
  ov.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closePrivacyModal() {
  const ov = document.getElementById('privacyOverlay');
  if (!ov) return;
  ov.classList.remove('open');
  document.body.style.overflow = '';
}
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closePrivacyModal();
});

/* ── COUNTER ANIMATION ── */
function animateCounter(el) {
  const target = parseInt(el.dataset.target || 0);
  const suffix = el.dataset.suffix || '';
  if (!target) return;
  const duration = 1800;
  const step = target / (duration / 16);
  let current = 0;
  const timer = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = Math.round(current) + suffix;
    if (current >= target) clearInterval(timer);
  }, 16);
}

const counterObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.querySelectorAll('.stat-num[data-target]').forEach(animateCounter);
      counterObs.unobserve(e.target);
    }
  });
}, { threshold: 0.3 });
const statsEl = document.querySelector('.stats-grid');
if (statsEl) counterObs.observe(statsEl);

/* ══ NOTIFICACIONES POR CORREO (EmailJS) ══════════════════════════════
   Configurado: cada llamada agendada o cotización se envía directo a tu
   correo vía EmailJS, con respaldo automático a mailto: si algo falla. */
const EMAILJS_PUBLIC_KEY  = 'GGgDb2RkPqUEnDFgt';
const EMAILJS_SERVICE_ID  = 'service_jyombda';
const EMAILJS_TEMPLATE_ID = 'template_e96cb38';
const EMAILJS_READY = (typeof emailjs !== 'undefined') &&
  EMAILJS_PUBLIC_KEY !== 'TU_PUBLIC_KEY' && EMAILJS_SERVICE_ID !== 'TU_SERVICE_ID' && EMAILJS_TEMPLATE_ID !== 'TU_TEMPLATE_ID';
if (EMAILJS_READY) emailjs.init({ publicKey: EMAILJS_PUBLIC_KEY });

function showToast(ok, title, msg) {
  const t = document.getElementById('formToast');
  if (!t) return;
  t.classList.toggle('error', !ok);
  document.getElementById('ftIco').textContent = ok ? '✅' : '⚠️';
  document.getElementById('ftTitle').textContent = title;
  document.getElementById('ftMsg').textContent = msg;
  t.classList.add('show');
  clearTimeout(t._hideTimer);
  t._hideTimer = setTimeout(() => t.classList.remove('show'), 7000);
}

/* Envía la notificación: usa EmailJS si está configurado (llega directo a tu correo,
   sin depender del cliente de correo del visitante); si no, recurre a mailto: */
function sendNotification(subject, body, formEl, btnEl, mailtoFallback, okMsg, isEs) {
  if (EMAILJS_READY) {
    const original = btnEl.innerHTML;
    btnEl.disabled = true;
    btnEl.style.opacity = '.6';
    const visitorEmail = formEl.querySelector('input[type="email"]')?.value || '';
    const visitorName  = formEl.querySelector('input[type="text"]')?.value || '';
    emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, {
      to_email: 'info@zepaiagency.com',
      subject: subject,
      message: body,
      from_name: visitorName,
      name: visitorName,
      reply_to: visitorEmail,
      email: visitorEmail,
      user_email: visitorEmail,
      from_email: visitorEmail
    }).then(() => {
      showToast(true, isEs ? '¡Listo, lo recibimos!' : 'Got it, all set!', okMsg);
      formEl.reset();
    }).catch((err) => {
      console.error('[EmailJS] send failed — status:', err && err.status, '| text:', err && err.text, '| raw:', err);
      showToast(false, isEs ? 'No se pudo enviar' : 'Could not send',
        isEs ? 'Intenta de nuevo o escríbenos directo a info@zepaiagency.com.' : 'Please try again or email us at info@zepaiagency.com.');
    }).finally(() => {
      btnEl.disabled = false;
      btnEl.style.opacity = '';
      btnEl.innerHTML = original;
    });
  } else {
    showToast(true, isEs ? 'Abriendo tu correo…' : 'Opening your email…',
      isEs ? 'Confirma el envío desde tu app de correo para que nos llegue.' : 'Please send it from your email app so it reaches us.');
    window.location.href = mailtoFallback;
  }
}

/* ── SCHEDULE SUBMIT ── */
function handleScheduleSubmit(e) {
  e.preventDefault();
  const name  = document.getElementById('sname').value;
  const email = document.getElementById('semail').value;
  const phone = document.getElementById('sphone').value;
  const biz   = document.getElementById('sbiz').value;
  const date  = document.getElementById('sdate').value;
  const time  = document.getElementById('stime').value;
  const goal  = document.getElementById('sgoal').value;
  const isEs  = currentLang === 'es';
  const subject = `📞 Solicitud de Llamada — ${name}${biz ? ' — '+biz : ''}`;
  const body = [
    `SOLICITUD DE LLAMADA — ZEPAI AGENCY`,
    ``,
    `Nombre: ${name}`,
    `Email: ${email}`,
    `Teléfono / WhatsApp: ${phone || 'No indicado'}`,
    `Tipo de negocio: ${biz || 'No indicado'}`,
    `Fecha preferida: ${date || 'Flexible'}`,
    `Horario preferido: ${time || 'Flexible'}`,
    ``,
    `¿Qué quiere lograr?`,
    goal || 'Sin comentarios adicionales.',
  ].join('\n');
  const mailtoFallback = 'mailto:info@zepaiagency.com?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);
  sendNotification(subject, body, e.target, e.target.querySelector('button[type="submit"]'), mailtoFallback,
    isEs ? 'Te confirmaremos tu llamada en menos de 24 horas.' : "We'll confirm your call within 24 hours.", isEs);
}

/* ── FORM SUBMIT ── */
function handleSubmit(e) {
  e.preventDefault();
  const name    = document.getElementById('fname').value;
  const company = document.getElementById('fcompany').value;
  const email   = document.getElementById('femail').value;
  const biz     = document.getElementById('fbiz').value;
  const service = document.getElementById('fservice').value;
  const msg     = document.getElementById('fmsg').value;
  const isEs    = currentLang === 'es';
  const subject = `Cotización Zepai Agency${company ? ' — ' + company : ''}`;
  const body    = [
    `Nombre: ${name}`,
    `Empresa: ${company || 'N/A'}`,
    `Email: ${email}`,
    `Tipo de negocio: ${biz || 'N/A'}`,
    `Servicio: ${service || 'N/A'}`,
    '',
    `Mensaje:`,
    msg
  ].join('\n');
  const mailtoFallback = 'mailto:info@zepaiagency.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  sendNotification(subject, body, e.target, e.target.querySelector('button[type="submit"]'), mailtoFallback,
    isEs ? 'Responderemos tu solicitud en menos de 24 horas.' : "We'll respond to your request within 24 hours.", isEs);
}

/* ── GLOBAL PERFORMANCE: pause all renderers when tab hidden or mobile ── */
const _isMobile = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
let _pagePaused = false;
document.addEventListener('visibilitychange', () => {
  _pagePaused = document.hidden;
});

/* Disable cursor effects on touch devices */
if(_isMobile || 'ontouchstart' in window) {
  /* Disable magnetic buttons on touch */
  document.querySelectorAll('.btn-p').forEach(b=>{
    b.onmousemove=null; b.onmouseleave=null;
  });
}

/* ── MAGNETIC BUTTONS ── */
document.querySelectorAll('.btn-p').forEach(btn=>{
  btn.addEventListener('mousemove', e=>{
    const r=btn.getBoundingClientRect();
    const x=(e.clientX-r.left-r.width/2)*0.24;
    const y=(e.clientY-r.top-r.height/2)*0.24;
    btn.style.transform=`translate(${x}px,${y}px) translateY(-2px)`;
  });
  btn.addEventListener('mouseleave',()=>btn.style.transform='');
  btn.addEventListener('click', e=>{
    const rpl=document.createElement('span');
    rpl.className='btn-ripple';
    const r=btn.getBoundingClientRect();
    rpl.style.left=(e.clientX-r.left)+'px';
    rpl.style.top =(e.clientY-r.top )+'px';
    btn.appendChild(rpl);
    setTimeout(()=>rpl.remove(),650);
  });
});

/* ── CONTACT TABS ── */
function setCtab(n) {
  document.querySelectorAll('.ctab-btn').forEach((b,i)=>b.classList.toggle('active',i===n));
  document.querySelectorAll('.ctab-content').forEach((c,i)=>{ c.style.display=i===n?'block':'none'; });
}

/* ── DATE PICKER (next 5 days) ── */
const DAYS_ES  = ['Dom','Lun','Mar','Mié','Jue','Vie','Sáb'];
const DAYS_EN  = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
const MONS_ES  = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];
const MONS_EN  = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

/* toISOString() da la fecha en UTC: en Espana, de madrugada, eso es el dia
   anterior, y el boton decia un dia y guardaba otro. */
function isoLocal(d) {
  return d.getFullYear() + '-' +
         String(d.getMonth() + 1).padStart(2, '0') + '-' +
         String(d.getDate()).padStart(2, '0');
}

function buildDatePicker() {
  const container = document.getElementById('datePicker');
  if (!container) return;
  const today = new Date();
  const isEn  = currentLang === 'en';
  container.innerHTML = '';
  for (let i = 0; i < 5; i++) {
    const d = new Date(today);
    d.setDate(today.getDate() + i);
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'date-btn' + (i===0?' active':'');
    const dayLabel = (isEn ? DAYS_EN : DAYS_ES)[d.getDay()];
    const monLabel = (isEn ? MONS_EN : MONS_ES)[d.getMonth()];
    btn.innerHTML = `<span class="date-day">${dayLabel}</span><span class="date-num">${d.getDate()}</span><span class="date-month">${monLabel}</span>`;
    const iso = isoLocal(d);
    btn.dataset.iso = iso;
    btn.onclick = () => selectDate(iso, btn);
    container.appendChild(btn);
  }
  // Pre-select today and build slots
  const iso0 = isoLocal(today);
  document.getElementById('sdate').value = iso0;
  buildTimeSlots(iso0);
}

/* ── TIME SLOTS with random availability ── */
const ALL_SLOTS_ES = ['9:00 AM','10:00 AM','11:00 AM','12:00 PM','2:00 PM','3:00 PM','4:00 PM','5:00 PM'];
const ALL_SLOTS_EN = ['9:00 AM','10:00 AM','11:00 AM','12:00 PM','2:00 PM','3:00 PM','4:00 PM','5:00 PM'];

function buildTimeSlots(dateStr) {
  const container = document.getElementById('timeSlots');
  if (!container) return;
  /* Antes un tercio de las horas salia como "Ocupado" segun un numero
     pseudoaleatorio. No hay agenda detras que consultar: era escasez
     inventada. Se ofrecen todas y el horario se confirma por correo, que es
     lo que ya promete el propio formulario. */
  container.innerHTML = '';
  ALL_SLOTS_ES.forEach(slot => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'time-btn';
    btn.textContent = slot;
    btn.onclick = () => selectTime(slot, btn);
    container.appendChild(btn);
  });
}

function selectDate(iso, btn) {
  document.getElementById('sdate').value = iso;
  document.querySelectorAll('.date-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('stime').value = '';
  document.querySelectorAll('.time-btn.active').forEach(b => b.classList.remove('active'));
  buildTimeSlots(iso);
}

function selectTime(slot, btn) {
  document.getElementById('stime').value = slot;
  document.querySelectorAll('.time-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

/* El selector no lo construia nadie: la web antigua lo lanzaba con un
   DOMContentLoaded que se perdio al portar a Next, asi que los contenedores
   quedaban vacios y no habia fechas ni horas que pulsar.

   No vale con repetir aquel DOMContentLoaded: este fichero se carga despues
   de montar la pagina, asi que ese evento ya ha pasado y el manejador no se
   ejecutaria nunca. */
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', buildDatePicker);
} else {
  buildDatePicker();
}
