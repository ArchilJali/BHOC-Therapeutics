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
  const OFFICIAL_LINKEDIN_COMPANY = 'https://www.linkedin.com/company/bhoc-therapeutics/';
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
  const addFooterSocialIcons = () => {
    if (!document.getElementById('bhoc-footer-social-style')) {
      const style = document.createElement('style');
      style.id = 'bhoc-footer-social-style';
      style.textContent = '.bhoc-footer-socials{display:flex;align-items:center;gap:7px;margin-top:7px;white-space:nowrap}.bhoc-footer-social-link{display:inline-flex;align-items:center;justify-content:center;width:29px;height:29px;border:1px solid currentColor;border-radius:9px;text-decoration:none;transition:transform .16s ease,opacity .16s ease}.bhoc-footer-social-link:hover{transform:translateY(-1px);opacity:.82}.bhoc-footer-social-link:focus-visible{outline:3px solid rgba(10,102,194,.2);outline-offset:2px}.bhoc-footer-social-link svg{width:17px;height:17px;display:block}.bhoc-footer-social-link[data-network="linkedin"]{color:#0a66c2}.bhoc-footer-social-link[data-network="youtube"]{color:#ff0000}';
      document.head.appendChild(style);
    }
    const makeSocial = (href, network, label, svg) => {
      const a = document.createElement('a');
      a.className = 'bhoc-footer-social-link';
      a.href = href;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.dataset.network = network;
      a.setAttribute('aria-label', label);
      a.title = label;
      a.innerHTML = svg;
      return a;
    };
    const linkedinSvg = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M5.3 7.9H1.8V19h3.5V7.9ZM3.55 2.5A2.04 2.04 0 1 0 3.55 6.58 2.04 2.04 0 0 0 3.55 2.5ZM19 12.65c0-3.35-1.79-4.91-4.18-4.91-1.93 0-2.79 1.06-3.27 1.8V7.9H8.06V19h3.49v-5.5c0-1.45.27-2.86 2.08-2.86 1.78 0 1.8 1.67 1.8 2.96V19H19v-6.35Z"/></svg>';
    const youtubeSvg = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="2.5" y="5.5" width="19" height="13" rx="4" fill="currentColor"/><path d="m10 9 5.5 3-5.5 3Z" fill="white"/></svg>';
    document.querySelectorAll('footer').forEach(footer => {
      if (footer.querySelector('.bhoc-footer-socials')) return;
      const nav = document.createElement('span');
      nav.className = 'bhoc-footer-socials';
      nav.setAttribute('role', 'group');
      nav.setAttribute('aria-label', 'BHOC social media');
      nav.append(
        makeSocial(OFFICIAL_LINKEDIN_COMPANY, 'linkedin', 'BHOC Therapeutics on LinkedIn', linkedinSvg),
        makeSocial(OFFICIAL_YOUTUBE_CHANNEL, 'youtube', 'BHOC Therapeutics on YouTube', youtubeSvg)
      );
      footer.querySelectorAll('a[href="https://www.linkedin.com/company/bhoc-therapeutics/"],a[href="https://www.youtube.com/@BHOCTherapeutics"]').forEach(link => {
        if (!link.classList.contains('bhoc-footer-social-link')) link.remove();
      });
      const homeBrand = footer.querySelector('.footer-grid > div:first-child');
      const homeSubtitle = homeBrand ? [...homeBrand.children].find(el => el.tagName === 'SPAN' && /Precision Oxygen Therapeutics/i.test(el.textContent || '')) : null;
      if (homeSubtitle) {
        homeSubtitle.insertAdjacentElement('afterend', nav);
        return;
      }
      const innerBrand = footer.querySelector('.footer-brand');
      const innerSubtitle = innerBrand && innerBrand.nextElementSibling && innerBrand.nextElementSibling.tagName === 'P'
        && /Precision Oxygen Therapeutics/i.test(innerBrand.nextElementSibling.textContent || '')
        ? innerBrand.nextElementSibling
        : null;
      if (innerSubtitle) {
        innerSubtitle.insertAdjacentElement('afterend', nav);
        return;
      }
      const fallback = footer.querySelector('.home-wrap, .footer-inner, .footer-container, .shell') || footer;
      fallback.appendChild(nav);
    });
  };
  const bottom = document.createElement('nav'); bottom.className = 'bhoc-context-bottom'; bottom.setAttribute('aria-label', 'End of page navigation');
  if (history.length > 1) bottom.append(backButton());
  if (returnContext) bottom.append(link(returnContext.url, 'Return to ' + clean(returnContext.label || labelFor(returnContext.url))));
  if (isBhoc && !isHub) bottom.append(link('/bhoc/', 'BHOC overview'));
  bottom.append(link(site.home, site.name), link('#' + body.id, '↑ Back to top')); main.append(bottom);
  addFooterSocialIcons();
  const top = document.createElement('button'); top.type = 'button'; top.className = 'bhoc-context-top'; top.textContent = '↑ Top'; top.setAttribute('aria-label', 'Back to top');
  top.addEventListener('click', () => window.scrollTo({top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'}));
  const updateTop = () => top.classList.toggle('is-visible', scrollY > 650); window.addEventListener('scroll', updateTop, {passive: true}); updateTop(); body.append(top);
})();
