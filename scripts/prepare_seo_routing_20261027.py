#!/usr/bin/env python3
"""One-time routing repair. Preserve existing scientific text, URLs and styles."""
from pathlib import Path
import html
import json
import re
import subprocess
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-27'
HOST = 'https://bhoctherapeutics.com'
SEPSIS = 'evidence/library/science/sepsis-microcirculation-tissue-oxygenation-bhoc.html'
MILITARY = '/applications/military-disaster-medicine/'
SURGERY = '/applications/#perioperative-oxygen-delivery'
FILES = ['topics/index.html', 'applications/index.html', SEPSIS,
         'seo/page-keyword-map.md', 'seo/BHOC-SEO-Keywords.md',
         'sitemap.xml', 'evidence/library/sitemap.xml']
before = {p: (ROOT / p).read_text() for p in FILES}
changes = dict(before)

def once(text, old, new):
    assert text.count(old) == 1, (old[:100], text.count(old))
    return text.replace(old, new, 1)

def text_only(value):
    return html.unescape(re.sub(r'<[^>]*>', '', value)).strip()

def json_scripts(text, edit):
    def change(m):
        value = json.loads(m.group(2))
        if edit(value):
            return m.group(1) + json.dumps(value, ensure_ascii=False, separators=(',', ':')) + m.group(3)
        return m.group(0)
    return re.sub(r'(<script\b[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>)(.*?)(</script>)', change, text, flags=re.S)

# 1. Topic directory: retain all 43 routes; give their links descriptive text.
topics = before['topics/index.html']
card_re = re.compile(r'<article\b[^>]*data-topic-card[^>]*>.*?</article>', re.S)
old_cards = card_re.findall(topics)
assert len(old_cards) == 43, len(old_cards)
short_names = {
 'BHOC Therapeutics: Precision Oxygen Therapeutics': 'Precision Oxygen Therapeutics',
 'What Is a Biological Hemoglobin Oxygen Carrier?': 'BHOC definition',
 'HBOC and Blood Substitute Terminology': 'Oxygen-carrier terminology',
 'Hemoglobin, Oxygen Affinity and P50': 'Hemoglobin and oxygen affinity',
 'Microcirculation and Tissue Oxygen Delivery': 'Microcirculation and oxygen delivery',
 'Nitric Oxide, Vascular Responses and HBOC Research': 'Nitric oxide and vascular responses',
 'Hemoglobin Dose in Red Cell Transfusion': 'Hemoglobin dose in transfusion',
 'Hemopure and HBOC-201: Evidence and History': 'Hemopure and HBOC-201 evidence',
 'Hemopure Expanded Access and Regulatory Context': 'Hemopure expanded access',
 'Prehospital Blood Access and Oxygen Delivery': 'Prehospital blood and oxygen delivery',
 'Air Medical Blood Logistics and Oxygen Delivery': 'Air medical blood logistics',
 'Donor Blood Availability and Supply Constraints': 'Donor blood availability',
 'Severe Anemia and Oxygen-Delivery Evidence': 'Severe anemia and oxygen delivery',
 'Bloodless Medicine and Oxygen Carrier Evidence': 'Bloodless medicine evidence',
 'Postpartum Hemorrhage and the Oxygen-Delivery Gap': 'Postpartum hemorrhage and blood access',
 'Hemorrhagic Shock and Tissue Oxygen Debt': 'Hemorrhagic shock and oxygen debt',
 'Tumor Hypoxia and Oxygen-Delivery Research': 'Tumor hypoxia research',
 'HIF, VHL and Physical Oxygen Availability': 'HIF, VHL and oxygen availability',
 'Oxygen Continuity: A Research Hypothesis': 'Oxygen-continuity research question',
 'Measuring Oxygen Delivery Beyond Saturation': 'Measuring functional oxygen delivery',
 'Ischemia, Reperfusion and Oxygen Carrier Research': 'Ischemia and reperfusion research',
 'Renal Anemia and Oxygen-Delivery Questions': 'Renal anemia research questions',
 'BHOC Research Collaboration': 'Research collaboration',
 'Sickle Cell Disease, Matched Blood and Oxygen Delivery': 'Sickle cell transfusion evidence',
 'Sepsis, Microcirculation and Tissue Oxygenation': 'Sepsis and tissue oxygenation',
 'Endothelium, Nitric Oxide and Oxygen Transport': 'Endothelium and oxygen transport',
 'Oxygen, Cellular Metabolism and Bioenergetics': 'Oxygen and cellular metabolism',
 'Mitochondria, Cellular Respiration and Oxygen Availability': 'Mitochondria and oxygen availability',
 'Endothelial Glycocalyx and Microvascular Barrier': 'Endothelial glycocalyx',
 'Inflammation, Immune Context and Tissue Oxygenation': 'Inflammation and tissue oxygenation',
 'Cardiac Ischemia and Oxygen-Carrier Research': 'Cardiac ischemia research',
 'Brain Microcirculation and Oxygen-Transport Models': 'Brain oxygen-transport models',
 'ECMO, Cardiopulmonary Bypass and Oxygen-Delivery Research': 'ECMO and bypass oxygen-delivery research',
 'Hemolysis, Oxidation and Cell-Free Hemoglobin': 'Hemolysis and cell-free hemoglobin',
 'Hypoxia, Hypoxemia and Functional Oxygen Delivery': 'Hypoxia and functional oxygen delivery',
 'Organ Dysfunction, Perfusion and Oxygen Use': 'Organ dysfunction and oxygen use',
 'Glycolysis, Oxidative Metabolism and Hypoxia': 'Glycolysis and oxidative metabolism',
 'Resuscitation, Oxygen Debt and Functional Endpoints': 'Resuscitation and functional endpoints',
 'Plasma and Red-Cell Oxygen-Transport Compartments': 'Plasma and red-cell oxygen transport',
 'Monitoring Perfusion, Oxygenation and Metabolism': 'Perfusion and metabolic monitoring',
 'Golden Hour, Trauma and Prehospital Oxygen Delivery': 'Golden Hour and prehospital care',
 'Medical Drone Delivery and Blood Logistics': 'Medical drone delivery and blood logistics',
}

