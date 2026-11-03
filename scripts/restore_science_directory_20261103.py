#!/usr/bin/env python3
"""Restore only the directory presentation; preserve article pages and SEO metadata."""
from pathlib import Path
from copy import deepcopy
from urllib.parse import urljoin
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
import hashlib, json, re, subprocess, sys
from bs4 import BeautifulSoup

ROOT=Path.cwd()
INDEX=Path('evidence/library/science/index.html')
PAGE2=INDEX.parent/'page/2/index.html'
ORIGINAL='80f95d7b19fdbbf3aebef31001f13ec289f1926d'
BASE='https://bhoctherapeutics.com'
DIR='/evidence/library/science/'
ASSET=Path('evidence/library/assets/science-directory-five-20261103.js')
OUT=Path('/tmp/science-directory-restore');OUT.mkdir(exist_ok=True,parents=True)
JS=r'''/* Original Science directory appearance; exactly five featured publications per page. */
(()=>{'use strict';
 const root=document.querySelector('[data-science-feed]');if(!root)return;
 const base='/evidence/library/science/',size=5,params=new URLSearchParams(location.search);
 const grid=root.querySelector('.science-cards'),input=root.querySelector('[data-science-search]'),status=root.querySelector('[data-science-status]'),pager=root.querySelector('.science-feed-page');
 const template=document.getElementById('science-all-articles');if(!grid||!input||!template||!pager)return;
 const all=[...template.content.querySelectorAll('article.paper-card')];
 const urlFor=(n,q)=>{const u=new URL(n===1?base:base+'page/'+n+'/',location.origin);if(q)u.searchParams.set('q',q);return u.pathname+u.search;};
 const legacy=Number(params.get('page'));
 if(legacy>0&&location.pathname.replace(/index\.html$/,'')===base){
   params.delete('page');const n=Math.min(Math.max(1,Math.trunc(legacy)),Math.ceil(all.length/size));
   location.replace((n===1?base:base+'page/'+n+'/')+(params.size?'?'+params:'')+location.hash);return;
 }
 const readPage=()=>Number(location.pathname.match(/\/page\/(\d+)\//)?.[1]||1);
 function render(n,q,update){
   const needle=q.toLowerCase().trim(),matches=needle?all.filter(c=>c.textContent.toLowerCase().includes(needle)):all;
   const total=Math.max(1,Math.ceil(matches.length/size));n=Math.min(Math.max(1,n),total);
   const start=(n-1)*size,selected=matches.slice(start,start+size);
   grid.replaceChildren(...selected.map(c=>c.cloneNode(true)));
   status.textContent=matches.length?(start+1)+'–'+(start+selected.length)+' of '+matches.length+' publications':'No matching publications';
   if(!matches.length){const p=document.createElement('p');p.className='science-feed-empty';p.textContent='No featured publication matches this search.';grid.append(p);}
   pager.replaceChildren();
   for(let p=1;p<=total;p++){const a=document.createElement('a');a.href=urlFor(p,q);a.textContent='Page '+p;a.dataset.page=String(p);if(p===n)a.setAttribute('aria-current','page');pager.append(a);}
   pager.hidden=total===1;
   if(update)history.replaceState(null,'',urlFor(n,q)+location.hash);
 }
 input.value=params.get('q')||'';render(readPage(),input.value,false);
 input.addEventListener('input',()=>render(1,input.value,true));
 window.addEventListener('popstate',()=>{input.value=new URLSearchParams(location.search).get('q')||'';render(readPage(),input.value,false);});
})();
'''
EXTRA_CSS='''
/* Pagination links use the original directory button styling. */
body[data-science-directory-layout="original-five"] .science-cards{display:block}
body[data-science-directory-layout="original-five"] .paper-card h3 a{color:inherit;text-decoration:none}
body[data-science-directory-layout="original-five"] .paper-card h3 a:hover{text-decoration:underline}
body[data-science-directory-layout="original-five"] .science-feed-page a{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:9px 14px;border:1px solid #d0d8de;border-radius:999px;background:#fff;color:#102f49;font:inherit;font-size:14px;font-weight:700;text-decoration:none}
body[data-science-directory-layout="original-five"] .science-feed-page a[aria-current="page"]{border-color:var(--teal);color:var(--teal);background:#e5f3f1}
body[data-science-directory-layout="original-five"] .science-feed-page a:focus-visible{outline:2px solid var(--teal);outline-offset:3px}
'''

def soup(source):return BeautifulSoup(source,'html.parser')
def original_source():return subprocess.check_output(['git','show',ORIGINAL+':'+str(INDEX)],text=True)
def serial(doc):
    out='\n'.join(line.rstrip() for line in str(doc).splitlines()).rstrip()+'\n'
    return out.replace('content="summary_large_image" name="twitter:card"','name="twitter:card" content="summary_large_image"')
