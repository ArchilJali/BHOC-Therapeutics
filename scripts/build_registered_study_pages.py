"""Render approved registry records separately from publication catalogues.

Inputs are dated ClinicalTrials.gov API snapshots. This script does not infer
trial/publication matches or count registry records as bibliographic additions.
Run after build_evidence_catalogues.py and sync_evidence_overviews.py.
"""
from pathlib import Path
from collections import Counter
import csv
import html
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'evidence/library'
ORIGIN = 'https://bhoctherapeutics.com'
DATE = '2026-10-31'
HUMAN = 'evidence/library/human/registered-clinical-studies.html'
VET = 'evidence/library/veterinary/Vet-fda-ema.html'
VET_ANCHOR = '#registered-veterinary-studies'
E = lambda value: html.escape(str(value if value is not None else ''), quote=True)
human = json.loads((BASE / 'human/data/registered-clinical-studies.json').read_text())
animal = json.loads((BASE / 'veterinary/data/oxyglobin-registry-scope.json').read_text())
records = human['records']
assert len(records) == 9 and len({r['nct_id'] for r in records}) == 9
assert Counter(r['study_type'] for r in records) == {'INTERVENTIONAL': 6, 'EXPANDED_ACCESS': 3}
assert human['checked_date'] == animal['checked_date'] == DATE
assert animal['nct_records_found'] == 0


def replace_section(source, marker, content, before='</main>'):
    pattern = rf'<!-- {marker}:start -->[\s\S]*?<!-- {marker}:end -->'
    block = f'<!-- {marker}:start -->\n{content}\n<!-- {marker}:end -->'
    if re.search(pattern, source):
        return re.sub(pattern, lambda _: block, source)
    assert before in source
    return source.replace(before, block + '\n' + before, 1)


def set_metadata(source, title=None, description=None, url=None):
    if title is not None:
        source = re.sub(r'<title>[\s\S]*?</title>', '<title>' + E(title) + '</title>', source, count=1)
    for names, value in [(['description', 'og:description', 'twitter:description'], description),
                         (['og:title', 'twitter:title'], title), (['og:url'], url)]:
        if value is None:
            continue
        for name in names:
            pattern = rf'(<meta\b(?=[^>]*(?:name|property)="{re.escape(name)}")[^>]*content=")[^"]*(")'
            source = re.sub(pattern, lambda m: m[1] + E(value) + m[2], source)
    if url:
        source = re.sub(r'(<link\b(?=[^>]*rel="canonical")[^>]*href=")[^"]*(")', lambda m: m[1] + url + m[2], source)

    def update_schema(match):
        data = json.loads(match[2])
        def visit(value):
            if isinstance(value, dict):
                if value.get('@type') in ['WebPage', 'CollectionPage']:
                    if title:
                        value['name'] = title
                        if 'headline' in value:
                            value['headline'] = title
                    if description:
                        value['description'] = description
                    value['dateModified'] = DATE
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)
        visit(data)
        return match[1] + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + match[3]
    return re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)([\s\S]*?)(</script>)', update_schema, source)


status_names = {'TERMINATED': 'Terminated', 'UNKNOWN': 'Unknown', 'COMPLETED': 'Completed',
                'ENROLLING_BY_INVITATION': 'Enrolling by invitation', 'NO_LONGER_AVAILABLE': 'No longer available'}


