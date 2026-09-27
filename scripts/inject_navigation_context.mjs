import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const navigationTag = '<link rel="stylesheet" href="/bhoc/navigation.css?v=20260917-nav1">\n<script src="/navigation-context.js?v=20260922-brand5" defer></script>';
const analyticsTag = '<script src="https://analytics.ahrefs.com/analytics.js" data-key="9SwV8W7kv8qdGkrTrb3arQ" async></script>';
const ga4Tag = '<script src="/assets/ga4.js?v=20260927" defer></script>';
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
  const rel = path.relative(root, file).replaceAll('\\\\', '/');
  let next = current;

  // Track real public pages, but keep private/visual preview routes out of analytics.
  const trackAnalytics = !rel.startsWith('preview/') && rel !== 'preview-2026.html';
  if (trackAnalytics && !next.includes('analytics.ahrefs.com/analytics.js')) {
    if (!/<\/head>/i.test(next)) {
      console.log(`${rel}: skipped analytics, no </head>`);
    } else {
      next = next.replace(/<\/head>/i, `${analyticsTag}\n</head>`);
    }
  }
  if (trackAnalytics && !next.includes('/assets/ga4.js')) {
    if (/<\/head>/i.test(next)) next = next.replace(/<\/head>/i, `${ga4Tag}\n</head>`);
  }

  // Knowledge-map pages manage their own navigation, but still receive analytics above.
  if (!next.includes('data-bhoc-knowledge-map')) {
    if (next.includes('/navigation-context.js')) {
      next = next.replace(
        /<script\b(?=[^>]*\bsrc=["']\/navigation-context\.js(?:\?[^"']*)?["'])[^>]*><\/script>/gi,
        '<script src="/navigation-context.js?v=20260922-brand5" defer></script>'
      );
    } else if (/<\/head>/i.test(next)) {
      next = next.replace(/<\/head>/i, `${navigationTag}\n</head>`);
    }
  }

  if (next === current) continue;
  await fs.writeFile(file, next);
  changed += 1;
  console.log(`${rel}: navigation/analytics context synchronized`);
}

console.log(`Navigation context injection complete: ${changed} HTML file(s) changed.`);
