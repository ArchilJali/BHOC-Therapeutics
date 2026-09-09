const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const LEGACY_DISCUSSION = 'https://archiljali.github.io/BHOC-platform/open-discussion/';
const CONCEPTS = 'https://archiljali.github.io/BHOC-platform/concepts-hypotheses/';
const EMS_CONCEPT = `${CONCEPTS}prehospital-oxygen-delivery-selection.html`;
const SKIP_DIRS = new Set(['.git', 'node_modules']);

function walk(dir) {
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.') && entry.name !== '.well-known') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) out.push(...walk(full));
    } else if (entry.isFile() && entry.name.toLowerCase().endsWith('.html')) {
      out.push(full);
    }
  }
  return out;
}

function normalizeConceptLinks(src) {
  return src
    .replaceAll(LEGACY_DISCUSSION, CONCEPTS)
    .replaceAll('Open Discussion ↗', 'Concepts & Hypotheses ↗')
    .replaceAll('Open Discussion <span>↗</span>', 'Concepts & Hypotheses <span>↗</span>')
    .replaceAll('Open Discussion: patient selection ↗', 'Concepts & Hypotheses: patient selection ↗');
}

function addPrimaryNavigation(src) {
  return src.replace(/(<nav class="home-links"[^>]*>)([\s\S]*?)(<\/nav>)/i, (whole, start, inner, end) => {
    if (inner.includes(CONCEPTS)) return whole;
    const next = inner.replace(
      /(<a href="\/evidence\/"[^>]*>Evidence<\/a>)/i,
      `$1<a href="${CONCEPTS}" target="_blank" rel="noopener">Concepts &amp; Hypotheses ↗</a>`
    );
    return `${start}${next}${end}`;
  });
}

function addFooterNavigation(src) {
  const footerAt = src.search(/<footer\b/i);
  if (footerAt < 0) return src;
  const before = src.slice(0, footerAt);
  let footer = src.slice(footerAt);
  if (footer.includes(CONCEPTS)) return src;

  const evidenceLink = /(<a href="\/evidence\/"[^>]*>Evidence<\/a>)/i;
  if (evidenceLink.test(footer)) {
    footer = footer.replace(evidenceLink, `$1 · <a href="${CONCEPTS}" target="_blank" rel="noopener">Concepts &amp; Hypotheses ↗</a>`);
    return before + footer;
  }

  const scienceColumn = /(<div><strong>Science<\/strong>[\s\S]*?)(<\/div>)/i;
  if (scienceColumn.test(footer)) {
    footer = footer.replace(scienceColumn, `$1<a href="${CONCEPTS}" target="_blank" rel="noopener">Concepts &amp; Hypotheses ↗</a>$2`);
  }
  return before + footer;
}

function addHomepageEvidenceCta(src, rel) {
  if (rel !== 'index.html' || src.includes('Concepts &amp; Hypotheses <span>↗</span>') || src.includes('Concepts & Hypotheses <span>↗</span>')) return src;
  return src.replace(
    /(<a class="home-button" href="https:\/\/archiljali\.github\.io\/BHOC-platform\/" target="_blank" rel="noopener">BHOC-platform <span>↗<\/span><\/a>)/i,
    `$1<a class="home-button" href="${CONCEPTS}" target="_blank" rel="noopener">Concepts &amp; Hypotheses <span>↗</span></a>`
  );
}

function addEmsConceptCta(src, rel) {
  if (rel !== 'applications/index.html' || src.includes(EMS_CONCEPT)) return src;
  return src.replace(
    /(<a class="visual-story-source" href="https:\/\/archiljali\.github\.io\/BHOC-platform\/clinical\/prehospital-ems\.html" target="_blank" rel="noopener">Explore EMS page ↗<\/a>)/i,
    `$1<a class="visual-story-source" href="${EMS_CONCEPT}" target="_blank" rel="noopener">Concepts &amp; Hypotheses: patient selection ↗</a>`
  );
}

let changed = 0;
for (const file of walk(ROOT)) {
  const rel = path.relative(ROOT, file).replace(/\\/g, '/');
  if (rel === 'preview-2026.html') continue;
  const src = fs.readFileSync(file, 'utf8');
  let next = normalizeConceptLinks(src);
  next = addPrimaryNavigation(next);
  next = addFooterNavigation(next);
  next = addHomepageEvidenceCta(next, rel);
  next = addEmsConceptCta(next, rel);
  if (next !== src) {
    fs.writeFileSync(file, next);
    changed += 1;
    console.log(`updated ${rel}`);
  }
}

console.log(`Concepts & Hypotheses navigation sync complete: ${changed} HTML files updated.`);
