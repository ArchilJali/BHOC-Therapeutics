"""Incorporate the user-approved 30 October Oxyglobin literature review.

The approved source file contains all publication metadata and classifications.
This import preserves existing records and anchors and is idempotent by PMID/DOI.
Run before build_evidence_catalogues.py and sync_evidence_overviews.py.
"""
from collections import Counter
from pathlib import Path
import json, re

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'evidence/library'
DP=BASE/'catalogues/data'
RELEASE='oxyglobin-literature-20261030'
DATA=json.loads((DP/'publications.json').read_text())
APPROVED=json.loads((DP/'approved-scientific-additions.json').read_text())
AUDIT=json.loads((DP/'source-link-audit.json').read_text())
selected=[r for r in APPROVED['records'] if r.get('release')==RELEASE]
assert len(selected)==23, 'The approved batch must contain exactly 23 publications'
start_public=sum(not r['recordType'].startswith('Import') for r in DATA['records'])
start_ids={r['id'] for r in DATA['records']}
old_snapshot=json.loads(json.dumps(DATA['records']))
inserted=[];release_rows=[]
for a in selected:
 existing=[r for r in DATA['records'] if (a['pmid'] and r.get('pmid')==a['pmid']) or (a['doi'] and r.get('doi','').casefold()==a['doi'].casefold())]
 assert len(existing)<=1, 'Duplicate publication identity'
 rid=existing[0]['id'] if existing else 'pub-pmid-'+a['pmid'] if a['pmid'] else 'pub-oxyglobin-berent-2005'
 if not existing:
  urls=list(dict.fromkeys(a['metadataSources']))
  row=dict(id=rid,title=a['title'],year=a['year'],authors=a['authors'],journal=a['journal'],doi=a['doi'],pmid=a['pmid'],citation=a['authors']+'. '+a['title']+'. '+a['journal']+'. '+a['year']+'.',product=a['product'],keywords='; '.join(a['topics']),directions=a['directions'],institutions=a['institutions'],species=a['species'],evidence=a['evidenceType'],urls=urls,notes=[],provenance=[{'source':'Approved scientific additions','row':a['id'],'title':a['title'],'year':a['year'],'doi':a['doi'],'pmid':a['pmid']}],originalVerification=a['originalVerification'],sourceReview=a['sourceReview'],catalogue=a['catalogue'],classificationBasis='User-approved literature review. Product-associated studies retain their tested formulation and design. Other formulations, indirect clinical context and unconfirmed commercial formulations remain Related Scientific Articles.',verification='PubMed metadata verified' if a['pmid'] else 'Publisher metadata verified',recordType='Bibliographic record',topics=a['topics'],titleAliases=[],catalogueSummary=a['catalogueSummary'],cohortLinks=a.get('cohortLinks',[]),added='2026-10-30',release=RELEASE)
  if a.get('sourceJournal'):row['sourceJournal']=a['sourceJournal']
  DATA['records'].append(row)
  AUDIT['records'][rid]={'publicLinks':urls,'checks':[{'url':u,'state':'matched','method':'Indexed PubMed/PMC identity or publisher DOI metadata; access level documented in publication note','sourceTitle':a['title']} for u in urls]}
  inserted.append(rid)
 release_rows.append({'id':rid,'pmid':a['pmid'],'doi':a['doi'],'title':a['title'],'year':a['year'],'catalogue':a['catalogue'],'applications':a['directions'],'evidenceType':a['evidenceType']})
assert DATA['records'][:len(old_snapshot)]==old_snapshot, 'Existing source records changed'
DATA['updated']='2026-10-30'
AUDIT['checked']='2026-10-30';AUDIT['publicRecords']=sum(not r['recordType'].startswith('Import') for r in DATA['records'])
AUDIT['uniqueUrlsChecked']=len({c['url'] for a in AUDIT['records'].values() for c in a['checks']})
AUDIT['states']=dict(Counter(c['state'] for a in AUDIT['records'].values() for c in a['checks']))
for path,value in [(DP/'publications.json',DATA),(DP/'source-link-audit.json',AUDIT)]:path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
release={'id':RELEASE,'date':'2026-10-30','approval':'User authorized adding missing publications, updating counters and documenting additions.','newPublications':23,'previousPublicRecords':651,'publicRecords':674,'previousDisplayedCounter':970,'displayedCounter':993,'newByCatalogue':dict(Counter(a['catalogue'] for a in selected)),'newByApplication':{label:sum(label in a['directions'] for a in selected) for label in ['Veterinary','Human Use','Transplant']},'records':release_rows,'deferredArchiveCandidates':7,'note':'The seven unverified archival citations are not added as verified publications or independent trials. Counts refer to publication records, including reviews and a conference abstract. Registry lists are prepared separately and have not been published.'}
(DP/'oxyglobin-literature-review-20261030.json').write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n')

