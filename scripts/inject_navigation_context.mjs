import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const scriptTag = '<link rel="stylesheet" href="/bhoc/navigation.css?v=20260917-nav1">\n<script src="/navigation-context.js?v=20260922-inline4" defer></script>';
const skipDirs = new Set(['.git', '.github', 'node_modules', 'assets', 'scripts', 'seo']);
const skipFiles = new Set(['preview-2026.html']);

async function walk(dir) {
  const entries = await fs.readdir(dir, {withFileTypes: true});
  const files = [];
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    const rel = path.relative(root, full).replaceAll('\\', '/');
    if (entry.isDirectory()) {
      if (!skipDirs.has(entry.name)) files.push(...await walk(full));
      continue;
    }
    if (entry.isFile() && entry.name.endsWith('.html') && !skipFiles.has(rel)) files.push(full);
  }
  return files;
}

const htmlFiles = await walk(root);
let changed = 0;
for (const file of htmlFiles) {
  const current = await fs.readFile(file, 'utf8');
  if (current.includes('data-bhoc-knowledge-map')) continue;
  let next = current;
  if (current.includes('/navigation-context.js')) {
    next = current.replace(
      /<script\b(?=[^>]*\bsrc=["']\/navigation-context\.js(?:\?[^"']*)?["'])[^>]*><\/script>/gi,
      '<script src="/navigation-context.js?v=20260922-inline4" defer></script>'
    );
  } else {
    if (!/<\/head>/i.test(current)) {
      console.log(`${path.relative(root, file)}: skipped, no </head>`);
      continue;
    }
    next = current.replace(/<\/head>/i, `${scriptTag}\n</head>`);
  }
  if (next === current) continue;
  await fs.writeFile(file, next);
  changed += 1;
  console.log(`${path.relative(root, file)}: navigation context synchronized`);
}

console.log(`Navigation context injection complete: ${changed} HTML file(s) changed.`);
