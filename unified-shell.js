/* Shared BHOC Therapeutics navigation. The original page content stays in place. */
(() => {
  'use strict';
  if (window.__bhocUnifiedShell) return;
  window.__bhocUnifiedShell = true;

  const HOME = 'https://bhoctherapeutics.com/';
  const LIBRARY = '/evidence/library/';
  const routes = [
    {name: 'BHOC', href: '/bhoc/', path: '/bhoc/'},
    {name: 'Science', href: '/science/', path: '/science/'},
    {name: 'Technology', href: '/technology/', path: '/technology/'},
    {name: 'Applications', href: '/applications/', path: '/applications/'},
    {name: 'Evidence', href: '/evidence/', path: '/evidence/'},
    {name: 'Concepts & Hypotheses', href: '/evidence/library/concepts-hypotheses/', path: '/evidence/library/concepts-hypotheses/'},
    {name: 'News', href: '/news/', path: '/news/'},
    {name: 'Company', href: '/#company', path: '/#company'},
    {name: 'Investors & Partners', href: '/partners/', path: '/partners/'},
    {name: 'Contact', href: '/contact/', path: '/contact/'}
  ];

  const makeLink = (href, label, className) => {
    const a = document.createElement('a');
    a.href = href;
    a.textContent = label;
    if (className) a.className = className;
    return a;
  };
  const clean = value => String(value || '').replace(/\s+/g, ' ').trim();
  const pagePath = location.pathname.replace(/\/index\.html$/, '/');
  const pageTitle = () => clean(document.querySelector('main h1')?.textContent || document.querySelector('h1')?.textContent || document.title.split('|')[0]);
  const section = () => {
    if (pagePath.startsWith('/evidence/library/concepts-hypotheses/')) return routes[5];
    if (pagePath === '/' && location.hash === '#company') return routes[7];
    return routes.find(route => route.path !== '/#company' && pagePath.startsWith(route.path));
  };

  function trailParts() {
    if (pagePath === '/') return [];
    const parts = [{label: 'Home', href: '/'}];
    const add = (label, href) => parts.push({label, href});
    if (pagePath.startsWith('/bhoc/')) add('BHOC', '/bhoc/');
    else if (pagePath.startsWith('/evidence/')) {
      add('Evidence', '/evidence/');
      if (pagePath.startsWith(LIBRARY)) {
        add('Scientific Evidence Hub', LIBRARY);
        const branch = pagePath.slice(LIBRARY.length).split('/')[0];
        const branches = {
          human: ['Human Use', LIBRARY + 'human/BHOC-Human-index.html'],
          veterinary: ['Veterinary', LIBRARY + 'veterinary/Vet-index.html'],
          transplant: ['Transplantation', LIBRARY + 'transplant/Transplant-index.html'],
          clinical: ['Applications', LIBRARY + 'clinical/'],
          science: ['Science', LIBRARY + 'science/'],
          'concepts-hypotheses': ['Concepts & Hypotheses', LIBRARY + 'concepts-hypotheses/'],
          'historical-sources': ['History', LIBRARY + 'historical-sources/'],
          'real-world-evidence': ['Real-World Evidence', LIBRARY + 'real-world-evidence/'],
          'social-media': ['LinkedIn Publications', LIBRARY + 'social-media/linkedin/']
        };
        if (branches[branch]) add(...branches[branch]);
      }
    } else if (pagePath.startsWith('/news/')) add('News', '/news/');
    else if (pagePath.startsWith('/applications/')) add('Applications', '/applications/');
    else if (pagePath.startsWith('/science/')) add('Science', '/science/');
    else if (pagePath.startsWith('/technology/')) add('Technology', '/technology/');
    else if (pagePath.startsWith('/partners/')) add('Investors & Partners', '/partners/');
    else if (pagePath.startsWith('/contact/')) add('Contact', '/contact/');
    const last = parts[parts.length - 1];
    const lastPath = last?.href && new URL(last.href, HOME).pathname.replace(/\/index\.html$/, '/');
    if (lastPath !== pagePath) {
      const title = pageTitle();
      add(title || 'Current page', null);
    }
    return parts;
  }

  function buildHeader() {
    const header = document.createElement('div');
    header.className = 'bhoc-shell-header';
    header.setAttribute('role', 'banner');
    const wrap = document.createElement('div');
    wrap.className = 'bhoc-shell-wrap bhoc-shell-header-inner';
    const logo = makeLink('/', 'BHOC', 'bhoc-shell-logo');
    logo.setAttribute('aria-label', 'BHOC Therapeutics home');
    logo.innerHTML = 'BH<span>O</span>C<small>THERAPEUTICS</small>';
    const button = document.createElement('button');
    button.className = 'bhoc-shell-menu-button';
    button.type = 'button';
    button.textContent = 'Menu ☰';
    button.setAttribute('aria-controls', 'bhoc-shell-main-nav');
    button.setAttribute('aria-expanded', 'false');
    const nav = document.createElement('nav');
    nav.id = 'bhoc-shell-main-nav';
    nav.className = 'bhoc-shell-nav';
    nav.setAttribute('aria-label', 'BHOC Therapeutics main navigation');
    for (const route of routes) {
      const a = makeLink(route.href, route.name);
      nav.append(a);
    }
    const markActive = () => {
      const selected = section();
      [...nav.children].forEach((a, index) => {
        const active = routes[index] === selected;
        a.classList.toggle('is-active', active);
        if (active) a.setAttribute('aria-current', new URL(routes[index].href, HOME).pathname === pagePath ? 'page' : 'location');
        else a.removeAttribute('aria-current');
      });
    };
    markActive();
    window.addEventListener('hashchange', markActive);
    button.addEventListener('click', () => {
      const open = button.getAttribute('aria-expanded') !== 'true';
      button.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    });
    nav.addEventListener('click', event => {
      if (event.target.closest('a')) {
        nav.classList.remove('is-open');
        button.setAttribute('aria-expanded', 'false');
      }
    });
    wrap.append(logo, button, nav);
    const utility = document.createElement('div');
    utility.className = 'bhoc-shell-utility';
    utility.innerHTML = `
      <div class="bhoc-shell-wrap bhoc-shell-utility-inner">
        <div class="bhoc-shell-utility-intro"><span>Understand BHOC</span><a href="/bhoc/">BHOC - What It Really Is. <b>Why It Exists. →</b></a></div>
        <div class="bhoc-shell-utility-network" role="group" aria-label="BHOC websites">
          <a href="/evidence/library/">Scientific Evidence Hub ↗</a>
          <a href="https://bhocvet.com/">BHOC Veterinary ↗</a>
          <a href="https://bhoctransplant.com/">BHOC Transplant ↗</a>
        </div>
      </div>`;
    header.append(wrap, utility);
    return header;
  }

  function buildTrail() {
    const parts = trailParts();
    if (!parts.length) return null;
    const nav = document.createElement('nav');
    nav.className = 'bhoc-shell-trail';
    nav.setAttribute('aria-label', 'Breadcrumb');
    const wrap = document.createElement('div');
    wrap.className = 'bhoc-shell-wrap bhoc-shell-trail-inner';
    parts.forEach((part, index) => {
      if (index) {
        const sep = document.createElement('span');
        sep.textContent = '›';
        sep.setAttribute('aria-hidden', 'true');
        wrap.append(sep);
      }
      const last = index === parts.length - 1;
      const element = last ? document.createElement('span') : makeLink(part.href, part.label);
      element.textContent = part.label;
      if (last) element.setAttribute('aria-current', 'page');
      element.title = part.label;
      wrap.append(element);
    });
    nav.append(wrap);
    return nav;
  }

  function buildLocalNavigation(header) {
    if (!pagePath.startsWith(LIBRARY) || !header) return null;
    const found = new Map();
    for (const a of header.querySelectorAll('nav a[href]')) {
      const url = new URL(a.href, HOME);
      if (url.origin !== location.origin || !url.pathname.startsWith(LIBRARY)) continue;
      const label = clean(a.textContent);
      if (label && label.length < 46 && !found.has(url.href)) found.set(url.href, label);
    }
    if (!found.size) return null;
    const details = document.createElement('details');
    details.className = 'bhoc-shell-local-nav bhoc-shell-wrap';
    const summary = document.createElement('summary');
    summary.textContent = 'Explore Evidence sections';
    const links = document.createElement('div');
    links.className = 'bhoc-shell-local-links';
    for (const [href, label] of found) {
      const a = makeLink(href, label);
      if (new URL(href).pathname.replace(/\/index\.html$/, '/') === pagePath) a.setAttribute('aria-current', 'page');
      links.append(a);
    }
    details.append(summary, links);
    return details;
  }

  function buildFooter() {
    const footer = document.createElement('div');
    footer.className = 'bhoc-shell-footer';
    footer.setAttribute('role', 'contentinfo');
    footer.innerHTML = `
      <div class="bhoc-shell-wrap">
        <div class="bhoc-shell-footer-grid">
          <div class="bhoc-shell-footer-brand"><strong>BHOC</strong><span>Precision Oxygen Therapeutics</span>
            <div class="bhoc-shell-social"><a href="https://www.linkedin.com/company/bhoc-therapeutics/" aria-label="BHOC Therapeutics on LinkedIn" title="LinkedIn" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M5.3 7.9H1.8V19h3.5V7.9ZM3.55 2.5A2.04 2.04 0 1 0 3.55 6.58 2.04 2.04 0 0 0 3.55 2.5ZM19 12.65c0-3.35-1.79-4.91-4.18-4.91-1.93 0-2.79 1.06-3.27 1.8V7.9H8.06V19h3.49v-5.5c0-1.45.27-2.86 2.08-2.86 1.78 0 1.8 1.67 1.8 2.96V19H19v-6.35Z"/></svg></a><a href="https://www.youtube.com/@BHOCTherapeutics" aria-label="BHOC Therapeutics on YouTube" title="YouTube @BHOCTherapeutics" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="5.5" width="19" height="13" rx="4" fill="currentColor"/><path d="m10 9 5.5 3-5.5 3Z" fill="white"/></svg></a></div>
            <a href="/bhoc/">What It Really Is. Why It Exists. →</a>
          </div>
          <div><strong>Science</strong><a href="/science/">Overview</a><a href="/science/">How It Works</a><a href="/evidence/library/concepts-hypotheses/">Concepts & Hypotheses ↗</a></div>
          <div><strong>Technology</strong><a href="/technology/">BHOC Platform</a><a href="/technology/">Design Principles</a></div>
          <div><strong>Applications</strong><a href="/applications/">Clinical Contexts</a><a href="https://bhocvet.com/">BHOC Veterinary</a></div>
          <div><strong>Company</strong><a href="/#company">About</a><a href="/news/">News</a><a href="/contact/">Contact</a></div>
          <div><strong>Investors & Partners</strong><a href="/partners/">Overview</a><a href="/partners/">Resources</a></div>
        </div>
        <div class="bhoc-shell-footer-bottom">First published 20 Aug 2026 · 79 updates · Last updated 08 Oct 2026 · Version 26.10.08 · <a href="https://bhocvet.com/">BHOC Veterinary</a> · <a href="https://bhoctherapeutics.com/evidence/library/">BHOC Information Hub</a><br>Scientific and educational website in development. References to Oxyglobin, Hemopure, HBOC and other third-party technologies are provided for scientific and historical context and do not imply ownership, affiliation or approved indications. © 2026 BHOC Therapeutics.</div>
      </div>`;
    return footer;
  }

  function init() {
    if (document.querySelector('.bhoc-shell-header')) return;
    const main = document.querySelector('main');
    const target = main || document.querySelector('h1') || document.body;
    if (!target.id) target.id = 'main-content';
    const legacyHeader = [...document.querySelectorAll('header')].find(el => !main?.contains(el));
    const legacyFooters = [...document.querySelectorAll('footer')].filter(el => !main?.contains(el));
    for (const oldSkip of document.querySelectorAll('a[href^="#"]')) {
      if (/^skip to (?:main |page )?content$/i.test(clean(oldSkip.textContent))) oldSkip.classList.add('bhoc-shell-old-skip');
    }
    const skip = makeLink('#' + target.id, 'Skip to content', 'bhoc-shell-skip');
    document.body.prepend(skip);
    const header = buildHeader();
    skip.after(header);
    const trail = buildTrail();
    if (trail) header.after(trail);
    const localNav = buildLocalNavigation(legacyHeader);
    if (localNav) (trail || header).after(localNav);
    if (legacyHeader) legacyHeader.classList.add('bhoc-shell-legacy');
    for (const oldTrail of document.querySelectorAll('nav[aria-label="Breadcrumb"], nav.bhoc-context-nav, nav[aria-label="Evidence hierarchy"], div.breadcrumb, div.crumbs')) {
      if (oldTrail !== trail && !oldTrail.closest('.bhoc-shell-header')) oldTrail.classList.add('bhoc-shell-old-trail');
    }
    for (const oldFooter of legacyFooters) oldFooter.classList.add('bhoc-shell-legacy');
    if (pagePath.startsWith(LIBRARY) && legacyFooters.length) {
      const notes = document.createElement('details');
      notes.className = 'bhoc-shell-page-notes bhoc-shell-wrap';
      const summary = document.createElement('summary');
      summary.textContent = 'Page sources and notes';
      notes.append(summary);
      for (const oldFooter of legacyFooters) {
        const copy = oldFooter.cloneNode(true);
        copy.classList.remove('bhoc-shell-legacy');
        notes.append(copy);
      }
      document.body.append(notes);
    }
    document.body.append(buildFooter());
    document.body.classList.add('bhoc-shell-ready');
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once: true});
  else init();
})();
