"""Synchronize visible metrics, metadata and catalogue navigation with search views."""
import re, json, html
from urllib.parse import quote
from evidence_catalogue_model import *
from build_evidence_catalogues import E, PREFIX, VERSION, TITLES, PATHS, metric_html, collection_summary, tabs, appnav, DESCRIPTIONS, HEADER, FOOTER, filters, card, BOUNDARIES, pagination, SOCIAL_IMAGE_PATTERN, SOCIAL_IMAGE_META, release_notice, LITERATURE_REVIEW

def css(s):
    href=PREFIX+'catalogues/catalogues.css?v='+VERSION
    if re.search(r'<link[^>]+href="[^"]*catalogues\.css[^"]*"[^>]*>',s):
        s=re.sub(r'<link[^>]+href="[^"]*catalogues\.css[^"]*"[^>]*>',f'<link rel="stylesheet" href="{href}">',s)
    else:s=s.replace('</head>',f'<link rel="stylesheet" href="{href}"></head>')
    return s

def catalogue_entry(cards=True):
    out='<section id="scientific-catalogues" class="catalogue-entry"><div class="eyebrow">Explore the scientific literature</div><h2>Scientific Evidence Relevant to BHOC</h2><p>Find publications by topic, species, author, institution, journal and year.</p>'
    out+=f'<p class="catalogue-search-action"><a href="{PREFIX+PATHS["all"]}">Search all publications together →</a></p>'
    if cards:
        out+='<div class="catalogue-card-grid">'
        for k in ['product','oxygen','related']:
            if k=='product':
                out+=f'<article class="catalogue-card"><div class="eyebrow">Research collections</div><h3>Veterinary, Human &amp; Transplant Evidence</h3><p>Browse veterinary, human-use and transplantation publications. Search by species, author, institution, journal and year.</p>{metric_html("applications")}<a class="button" href="#evidence-hubs">Explore collections →</a></article>'
                continue
            out+=f'<article class="catalogue-card"><div class="eyebrow">Research catalogue</div><h3>{E(TITLES[k])}</h3><p>{E(DESCRIPTIONS[k])}</p>{metric_html(k)}<a class="button" href="{PREFIX+PATHS[k]}">Explore catalogue →</a></article>'
        out+='</div>'
    else:out+=tabs()
    return out+'</section>'

