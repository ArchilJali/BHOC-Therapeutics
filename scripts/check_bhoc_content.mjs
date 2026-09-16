import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const pagePath = path.join(root, 'bhoc', 'index.html');
const childPath = path.join(root, 'bhoc', 'artificial-blood-blood-substitute', 'index.html');
const baselinePath = path.join(root, 'bhoc', 'content-baseline.json');
const authorityCssPath = path.join(root, 'bhoc', 'bhoc-authority.css');
const navigationPath = path.join(root, 'navigation-context.js');

const sectionSpecs = [
  {number: '01', id: 'what-bhoc-detail', status: 'loaded'},
  {number: '02', id: 'why-bhoc', status: 'loaded'},
  {number: '03', id: 'artificial-blood', status: 'in-development'},
  {number: '04', id: 'natural-regulation', status: 'loaded'},
  {number: '05', id: 'evolution-adaptation', status: 'in-development'},
  {number: '06', id: 'outside-rbc', status: 'loaded'},
  {number: '07', id: 'what-different', status: 'loaded'},
  {number: '08', id: 'precision-oxygen', status: 'loaded'}
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

function childRecord(html) {
  const robots = html.match(/<meta\b[^>]*name\s*=\s*(["'])robots\1[^>]*content\s*=\s*(["'])(.*?)\2/i)?.[3]
    || html.match(/<meta\b[^>]*content\s*=\s*(["'])(.*?)\1[^>]*name\s*=\s*(["'])robots\3/i)?.[2]
    || '';
  const fragment = extractSection(html, 'artificial-blood');
  if (!fragment) throw new Error('Missing protected child-page section #artificial-blood');
  const openingTag = fragment.match(/^<section\b[^>]*>/i)?.[0] || '';
  return {robots, status: attributes(openingTag)['data-bhoc-status'] || ''};
}

const page = await fs.readFile(pagePath, 'utf8');
const child = await fs.readFile(childPath, 'utf8');
const authorityCss = await fs.readFile(authorityCssPath, 'utf8');
const navigation = await fs.readFile(navigationPath, 'utf8');
const snapshot = {
  sections: Object.fromEntries(sectionSpecs.map(spec => [spec.id, sectionRecord(page, spec)])),
  auxiliarySections: Object.fromEntries(auxiliarySectionIds.map(id => [id, auxiliarySectionRecord(page, id)])),
  expandedDetails: expandedDetailRecords(page),
  map: mapRecords(page),
  childPage: childRecord(child),
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
if (JSON.stringify(snapshot.childPage) !== JSON.stringify(baseline.childPage)) errors.push('Artificial Blood child-page status or robots policy changed');

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

console.log(`BHOC content preservation check passed: ${sectionSpecs.length} sections, ${snapshot.map.length} map routes, child-page status protected.`);
