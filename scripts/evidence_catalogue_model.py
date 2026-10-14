"""Shared catalogue views and statistics from imported and user-approved sources."""
import json, re, subprocess
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'evidence/library'
DATA = json.loads((BASE / 'catalogues/data/publications.json').read_text())
ALL_RECORDS = DATA['records']
RECORDS = [dict(r) for r in ALL_RECORDS if not r['recordType'].startswith('Import')]
TITLES = {'product': 'Oxyglobin & Hemopure Evidence', 'oxygen': 'Oxygen Diffusion & Microcirculation', 'related': 'Related Scientific Articles', 'veterinary': 'Veterinary Publication Search', 'human': 'Human-Use Publication Search', 'transplant': 'Transplantation Publication Search'}
PATHS = {**{k:f'catalogues/{k}.html' for k in ['product','oxygen','related']}, 'veterinary':'veterinary/Vet-search.html', 'human':'human/BHOC-Human-search.html', 'transplant':'transplant/Transplant-search.html'}
GROUP_FIELDS = {'human':'direction', 'transplant':'organ'}
GROUP_LABELS = {'human':'Therapeutic areas', 'transplant':'Organ groups'}
APP_LABELS = {'veterinary':'Veterinary','human':'Human Use','transplant':'Transplant'}
TITLES['all']='Scientific Evidence Relevant to BHOC'
PATHS['all']='catalogues/'

def read(name):
    return json.loads((BASE / name).read_text())

def unique(values):
    found={}
    for value in values:
        value=re.sub(r'\s+',' ',str(value or '')).strip()
        if value: found.setdefault(value.casefold(),value)
    return sorted(found.values(), key=str.casefold)

# Only aliases explicitly present in the supplied catalogue are consolidated.
JOURNAL_ALIASES = {
    'Am J Ther':'American Journal of Therapeutics','Am J Transplant':'American Journal of Transplantation',
    'Am J Vet Res':'American Journal of Veterinary Research','Anal Chem':'Analytical Chemistry',
    'Br J Anaesth':'British Journal of Anaesthesia','Clin Chem':'Clinical Chemistry',
    'Crit Care Med':'Critical Care Medicine','J Appl Physiol (1985)':'Journal of Applied Physiology',
    'J Cardiothorac Vasc Anesth':'Journal of Cardiothoracic and Vascular Anesthesia',
    'J Clin Anesth':'Journal of Clinical Anesthesia','J Feline Med Surg':'Journal of Feline Medicine and Surgery',
    'J Trauma':'Journal of Trauma','Mil Med':'Military Medicine',
    'The New England Journal of Medicine':'New England Journal of Medicine',
    'The Journal of Heart and Lung Transplantation':'Journal of Heart and Lung Transplantation',
    'al. Am J Transplant':'American Journal of Transplantation','al.  Ann Surg':'Annals of Surgery',
    'J of Vet Int Med. ACVIM ABSTRACTS':'Journal of Veterinary Internal Medicine',
}
REJECT_JOURNALS={'Today','Update','USA','No abstract available','In A44','NANOBIOTHERAPEUTIC BASED BLOOD SUBSTITUTES'}
core_journals=json.loads(subprocess.check_output(['node','-e',"const C=require('./evidence/library/assets/publications-core.js');const D=require('./evidence/library/catalogues/data/publications.json');console.log(JSON.stringify(Object.fromEntries(D.records.map(r=>[r.id,C.journalName(r)]))))"],cwd=ROOT,text=True))
core_scopes=json.loads(subprocess.check_output(['node','-e',"const C=require('./evidence/library/assets/publications-core.js');const D=require('./evidence/library/catalogues/data/publications.json');console.log(JSON.stringify(Object.fromEntries(D.records.map(r=>[r.id,C.isCorePublication(r)]))))"],cwd=ROOT,text=True))

def species(r):
    s=' '.join(r['species']).lower(); result=[]
    for label,pattern in [('Canine (Dog)',r'canine|\bdogs?\b|foxhound'),('Feline (Cat)',r'feline|\bcats?\b'),('Equine (Horse)',r'equine|horse|foal'),('Porcine (Pig)',r'porcine|\bpigs?\b|swine'),('Ovine (Sheep)',r'ovine|sheep|lamb'),('Rodent',r'rodent|\brats?\b|mice|mouse|hamster|hampster|guinea'),('Avian (Bird)',r'avian|bird|duck|hawk'),('Other animal',r'ferret|rabbit|tamandua|otter|other animal'),('Human',r'human'),('In vitro / laboratory',r'in vitro|samples|plasma|cell culture|analytes|instruments|machinery'),('In silico / modelling',r'in silico|computational|mathematical model')]:
        if re.search(pattern,s):result.append(label)
    return result

