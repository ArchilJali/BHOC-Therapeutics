"""User-approved feline bibliography reconciliation; no treatment instructions.
Run on a preview branch before build_evidence_catalogues.py and
sync_evidence_overviews.py. Existing identities/provenance are preserved.
"""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import json
import re
import subprocess
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
DP = ROOT / 'evidence/library/catalogues/data'
DATE = '2026-11-03'
RELEASE = 'feline-catalogue-20261103'
MANIFEST = 'feline-literature-review-20261103.json'
CITING = 'https://journals.sagepub.com/doi/10.1016/j.jfms.2007.10.012'


def load(name):
    return json.loads((DP / name).read_text())


def save(name, value):
    (DP / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def norm(value):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', str(value or '')).casefold())


def snapshot():
    code = "import sys,json;sys.path.insert(0,'scripts');from evidence_catalogue_model import *;print(json.dumps({'audit':audit(),'allRecords':len(ALL_RECORDS),'netAddedRecords':count_reconciliation()['netAddedRecords'],'feline':sum('Feline (Cat)' in r['speciesGroups'] for r in VIEWS['veterinary'])}))"
    return json.loads(subprocess.check_output([sys.executable, '-c', code], cwd=ROOT, text=True))


def entry(key, title, year, authors, journal, doi, pmid, catalogue, evidence, product, summary, urls, citation, archive=False, review=''):
    return dict(key=key, title=title, year=str(year), authors=authors, journal=journal,
                doi=doi, pmid=pmid, catalogue=catalogue, evidence=evidence,
                product=product, summary=summary, urls=urls, citation=citation,
                archive=archive, review=review)


ADDITIONS = [
    entry('maldonado-moreno-2023-pima',
          'Clinical findings, treatment and outcome in cats diagnosed with precursor-targeted immune-mediated anaemia in a referral hospital in the UK: 30 cases (2010-2021)',
          2023, 'Alba Maldonado-Moreno; Mayank Seth; Paola Monti; Rachel Miller',
          'Veterinary Record Open', '10.1002/vro2.70', '37645469', 'product',
          'Retrospective clinical series', 'Oxyglobin',
          'Retrospective series of 30 cats with precursor-targeted immune-mediated anaemia. Oxyglobin was used in a subset alongside other care. The entire cohort is not an Oxyglobin-treated cohort, and this was not a controlled trial of the carrier.',
          ['https://pubmed.ncbi.nlm.nih.gov/37645469/', 'https://doi.org/10.1002/vro2.70'],
          'Maldonado-Moreno A, Seth M, Monti P, Miller R. Clinical findings, treatment and outcome in cats diagnosed with precursor-targeted immune-mediated anaemia in a referral hospital in the UK: 30 cases (2010-2021). Vet Rec Open. 2023;10(2):e70. doi:10.1002/vro2.70.'),
    entry('barfield-adamantos-2011-transfusions',
          'Feline blood transfusions: A pinker shade of pale',
          2011, 'Dominic Barfield; Sophie Adamantos', 'Journal of Feline Medicine and Surgery',
          '10.1016/j.jfms.2010.11.006', '21215945', 'related', 'Clinical review', '',
          'Clinical review of feline transfusion practice, including historical discussion of haemoglobin-based oxygen carriers. This is clinical context, not a new Oxyglobin patient cohort or evidence of efficacy of a new BHOC formulation.',
          ['https://pubmed.ncbi.nlm.nih.gov/21215945/', 'https://doi.org/10.1016/j.jfms.2010.11.006'],
          'Barfield D, Adamantos S. Feline blood transfusions: A pinker shade of pale. J Feline Med Surg. 2011;13(1):11-23. doi:10.1016/j.jfms.2010.11.006.'),
    entry('rebel-2002-cerebral-ischaemia',
          'Regional cerebral blood flow in cats with cross-linked hemoglobin transfusion during focal cerebral ischemia',
          2002, 'Annette Rebel; John A Ulatowski; Karena Joung; Enrico Bucci; Richard J Traystman; Raymond C Koehler',
          'American Journal of Physiology - Heart and Circulatory Physiology',
          '10.1152/ajpheart.00880.2001', '11834476', 'oxygen', 'Experimental animal study',
          'Tetrameric cross-linked haemoglobin; not Oxyglobin',
          'Experimental feline study of regional cerebral blood flow and oxygen transport during focal ischaemia. The carrier was a different cross-linked haemoglobin, not Oxyglobin. The study must not be represented as clinical evidence for Oxyglobin or BHOC.',
          ['https://pubmed.ncbi.nlm.nih.gov/11834476/', 'https://doi.org/10.1152/ajpheart.00880.2001'],
          'Rebel A, Ulatowski JA, Joung K, Bucci E, Traystman RJ, Koehler RC. Regional cerebral blood flow in cats with cross-linked hemoglobin transfusion during focal cerebral ischemia. Am J Physiol Heart Circ Physiol. 2002;282(3):H832-H841. doi:10.1152/ajpheart.00880.2001.'),
    entry('rebel-2003-cerebrovascular-response',
          'Cerebrovascular response to decreased hematocrit: effect of cell-free hemoglobin, plasma viscosity, and CO2',
          2003, 'Annette Rebel; John A Ulatowski; Herman Kwansa; Enrico Bucci; Raymond C Koehler',
          'American Journal of Physiology - Heart and Circulatory Physiology',
          '10.1152/ajpheart.00077.2003', '12816746', 'oxygen', 'Experimental animal study',
          'Zero-link haemoglobin polymer; not Oxyglobin',
          'Experimental feline study of cerebrovascular responses to cell-free haemoglobin and plasma viscosity. A zero-link haemoglobin polymer was studied, not Oxyglobin. This is mechanistic physiology rather than evidence of clinical efficacy of BHOC.',
          ['https://pubmed.ncbi.nlm.nih.gov/12816746/', 'https://doi.org/10.1152/ajpheart.00077.2003'],
          'Rebel A, Ulatowski JA, Kwansa H, Bucci E, Koehler RC. Cerebrovascular response to decreased hematocrit: effect of cell-free hemoglobin, plasma viscosity, and CO2. Am J Physiol Heart Circ Physiol. 2003;285(4):H1600-H1608. doi:10.1152/ajpheart.00077.2003.'),
    entry('taylor-2021-isfm-guidelines',
          '2021 ISFM Consensus Guidelines on the Collection and Administration of Blood and Blood Products in Cats',
          2021, 'Samantha Taylor; Eva Spada; Mary Beth Callan; Rachel Korman; Ellie Leister; Paulo Steagall; Remo Lobetti; Mayank Seth; Séverine Tasker',
          'Journal of Feline Medicine and Surgery', '10.1177/1098612X211007071', '', 'related',
          'Consensus guidelines', '',
          'ISFM consensus guidance on feline blood and blood products. Included as transfusion-medicine context, not an independent Oxyglobin trial or evidence of BHOC efficacy. Read together with the publisher-linked corrigendum, DOI 10.1177/1098612X221149363.',
          ['https://doi.org/10.1177/1098612X211007071', 'https://journals.sagepub.com/doi/10.1177/1098612X211007071'],
          'Taylor S, Spada E, Callan MB, Korman R, Leister E, Steagall P, Lobetti R, Seth M, Tasker S. 2021 ISFM Consensus Guidelines on the Collection and Administration of Blood and Blood Products in Cats. J Feline Med Surg. 2021;23(5):410-432. doi:10.1177/1098612X211007071.'),
    entry('crystal-1999-no-matching-donor', 'Blood loss and no matching donor',
          1999, 'M A Crystal; J Mott; P Van der Veldt', 'Veterinary Forum', '', '', 'related',
          'Archival bibliographic citation - original not reviewed', '',
          'Archival citation identified in the references of Weingart and Kohn (2008). The original report, complete author identities and formulation have not been independently verified. Retained for historical discovery only; not evidence of product efficacy.', [],
          'Crystal MA, Mott J, Van der Veldt P. Blood loss and no matching donor. Veterinary Forum. 1999;16:72-73. [Citation transcribed from Weingart and Kohn, 2008; original not obtained.]', True,
          'Citation-only source: ' + CITING + '. No verified original article URL or DOI/PMID is available. Do not treat the citing article as the original case report.'),
    entry('nolte-1999-acetaminophen', 'Cyanosis from acetaminophen toxicosis',
          1999, 'D M Nolte; A Crovatto', 'Veterinary Forum', '', '', 'related',
          'Archival bibliographic citation - original not reviewed', '',
          'Archival citation identified in the references of Weingart and Kohn (2008). The original report, complete author identities and formulation have not been independently verified. Retained for historical discovery only; not evidence of product efficacy.', [],
          'Nolte DM, Crovatto A. Cyanosis from acetaminophen toxicosis. Veterinary Forum. 1999;16:55-57. [Citation transcribed from Weingart and Kohn, 2008; original not obtained.]', True,
          'Citation-only source: ' + CITING + '. No verified original article URL or DOI/PMID is available. Do not treat the citing article as the original case report.'),
]


def main():
    if (DP / MANIFEST).exists():
        report = load(MANIFEST)
        assert all(any(r['id'] == item['recordId'] for r in load('publications.json')['records']) for item in report['records'])
        print(json.dumps({'alreadyApplied': True, 'report': report}, ensure_ascii=False))
        return
    before = snapshot()
    data = load('publications.json')
    approved = load('approved-scientific-additions.json')
    link_audit = load('source-link-audit.json')
    old = deepcopy(data['records'])
    old_ids = {r['id'] for r in old}
    changed = set()
    corrections = []

    def one(test):
        found = [r for r in data['records'] if test(r)]
        assert len(found) == 1, 'An existing correction target is missing or duplicated'
        return found[0]

    for pmid, species, year in [('26116621', ['Cat'], '2016'), ('14664199', ['Dog', 'Cat'], None)]:
        r = one(lambda x: str(x.get('pmid')) == pmid)
        previous = {'species': deepcopy(r.get('species', [])), 'year': r.get('year')}
        r['species'] = list(dict.fromkeys([*r.get('species', []), *species]))
        if year:
            r['year'] = year
            r['onlinePublicationDate'] = '2015-06-26'
            r['printPublicationYear'] = year
            note = 'Publication date clarified: online first 26 June 2015; print issue August 2016. One publication, not two.'
            r.setdefault('notes', [])
            if note not in r['notes']:
                r['notes'].append(note)
        if 'Veterinary' not in r['directions']:
            r['directions'].append('Veterinary')
        corrections.append(dict(recordId=r['id'], before=previous, after={'species': r['species'], 'year': r['year']}))
        changed.add(r['id'])
    ferret = one(lambda r: norm(r['title']).startswith(norm('Clinical aspects of systemic granulomatous inflammatory syndrome in ferrets')))
    corrections.append(dict(recordId=ferret['id'], before={'species': ferret['species']}, after={'species': ['Ferret']}))
    ferret['species'] = ['Ferret']
    changed.add(ferret['id'])

    selected = []
    added_ids = []
    for item in ADDITIONS:
        matches = [r for r in data['records'] if (item['doi'] and norm(r.get('doi')) == norm(item['doi'])) or (item['pmid'] and str(r.get('pmid')) == item['pmid']) or norm(r['title']) == norm(item['title'])]
        assert len(matches) <= 1, 'Duplicate bibliographic identity: ' + item['title']
        if matches:
            r = matches[0]
            assert not r['recordType'].startswith('Import'), 'Imported fragment needs explicit reconciliation'
            r['species'] = list(dict.fromkeys([*r['species'], 'Cat']))
            r['directions'] = list(dict.fromkeys([*r['directions'], 'Veterinary']))
            changed.add(r['id'])
            selected.append(dict(recordId=r['id'], title=item['title'], status='existing global record; feline veterinary tags reconciled', archive=item['archive']))
            continue
        rid = 'pub-feline-' + item['key']
        aid = 'feline-' + item['key']
        assert rid not in old_ids and not any(a['id'] == aid for a in approved['records'])
        verification = 'Bibliographic verification required' if item['archive'] else 'Primary bibliographic metadata verified'
        review = item['review'] or ('PubMed or publisher title, DOI and complete authorship checked for this release. All five primary additions passed the live BHOC author stop-list check with no matches; that check is not a scientific-validity assessment. No treatment protocol or new quantitative efficacy claim is extracted in this catalogue update.')
        topics = ['Feline evidence', 'Feline oxygen transport']
        if item['archive']:
            topics.append('Historical bibliographic archive')
        meta = dict(id=aid, title=item['title'], year=item['year'], authors=item['authors'], journal=item['journal'], doi=item['doi'], pmid=item['pmid'],
                    product=item['product'], topics=topics, directions=['Veterinary'], institutions=[], species=['Cat'], evidenceType=item['evidence'],
                    catalogue=item['catalogue'], metadataSources=item['urls'] or [CITING], originalVerification=verification, sourceReview=review,
                    catalogueSummary=item['summary'], release=RELEASE, citation=item['citation'], verified=DATE)
        row = dict(id=rid, title=item['title'], year=item['year'], authors=item['authors'], journal=item['journal'], doi=item['doi'], pmid=item['pmid'],
                   citation=item['citation'], product=item['product'], keywords='; '.join(topics), directions=['Veterinary'], institutions=[], species=['Cat'], evidence=item['evidence'],
                   urls=item['urls'], notes=[], provenance=[dict(source='Approved scientific additions', row=aid, title=item['title'], year=item['year'], doi=item['doi'], pmid=item['pmid'])],
                   originalVerification=verification, sourceReview=review, catalogue=item['catalogue'], classificationBasis=item['summary'], verification=verification,
                   recordType='Archival bibliographic citation' if item['archive'] else 'Bibliographic record', topics=topics, titleAliases=[], catalogueSummary=item['summary'], cohortLinks=[], added=DATE, release=RELEASE)
        approved['records'].append(meta)
        data['records'].append(row)
        link_audit['records'][rid] = dict(publicLinks=item['urls'], checks=[dict(url=u, state='matched', method='Primary bibliographic identity and full authorship verified; not an efficacy assessment', sourceTitle=item['title']) for u in item['urls']])
        added_ids.append(rid)
        selected.append(dict(recordId=rid, title=item['title'], status='added', archive=item['archive']))

    assert old_ids <= {r['id'] for r in data['records']}, 'An existing record was removed'
    now = {r['id']: r for r in data['records']}
    assert all(now[r['id']] == r for r in old if r['id'] not in changed), 'Unrelated record changed'
    data['updated'] = DATE
    public = [r for r in data['records'] if not r['recordType'].startswith('Import')]
    link_audit.update(publicRecords=len(public), checked=DATE)
    link_audit['uniqueUrlsChecked'] = len({c['url'] for a in link_audit['records'].values() for c in a['checks']})
    link_audit['states'] = dict(Counter(c['state'] for a in link_audit['records'].values() for c in a['checks']))
    coverage = load('source-coverage.json')
    occurrences = sum(len(r['provenance']) for r in data['records'])
    repeated = occurrences - len(data['records'])
    fragments = len(data['records']) - len(public)
    coverage.update(checked=DATE, sourceOccurrences=occurrences, retainedRecordsIncludingFragments=len(data['records']), publicRecords=len(public),
                    repeatedSourceOccurrences=repeated, incompleteSourceFragments=fragments, catalogues=dict(Counter(r['catalogue'] for r in public)),
                    calculation=f'{occurrences} source occurrences - {repeated} repeated occurrences - {fragments} incomplete fragments = {len(public)} public records')
    for source in coverage.get('sources', []):
        if source.get('source') == 'Approved scientific additions':
            source.update(rows=len(approved['records']), retainedRows=len(approved['records']), missingRows=0)
    for name, obj in [('publications.json', data), ('approved-scientific-additions.json', approved), ('source-link-audit.json', link_audit), ('source-coverage.json', coverage)]:
        save(name, obj)
    after = snapshot()
    b, a = before['audit'], after['audit']
    report = dict(release=RELEASE, checked=DATE, requestedAdditions=7, newPublications=len(added_ids), reusedGlobalRecords=7-len(added_ids),
                  records=selected, corrections=corrections, before=before, after=after,
                  evidenceBoundary='The feline filter counts bibliographic records, including two explicitly unverified archival citations; it is not a count of independent clinical trials.')
    save(MANIFEST, report)

    # Advance release snapshot assertions, while retaining all structural and source audits.
    checks_path = ROOT / 'scripts/check_evidence_catalogues.py'
    checks = checks_path.read_text()
    pairs = [
        (f"reconciliation['netAddedRecords']=={before['netAddedRecords']}", f"reconciliation['netAddedRecords']=={after['netAddedRecords']}"),
        (f"{before['netAddedRecords']} net additions", f"{after['netAddedRecords']} net additions"),
        (f"collection_stats['entries']=={b['collectionTotals']['entries']}", f"collection_stats['entries']=={a['collectionTotals']['entries']}"),
        (f"collection_stats['distinctRecordsInFiveCollections']=={b['collectionTotals']['distinctRecordsInFiveCollections']}", f"collection_stats['distinctRecordsInFiveCollections']=={a['collectionTotals']['distinctRecordsInFiveCollections']}"),
        (f"data-publication-counter>{b['publicationCounter']['displayedTotal']}</strong>", f"data-publication-counter>{a['publicationCounter']['displayedTotal']}</strong>"),
        (f"publication_counter()['newPublications']=={b['publicationCounter']['newPublications']}", f"publication_counter()['newPublications']=={a['publicationCounter']['newPublications']}"),
        (f"len(ALL_RECORDS)=={before['allRecords']} and len(RECORDS)=={b['publicRecords']}", f"len(ALL_RECORDS)=={after['allRecords']} and len(RECORDS)=={a['publicRecords']}"),
        (f"<strong>{b['views']['product']['records']}</strong><span>Publication records</span>", f"<strong>{a['views']['product']['records']}</strong><span>Publication records</span>"),
    ]
    for kind in ['transplant', 'human', 'veterinary', 'oxygen', 'related']:
        pairs.append((f"'{kind}':{b['views'][kind]['records']}", f"'{kind}':{a['views'][kind]['records']}"))
    for old_text, new_text in pairs:
        assert checks.count(old_text) == 1, 'Unexpected release assertion: ' + old_text
        checks = checks.replace(old_text, new_text, 1)
    key = "|{'pub-doi-10-1136-inpract-27-8-399'}"
    assert checks.count(key) == 1
    checks = checks.replace(key, key + '|set(' + repr(added_ids) + ')', 1)
    checks += '''\n# User-approved feline release: each requested source once, without species leakage.\nfeline_release=read('catalogues/data/feline-literature-review-20261103.json')\nassert len(feline_release['records'])==7\nfeline_rows=[r for r in VIEWS['veterinary'] if 'Feline (Cat)' in r['speciesGroups']]\nassert len(feline_rows)==feline_release['after']['feline']\nassert all(any(r['id']==item['recordId'] for r in feline_rows) for item in feline_release['records'])\nassert all('ferrets' not in r['title'].lower() for r in feline_rows)\nassert any(r['pmid']=='26116621' and r['year']=='2016' for r in feline_rows)\nassert any(r['pmid']=='14664199' for r in feline_rows)\nfor item in feline_release['records']:\n    record=next(r for r in RECORDS if r['id']==item['recordId'])\n    if item['archive']:\n        assert record['recordType']=='Archival bibliographic citation'\n        assert record['verification']=='Bibliographic verification required'\n        assert record['urls']==[] and 'original' in record['sourceReview'].lower()\nprint('PASS: feline tags, requested records, archival qualifications and counters agree.')\n'''
    checks_path.write_text(checks)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
