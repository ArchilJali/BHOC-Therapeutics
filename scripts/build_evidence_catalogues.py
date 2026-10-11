"""Build every public search and its statistics from the shared catalogue model."""
import html, json, re
from urllib.parse import urlparse
from evidence_catalogue_model import *
E=lambda value:html.escape(str(value or ''),quote=True)
PREFIX='/evidence/library/'
ORIGIN='https://bhoctherapeutics.com'
VERSION='20261011-pages4'
DESCRIPTIONS={
 'product':'Research on Oxyglobin, Hemopure and their historical development. Search by species, author, institution, journal and year.',
 'oxygen':'Research on oxygen diffusion, tissue oxygenation, microcirculation and perfusion. Search by author, journal, year and study model.',
 'related':'Scientific context for oxygen therapeutics across oncology, veterinary medicine, transplantation, emergency care and transfusion practice.',
 'veterinary':'Search veterinary and comparative oxygen-carrier literature by species, author, institution, journal and year.',
 'human':'Search human-use and translational oxygen-carrier literature by therapeutic area, evidence group, author, institution, journal and year.',
 'transplant':'Search oxygen-carrier and related transplantation research by organ, evidence group, author, institution, journal and year.'}
BOUNDARIES={
 'product':'Historical product findings do not establish the efficacy or approval of a future BHOC formulation.',
 'oxygen':'Physiological and mechanistic studies provide research context. Inclusion does not establish a clinical benefit of BHOC.',
 'related':'These studies provide scientific context and are not presented as direct evidence of Oxyglobin, Hemopure or BHOC efficacy.',
 'veterinary':'Species and model labels describe the indexed literature. They do not imply clinical use or approval in every species.',
 'human':'Human clinical and preclinical evidence are labelled separately. Animal studies are not presented as human clinical evidence.',
 'transplant':'Historical oxygen-carrier research and related transplantation studies remain separately classified.'}
HOME=(BASE/'index.html').read_text()
HEADER=re.search(r'<header class="site-header">[\s\S]*?</header>',HOME)[0]
FOOTER=re.search(r'<footer class="site-footer">[\s\S]*?</footer>',HOME)[0]
FOOTER=re.sub(r'<p class="platform-version"[\s\S]*?</p>','',FOOTER)
LINK_AUDIT_PATH=BASE/'catalogues/data/source-link-audit.json'
LINK_AUDIT=json.loads(LINK_AUDIT_PATH.read_text())['records']

def tabs(current=''):
    selected='product' if current in ['veterinary','human','transplant'] else current
    return '<nav class="catalogue-tabs" aria-label="Evidence catalogues">'+''.join(f'<a href="{PREFIX+PATHS[k]}"'+((' aria-current="page"' if current==k else ' aria-current="location"') if k==selected else '')+f'><span>0{i}</span>{E(TITLES[k])}</a>' for i,k in enumerate(['product','oxygen','related'],1))+'</nav>'

def appnav(current=''):
    if current not in ['product','veterinary','human','transplant']:return ''
    return '<nav class="application-tabs" aria-label="Search by application"><span>By application:</span>'+''.join(f'<a href="{PREFIX+PATHS[k]}"'+(' aria-current="page"' if k==current else '')+f'>{E(APP_LABELS[k])}</a>' for k in ['veterinary','human','transplant'])+'</nav>'

def pagination():
    return '<nav class="pagination" aria-label="Publication pages" hidden><button id="previous" type="button" aria-label="Previous page">‹</button><div id="page-numbers" class="page-numbers"></div><button id="next" type="button" aria-label="Next page">›</button><span id="page-label" class="visually-hidden" aria-live="polite"></span></nav>'

def metric_html(kind, live=False):
    s=STATS[kind] if kind in STATS else TOTAL
    labels={'records':'Publication records','groups':s['groupLabel'],'institutions':'Author institutions','journals':'Journals'}
    return '<div class="evidence-metrics"'+(' id="evidence-metrics" aria-label="Statistics for matching publications"' if live else '')+'>'+''.join(f'<div><strong'+(f' data-metric="{key}"' if live else '')+f'>{s[key]}</strong><span>{label}</span></div>' for key,label in labels.items())+'</div>'

def public_url(url):
    try:p=urlparse(url);host=p.hostname or ''
    except ValueError:return False
    return p.scheme in ['https','http'] and bool(re.fullmatch(r'(?:[a-z0-9-]+\.)+[a-z]{2,}',host,re.I)) and not host.endswith(('.local','.internal','.localhost'))

def field(label,value):
    return f'<div><dt>{label}</dt><dd>{E(value)}</dd></div>' if value else ''

