import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const hubPath = path.join(root, 'bhoc', 'index.html');
const navigationVersion = '202609163';
const authorityCssVersion = '202609164';
const socialImage = 'https://bhoctherapeutics.com/assets/bhoc-social-preview-20260905-initiative-logo.png';

const sections = [
  {
    number: '01',
    id: 'what-bhoc-detail',
    slug: 'what-is-bhoc',
    status: 'loaded',
    name: 'What is BHOC?',
    title: 'What Is BHOC? Biological Hemoglobin Oxygen Carrier',
    description: 'Learn the approved BHOC definition: how a Biological Hemoglobin Oxygen Carrier isolates oxygen-delivery function without claiming to replace every function of blood.',
    previous: null,
    next: '02'
  },
  {
    number: '02',
    id: 'why-bhoc',
    slug: 'why-bhoc',
    status: 'loaded',
    name: 'Why BHOC?',
    title: 'Why BHOC? From Blood Replacement to Oxygen Delivery',
    description: 'Understand why BHOC reframes the question from replacing blood as a whole to supporting oxygen-delivery function by physiology, context and evidence.',
    previous: '01',
    next: '03'
  },
  {
    number: '03',
    id: 'artificial-blood',
    slug: 'artificial-blood-blood-substitute',
    status: 'in-development',
    name: 'Artificial Blood & Blood Substitute',
    title: 'Artificial Blood & Blood Substitute | BHOC — In Development',
    description: 'BHOC section on artificial blood and blood-substitute history is currently in development.',
    previous: '02',
    next: '04'
  },
  {
    number: '04',
    id: 'natural-regulation',
    slug: 'oxygen-regulation',
    status: 'loaded',
    name: 'Oxygen Regulation',
    title: 'Oxygen Regulation: P50, RBC, Flow & Tissue | BHOC',
    description: 'Explore the approved BHOC framework for oxygen regulation across hemoglobin affinity, P50, red cells, circulation, microcirculation and tissue demand.',
    previous: '03',
    next: '05'
  },
  {
    number: '05',
    id: 'evolution-adaptation',
    slug: 'evolution-adaptation',
    status: 'in-development',
    name: 'Evolution & Adaptation',
    title: 'Evolution & Adaptation | BHOC — In Development',
    description: 'BHOC section on hemoglobin evolution, comparative oxygen biology and biological adaptation is currently in development.',
    previous: '04',
    next: '06'
  },
  {
    number: '06',
    id: 'outside-rbc',
    slug: 'hemoglobin-outside-red-blood-cell',
    status: 'loaded',
    name: 'Outside the RBC',
    title: 'Hemoglobin Outside the Red Blood Cell | BHOC',
    description: 'See what changes when hemoglobin leaves the red blood cell, including molecular size, oxidation, P50, nitric oxide interaction and microcirculatory behavior.',
    previous: '05',
    next: '07'
  },
  {
    number: '07',
    id: 'what-different',
    slug: 'what-makes-bhoc-different',
    status: 'loaded',
    name: 'What Makes BHOC Different?',
    title: 'What Makes BHOC Different? Function, Evidence & Design',
    description: 'Understand the BHOC function-first framework connecting biology, oxygen-delivery technology, product-specific physiology, evidence and application.',
    previous: '06',
    next: '08'
  },
  {
    number: '08',
    id: 'precision-oxygen',
    slug: 'precision-oxygen-therapeutics',
    status: 'loaded',
    name: 'Why We Exist',
    title: 'Precision Oxygen Therapeutics: Why BHOC Exists',
    description: 'Learn why BHOC defines Precision Oxygen Therapeutics by oxygen made available to tissue under the conditions where function is needed.',
    previous: '07',
    next: null
  }
];

const byNumber = new Map(sections.map(section => [section.number, section]));