def replace_card(m):
    card = m.group(0)
    heading = text_only(re.search(r'<h2[^>]*>(.*?)</h2>', card, re.S).group(1))
    label = short_names.get(heading, heading)
    assert card.count('>Explore this topic</a>') == 1, heading
    return card.replace('>Explore this topic</a>', '>' + html.escape(label) + '</a>')

topics = card_re.sub(replace_card, topics)
new_routes = [
    {'name': 'Military & Disaster Medicine: Delayed Evacuation', 'url': HOST + MILITARY,
     'summary': 'Prolonged casualty care, battlefield blood logistics and oxygen-delivery research when medical evacuation is delayed.',
     'label': 'Prolonged casualty care and delayed evacuation'},
    {'name': 'Surgery, Perioperative Oxygen Delivery and Blood Management', 'url': HOST + SURGERY,
     'summary': 'A guided route to existing work on perioperative anemia, surgical blood loss, hemoglobin dose, donor blood availability and cardiopulmonary bypass.',
     'label': 'Perioperative oxygen delivery and blood management'}
]
for route, after_url in zip(new_routes, [HOST + '/evidence/library/clinical/prehospital-ems.html#air-medical', HOST + '/applications/severe-anemia-oxygen-delivery/#bloodless-medicine']):
    card = '<article class="topic-card" data-topic-card><h2>' + html.escape(route['name']) + '</h2><p>' + html.escape(route['summary']) + '</p><a href="' + route['url'] + '">' + html.escape(route['label']) + '</a></article>'
    matched = [c for c in card_re.findall(topics) if 'href="' + after_url + '"' in c]
    assert len(matched) == 1, after_url
    topics = once(topics, matched[0], matched[0] + card)