def record_card(row):
    heading = row.get('brief_title') or row['official_title']
    official_title = '<p><small>Official title: ' + E(row['official_title']) + '</small></p>' if heading != row['official_title'] else ''
    enrollment = 'Not reported'
    if row['enrollment_count'] is not None:
        enrollment = f"{row['enrollment_count']} ({'actual' if row['enrollment_type'] == 'ACTUAL' else 'estimated'})"
    phase = 'Phase 2' if row['phase'] == ['PHASE2'] else 'Not applicable / not assigned'
    design = ', '.join(E(v.replace('_', ' ').lower()) for v in [row.get('allocation'), row.get('intervention_model'), row.get('masking')] if v)
    note = ''
    if row['status'] == 'UNKNOWN':
        note = '<p class="notice">The last known status was Recruiting in 2008. Current recruitment is not confirmed.</p>'
    if row['nct_id'] == 'NCT01881503':
        note = '<p class="notice">The title says Expanded Access Study, but the registry classifies this record as Interventional. Status was last verified in August 2021. The listed status does not confirm present access or availability.</p>'
    return f'''<article class="panel registry-card" id="{E(row['nct_id'])}"><div class="eyebrow">{E(row['nct_id'])} · {E(row['study_type'].replace('_', ' ').title())}</div><h3>{E(heading)}</h3>{official_title}<dl class="registry-facts"><div><dt>Protocol</dt><dd>{E(row['protocol_id'])}</dd></div><div><dt>Registry status</dt><dd>{E(status_names[row['status']])}</dd></div><div><dt>Enrollment</dt><dd>{enrollment}</dd></div><div><dt>Phase</dt><dd>{phase}</dd></div><div><dt>Design</dt><dd>{design or 'Not assigned in this record'}</dd></div><div><dt>Participants</dt><dd>Humans, {E(row['minimum_age'])} to {E(row['maximum_age'])}</dd></div><div><dt>Last update posted</dt><dd><time datetime="{row['last_update_posted']}">{row['last_update_posted']}</time></dd></div><div><dt>Status last verified</dt><dd>{E(row['status_verified_date'])}</dd></div></dl>{note}<p><a href="{E(row['official_url'])}" target="_blank" rel="noopener noreferrer">Official ClinicalTrials.gov record: {E(row['nct_id'])} ↗</a> · <a href="{E(row['official_api_url'])}" target="_blank" rel="noopener noreferrer">Official API data ↗</a></p></article>'''


template = (BASE / 'human/BHOC-Human-fda-expanded-access.html').read_text()
head = template.split('<head>', 1)[1].split('</head>', 1)[0]
head = re.sub(r'<script\b[^>]*type="application/ld\+json"[^>]*>[\s\S]*?</script>', '', head)
title = 'Hemopure ClinicalTrials.gov Records | HBOC-201 Studies'
description = 'Nine official Hemopure/HBOC-201 human registry records: six interventional studies and three expanded-access records, with status dates and source links.'
head = set_metadata(head, title, description, ORIGIN + '/' + HUMAN)
head += '''<style>.registry-summary{padding:24px;border-left:4px solid var(--teal);background:var(--wash);margin:24px 0}.registry-nav{display:flex;flex-wrap:wrap;gap:12px;margin:20px 0}.registry-card{margin:16px 0;padding:24px}.registry-card h3{font-size:20px;line-height:1.35;max-width:900px}.registry-facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 24px}.registry-facts div{border-top:1px solid var(--line);padding-top:8px}.registry-facts dt{font-size:12px;color:var(--muted)}.registry-facts dd{margin:4px 0;overflow-wrap:anywhere}.registry-table-wrap{overflow-x:auto}.registry-table{width:100%;border-collapse:collapse;font-size:13px}.registry-table th,.registry-table td{text-align:left;padding:12px;border-bottom:1px solid var(--line);vertical-align:top}.registry-table caption{text-align:left;margin:12px 0;font-weight:600}.registry-answers h3{font-size:19px}.registry-source-date{font-size:13px;color:var(--muted)}@media(max-width:640px){.registry-facts{grid-template-columns:1fr}.registry-card{padding:18px}.registry-table{min-width:650px}}</style>'''
head += '<style>.registry-summary a{display:inline-block}</style>'
items = [{'@type': 'ListItem', 'position': i, 'name': r['nct_id'] + ': ' + r['official_title'], 'url': r['official_url']} for i, r in enumerate(records, 1)]
url = ORIGIN + '/' + HUMAN
graph = {'@context': 'https://schema.org', '@graph': [
    {'@type': 'CollectionPage', '@id': url + '#webpage', 'url': url, 'name': title, 'description': description, 'inLanguage': 'en', 'dateModified': DATE, 'author': {'@id': ORIGIN + '/#archil-jaliashvili'}, 'publisher': {'@id': ORIGIN + '/#organization'}, 'isPartOf': {'@id': ORIGIN + '/evidence/library/#website'}, 'mainEntity': {'@id': url + '#records'}},
    {'@type': 'ItemList', '@id': url + '#records', 'name': 'Official human Hemopure/HBOC-201 registry records', 'numberOfItems': 9, 'itemListElement': items},
    {'@type': 'Dataset', '@id': url + '#dataset', 'name': 'Hemopure / HBOC-201 ClinicalTrials.gov registry snapshot', 'description': description, 'url': url, 'dateModified': DATE, 'creator': {'@id': ORIGIN + '/#organization'}, 'isBasedOn': [r['official_api_url'] for r in records], 'variableMeasured': ['NCT identifier', 'Protocol identifier', 'Study type', 'Phase', 'Enrollment', 'Registry status', 'Last update posted'], 'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'application/json', 'contentUrl': ORIGIN + '/evidence/library/human/data/registered-clinical-studies.json'}, {'@type': 'DataDownload', 'encodingFormat': 'text/csv', 'contentUrl': ORIGIN + '/evidence/library/human/data/registered-clinical-studies.csv'}]},
    {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i, 'name': name, 'item': link} for i, (name, link) in enumerate([('Evidence Library', ORIGIN + '/evidence/library/'), ('Human evidence', ORIGIN + '/evidence/library/human/BHOC-Human-index.html'), ('Registered clinical studies', url)], 1)]}
]}
# Retain the verified organization/person identities from the existing site.
identity = re.search(r'<script[^>]*data-bhoc-identity[^>]*>[\s\S]*?</script>', template)
if identity:
    identity_data = json.loads(re.search(r'>([\s\S]*?)</script>', identity[0])[1])
    graph['@graph'] += [v for v in identity_data['@graph'] if v.get('@type') in ['Organization', 'Person', 'WebSite']]