def card(r,kind):
    attrs={'year':r['year'],'application':'|'.join(r['application']),'species':'|'.join(r['speciesGroups']), 'journal':r['journalLabel'],'institution':'|'.join(r['institutions']),'product':'|'.join(r['products']), 'direction':'|'.join(r['direction']),'organ':'|'.join(r['organ']),'evidence':'|'.join(r['evidenceGroups']), 'catalogue':r['catalogue'],'site':'|'.join(r['sites']),'author':r['authors'],'title':r['title'], 'legacy':'|'.join(r['legacyIds'])}
    # Search the approved original citation as well as the displayed normalized labels.
    attrs['search']=' '.join([r['title'],r['authors'],r['journal'],r['citation'],r['doi'],r['pmid'],r['keywords'],r['product'],*r['institutions'],*r['species']])
    attrs['scope']=r['scope'];attrs['collection']='|'.join(r['collection'])
    links=[]
    checked=LINK_AUDIT[r['id']]
    source_urls=checked['publicLinks']
    for u in source_urls:
        if not public_url(u) or '?term=' in u or 'scholar.google' in u:continue
        label='PubMed / abstract' if 'pubmed' in u else 'Publisher / DOI' if 'doi.org/' in u else 'PDF' if '.pdf' in u.lower() else 'Full text / PMC' if '/pmc/' in u or 'pmc.ncbi.nlm.nih.gov' in u else 'Source'
        links.append(f'<a href="{E(u)}" target="_blank" rel="noopener noreferrer">{label} ↗</a>')
    url=PREFIX+PATHS[r['catalogue']]+'#'+r['id']
    details=field('Authors',r['authors'])+field('Journal',r['journalLabel'] or r['journal'])+field('Year',r['year'])+field('Species / model',', '.join(r['speciesGroups']))+field('Author institutions',', '.join(r['institutions']))+field('Evidence type','; '.join(r['evidenceGroups']) or r['evidence'])+field('DOI',r['doi'])+field('PMID',r['pmid'])+field('Original citation',r['citation'])
    annotation='<p class="record-summary">'+E(r.get('catalogueSummary',''))+'</p>' if r.get('catalogueSummary') else ''
    summary_label='Summary &amp; details' if annotation else 'Record details'
    availability='' if links else '<p class="source-availability">Citation record. A verified article link or abstract is not currently available.</p>'
    note='<p class="metadata-note">Bibliographic details require source verification.</p>' if r['verification']=='Bibliographic verification required' else ''
    return f'''<article class="publication" id="{r['id']}" {' '.join('data-'+k+'="'+E(v)+'"' for k,v in attrs.items())}>
<div class="record-meta"><span>{E(r['year'] or 'Year not recorded')}</span><span>{E(' · '.join(r['speciesGroups']))}</span></div>
<h2>{E(r['title'])}</h2><p class="citation-line">{E(' · '.join(v for v in [r['authors'],r['journalLabel']] if v))}</p>
<div class="source-links">{''.join(links)}</div>
<details><summary>{summary_label}</summary>{annotation}{availability}{note}<dl>{details}</dl>{'<p>'+E(r['sourceReview'])+'</p>' if r['sourceReview'] else ''}{'<p>'+E('; '.join(r['notes']))+'</p>' if r['notes'] else ''}</details></article>'''

def select(fid,label,placeholder='All'):
    return f'<label>{label}<select id="{fid}"><option value="">{placeholder}</option></select></label>'

def filters(kind):
    primary=('direction','Therapeutic area','All areas') if kind=='human' else ('organ','Organ','All organs') if kind=='transplant' else ('species','Species / model','All species / models')
    basic='<label class="search">Search publications<input id="q" type="search" placeholder="Title, author, topic, DOI or PMID"></label>'+select(*primary)+select('year','Year','All years')+select('journal','Journal','All journals')
    advanced='<label><span id="authorInput"></span>Author<input id="author" type="search" list="authors" placeholder="Type an author"><datalist id="authors"></datalist></label><label><span id="institutionSearch"></span>Author institution<input id="institution" type="search" list="institutions" placeholder="Type an institution"><datalist id="institutions"></datalist></label>'
    if primary[0]!='species':advanced+=select('species','Species / model','All species / models')
    advanced+=select('product','Product','All products')+select('evidence','Evidence group','All evidence groups')
    if kind in ['product','oxygen','related']:advanced+=select('application','Application','All applications')
    else:advanced+=select('catalogue','Catalogue','All catalogues')
    if kind=='veterinary':advanced+=select('site','Documented study site','All documented sites')
    if kind=='transplant':advanced+=select('collection','Research collection','All collections')
    return '<span id="journalInput"></span><span id="scopeSelect"></span><form class="catalogue-filters" onsubmit="return false" aria-label="Filter publications"><div class="filter-grid">'+basic+'</div><div class="filter-actions"><details id="advanced"><summary>More filters</summary><div class="filter-grid advanced-grid">'+advanced+'</div></details><button id="reset" type="button">Reset filters</button></div></form>'