def edit_topic_schema(value):
    changed = False
    for node in value.get('@graph', []):
        if node.get('@type') != 'CollectionPage':
            continue
        items = node['mainEntity']['itemListElement']
        assert len(items) == 43
        for route, after_url in zip(new_routes, [HOST + '/evidence/library/clinical/prehospital-ems.html#air-medical', HOST + '/applications/severe-anemia-oxygen-delivery/#bloodless-medicine']):
            index = next(i for i, item in enumerate(items) if item['url'] == after_url)
            items.insert(index + 1, {'@type': 'ListItem', 'name': route['name'], 'url': route['url']})
        for i, item in enumerate(items, 1):
            item['position'] = i
        node['mainEntity']['numberOfItems'] = len(items)
        node['dateModified'] = DATE
        changed = True
    return changed

topics = json_scripts(topics, edit_topic_schema)
topics = once(topics, '>43 topic routes</p>', '>45 topic routes</p>')
assert 'Explore this topic' not in topics
assert len(card_re.findall(topics)) == 45
changes['topics/index.html'] = topics

# 2. One section in the existing Applications page, not another review or URL.
apps = before['applications/index.html']
section = '''<!-- PERIOPERATIVE ROUTE 20261027 START -->
<section class="topic-shell topic-section" id="perioperative-oxygen-delivery" aria-labelledby="perioperative-heading">
<h2 id="perioperative-heading">Surgery, perioperative oxygen delivery and blood management</h2>
<p>Explore the existing evidence and research questions on perioperative anemia, surgical blood loss, hemoglobin dose, donor blood availability and cardiopulmonary bypass. This section connects the related materials rather than duplicating them.</p>
<div class="topic-source-list">
<a href="/applications/severe-anemia-oxygen-delivery/"><strong>Severe anemia and oxygen-delivery evidence</strong></a>
<a href="/science/rbc-unit-hemoglobin-dose-variability.html"><strong>Hemoglobin dose and red-cell unit variability</strong></a>
<a href="/applications/donor-blood-availability/"><strong>Donor blood availability and supply resilience</strong></a>
<a href="/applications/extracorporeal-oxygen-delivery/"><strong>Cardiopulmonary bypass and ECMO research</strong></a>
<a href="/evidence/library/human/BHOC-Human-index.html"><strong>Historical human-use and surgical evidence</strong></a>
</div>
<p>Historical studies remain specific to their product and clinical setting. This research navigation does not establish a BHOC surgical indication or a treatment protocol.</p>
</section>
<!-- PERIOPERATIVE ROUTE 20261027 END -->
'''
assert 'id="perioperative-oxygen-delivery"' not in apps
apps = once(apps, '<!-- TOPIC EXTENSION research-routes START -->', section + '<!-- TOPIC EXTENSION research-routes START -->')
nav = '<a href="#perioperative-oxygen-delivery">Surgery <span>Perioperative oxygen delivery</span></a>'
anchor = '<a href="#military-context">Military &amp; Disaster Medicine</a>'
apps = once(apps, anchor, anchor + '\n      ' + nav)
links = '<a href="' + MILITARY + '"><strong>Military, disaster and delayed evacuation</strong></a><a href="#perioperative-oxygen-delivery"><strong>Surgery and perioperative oxygen delivery</strong></a>'
anchor = '<a href="https://bhoctherapeutics.com/topics/"><strong>All oxygen-delivery research topics</strong></a>'
apps = once(apps, anchor, links + anchor)
# Prove that removing the three additions restores the complete original page.
assert apps.replace(section, '').replace('\n      ' + nav, '').replace(links, '') == before['applications/index.html']
changes['applications/index.html'] = apps

