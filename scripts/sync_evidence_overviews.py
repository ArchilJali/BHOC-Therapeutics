"""Synchronize visible metrics, metadata and catalogue navigation with search views."""
import re, json, html
from urllib.parse import quote
from evidence_catalogue_model import *
from build_evidence_catalogues import E, PREFIX, VERSION, TITLES, PATHS, metric_html, tabs, appnav, DESCRIPTIONS, HEADER, FOOTER, filters, card, BOUNDARIES, pagination, SOCIAL_IMAGE_PATTERN, SOCIAL_IMAGE_META

def css(s):
    href=PREFIX+'catalogues/catalogues.css?v='+VERSION
    if re.search(r'<link[^>]+href="[^"]*catalogues\.css[^"]*"[^>]*>',s):
        s=re.sub(r'<link[^>]+href="[^"]*catalogues\.css[^"]*"[^>]*>',f'<link rel="stylesheet" href="{href}">',s)
    else:s=s.replace('</head>',f'<link rel="stylesheet" href="{href}"></head>')
    return s

def catalogue_entry(cards=True):
    out='<section id="scientific-catalogues" class="catalogue-entry"><div class="eyebrow">Explore the scientific literature</div><h2>Scientific Evidence Relevant to BHOC</h2><p>Find publications by topic, species, author, institution, journal and year.</p>'
    if cards:
        out+='<div class="catalogue-card-grid catalogue-card-pair">'
        for k in ['oxygen','related']:
            out+=f'<article class="catalogue-card"><div class="eyebrow">Research catalogue</div><h3>{E(TITLES[k])}</h3><p>{E(DESCRIPTIONS[k])}</p>{metric_html(k)}<a class="button" href="{PREFIX+PATHS[k]}">Explore catalogue →</a></article>'
        out+='</div>'
    else:out+=tabs()
    return out+'</section>'

for f in [BASE/'index.html',ROOT/'evidence/index.html']:
    s=f.read_text();s=re.sub(r'<section[^>]*id="scientific-catalogues"[\s\S]*?</section>',catalogue_entry(f==BASE/'index.html'),s)
    if f==ROOT/'evidence/index.html':
        s=re.sub(r'<strong>\d+</strong><span>publication &amp; evidence records</span>|<strong>\d+</strong><span>publication & evidence records</span>',f'<strong>{TOTAL["records"]}</strong><span>publication records</span>',s)
        s=re.sub(r'<strong>\d+</strong><span>publication records</span>',f'<strong>{TOTAL["records"]}</strong><span>publication records</span>',s)
        s=re.sub(r'<strong>\d+</strong><span>scientific journals</span>',f'<strong>{TOTAL["journals"]}</strong><span>scientific journals</span>',s)
    if f==BASE/'index.html':
        # The original application hubs stay together, before the two new research catalogues.
        s=re.sub(r'<section[^>]*id="scientific-catalogues"[\s\S]*?</section>','',s)
        s=re.sub(r'(<section id="evidence-hubs"[\s\S]*?</section>)',lambda m:m[1]+'\n'+catalogue_entry(True),s)
        s=s.replace('href="#scientific-catalogues">Explore the evidence','href="#evidence-hubs">Explore the evidence')
        product_link=f'<p class="application-catalogue-link" data-product-catalogue-link><a href="{PREFIX+PATHS["product"]}">Oxyglobin &amp; Hemopure: search {STATS["product"]["records"]} product-specific records across applications →</a></p>'
        s=re.sub(r'<p[^>]*data-product-catalogue-link[\s\S]*?</p>','',s)
        s=re.sub(r'(<section id="evidence-hubs"[\s\S]*?)(</section>)',lambda m:m[1]+product_link+m[2],s)
        if 'data-evidence-layout-fix' not in s:
            s=s.replace('</head>','<style data-evidence-layout-fix>body.evidence-library-unified.bhoc-shell-ready>.bhoc-shell-header,body.evidence-library-unified.bhoc-shell-ready>.bhoc-shell-trail,body.evidence-library-unified.bhoc-shell-ready>.bhoc-shell-footer{width:100%;margin-left:0}</style></head>')
        if 'data-evidence-unified=' not in s:s=s.replace('<body','<body data-evidence-unified="true"',1)
        if 'evidence-library-unified' not in re.search(r'<body[^>]*>',s)[0]:s=re.sub(r'<body([^>]*)class="([^"]*)"',lambda m:'<body'+m[1]+'class="'+m[2]+' evidence-library-unified"',s,count=1)
        s=re.sub(r'<section (?:class="overview-stats platform-stats"|aria-label="Evidence Library statistics")[\s\S]*?</section>','<section aria-label="Evidence Library statistics">'+metric_html('all')+'</section>',s)
        breakdown='<div class="count-breakdown" id="catalogue-count-breakdown">'+''.join(f'<a href="{PREFIX+PATHS[k]}"><strong>{STATS[k]["records"]}</strong> {E(TITLES[k])}</a>' for k in ['product','oxygen','related'])+'</div>'
        s=re.sub(r'<div class="count-breakdown" id="catalogue-count-breakdown">[\s\S]*?</div>','',s)
        s=re.sub(r'<p class="metric-note" id="institutions-note">[\s\S]*?</p>',breakdown+'<p class="metric-note" id="institutions-note">The total counts each publication record once across these three catalogues. Veterinary, Human Use and Transplant searches overlap. <a href="'+PREFIX+'catalogues/methodology.html#counting">How the total is calculated →</a><br>Institution and journal counts use recorded metadata. Author affiliations do not imply endorsement.</p>',s)
        for kind,cls in [('veterinary','vet'),('transplant','transplant'),('human','human')]:
            pattern=r'(<article class="panel hub-card '+cls+r'">[\s\S]*?<div class="hub-facts">)[\s\S]*?(</div><a class="button")'
            st=STATS[kind];facts=''.join(f'<div><strong>{st[field]}</strong><span>{label}</span></div>' for field,label in [('records','PUBLICATION RECORDS'),('groups',st['groupLabel'].upper()),('institutions','AUTHOR INSTITUTIONS'),('journals','JOURNALS')])
            s=re.sub(pattern,lambda m:m[1]+facts+m[2],s)
        s=s.replace('Updated 4 Oct 2026','Updated 11 Oct 2026')
    f.write_text(re.sub(r' +\n','\n',css(s)))

