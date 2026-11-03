#!/usr/bin/env python3
"""Check actual desktop/mobile rendering, source preservation and crawlable navigation."""
from pathlib import Path
from urllib.parse import urlparse, unquote
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from collections import Counter
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json, zipfile, re

ROOT=Path.cwd(); OUT=Path('/tmp/bhoc-science');OUT.mkdir(parents=True,exist_ok=True)
PATHS=sorted(Path('evidence/library/science').glob('*.html'))+[Path('evidence/library/science/page/2/index.html'),Path('science/rbc-unit-hemoglobin-dose-variability.html'),Path('science/hypoxic-rbc-storage-kidney-oxygen-delivery.html')]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Quiet)
Thread(target=server.serve_forever,daemon=True).start()
BASE='http://127.0.0.1:'+str(server.server_port)
errors=[];report=[];seen_titles=set();seen_urls=set()
def check(value,message):
    if not value: errors.append(message)
original=zipfile.ZipFile(OUT/'source-before.zip')
for path in PATHS:
    s=BeautifulSoup(path.read_text(),'html.parser')
    check(len(s.select('h1'))==1,f'{path}: multiple/missing H1')
    check(len(s.select('link[rel=canonical]'))==1,f'{path}: canonical count')
    check(len(s.select('meta[name=description]'))==1,f'{path}: description count')
    check(s.title.get_text() not in seen_titles,f'{path}: duplicate title');seen_titles.add(s.title.get_text())
    url=s.select_one('link[rel=canonical]')['href'];check(url not in seen_urls,f'{path}: duplicate canonical');seen_urls.add(url)
    for node in s.select('script[type="application/ld+json"]'):json.loads(node.string or node.get_text())
    for el in s.select('[href],[src]'):
        for attr in ('href','src'):
            target=el.get(attr,'');u=urlparse(target)
            if target.startswith('/') and not target.startswith('//'):
                local=ROOT/unquote(u.path.lstrip('/'))
                check(local.exists(),f'{path}: missing local {target}')
    if str(path) in original.namelist():
        old=BeautifulSoup(original.read(str(path)).decode(),'html.parser')
        for sc in old.select('script[type="application/ld+json"]'):
            oldj=json.loads(sc.string or sc.get_text())
            if oldj.get('@type')=='ItemList':
                allnew=[json.loads(x.string or x.get_text()) for x in s.select('script[type="application/ld+json"]')]
                check(oldj in allnew,f'{path}: original bibliographic schema changed')
        check(len(old.select('article.publication'))==len(s.select('article.publication')),f'{path}: catalogue record loss')
        def sources(doc):
            return Counter(a['href'] for a in doc.select('main a[href]') if a['href'].startswith('http') and any(x in a['href'] for x in ('doi.org/','pubmed.ncbi.nlm.nih.gov/','nobelprize.org/')))
        check(not (sources(old)-sources(s)),f'{path}: a scientific source link was lost')
