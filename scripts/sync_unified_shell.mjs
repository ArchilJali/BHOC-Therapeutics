import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const version = '20260928-shell1';
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
  next = next.replace(/<\/head>/i, `${headTags}\n</head>`);
  if (next === source) continue;
  await fs.writeFile(file, next);
  changed++;
  console.log('Unified shell:', relative);
}
console.log(`Unified shell synchronized on ${changed} HTML page(s).`);