# Science keeps every original feature and article. The complete Related catalogue follows them.
p=BASE/'science/index.html';s=p.read_text()
rows=VIEWS['related']
embedded=f'''<section id="scientific-catalogues" class="catalogue-entry evidence-catalogue embedded-catalogue" data-query-prefix="related_" data-view="related" data-group="species" aria-labelledby="related-catalogue-title"><div class="eyebrow">Complete research catalogue</div><h2 id="related-catalogue-title">Related Scientific Articles</h2><p>The featured articles above provide scientific analysis and commentary. Below, search all {len(rows)} bibliographic records from the <a href="{PREFIX+PATHS['related']}">Related Scientific Articles catalogue</a>. This is the same collection, counted once in the Evidence Library.</p>{metric_html('related',True)}{filters('related')}<div class="results-bar"><p id="result-count" aria-live="polite">{len(rows)} publication records</p><div class="result-actions"><label class="visually-hidden" for="sort">Sort results</label><select id="sort"><option value="newest">Newest first</option><option value="oldest">Oldest first</option><option value="title">Title A–Z</option></select><button id="export" type="button">Export CSV</button></div></div><noscript><p>All publications are shown below. Use your browser’s Find command to search.</p></noscript><div id="results">{''.join(card(r,'related').replace('<h2>','<h3>').replace('</h2>','</h3>') for r in rows)}</div><p id="empty" hidden>No publications match these filters. Try a broader search or reset the filters.</p>{pagination()}<p class="catalogue-context">{E(BOUNDARIES['related'])} <a href="{PREFIX}catalogues/methodology.html">About the catalogue</a>.</p></section>'''
s=re.sub(r'<section[^>]*id="scientific-catalogues"[\s\S]*?</section>',lambda m:embedded,s)
if 'id="featured-publications"' not in s:s=s.replace('<section class="panel knowledge-card">','<section class="panel knowledge-card" id="featured-publications">',1)
if 'href="#scientific-catalogues"' not in s:s=s.replace('<div class="knowledge-actions">','<div class="knowledge-actions"><a class="button" href="#scientific-catalogues">Search all related publications →</a>',1)
s=re.sub(r'<script[^>]*src="[^"]*catalogues/catalogues.js[^"]*"[^>]*></script>','',s)
s=s.replace('</head>',f'<script defer src="{PREFIX}catalogues/catalogues.js?v={VERSION}"></script></head>')
schema={'@context':'https://schema.org','@type':'ItemList','@id':'https://bhoctherapeutics.com/evidence/library/science/#scientific-catalogues','name':'Related Scientific Articles','numberOfItems':len(rows),'itemListElement':[{'@type':'ListItem','position':i,'name':r['title'],'url':'https://bhoctherapeutics.com'+PREFIX+PATHS['related']+'#'+r['id']} for i,r in enumerate(rows,1)]}
s=re.sub(r'<script[^>]*id="science-related-catalogue-schema"[\s\S]*?</script>','',s)
s=s.replace('</head>','<script type="application/ld+json" id="science-related-catalogue-schema">'+json.dumps(schema,ensure_ascii=False).replace('</','<\\/')+'</script></head>')
p.write_text(css(s))

