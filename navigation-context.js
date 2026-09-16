(() => {
  'use strict';
  if (window.__bhocContextNavigation) return;
  window.__bhocContextNavigation = true;

  const body = document.body;
  const main = document.querySelector('main');
  if (!body || !main) return;
  if (!body.id) body.id = 'top';

  const current = new URL(window.location.href);
  const pageBase = value => {
    const url = new URL(value, current.href);
    return `${url.origin}${url.pathname.replace(/\/index\.html$/, '/')}`;
  };
  const currentBase = pageBase(current.href);
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
    if (host === 'bhoctherapeutics.com' || host === 'www.bhoctherapeutics.com' || host === '127.0.0.1' || host === 'localhost') {
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
      if (p.startsWith('/bhoc/')) return {label: 'Understand BHOC', href: 'https://bhoctherapeutics.com/bhoc/'};
      if (p.startsWith('/news/')) return {label: 'News', href: 'https://bhoctherapeutics.com/news/'};
      const map = [['science/', 'Science'], ['technology/', 'Technology'], ['applications/', 'Applications'], ['evidence/', 'Evidence'], ['partners/', 'Partners'], ['archil-jaliashvili/', 'Archil Jaliashvili']];
      const hit = map.find(([segment]) => p.includes('/' + segment));
      return hit ? {label: hit[1], href: current.href.split('#')[0]} : {label: pageHeading, href: current.href.split('#')[0]};
    }
    return {label: pageHeading, href: current.href.split('#')[0]};
  })();

  const isBhocSection = site.name === 'BHOC Therapeutics' && current.pathname.startsWith('/bhoc/');
  const isBhocHub = isBhocSection && /^\/bhoc\/(?:index\.html)?$/.test(current.pathname);
  if (isBhocSection) body.classList.add('bhoc-section-page');

  const bhocNavigation = [
    {label: 'Overview', location: 'Overview', href: '/bhoc/#what-bhoc', target: 'what-bhoc'},
    {label: 'Latest Updates', location: 'Latest Updates', href: '/bhoc/#knowledge-updates', target: 'knowledge-updates'},
    {label: '01 What', location: '01 · What is BHOC?', href: '/bhoc/#what-bhoc-detail', target: 'what-bhoc-detail'},
    {label: '02 Why', location: '02 · Why BHOC?', href: '/bhoc/#why-bhoc', target: 'why-bhoc'},
    {label: '03 Artificial Blood', location: '03 · Artificial Blood & Blood Substitute', href: '/bhoc/artificial-blood-blood-substitute/', target: 'artificial-blood', path: '/bhoc/artificial-blood-blood-substitute/'},
    {label: '04 Oxygen Regulation', location: '04 · Oxygen Regulation', href: '/bhoc/#natural-regulation', target: 'natural-regulation'},
    {label: '05 Evolution', location: '05 · Evolution & Adaptation', href: '/bhoc/#evolution-adaptation', target: 'evolution-adaptation'},
    {label: '06 Outside RBC', location: '06 · Outside the RBC', href: '/bhoc/#outside-rbc', target: 'outside-rbc'},
    {label: '07 BHOC Difference', location: '07 · BHOC Difference', href: '/bhoc/#what-different', target: 'what-different'},
    {label: '08 Why We Exist', location: '08 · Why We Exist', href: '/bhoc/#precision-oxygen', target: 'precision-oxygen'},
    {label: 'History', location: 'Historical Evolution', href: '/bhoc/historical-evolution/', path: '/bhoc/historical-evolution/'}
  ];

  let referrer = null;
  try {
    if (document.referrer) {
      const candidate = new URL(document.referrer);
      const candidateBase = pageBase(candidate.href);
      if (trustedHost(candidate.hostname) && candidateBase !== currentBase) {
        referrer = {url: candidate.href, label: ecosystemLabel(candidate)};
      }
    }
  } catch (_error) {}

  let stored = null;
  try {
    stored = JSON.parse(sessionStorage.getItem('bhocNavigationReturn') || 'null');
    if (stored && (!stored.url || Date.now() - Number(stored.time || 0) > 6 * 60 * 60 * 1000 || pageBase(stored.url) === currentBase)) stored = null;
  } catch (_error) { stored = null; }

  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link) return;
    try {
      const destination = new URL(link.href, current.href);
      if (!trustedHost(destination.hostname)) return;
      const destinationBase = pageBase(destination.href);
      if (destinationBase === currentBase) return;
      if (destination.origin === current.origin) {
        sessionStorage.setItem('bhocNavigationReturn', JSON.stringify({url: current.href, label: pageHeading, time: Date.now()}));
      }
    } catch (_error) {}
  }, true);

  // Keep the expanded route interface inside the BHOC authority section.
  // Other site pages retain their established header, layout and native breadcrumbs.
  if (!isBhocSection) return;

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
      .bhoc-context-nav{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-top:8px;margin-bottom:8px;padding:9px 12px;border:1px solid #d9e5ef;border-radius:12px;background:linear-gradient(90deg,#f7fbfe 0%,#fff 62%,#fff8f7 100%)}
      .bhoc-context-trail,.bhoc-context-actions,.bhoc-context-bottom{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
      .bhoc-context-nav a,.bhoc-context-nav button,.bhoc-context-bottom a,.bhoc-context-bottom button{appearance:none;border:0;background:none;padding:0;color:#174c70;font:inherit;text-decoration:none;cursor:pointer}
      .bhoc-context-nav a:hover,.bhoc-context-nav button:hover,.bhoc-context-bottom a:hover,.bhoc-context-bottom button:hover{color:#d82d2a;text-decoration:none}
      .bhoc-context-sep{color:#9aabb7;font-weight:600}
      .bhoc-context-current{display:inline-flex;align-items:center;min-height:26px;padding:4px 10px;border:1px solid #c8deea;border-radius:999px;background:#eaf5fa;box-shadow:inset 3px 0 0 #f22c26;color:#123f60;font-weight:850}
      .bhoc-context-actions a,.bhoc-context-actions button{padding:4px 7px;border-radius:7px}
      .bhoc-context-bottom{justify-content:flex-end;margin-top:34px;padding:16px 0 10px;border-top:1px solid rgba(51,79,72,.16)}
      .bhoc-context-top{position:fixed;right:18px;bottom:18px;z-index:1200;display:none;align-items:center;justify-content:center;min-width:48px;height:38px;padding:0 12px;border:1px solid rgba(49,93,84,.24);border-radius:999px;background:rgba(255,255,255,.96);box-shadow:0 8px 28px rgba(24,47,42,.14);color:#315d54;font:800 12px/1 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;cursor:pointer}
      .bhoc-context-top.is-visible{display:flex}
      .bhoc-section-page .bhoc-guide,.bhoc-section-page .bhoc-crumbs,.bhoc-section-page .legacy-bhoc-crumbs{display:none!important}
      .bhoc-subnav{position:sticky;top:0;z-index:45;border-top:1px solid #d9e5f4;border-bottom:1px solid #d9e5f4;background:rgba(255,255,255,.97);backdrop-filter:blur(10px)}
      .bhoc-subnav-inner{display:flex;align-items:center;gap:5px;width:min(1180px,calc(100% - 48px));min-height:48px;margin:auto;overflow-x:auto;scrollbar-width:thin}
      .bhoc-subnav .subnav-title{flex:0 0 auto;margin-right:4px;color:#f22c26;font:900 8px/1.2 Arial,sans-serif;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap}
      .bhoc-subnav a{flex:0 0 auto;padding:7px 10px;border:1px solid transparent;border-radius:999px;color:#0b377f;font:800 9.5px/1.2 Arial,sans-serif;text-decoration:none;white-space:nowrap}
      .bhoc-subnav a:hover,.bhoc-subnav a:focus{border-color:#cddde8;background:#f3f8ff;color:#d82d2a;outline:none}
      .bhoc-subnav a.is-active,.bhoc-subnav a[aria-current="location"],.bhoc-subnav a[aria-current="page"]{border-color:#102f49;background:#102f49;color:#fff;box-shadow:0 5px 14px rgba(16,47,73,.16)}
      @media(max-width:720px){.bhoc-context-nav{align-items:flex-start;flex-direction:column;gap:7px;margin-top:6px;padding:8px 10px}.bhoc-context-trail{gap:6px}.bhoc-context-actions{width:100%;overflow-x:auto;flex-wrap:nowrap;padding-bottom:2px}.bhoc-context-actions a,.bhoc-context-actions button{flex:0 0 auto}.bhoc-context-current{max-width:calc(100vw - 88px);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.bhoc-context-bottom{justify-content:flex-start}.bhoc-context-top{right:12px;bottom:12px}.bhoc-subnav-inner{width:calc(100% - 24px);min-height:46px}.bhoc-subnav .subnav-title{display:none}}
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
  let currentLocationLabel = null;

  if (route.label !== 'Home') {
    const sep = document.createElement('span'); sep.className = 'bhoc-context-sep'; sep.setAttribute('aria-hidden', 'true'); sep.textContent = '›';
    trail.appendChild(sep);
    if (isBhocSection) {
      const section = document.createElement('a'); section.href = route.href; section.textContent = route.label; trail.appendChild(section);
      const sep2 = document.createElement('span'); sep2.className = 'bhoc-context-sep'; sep2.setAttribute('aria-hidden', 'true'); sep2.textContent = '›';
      currentLocationLabel = document.createElement('span');
      currentLocationLabel.className = 'bhoc-context-current';
      currentLocationLabel.setAttribute('aria-current', 'page');
      const childItem = bhocNavigation.find(item => item.path === current.pathname.replace(/\/index\.html$/, '/'));
      currentLocationLabel.textContent = isBhocHub ? 'Overview' : (childItem?.location || pageHeading);
      trail.append(sep2, currentLocationLabel);
    } else if ((current.pathname.startsWith('/initiative/') && site.name === 'BHOC Veterinary') || (current.pathname.startsWith('/news/') && site.name === 'BHOC Therapeutics')) {
      const section = document.createElement('a'); section.href = route.href; section.textContent = route.label; trail.appendChild(section);
      if (pageHeading !== route.label && currentBase !== pageBase(route.href)) {
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
    back.textContent = '← Back';
    back.addEventListener('click', goBack);
    actions.appendChild(back);
  }
  if (route.label !== 'Home' && route.href && currentBase !== pageBase(route.href)) {
    const sectionHome = document.createElement('a'); sectionHome.href = route.href; sectionHome.textContent = isBhocSection ? 'BHOC map' : `${route.label} home`; actions.appendChild(sectionHome);
  }
  const top = document.createElement('a'); top.href = '#top'; top.textContent = '↑ Top'; actions.appendChild(top);
  bar.append(trail, actions);

  const header = document.querySelector('header');
  if (header) header.insertAdjacentElement('afterend', bar);
  else main.prepend(bar);

  const ensureBhocSubnav = () => {
    if (!isBhocSection) return null;
    let subnav = document.querySelector('.bhoc-subnav');
    if (!subnav) {
      subnav = document.createElement('nav');
      subnav.className = 'bhoc-subnav';
      subnav.setAttribute('aria-label', 'Understand BHOC sections and pages');
      const inner = document.createElement('div');
      inner.className = 'bhoc-subnav-inner';
      const title = document.createElement('span');
      title.className = 'subnav-title';
      title.textContent = 'Understand BHOC';
      inner.appendChild(title);
      for (const item of bhocNavigation) {
        const link = document.createElement('a');
        link.href = item.href;
        link.textContent = item.label;
        link.dataset.bhocTarget = item.target || '';
        if (item.path) link.dataset.bhocPath = item.path;
        inner.appendChild(link);
      }
      subnav.appendChild(inner);
      const insertionPoint = document.querySelector('.brand-network') || document.querySelector('.bhoc-guide') || bar;
      insertionPoint.insertAdjacentElement('afterend', subnav);
    }

    for (const link of subnav.querySelectorAll('a[href]')) {
      const resolved = new URL(link.href, current.href);
      const item = bhocNavigation.find(candidate => candidate.path
        ? resolved.pathname.replace(/\/index\.html$/, '/') === candidate.path
        : resolved.hash === `#${candidate.target}`);
      if (!item) continue;
      link.dataset.bhocTarget = item.target || '';
      if (item.path) link.dataset.bhocPath = item.path;
    }
    return subnav;
  };

  const bhocSubnav = ensureBhocSubnav();
  const markBhocLocation = item => {
    if (!item || !bhocSubnav) return;
    for (const link of bhocSubnav.querySelectorAll('a[href]')) {
      const matchesTarget = item.target && link.dataset.bhocTarget === item.target;
      const matchesPath = item.path && link.dataset.bhocPath === item.path;
      const active = Boolean(matchesTarget || matchesPath);
      link.classList.toggle('is-active', active);
      if (active) link.setAttribute('aria-current', isBhocHub ? 'location' : 'page');
      else link.removeAttribute('aria-current');
    }
    if (currentLocationLabel) currentLocationLabel.textContent = item.location;
  };

  if (bhocSubnav) {
    if (isBhocHub) {
      const sectionItems = bhocNavigation
        .filter(item => item.target && document.getElementById(item.target))
        .map(item => ({item, element: document.getElementById(item.target)}));
      let locationFrame = 0;
      const updateBhocLocation = () => {
        locationFrame = 0;
        const threshold = (bhocSubnav.getBoundingClientRect().height || 48) + 34;
        let active = sectionItems[0]?.item;
        for (const entry of sectionItems) {
          if (entry.element.getBoundingClientRect().top <= threshold) active = entry.item;
          else break;
        }
        markBhocLocation(active);
      };
      const requestLocationUpdate = () => {
        if (!locationFrame) locationFrame = window.requestAnimationFrame(updateBhocLocation);
      };
      window.addEventListener('scroll', requestLocationUpdate, {passive: true});
      window.addEventListener('resize', requestLocationUpdate, {passive: true});
      window.addEventListener('hashchange', requestLocationUpdate);
      requestLocationUpdate();
    } else {
      const normalizedPath = current.pathname.replace(/\/index\.html$/, '/');
      markBhocLocation(bhocNavigation.find(item => item.path === normalizedPath) || {location: pageHeading});
    }
  }

  const bottom = document.createElement('nav');
  bottom.className = 'bhoc-context-bottom';
  bottom.setAttribute('aria-label', 'End of page navigation');
  if (returnContext || window.history.length > 1) {
    const back = document.createElement('button'); back.type = 'button'; back.textContent = '← Back'; back.addEventListener('click', goBack); bottom.appendChild(back);
    const sep = document.createElement('span'); sep.className = 'bhoc-context-sep'; sep.textContent = '·'; bottom.appendChild(sep);
  }
  if (route.label !== 'Home' && route.href && currentBase !== pageBase(route.href)) {
    const sectionHome = document.createElement('a'); sectionHome.href = route.href; sectionHome.textContent = isBhocSection ? 'BHOC map' : `${route.label} home`; bottom.appendChild(sectionHome);
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