head += '<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False).replace('</', '<\\/') + '</script>'
table_rows = ''.join(f'<tr><th scope="row"><a href="#{r["nct_id"]}">{r["nct_id"]}</a><br>{E(r["protocol_id"])}</th><td>{E(r["study_type"].replace("_", " ").title())}</td><td>{E(status_names[r["status"]])}</td><td>{E(r["last_update_posted"])}</td></tr>' for r in records)
main = f'''<main id="main" class="shell"><nav class="registry-nav" aria-label="Breadcrumb"><a href="/evidence/library/">Evidence Library</a><span>›</span><a href="BHOC-Human-index.html">Human evidence</a><span>› Registered studies</span></nav><section class="page-intro"><div class="eyebrow">Human registry records · Hemopure / HBOC-201</div><h1>Hemopure: registered human clinical studies</h1><p>Official ClinicalTrials.gov records for Hemopure, HBOC-201 and hemoglobin glutamer-250 (bovine). Registry records are listed separately from journal publications.</p></section><section class="registry-summary" aria-labelledby="registry-answer"><h2 id="registry-answer">How many records were found?</h2><p><strong>Nine human records were found: six Interventional records and three Expanded Access records.</strong> Five of the six interventional records are Phase 2; the sixth is classified as Interventional with phase Not Applicable, despite Expanded Access Study in its title. Four of the five Phase 2 records are randomized. These are not nine randomized controlled trials.</p><p>Oxyglobin is a different veterinary formulation, hemoglobin glutamer-200 / HBOC-301. No ClinicalTrials.gov records were found for the four checked Oxyglobin aliases. <a href="/{VET}{VET_ANCHOR}">Read the separate veterinary registry and FDA/EMA source note →</a></p><p class="registry-source-date">Registry search checked <time datetime="{DATE}">31 October 2026</time>. Each record below retains its own last-update and status-verification dates. Registration does not establish efficacy, approval or current access.</p></section><nav class="registry-nav" aria-label="Study sections"><a href="#interventional">6 interventional records</a><a href="#expanded-access">3 expanded-access records</a><a href="#registry-questions">Questions and scope</a><a href="data/registered-clinical-studies.csv" download>Download CSV</a><a href="data/registered-clinical-studies.json">Source-linked JSON</a></nav><div class="registry-table-wrap"><table class="registry-table"><caption>Registry overview. Open an NCT identifier for the full record summary.</caption><thead><tr><th scope="col">NCT / protocol</th><th scope="col">Registry type</th><th scope="col">Registry status</th><th scope="col">Last update posted</th></tr></thead><tbody>{table_rows}</tbody></table></div>'''
for study_type, anchor, heading in [('INTERVENTIONAL', 'interventional', 'Six interventional records'), ('EXPANDED_ACCESS', 'expanded-access', 'Three expanded-access records')]:
    main += f'<section id="{anchor}"><h2>{heading}</h2>' + ''.join(record_card(r) for r in records if r['study_type'] == study_type) + '</section>'
