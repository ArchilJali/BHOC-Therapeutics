"""Synchronize navigation only; preserve protected prose, URLs and draft status."""
from pathlib import Path
from collections import Counter
import html, json, re, subprocess

ROOT = Path(__file__).resolve().parents[1]
VERSION = '20260917-nav1'
CONFIG = json.loads((ROOT / 'bhoc/navigation.json').read_text())
HUB = ROOT / 'bhoc/index.html'
CHECK = ROOT / 'scripts/check_bhoc_content.mjs'
BASELINE = ROOT / 'bhoc/content-baseline.json'


def snapshot():
    return json.loads(subprocess.check_output(['node', str(CHECK), '--snapshot'], cwd=ROOT, text=True))


def nav(is_hub):
    parts = ['<nav class="bhoc-subnav" aria-label="Understand BHOC contents">',
             '<button class="bhoc-contents-toggle" type="button" aria-expanded="false" aria-controls="bhoc-section-links"><span>Contents</span><span class="bhoc-contents-current">Overview</span><span class="bhoc-contents-chevron" aria-hidden="true">▾</span></button>',
             '<div class="bhoc-subnav-inner" id="bhoc-section-links"><span class="subnav-title">Explore BHOC</span>']
    for item in CONFIG['sections']:
        href = ('#' if is_hub else '/bhoc/#') + item['id']
        extra = ' data-location="' + html.escape(item.get('location', item['label']), quote=True) + '"'
        if item.get('childPath'):
            extra += ' data-bhoc-path="' + html.escape(item['childPath'], quote=True) + '"'
        parts.append('<a href="' + href + '"' + extra + '>' + html.escape(item['label']) + '</a>')
    return '\n'.join(parts) + '\n</div></nav>'


original = HUB.read_text()
before = snapshot()
positions = [original.index('id="' + item['id'] + '"') for item in CONFIG['sections']]
assert positions == sorted(positions), 'Config must follow actual section order'
section_re = re.compile(r'<section\b[^>]*\bid="terminology"[^>]*>[\s\S]*?</section>')
match = section_re.search(original)
assert match, 'The approved terminology anchor must exist'
old_section = match.group()
new_section = old_section
old_title = re.search(r'<h2>([\s\S]*?)</h2>', old_section).group(1)
assert html.unescape(old_title) in ['HBOC, Artificial Blood & Blood Substitute Terminology', CONFIG['terminologyTitle']], 'Unreviewed terminology title: stop instead of overwriting'
new_section = re.sub(r'<h2>[\s\S]*?</h2>', '<h2>' + html.escape(CONFIG['terminologyTitle']) + '</h2>', new_section, count=1)
new_section = re.sub(r'<p class="eyebrow">[\s\S]*?</p>', '<p class="eyebrow">' + html.escape(CONFIG['terminologyEyebrow']) + '</p>', new_section, count=1)
if 'class="bhoc-section-actions"' not in new_section:
    reading = '<nav class="bhoc-section-actions" aria-label="Terminology reading routes"><a href="#bhoc-overview">← BHOC overview</a><a href="/bhoc/historical-evolution/">Read the historical timeline →</a></nav>'
    new_section = new_section.replace('</section>', reading + '\n</section>')
paragraphs = lambda text: re.findall(r'<p(?! class="eyebrow")\b[^>]*>[\s\S]*?</p>', text)
assert paragraphs(old_section) == paragraphs(new_section), 'Terminology prose changed'
updated = original[:match.start()] + new_section + original[match.end():]
HUB.write_text(updated)

for file in sorted(ROOT.rglob('*.html')):
    if any(part in {'.git', 'node_modules', 'drafts', 'preview', 'tests'} for part in file.relative_to(ROOT).parts):
        continue
    if file.name.startswith('preview-'):
        continue
    source = file.read_text()
    if '/navigation-context.js' not in source:
        continue
    target = source
    if file == HUB:
        target, count = re.subn(r'<nav\b[^>]*class="bhoc-subnav"[^>]*>[\s\S]*?</nav>', lambda _: nav(True), target, count=1)
        assert count == 1, 'Hub navigation was not found'
    elif 'bhoc' in file.relative_to(ROOT).parts and '<main' in target and not re.search(r'noindex\s*,\s*nofollow', target, re.I):
        if re.search(r'<nav\b[^>]*class="bhoc-subnav"', target):
            target = re.sub(r'<nav\b[^>]*class="bhoc-subnav"[^>]*>[\s\S]*?</nav>', lambda _: nav(False), target, count=1)
        else:
            target = re.sub(r'<main\b', lambda _: nav(False) + '\n<main', target, count=1)
    target = re.sub(r'/navigation-context\.js(?:\?[^"\s>]*)?', '/navigation-context.js?v=' + VERSION, target)
    css = '<link rel="stylesheet" href="/bhoc/navigation.css?v=' + VERSION + '">'
    if '/bhoc/navigation.css' not in target:
        target = target.replace('</head>', css + '\n</head>')
    else:
        target = re.sub(r'/bhoc/navigation\.css(?:\?[^"\s>]*)?', '/bhoc/navigation.css?v=' + VERSION, target)
    anchors = lambda text: Counter(html.unescape(x) for x in re.findall(r'<a\b[^>]*\bhref="([^"]*)"', text))
    lost = anchors(source) - anchors(target)
    assert not lost, f'{file}: existing links lost: {lost}'
    if target != source:
        file.write_text(target)
        print('Navigation synchronized:', file.relative_to(ROOT))

injector = ROOT / 'scripts/inject_navigation_context.mjs'
text = injector.read_text()
text = re.sub(r"const scriptTag = '[^']*';", "const scriptTag = '<link rel=\"stylesheet\" href=\"/bhoc/navigation.css?v=" + VERSION + "\">\\n<script src=\"/navigation-context.js?v=" + VERSION + "\" defer></script>';", text)
text = text.replace('\">\n<script src="/navigation-context.js', '\">\\n<script src="/navigation-context.js')
injector.write_text(text)

after = snapshot()
for key in before['sections']:
    if key != 'terminology':
        assert before['sections'][key] == after['sections'][key], 'Protected section changed: ' + key
baseline = json.loads(BASELINE.read_text())
baseline['sections']['terminology'] = after['sections']['terminology']
baseline['approvedNavigationUpdate'] = {
    'startingCommit': '89ddd34c464278a79528f5be3c1776b0fc9af256',
    'scope': 'User-requested terminology heading and reading links; other section fingerprints unchanged'
}
BASELINE.write_text(json.dumps(baseline, indent=2) + '\n')
checker = CHECK.read_text()
old = "const expectedTargets = ['history', ...protectedSections.map(([id]) => id).filter(id => id !== 'history')];"
new = "const expectedTargets = JSON.parse(await fs.readFile(path.join(root, 'bhoc', 'navigation.json'), 'utf8')).sections.map(item => item.id);"
assert old in checker or new in checker, 'Unknown navigation checker: stop'
checker = checker.replace(old, new)
checker = checker.replace('exact 15 Sep 2026 09:42 hub preserved', 'protected hub preserved with the user-approved terminology heading and navigation')
CHECK.write_text(checker)
assert not (ROOT / 'bhoc/artificial-blood-blood-substitute/index.html').exists(), 'Closed standalone draft must remain unpublished'
print('Preservation verified: all protected non-terminology text/link fingerprints unchanged; terminology paragraphs unchanged; no original HTML links removed.')