def overview(kind):
    st=STATS[kind];link=PREFIX+PATHS[kind]
    return '<section class="overview-stats" aria-label="Catalogue statistics">'+''.join(f'<a class="overview-stat" href="{link+anchor}"><strong>{st[field]}</strong><span>{label}</span><small>{detail}</small></a>' for field,label,detail,anchor in [('records','Publication records','Unique records in this application view',''),('groups',st['groupLabel'],'Recorded catalogue groups','#'+GROUP_FIELDS.get(kind,'species')),('institutions','Author institutions','Indexed author affiliations','#institution'),('journals','Journals','Normalized journal labels','#journal')])+'</section>'

def distribution(kind,field,cls):
    counter=Counter(v for r in VIEWS[kind] for v in r[field]);maximum=max(counter.values())
    items=[]
    for label,count in sorted(counter.items(),key=lambda kv:-kv[1]):
        value=label;param='species' if field=='speciesGroups' else field
        url=PREFIX+PATHS[kind]+'?'+param+'='+quote(value)
        items.append(f'<a class="{cls}-item" href="{url}"><span class="{cls}-name">{E(label)}<span class="{cls}-track" aria-hidden="true"><span style="width:{count/maximum*100:.2f}%"></span></span></span><strong>{count}<span class="species-arrow" aria-hidden="true"> ↗</span></strong></a>')
    if field=='speciesGroups':
        missing=sum(not r[field] for r in VIEWS[kind])
        if missing:items.append(f'<a class="{cls}-item" href="{PREFIX+PATHS[kind]}?species=__other__"><span class="{cls}-name">Species / model not specified</span><strong>{missing}</strong></a>')
    return '<div class="'+cls+'-list">'+''.join(items)+'</div>'

