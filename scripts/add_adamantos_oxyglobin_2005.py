"""Add the user-approved Adamantos et al. review without duplicating publications.

Source: In Practice 2005;27(8):399-405, DOI 10.1136/inpract.27.8.399.
Bibliography and publisher abstract checked 2026-11-02; full text not reviewed.
Run before build_evidence_catalogues.py and sync_evidence_overviews.py.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
DP = ROOT / 'evidence/library/catalogues/data'
DATE = '2026-11-02'
DOI = '10.1136/inpract.27.8.399'
RID = 'pub-doi-10-1136-inpract-27-8-399'
AID = 'adamantos-2005-oxyglobin-clinical-review'
TITLE = 'Clinical use of a haemoglobin-based oxygen-carrying solution in dogs and cats'
AUTHORS = 'Sophie Adamantos; Amanda Boag; Dez Hughes'
RELEASE = 'adamantos-oxyglobin-review-20261102'
URLS = ['https://doi.org/' + DOI,
        'https://bvajournals.onlinelibrary.wiley.com/doi/abs/' + DOI]
SUMMARY = ('Clinical-practice review of historical Oxyglobin use in dogs and cats, '
           'discussing clinical applications and limitations from the authors\' experience. '
           'This is a review, not an independent controlled efficacy trial. '
           'Bibliography and publisher abstract verified; full text not reviewed.')
REVIEW = ('Publisher metadata and abstract verified on 2 November 2026; Crossref '
          'confirms all three authors and the DOI. BHOC Source Guard found no author '
          'stop-list match; this is not a scientific-validity assessment. Full text '
          'remains unreviewed. No numerical treatment outcomes are extracted from '
          'the abstract. Discussion of cats does not establish a licensed feline indication.')

def load(name):
    return json.loads((DP / name).read_text())

def save(name, value):
    (DP / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def norm_doi(value):
    return str(value or '').strip().lower().removeprefix('https://doi.org/').removeprefix('http://dx.doi.org/')

def norm_title(value):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', str(value)).casefold())

def main():
    data = load('publications.json')
    approved = load('approved-scientific-additions.json')
    audit = load('source-link-audit.json')
    existing = [r for r in data['records'] if norm_doi(r.get('doi')) == DOI or norm_title(r.get('title', '')) == norm_title(TITLE)]
    if existing:
        assert len(existing) == 1, 'Existing duplicate identities require review'
        print(json.dumps({'inserted': 0, 'existingId': existing[0]['id'], 'doi': DOI}))
        return
    assert not any(r['id'] == RID for r in data['records']), 'Record ID collision'
    assert not any(norm_doi(r.get('doi')) == DOI or r['id'] == AID for r in approved['records']), 'Approved-only entry requires reconciliation'
    old_records = deepcopy(data['records'])
    old_approved = deepcopy(approved['records'])
    original_ids = {r['id'] for r in old_records}
    entry = dict(id=AID, title=TITLE, year='2005', authors=AUTHORS,
                 journal='In Practice', doi=DOI, pmid='',
                 product='Oxyglobin (HBOC-301; Biopure)',
                 topics=['Oxyglobin', 'Veterinary anemia', 'Clinical practice', 'Oxygen-carrying solutions'],
                 directions=['Veterinary'], institutions=[], species=['Dog', 'Cat'],
                 evidenceType='Clinical practice review', catalogue='product',
                 metadataSources=URLS,
                 originalVerification='Publisher bibliography and abstract verified; full text not reviewed',
                 sourceReview=REVIEW, catalogueSummary=SUMMARY, release=RELEASE,
                 citation='Adamantos S, Boag A, Hughes D. ' + TITLE + '. In Practice. 2005;27(8):399-405. doi:' + DOI,
                 datePublished='2005-09-01', verified=DATE,
                 requestedSource='https://www.ovid.com/journals/ipcevp/abstract/10.1136/inpract.27.8.399~clinical-use-of-a-haemoglobinbased-oxygencarrying-solution?redirectionsource=fulltextview')
    row = dict(id=RID, title=TITLE, year='2005', authors=AUTHORS,
               journal='In Practice', doi=DOI, pmid='', citation=entry['citation'],
               product=entry['product'], keywords='; '.join(entry['topics']),
               directions=entry['directions'], institutions=[], species=entry['species'],
               evidence=entry['evidenceType'], urls=URLS, notes=[],
               provenance=[dict(source='Approved scientific additions', row=AID,
                                title=TITLE, year='2005', doi=DOI, pmid='')],
               originalVerification=entry['originalVerification'], sourceReview=REVIEW,
               catalogue='product', classificationBasis='User-approved historical Oxyglobin clinical-practice review; not a controlled trial or evidence of a new BHOC formulation.',
               verification='Publisher metadata and abstract verified', recordType='Bibliographic record',
               topics=entry['topics'], titleAliases=[], catalogueSummary=SUMMARY,
               cohortLinks=[], added=DATE, release=RELEASE)
    approved['records'].append(entry)
    data['records'].append(row)
    data['updated'] = DATE
    audit['records'][RID] = dict(publicLinks=URLS,
        checks=[dict(url=u, state='matched', method='DOI and full authorship verified through Crossref; publisher metadata and abstract checked; full text not reviewed', sourceTitle=TITLE) for u in URLS])
    public = [r for r in data['records'] if not r['recordType'].startswith('Import')]
    audit['publicRecords'] = len(public)
    audit['uniqueUrlsChecked'] = len({c['url'] for a in audit['records'].values() for c in a['checks']})
    audit['states'] = dict(Counter(c['state'] for a in audit['records'].values() for c in a['checks']))
    audit['checked'] = DATE
    coverage = load('source-coverage.json')
    total_sources = sum(len(r['provenance']) for r in data['records'])
    repeated = total_sources - len(data['records'])
    fragments = len(data['records']) - len(public)
    coverage.update(checked=DATE, sourceOccurrences=total_sources,
        retainedRecordsIncludingFragments=len(data['records']), publicRecords=len(public),
        repeatedSourceOccurrences=repeated, incompleteSourceFragments=fragments,
        catalogues=dict(Counter(r['catalogue'] for r in public)),
        calculation=f'{total_sources} source occurrences - {repeated} repeated occurrences - {fragments} incomplete fragments = {len(public)} public records')
    for source in coverage.get('sources', []):
        if source.get('source') == 'Approved scientific additions':
            source.update(rows=len(approved['records']), retainedRows=len(approved['records']), missingRows=0)
    assert data['records'][:-1] == old_records, 'An existing publication was changed'
    assert approved['records'][:-1] == old_approved, 'An existing approved source was changed'
    assert original_ids < {r['id'] for r in data['records']}, 'An existing publication was removed'
    # Advance only the exact release-count expectations affected by this one record.
    check_path = ROOT / 'scripts/check_evidence_catalogues.py'
    checks = check_path.read_text()
    replacements = {
        "reconciliation['netAddedRecords']==341": "reconciliation['netAddedRecords']==342",
        '341 net additions': '342 net additions',
        "collection_stats['entries']==1025": "collection_stats['entries']==1026",
        "'veterinary':294": "'veterinary':295",
        "collection_stats['distinctRecordsInFiveCollections']==666": "collection_stats['distinctRecordsInFiveCollections']==667",
        'data-publication-counter>994</strong>': 'data-publication-counter>995</strong>',
        "publication_counter()['newPublications']==32": "publication_counter()['newPublications']==33",
        "'pub-pmid-39407836'}|oxy_ids": "'pub-pmid-39407836'}|oxy_ids|{'" + RID + "'}",
        'len(ALL_RECORDS)==723 and len(RECORDS)==675': 'len(ALL_RECORDS)==724 and len(RECORDS)==676',
        '<strong>204</strong><span>Publication records</span>': '<strong>205</strong><span>Publication records</span>',
    }
    for old, new in replacements.items():
        assert checks.count(old) == 1, 'Unexpected catalogue baseline: ' + old
        checks = checks.replace(old, new, 1)
    checks += ('\n# User-approved Adamantos clinical-practice review; retain the evidence boundary.\n'
               "adamantos = [r for r in RECORDS if r['doi'] == '" + DOI + "']\n"
               "assert len(adamantos) == 1 and adamantos[0]['id'] == '" + RID + "'\n"
               "assert adamantos[0]['catalogue'] == 'product' and adamantos[0]['directions'] == ['Veterinary']\n"
               "assert adamantos[0]['evidence'] == 'Clinical practice review'\n"
               "assert 'full text not reviewed' in adamantos[0]['catalogueSummary'].lower()\n")
    for name, value in [('publications.json', data), ('approved-scientific-additions.json', approved),
                        ('source-link-audit.json', audit), ('source-coverage.json', coverage)]:
        save(name, value)
    check_path.write_text(checks)
    print(json.dumps({'inserted': 1, 'id': RID, 'doi': DOI, 'publicRecords': len(public),
                      'existingRecordsPreserved': len(old_records), 'fullTextReviewed': False}))

if __name__ == '__main__':
    main()
