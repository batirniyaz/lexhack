"""JavaScript run inside scanned pages. Kept here so crawler.py stays readable."""

# Injected before any page script runs: records permission requests a visitor would be asked for.
HOOKS_JS = r"""
(() => {
  if (window.__qalqon) return;
  const q = window.__qalqon = { permissions: [] };
  const note = (item) => { try { if (q.permissions.length < 100) q.permissions.push(Object.assign({ t: Date.now() }, item)); } catch (e) {} };
  try {
    const md = navigator.mediaDevices;
    if (md && md.getUserMedia) {
      const orig = md.getUserMedia.bind(md);
      md.getUserMedia = (c) => { note({ api: 'camera_or_microphone', video: !!(c && c.video), audio: !!(c && c.audio) }); return orig(c); };
    }
  } catch (e) {}
  try {
    const geo = navigator.geolocation;
    if (geo) {
      const g1 = geo.getCurrentPosition.bind(geo), g2 = geo.watchPosition.bind(geo);
      geo.getCurrentPosition = (...a) => { note({ api: 'geolocation' }); return g1(...a); };
      geo.watchPosition = (...a) => { note({ api: 'geolocation' }); return g2(...a); };
    }
  } catch (e) {}
})();
"""

# One call per page: title, storage keys, permission log, forms, legal-document links, interesting inline scripts.
PAGE_JS = r"""
() => {
  const clean = (s) => (s || '').replace(/\s+/g, ' ').trim();
  const textOf = (el) => clean(el && (el.innerText || el.textContent));
  const keys = (s) => { try { return Object.keys(s); } catch (e) { return []; } };
  const LEGAL = /(maxfiylik|konfiden|конфиденц|privacy|politika|политик|policy|siyosat|oferta|оферт|offer|shartlar|условия|terms|agreement|соглашени|shaxsiy ma.lumot|персональн|personal data|cookie)/i;
  const CONSENT = /(rozilik|roziman|rozi |согласи|соглаша|consent|agree|maxfiylik|politika|политик|персональн|shaxsiy ma.lumot|personal data)/i;

  const labelFor = (el) => {
    let t = '';
    if (el.labels && el.labels.length) t = Array.from(el.labels).map(textOf).join(' ');
    if (!t) t = el.getAttribute('aria-label') || '';
    if (!t) {
      const ids = (el.getAttribute('aria-labelledby') || '').split(/\s+/).filter(Boolean);
      t = ids.map((id) => textOf(document.getElementById(id))).join(' ');
    }
    if (!t) { const p = el.closest('label'); if (p) t = textOf(p); }
    if (!t && el.parentElement) t = textOf(el.parentElement).slice(0, 80);
    return clean(t).slice(0, 120);
  };
  const containerOf = (el) => {
    if (el.form) return el.form;
    let n = el.parentElement;
    for (let i = 0; n && i < 8; i++, n = n.parentElement) {
      if (n.querySelector('button, [type=submit], [role=button]')) return n;
    }
    return document.body;
  };

  const SKIP = new Set(['hidden', 'submit', 'button', 'image', 'reset']);
  const groups = new Map();
  for (const el of document.querySelectorAll('input, select, textarea')) {
    const type = (el.type || el.tagName).toLowerCase();
    if (SKIP.has(type)) continue;
    const c = containerOf(el);
    if (!groups.has(c)) groups.set(c, []);
    groups.get(c).push(el);
  }

  const forms = [];
  for (const [c, els] of groups) {
    if (forms.length >= 30) break;
    const isForm = c.tagName === 'FORM';
    const fields = els.slice(0, 40).map((el) => ({
      tag: el.tagName.toLowerCase(),
      type: (el.type || '').toLowerCase(),
      name: el.getAttribute('name') || '',
      id: el.id || '',
      placeholder: el.getAttribute('placeholder') || '',
      label: labelFor(el),
      autocomplete: el.getAttribute('autocomplete') || '',
      pattern: el.getAttribute('pattern') || '',
      maxlength: el.maxLength > 0 ? el.maxLength : null,
      inputmode: el.getAttribute('inputmode') || '',
      accept: el.getAttribute('accept') || '',
      capture: el.getAttribute('capture'),
      required: !!el.required,
      visible: !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length),
    }));
    const checkboxes = els.filter((el) => (el.type || '').toLowerCase() === 'checkbox')
      .map((el) => ({ label: labelFor(el), checked: !!el.checked, required: !!el.required }));
    const containerText = textOf(c).slice(0, 1500);
    const consentCheckbox = checkboxes.find((cb) => CONSENT.test(cb.label)) || null;
    const consentSentence = (containerText.match(/[^.!?]*(rozilik|roziman|согласи|соглаша|consent|agree)[^.!?]*[.!?]?/i) || [null])[0];
    forms.push({
      is_form_element: isForm,
      action: isForm && c.getAttribute('action') ? c.action : null,
      method: isForm ? (c.getAttribute('method') || 'get').toLowerCase() : null,
      fields,
      checkboxes,
      consent: {
        checkbox: consentCheckbox,
        sentence: consentSentence ? clean(consentSentence).slice(0, 300) : null,
        policy_links: Array.from(c.querySelectorAll('a[href]')).filter((a) => LEGAL.test(a.href + ' ' + textOf(a)))
          .slice(0, 5).map((a) => ({ href: a.href, text: textOf(a).slice(0, 80) })),
      },
      buttons: Array.from(c.querySelectorAll('button, [type=submit]')).slice(0, 5).map((b) => textOf(b).slice(0, 40) || b.value || ''),
    });
  }

  const legalLinks = Array.from(document.querySelectorAll('a[href]'))
    .filter((a) => LEGAL.test(a.href + ' ' + textOf(a)))
    .slice(0, 30).map((a) => ({ href: a.href, text: textOf(a).slice(0, 100) }));

  const INTERESTING = /(firebase|supabase|amazonaws|storage\.googleapis|api\.telegram\.org|script\.google|bitrix24|amocrm|webvisor)/i;
  const inline = Array.from(document.scripts).filter((s) => !s.src && INTERESTING.test(s.textContent || ''))
    .map((s) => (s.textContent || '').slice(0, 200000)).slice(0, 10);

  return {
    title: document.title,
    storage_keys: { local: keys(window.localStorage), session: keys(window.sessionStorage) },
    permissions: (window.__qalqon && window.__qalqon.permissions) || [],
    forms,
    legal_links: legalLinks,
    inline_scripts: inline,
  };
}
"""

LINKS_JS = """() => Array.from(document.querySelectorAll('a[href]'))
  .map(a => [a.href, (a.textContent || '').trim().slice(0, 80)])"""

TEXT_JS = "() => (document.body ? document.body.innerText : '').slice(0, 150000)"