with sync_playwright() as pw:
    browser=pw.chromium.launch()
    for width in (390,768,1440):
        context=browser.new_context(viewport={'width':width,'height':1000},device_scale_factor=1)
        context.route(re.compile(r'https?://(?!127\.0\.0\.1)'),lambda route:route.abort())
        for path in PATHS:
            page=context.new_page();js_errors=[];missing=[]
            page.on('pageerror',lambda e:js_errors.append(str(e)))
            page.on('response',lambda r:missing.append(r.url) if r.status==404 and '127.0.0.1' in r.url else None)
            page.goto(BASE+'/'+str(path),wait_until='networkidle',timeout=30000)
            page.wait_for_selector('.bhoc-shell-header')
            dimensions=page.evaluate('''() => {const m=document.querySelector('main'),h=document.querySelector('main h1');return {viewport:innerWidth,scroll:document.documentElement.scrollWidth,mainWidth:m.getBoundingClientRect().width,mainX:m.getBoundingClientRect().x,h1:getComputedStyle(h).color,h1size:getComputedStyle(h).fontSize,h1visible:h.getBoundingClientRect().height>0,overflows:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>innerWidth+1||r.left < -1)&&!e.closest('.science-table-wrap,.rbc-table-wrap,.table-wrap,.bhoc-shell-old-skip,.bhoc-shell-skip,.skip')}).slice(0,12).map(e=>({tag:e.tagName,cls:e.className,width:e.getBoundingClientRect().width}))}}''')
            check(dimensions['scroll']<=width+1,f'{path} {width}: horizontal overflow {dimensions}')
            check(dimensions['mainWidth']<=1180.5,f'{path} {width}: article too wide')
            check(dimensions['mainWidth']>=width-45 if width<1180 else dimensions['mainWidth']>1100,f'{path} {width}: article too narrow')
            check(dimensions['h1visible'],f'{path} {width}: hidden heading')
            check(not js_errors,f'{path} {width}: JS errors {js_errors}')
            check(not missing,f'{path} {width}: local 404 {missing}')
            report.append({'page':str(path),'width':width,'dimensions':dimensions,'javascript_errors':js_errors,'missing_resources':missing})
            if width in (390,1440):
                name=('science-index' if path==Path('evidence/library/science/index.html') else 'science-page2' if '/page/2/' in str(path) else path.stem)
                page.screenshot(path=str(OUT/(name+'-'+str(width)+'.png')),full_page=False)
            page.close()
        context.close()
    ctx=browser.new_context(viewport={'width':1440,'height':1000})
    ctx.route(re.compile(r'https?://(?!127\.0\.0\.1)'),lambda route:route.abort())
    page=ctx.new_page();page.goto(BASE+'/evidence/library/science/?page=2',wait_until='networkidle')
    check('/science/page/2/' in page.url,'Legacy ?page=2 did not resolve to static page 2')
    check(page.locator('.science-cards .paper-card').count()==4,'Page2 featured count')
    page.locator('.science-feed-page a[data-page="1"]').click();page.wait_for_load_state('networkidle')
    check(page.locator('.science-cards .paper-card').count()==6,'Page1 featured count')
    page.locator('[data-science-search]').fill('L-TOF')
    check(page.locator('.science-cards .paper-card').count()==1,'Featured search does not span pages')
    page.locator('[data-science-search]').fill('no-such-scientific-paper-47258')
    check(page.locator('.science-cards .paper-card').count()==0,'Empty search fails')
    page.locator('[data-science-search]').fill('')
    check(page.locator('.science-cards .paper-card').count()==6,'Search reset fails')
    check(page.locator('.evidence-catalogue').count()==1,'Embedded catalogue missing')
    if page.locator('#q').count():
        page.locator('#q').fill('hypoxic');page.wait_for_timeout(500)
        check('230 publication records'!=page.locator('#result-count').inner_text(),'Catalogue search did not update')
        page.locator('#reset').click()
    ctx.close()
    ctx=browser.new_context(viewport={'width':390,'height':900});page=ctx.new_page()
    ctx.route(re.compile(r'https?://(?!127\.0\.0\.1)'),lambda route:route.abort())
    page.goto(BASE+'/evidence/library/science/oxygen-delivery-potency.html',wait_until='networkidle')
    page.locator('.bhoc-shell-menu-button').click()
    check(page.locator('.bhoc-shell-menu-button').get_attribute('aria-expanded')=='true','Mobile navigation fails')
    page.locator('.science-toc summary').click();check(page.locator('.science-toc').get_attribute('open') is not None,'Article TOC fails');ctx.close()
    ctx=browser.new_context(java_script_enabled=False);page=ctx.new_page()
    for route,count in [('/evidence/library/science/',6),('/evidence/library/science/page/2/',4)]:
        page.goto(BASE+route);check(page.locator('.science-cards .paper-card').count()==count,'No-JS pagination '+route)
    ctx.close();browser.close()
server.shutdown()
(OUT/'rendered-checks.json').write_text(json.dumps({'rendered_pages':len(report),'checks':report,'errors':errors},indent=2))
with zipfile.ZipFile(OUT/'source-after.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in PATHS+[Path('evidence/library/assets/science-20261103.css'),Path('evidence/library/assets/science-20261103.js'),Path('unified-shell.css'),Path('unified-shell.js')]:z.write(p)
print(json.dumps({'rendered_pages':len(report),'errors':errors},indent=2))
assert not errors,'Science verification failed; see rendered-checks.json'