# 3. Align only sepsis metadata; preserve its complete visible body byte-for-byte.
old_title = 'Tissue Oxygenation & Microcirculation | BHOC Science'
new_title = 'Sepsis, Microcirculation & Tissue Oxygenation | BHOC'
old_desc = 'Scientific context for sepsis, tissue oxygenation, microcirculation and endothelial dysfunction, with relevance to BHOC and Precision Oxygen Therapeutics.'
new_desc = 'Review sepsis, microcirculatory dysfunction and tissue oxygenation, with source-linked physiology and clearly separated oxygen-carrier research questions.'
head, body = before[SEPSIS].split('</head>', 1)
assert old_title in head and html.escape(old_title) in head
head = head.replace(old_title, new_title).replace(html.escape(old_title), html.escape(new_title)).replace(old_desc, new_desc)
head = head.replace('"name": "Tissue oxygenation and microcirculation"', '"name": "Sepsis, microcirculation and tissue oxygenation"')
changes[SEPSIS] = head + '</head>' + body
assert changes[SEPSIS].split('</head>', 1)[1] == before[SEPSIS].split('</head>', 1)[1]

# 4. Update existing ownership and keyword documents, never a parallel master.
route_map = before['seo/page-keyword-map.md']
route_map = re.sub(r'^Updated: .*$', 'Updated: 27 October 2026', route_map, count=1, flags=re.M)
anchor = '| `/applications/military-disaster-medicine/` | Prolonged casualty care and delayed evacuation | battlefield blood logistics; contested evacuation; disaster medicine; oxygen delivery before definitive care |'
extra = '\n| `/applications/#perioperative-oxygen-delivery` | Surgery and perioperative oxygen delivery | perioperative anemia; surgical blood loss; patient blood management; hemoglobin dose; donor blood availability; cardiopulmonary bypass |\n| `/evidence/library/science/sepsis-microcirculation-tissue-oxygenation-bhoc.html` | Sepsis, microcirculation and tissue oxygenation | septic shock; endothelial dysfunction; perfusion monitoring; organ dysfunction; cellular metabolism |'
route_map = once(route_map, anchor, anchor + extra)
route_map += '''

## Routing corrections — 27 October 2026

- `/topics/` retains its existing 43 routes and adds two: military/disaster medicine and the perioperative section of `/applications/`. Its 45 route cards and ItemList use the same destinations.
- Perioperative ownership is an anchored section of an existing page, not a separate indexable page. Hemoglobin-dose, anemia, donor-blood and bypass articles retain their own primary intent and canonical URLs.
- All topic-card anchors now describe their subject instead of repeating `Explore this topic`. Existing titles, summaries and destinations are retained.
- Sepsis title, Open Graph, Twitter title and WebPage name: `Sepsis, Microcirculation & Tissue Oxygenation | BHOC`. Scientific text and the established URL remain unchanged.
- Existing oncology, SCD, physiology, publication titles, DOI records and homepage positioning are preserved. Wound healing and longevity remain research reserves; this repair does not publish new treatment claims or new disease pages.
- Use the relevant permanent topic page in publication announcements and editorial plans; do not rewrite old social posts as part of this repair. The existing donor-blood page remains the route for blood-system resilience and availability.
- These are implemented content/routing corrections, not measured ranking gains. Search volume, positions and traffic impact require separate comparable measurements.
'''
changes['seo/page-keyword-map.md'] = route_map
master = before['seo/BHOC-SEO-Keywords.md']
master = once(master, '### 4.11 Surgery\n\n**Primary:** surgical blood loss', '### 4.11 Surgery\n\n**Primary:** surgical blood loss\n\n**Existing route:** `/applications/#perioperative-oxygen-delivery` (assigned 27 October 2026). A section linking existing anemia, hemoglobin-dose, donor-blood and bypass sources, not a duplicate review.')
master = once(master, '### 4.4 Prehospital / EMS / HEMS\n\n**Primary:** prehospital oxygenation', '### 4.4 Prehospital / EMS / HEMS\n\n**Primary:** prehospital oxygenation\n\n**Military/disaster subcluster owner:** `/applications/military-disaster-medicine/`. Keep delayed evacuation, prolonged casualty care, military blood logistics and disaster blood availability with this existing page; the general EMS evidence page keeps its broader prehospital intent.')
# Add only the limited, approved routing terms absent from this existing master.
new_terms = [t for t in ['prolonged casualty care', 'delayed medical evacuation', 'contested medical evacuation', 'military blood logistics', 'disaster medicine blood supply', 'perioperative oxygen delivery'] if not re.search(r'^- ' + re.escape(t) + r'\s*$', master, flags=re.M | re.I)]
if new_terms:
    master += '\n\n### Routing vocabulary synchronized 27 October 2026\n\nThese terms support the existing military/disaster page and perioperative section. They are editorial targets, not measured search demand or evidence of BHOC efficacy.\n\n' + ''.join('- ' + t + '\n' for t in new_terms)
