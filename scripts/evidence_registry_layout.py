"""Apply the user-approved registry navigation and compact source layouts.

This only arranges existing, approved material. Publication records, registry
snapshots and historical scientific paragraphs are not rewritten.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'evidence/library'
STYLE = '<link rel="stylesheet" href="/evidence/library/assets/registered-studies.css?v=20261031-registry-entry">'
HUMAN = '/evidence/library/human/registered-clinical-studies.html'
UPDATES = '/news/knowledge-updates/#oxyglobin-literature-20261030-details'
ELECTRONIC_TITLE = 'Electronically Registered Clinical Studies | Hemopure'
ELECTRONIC_DESCRIPTION = 'Hemopure and HBOC-201 clinical studies in the electronic ClinicalTrials.gov registry, with protocol identifiers, study types, status dates and official source links.'


def styled(source):
    source = re.sub(r'<link\b[^>]*href="[^"]*/registered-studies\.css[^"]*"[^>]*>', '', source)
    return source.replace('</head>', STYLE + '\n</head>', 1)


def replace_marker(source, marker, content):
    block = f'<!-- {marker}:start -->\n{content}\n<!-- {marker}:end -->'
    pattern = rf'<!-- {marker}:start -->[\s\S]*?<!-- {marker}:end -->'
    if re.search(pattern, source):
        return re.sub(pattern, lambda _: block, source)
    return source.replace('</main>', block + '\n</main>', 1)


def context_nav(active):
    links = [('overview', '/evidence/library/human/BHOC-Human-index.html', 'Overview'),
             ('publications', '/evidence/library/human/BHOC-Human-search.html', 'Publications'),
             ('registry', HUMAN, 'Registered clinical studies'),
             ('access', '/evidence/library/human/BHOC-Human-fda-expanded-access.html', 'FDA expanded access')]
    return '<nav class="registry-context-nav" aria-label="Human Use evidence navigation"><strong>Human Use</strong>' + ''.join('<a href="' + url + '"' + (' aria-current="page"' if key == active else '') + '>' + label + '</a>' for key, url, label in links) + '</nav>'


def move_publication_log():
    oxy_path = BASE / 'veterinary/Vet-03-publication-BHOC-Oxyglobin.html'
    news_path = ROOT / 'news/knowledge-updates/index.html'
    oxy, news = oxy_path.read_text(), news_path.read_text()
    section = re.search(r'<section id="literature-update-20261030"[\s\S]*?</section>', oxy)
    if section:
        content = section[0]
        content = content.replace('id="literature-update-20261030" class="panel"', 'id="oxyglobin-literature-20261030-details" class="publication-update-list"')
        content = re.sub(r'<div class="eyebrow">[\s\S]*?</div>', '', content, count=1)
        content = content.replace('<h3>', '<h4>').replace('</h3>', '</h4>')
        content = content.replace('<h2>23 source-linked publication records added</h2>', '<h3>23 source-linked publication records added</h3>')
        news = re.sub(r'<section id="oxyglobin-literature-20261030-details"[\s\S]*?</section>', '', news)
        article = re.search(r'<article class="timeline-item" id="oxyglobin-literature-20261030">[\s\S]*?</article>', news)
        assert article, 'Keep the dated literature-release entry'
        updated = article[0].replace('</div></article>', content + '</div></article>')
        assert content in updated
        news = news[:article.start()] + updated + news[article.end():]
        oxy = oxy[:section.start()] + oxy[section.end():]
    assert 'id="oxyglobin-literature-20261030-details"' in news
    oxy = re.sub(r'<p[^>]*id="literature-update-20261030"[\s\S]*?</p>', '', oxy)
    compact = '<p id="literature-update-20261030" class="catalogue-relationship"><a href="' + UPDATES + '">Publication updates →</a></p>'
    oxy = oxy.replace('</main>', compact + '\n</main>', 1)
    news = news.replace('/evidence/library/veterinary/Vet-03-publication-BHOC-Oxyglobin.html#literature-update-20261030', UPDATES)
    oxy_path.write_text(oxy)
    news_path.write_text(styled(news))


def apply_approved_registry_layout(set_metadata):
    move_publication_log()
    registry_path = ROOT / HUMAN.lstrip('/')
    registry = registry_path.read_text()
    registry = set_metadata(registry, title=ELECTRONIC_TITLE, description=ELECTRONIC_DESCRIPTION)
    old_intro = re.search(r'<main id="main" class="shell">[\s\S]*?(?=<section class="registry-summary")', registry)
    assert old_intro
    intro = '<main id="main" class="shell">' + context_nav('registry') + '<section class="page-intro"><p class="registry-location"><a href="/evidence/library/">Evidence Library</a> / <a href="BHOC-Human-index.html">Human Use</a> / <strong>ClinicalTrials.gov</strong></p><div class="eyebrow">Hemopure / HBOC-201 · Official electronic registry</div><h1>Electronically registered <br>clinical studies</h1><p>Clinical trials and expanded-access programmes recorded in the electronic ClinicalTrials.gov registry. Official NCT records, study types, status dates and source links are kept together here.</p></section>'
    registry = registry[:old_intro.start()] + intro + registry[old_intro.end():]
    registry = registry.replace('"name": "Registered clinical studies"', '"name": "Electronically registered clinical studies"')
    registry_path.write_text(styled(registry))

    hub_path = BASE / 'human/BHOC-Human-index.html'
    hub = hub_path.read_text()
    hub = re.sub(r'<!-- registered-studies-navigation:start -->[\s\S]*?<!-- registered-studies-navigation:end -->', '', hub)
    hub = re.sub(r'<!-- registry-entry:start -->[\s\S]*?<!-- registry-entry:end -->', '', hub)
    entry = '<section class="registry-entry" id="registered-studies" aria-labelledby="registry-entry-title"><div><div class="eyebrow">ClinicalTrials.gov · Official electronic registry</div><h2 id="registry-entry-title">Electronically registered clinical studies</h2><p>Hemopure / HBOC-201. Six interventional studies and three expanded-access records.</p></div><div class="registry-entry-count"><strong>9</strong><span>registry records</span></div><a class="registry-entry-button" href="registered-clinical-studies.html">Open registry →</a></section>'
    intro = re.search(r'<section class="page-intro overview-intro">[\s\S]*?</section>', hub)
    assert intro
    hub = hub[:intro.end()] + '\n<!-- registry-entry:start -->' + entry + '<!-- registry-entry:end -->\n' + hub[intro.end():]
    if 'href="registered-clinical-studies.html">Registered clinical studies →' not in hub:
        hub = hub.replace('href="BHOC-Human-search.html">Explore publications →</a>', 'href="BHOC-Human-search.html">Explore publications →</a><a class="button" href="registered-clinical-studies.html">Registered clinical studies →</a>', 1)
    hub_path.write_text(styled(hub))

    for relative, active in [('human/BHOC-Human-search.html', 'publications'), ('human/BHOC-Human-fda-expanded-access.html', 'access')]:
        path = BASE / relative
        source = path.read_text()
        source = re.sub(r'<nav class="registry-context-nav"[\s\S]*?</nav>', '', source)
        source = re.sub(r'(<main\b[^>]*>)', lambda m: m[1] + context_nav(active), source, count=1)
        path.write_text(styled(source))

    vet_path = BASE / 'veterinary/Vet-fda-ema.html'
    vet = vet_path.read_text()
    block = '''<section class="registry-vet-block" id="registered-veterinary-studies" aria-labelledby="vet-registry-title">
<div class="eyebrow">Oxyglobin · FDA / EMA</div><h2 id="vet-registry-title">Veterinary studies and electronic registration</h2>
<div class="registry-vet-grid"><div><span class="registry-vet-label">FDA pivotal clinical study · Anaemic dogs</span><div class="registry-vet-figures"><div><strong>64</strong><span>dogs enrolled</span></div><div><strong>30 / 34</strong><span>Oxyglobin / control</span></div></div><p><strong>24-hour endpoint:</strong> no additional oxygen-carrying support required. This was not a survival endpoint.</p><div class="registry-vet-links"><a href="https://animaldrugsatfda.fda.gov/adafda/app/search/public/document/downloadFoi/3700" target="_blank" rel="noopener noreferrer">FDA study summary · 12 Jan 1998 ↗</a><a href="https://www.ema.europa.eu/en/medicines/veterinary/EPAR/oxyglobin" target="_blank" rel="noopener noreferrer">EMA record ↗</a></div></div>
<div><span class="registry-vet-label">ClinicalTrials.gov · Electronic registry search</span><div class="registry-vet-figures"><div><strong>0</strong><span>matching Oxyglobin records</span></div></div><p>Checked 31 October 2026: Oxyglobin, HBOC-301, HBOC-200 and hemoglobin glutamer-200.</p><p>FDA/EMA study documents are regulatory evidence. <strong>NADA 141-067</strong> is an approval application number; neither this number nor an EMA authorisation is an NCT trial registration.</p></div></div>
<div class="registry-vet-scope"><p>ClinicalTrials.gov concerns studies in people. This search does not establish the absence of veterinary clinical or preclinical studies, or completeness across veterinary registries. The AVMA database search remains unverified. Published animal, organ and cell studies stay separately classified in the literature catalogue.</p><div class="registry-vet-links"><a href="data/oxyglobin-registry-scope.json">Search scope &amp; official sources</a><a href="https://medlineplus.gov/clinicaltrials.html" target="_blank" rel="noopener noreferrer">NLM: clinical trials ↗</a><a href="Vet-search.html">Publications by species →</a><a class="registry-other-route" href="../human/registered-clinical-studies.html">Human registered studies →</a></div></div></section>'''
    vet = replace_marker(vet, 'oxyglobin-registry', block)
    if 'href="#registered-veterinary-studies"' not in vet:
        vet = re.sub(r'(<nav class="vet-route-strip"[^>]*>)', r'\1<a href="#registered-veterinary-studies">Clinical studies &amp; registration ↓</a>', vet, count=1)
    vet_path.write_text(styled(vet))

    # All existing notice URLs now point directly to the update log. The old
    # Oxyglobin fragment remains available as a short forwarding explanation.
    for path in BASE.rglob('*.html'):
        source = path.read_text()
        changed = re.sub(r'((?:https://bhoctherapeutics.com)?/evidence/library/)?veterinary/Vet-03-publication-BHOC-Oxyglobin\.html#literature-update-20261030', UPDATES, source)
        if changed != source:
            path.write_text(changed)

    updates = json.loads((ROOT / 'site-release.json').read_text())['updates']
    for relative in ['evidence/library/human/BHOC-Human-index.html',
                     'evidence/library/human/BHOC-Human-search.html',
                     'evidence/library/human/BHOC-Human-fda-expanded-access.html',
                     'evidence/library/human/registered-clinical-studies.html',
                     'evidence/library/veterinary/Vet-fda-ema.html',
                     'evidence/library/veterinary/Vet-03-publication-BHOC-Oxyglobin.html',
                     'news/knowledge-updates/index.html']:
        path = ROOT / relative
        source = path.read_text()
        changed = source.replace('87 updates · Last updated 31 Oct 2026 · Version 26.10.31', f'{updates} updates · Last updated 31 Oct 2026 · Version 26.10.31')
        if changed != source:
            path.write_text(changed)
    clean_editorial_notes(set_metadata)


def clean_editorial_notes(set_metadata):
    """Keep research-process commentary out of public study and source pages."""
    registry_path = ROOT / HUMAN.lstrip('/')
    registry = registry_path.read_text()
    registry = re.sub(r'<section class="registry-summary"[\s\S]*?</section>', '', registry)
    registry = re.sub(r'<section class="panel registry-card registry-answers"[\s\S]*?</section>', '', registry)
    registry = re.sub(r'<p class="notice">[\s\S]*?</p>', '', registry)
    registry = registry.replace('<a href="#registry-questions">Questions and scope</a>', '')
    registry = registry.replace('Clinical trials and expanded-access programmes recorded in the electronic ClinicalTrials.gov registry. Official NCT records, study types, status dates and source links are kept together here.', 'Hemopure / HBOC-201. Clinical studies and expanded-access programmes registered in ClinicalTrials.gov.')
    registry = registry.replace('Registry overview. Open an NCT identifier for the full record summary.', 'ClinicalTrials.gov · Hemopure / HBOC-201')
    registry = registry.replace('6 interventional records', 'Interventional studies').replace('3 expanded-access records', 'Expanded access')
    registry = registry.replace('Six interventional records', 'Interventional studies').replace('Three expanded-access records', 'Expanded access')
    registry_path.write_text(registry)

    hub_path = BASE / 'human/BHOC-Human-index.html'
    hub = hub_path.read_text().replace('ClinicalTrials.gov · Official electronic registry', 'ClinicalTrials.gov')
    hub = hub.replace('Hemopure / HBOC-201. Six interventional studies and three expanded-access records.', 'Hemopure / HBOC-201')
    hub = hub.replace('<span>registry records</span>', '<span>ClinicalTrials.gov records</span>')
    hub = hub.replace('<dt>Human clinical records</dt>', '<dt>Human clinical publications</dt>')
    hub = hub.replace('<dt>Translational preclinical records</dt>', '<dt>Translational preclinical publications</dt>')
    hub_path.write_text(hub)

    home_path = BASE / 'index.html'
    home = home_path.read_text()
    home = re.sub(r'<div class="home-registry-entry"[\s\S]*?</div>', '', home)
    hero = re.search(r'<section class="home-hero">[\s\S]*?</section>', home)
    assert hero
    entry = '<div class="home-registry-entry" id="electronic-clinical-studies"><a href="/evidence/library/human/registered-clinical-studies.html">Electronically registered clinical studies →</a><span>Hemopure / HBOC-201 · ClinicalTrials.gov</span></div>'
    home = home[:hero.start()] + hero[0].replace('</section>', entry + '</section>') + home[hero.end():]
    home_path.write_text(styled(home))

    short_routes = {
        'human/BHOC-Human-fda-expanded-access.html': '<nav class="registry-context-nav" id="registered-studies" aria-label="ClinicalTrials.gov"><strong>ClinicalTrials.gov</strong><a href="registered-clinical-studies.html">Electronically registered clinical studies →</a></nav>',
        'human/BHOC-Human-search.html': '<p class="catalogue-relationship" id="registered-studies"><a href="registered-clinical-studies.html">ClinicalTrials.gov: registered clinical studies →</a></p>',
        'veterinary/Vet-index.html': '<nav class="registry-context-nav" id="registered-studies" aria-label="Clinical study sources"><strong>Clinical studies</strong><a href="Vet-fda-ema.html#registered-veterinary-studies">Oxyglobin · FDA / EMA →</a><a href="../human/registered-clinical-studies.html">Human registered clinical studies →</a></nav>',
        'veterinary/Vet-03-publication-BHOC-Oxyglobin.html': '<nav class="registry-context-nav" id="study-registration" aria-label="Clinical study sources"><a href="Vet-fda-ema.html#registered-veterinary-studies">Oxyglobin veterinary clinical study →</a><a href="../human/registered-clinical-studies.html">Human registered clinical studies →</a></nav>',
        'index.html': '<nav class="registry-context-nav" id="registered-studies" aria-label="Clinical study sources"><strong>Clinical studies</strong><a href="/evidence/library/human/registered-clinical-studies.html">Human electronic registry →</a><a href="/evidence/library/veterinary/Vet-fda-ema.html#registered-veterinary-studies">Veterinary clinical study →</a></nav>',
    }
    for relative, block in short_routes.items():
        path = BASE / relative
        source = replace_marker(path.read_text(), 'registered-studies-navigation', block)
        if relative.startswith('veterinary/Vet-03'):
            source = re.sub(r'<p class="notice">Evidence page updated [\s\S]*?</p>', '', source)
        path.write_text(styled(source))

    vet_path = BASE / 'veterinary/Vet-fda-ema.html'
    vet = vet_path.read_text()
    compact_study = '''<section class="registry-vet-block" id="registered-veterinary-studies" aria-labelledby="vet-registry-title"><div class="eyebrow">Oxyglobin · FDA regulatory documents</div><h2 id="vet-registry-title">Veterinary clinical study</h2><div class="registry-vet-grid"><div><span class="registry-vet-label">Anaemic dogs</span><div class="registry-vet-figures"><div><strong>64</strong><span>dogs enrolled</span></div><div><strong>30 / 34</strong><span>Oxyglobin / control</span></div></div></div><div><span class="registry-vet-label">Study endpoint</span><p>No additional oxygen-carrying support required during the first 24 hours.</p><p>FDA original approval summary · 12 January 1998</p></div></div><div class="registry-vet-links"><a href="https://animaldrugsatfda.fda.gov/adafda/app/search/public/document/downloadFoi/3700" target="_blank" rel="noopener noreferrer">FDA study report ↗</a><a href="https://www.ema.europa.eu/en/medicines/veterinary/EPAR/oxyglobin" target="_blank" rel="noopener noreferrer">EMA documents ↗</a><a href="Vet-search.html">Veterinary publications →</a><a class="registry-other-route" href="../human/registered-clinical-studies.html">Human registered studies →</a></div></section>'''
    vet = replace_marker(vet, 'oxyglobin-registry', compact_study)
    vet = vet.replace('Clinical studies &amp; registration ↓', 'Clinical study ↓')
    vet = set_metadata(vet, description='Official FDA and EMA regulatory documents for Oxyglobin, including the pivotal clinical study in 64 anaemic dogs and original approval source reports.')
    vet_path.write_text(vet)

    # The release history belongs in What's new, without repeating search and
    # verification notes throughout the reading and search interfaces.
    for path in BASE.rglob('*.html'):
        source = path.read_text()
        changed = re.sub(r'<p\b[^>]*data-literature-update="20261030"[^>]*>[\s\S]*?</p>', '', source)
        if changed != source:
            path.write_text(changed)
    news_path = ROOT / 'news/knowledge-updates/index.html'
    news = news_path.read_text()
    section = re.search(r'<section id="oxyglobin-literature-20261030-details"[\s\S]*?</section>', news)
    if section:
        listing = re.sub(r'<p>[\s\S]*?</p>', '', section[0])
        news = news[:section.start()] + listing + news[section.end():]
    news = news.replace(' Seven archival citations still await primary documents.', '')
    news = news.replace(' Registry records do not increase the publication count.', '')
    news_path.write_text(news)

    # Keep the two regulatory pages aligned with the surrounding Evidence Hub.
    for relative, body_class in [('veterinary/Vet-fda-ema.html', 'regulatory-source-page'),
                                 ('veterinary/Vet-EMA-approvals-summary.html', 'ema-regulatory-page')]:
        path = BASE / relative
        source = path.read_text()
        def add_class(match):
            names = match[2].split()
            if body_class not in names:
                names.append(body_class)
            return match[1] + ' '.join(names) + match[3]
        source = re.sub(r'(<body\b[^>]*class=")([^"]*)(")', add_class, source, count=1)
        if body_class == 'ema-regulatory-page':
            source = re.sub(r'<p class="notice">Archival source note\.[\s\S]*?</p>', '', source)
            source = source.replace(' This historical Oxyglobin record supports veterinary HBOC context; it does not establish approval of BHOC or another future formulation.', '')
        else:
            source = re.sub(r'<p class="notice">Historical approvals apply only to Oxyglobin[\s\S]*?</p>', '', source)
            source = source.replace(' Oxyglobin is a historical veterinary HBOC precedent; BHOC - Biological Hemoglobin Oxygen Carrier - is a developing category framework, not this approval.', '')
        path.write_text(styled(source))
