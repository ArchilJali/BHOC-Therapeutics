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
assert link_audit['publicRecords']==len(RECORDS),'Source audit total mismatch'
for r in RECORDS:
    checked=link_audit['records'][r['id']]
    assert {c['url'] for c in checked['checks']}==set(r['urls']),r['id']+' source audit is stale'
    assert set(checked['publicLinks'])=={c['url'] for c in checked['checks'] if c['state'].startswith('matched')},r['id']+' source was not verified'
for kind,rows in VIEWS.items():
    source=(BASE/PATHS[kind]/'index.html' if PATHS[kind].endswith('/') else BASE/PATHS[kind]).read_text();page=Page(source);st=STATS[kind]
    assert {a['id'] for a in page.records}=={r['id'] for r in rows},kind+' record mismatch'
    assert len(page.records)==st['records'],kind+' total mismatch'
    assert len(page.ids)==len(set(page.ids)),kind+' duplicate HTML IDs'
    for metric in ['records','groups','institutions','journals']:
        if kind=='all' and metric=='records':
            assert f'data-metric="publicationCounter" data-publication-counter>{publication_counter()["displayedTotal"]}</strong>' in source
        else:
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
    assert ('aria-label="Search by application"' in source)==(kind in ['product','veterinary','human','transplant','all']),kind+' application navigation mismatch'
    assert 'href="/evidence/library/catalogues/"' in source,kind+' combined-search entry missing'
    for block in re.findall(r'<div class="source-links">([\s\S]*?)</div>',source):
        assert '?term=' not in block and 'Publication link' not in block,'Misleading source action'
    print(kind+': '+str(st['records'])+' records; statistics, facets, source links and structured data agree')

platform=json.loads((BASE/'platform-overview.json').read_text())
assert platform['uniquePublications']==sum(STATS[k]['records'] for k in ['product','oxygen','related'])
assert platform['hubs']=={k:STATS[k]['records'] for k in APP_LABELS}
for p in [BASE/'index.html',BASE/'science/index.html',ROOT/'evidence/index.html']:
    s=p.read_text();assert '48 incomplete imported fragments' not in s
    assert s.count('id="scientific-catalogues"')==1
assert len(VIEWS['human'])==180
assert sum(any(p['source']=='Human Use' for p in r['provenance']) for r in VIEWS['human'])==180
assert sum('Historical oxygen-carrier research' in r['collection'] for r in VIEWS['transplant'])==54
assert sum('Related transplantation studies' in r['collection'] for r in VIEWS['transplant'])==10
science=(BASE/'science/index.html').read_text();embedded=Page(science)
assert {a['id'] for a in embedded.records}=={r['id'] for r in VIEWS['related']},'Science / Related collection mismatch'
assert len(embedded.records)==len(VIEWS['related']) and len(embedded.ids)==len(set(embedded.ids))
assert science.index('class="nobel-feature"')<science.index('class="paper-card"')<science.index('id="scientific-catalogues"')
home=(BASE/'index.html').read_text()
combined=(BASE/'catalogues/index.html').read_text()
assert {a['id'] for a in Page(combined).records}=={r['id'] for r in RECORDS},'Combined search must contain every public record exactly once'
assert STATS['all']==TOTAL and len(VIEWS['all'])==len(RECORDS)
assert 'id="combined-applications" hidden' in combined,'Application shortcuts must start hidden in the combined search'
for kind in ['product','oxygen','related']:
    assert f'data-catalogue-filter="{kind}"' in combined,'Combined catalogue switch missing'
assert home.count('id="all-publications-entry"')==1 and 'Search all publications together' in home
reconciliation=count_reconciliation()
assert json.loads((BASE/'catalogues/data/count-reconciliation.json').read_text())==reconciliation
assert reconciliation['originalSourceRows']==475 and reconciliation['originalDistinctRecords']==334
assert reconciliation['netAddedRecords']==315
home_metrics=re.search(r'<section aria-label="Evidence Library statistics">([\s\S]*?)</section>',home)[1]
assert [int(v) for v in re.findall(r'<strong\b[^>]*>(\d+)</strong>',home_metrics)]==[publication_counter()['displayedTotal'],TOTAL['groups'],TOTAL['institutions'],TOTAL['journals']], 'Homepage statistics are stale'
for merged in DATA['mergedRecords']:
    old=merged['record'];target=next(r for r in RECORDS if r['id']==merged['retainedId'])
    assert old['id'] not in {r['id'] for r in RECORDS}
    assert old['id'] in target['aliases']
    assert all(p in target['provenance'] for p in old['provenance']), 'Merged source provenance lost'
    original_page=(BASE/PATHS[old['catalogue']]).read_text()
    assert 'id="'+old['id']+'"' in original_page, 'Old publication anchor lost'
    if target['catalogue']!=old['catalogue']:
        assert PATHS[target['catalogue']]+'#'+target['id'] in original_page,'Cross-catalogue alias lost'