main += '''<section class="panel registry-card registry-answers" id="registry-questions"><h2>Questions and search scope</h2><h3>Are these Oxyglobin trials?</h3><p>No. The nine human records concern Hemopure / HBOC-201 / hemoglobin glutamer-250. Oxyglobin is the veterinary glutamer-200 formulation. Evidence for either historical product is not proof of a BHOC product's safety, efficacy or approval.</p><h3>Does Unknown mean Recruiting?</h3><p>No. NCT00301483 and NCT00301535 have Unknown current status. Recruiting is their last known status from 2008. NCT01881503 lists Enrolling by invitation, with status last verified in August 2021. Confirm any present access directly with the responsible study team.</p><h3>Are results posted in the registry?</h3><p>None of these nine records had structured results posted at the check date. This does not establish that journal articles are absent. A publication is linked to an NCT record only after its protocol and participant cohort have been matched.</p><h3>Are expanded access and marketing approval the same?</h3><p>No. Expanded access concerns investigational treatment under the relevant regulatory pathway. It is not a marketing approval. <a href="BHOC-Human-fda-expanded-access.html">Read the FDA expanded-access source note.</a></p><h3>How was this list compiled?</h3><p>The dated API audit checks Oxyglobin, HBOC-301, HBOC-200, hemoglobin glutamer-200, Hemopure, HBOC-201 and hemoglobin glutamer-250, plus a broader Biopure query. The broader query includes unrelated products, which were excluded. This is a product-specific ClinicalTrials.gov search, not an inventory of every historical human HBOC protocol or every registry worldwide.</p><p><a href="data/clinicaltrials-query-audit.json">View exact queries, counts, timestamps and official API links</a> · <a href="BHOC-Human-search.html">Search human clinical and separately labelled translational publications</a></p></section></main>'''
header = re.search(r'<header\b[\s\S]*?</header>', template)[0]
footer = template.split('</main>', 1)[1]
page = '<!doctype html><html lang="en"><head>' + head + '</head><body class="theme-human"><a class="skip" href="#main">Skip to content</a>' + header + main + footer
(ROOT / HUMAN).write_text('\n'.join(line.rstrip() for line in page.splitlines()) + '\n')
with (BASE / 'human/data/registered-clinical-studies.csv').open('w', newline='') as f:
    keys = ['nct_id', 'protocol_id', 'brief_title', 'official_title', 'product', 'participant_species', 'study_type', 'phase', 'status', 'enrollment_count', 'enrollment_type', 'last_update_posted', 'status_verified_date', 'official_url']
    writer = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore', lineterminator='\n'); writer.writeheader()
    writer.writerows({**r, 'phase': '; '.join(r['phase'])} for r in records)