def metadata(kind,rows,path=None):
    path=path or PATHS[kind];url=ORIGIN+PREFIX+path;title=TITLES[kind]+' | BHOC Evidence';description=DESCRIPTIONS[kind]
    schema={'@context':'https://schema.org','@graph':[{'@type':'CollectionPage','@id':url+'#page','name':title,'description':description,'url':url,'inLanguage':'en','dateModified':'2026-10-11','isPartOf':{'@id':ORIGIN+PREFIX+'#website'},'mainEntity':{'@type':'ItemList','numberOfItems':len(rows),'itemListElement':[{'@type':'ListItem','position':i,'name':r['title'],'url':ORIGIN+PREFIX+PATHS[r['catalogue']]+'#'+r['id']} for i,r in enumerate(rows,1)]}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Evidence Library','item':ORIGIN+PREFIX},{'@type':'ListItem','position':2,'name':TITLES[kind],'item':url}]}]}
    return f'''<title>{E(title)}</title><meta name="description" content="{E(description)}"><link rel="canonical" href="{url}"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="yandex" content="noindex"><meta name="author" content="Archil Jaliashvili"><link rel="author" href="https://orcid.org/0009-0006-4712-4942"><link rel="sitemap" href="{PREFIX}sitemap.xml" type="application/xml">
<meta property="og:type" content="website"><meta property="og:site_name" content="BHOC Therapeutics"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{ORIGIN+PREFIX}assets/bhoc-evidence-social.png"><meta property="og:image:alt" content="BHOC scientific evidence library"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(description)}"><meta name="twitter:image" content="{ORIGIN+PREFIX}assets/bhoc-evidence-social.png">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('</','<\\/')}</script>'''

def page(kind,path=None):
    rows=VIEWS[kind];group=GROUP_FIELDS.get(kind,'species');path=path or PATHS[kind]
    extra=''
    if kind=='product':extra=f'<a href="{PREFIX}veterinary/Vet-03-publication-BHOC-Oxyglobin.html">Oxyglobin clinical &amp; regulatory evidence</a><a href="{PREFIX}human/BHOC-Human-fda-expanded-access.html">Hemopure Expanded Access</a>'
    if kind=='related':extra=f'<a href="{PREFIX}science/#featured-publications">Read the featured Science analyses →</a><a href="{PREFIX}science/#scientific-catalogues">Browse this same catalogue within Science →</a>'
    text=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{metadata(kind,rows,path)}
<link rel="stylesheet" href="{PREFIX}assets/evidence.css"><link rel="stylesheet" href="{PREFIX}assets/platform-shell.css"><link rel="stylesheet" href="{PREFIX}catalogues/catalogues.css?v={VERSION}"><script defer src="{PREFIX}assets/navigation.js"></script><script defer src="{PREFIX}catalogues/catalogues.js?v={VERSION}"></script><script src="https://analytics.ahrefs.com/analytics.js" data-key="9SwV8W7kv8qdGkrTrb3arQ" async></script></head>
<body class="evidence-catalogue" data-view="{kind}" data-group="{group}"><a class="skip" href="#main">Skip to content</a>{HEADER}<main id="main" class="catalogue-shell"><div class="breadcrumbs"><a href="{PREFIX}">Evidence Library</a> / {E(TITLES[kind])}</div>{tabs(kind)}{appnav(kind)}
<section class="catalogue-hero"><div class="eyebrow">Scientific Evidence Relevant to BHOC</div><h1>{E(TITLES[kind])}</h1><p>{E(DESCRIPTIONS[kind])}</p>{('<p class="catalogue-relationship">Also available below the featured analyses in <a href="'+PREFIX+'science/#scientific-catalogues">Science</a>. Both views use the same publication records and counts.</p>' if kind=='related' else '')}{metric_html(kind,True)}</section>
{filters(kind)}<div class="results-bar"><p id="result-count" aria-live="polite">{len(rows)} publication records</p><div class="result-actions"><label class="visually-hidden" for="sort">Sort results</label><select id="sort"><option value="newest">Newest first</option><option value="oldest">Oldest first</option><option value="title">Title A–Z</option></select><button id="export" type="button">Export CSV</button></div></div>
<noscript><p>All publications are shown below. Use your browser’s Find command to search.</p></noscript><div id="results">{''.join(card(r,kind) for r in rows)}</div><p id="empty" hidden>No publications match these filters. Try a broader search or reset the filters.</p>
{pagination()}
<p class="catalogue-context">{E(BOUNDARIES[kind])} Author affiliations do not imply institutional endorsement. <a href="{PREFIX}catalogues/methodology.html">About the catalogue</a>.</p><div class="application-tabs">{extra}</div><p class="updated">Updated 11 October 2026</p><aside class="notice" data-usage-permission><a href="{PREFIX}usage-permission.html">Terms of Use &amp; Written Permission</a></aside></main>{FOOTER}</body></html>'''
    (BASE/path).write_text(text)

if __name__=='__main__':
    result=audit()
    for k in VIEWS:page(k)
    # Existing citation-catalogue URL remains a functioning view, including old record anchors.
    page('veterinary','veterinary/publication-catalogue.html')
    p=BASE/'veterinary/publication-catalogue.html'
    s=p.read_text();s=re.sub(r'<link rel="canonical"[^>]+>',f'<link rel="canonical" href="{ORIGIN+PREFIX+PATHS["veterinary"]}">',s);p.write_text(s)
    (BASE/'catalogues/data/statistics.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