def products(r):
    text=r['title']+' '+r['keywords']; result=[]
    if re.search(r'oxyglobin|hboc[- ]?301|glutamer[- ]?200|hb-200',text,re.I):result.append('Oxyglobin')
    if re.search(r'hemopure|hboc[- ]?201|glutamer[- ]?250',text,re.I):result.append('Hemopure')
    if not result:
        if re.search(r'oxyglobin|301',r['product'],re.I):result.append('Oxyglobin')
        if re.search(r'hemopure|201',r['product'],re.I):result.append('Hemopure')
    return result

sources={
 'Human Use':{str(r['id']):r for r in read('human/BHOC-Human-publications.json')},
 'Transplant':{str(r['id']):r for r in read('transplant/Transplant-publications.json')},
 'Veterinary base':{str(r['id']):r for r in read('veterinary/Vet-publications.json')},
 'Veterinary curated additions':{str(r['id']):r for r in read('veterinary/Vet-publications-curation.json')['additions']},
 'Approved scientific additions':{str(r['id']):r for r in read('catalogues/data/approved-scientific-additions.json')['records']},
}
for path in ['transplant/related/data/related-evidence.json','transplant/Transplant-relevant-evidence.json']:
    sources[path]={str(r['id']):r for r in read(path)['records']}

def source_for(p):
    rows=sources.get(p['source'],{})
    if str(p['row']) in rows:return rows[str(p['row'])]
    # Historical related files use ordinal source-row provenance.
    for r in rows.values():
        if p.get('doi') and re.sub(r'\W','',p['doi']).lower()==re.sub(r'\W','',r.get('doi','')).lower():return r
        if p.get('title','').rstrip('.').casefold()==r.get('title','').rstrip('.').casefold():return r
    return {}

for r in RECORDS:
    originals=[(p['source'],source_for(p)) for p in r['provenance']]
    r['direction']=unique(o.get('direction') for s,o in originals if s=='Human Use')
    r['organ']=unique(o.get('organ') for s,o in originals if s=='Transplant' or s.startswith('transplant/'))
    r['evidenceGroups']=unique(o.get('evidenceGroup') or o.get('evidence') or o.get('evidenceType') for s,o in originals)
    r['sites']=unique(site.get('institution') for s,o in originals for site in o.get('study_sites',[]) if site.get('source_url') and site.get('locator'))
    r['legacyIds']=unique([*(str(o.get('id','')) for s,o in originals),*r.get('aliases',[])])
    r['scope']='core' if core_scopes[r['id']] else 'related'
    r['collection']=unique('Historical oxygen-carrier research' if s=='Transplant' else 'Related transplantation studies' for s,o in originals if s=='Transplant' or s.startswith('transplant/'))
    r['application']=r['directions'];r['speciesGroups']=species(r);r['products']=products(r)
    j=JOURNAL_ALIASES.get(r['journal'],core_journals[r['id']])
    if len(j)>100 or re.match(r'^(?:A\d+-|doi:|Edited by |Blood Transfusions and Blood Substitutes\. In:)',j) or j in REJECT_JOURNALS:j=''
    r['journalLabel']=j;r['institutions']=unique(r['institutions'])

VIEWS={k:[r for r in RECORDS if r['catalogue']==k] for k in ['product','oxygen','related']}
VIEWS.update({k:[r for r in RECORDS if label in r['application']] for k,label in APP_LABELS.items()})
VIEWS['all']=RECORDS

def stats(rows,kind='all'):
    field=GROUP_FIELDS.get(kind,'speciesGroups')
    return {'records':len(rows),'groups':len(unique(v for r in rows for v in r[field])),
            'institutions':len(unique(v for r in rows for v in r['institutions'])),
            'journals':len(unique(r['journalLabel'] for r in rows)),
            'groupField':field,'groupLabel':GROUP_LABELS.get(kind,'Species / model groups')}

STATS={k:stats(rows,k) for k,rows in VIEWS.items()}
TOTAL=stats(RECORDS)

def publication_counter():
    """Retain the user-approved display baseline; count each new publication once."""
    counter=read('catalogues/data/publication-counter.json')
    baseline=set(counter['baselineRecordIds'])
    additions=[r['id'] for r in RECORDS if r['id'] not in baseline and not baseline.intersection(r.get('aliases',[]))]
    return {'baseline':counter['baseline'],'newPublications':len(additions),
            'displayedTotal':counter['baseline']+len(additions),'newRecordIds':sorted(additions)}