for f in [BASE/'index.html',ROOT/'evidence/index.html']:
    s=f.read_text();s=re.sub(r'<!-- collection-summary:start -->[\s\S]*?<!-- collection-summary:end -->','',s);s=re.sub(r'<section[^>]*id="scientific-catalogues"[\s\S]*?</section>',catalogue_entry(f==BASE/'index.html'),s)
    if f==ROOT/'evidence/index.html':
        s=re.sub(r'<strong>\d+</strong><span>publication &amp; evidence records</span>|<strong>\d+</strong><span>publication & evidence records</span>',f'<strong>{TOTAL["records"]}</strong><span>publication records</span>',s)
        s=re.sub(r'<strong>\d+</strong><span>(?:publication records|entries across five collections|library entries)</span>',f'<strong>{publication_counter()["displayedTotal"]}</strong><span>library entries</span>',s)
        s=s.replace('href="https://bhoctherapeutics.com/evidence/library/" target="_blank" rel="noopener noreferrer">Explore the evidence ↗','href="/evidence/library/catalogues/">Search all publications →')
        s=re.sub(r'<strong>\d+</strong><span>scientific journals</span>',f'<strong>{TOTAL["journals"]}</strong><span>scientific journals</span>',s)
        s=re.sub(r'<strong>\d+</strong><span>author institutions</span>',f'<strong>{TOTAL["institutions"]}</strong><span>author institutions</span>',s)
        s=s.replace('<strong>3</strong><span>application hubs</span>','<strong>5</strong><span>publication collections</span>')
        s=re.sub(r'<p id="evidence-count-note">[\s\S]*?</p>','',s)
    if f==BASE/'index.html':
        # The original application hubs stay together, followed by the combined search and three catalogues.
        s=re.sub(r'<section[^>]*id="scientific-catalogues"[\s\S]*?</section>','',s)
        s=re.sub(r'(<section id="evidence-hubs"[\s\S]*?</section>)',lambda m:m[1]+'\n'+catalogue_entry(True),s)
        s=s.replace('href="#scientific-catalogues">Explore the evidence','href="#evidence-hubs">Explore the evidence')
        product_link=f'<p class="application-catalogue-link" data-product-catalogue-link><a href="{PREFIX+PATHS["product"]}">Oxyglobin &amp; Hemopure: search product evidence across applications →</a></p>'
        s=re.sub(r'<p[^>]*data-product-catalogue-link[\s\S]*?</p>','',s)
        s=re.sub(r'(<section id="evidence-hubs"[\s\S]*?)(</section>)',lambda m:m[1]+product_link+m[2],s)
        if 'data-evidence-layout-fix' not in s:
            s=s.replace('</head>','<style data-evidence-layout-fix>body.evidence-library-unified.bhoc-shell-ready>.bhoc-shell-header,body.evidence-library-unified.bhoc-shell-ready>.bhoc-shell-trail,body.evidence-library-unified.bhoc-shell-ready>.bhoc-shell-footer{width:100%;margin-left:0}</style></head>')
        if 'data-evidence-unified=' not in s:s=s.replace('<body','<body data-evidence-unified="true"',1)
        if 'evidence-library-unified' not in re.search(r'<body[^>]*>',s)[0]:s=re.sub(r'<body([^>]*)class="([^"]*)"',lambda m:'<body'+m[1]+'class="'+m[2]+' evidence-library-unified"',s,count=1)
        s=re.sub(r'<section (?:class="overview-stats platform-stats"|aria-label="Evidence Library statistics")[\s\S]*?</section>',collection_summary()+'<section aria-label="Evidence Library statistics">'+metric_html('all')+'</section>',s)
        s=re.sub(r'<p class="catalogue-search-action" id="all-publications-entry"[^>]*>[\s\S]*?</p>','',s)
        s=re.sub(r'(<section aria-label="Evidence Library statistics">[\s\S]*?</section>)',lambda m:m[1]+f'<p class="catalogue-search-action" id="all-publications-entry" style="text-align:center"><a href="{PREFIX+PATHS["all"]}">Search all publications together →</a></p>',s)
        application_total=sum(STATS[k]['records'] for k in APP_LABELS)
        s=re.sub(r'<div class="count-breakdown" id="catalogue-count-breakdown">[\s\S]*?</div>','',s)
        s=re.sub(r'<p class="metric-note" id="institutions-note">[\s\S]*?</p>','',s)
        for kind,cls in [('veterinary','vet'),('transplant','transplant'),('human','human')]:
            pattern=r'(<article class="panel hub-card '+cls+r'">[\s\S]*?<div class="hub-facts">)[\s\S]*?(</div><a class="button")'
            st=STATS[kind];facts=''.join(f'<div><strong>{st[field]}</strong><span>{label}</span></div>' for field,label in [('records','PUBLICATION RECORDS'),('groups',st['groupLabel'].upper()),('institutions','AUTHOR INSTITUTIONS'),('journals','JOURNALS')])
            s=re.sub(pattern,lambda m:m[1]+facts+m[2],s)
        s=re.sub(r'<span class="tag">Updated \d{1,2} [A-Za-z]+ \d{4}</span>','',s)
    s=re.sub(r'<p[^>]*data-literature-update="20261030"[^>]*>[\s\S]*?</p>','',s)
    if LITERATURE_REVIEW:
        marker='<section id="scientific-catalogues"'
        s=s.replace(marker,release_notice('all')+marker,1)
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
    s=re.sub(r'Search \d+ author institutions, browse \d+ normalized journal labels',f'Search {st["institutions"]} author institutions, browse {st["journals"]} normalized journal labels',s)
    s=re.sub(r'Search \d+ indexed author institutions and \d+ normalized journal labels',f'Search {st["institutions"]} indexed author institutions and {st["journals"]} normalized journal labels',s)
    if kind=='veterinary':
        s=re.sub(r'<p class="overview-caption">The (?:species distribution and catalogue below|distribution and search use the same)[\s\S]*?</p>',f'<p class="overview-caption">The distribution and search use the same {st["records"]} unique publication records. A record can carry more than one species or model label.</p>',s)
        s=re.sub(r'(?:236|239) (?:base |searchable )?(?:publication )?records',f'{st["records"]} publication records',s)
        s=s.replace('Other / In vitro includes in-vitro labels and 13 records with no species label.','Missing species labels are shown separately from in-vitro models.')
        s=s.replace('Use Library scope to separate BHOC / Oxyglobin-focused records from background literature. Every record remains accessible under All records.','Use the Catalogue filter to distinguish Oxyglobin and Hemopure research, oxygen physiology and related scientific literature.')
    if kind=='human':
        s=re.sub(r'\b\d+ source-linked human clinical and separately labelled translational records',str(st['records'])+' source-linked human clinical and separately labelled translational records',s)
        s=re.sub(r'\b(?:180|181|184|185) (human-use and translational publications|publications|total records|records)',lambda m:str(st['records'])+' '+m[1],s)
        s=s.replace('<strong>46</strong>','<strong>45</strong>')
        clinical=sum('Human clinical evidence' in r['evidenceGroups'] for r in VIEWS[kind])
        s=s.replace('<dt>Human clinical records</dt>','<dt>Human clinical publications</dt>')
        s=s.replace('<dt>Translational preclinical records</dt>','<dt>Translational preclinical publications</dt>')
        s=re.sub(r'(<dt>Human clinical publications</dt><dd>)\d+',lambda m:m[1]+str(clinical),s)
    if kind=='transplant':
        historical=sum('Historical oxygen-carrier research' in r['collection'] for r in VIEWS[kind])
        related_count=sum('Related transplantation studies' in r['collection'] for r in VIEWS[kind])
        s=re.sub(r'The statistics below cover all \d+ unique transplantation records\. Use the research-collection filter to separate \d+ historical oxygen-carrier records from \d+ related studies\.',f'The statistics below cover all {st["records"]} unique transplantation records. Use the research-collection filter to separate {historical} historical oxygen-carrier records from {related_count} related studies.',s)
        # Keep the two scientific evidence layers and expose their actual matching subsets.
        s=re.sub(r'\b(?:5|8|10) related records',str(sum('Related transplantation studies' in r['collection'] for r in VIEWS[kind]))+' related records',s)
        s=s.replace('href="Transplant-search.html">Historical HBOC evidence','href="Transplant-search.html?collection=Historical%20oxygen-carrier%20research">Historical HBOC evidence')
        s=s.replace('href="Transplant-search.html">Search historical evidence','href="Transplant-search.html?collection=Historical%20oxygen-carrier%20research">Search historical evidence')
        s=s.replace('<h2>54 source-linked records</h2>','<h2>Search the complete transplantation catalogue</h2>')
        s=s.replace('The statistics below apply to the existing HBOC / oxygen-carrier catalogue only. The external relevant-evidence layer is counted separately.','The statistics below cover all 64 unique transplantation records. Use the research-collection filter to separate 54 historical oxygen-carrier records from 10 related studies.')
        s=s.replace('Historical evidence by organ','Browse evidence by organ')
        s=s.replace('Counts represent catalogue records assigned to one primary transplant direction.','Counts represent records with the selected organ label. A study may appear under more than one organ.')
        s=s.replace('>Historical / direct oxygen-carrier catalogue</div><h2>Search','>Complete transplantation catalogue</div><h2>Search')
        # The collection remains 54 in the layer card; metadata describes the complete search.
        before,body=s.split('</head>',1)
        before=re.sub(r'\b54 (source-linked publications|publications|publication records)',lambda m:str(STATS[kind]['records'])+' '+m[1],before)
        before=re.sub(r'\b62 (source-linked publications|publications|publication records)',lambda m:str(STATS[kind]['records'])+' '+m[1],before)
        before=re.sub(r'\b\d+ (source-linked publications|publications|publication records)',lambda m:str(STATS[kind]['records'])+' '+m[1],before)
        before=before.replace('"dateModified":"2026-10-04"','"dateModified":"2026-10-11"')
        s=before+'</head>'+body
    # Legacy "institutionSearch" and other filter anchors are handled by the new shared search.
    p.write_text(css(s).replace('\\n  ','\n  '))

