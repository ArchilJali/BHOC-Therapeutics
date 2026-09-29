"""Apply the user-approved Levien 2006 news release without duplicating evidence."""
from pathlib import Path
import copy
import json
import re
import xml.etree.ElementTree as ET

DOI = '10.1111/j.1751-2824.2006.00025.x'
SOURCE = 'https://doi.org/' + DOI
ROUTE = '/news/hemopure-south-africa-2006/'
URL = 'https://bhoctherapeutics.com' + ROUTE
IMAGE = '/assets/news/hemopure-south-africa-2006-wiley-header.webp'
TITLE = 'Hemopure in South Africa: Beyond Blood Replacement'
ALT = 'Wiley article header for L. J. Levien’s 2006 report, South Africa: clinical experience with Hemopure.'
DATE = '2026-09-29'

# Edit only the existing entry, keeping IDs, provenance and all other records intact.
for rel in ['evidence/library/human/BHOC-Human-publications.json', 'evidence/library/veterinary/Vet-publications.json']:
    p = Path(rel)
    text = p.read_text()
    before = json.loads(text)
    after = copy.deepcopy(before)
    targets = [r for r in after if 'south africa' in r.get('title','').lower() and 'clinical experience' in r.get('title','').lower()]
    assert len(targets) == 1, (rel, len(targets))
    row = targets[0]
    oldrow = next(r for r in before if r.get('id') == row['id'])
    row.update(title='South Africa: clinical experience with Hemopure', authors='Levien LJ', journal='ISBT Science Series', doi=DOI)
    if isinstance(row['id'], int):
        assert row['id'] == 369
        row.update(doiUrl=SOURCE, citation='Levien LJ. South Africa: clinical experience with Hemopure. ISBT Science Series. 2006;1(1):167–173. doi: ' + DOI + '.', verification='Publisher metadata and abstract checked (2026-09-29)', note='Historical clinical surveillance report of 336 patients. Observational evidence, not a randomized comparison or clinical validation of BHOC. First published online 15 August 2006.')
    else:
        assert row['id'] == 'bhoc-118'
        row.update(doi_url=SOURCE, link=SOURCE, metadata_checked=DATE)
    decoder = json.JSONDecoder()
    offset = 1
    replaced = False
    while offset < len(text):
        while offset < len(text) and (text[offset].isspace() or text[offset] == ','):
            offset += 1
        if text[offset:offset+1] == ']':
            break
        value, end = decoder.raw_decode(text, offset)
        if value.get('id') == row['id']:
            replacement = json.dumps(row, ensure_ascii=False, indent=2).replace('\n', '\n  ')
            text = text[:offset] + replacement + text[end:]
            replaced = True
            break
        offset = end
    assert replaced
    parsed = json.loads(text)
    assert len(parsed) == len(before)
    assert [r for r in parsed if r.get('id') != row['id']] == [r for r in before if r.get('id') != row['id']]
    p.write_text(text)
    print('Corrected existing record',rel,row['id'],'count unchanged',len(parsed))

p = Path('news/index.html')
s = p.read_text()
card = f'''\n<article class="news-card featured" id="hemopure-south-africa-2006">
  <div class="news-media news-photo"><a href="{ROUTE}" aria-label="Read the Hemopure historical perspective"><img src="{IMAGE}" width="1248" height="616" loading="lazy" decoding="async" alt="{ALT}"></a></div>
  <div class="news-copy">
    <div class="news-meta"><time datetime="{DATE}">29 September 2026</time><span>Historical Perspective · 2006</span></div>
    <h2>{TITLE}</h2>
    <p class="news-summary-text">Revisiting Levien’s clinical report from South Africa and a shift in emphasis from red-cell replacement toward tissue oxygenation.</p>
    <div class="news-actions"><a class="news-action primary" href="{ROUTE}">Read the historical perspective →</a><a class="news-action" href="{SOURCE}" target="_blank" rel="noopener noreferrer">Original 2006 article ↗</a></div>
    <div class="news-note">Historical Hemopure evidence; not clinical validation of BHOC.</div>
  </div>
</article>\n'''
if 'id="hemopure-south-africa-2006"' not in s:
    marker = '<div class="news-feed">'
    assert s.count(marker) == 1
    s = s.replace(marker, marker + card, 1)