for kind,file,field,cls in [('veterinary','veterinary/Vet-index.html','speciesGroups','species'),('human','human/BHOC-Human-index.html','direction','direction'),('transplant','transplant/Transplant-index.html','organ','organ')]:
    p=BASE/file;s=p.read_text();st=STATS[kind]
    s=re.sub(r'<section[^>]*class="overview-stats"[\s\S]*?</section>',overview(kind),s)
    s=re.sub(r'<div class="'+cls+r'-list">[\s\S]*?</div>',distribution(kind,field,cls),s)
    s=re.sub(r'<span class="tag">\d+ total records</span>',f'<span class="tag">{st["records"]} total records</span>',s)
    # Old source snapshot metrics are replaced; clinical source paragraphs are untouched.
    s=s.replace('Search 154 author institutions, browse 109 normalized journal labels',f'Search {st["institutions"]} author institutions, browse {st["journals"]} normalized journal labels')
    s=re.sub(r'Search \d+ indexed author institutions and \d+ normalized journal labels',f'Search {st["institutions"]} indexed author institutions and {st["journals"]} normalized journal labels',s)
    if kind=='veterinary':
        s=re.sub(r'<p class="overview-caption">The species distribution and catalogue below[\s\S]*?</p>','<p class="overview-caption">The distribution and search use the same 260 unique publication records. A record can carry more than one species or model label.</p>',s)
        s=re.sub(r'(?:236|239) (?:base |searchable )?(?:publication )?records',f'{st["records"]} publication records',s)
        s=s.replace('Other / In vitro includes in-vitro labels and 13 records with no species label.','Missing species labels are shown separately from in-vitro models.')
        s=s.replace('Use Library scope to separate BHOC / Oxyglobin-focused records from background literature. Every record remains accessible under All records.','Use the Catalogue filter to distinguish Oxyglobin and Hemopure research, oxygen physiology and related scientific literature.')
    if kind=='human':
        s=re.sub(r'\b(?:180|181|184|185) (human-use and translational publications|publications|total records|records)',lambda m:str(st['records'])+' '+m[1],s)
        s=s.replace('<strong>46</strong>','<strong>45</strong>')
        clinical=sum('Human clinical evidence' in r['evidenceGroups'] for r in VIEWS[kind])
        s=re.sub(r'(<dt>Human clinical records</dt><dd>)\d+',lambda m:m[1]+str(clinical),s)
    if kind=='transplant':
        # Keep the two scientific evidence layers and expose their actual matching subsets.
        s=s.replace('5 related records','8 related records')
        s=s.replace('href="Transplant-search.html">Historical HBOC evidence','href="Transplant-search.html?collection=Historical%20oxygen-carrier%20research">Historical HBOC evidence')
        s=s.replace('href="Transplant-search.html">Search historical evidence','href="Transplant-search.html?collection=Historical%20oxygen-carrier%20research">Search historical evidence')
        s=s.replace('<h2>54 source-linked records</h2>','<h2>Search the complete transplantation catalogue</h2>')
        s=s.replace('The statistics below apply to the existing HBOC / oxygen-carrier catalogue only. The external relevant-evidence layer is counted separately.','The statistics below cover all 62 unique transplantation records. Use the research-collection filter to separate 54 historical oxygen-carrier records from 8 related studies.')
        s=s.replace('Historical evidence by organ','Browse evidence by organ')
        s=s.replace('Counts represent catalogue records assigned to one primary transplant direction.','Counts represent records with the selected organ label. A study may appear under more than one organ.')
        s=s.replace('>Historical / direct oxygen-carrier catalogue</div><h2>Search','>Complete transplantation catalogue</div><h2>Search')
        # The collection remains 54 in the layer card; metadata describes the complete search.
        before,body=s.split('</head>',1)
        before=re.sub(r'\b54 (source-linked publications|publications|publication records)',lambda m:'62 '+m[1],before)
        before=before.replace('"dateModified":"2026-10-04"','"dateModified":"2026-10-11"')
        s=before+'</head>'+body
    # Legacy "institutionSearch" and other filter anchors are handled by the new shared search.
    p.write_text(css(s).replace('\\n  ','\n  '))

p=BASE/'veterinary/Vet-03-publication-BHOC-Oxyglobin.html';s=p.read_text()
s=re.sub(r'<section class="vet-pub-metrics"[\s\S]*?</section>',overview('product'),s);p.write_text(css(s))