vet_block = f'''<section class="panel" id="registered-veterinary-studies" aria-labelledby="vet-registry-title"><div class="eyebrow">Animals · Registry scope and regulatory-assessed studies</div><h2 id="vet-registry-title">Oxyglobin: veterinary studies and ClinicalTrials.gov registration</h2><p><strong>No ClinicalTrials.gov records were found for Oxyglobin, HBOC-301, HBOC-200 or hemoglobin glutamer-200 in the four exact-name searches checked on 31 October 2026.</strong> This is a scoped registry finding, not a claim that veterinary clinical or preclinical studies do not exist.</p><h3>Where are the official animal study documents?</h3><p>FDA and EMA regulatory documents assess veterinary studies. These belong in the regulatory evidence section, separately from human NCT records and publication counts.</p><dl class="facts"><div><dt>Product / species</dt><dd>Oxyglobin / dogs</dd></div><div><dt>FDA pivotal clinical study</dt><dd>64 anaemic dogs: 30 Oxyglobin, 34 control</dd></div><div><dt>Study endpoint</dt><dd>No additional oxygen-carrying support required during the first 24 hours. This was not a survival endpoint.</dd></div><div><dt>Official source</dt><dd><a href="https://animaldrugsatfda.fda.gov/adafda/app/search/public/document/downloadFoi/3700" target="_blank" rel="noopener noreferrer">FDA original approval FOI summary, 12 January 1998</a></dd></div></dl><p><strong>NADA 141-067 is an FDA animal-drug approval application number, not an NCT trial identifier.</strong> The EMA product authorisation is likewise a regulatory record, not a ClinicalTrials.gov registration.</p><h3>Does this mean there are no registered animal studies anywhere?</h3><p>No. ClinicalTrials.gov concerns research in people. This audit does not establish completeness across veterinary registries; the AVMA Animal Health Studies Database search was not verified. Published dog, cat, horse, sheep, rodent and organ/cell studies remain separately classified in the literature catalogue.</p><p><a href="data/oxyglobin-registry-scope.json">Download the animal registry scope, exact queries and official sources</a> · <a href="https://medlineplus.gov/clinicaltrials.html" target="_blank" rel="noopener noreferrer">NLM clinical-trials definition</a> · <a href="/{HUMAN}">Separate human Hemopure / HBOC-201 registry list</a> · <a href="Vet-search.html">Veterinary publications by species</a></p></section>'''
p = ROOT / VET
p.write_text(replace_section(p.read_text(), 'oxyglobin-registry', vet_block))
connections = {
    'evidence/library/human/BHOC-Human-index.html': '<section class="panel" id="registered-studies"><div class="eyebrow">Official trial registry</div><h2>Registered Hemopure / HBOC-201 human studies</h2><p>Nine ClinicalTrials.gov records: six interventional and three expanded-access records. Status dates and study types are shown separately from publication counts.</p><a href="registered-clinical-studies.html">Open the official human registry list →</a></section>',
    'evidence/library/human/BHOC-Human-fda-expanded-access.html': '<section class="panel" id="registered-studies"><h2>All identified human registry records</h2><p>Compare the six interventional and three expanded-access records, including each NCT identifier, registry status and update date. NCT01881503 is classified as Interventional even though its title says Expanded Access Study.</p><a href="registered-clinical-studies.html">Hemopure / HBOC-201 registered clinical studies →</a></section>',
    'evidence/library/human/BHOC-Human-search.html': '<p class="catalogue-relationship" id="registered-studies"><a href="registered-clinical-studies.html">Official human study registry: 9 Hemopure / HBOC-201 records, separate from these publications →</a></p>',
    'evidence/library/veterinary/Vet-index.html': '<section class="panel" id="registered-studies"><h2>Animal studies: official regulatory sources and registry scope</h2><p>Oxyglobin FDA/EMA study documents are retained as regulatory evidence. They are distinct from ClinicalTrials.gov records for human Hemopure studies.</p><a href="Vet-fda-ema.html#registered-veterinary-studies">Read the veterinary study and registry source note →</a></section>',
    'evidence/library/veterinary/Vet-03-publication-BHOC-Oxyglobin.html': '<section class="panel" id="study-registration"><h2>Are these publications registered clinical trials?</h2><p>A publication record is not a trial registration. The library includes clinical, preclinical, analytical and review literature. No NCT records were found for the checked Oxyglobin aliases; official veterinary studies are documented in FDA/EMA sources. The nine identified human NCT records concern the different product Hemopure / HBOC-201.</p><p><a href="Vet-fda-ema.html#registered-veterinary-studies">Animal registry scope and official study documents →</a> · <a href="../human/registered-clinical-studies.html">Separate human registry list →</a></p></section>',
    'evidence/library/index.html': f'<p class="notice" id="registered-studies">Official study records: <a href="/{HUMAN}">Human Hemopure / HBOC-201 registry list</a> · <a href="/{VET}{VET_ANCHOR}">Animal Oxyglobin regulatory studies and registry scope</a>. Registry counts are separate from publication counts.</p>',
}
for path, block in connections.items():
    p = ROOT / path
    p.write_text(replace_section(p.read_text(), 'registered-studies-navigation', block))