if 'data-hemopure-news-image' not in s:
    css = '''<style data-hemopure-news-image>
#hemopure-south-africa-2006 .news-media{background:#fff;display:flex;align-items:center;min-width:0;overflow:hidden}
#hemopure-south-africa-2006 .news-media a{display:block;width:100%}
#hemopure-south-africa-2006 .news-media img{display:block;width:100%;height:auto;max-height:none;object-fit:contain;aspect-ratio:1248/616;background:#fff}
</style>\n'''
    s = s.replace('</head>',css+'</head>',1)

def update_graph(match):
    data = json.loads(match.group(2))
    graph = data.get('@graph', [data])
    modified = False
    for obj in graph:
        if obj.get('@type') == 'ItemList':
            items = obj.get('itemListElement', [])
            if not any(URL in json.dumps(item) for item in items):
                items.insert(0, {'@type':'ListItem','position':1,'url':URL,'name':TITLE})
                for i, item in enumerate(items, 1):
                    item['position'] = i
                obj['numberOfItems'] = len(items)
                modified = True
    if modified:
        return match.group(1) + json.dumps(data,ensure_ascii=False,separators=(',',':')) + match.group(3)
    return match.group(0)
s = re.sub(r'(<script\b[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>)(.*?)(</script>)', update_graph, s, flags=re.S)
p.write_text(s)

# Add one historical source card, not a duplicate library publication.
p = Path('evidence/library/historical-sources/index.html')
s = p.read_text()
if 'id="levien-hemopure-2006"' not in s:
    marker = '<section class="history-grid" aria-label="Historical articles and primary sources">'
    assert s.count(marker) == 1
    item = f'''\n      <article class="panel history-card" id="levien-hemopure-2006">
        <div class="eyebrow">Clinical history · 2006</div>
        <h2>Hemopure in South Africa</h2>
        <p class="subtitle">Beyond Blood Replacement</p>
        <p>L. J. Levien’s clinical surveillance report documents increasing attention to tissue oxygenation rather than red-cell substitution. An observational historical source, not a randomized comparison.</p>
        <p class="people">Levien LJ · ISBT Science Series · 2006;1(1):167–173 · <a href="{SOURCE}" target="_blank" rel="noopener noreferrer">Original publication ↗</a></p>
        <a class="history-link" href="{ROUTE}">Read the historical perspective →</a>
      </article>\n'''
    s = s.replace(marker,marker+item,1)
    p.write_text(s)

# Preserve the existing timeline and all original anchors and source URLs.
p = Path('bhoc/historical-evolution/index.html')
s = p.read_text()
if 'id="levien-2006-tissue-oxygenation"' not in s:
    start = s.index('id="heading-24"')
    end = s.index('</div></div>', start) + len('</div></div>')
    item = f'''\n<div class="event" id="levien-2006-tissue-oxygenation"><div class="year">2006</div><div><h3>Hemopure: clinical use and tissue oxygenation</h3><p>Levien’s South African clinical surveillance report described growing interest in Hemopure’s tissue-oxygenation function rather than red-cell substitution, and called for controlled prospective studies.</p><a class="source-link" href="{ROUTE}">Historical perspective: beyond blood replacement</a><br><a class="source-link" data-source-url="{SOURCE}" href="{SOURCE}" target="_blank" rel="noopener noreferrer">Levien, ISBT Science Series, 2006 ↗</a></div></div>'''
    s = s[:end] + item + s[end:]
    p.write_text(s)

# Sitemap entry uses the date of our news, never the date of the historical source.
p = Path('sitemap.xml')
s = p.read_text()
if '<loc>'+URL+'</loc>' not in s:
    assert '</urlset>' in s
    s = s.replace('</urlset>',f'  <url><loc>{URL}</loc><lastmod>{DATE}</lastmod></url>\n</urlset>')
    ET.fromstring(s)
    p.write_text(s)

# Article/header screenshot identification must be accurate.
p = Path('news/hemopure-south-africa-2006/index.html')
s = p.read_text().replace('Original research publication: 2006','Original clinical report: 2006')
p.write_text(s)
print('News, source records, historical links and sitemap prepared.')
