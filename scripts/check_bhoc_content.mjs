import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const pagePath = path.join(root, 'bhoc', 'index.html');
const baselinePath = path.join(root, 'bhoc', 'content-baseline.json');
const authorityCssPath = path.join(root, 'bhoc', 'bhoc-authority.css');
const navigationPath = path.join(root, 'navigation-context.js');
const sitemapPath = path.join(root, 'sitemap.xml');

const sectionSpecs = [
  {number: '01', id: 'what-bhoc-detail', slug: 'what-is-bhoc', status: 'loaded'},
  {number: '02', id: 'why-bhoc', slug: 'why-bhoc', status: 'loaded'},
  {number: '03', id: 'artificial-blood', slug: 'artificial-blood-blood-substitute', status: 'in-development'},
  {number: '04', id: 'natural-regulation', slug: 'oxygen-regulation', status: 'loaded'},
  {number: '05', id: 'evolution-adaptation', slug: 'evolution-adaptation', status: 'in-development'},
  {number: '06', id: 'outside-rbc', slug: 'hemoglobin-outside-red-blood-cell', status: 'loaded'},
  {number: '07', id: 'what-different', slug: 'what-makes-bhoc-different', status: 'loaded'},
  {number: '08', id: 'precision-oxygen', slug: 'precision-oxygen-therapeutics', status: 'loaded'}
];

const auxiliarySectionIds = ['knowledge-updates', 'resources'];
const expandedDetailIds = ['molecular-core', 'erythrocyte-system', 'circulation-control', 'tissue-control'];

const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');

