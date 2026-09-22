(() => {
  'use strict';
  if (document.documentElement.hasAttribute('data-bhoc-knowledge-map')) return;
  if (window.__bhocContextNavigation) return;
  window.__bhocContextNavigation = true;
  const main = document.querySelector('main');
  if (!main) return;
  const body = document.body;
  if (!body.id) body.id = main.id === 'top' ? 'page-top' : 'top';
  if (!main.id) main.id = 'main-content';
  const current = new URL(location.href);
  const OFFICIAL_YOUTUBE_CHANNEL = 'https://www.youtube.com/@BHOCTherapeutics';
  const clean = value => String(value || '').replace(/\s+/g, ' ').trim();
  const pageBase = value => {
    const url = new URL(value, current.href);
    return url.origin + url.pathname.replace(/\/index\.html$/, '/');
  };
  const trusted = value => {
    try {
      const u = new URL(value, current.href);
      return u.protocol === 'https:' && (
        ['bhoctherapeutics.com', 'www.bhoctherapeutics.com', 'bhocvet.com', 'www.bhocvet.com'].includes(u.hostname) ||
        (u.hostname === 'archiljali.github.io' && /^\/BHOC-(?:VET-)?platform\//.test(u.pathname))
      );
    } catch (_) { return false; }
  };
  const pageHeading = clean(main.querySelector('h1')?.textContent || document.title.split('|')[0]);
  const isVet = /^(www\.)?bhocvet\.com$/.test(current.hostname);
  const site = {name: isVet ? 'BHOC Veterinary' : 'BHOC Therapeutics', home: isVet ? 'https://bhocvet.com/' : 'https://bhoctherapeutics.com/'};
  const isBhoc = !isVet && current.pathname.startsWith('/bhoc/');
  const isHub = isBhoc && /^\/bhoc\/(?:index\.html)?$/.test(current.pathname);
  if (isBhoc) body.classList.add('bhoc-section-page');
  const routes = isVet
    ? [['/initiative/', 'Initiative'], ['/product.html', 'Product'], ['/applications.html', 'Applications'], ['/science.html', 'Science'], ['/evidence.html', 'Evidence'], ['/news.html', 'News'], ['/contact.html', 'Contact']]
    : [['/bhoc/', 'Understand BHOC'], ['/science/', 'Science'], ['/technology/', 'Technology'], ['/applications/', 'Applications'], ['/evidence/', 'Evidence'], ['/news/', 'News'], ['/partners/', 'Investors & Partners'], ['/archil-jaliashvili/', 'Archil Jaliashvili']];
  const found = routes.find(([path]) => current.pathname.startsWith(path));
  const route = found ? {label: found[1], href: new URL(found[0], site.home).href} : {label: pageHeading, href: current.href.split('#')[0]};
  const labelFor = value => {
    const u = new URL(value, current.href);
    if (u.hostname === 'archiljali.github.io') return u.pathname.startsWith('/BHOC-VET-platform/') ? 'BHOC VET Knowledge Base' : 'BHOC Evidence Platform';
    if (/bhocvet\.com$/.test(u.hostname)) return u.pathname.startsWith('/initiative/') ? 'BHOC Species & Biodiversity Initiative' : 'BHOC Veterinary';
    const hit = routes.find(([path]) => u.pathname.startsWith(path));
    return hit?.[1] || 'BHOC Therapeutics';
  };
  let returnContext = null;
  try {
    const saved = JSON.parse(sessionStorage.getItem('bhocNavigationReturn') || 'null');
    if (saved && trusted(saved.url) && Date.now() - Number(saved.time) < 21600000 && pageBase(saved.url) !== pageBase(current.href)) returnContext = saved;
  } catch (_) {}
  if (!returnContext && document.referrer && trusted(document.referrer) && pageBase(document.referrer) !== pageBase(current.href)) {
    returnContext = {url: document.referrer, label: labelFor(document.referrer)};
  }
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link) return;
    try {
      const destination = new URL(link.href, current.href);
      if (destination.origin === current.origin && pageBase(destination.href) !== pageBase(current.href)) {
        sessionStorage.setItem('bhocNavigationReturn', JSON.stringify({url: location.href, label: route.label || pageHeading, time: Date.now()}));
      }
    } catch (_) {}
  }, true);
  const link = (href, text) => { const a = document.createElement('a'); a.href = href; a.textContent = text; return a; };
  const separator = () => { const s = document.createElement('span'); s.className = 'bhoc-context-sep'; s.textContent = '›'; s.setAttribute('aria-hidden', 'true'); return s; };
  const backButton = () => { const b = document.createElement('button'); b.type = 'button'; b.textContent = '← Back'; b.addEventListener('click', () => history.back()); return b; };
  if (!document.querySelector('a.bhoc-skip-link')) { const skip = link('#' + main.id, 'Skip to content'); skip.className = 'bhoc-skip-link'; body.prepend(skip); }
  const bar = document.createElement('nav'); bar.className = 'bhoc-context-nav'; bar.setAttribute('aria-label', 'Page location and return navigation');
  const trail = document.createElement('div'); trail.className = 'bhoc-context-trail'; trail.append(link(site.home, site.name));
  const locationLabel = document.createElement('span'); locationLabel.className = 'bhoc-context-current'; locationLabel.setAttribute('aria-current', isHub ? 'location' : 'page');
  if (isBhoc) trail.append(separator(), link('/bhoc/', 'Understand BHOC'));
  if (current.pathname !== '/' && current.pathname !== '/index.html') { locationLabel.textContent = isHub ? 'Overview' : pageHeading; trail.append(separator(), locationLabel); }
  const actions = document.createElement('div'); actions.className = 'bhoc-context-actions';
  if (history.length > 1) actions.append(backButton());
  if (returnContext) { const a = link(returnContext.url, 'Return to ' + clean(returnContext.label || labelFor(returnContext.url))); a.dataset.bhocReturn = ''; actions.append(a); }
  if (isBhoc && !isHub) actions.append(link('/bhoc/', 'BHOC overview'));
  actions.append(link('#' + body.id, '↑ Top')); bar.append(trail, actions);
  const header = document.querySelector('header'); if (header) header.insertAdjacentElement('afterend', bar); else main.before(bar);

  // The rendered, static contents list is the only runtime source for labels and targets.
  const nav = isBhoc ? document.querySelector('.bhoc-subnav') : null;
  if (nav) {
    const toggle = nav.querySelector('.bhoc-contents-toggle');
    const caption = nav.querySelector('.bhoc-contents-current');
    const links = [...nav.querySelectorAll('.bhoc-subnav-inner a[href]')];
    const mobile = matchMedia('(max-width: 720px)');
    const setOpen = open => { nav.classList.toggle('is-open', open); toggle?.setAttribute('aria-expanded', String(open)); };
    if (toggle) { nav.dataset.enhanced = 'true'; toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true')); }
    const offset = () => {
      const height = mobile.matches && toggle ? toggle.getBoundingClientRect().height : nav.getBoundingClientRect().height;
      const value = Math.ceil(height) + 16;
      document.documentElement.style.setProperty('--bhoc-anchor-offset', value + 'px');
      return value;
    };
    const mark = selected => {
      for (const a of links) { const active = a === selected; a.classList.toggle('is-active', active); if (active) a.setAttribute('aria-current', isHub ? 'location' : 'page'); else a.removeAttribute('aria-current'); }
      const text = selected ? clean(selected.dataset.location || selected.textContent) : pageHeading;
      locationLabel.textContent = text;
      if (caption) { caption.textContent = text; caption.title = text; }
    };
    const local = links.map(a => {
      const u = new URL(a.href, current.href);
      let id = ''; try { id = decodeURIComponent(u.hash.slice(1)); } catch (_) {}
      return {a, element: pageBase(u.href) === pageBase(current.href) ? document.getElementById(id) : null};
    }).filter(entry => entry.element).sort((a, b) => a.element === b.element ? 0 : (a.element.compareDocumentPosition(b.element) & Node.DOCUMENT_POSITION_FOLLOWING) ? -1 : 1);
    let frame = 0;
    const update = () => {
      frame = 0;
      const threshold = offset() + 8;
      if (!isHub) { const selected = links.find(a => a.dataset.bhocPath === current.pathname.replace(/\/index\.html$/, '/')); mark(selected); return; }
      let selected = local[0]?.a;
      for (const entry of local) { if (entry.element.getBoundingClientRect().top <= threshold) selected = entry.a; else break; }
      mark(selected);
    };
    const queue = () => { if (!frame) frame = requestAnimationFrame(update); };
    nav.addEventListener('click', event => { if (event.target.closest('a[href]')) { setOpen(false); offset(); } });
    document.addEventListener('keydown', event => { if (event.key === 'Escape' && nav.classList.contains('is-open')) { setOpen(false); toggle?.focus(); } });
    document.addEventListener('click', event => { if (!nav.contains(event.target)) setOpen(false); });
    mobile.addEventListener('change', () => { setOpen(false); queue(); });
    window.addEventListener('scroll', queue, {passive: true}); window.addEventListener('resize', queue, {passive: true}); window.addEventListener('hashchange', queue);
    if ('ResizeObserver' in window) new ResizeObserver(queue).observe(nav);
    offset(); queue();
    // The sticky menu height varies with viewport width. Keep deep links below it.
    const alignInitial = () => {
      let id = ''; try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) {}
      const target = id && document.getElementById(id);
      if (target && isHub) { offset(); target.scrollIntoView({block: 'start', behavior: 'instant'}); queue(); }
    };
    if (document.readyState === 'complete') requestAnimationFrame(alignInitial); else window.addEventListener('load', alignInitial, {once: true});
  }
  const bottom = document.createElement('nav'); bottom.className = 'bhoc-context-bottom'; bottom.setAttribute('aria-label', 'End of page navigation');
  if (history.length > 1) bottom.append(backButton());
  if (returnContext) bottom.append(link(returnContext.url, 'Return to ' + clean(returnContext.label || labelFor(returnContext.url))));
  if (isBhoc && !isHub) bottom.append(link('/bhoc/', 'BHOC overview'));
  const youtubeLink = link(OFFICIAL_YOUTUBE_CHANNEL, 'YouTube @BHOCTherapeutics'); youtubeLink.target = '_blank'; youtubeLink.rel = 'noopener noreferrer';
  bottom.append(link(site.home, site.name), youtubeLink, link('#' + body.id, '↑ Back to top')); main.append(bottom);
  const top = document.createElement('button'); top.type = 'button'; top.className = 'bhoc-context-top'; top.textContent = '↑ Top'; top.setAttribute('aria-label', 'Back to top');
  top.addEventListener('click', () => window.scrollTo({top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'}));
  const updateTop = () => top.classList.toggle('is-visible', scrollY > 650); window.addEventListener('scroll', updateTop, {passive: true}); updateTop(); body.append(top);
})();
