import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const hubPath = path.join(root, 'bhoc', 'index.html');
const draftPath = path.join(root, 'bhoc', 'artificial-blood-blood-substitute', 'index.html');
const baselinePath = path.join(root, 'bhoc', 'content-baseline.json');
const sitemapPath = path.join(root, 'sitemap.xml');

const protectedSections = [
  ['bhoc-overview', 'BHOC overview'],
  ['why-bhoc', 'Why BHOC'],
  ['terminology', 'Terminology'],
  ['hemoglobin-system', 'Hemoglobin system'],
  ['molecular-core', 'Molecular core'],
  ['erythrocyte-system', 'Erythrocyte system'],
  ['circulation-control', 'Circulation control'],
  ['tissue-control', 'Tissue control'],
  ['species-adaptation', 'Species adaptation'],
  ['human-variation', 'Human variation'],
  ['evidence-map', 'Evidence map'],
  ['history', 'Historical evolution']
];

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
      depth += /^<\/section/i.test(token[0]) ? -1 : 1;
      if (depth === 0) return html.slice(start, sectionTags.lastIndex);
    }
  }
  return null;
}

function record(fragment) {
  const text = visibleText(fragment);
  const links = [...fragment.matchAll(/<a\b[^>]*\bhref\s*=\s*(["'])(.*?)\1/gi)].map(match => decodeEntities(match[2]));
  return {
    textCharacters: text.length,
    textSha256: sha256(text),
    linksSha256: sha256(links.join('\n'))
  };
}

function robotsValue(html) {
  return html.match(/<meta\b[^>]*name\s*=\s*(["'])robots\1[^>]*content\s*=\s*(["'])(.*?)\2/i)?.[3]
    || html.match(/<meta\b[^>]*content\s*=\s*(["'])(.*?)\1[^>]*name\s*=\s*(["'])robots\3/i)?.[2]
    || '';
}

const [hub, sitemap] = await Promise.all([
  fs.readFile(hubPath, 'utf8'),
  fs.readFile(sitemapPath, 'utf8')
]);

const sections = Object.fromEntries(protectedSections.map(([id, label]) => {
  const fragment = extractSection(hub, id);
  if (!fragment) throw new Error(`Missing protected section ${label} (#${id})`);
  return [id, record(fragment)];
}));
const snapshot = {
  sourceCommit: '64c32a80720d7a82bfd488ad9c5d89a624819614',
  architecture: 'restored-2026-09-15-0942-hub',
  sections
};

if (process.argv.includes('--snapshot')) {
  console.log(JSON.stringify(snapshot, null, 2));
  process.exit(0);
}

const baseline = JSON.parse(await fs.readFile(baselinePath, 'utf8'));
const errors = [];

for (const [id, label] of protectedSections) {
  const actual = snapshot.sections[id];
  const expected = baseline.sections?.[id];
  if (!expected) {
    errors.push(`${label}: missing from baseline`);
    continue;
  }
  if (actual.textSha256 !== expected.textSha256) errors.push(`${label}: approved text changed`);
  if (actual.linksSha256 !== expected.linksSha256) errors.push(`${label}: approved links changed`);
  if (actual.textCharacters < expected.textCharacters) errors.push(`${label}: content became shorter`);
}

const subnav = hub.match(/<nav\b[^>]*class=(["'])bhoc-subnav\1[^>]*>[\s\S]*?<\/nav>/i)?.[0] || '';
const subnavTargets = [...subnav.matchAll(/<a\b[^>]*href=(["'])#([^"']+)\1/gi)].map(match => match[2]);
const expectedTargets = ['history', ...protectedSections.map(([id]) => id).filter(id => id !== 'history')];
if (JSON.stringify(subnavTargets) !== JSON.stringify(expectedTargets)) errors.push(`BHOC subnavigation is ${subnavTargets.join(', ')}; expected ${expectedTargets.join(', ')}`);

if (/href=(["'])\/bhoc\/artificial-blood-blood-substitute\/?\1/i.test(hub)) errors.push('Artificial Blood direct route is exposed in the hub');
try {
  await fs.access(draftPath);
  errors.push('Artificial Blood direct page must remain unpublished');
} catch (error) {
  if (error?.code !== 'ENOENT') errors.push(`Unable to verify Artificial Blood page status: ${error.message}`);
}
if (sitemap.includes('/bhoc/artificial-blood-blood-substitute/')) errors.push('Artificial Blood draft must not be in the sitemap');

const ids = new Set([...hub.matchAll(/\bid\s*=\s*(["'])(.*?)\1/gi)].map(match => decodeEntities(match[2])));
const missingFragments = [...new Set([...hub.matchAll(/<a\b[^>]*\bhref\s*=\s*(["'])#([^"']+)\1/gi)]
  .map(match => decodeEntities(match[2]))
  .filter(fragment => fragment !== 'top' && !ids.has(fragment)))];
if (missingFragments.length) errors.push(`Missing local fragment targets: ${missingFragments.map(fragment => `#${fragment}`).join(', ')}`);

if (errors.length) {
  console.error('BHOC CONTENT PROTECTION CHECK FAILED');
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log('BHOC content protection check passed: exact 15 Sep 2026 09:42 hub preserved and the Artificial Blood direct page remains unpublished.');
