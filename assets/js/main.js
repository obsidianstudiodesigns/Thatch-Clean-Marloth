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
    }, { rootMargin: '-76px 0px 0px 0px', threshold: 0 });
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

  // Hero: a few slow motes of light drifting through the sunbeam.
  const cv = document.querySelector('.hero__motes');
  if (cv && !reduce && cv.getContext) {
    const ctx = cv.getContext('2d');
    let w = 0, h = 0, dpr = 1, motes = [], raf = 0, running = false;
    const size = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = cv.clientWidth; h = cv.clientHeight;
      cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const count = Math.round(Math.min(70, (w * h) / 22000));
      motes = Array.from({ length: count }, () => ({
        x: w * (0.35 + Math.random() * 0.65),
        y: Math.random() * h,
        r: 0.6 + Math.random() * 1.8,
        vx: -0.05 + Math.random() * 0.12,
        vy: -0.05 - Math.random() * 0.16,
        a: 0.15 + Math.random() * 0.45,
        t: Math.random() * Math.PI * 2
      }));
    };
    const tick = () => {
      ctx.clearRect(0, 0, w, h);
      for (const m of motes) {
        m.t += 0.01;
        m.x += m.vx + Math.sin(m.t) * 0.08;
        m.y += m.vy;
        if (m.y < -10) { m.y = h + 10; m.x = w * (0.35 + Math.random() * 0.65); }
        const g = ctx.createRadialGradient(m.x, m.y, 0, m.x, m.y, m.r * 3);
        g.addColorStop(0, `rgba(255,226,170,${m.a * (0.7 + 0.3 * Math.sin(m.t * 2))})`);
        g.addColorStop(1, 'rgba(255,226,170,0)');
        ctx.fillStyle = g;
        ctx.beginPath(); ctx.arc(m.x, m.y, m.r * 3, 0, Math.PI * 2); ctx.fill();
      }
      raf = requestAnimationFrame(tick);
    };
    const start = () => { if (!running) { running = true; raf = requestAnimationFrame(tick); } };
    const stop = () => { running = false; cancelAnimationFrame(raf); };
    size();
    let rt;
    window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(size, 200); }, { passive: true });
    new IntersectionObserver(([e]) => (e.isIntersecting ? start() : stop())).observe(cv);
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
  }
})();
