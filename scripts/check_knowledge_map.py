"""Protect the user-approved multi-page BHOC release, using only Python stdlib."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import hashlib, json, re
ROOT=Path(__file__).resolve().parents[1]
ORIGIN='https://bhoctherapeutics.com'
BASELINE=ROOT/'bhoc/knowledge-map-baseline.json'

def normalized(parts):return ' '.join(' '.join(x.strip() for x in parts if x.strip()).split())
class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.ids=[];self.links=[];self.meta={};self.canonical=[];self.title=[];self.headings=[]
        self.main=[];self.paragraphs=[];self.h1count=0
        self.active_main=False;self.p=None;self.heading=None;self.intitle=False;self.skip=0
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.append(a['id'])
        if tag in ('script','style'):self.skip+=1
        if tag=='main':self.active_main=True
        if tag=='title':self.intitle=True
        if tag=='p':self.p=[]
        if tag in ('h1','h2','h3','h4'):self.heading=[]
        if tag=='h1':self.h1count+=1
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag=='meta':self.meta.setdefault(a.get('name') or a.get('property'),[]).append(a.get('content',''))
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
    def handle_endtag(self,tag):
        if tag in ('script','style'):self.skip=max(0,self.skip-1)
        if tag=='main':self.active_main=False
        if tag=='title':self.intitle=False
        if tag=='p' and self.p is not None:self.paragraphs.append(normalized(self.p));self.p=None
        if tag in ('h1','h2','h3','h4') and self.heading is not None:self.headings.append(normalized(self.heading));self.heading=None
    def handle_data(self,data):
        if self.skip:return
        if self.active_main:self.main.append(data)
        if self.p is not None:self.p.append(data)
        if self.heading is not None:self.heading.append(data)
        if self.intitle:self.title.append(data)

def check():
    b=json.loads(BASELINE.read_text())
    pages={};allparas=[];links=set();headings=[]
    for rel,record in b['pages'].items():
        p=Page((ROOT/rel).read_text());pages[rel]=p
        assert p.h1count==1,(rel,'H1 count',p.h1count)
        assert p.canonical==[record['canonical']],(rel,'canonical changed')
        assert len(p.ids)==len(set(p.ids)),(rel,'duplicate fragment IDs')
        actual=hashlib.sha256(normalized(p.main).encode()).hexdigest()
        assert actual==record['textSha256'],(rel,'approved main text changed')
        allparas.extend(p.paragraphs);headings.extend(p.headings)
        links.update(urljoin(ORIGIN+'/'+rel,a) for a in p.links)
        tokens=set(','.join(p.meta.get('robots',[])).lower().split(','))
        assert 'index' in tokens and not tokens.intersection({'noindex','nofollow','none'}),(rel,'global indexing blocked')
        assert p.meta.get('yandex')==['noindex'],(rel,'Yandex-only policy changed')
    missing=[t for t in b['sourceParagraphs']+b.get('archivedParagraphs',[]) if t not in allparas]
    assert not missing,('original prose missing',missing)
    assert all(t in headings for t in b.get('sourceHeadings',[])), 'Original chapter heading missing'
    assert set(b['originalLinkDestinations']).issubset(links), ('original source links missing',set(b['originalLinkDestinations'])-links)
    home=pages['bhoc/index.html']
    assert set(b['originalHubIds']).issubset(home.ids),'Old overview anchors removed'
    sitemap=(ROOT/'sitemap.xml').read_text()
    assert all('<loc>'+url+'</loc>' in sitemap for url in b['oldSitemapURLs']),'Existing sitemap URL removed'
    assert all('<loc>'+record['canonical']+'</loc>' in sitemap for record in b['pages'].values()),'New chapter missing from sitemap'
    rbc=pages['bhoc/red-blood-cell/index.html']
    assert b['bloodGroups']['source'] in rbc.links,'Blood-group internal link missing'
    assert '49 human blood-group systems and 400 antigens in the August 2026 ISBT release' in normalized(rbc.main),'Dated approved count changed'
    assert 'blood-group-systems' in rbc.ids,'RBC blood-group section missing'
    terms=pages['bhoc/terminology/index.html']
    assert 'In recent years' in normalized(terms.main),'Approved recent-years wording lost'
    assert 'In development' in normalized(terms.main),'Class-effect placeholder missing'
    assert not (ROOT/'bhoc/artificial-blood-blood-substitute/index.html').exists(),'Closed standalone draft exposed'
    for p in pages.values():
        assert not any('class-effect-review/' in href for href in p.links),'Unpublished class-effect article exposed'
    print(f'PASS: {len(pages)} knowledge-map pages, {len(b["sourceParagraphs"])} original paragraphs, {len(b.get("archivedParagraphs",[]))} restored approved paragraphs; existing IDs/URLs and blood-group source preserved.')

if __name__=='__main__':check()