assert home.index('class="regulatory-strip"')<home.index('id="evidence-hubs"')<home.index('id="scientific-catalogues"')
assert json.loads((ROOT/'site-release.json').read_text())==json.loads((BASE/'version.json').read_text()),'Release counter mismatch'
print('PASS: Science and Related expose the same collection; application hubs stay together; release counters agree.')
print('PASS: all 475 legacy source rows map to 334 distinct records; 315 net additions; all 1,189 source occurrences retained.')
print('PASS: one public catalogue source; no duplicate IDs, DOI or PMID; all 243 Oxygen Master source rows retained in the source archive.')

coverage=json.loads((BASE/'catalogues/data/source-coverage.json').read_text())
assert coverage['publicRecords']==len(RECORDS) and coverage['missingSourceRows']==0
assert coverage['sourceOccurrences']==sum(len(r['provenance']) for r in ALL_RECORDS)
assert coverage['retainedRecordsIncludingFragments']==len(ALL_RECORDS)
assert coverage['catalogues']=={k:len(VIEWS[k]) for k in ['product','oxygen','related']}

collection_stats=collection_totals()
assert collection_stats['entries']==974
assert collection_stats['collections']=={'transplant':64,'human':180,'veterinary':273,'oxygen':244,'related':213}
assert collection_stats['distinctRecordsInFiveCollections']==640
assert len(collection_stats['additionalProductRecordIds'])==9
assert collection_stats['distinctRecordsInFullLibrary']==len(RECORDS)
for source in [home,combined]:
    assert 'data-publication-counter>968</strong>' in source
    assert 'Library entries' in source
    assert 'Distinct publications' not in source
    for kind in COLLECTIONS:
        assert 'data-collection-link="'+kind+'"' in source
assert "{name: 'Evidence', href: '/evidence/library/catalogues/', path: '/evidence/'}" in (ROOT/'unified-shell.js').read_text()
assert publication_counter()['baseline']==962 and publication_counter()['newPublications']==6
assert set(publication_counter()['newRecordIds'])=={'pub-pmid-12683610','pub-pmid-1111380','pub-pmid-3740627','pub-pmid-19430240','pub-pmid-24612155','pub-muir-oc99-2014'}
assert len([r for r in RECORDS if r['doi']=='10.1111/j.1939-1676.2003.tb02423.x'])==1
assert any(r['pmid']=='12683610' for r in VIEWS['veterinary']) and any(r['pmid']=='12683610' for r in VIEWS['oxygen'])
print('PASS: displayed publication counter 962 + six distinct additions = 968; records indexed once.')

selection=read('catalogues/data/oxygen-transport-review-20261014.json')
assert selection['requestedPublications']==30 and selection['newPublications']==27 and selection['alreadyPublished']==3
assert selection['newByCatalogue']=={'oxygen':22,'related':5}
for selected in selection['records']:
    matched=[r for r in RECORDS if r['pmid']==selected['pmid']]
    assert len(matched)==1 and matched[0]['id']==selected['recordId'], 'Requested publication missing or duplicated'
    assert matched[0]['doi'].casefold()==selected['doi'].casefold()
    assert matched[0]['topics']==selected['topics']
assert len(selection['researchDirections'])==6
assert all('data-topic=' in (BASE/PATHS[k]/'index.html' if PATHS[k].endswith('/') else BASE/PATHS[k]).read_text() for k in ['all','oxygen','related','veterinary'])
print('PASS: all 30 requested publications are indexed once; 27 additions, 3 existing; six research directions are searchable.')
