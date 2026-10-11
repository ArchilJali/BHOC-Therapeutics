import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const version = '20261011-shell3';
const release = JSON.parse(await fs.readFile(path.join(root, 'site-release.json'), 'utf8'));
const releaseSummary = `First published ${release.first_published} · ${release.updates} updates · Last updated ${release.updated} · Version ${release.version}`;
const shellPath = path.join(root, 'unified-shell.js');
const shellSource = await fs.readFile(shellPath, 'utf8');
await fs.writeFile(shellPath, shellSource.replace(/const releaseSummary = '[^']+';/, `const releaseSummary = '${releaseSummary}';`));
await fs.writeFile(path.join(root, 'evidence/library/version.json'), JSON.stringify(release, null, 2) + '\n');
const evidenceLinks = `<nav class="bhoc-evidence-links" aria-label="Explore BHOC evidence and history" data-bhoc-evidence-links><div class="bhoc-shell-wrap"><a href="/evidence/library/">Evidence Library</a><a href="/evidence/library/veterinary/Vet-index.html">Veterinary</a><a href="/evidence/library/human/BHOC-Human-index.html">Human Use</a><a href="/evidence/library/transplant/Transplant-index.html">Transplantation</a><a href="/evidence/library/science/">Science</a><a href="/evidence/library/catalogues/product.html">Oxyglobin &amp; Hemopure</a><a href="/evidence/library/catalogues/oxygen.html">Oxygen &amp; Microcirculation</a><a href="/evidence/library/catalogues/related.html">Related Articles</a><a href="/evidence/library/historical-sources/">Historical Sources</a><a href="/news/knowledge-updates/">What’s new</a></div></nav>`;
const headTags = `<link rel="stylesheet" href="/unified-shell.css?v=${version}">\n<script src="/unified-shell.js?v=${version}" defer></script>`;
const skipDirs = new Set(['.git', '.github', 'assets', 'scripts', 'preview', 'node_modules', 'seo', '_includes']);

async function files(dir) {
  const result = [];
  for (const entry of await fs.readdir(dir, {withFileTypes: true})) {
    if (entry.isDirectory()) {
      if (!skipDirs.has(entry.name)) result.push(...await files(path.join(dir, entry.name)));
    } else if (/\.html?$/i.test(entry.name)) result.push(path.join(dir, entry.name));
  }
  return result;
}

let changed = 0;
for (const file of await files(root)) {
  const relative = path.relative(root, file).replaceAll('\\', '/');
  if (relative === '404.html' || relative.startsWith('preview-')) continue;
  const source = await fs.readFile(file, 'utf8');
  if (/<meta\b[^>]*name=["']robots["'][^>]*content=["'][^"']*noindex/i.test(source) ||
      /<meta\b[^>]*content=["'][^"']*noindex[^"']*["'][^>]*name=["']robots/i.test(source)) continue;
  if (!/<\/head>/i.test(source) || !/<body\b/i.test(source)) continue;
  let next = source.replace(/<link\b[^>]*href=["']\/unified-shell\.css(?:\?[^"']*)?["'][^>]*>\s*/gi, '')
    .replace(/<script\b[^>]*src=["']\/unified-shell\.js(?:\?[^"']*)?["'][^>]*><\/script>\s*/gi, '');
  next = next.replace(/First published 20 Aug 2026 · \d+ updates · Last updated [^<\n]+? · Version [0-9.]+/g, releaseSummary);
  next = next.replace(/<nav\b[^>]*data-bhoc-evidence-links[^>]*>[\s\S]*?<\/nav>\s*/g, '');
  next = next.replace(/<footer\b/i, `${evidenceLinks}\n<footer`);
  next = next.replace(/<\/head>/i, `${headTags}\n</head>`);
  if (next === source) continue;
  await fs.writeFile(file, next);
  changed++;
  console.log('Unified shell:', relative);
}
console.log(`Unified shell synchronized on ${changed} HTML page(s).`);
