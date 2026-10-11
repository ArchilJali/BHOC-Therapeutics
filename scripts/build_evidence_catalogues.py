"""Render all three evidence catalogues from one canonical record store."""
import json,html,re
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'evidence/library'
DATA=json.loads((BASE/'catalogues/data/publications.json').read_text())
records=DATA['records']
E=lambda s:html.escape(str(s or ''),quote=True)
titles={'product':'Oxyglobin & Hemopure Evidence','oxygen':'Oxygen Diffusion & Microcirculation','related':'Related Scientific Articles'}
descs={
 'product':'Research and source records directly associated with Oxyglobin, Hemopure and their historical development. General scientific context is catalogued separately.',
 'oxygen':'Oxygen diffusion, tissue oxygenation, microcirculation, capillaries, perfusion and oxygen physiology. Includes the complete supplied Oxygen Master import.',
 'related':'Scientific and clinical context for possible BHOC applications: oncology, veterinary medicine, transplantation, emergency care and transfusion practice.'}
boundaries={
 'product':'Inclusion requires an explicit product association in the approved source metadata. Historical product findings do not establish the efficacy or approval of a future BHOC formulation.',
 'oxygen':'Physiology and mechanistic research inform research questions. Inclusion does not establish a clinical benefit of BHOC. Named-product studies belong in catalogue 01.',
 'related':'These records provide scientific context. They are not presented as direct evidence of Oxyglobin, Hemopure or BHOC efficacy. Oxygen physiology belongs in catalogue 02.'}
head= (BASE/'index.html').read_text()
header=re.search(r'<header class="site-header">[\s\S]*?</header>',head)[0]
footer=re.search(r'<footer class="site-footer">[\s\S]*?</footer>',head)[0]
footer=re.sub(r'<p class="platform-version"[\s\S]*?</p>','',footer)
def nav(current=''):
 return '<nav class="catalogue-tabs" aria-label="Evidence catalogues">'+''.join(f'<a href="/evidence/library/catalogues/{k}.html"'+(' aria-current="page"' if current==k else '')+f'><span>0{i}</span>{E(v)}</a>' for i,(k,v) in enumerate(titles.items(),1))+'</nav>'
def product(r):
 t=r['title']+' '+r['keywords'];p=[]
 if re.search(r'oxyglobin|hboc[- ]?301|glutamer[- ]?200|hb-200',t,re.I):p.append('Oxyglobin')
 if re.search(r'hemopure|hboc[- ]?201|glutamer[- ]?250',t,re.I):p.append('Hemopure')
 return p or ([r['product']] if r['product'] else [])
def field(label,value):return f'<div><dt>{label}</dt><dd>{E(value)}</dd></div>' if value else ''
def card(r):
 fragment=r['recordType'].startswith('Import')
 attrs={'data-year':r['year'],'data-direction':'|'.join(r['directions']),'data-species':'|'.join(r['species']),'data-journal':r['journal'],'data-institution':'|'.join(r['institutions']),'data-status':'fragment' if fragment else 'bibliography','data-product':'|'.join(product(r)),'data-title':r['title']}
 search=' '.join([r['title'],r['authors'],r['journal'],r['citation'],r['doi'],r['pmid'],r['keywords'],r['product'],*r['institutions'],*r['species']])
 attrs['data-search']=search
 links=[]
 for u in r['urls']:
  label='PubMed' if re.search(r'/\d+/?$',u) and 'pubmed' in u else 'DOI' if 'doi.org/' in u else 'Source search' if '?term=' in u or 'scholar.google' in u else 'Source record'
  links.append(f'<a href="{E(u)}" target="_blank" rel="noopener noreferrer">{label} ↗</a>')
 provenance=''.join('<li>'+E(p['source'])+' · row '+E(p['row'])+'</li>' for p in r['provenance'])
 details=field('Authors',r['authors'])+field('Journal',r['journal'])+field('Year',r['year'])+field('Species / model',', '.join(r['species']))+field('Author institutions',', '.join(r['institutions']))+field('Evidence type',r['evidence'])+field('DOI',r['doi'])+field('PMID',r['pmid'])
 return f'''<article class="publication" id="{r['id']}" {' '.join(k+'="'+E(v)+'"' for k,v in attrs.items())}>
 <div class="record-meta"><span>{E(r['year'] or 'Year unconfirmed')}</span><span>{E(' · '.join(r['directions']) or 'Scientific context')}</span><span class="status">{E(r['verification'])}</span></div>
 <h2>{E(r['title'])}</h2><p class="citation-line">{E(' · '.join(x for x in [r['authors'],r['journal']] if x))}</p>
 {'<p class="fragment-note">Incomplete imported text. This item is retained for source review and is not counted as a complete bibliographic record.</p>' if fragment else ''}
 <div class="source-links">{''.join(links) or '<span>Primary source link requires verification</span>'}<a class="permalink" href="#{r['id']}">Record link</a></div>
 <details><summary>Bibliographic details &amp; source trace</summary><dl>{details}</dl><p>{E(r['sourceReview'])}</p><p>{E('; '.join(r['notes']))}</p><p>{E(r['citation'])}</p><p>Classification: {E(r['classificationBasis'])}.</p><ul>{provenance}</ul></details></article>'''