p=BASE/'veterinary/Vet-03-publication-BHOC-Oxyglobin.html';s=p.read_text()
s=re.sub(r'<section class="(?:vet-pub-metrics|overview-stats)"[\s\S]*?</section>',overview('product'),s)
if LITERATURE_REVIEW:
    s=s.replace('The new <a href="../catalogues/product.html">Product Evidence Catalogue</a> separates direct product-associated records from general scientific literature. The figures below refer to the preserved broader veterinary source index, including related literature.','The <a href="../catalogues/product.html">Product Evidence Catalogue</a> contains product-associated Oxyglobin and Hemopure publication records across applications. The figures below describe that catalogue. They include different study designs and are not a count of independent clinical trials.')
    s=re.sub(r'Evidence page updated 26 September 2026\. The active publication search contains the preserved 236-record base bibliography plus three source-verified curated additions\.','Evidence page updated 30 October 2026. Twenty-three source-linked publications were added to the shared library, including 21 in the Veterinary application view. The original 236-record bibliography and three earlier curated additions remain preserved.',s)
    s=re.sub(r'<section id="literature-update-20261030"[\s\S]*?</section>','',s)
    blocks=[]
    for kind,label in [('product','Product-associated publications'),('related','Related studies, reviews and formulation context')]:
        items=[]
        for r in sorted([r for r in LITERATURE_REVIEW['records'] if r['catalogue']==kind],key=lambda r:(-int(r['year']),r['title'])):
            target=PREFIX+PATHS[kind]+'#'+r['id']
            items.append('<li><a href="'+E(target)+'">'+E(r['title'])+'</a> ('+E(r['year'])+'). <small>'+E(r['evidenceType'])+'</small></li>')
        blocks.append('<h3>'+label+'</h3><ol>'+''.join(items)+'</ol>')
    update='<section id="literature-update-20261030" class="panel"><div class="eyebrow">Library update · 30 October 2026</div><h2>23 source-linked publication records added</h2><p>The additions include clinical reports, preclinical studies, analytical methods, reviews and one conference abstract. Twelve are product-associated records and eleven remain in Related Scientific Articles. Publication counts do not represent independent trial counts.</p><p>Each record states its study setting and source-review limits. Unconfirmed commercial formulations remain related context. Seven archival citations still require primary documents and were not added as verified publications. Existing records, including Callan and Rentko 2003 and the Zambelli 2009 clinical comparison, were retained without duplication.</p>'+''.join(blocks)+'</section>'
    s=s.replace('</main>',update+'</main>')