changes['seo/BHOC-SEO-Keywords.md'] = master

# Update lastmod only for changed documents already listed; never add fragment URLs.
for sitemap, urls in [('sitemap.xml', [HOST + '/topics/', HOST + '/applications/']), ('evidence/library/sitemap.xml', [HOST + '/' + SEPSIS])]:
    value = before[sitemap]
    for url in urls:
        pat = re.compile(r'<url>\s*<loc>' + re.escape(url) + r'</loc>.*?</url>', re.S)
        found = pat.findall(value)
        assert len(found) == 1, (sitemap, url, len(found))
        node = found[0]
        if re.search(r'<lastmod>.*?</lastmod>', node, re.S):
            new = re.sub(r'<lastmod>.*?</lastmod>', '<lastmod>' + DATE + '</lastmod>', node, count=1, flags=re.S)
        else:
            new = node.replace('</loc>', '</loc><lastmod>' + DATE + '</lastmod>', 1)
        value = value.replace(node, new, 1)
    changes[sitemap] = value

# Do not silently change frozen baselines or an unrelated generator. Detect source rules.
generator_hits = []
for path in ROOT.rglob('*'):
    if not path.is_file() or path.suffix not in ('.py', '.js', '.cjs', '.mjs') or '.git' in path.parts or path == Path(__file__).resolve():
        continue
    try:
        raw = path.read_text()
    except (UnicodeError, OSError):
        continue
    if old_title in raw or html.escape(old_title) in raw or 'Explore this topic' in raw:
        generator_hits.append(str(path.relative_to(ROOT)))
assert not generator_hits, 'Inspect active generator rules before publishing: ' + repr(generator_hits)

# Preserve all old source destinations and heading/paragraph text in the directory.
for old in old_cards:
    for tag in ('h2', 'p'):
        content = re.search(r'<' + tag + r'[^>]*>(.*?)</' + tag + '>', old, re.S).group(1)
        assert content in topics, content
old_links = Counter(re.findall(r'href=[\"\']([^\"\']+)', before['topics/index.html']))
new_links = Counter(re.findall(r'href=[\"\']([^\"\']+)', topics))
assert not (old_links - new_links)
for name in FILES:
    if name.endswith('.html'):
        old_can = re.search(r'<link\b[^>]*rel="canonical"[^>]*>', before[name]).group(0)
        assert old_can in changes[name]
        for script in re.findall(r'<script\b[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>(.*?)</script>', changes[name], re.S):
            json.loads(script)
    (ROOT / name).write_text(changes[name])

# Small machine-readable report and patch for independent inspection, not site content.
report = {'date': DATE, 'starting_commit': 'b983a810454fe6c03fd0e4164b8c73d9313e9e01', 'topic_routes_before': 43, 'topic_routes_after': 45, 'descriptive_topic_anchors': 45, 'sepsis_body_unchanged': True, 'applications_original_content_preserved': True, 'new_pages': 0, 'new_routes': new_routes, 'changed_files': FILES, 'generator_rules_found': generator_hits}
Path('/tmp/seo-routing-report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
print(json.dumps(report, ensure_ascii=False))
