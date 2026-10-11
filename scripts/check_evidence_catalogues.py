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
print('PASS: one public catalogue source; no duplicate IDs, DOI or PMID; all 243 Oxygen Master source rows retained in the source archive.')