COLLECTIONS = ['transplant', 'human', 'veterinary', 'oxygen', 'related']
COLLECTION_LABELS = {'transplant':'Transplant', 'human':'Human', 'veterinary':'Veterinary',
                     'oxygen':'Oxygen Diffusion & Microcirculation', 'related':'Related Scientific Articles'}

def collection_totals():
    ids = {r['id'] for kind in COLLECTIONS for r in VIEWS[kind]}
    return {'entries':sum(len(VIEWS[k]) for k in COLLECTIONS),
            'collections':{k:len(VIEWS[k]) for k in COLLECTIONS},
            'distinctRecordsInFiveCollections':len(ids),
            'repeatedPlacements':sum(len(VIEWS[k]) for k in COLLECTIONS)-len(ids),
            'additionalProductRecordIds':sorted(r['id'] for r in RECORDS if r['id'] not in ids),
            'distinctRecordsInFullLibrary':len(RECORDS)}

def count_reconciliation():
    """Account for every original source row and each net addition, without adding views."""
    legacy_sources=['Veterinary base','Human Use','Transplant']
    source_counts=Counter(p['source'] for r in ALL_RECORDS for p in r['provenance'])
    expected={name:len(rows) for name,rows in sources.items()}
    expected.update({'Master Catalogue':414,'Oxygen Master':243})
    assert dict(source_counts)==expected, 'Imported source rows missing or counted twice'
    mapping=[{'source':p['source'],'row':p['row'],'recordId':r['id'],'catalogue':r['catalogue']}
             for r in RECORDS for p in r['provenance'] if p['source'] in legacy_sources]
    assert len({(m['source'],m['row']) for m in mapping})==len(mapping)
    for name in legacy_sources:
        assert {m['row'] for m in mapping if m['source']==name}==set(sources[name]), name+' source coverage'
    cohorts=[('Original Veterinary, Human and Transplant lists',set(legacy_sources)),
             ('Veterinary curated additions',{'Veterinary curated additions'}),
             ('Additional Master Catalogue records',{'Master Catalogue'}),
             ('Related transplantation studies',{'transplant/related/data/related-evidence.json','transplant/Transplant-relevant-evidence.json'}),
             ('Additional Oxygen Master records',{'Oxygen Master'}),
             ('User-approved scientific additions',{'Approved scientific additions'})]
    seen=set(); additions=[]
    for label,names in cohorts:
        ids=sorted(r['id'] for r in RECORDS if r['id'] not in seen and any(p['source'] in names for p in r['provenance']))
        additions.append({'label':label,'records':len(ids),'recordIds':ids});seen.update(ids)
    assert seen=={r['id'] for r in RECORDS}, 'Unaccounted public record'
    return {'checked':DATA['updated'],'originalSourceRows':len(mapping),
            'originalSourceCounts':{name:source_counts[name] for name in legacy_sources},
            'originalDistinctRecords':additions[0]['records'],
            'originalRepeatedOccurrences':len(mapping)-additions[0]['records'],
            'netAddedRecords':len(RECORDS)-additions[0]['records'],'publicRecords':len(RECORDS),
            'catalogues':{k:len(VIEWS[k]) for k in ['product','oxygen','related']},
            'sourceOccurrences':dict(source_counts),'cohorts':additions,'originalRecordMapping':mapping}

def audit():
    for field in ['id','doi','pmid']:
        c=Counter(str(r[field]).strip().casefold() for r in RECORDS if r[field])
        assert not [v for v,n in c.items() if n>1],f'Duplicate {field}'
    assert sum(len(VIEWS[k]) for k in ['product','oxygen','related'])==len(RECORDS)
    assert len({r['id'] for k in ['product','oxygen','related'] for r in VIEWS[k]})==len(RECORDS)
    assert sum(p['source']=='Oxygen Master' for r in ALL_RECORDS for p in r['provenance'])==243
    count_reconciliation()
    return {'updated':DATA['updated'],'total':TOTAL,'views':STATS,'publicRecords':len(RECORDS),'collectionTotals':collection_totals(),'publicationCounter':publication_counter(),
            'archivedIncompleteEntries':len(ALL_RECORDS)-len(RECORDS),'duplicateIds':0,'duplicateDOIs':0,'duplicatePMIDs':0,
            'notes':'Catalogue totals are mutually exclusive. Application views can overlap. Missing affiliation, journal and model labels are excluded from those facet counts.'}