def article_hashes():
    paths=[p for p in INDEX.parent.glob('*.html') if p.name!='index.html']
    paths += [Path('science/rbc-unit-hemoglobin-dose-variability.html'),Path('science/hypoxic-rbc-storage-kidney-oxygen-delivery.html')]
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
def canonicalize_relative(node):
    for el in [node]+list(node.select('[href],[src]')):
        for attr in ('href','src'):
            value=el.get(attr)
            if value and not value.startswith(('/', '#','http:','https:','mailto:','tel:','data:')):
                el[attr]=urljoin(BASE+DIR,value).removeprefix(BASE)
def record_fingerprints(doc):
    return {x.get('id'):x.get_text(' ',strip=True) for x in doc.select('article.publication')}

def migrate():
    before_hashes=article_hashes();old=soup(original_source());current=soup(INDEX.read_text())
    template=current.select_one('#science-all-articles');assert template is not None
    cards=[deepcopy(c) for c in template.select('article.paper-card')]
    assert len(cards)==10, 'Unexpected publication count: review before changing pagination'
    records=record_fingerprints(current)
    for n,path in [(1,INDEX),(2,PAGE2)]:
        doc=soup(path.read_text());old_metadata=[str(e) for e in doc.head.select('meta,link[rel=canonical],title')]
        for el in list(doc.head.select('style,link[rel=stylesheet],script[src]')):el.decompose()
        # Reuse the exact visual CSS and navigation dependency order from before PR 89.
        for el in old.head.select('style,link[rel=stylesheet],script[src]'):
            copy=deepcopy(el);canonicalize_relative(copy);doc.head.append(copy)
        css=doc.new_tag('style',id='science-directory-five-controls');css.string=EXTRA_CSS;doc.head.append(css)
        doc.head.append(doc.new_tag('script',src='/'+str(ASSET),defer=''))
        for el in list(doc.select('body>header')):el.decompose()
        header=deepcopy(old.select_one('body>header'));canonicalize_relative(header);doc.body.insert(0,header)
        doc.body['class']=list(old.body.get('class',[]));doc.body['data-science-directory-layout']='original-five'
        doc.main.attrs=deepcopy(old.main.attrs)
        doc.h1.clear()
        for child in old.h1.contents:doc.h1.append(deepcopy(child))
        feed=doc.select_one('[data-science-feed]');grid=feed.select_one('.science-cards');grid.clear()
        selected=cards[(n-1)*5:n*5]
        for card in selected:grid.append(deepcopy(card))
        feed['data-page-size']='5';feed['data-pages']='2';feed['data-status']=f'{(n-1)*5+1}–{n*5} of {len(cards)} publications'
        feed.select_one('[data-science-status]').string=feed['data-status']
        label=feed.select_one('.science-feed-tools label');label['class']=['science-feed-search']
        input_tag=deepcopy(label.find('input'));input_tag['placeholder']='Search publications…';input_tag['aria-label']='Search publications';label.clear()
        hidden=doc.new_tag('span',attrs={'class':'sr-only'});hidden.string='Search publications';label.append(hidden);label.append(input_tag)
        pager=feed.select_one('.science-feed-page');pager.clear()
        for page_number in (1,2):
            a=doc.new_tag('a',href=DIR if page_number==1 else DIR+'page/2/');a['data-page']=str(page_number);a.string='Page '+str(page_number)
            if page_number==n:a['aria-current']='page'
            pager.append(a)
        schema=doc.select_one('#science-featured-schema');data=json.loads(schema.string)
        data['numberOfItems']=5
        data['itemListElement']=[{'@type':'ListItem','position':(n-1)*5+i+1,'name':card.h3.get_text(' ',strip=True),'url':urljoin(BASE,card.h3.a['href'])} for i,card in enumerate(selected)]
        schema.string=json.dumps(data,ensure_ascii=False,separators=(',',':'))
        assert record_fingerprints(doc)==records, 'Bibliography content must remain unchanged'
        assert old_metadata==[str(e) for e in doc.head.select('meta,link[rel=canonical],title')], 'Existing SEO metadata must stay intact'
        path.write_text(serial(doc))
    ASSET.write_text(JS.strip()+'\n')
    assert article_hashes()==before_hashes, 'An article was modified'
    report={'restored_from':ORIGINAL,'featured_publications':len(cards),'per_page':5,'catalogue_records_preserved':len(records),'article_hashes_unchanged':before_hashes,'changed_site_files':[str(INDEX),str(PAGE2),str(ASSET)]}
    (OUT/'migration.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

def verify():
    from playwright.sync_api import sync_playwright
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Quiet);Thread(target=server.serve_forever,daemon=True).start()
    origin='http://127.0.0.1:'+str(server.server_port)
    expected=soup(INDEX.read_text()).select_one('#science-all-articles').select('article.paper-card')
    expected_titles=[c.h3.get_text(' ',strip=True) for c in expected]
    assert len(expected_titles)==10
    metrics_js='''() => {const selectors=['main','.knowledge-hero','.knowledge-hero h1','.knowledge-grid','.knowledge-card','.paper-card h3','.science-side'];const out={};for(const selector of selectors){const el=document.querySelector(selector),cs=getComputedStyle(el);out[selector]={width:Math.round(el.getBoundingClientRect().width),fontSize:cs.fontSize,color:cs.color,background:cs.backgroundColor,padding:cs.padding,display:cs.display,gridTemplateColumns:cs.gridTemplateColumns};}return out;}'''
    results=[];before_metrics={};new_index=INDEX.read_text()
    with sync_playwright() as pw:
        browser=pw.chromium.launch()
        try:
            INDEX.write_text(original_source())
            for width in (390,768,1440):
                ctx=browser.new_context(viewport={'width':width,'height':1000})
                ctx.route(re.compile(r'https?://(?!127\.0\.0\.1)'),lambda route:route.abort())
                page=ctx.new_page();page.goto(origin+DIR,wait_until='networkidle');page.wait_for_selector('.bhoc-shell-header')
                before_metrics[width]=page.evaluate(metrics_js)
                if width!=768:page.screenshot(path=str(OUT/f'original-{width}.png'))
                ctx.close()
        finally:INDEX.write_text(new_index)
        for width in (390,768,1440):
            ctx=browser.new_context(viewport={'width':width,'height':1000})
            ctx.route(re.compile(r'https?://(?!127\.0\.0\.1)'),lambda route:route.abort())
            for n,route in ((1,DIR),(2,DIR+'page/2/')):
                page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                response=page.goto(origin+route,wait_until='networkidle');page.wait_for_selector('.bhoc-shell-header')
                assert response.status==200
                assert page.locator('.science-cards .paper-card').count()==5
                titles=page.locator('.science-cards .paper-card h3').all_text_contents()
                assert [t.strip() for t in titles]==expected_titles[(n-1)*5:n*5]
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
                now=page.evaluate(metrics_js)
                for selector,properties in before_metrics[width].items():
                    for key,value in properties.items():
                        if key=='width' and selector=='.paper-card h3':continue
                        assert now[selector][key]==value,(width,n,selector,key,value,now[selector][key])
                assert not errors,errors
                results.append({'width':width,'page':n,'visible_publications':5,'layout_matches_original':True,'javascript_errors':errors})
                if width!=768:page.screenshot(path=str(OUT/f'restored-page{n}-{width}.png'))
                page.close()
            ctx.close()
        ctx=browser.new_context();ctx.route(re.compile(r'https?://(?!127\.0\.0\.1)'),lambda route:route.abort())
        page=ctx.new_page();page.goto(origin+DIR+'?page=2',wait_until='networkidle')
        assert '/page/2/' in page.url
        assert page.locator('.science-cards .paper-card').count()==5
        page.locator('.science-feed-page a[data-page="1"]').click();page.wait_for_load_state('networkidle')
        assert page.locator('.science-cards .paper-card').count()==5
        page.locator('[data-science-search]').fill('oxygen');assert 0<page.locator('.science-cards .paper-card').count()<=5
        if page.locator('.science-feed-page a[data-page="2"]').count():
            page.locator('.science-feed-page a[data-page="2"]').click();page.wait_for_load_state('networkidle');assert 0<page.locator('.science-cards .paper-card').count()<=5
        page.locator('[data-science-search]').fill('no-match-37854390');assert page.locator('.science-cards .paper-card').count()==0
        page.locator('[data-science-search]').fill('');assert page.locator('.science-cards .paper-card').count()==5
        page.locator('#q').fill('hypoxic');page.wait_for_timeout(400)
        assert page.locator('#result-count').inner_text()!='230 publication records'
        page.locator('#reset').click();ctx.close()
        ctx=browser.new_context(java_script_enabled=False);page=ctx.new_page()
        for route in (DIR,DIR+'page/2/'):
            page.goto(origin+route);assert page.locator('.science-cards .paper-card').count()==5
        ctx.close();browser.close()
    server.shutdown()
    (OUT/'verification.json').write_text(json.dumps({'result':'PASS','pages':results,'legacy_url':'PASS','search_pagination':'PASS','no_javascript':'PASS','catalogue_search':'PASS'},indent=2));print('PASS: original layout restored; five items per page; links, search, catalogue, legacy URL and no-JS pagination verified.')

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='verify':verify()
    else:migrate()