counts={k:sum(r['catalogue']==k and not r['recordType'].startswith('Import') for r in records) for k in titles}
for i,(kind,title) in enumerate(titles.items(),1):
 selected=[r for r in records if r['catalogue']==kind]
 fragment_count=sum(r['recordType'].startswith('Import') for r in selected)
 filters='<label class="search">Search<input id="q" type="search" placeholder="Title, author, journal, DOI, PMID, topic…"></label>'
 for fid,label,placeholder in [('year','Year','All years'),('direction','Source direction','All directions'),('species','Species / model','All species'),('journal','Journal','All journals')]+([('product','Product','All products')] if kind=='product' else []):
  filters+=f'<label>{label}<select id="{fid}"><option value="">{placeholder}</option></select></label>'
 filters+='<label class="search">Author institution<input id="institution" type="search" list="institutions" placeholder="Type an institution name"><datalist id="institutions"></datalist></label>'
 filters+='<label>Record status<select id="status"><option value="bibliography">Bibliographic records</option><option value="fragment">Import fragments requiring review</option><option value="">All retained records</option></select></label><label>Sort<select id="sort"><option value="newest">Year: newest first</option><option value="oldest">Year: oldest first</option><option value="title">Title: A–Z</option></select></label><button id="reset" type="button">Reset filters</button>'
 extra=''
 if kind=='product':extra='<a href="../veterinary/Vet-03-publication-BHOC-Oxyglobin.html">Oxyglobin clinical &amp; regulatory evidence →</a> · <a href="../human/BHOC-Human-fda-expanded-access.html">Hemopure Expanded Access record →</a>'
 if kind=='oxygen':extra=f'All 243 Oxygen Master source rows are retained, representing 242 distinct imported entries after one duplicate merge. Incomplete fragments remain accessible below. <a href="?status=fragment">Review {fragment_count} incomplete source fragments →</a>'
 if kind=='related':extra='<a href="../science/">Scientific Evidence Relevant to BHOC →</a> · <a href="../transplant/related/evidence.html">Transplant research context →</a>'
 url=f'https://bhoctherapeutics.com/evidence/library/catalogues/{kind}.html'
 text=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
 <title>{E(title)} Catalogue | BHOC</title><meta name="description" content="{E(descs[kind])}"><link rel="canonical" href="{url}"><meta name="robots" content="index,follow"><meta name="yandex" content="noindex"><meta name="twitter:card" content="summary_large_image">
 <meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(descs[kind])}"><meta property="og:url" content="{url}"><meta property="og:image" content="https://bhoctherapeutics.com/evidence/library/assets/bhoc-evidence-social.png">
 <link rel="stylesheet" href="../assets/evidence.css"><link rel="stylesheet" href="../assets/platform-shell.css"><link rel="stylesheet" href="catalogues.css"><script defer src="../assets/navigation.js"></script><script defer src="catalogues.js"></script></head>
 <body><a class="skip" href="#main">Skip to content</a>{header}<main id="main" class="catalogue-shell"><div class="breadcrumbs"><a href="../">Evidence Library</a> / Catalogue 0{i}</div>{nav(kind)}
 <section class="catalogue-hero"><div class="eyebrow">Scientific evidence catalogue · 0{i}</div><h1>{E(title)}</h1><p>{E(descs[kind])}</p><div class="catalogue-total"><strong>{counts[kind]}</strong> bibliographic records{f' <span>+ {fragment_count} incomplete source fragments</span>' if fragment_count else ''}</div><p class="boundary">{E(boundaries[kind])}</p><p>{extra}</p></section>
 <p class="method">One primary catalogue per record. DOI, PMID and bibliographic comparisons link repeated source entries to one record. “Source identifier supplied” means an identifier exists in the source data, not independent verification of every citation. <a href="methodology.html">Source reconciliation and classification →</a></p>
 <form class="catalogue-filters" onsubmit="return false" aria-label="Filter publications">{filters}</form><div class="results-bar"><p id="result-count" aria-live="polite">{counts[kind]} bibliographic records</p><button id="export" type="button">Export matching records (CSV)</button></div>
 <noscript><p>JavaScript is disabled. All records are shown below; use your browser’s Find command to search.</p></noscript><div id="results">{''.join(card(r) for r in selected)}</div><p id="empty" hidden>No records match these filters. Try a broader search or reset the filters.</p>
 <nav class="pagination" aria-label="Results pages"><button id="previous" type="button">← Previous</button><span id="page-label"></span><button id="next" type="button">Next →</button></nav><p class="updated">Catalogue reconciliation: 11 October 2026. Original source records remain traceable.</p></main>{footer}</body></html>'''
 (BASE/f'catalogues/{kind}.html').write_text(text)
summary={'updated':DATA['updated'],'counts':counts,'bibliographicRecords':sum(counts.values()),'incompleteFragments':sum(r['recordType'].startswith('Import') for r in records),'retainedRecords':len(records),'sourceRows':sum(len(r['provenance']) for r in records),'sourceOccurrences':dict(Counter(p['source'] for r in records for p in r['provenance'])),'oxygenImportRows':243,'oxygenImportEntries':242}
(BASE/'catalogues/data/reconciliation.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
