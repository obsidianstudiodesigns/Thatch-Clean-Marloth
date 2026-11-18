(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const header = document.querySelector('.site-header');
  const hero = document.querySelector('.hero');
  const mbar = document.querySelector('.mbar');
  const yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  // Header goes solid and the mobile action bar appears once the hero has scrolled away.
  if (hero && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(([e]) => {
      const past = !e.isIntersecting;
      header.classList.toggle('is-solid', past);
      if (mbar) mbar.classList.toggle('show', past);
    }, { rootMargin: '-86px 0px 0px 0px', threshold: 0 });
    io.observe(hero);
  } else if (header) {
    header.classList.add('is-solid');
  }

  // Mobile menu
  const btn = document.querySelector('.menu-btn');
  const nav = document.getElementById('nav');
  if (btn && nav) {
    const set = (open) => {
      document.body.classList.toggle('menu-open', open);
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };
    btn.addEventListener('click', () => set(!document.body.classList.contains('menu-open')));
    nav.addEventListener('click', (e) => { if (e.target.closest('a')) set(false); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') set(false); });
  }

  // Scroll reveal
  const rv = document.querySelectorAll('.rv');
  if (reduce || !('IntersectionObserver' in window)) {
    rv.forEach((el) => el.classList.add('in'));
  } else {
    const ro = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); ro.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    rv.forEach((el) => ro.observe(el));
  }

  // Process: the sticky photo follows the step in view.
  const steps = document.querySelectorAll('.step');
  const pics = document.querySelectorAll('.process__media img');
  if (steps.length && pics.length && 'IntersectionObserver' in window) {
    const so = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const n = e.target.dataset.step;
        steps.forEach((s) => s.classList.toggle('active', s === e.target));
        pics.forEach((p) => p.classList.toggle('on', p.dataset.step === n));
      });
    }, { rootMargin: '-45% 0px -45% 0px', threshold: 0 });
    steps.forEach((s) => so.observe(s));
  }

  // Quote form opens WhatsApp with the details filled in.
  const form = document.getElementById('quote');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let ok = true;
      ['name', 'service'].forEach((n) => {
        const el = form.elements[n];
        const f = el.closest('.field');
        const bad = !el.value.trim();
        f.classList.toggle('invalid', bad);
        el.setAttribute('aria-invalid', String(bad));
        if (bad) {
          el.setAttribute('aria-describedby', el.id + '-err');
          if (ok) el.focus();
          ok = false;
        }
      });
      if (!ok) return;
      const v = (n) => form.elements[n].value.trim();
      const lines = [
        'Hi Andre, I would like a free quote.',
        'Name: ' + v('name'),
        v('area') ? 'Property: ' + v('area') : '',
        'Service: ' + v('service'),
        v('message') ? 'Details: ' + v('message') : ''
      ].filter(Boolean);
      window.open('https://wa.me/27825631277?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
    });
    form.addEventListener('input', (e) => {
      const f = e.target.closest('.field');
      if (f && f.classList.contains('invalid') && e.target.value.trim()) {
        f.classList.remove('invalid');
        e.target.setAttribute('aria-invalid', 'false');
      }
    });
  }
})();
