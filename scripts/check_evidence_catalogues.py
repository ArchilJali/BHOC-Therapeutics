"""Audit public counts, rendered records, metadata and application navigation."""
import json,re
from html.parser import HTMLParser
from evidence_catalogue_model import *

class Page(HTMLParser):
    def __init__(self,source):
        super().__init__();self.records=[];self.ids=[];self.feed(source)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.append(a['id'])
        if tag=='article' and a.get('class')=='publication':self.records.append(a)

audit()
link_audit=json.loads((BASE/'catalogues/data/source-link-audit.json').read_text())
assert set(link_audit['records'])=={r['id'] for r in RECORDS},'Source audit coverage mismatch'
for r in RECORDS:
    checked=link_audit['records'][r['id']]
    assert {c['url'] for c in checked['checks']}==set(r['urls']),r['id']+' source audit is stale'
    assert set(checked['publicLinks'])=={c['url'] for c in checked['checks'] if c['state'].startswith('matched')},r['id']+' source was not verified'
for kind,rows in VIEWS.items():
    source=(BASE/PATHS[kind]).read_text();page=Page(source);st=STATS[kind]
    assert {a['id'] for a in page.records}=={r['id'] for r in rows},kind+' record mismatch'
    assert len(page.records)==st['records'],kind+' total mismatch'
    assert len(page.ids)==len(set(page.ids)),kind+' duplicate HTML IDs'
    for metric in ['records','groups','institutions','journals']:
        assert f'data-metric="{metric}">{st[metric]}</strong>' in source,kind+' metric mismatch '+metric
    assert 'incomplete imported fragments' not in source and 'data-status="fragment"' not in source,kind+' internal import text exposed'
    canonical=re.findall(r'<link rel="canonical" href="([^"]+)"',source)
    assert canonical==['https://bhoctherapeutics.com/evidence/library/'+PATHS[kind]],kind+' canonical mismatch'
    schemas=[json.loads(s) for s in re.findall(r'<script type="application/ld\+json"[^>]*>([\s\S]*?)</script>',source)]
    listing=schemas[0]['@graph'][0]['mainEntity']
    assert listing['numberOfItems']==len(page.records)==len(listing['itemListElement']),kind+' schema count mismatch'
    group='species' if st['groupField']=='speciesGroups' else st['groupField']
    computed={k:len({v.casefold() for a in page.records for v in a.get('data-'+f,'').split('|') if v}) for k,f in [('groups',group),('institutions','institution'),('journals','journal')]}
    assert all(computed[k]==st[k] for k in computed),kind+' rendered facet counts mismatch'
    assert not re.search(r'href="https?://(?:10\.|doi:|bateman)',source,re.I),kind+' malformed source link'
    assert ('aria-label="Search by application"' in source)==(kind in ['product','veterinary','human','transplant']),kind+' application navigation mismatch'
    for block in re.findall(r'<div class="source-links">([\s\S]*?)</div>',source):
        assert '?term=' not in block and 'Publication link' not in block,'Misleading source action'
    print(kind+': '+str(st['records'])+' records; statistics, facets, source links and structured data agree')

platform=json.loads((BASE/'platform-overview.json').read_text())
assert platform['uniquePublications']==sum(STATS[k]['records'] for k in ['product','oxygen','related'])
assert platform['hubs']=={k:STATS[k]['records'] for k in APP_LABELS}
for p in [BASE/'index.html',BASE/'science/index.html',ROOT/'evidence/index.html']:
    s=p.read_text();assert '48 incomplete imported fragments' not in s
    assert s.count('id="scientific-catalogues"')==1
assert len(VIEWS['human'])==181
assert sum(any(p['source']=='Human Use' for p in r['provenance']) for r in VIEWS['human'])==181
assert sum('Historical oxygen-carrier research' in r['collection'] for r in VIEWS['transplant'])==54
assert sum('Related transplantation studies' in r['collection'] for r in VIEWS['transplant'])==8
science=(BASE/'science/index.html').read_text();embedded=Page(science)
assert {a['id'] for a in embedded.records}=={r['id'] for r in VIEWS['related']},'Science / Related collection mismatch'
assert len(embedded.records)==len(VIEWS['related']) and len(embedded.ids)==len(set(embedded.ids))
assert science.index('class="nobel-feature"')<science.index('class="paper-card"')<science.index('id="scientific-catalogues"')
home=(BASE/'index.html').read_text()
assert home.index('class="regulatory-strip"')<home.index('id="evidence-hubs"')<home.index('id="scientific-catalogues"')
assert json.loads((ROOT/'site-release.json').read_text())==json.loads((BASE/'version.json').read_text()),'Release counter mismatch'
print('PASS: Science and Related expose the same collection; application hubs stay together; release counters agree.')
print('PASS: one public catalogue source; no duplicate IDs, DOI or PMID; all 243 Oxygen Master source rows retained in the source archive.')