# Keep social descriptions and page-level schema aligned with visible counters.
descriptions = {
    'evidence/library/human/BHOC-Human-index.html': 'Explore 195 source-linked human clinical and separately labelled translational records on HBOC-201, Hemopure, severe anemia, trauma and surgery.',
    'evidence/library/transplant/Transplant-index.html': 'Explore 65 source-linked publications on BHOC and HBOC oxygen carriers in liver, kidney, heart and limb transplantation, perfusion and organ preservation.',
    VET: 'Official Oxyglobin FDA and EMA documents, the 64-dog pivotal study and a dated ClinicalTrials.gov search, with veterinary registry scope explained.',
}
for path, description in descriptions.items():
    p = ROOT / path
    p.write_text(set_metadata(p.read_text(), description=description))

# One release includes the already approved 30 October literature review and the
# 31 October registry/SEO completion. Stable review IDs and record dates remain.
for path in ['site-release.json', 'evidence/library/version.json']:
    p = ROOT / path
    release = json.loads(p.read_text())
    release.update(version='26.10.31', updated='31 Oct 2026', updated_iso=DATE)
    p.write_text(json.dumps(release, indent=2) + '\n')
p = ROOT / 'unified-shell.js'
p.write_text(p.read_text().replace('Last updated 30 Oct 2026 · Version 26.10.30', 'Last updated 31 Oct 2026 · Version 26.10.31'))
changed = subprocess.check_output(['git', 'diff', '--name-only', '--', '*.html'], cwd=ROOT, text=True).splitlines() + [HUMAN]
for path in changed:
    p = ROOT / path
    source = p.read_text()
    source = source.replace('to this view on 30 October 2026.', 'to this view on 31 October 2026.')
    source = source.replace('Library update · 30 October 2026', 'Literature review · 30 October 2026')
    source = source.replace('Evidence page updated 30 October 2026.', 'Evidence page updated 31 October 2026.')
    source = re.sub(r'First published 20 Aug 2026 · \d+ updates · Last updated (?:25|30|31) Oct 2026 · Version 26\.10\.(?:25|30|31)', 'First published 20 Aug 2026 · 87 updates · Last updated 31 Oct 2026 · Version 26.10.31', source)
    if path == 'news/knowledge-updates/index.html':
        pattern = r'(<article class="timeline-item" id="oxyglobin-literature-20261030">)[\s\S]*?(</article>)'
        match = re.search(pattern, source)
        assert match
        article = match[0].replace('<time datetime="2026-10-30">30 October 2026</time>', '<time datetime="2026-10-31">31 October 2026</time>')
        article = article.replace('</div></article>', f'<p>Separate official registry lists: <a href="/{HUMAN}">9 human Hemopure/HBOC-201 records</a> and <a href="/{VET}{VET_ANCHOR}">veterinary Oxyglobin study documents and registry scope</a>. Registry records do not increase the publication count.</p></div></article>')
        if 'Separate official registry lists:' in match[0]:
            article = match[0]
        source = source[:match.start()] + article + source[match.end():]
    p.write_text(source)

# Preserve every existing sitemap entry; date only pages changed by this release.
changed_urls = {ORIGIN + '/' + p.removesuffix('index.html') if p.endswith('/index.html') else ORIGIN + '/' + p for p in changed}
for path in ['sitemap.xml', 'evidence/library/sitemap.xml']:
    p = ROOT / path
    source = p.read_text()
    def lastmod(match):
        block = match[0]
        loc = re.search(r'<loc>\s*([^<]+)', block)[1]
        if loc not in changed_urls:
            return block
        if '<lastmod>' in block:
            return re.sub(r'<lastmod>.*?</lastmod>', '<lastmod>' + DATE + '</lastmod>', block)
        return block.replace('</loc>', '</loc><lastmod>' + DATE + '</lastmod>', 1)
    source = re.sub(r'<url>[\s\S]*?</url>', lastmod, source)
    if url not in source:
        source = source.replace('</urlset>', f'  <url><loc>{url}</loc><lastmod>{DATE}</lastmod></url>\n</urlset>')
    p.write_text(source)
print('Rendered 9 human registry records, separate veterinary source note, metadata, links and dated sitemaps. Publication counts unchanged.')