function attributes(tag) {
  const values = {};
  for (const match of tag.matchAll(/([:\w-]+)\s*=\s*(["'])(.*?)\2/gs)) values[match[1]] = match[3];
  return values;
}

function extractSection(html, id) {
  const openingTags = /<section\b[^>]*>/gi;
  let opening;
  while ((opening = openingTags.exec(html))) {
    if (attributes(opening[0]).id !== id) continue;
    const start = opening.index;
    const sectionTags = /<\/?section\b[^>]*>/gi;
    sectionTags.lastIndex = start;
    let depth = 0;
    let token;
    while ((token = sectionTags.exec(html))) {
      if (/^<\/section/i.test(token[0])) depth -= 1;
      else depth += 1;
      if (depth === 0) return html.slice(start, sectionTags.lastIndex);
    }
  }
  throw new Error(`Missing source section #${id}`);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function loadedFragment(hub, section) {
  let fragment = extractSection(hub, section.id);
  fragment = fragment.replace(/\s*<p class="section-page-route">[\s\S]*?<\/p>/i, '');
  fragment = fragment.replace(/\s*<div class="chapter-nav">[\s\S]*?<\/div>\s*(?=<\/section>\s*$)/i, '\n');
  fragment = fragment.replace('<h2>', '<h1>').replace('</h2>', '</h1>');
  fragment = fragment.replaceAll('href="#bhoc-map"', 'href="/bhoc/#bhoc-map"');
  if (section.number === '04') {
    fragment = fragment.replace('href="#species-adaptation"', 'href="/bhoc/evolution-adaptation/"');
  }
  return fragment;
}

function developmentFragment(section) {
  const intro = section.number === '03'
    ? 'This section route is preserved. The full section remains in development pending scientific and historical review.'
    : 'This section route is preserved. The full section remains in development pending scientific review.';
  return `<section class="chapter" id="${section.id}" data-bhoc-status="in-development">
    <div class="chapter-header"><div class="chapter-no">${section.number}</div><div><p class="eyebrow">Understand BHOC</p><h1>${escapeHtml(section.name)}</h1><p class="chapter-intro">${intro}</p><span class="section-status is-development">In development</span></div></div>
    <div class="key-idea"><small>Status</small><p>No previously approved BHOC content has been removed. This dedicated page will be completed only after review.</p></div>
  </section>`;
}

function sequenceLink(number, direction) {
  if (!number) return '';
  const target = byNumber.get(number);
  const arrow = direction === 'previous' ? '← ' : ' →';
  const label = `${target.number} · ${target.name}`;
  return `<a href="/bhoc/${target.slug}/">${direction === 'previous' ? arrow : ''}${escapeHtml(label)}${direction === 'next' ? arrow : ''}</a>`;
}

function sequenceNav(section) {
  return `<nav class="chapter-nav section-page-sequence" aria-label="BHOC section sequence">
    ${sequenceLink(section.previous, 'previous')}
    <a href="/bhoc/#bhoc-map">↑ Back to BHOC map</a>
    ${sequenceLink(section.next, 'next')}
  </nav>`;
}

function structuredData(section, canonical) {
  return JSON.stringify({
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebPage',
        '@id': `${canonical}#webpage`,
        url: canonical,
        name: section.title,
        description: section.description,
        isPartOf: {'@type': 'WebSite', name: 'BHOC Therapeutics', url: 'https://bhoctherapeutics.com/'},
        author: {'@type': 'Person', name: 'Archil Jaliashvili', url: 'https://bhoctherapeutics.com/archil-jaliashvili/'},
        dateModified: '2026-09-16'
      },
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          {'@type': 'ListItem', position: 1, name: 'BHOC Therapeutics', item: 'https://bhoctherapeutics.com/'},
          {'@type': 'ListItem', position: 2, name: 'Understand BHOC', item: 'https://bhoctherapeutics.com/bhoc/'},
          {'@type': 'ListItem', position: 3, name: section.name, item: canonical}
        ]
      }
    ]
  });
}

function pageHtml(hub, section) {
  const canonical = `https://bhoctherapeutics.com/bhoc/${section.slug}/`;
  const robots = section.status === 'loaded'
    ? 'index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1'
    : 'noindex,nofollow';
  const content = section.status === 'loaded' ? loadedFragment(hub, section) : developmentFragment(section);
  const detailControls = section.number === '04'
    ? "const scienceDetails=[...document.querySelectorAll('#natural-regulation .science-detail')];document.querySelector('[data-science-details=\"open\"]')?.addEventListener('click',()=>scienceDetails.forEach(detail=>detail.open=true));document.querySelector('[data-science-details=\"close\"]')?.addEventListener('click',()=>scienceDetails.forEach(detail=>detail.open=false));"
    : '';
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${escapeHtml(section.title)}</title>
  <meta name="description" content="${escapeHtml(section.description)}">
  <meta name="author" content="Archil Jaliashvili">
  <meta name="robots" content="${robots}">
  <meta name="yandex" content="noindex">
  <link rel="canonical" href="${canonical}">
  <meta property="og:site_name" content="BHOC Therapeutics">
  <meta property="og:locale" content="en_US">
  <meta property="og:type" content="website">
  <meta property="og:title" content="${escapeHtml(section.title)}">
  <meta property="og:description" content="${escapeHtml(section.description)}">
  <meta property="og:url" content="${canonical}">
  <meta property="og:image" content="${socialImage}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="BHOC - Biological Hemoglobin Oxygen Carrier and Precision Oxygen Therapeutics">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${escapeHtml(section.title)}">
  <meta name="twitter:description" content="${escapeHtml(section.description)}">
  <meta name="twitter:image" content="${socialImage}">
  <meta name="theme-color" content="#ffffff">
  <link rel="stylesheet" href="/inner-visual.css?v=202609058">
  <link rel="stylesheet" href="/site-header.css?v=202609082">
  <link rel="stylesheet" href="/bhoc/bhoc-authority.css?v=${authorityCssVersion}">
  <script type="application/ld+json">${structuredData(section, canonical)}</script>
  <script src="/navigation-context.js?v=${navigationVersion}" defer></script>
</head>
<body class="bhoc-child-page${section.status === 'in-development' ? ' is-development' : ''}">
<header class="home-header"><div class="home-wrap home-nav"><a class="home-logo" href="/" aria-label="BHOC Therapeutics home"><span><b>BH<span class="logo-o">O</span>C</b><small>THERAPEUTICS</small></span></a><nav class="home-links" id="home-nav" aria-label="Primary navigation"><a href="/science/">Science</a><a href="/technology/">Technology</a><a href="/applications/">Applications</a><a href="/evidence/">Evidence</a><a href="https://archiljali.github.io/BHOC-platform/concepts-hypotheses/" target="_blank" rel="noopener noreferrer">Concepts &amp; Hypotheses ↗</a><a href="/news/">News</a><a href="/#company">Company</a><a href="/partners/">Investors &amp; Partners</a><a href="mailto:info@bhoctherapeutics.com">Contact</a></nav><button class="home-menu" type="button" aria-label="Open navigation" aria-controls="home-nav" aria-expanded="false">☰</button></div></header>
<div class="bhoc-guide"><div class="home-wrap bhoc-guide-inner"><span class="bhoc-guide-label">Understand BHOC</span><a href="/bhoc/"><strong>BHOC - What It Really Is.</strong><span>Why It Exists.</span><b>→</b></a></div></div>
<div class="brand-network"><div class="brand-network-inner" role="group" aria-label="BHOC websites"><span class="brand-network-title">BHOC NETWORK</span><a class="brand-network-link" href="https://archiljali.github.io/BHOC-platform/" target="_blank" rel="noopener noreferrer" aria-label="Open BHOC Scientific Evidence Hub">Scientific Evidence Hub ↗</a><a class="brand-network-link" href="https://bhocvet.com/" aria-label="Open BHOC Veterinary website"><span class="vet-wordmark">BH<span class="vet-o">O</span>C</span> Veterinary <small>bhocvet.com</small></a><span class="brand-network-link brand-network-pending" aria-disabled="true" title="Coming soon">BHOC Transplant <small>coming soon</small></span></div></div>
<main class="bhoc-page bhoc-section-detail">
  <nav class="bhoc-crumbs" aria-label="Breadcrumb"><a href="/">BHOC Therapeutics</a><span>›</span><a href="/bhoc/">Understand BHOC</a><span>›</span><strong>${escapeHtml(section.name)}</strong></nav>
  ${content}
  ${sequenceNav(section)}
</main>
<footer><div class="footer-brand">BHOC THERAPEUTICS</div><p>Precision Oxygen Therapeutics</p><p><a href="/">Home</a> · <a href="/bhoc/">BHOC</a> · <a href="/science/">Science</a> · <a href="/technology/">Technology</a> · <a href="/applications/">Applications</a> · <a href="/evidence/">Evidence</a> · <a href="https://archiljali.github.io/BHOC-platform/concepts-hypotheses/" target="_blank" rel="noopener">Concepts &amp; Hypotheses ↗</a> · <a href="/news/">News</a> · <a href="/partners/">Investors &amp; Partners</a> · <a href="https://archiljali.github.io/BHOC-platform/" target="_blank" rel="noopener noreferrer">BHOC-platform ↗</a> · <a href="mailto:info@bhoctherapeutics.com">Contact</a></p><p class="legal">Scientific and educational website in development. References to Oxyglobin, Hemopure, HBOC, Biopure or other third-party technologies are provided for scientific and historical context and do not imply ownership, affiliation or approved indications.</p><p class="version">Section ${section.number} · ${section.status === 'loaded' ? 'Approved content' : 'In development'} · Updated 16 Sep 2026</p><p class="copyright">© 2026 BHOC Therapeutics.</p></footer>
<script>const homeMenu=document.querySelector('.home-menu');const homeNav=document.getElementById('home-nav');if(homeMenu&&homeNav){homeMenu.addEventListener('click',()=>{const open=homeNav.classList.toggle('open');homeMenu.setAttribute('aria-expanded',String(open));homeMenu.setAttribute('aria-label',open?'Close navigation':'Open navigation')});document.querySelectorAll('.home-links a').forEach(a=>a.addEventListener('click',()=>{homeNav.classList.remove('open');homeMenu.setAttribute('aria-expanded','false');homeMenu.setAttribute('aria-label','Open navigation')}));}${detailControls}</script>
</body>
</html>
`;
}

const hub = await fs.readFile(hubPath, 'utf8');
for (const section of sections) {
  const directory = path.join(root, 'bhoc', section.slug);
  await fs.mkdir(directory, {recursive: true});
  await fs.writeFile(path.join(directory, 'index.html'), pageHtml(hub, section));
  console.log(`Generated /bhoc/${section.slug}/`);
}