# Shared counting method is user-facing; source-import housekeeping stays in the audit data.
p=BASE/'catalogues/methodology.html';old=p.read_text();head=old.split('</head>')[0]+'</head>'
head=re.sub(SOCIAL_IMAGE_PATTERN,'',head).replace('</head>',SOCIAL_IMAGE_META+'</head>')
reconciliation=count_reconciliation()
counting=f'''<section id="counting"><h2>How the publication total is calculated</h2><p>The three topic catalogues divide the same collection. They are not additions to the application searches.</p><table class="count-table"><thead><tr><th scope="col">Scientific catalogue</th><th scope="col">Records</th></tr></thead><tbody>{''.join(f'<tr><th scope="row"><a href="{PREFIX+PATHS[k]}">{E(TITLES[k])}</a></th><td>{STATS[k]["records"]}</td></tr>' for k in ['product','oxygen','related'])}<tr><th scope="row">Total, counted once</th><td><strong>{TOTAL['records']}</strong></td></tr></tbody></table><h3>Reconciling the earlier 475</h3><p>The earlier total added 236 Veterinary, 185 Human Use and 54 Transplant source entries. All 475 source entries remain represented. After reconciling repeated citations within and between those lists, they identify {reconciliation['originalDistinctRecords']} distinct publication records. Other imported sources contribute {reconciliation['netAddedRecords']} additional records: {reconciliation['originalDistinctRecords']} + {reconciliation['netAddedRecords']} = {TOTAL['records']}.</p><p>Different title forms and ahead-of-print citations are combined only when the publication identity is established. Related papers, conference abstracts and full articles with different identifiers remain separate. <a href="{PREFIX}catalogues/data/count-reconciliation.json">View the source-to-record count audit</a>.</p></section>'''
main=f'''<main id="main" class="catalogue-shell"><div class="breadcrumbs"><a href="{PREFIX}">Evidence Library</a> / About the catalogue</div>{tabs()}{appnav()}<section class="catalogue-hero"><h1>About the evidence catalogue</h1><p>Find publications across oxygen therapeutics, oxygen physiology and relevant clinical research.</p></section><section><h2>Three topics, one publication record</h2><p>Each publication has one primary scientific catalogue. Repeated entries are reconciled using DOI, PMID and bibliographic comparisons. Application searches draw from the same publication records and can overlap.</p><h2>How the statistics work</h2><p>Publication totals count unique records. Species, model and therapeutic groups follow the recorded metadata. Author institutions count indexed affiliation names; journal abbreviations and corresponding full names are combined. Missing labels are excluded from these counts. Statistics on search pages update with the active filters.</p><h2>Read findings in context</h2><p>Clinical, preclinical, analytical and review evidence should be interpreted at publication level. Historical product findings and studies of oxygen physiology do not establish BHOC efficacy, safety or regulatory approval. Author affiliations do not imply institutional endorsement or identify a confirmed study location.</p><p>Available DOI, PubMed and original source links support source checking. A supplied identifier does not mean that every bibliographic field or study conclusion has been independently verified. Incomplete source entries are excluded from public search.</p><p><a href="{PREFIX}usage-permission.html">Terms of Use &amp; Written Permission</a></p></section></main>'''
main=main.replace('</main>',counting+'</main>')
p.write_text(css(head)+'<body class="evidence-catalogue">'+HEADER+main+FOOTER+'</body></html>')

# Every linked metrics endpoint reflects the same published views.
platform={'snapshot':'2026-10-11','uniquePublications':len(RECORDS),'hubPlacements':sum(len(VIEWS[k]) for k in APP_LABELS),'evidenceHubs':3,'indexedAuthorInstitutions':TOTAL['institutions'],'normalizedJournalLabels':TOTAL['journals'],'catalogues':{k:STATS[k]['records'] for k in ['product','oxygen','related']},'hubs':{k:STATS[k]['records'] for k in APP_LABELS},'notes':{'counts':'Three topic catalogues are mutually exclusive. Application views overlap. Statistics use public bibliographic records only.','institutions':'Indexed author affiliations, not endorsements or confirmed study locations.'}}
(BASE/'platform-overview.json').write_text(json.dumps(platform,indent=2)+'\n')
news=ROOT/'news/knowledge-updates/index.html';s=news.read_text()
s=re.sub(r'The library contains \d+ unique publication records;',f'The library contains {len(RECORDS)} unique publication records;',s)
news.write_text(s)
vet={'snapshot':'2026-10-11',**STATS['veterinary'],'total':STATS['veterinary']['records'],'journalLabels':STATS['veterinary']['journals'],'groups':[{'value':v,'label':v,'count':n} for v,n in Counter(v for r in VIEWS['veterinary'] for v in r['speciesGroups']).items()],'notes':{'counts':'Records may carry more than one species or model label. Missing labels are not counted as an in-vitro model.'}}
(BASE/'veterinary/overview-statistics.json').write_text(json.dumps(vet,indent=2)+'\n')

# Preserve queries and anchors through the old root search URL.
p=BASE/'Vet-search.html';s=p.read_text()
if 'location.replace' not in s:s=s.replace('</head>','<script>location.replace("veterinary/Vet-search.html"+location.search+location.hash);</script></head>')
p.write_text(s)
print('Overview metrics, catalogue cards, application distributions and metadata synchronized.')
