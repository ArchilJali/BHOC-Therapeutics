import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const hubPath = path.join(root, 'bhoc', 'index.html');
const draftPath = path.join(root, 'bhoc', 'artificial-blood-blood-substitute', 'index.html');
const baselinePath = path.join(root, 'bhoc', 'content-baseline.json');
const sitemapPath = path.join(root, 'sitemap.xml');
const authorityCssPath = path.join(root, 'bhoc', 'bhoc-authority.css');

const protectedSections = [
  ['what-bhoc', 'Overview'],
  ['bhoc-map', 'Knowledge map'],
  ['knowledge-updates', 'Knowledge updates'],
  ['what-bhoc-detail', '01 What is BHOC'],
  ['why-bhoc', '02 Why BHOC'],
  ['natural-regulation', '04 Oxygen regulation'],
  ['evolution-adaptation', '05 Evolution and adaptation'],
  ['outside-rbc', '06 Outside the RBC'],
  ['what-different', '07 BHOC difference'],
  ['resources', 'Resources'],
  ['precision-oxygen', '08 Precision Oxygen Therapeutics']
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

const [hub, draft, sitemap, authorityCss] = await Promise.all([
  fs.readFile(hubPath, 'utf8'),
  fs.readFile(draftPath, 'utf8'),
  fs.readFile(sitemapPath, 'utf8'),
  fs.readFile(authorityCssPath, 'utf8')
]);

const sections = Object.fromEntries(protectedSections.map(([id, label]) => {
  const fragment = extractSection(hub, id);
  if (!fragment) throw new Error(`Missing protected section ${label} (#${id})`);
  return [id, record(fragment)];
}));
const snapshot = {
  sourceCommit: 'f223aea4d24286df85190b4a6a91b8963ad438bb',
  architecture: 'continuous-morning-hub',
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

const map = extractSection(hub, 'bhoc-map') || '';
const mapNumbers = [...map.matchAll(/<span\b[^>]*class=(["'])num\1[^>]*>(.*?)<\/span>/gi)].map(match => visibleText(match[2]));
if (JSON.stringify(mapNumbers) !== JSON.stringify(['01', '02', '04', '05', '06', '07', '08'])) errors.push(`Published map is ${mapNumbers.join(', ')}; expected 01, 02, 04, 05, 06, 07, 08`);

if (/id=(["'])artificial-blood\1/i.test(hub)) errors.push('Artificial Blood section is exposed in the hub');
if (/href=(["'])#artificial-blood\1/i.test(hub)) errors.push('Artificial Blood route is exposed in the hub');
if (robotsValue(draft) !== 'noindex,nofollow') errors.push('Artificial Blood draft must remain noindex,nofollow');
if (!visibleText(draft).includes('In development')) errors.push('Artificial Blood direct route must show only its draft status');
if (sitemap.includes('/bhoc/artificial-blood-blood-substitute/')) errors.push('Artificial Blood draft must not be in the sitemap');
if (authorityCss.includes('#evolution-adaptation>p') || authorityCss.includes('#evolution-adaptation .chapter-intro{font-size:0}')) errors.push('05 Evolution and adaptation must remain fully visible');
if (!authorityCss.includes('.map-card[href="#evolution-adaptation"]:after{content:"Loaded 15 Sep 2026"}')) errors.push('05 Evolution and adaptation must remain marked as loaded');

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

console.log('BHOC content protection check passed: morning hub preserved, 01/02 and 04–08 visible, only Artificial Blood closed.');
