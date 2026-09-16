(() => {
  'use strict';
  if (window.__bhocContextNavigation) return;
  window.__bhocContextNavigation = true;

  const body = document.body;
  const main = document.querySelector('main');
  if (!body || !main) return;
  if (!body.id) body.id = 'top';

  const current = new URL(window.location.href);
  const currentBase = `${current.origin}${current.pathname}${current.search}`;
  const clean = value => String(value || '').replace(/\s+/g, ' ').trim();
  const clamp = (value, max = 58) => {
    const text = clean(value);
    return text.length > max ? `${text.slice(0, max - 1)}…` : text;
  };
  const pageHeading = clamp(document.querySelector('main h1')?.textContent || document.title.split('|')[0] || 'Current page');

  const trustedHost = hostname => [
    'bhocvet.com', 'www.bhocvet.com',
    'bhoctherapeutics.com', 'www.bhoctherapeutics.com',
    'archiljali.github.io'
  ].includes(hostname.toLowerCase());

  const ecosystemLabel = url => {
    const host = url.hostname.toLowerCase();
    const path = url.pathname;
    if (host === 'bhocvet.com' || host === 'www.bhocvet.com') {
      if (/^\/initiative\//.test(path)) return 'BHOC Species & Biodiversity Initiative';
      if (/applications\.html$/.test(path)) return 'BHOC Veterinary Applications';
      if (/science\.html$/.test(path)) return 'BHOC Veterinary Science';
      if (/news\.html$/.test(path)) return 'BHOC Veterinary News';
      return 'BHOC Veterinary';
    }
    if (host === 'bhoctherapeutics.com' || host === 'www.bhoctherapeutics.com') {
      if (/^\/news\//.test(path)) return 'BHOC Therapeutics News';
      if (/^\/bhoc\//.test(path)) return 'BHOC Therapeutics · BHOC';
      return 'BHOC Therapeutics';
    }
    if (host === 'archiljali.github.io') {
      if (path.startsWith('/BHOC-VET-platform/')) return 'BHOC VET Knowledge Base';
      if (path.startsWith('/BHOC-platform/veterinary/')) return 'Vet Real-World Evidence & Cases';
      if (path.startsWith('/BHOC-platform/')) return 'BHOC Evidence Platform';
    }
    return 'Previous BHOC page';
  };

  const site = (() => {
    const host = current.hostname.toLowerCase();
    if (host === 'bhocvet.com' || host === 'www.bhocvet.com') {
      return {name: 'BHOC Veterinary', home: 'https://bhocvet.com/'};
    }
    if (host === 'bhoctherapeutics.com' || host === 'www.bhoctherapeutics.com') {
      return {name: 'BHOC Therapeutics', home: 'https://bhoctherapeutics.com/'};
    }
    return {name: 'BHOC', home: '/'};
  })();

  const route = (() => {
    const p = current.pathname;
    if (site.name === 'BHOC Veterinary') {
      if (p === '/' || (/\/index\.html$/.test(p) && !p.startsWith('/initiative/'))) return {label: 'Home', href: site.home};
      if (p.startsWith('/initiative/')) return {label: 'Initiative', href: 'https://bhocvet.com/initiative/'};
      const map = [
        ['product.html', 'Product'], ['applications.html', 'Applications'], ['evidence.html', 'Evidence'],
        ['science.html', 'Science'], ['initiative.html', 'Initiative'], ['related-information.html', 'Related Information'],
        ['news.html', 'News'], ['contact.html', 'Contact'], ['publications.html', 'Publications']
      ];
      const hit = map.find(([suffix]) => p.endsWith('/' + suffix) || p.endsWith(suffix));
      return hit ? {label: hit[1], href: current.href.split('#')[0]} : {label: pageHeading, href: current.href.split('#')[0]};
    }
    if (site.name === 'BHOC Therapeutics') {
      if (p === '/' || p === '/index.html') return {label: 'Home', href: site.home};
      if (p.startsWith('/bhoc/')) return {label: 'BHOC', href: 'https://bhoctherapeutics.com/bhoc/'};
      if (p.startsWith('/news/')) return {label: 'News', href: 'https://bhoctherapeutics.com/news/'};
      const map = [['science/', 'Science'], ['technology/', 'Technology'], ['applications/', 'Applications'], ['evidence/', 'Evidence'], ['partners/', 'Partners'], ['archil-jaliashvili/', 'Archil Jaliashvili']];
      const hit = map.find(([segment]) => p.includes('/' + segment));
      return hit ? {label: hit[1], href: current.href.split('#')[0]} : {label: pageHeading, href: current.href.split('#')[0]};
    }
    return {label: pageHeading, href: current.href.split('#')[0]};
  })();

  let referrer = null;
  try {
    if (document.referrer) {
      const candidate = new URL(document.referrer);
      const candidateBase = `${candidate.origin}${candidate.pathname}${candidate.search}`;
      if (trustedHost(candidate.hostname) && candidateBase !== currentBase) {
        referrer = {url: candidate.href, label: ecosystemLabel(candidate)};
      }
    }
  } catch (_error) {}

  let stored = null;
  try {
    stored = JSON.parse(sessionStorage.getItem('bhocNavigationReturn') || 'null');
    if (stored && (!stored.url || Date.now() - Number(stored.time || 0) > 6 * 60 * 60 * 1000 || stored.url.split('#')[0] === current.href.split('#')[0])) stored = null;
  } catch (_error) { stored = null; }

  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link) return;
    try {
      const destination = new URL(link.href, current.href);
      if (!trustedHost(destination.hostname)) return;
      const destinationBase = `${destination.origin}${destination.pathname}${destination.search}`;
      if (destinationBase === currentBase) return;
      if (destination.origin === current.origin) {
        sessionStorage.setItem('bhocNavigationReturn', JSON.stringify({url: current.href, label: pageHeading, time: Date.now()}));
      }
    } catch (_error) {}
  }, true);

  const returnContext = referrer || stored;
  const goBack = () => {
    if (window.history.length > 1) {
      window.history.back();
      return;
    }
    if (returnContext?.url) window.location.href = returnContext.url;
    else window.location.href = route.href || site.home;
  };

  if (!document.getElementById('bhoc-context-navigation-style')) {
    const style = document.createElement('style');
    style.id = 'bhoc-context-navigation-style';
    style.textContent = `
      .bhoc-context-nav,.bhoc-context-bottom{box-sizing:border-box;width:min(1180px,calc(100% - 32px));margin:0 auto;color:#53645f;font:700 12px/1.45 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
      .bhoc-context-nav{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:10px 0 11px;border-bottom:1px solid rgba(51,79,72,.16)}
      .bhoc-context-trail,.bhoc-context-actions,.bhoc-context-bottom{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
      .bhoc-context-nav a,.bhoc-context-nav button,.bhoc-context-bottom a,.bhoc-context-bottom button{appearance:none;border:0;background:none;padding:0;color:#315d54;font:inherit;text-decoration:none;cursor:pointer}
      .bhoc-context-nav a:hover,.bhoc-context-nav button:hover,.bhoc-context-bottom a:hover,.bhoc-context-bottom button:hover{text-decoration:underline;text-underline-offset:3px}
      .bhoc-context-sep{color:#a5b0ad;font-weight:500}
      .bhoc-context-current{color:#6a7673;font-weight:650}
      .bhoc-context-bottom{justify-content:flex-end;margin-top:34px;padding:16px 0 10px;border-top:1px solid rgba(51,79,72,.16)}
      .bhoc-context-top{position:fixed;right:18px;bottom:18px;z-index:1200;display:none;align-items:center;justify-content:center;min-width:48px;height:38px;padding:0 12px;border:1px solid rgba(49,93,84,.24);border-radius:999px;background:rgba(255,255,255,.96);box-shadow:0 8px 28px rgba(24,47,42,.14);color:#315d54;font:800 12px/1 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;cursor:pointer}
      .bhoc-context-top.is-visible{display:flex}
      @media(max-width:720px){.bhoc-context-nav{align-items:flex-start;flex-direction:column;gap:7px}.bhoc-context-actions{width:100%}.bhoc-context-bottom{justify-content:flex-start}.bhoc-context-top{right:12px;bottom:12px}}
    `;
    document.head.appendChild(style);
  }

  const bar = document.createElement('nav');
  bar.className = 'bhoc-context-nav';
  bar.setAttribute('aria-label', 'Page location and return navigation');

  const trail = document.createElement('div');
  trail.className = 'bhoc-context-trail';
  const home = document.createElement('a');
  home.href = site.home;
  home.textContent = site.name;
  trail.appendChild(home);

  if (route.label !== 'Home') {
    const sep = document.createElement('span'); sep.className = 'bhoc-context-sep'; sep.setAttribute('aria-hidden', 'true'); sep.textContent = '›';
    trail.appendChild(sep);
    if ((current.pathname.startsWith('/initiative/') && site.name === 'BHOC Veterinary') || (current.pathname.startsWith('/news/') && site.name === 'BHOC Therapeutics') || (current.pathname.startsWith('/bhoc/') && site.name === 'BHOC Therapeutics')) {
      const section = document.createElement('a'); section.href = route.href; section.textContent = route.label; trail.appendChild(section);
      if (pageHeading !== route.label && current.href.split('#')[0] !== route.href) {
        const sep2 = document.createElement('span'); sep2.className = 'bhoc-context-sep'; sep2.setAttribute('aria-hidden', 'true'); sep2.textContent = '›';
        const currentLabel = document.createElement('span'); currentLabel.className = 'bhoc-context-current'; currentLabel.setAttribute('aria-current', 'page'); currentLabel.textContent = pageHeading;
        trail.append(sep2, currentLabel);
      }
    } else {
      const currentLabel = document.createElement('span'); currentLabel.className = 'bhoc-context-current'; currentLabel.setAttribute('aria-current', 'page'); currentLabel.textContent = pageHeading || route.label;
      trail.appendChild(currentLabel);
    }
  }

  const actions = document.createElement('div');
  actions.className = 'bhoc-context-actions';
  if (returnContext || window.history.length > 1) {
    const back = document.createElement('button');
    back.type = 'button';
    back.textContent = returnContext ? `← Return to ${clamp(returnContext.label, 40)}` : '← Back';
    back.addEventListener('click', goBack);
    actions.appendChild(back);
  }
  if (route.label !== 'Home' && route.href && route.href !== current.href.split('#')[0]) {
    const sectionHome = document.createElement('a'); sectionHome.href = route.href; sectionHome.textContent = `${route.label} home`; actions.appendChild(sectionHome);
  }
  const top = document.createElement('a'); top.href = '#top'; top.textContent = '↑ Top'; actions.appendChild(top);
  bar.append(trail, actions);

  const header = document.querySelector('header');
  if (header) header.insertAdjacentElement('afterend', bar);
  else main.prepend(bar);

  const bottom = document.createElement('nav');
  bottom.className = 'bhoc-context-bottom';
  bottom.setAttribute('aria-label', 'End of page navigation');
  if (returnContext || window.history.length > 1) {
    const back = document.createElement('button'); back.type = 'button'; back.textContent = returnContext ? `← Return to ${clamp(returnContext.label, 40)}` : '← Back'; back.addEventListener('click', goBack); bottom.appendChild(back);
    const sep = document.createElement('span'); sep.className = 'bhoc-context-sep'; sep.textContent = '·'; bottom.appendChild(sep);
  }
  if (route.label !== 'Home' && route.href && route.href !== current.href.split('#')[0]) {
    const sectionHome = document.createElement('a'); sectionHome.href = route.href; sectionHome.textContent = `${route.label} home`; bottom.appendChild(sectionHome);
    const sep = document.createElement('span'); sep.className = 'bhoc-context-sep'; sep.textContent = '·'; bottom.appendChild(sep);
  }
  const siteHome = document.createElement('a'); siteHome.href = site.home; siteHome.textContent = site.name; bottom.appendChild(siteHome);
  const sepTop = document.createElement('span'); sepTop.className = 'bhoc-context-sep'; sepTop.textContent = '·';
  const topBottom = document.createElement('a'); topBottom.href = '#top'; topBottom.textContent = '↑ Back to top'; bottom.append(sepTop, topBottom);
  main.appendChild(bottom);

  const floating = document.createElement('button');
  floating.type = 'button'; floating.className = 'bhoc-context-top'; floating.textContent = '↑ Top'; floating.setAttribute('aria-label', 'Back to top');
  floating.addEventListener('click', () => window.scrollTo({top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}));
  const updateFloating = () => floating.classList.toggle('is-visible', window.scrollY > 650);
  window.addEventListener('scroll', updateFloating, {passive: true}); updateFloating(); document.body.appendChild(floating);
})();