function decodeEntities(value) {
  return value
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"')
    .replace(/&#39;|&apos;/gi, "'")
    .replace(/&#(\d+);/g, (_match, code) => String.fromCodePoint(Number(code)))
    .replace(/&#x([\da-f]+);/gi, (_match, code) => String.fromCodePoint(Number.parseInt(code, 16)));
}

function visibleText(fragment) {
  return decodeEntities(fragment
    .replace(/<!--[\s\S]*?-->/g, ' ')
    .replace(/<script\b[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style\b[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' '))
    .replace(/\s+/g, ' ')
    .trim();
}

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
  return null;
}

function sectionRecord(html, spec) {
  const fragment = extractSection(html, spec.id);
  if (!fragment) throw new Error(`Missing protected section #${spec.id}`);
  const openingTag = fragment.match(/^<section\b[^>]*>/i)?.[0] || '';
  const status = attributes(openingTag)['data-bhoc-status'] || '';
  const text = visibleText(fragment);
  const links = [...fragment.matchAll(/<a\b[^>]*\bhref\s*=\s*(["'])(.*?)\1/gi)].map(match => decodeEntities(match[2]));
  return {
    number: spec.number,
    status,
    textCharacters: text.length,
    textSha256: sha256(text),
    links,
    linksSha256: sha256(links.join('\n'))
  };
}

function auxiliarySectionRecord(html, id) {
  const fragment = extractSection(html, id);
  if (!fragment) throw new Error(`Missing protected supporting section #${id}`);
  const text = visibleText(fragment);
  const links = [...fragment.matchAll(/<a\b[^>]*\bhref\s*=\s*(["'])(.*?)\1/gi)].map(match => decodeEntities(match[2]));
  return {
    textCharacters: text.length,
    textSha256: sha256(text),
    links,
    linksSha256: sha256(links.join('\n'))
  };
}

function expandedDetailRecords(html) {
  const records = {};
  for (const id of expandedDetailIds) {
    const openingTag = [...html.matchAll(/<details\b[^>]*>/gi)].map(match => match[0]).find(tag => attributes(tag).id === id) || '';
    records[id] = Boolean(openingTag && /\sopen(?:\s|>|=)/i.test(openingTag));
  }
  return records;
}

function mapRecords(html) {
  const fragment = extractSection(html, 'bhoc-map');
  if (!fragment) throw new Error('Missing protected section #bhoc-map');
  return [...fragment.matchAll(/<a\b[^>]*class\s*=\s*(["'])[^"']*\bmap-card\b[^"']*\1[^>]*>[\s\S]*?<\/a>/gi)].map(match => {
    const openingTag = match[0].match(/^<a\b[^>]*>/i)?.[0] || '';
    const attrs = attributes(openingTag);
    const number = visibleText(match[0].match(/<span\b[^>]*class\s*=\s*(["'])num\1[^>]*>[\s\S]*?<\/span>/i)?.[0] || '');
    return {number, href: attrs.href || '', status: attrs['data-bhoc-status'] || ''};
  });
}

function robotsValue(html) {
  return html.match(/<meta\b[^>]*name\s*=\s*(["'])robots\1[^>]*content\s*=\s*(["'])(.*?)\2/i)?.[3]
    || html.match(/<meta\b[^>]*content\s*=\s*(["'])(.*?)\1[^>]*name\s*=\s*(["'])robots\3/i)?.[2]
    || '';
}

function sectionCore(fragment) {
  return fragment
    .replace(/\s*<p\b[^>]*class\s*=\s*(["'])[^"']*\bsection-page-route\b[^"']*\1[^>]*>[\s\S]*?<\/p>/gi, '')
    .replace(/\s*<div\b[^>]*class\s*=\s*(["'])[^"']*\bchapter-nav\b[^"']*\1[^>]*>[\s\S]*?<\/div>/gi, '');
}

function normalizeSectionLink(link, spec) {
  if (link === '#bhoc-map') return '/bhoc/#bhoc-map';
  if (spec.number === '04' && link === '#species-adaptation') return '/bhoc/evolution-adaptation/';
  return link;
}

function sectionPageRecord(html, spec) {
  const route = `/bhoc/${spec.slug}/`;
  const fragment = extractSection(html, spec.id);
  if (!fragment) throw new Error(`Missing dedicated page section #${spec.id} at ${route}`);
  const openingTag = fragment.match(/^<section\b[^>]*>/i)?.[0] || '';
  const core = sectionCore(fragment);
  const coreText = visibleText(core);
  const coreLinks = [...core.matchAll(/<a\b[^>]*\bhref\s*=\s*(["'])(.*?)\1/gi)]
    .map(match => normalizeSectionLink(decodeEntities(match[2]), spec));
  const canonical = html.match(/<link\b[^>]*rel\s*=\s*(["'])canonical\1[^>]*href\s*=\s*(["'])(.*?)\2/i)?.[3]
    || html.match(/<link\b[^>]*href\s*=\s*(["'])(.*?)\1[^>]*rel\s*=\s*(["'])canonical\3/i)?.[2]
    || '';
  return {
    path: route,
    status: attributes(openingTag)['data-bhoc-status'] || '',
    robots: robotsValue(html),
    canonical,
    h1Count: [...html.matchAll(/<h1\b/gi)].length,
    textCharacters: coreText.length,
    textSha256: sha256(coreText),
    links: coreLinks,
    linksSha256: sha256(coreLinks.join('\n'))
  };
}

function hubCoreRecord(html, spec) {
  const fragment = extractSection(html, spec.id);
  if (!fragment) throw new Error(`Missing protected hub section #${spec.id}`);
  const core = sectionCore(fragment);
  const text = visibleText(core);
  const links = [...core.matchAll(/<a\b[^>]*\bhref\s*=\s*(["'])(.*?)\1/gi)]
    .map(match => normalizeSectionLink(decodeEntities(match[2]), spec));
  return {textCharacters: text.length, textSha256: sha256(text), links, linksSha256: sha256(links.join('\n'))};
}

const page = await fs.readFile(pagePath, 'utf8');
const authorityCss = await fs.readFile(authorityCssPath, 'utf8');
const navigation = await fs.readFile(navigationPath, 'utf8');
const sitemap = await fs.readFile(sitemapPath, 'utf8');
const sectionPageSources = Object.fromEntries(await Promise.all(sectionSpecs.map(async spec => [
  spec.id,
  await fs.readFile(path.join(root, 'bhoc', spec.slug, 'index.html'), 'utf8')
])));
const snapshot = {
  sections: Object.fromEntries(sectionSpecs.map(spec => [spec.id, sectionRecord(page, spec)])),
  auxiliarySections: Object.fromEntries(auxiliarySectionIds.map(id => [id, auxiliarySectionRecord(page, id)])),
  expandedDetails: expandedDetailRecords(page),
  map: mapRecords(page),
  sectionPages: Object.fromEntries(sectionSpecs.map(spec => [spec.id, sectionPageRecord(sectionPageSources[spec.id], spec)])),
  navigationScopedToBhoc: navigation.includes('if (!isBhocSection) return;')
};

if (process.argv.includes('--snapshot')) {
  console.log(JSON.stringify(snapshot, null, 2));
  process.exit(0);
}

const baseline = JSON.parse(await fs.readFile(baselinePath, 'utf8'));
const errors = [];

for (const spec of sectionSpecs) {
  const expected = baseline.sections?.[spec.id];
  const actual = snapshot.sections[spec.id];
  if (!expected) {
    errors.push(`#${spec.id}: missing from content baseline`);
    continue;
  }
  if (actual.status !== spec.status || actual.status !== expected.status) errors.push(`#${spec.id}: status ${actual.status || '(missing)'}; expected ${expected.status}`);
  if (actual.textSha256 !== expected.textSha256) errors.push(`#${spec.id}: approved text changed`);
  if (actual.linksSha256 !== expected.linksSha256) errors.push(`#${spec.id}: approved links changed`);
  if (actual.textCharacters < expected.textCharacters) errors.push(`#${spec.id}: text became shorter (${actual.textCharacters} < ${expected.textCharacters})`);
}

for (const id of auxiliarySectionIds) {
  const expected = baseline.auxiliarySections?.[id];
  const actual = snapshot.auxiliarySections[id];
  if (!expected) {
    errors.push(`#${id}: missing from supporting-content baseline`);
    continue;
  }
  if (actual.textSha256 !== expected.textSha256) errors.push(`#${id}: approved supporting text changed`);
  if (actual.linksSha256 !== expected.linksSha256) errors.push(`#${id}: approved supporting links changed`);
  if (actual.textCharacters < expected.textCharacters) errors.push(`#${id}: supporting text became shorter (${actual.textCharacters} < ${expected.textCharacters})`);
}

if (JSON.stringify(snapshot.expandedDetails) !== JSON.stringify(baseline.expandedDetails)) errors.push('Approved scientific detail visibility changed');
if (!snapshot.navigationScopedToBhoc || snapshot.navigationScopedToBhoc !== baseline.navigationScopedToBhoc) errors.push('Expanded route interface is no longer limited to BHOC pages');

for (const spec of sectionSpecs.filter(item => item.status === 'loaded')) {
  const hiddenRule = new RegExp(`#${spec.id}[^{}]*\\{[^}]*display\\s*:\\s*none`, 'i');
  if (hiddenRule.test(authorityCss)) errors.push(`#${spec.id}: loaded content is hidden by CSS`);
}

if (JSON.stringify(snapshot.map) !== JSON.stringify(baseline.map)) errors.push('BHOC map routes or completion statuses changed');

for (const [index, spec] of sectionSpecs.entries()) {
  const expected = baseline.sectionPages?.[spec.id];
  const actual = snapshot.sectionPages[spec.id];
  const source = sectionPageSources[spec.id];
  const route = `/bhoc/${spec.slug}/`;
  const canonical = `https://bhoctherapeutics.com${route}`;
  if (!expected) {
    errors.push(`${route}: missing from dedicated-page baseline`);
    continue;
  }
  if (actual.path !== expected.path || actual.path !== route) errors.push(`${route}: dedicated page route changed`);
  if (actual.status !== expected.status || actual.status !== spec.status) errors.push(`${route}: status ${actual.status || '(missing)'}; expected ${spec.status}`);
  if (actual.robots !== expected.robots) errors.push(`${route}: robots policy changed (${actual.robots || '(missing)'})`);
  if (actual.canonical !== canonical) errors.push(`${route}: canonical route is ${actual.canonical || '(missing)'}`);
  if (actual.h1Count !== 1) errors.push(`${route}: expected exactly one H1, found ${actual.h1Count}`);
  if (!page.includes(`href="${route}"`) && !page.includes(`href='${route}'`)) errors.push(`${route}: hub link is missing`);
  if (!navigation.includes(`path: '${route}'`)) errors.push(`${route}: top route navigation mapping is missing`);
  if (!source.includes('href="/bhoc/#bhoc-map"')) errors.push(`${route}: return to BHOC map is missing`);

  const sitemapHasRoute = sitemap.includes(`<loc>${canonical}</loc>`);
  if (spec.status === 'loaded') {
    const hubCore = hubCoreRecord(page, spec);
    if (actual.textSha256 !== hubCore.textSha256 || actual.textCharacters !== hubCore.textCharacters) errors.push(`${route}: full approved section text is not synchronized with the hub`);
    if (actual.linksSha256 !== hubCore.linksSha256) errors.push(`${route}: approved section links are not synchronized with the hub`);
    if (!/^index,follow/i.test(actual.robots)) errors.push(`${route}: loaded page must be indexable`);
    if (!sitemapHasRoute) errors.push(`${route}: loaded page is missing from sitemap`);
  } else {
    if (actual.robots !== 'noindex,nofollow') errors.push(`${route}: in-development page must remain noindex,nofollow`);
    if (sitemapHasRoute) errors.push(`${route}: in-development page must not be in sitemap`);
  }

  const previous = sectionSpecs[index - 1];
  const next = sectionSpecs[index + 1];
  if (previous && !source.includes(`href="/bhoc/${previous.slug}/"`)) errors.push(`${route}: previous-section route is missing`);
  if (next && !source.includes(`href="/bhoc/${next.slug}/"`)) errors.push(`${route}: next-section route is missing`);
}

for (const route of baseline.requiredRoutes || []) {
  if (!page.includes(`href="${route}"`) && !page.includes(`href='${route}'`)) errors.push(`Required route is missing: ${route}`);
}

for (const phrase of baseline.requiredApprovedText || []) {
  if (!visibleText(page).includes(phrase)) errors.push(`Required approved text is missing: ${phrase}`);
}

if (errors.length) {
  console.error('BHOC CONTENT PRESERVATION CHECK FAILED');
  for (const error of errors) console.error(`- ${error}`);
  console.error('Do not update bhoc/content-baseline.json unless the user explicitly approved each content/status change.');
  process.exit(1);
}

console.log(`BHOC content preservation check passed: ${sectionSpecs.length} hub sections, ${snapshot.map.length} dedicated routes, statuses and full-page content protected.`);