# Original workbook provenance remains intact; update the aggregate coverage.
coverage=json.loads((DP/'source-coverage.json').read_text())
coverage.update(checked='2026-10-30',sourceOccurrences=sum(len(r['provenance']) for r in DATA['records']),retainedRecordsIncludingFragments=len(DATA['records']),publicRecords=AUDIT['publicRecords'],catalogues=dict(Counter(r['catalogue'] for r in DATA['records'] if not r['recordType'].startswith('Import'))))
coverage['repeatedSourceOccurrences']=coverage['sourceOccurrences']-len(DATA['records'])
coverage['incompleteSourceFragments']=len(DATA['records'])-AUDIT['publicRecords']
coverage['calculation']=f"{coverage['sourceOccurrences']} source occurrences - {coverage['repeatedSourceOccurrences']} repeated occurrences - {coverage['incompleteSourceFragments']} incomplete fragments = {coverage['publicRecords']} public records"
source_count=Counter(p['source'] for r in DATA['records'] for p in r['provenance'])
for source in coverage.get('sources',[]):
 if source.get('source')=='Approved scientific additions':source.update(rows=source_count['Approved scientific additions'],retainedRows=source_count['Approved scientific additions'],missingRows=0)
(DP/'source-coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')

release_path=ROOT/'site-release.json';site_release=json.loads(release_path.read_text())
if site_release['updated_iso']!='2026-10-30':
 site_release.update(version='26.10.30',updates=site_release['updates']+1,updated='30 Oct 2026',updated_iso='2026-10-30')
for path in [release_path,BASE/'version.json']:path.write_text(json.dumps(site_release,indent=2)+'\n')
summary=f"First published {site_release['first_published']} · {site_release['updates']} updates · Last updated {site_release['updated']} · Version {site_release['version']}"
shell=ROOT/'unified-shell.js'
shell.write_text(re.sub(r"const releaseSummary = '[^']+';",lambda m:"const releaseSummary = '"+summary+"';",shell.read_text()))

# Add a dated item to the existing public knowledge-update timeline.
timeline=ROOT/'news/knowledge-updates/index.html'
text=timeline.read_text()
entry='<article class="timeline-item" id="oxyglobin-literature-20261030"><div class="timeline-date"><time datetime="2026-10-30">30 October 2026</time><span>Evidence · Literature review</span></div><div class="timeline-copy"><h2>23 source-linked publications added to the evidence library</h2><p>Expanded the Oxyglobin literature review with clinical reports, preclinical studies, monitoring methods, reviews and formulation context. Added 12 product-associated records and 11 related scientific records. Existing publications and original source links were retained; application counters and the shared library total were synchronized. Seven archival citations still await primary documents.</p><div class="timeline-links"><a href="/evidence/library/veterinary/Vet-03-publication-BHOC-Oxyglobin.html#literature-update-20261030">See all 23 additions →</a><a href="/evidence/library/catalogues/">Search the updated library →</a></div></div></article>'
text=re.sub(r'<article class="timeline-item" id="oxyglobin-literature-20261030">[\s\S]*?</article>','',text)
text=text.replace('<section class="timeline" aria-label="October 2026 BHOC knowledge updates">','<section class="timeline" aria-label="October 2026 BHOC knowledge updates">\n'+entry,1)
text=re.sub(r'"dateModified":"\d{4}-\d{2}-\d{2}"','"dateModified":"2026-10-30"',text,count=1)
timeline.write_text(text)
print(json.dumps({'inserted':len(inserted),'ids':inserted,'publicRecords':AUDIT['publicRecords'],'newByCatalogue':release['newByCatalogue'],'newByApplication':release['newByApplication']}))