p.write_text(css(s))

# Keep catalogue guidance without public counting explanations.
p=BASE/'catalogues/methodology.html';old=p.read_text();head=old.split('</head>')[0]+'</head>'
head=re.sub(SOCIAL_IMAGE_PATTERN,'',head).replace('</head>',SOCIAL_IMAGE_META+'</head>')
head=re.sub(r'<meta\b(?=[^>]*\bproperty=["\']og:type["\'])[^>]*>','',head,flags=re.I)
head=head.replace('</head>','<meta property="og:type" content="website"></head>')
main=f'''<main id="main" class="catalogue-shell"><div class="breadcrumbs"><a href="{PREFIX}">Evidence Library</a> / About the catalogue</div>{tabs()}{appnav()}<section class="catalogue-hero"><h1>About the evidence catalogue</h1><p>Find publications across oxygen therapeutics, oxygen physiology and relevant clinical research.</p></section><section><h2>Read findings in context</h2><p>Clinical, preclinical, analytical and review evidence should be interpreted at publication level. Historical product findings and studies of oxygen physiology do not establish BHOC efficacy, safety or regulatory approval. Author affiliations do not imply institutional endorsement or identify a confirmed study location.</p><p>Available DOI, PubMed and original source links support source checking. A supplied identifier does not mean that every bibliographic field or study conclusion has been independently verified. Incomplete source entries are excluded from public search.</p><p><a href="{PREFIX}usage-permission.html">Terms of Use &amp; Written Permission</a></p></section></main>'''
main=main.replace('</main>',collection_summary()+'</main>')
method_header=re.search(r'<header class="site-header">[\s\S]*?</header>',old)
method_footer=re.search(r'<footer class="site-footer">[\s\S]*?</footer>',old)
p.write_text(css(head)+'<body class="evidence-catalogue">'+(method_header[0] if method_header else HEADER)+main+(method_footer[0] if method_footer else FOOTER)+'</body></html>')

# Every linked metrics endpoint reflects the same published views.
platform={'publicationCounter':publication_counter(),'collectionTotals':collection_totals(),'snapshot':DATA['updated'],'uniquePublications':len(RECORDS),'hubPlacements':sum(len(VIEWS[k]) for k in APP_LABELS),'evidenceHubs':3,'indexedAuthorInstitutions':TOTAL['institutions'],'normalizedJournalLabels':TOTAL['journals'],'catalogues':{k:STATS[k]['records'] for k in ['product','oxygen','related']},'hubs':{k:STATS[k]['records'] for k in APP_LABELS},'notes':{'counts':'The displayed publication counter retains the user-approved baseline and increments once per new publication. Topic catalogues are mutually exclusive; application views overlap.','institutions':'Indexed author affiliations, not endorsements or confirmed study locations.'}}
(BASE/'platform-overview.json').write_text(json.dumps(platform,indent=2)+'\n')
# Historical knowledge-update entries retain the counts at their publication date.
vet={'snapshot':DATA['updated'],**STATS['veterinary'],'total':STATS['veterinary']['records'],'journalLabels':STATS['veterinary']['journals'],'groups':[{'value':v,'label':v,'count':n} for v,n in Counter(v for r in VIEWS['veterinary'] for v in r['speciesGroups']).items()],'notes':{'counts':'Records may carry more than one species or model label. Missing labels are not counted as an in-vitro model.'}}
(BASE/'veterinary/overview-statistics.json').write_text(json.dumps(vet,indent=2)+'\n')

# Preserve queries and anchors through the old root search URL.
p=BASE/'Vet-search.html';s=p.read_text()
if 'location.replace' not in s:s=s.replace('</head>','<script>location.replace("veterinary/Vet-search.html"+location.search+location.hash);</script></head>')
p.write_text(s)
print('Overview metrics, catalogue cards, application distributions and metadata synchronized.')
