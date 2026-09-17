"""Validate real browser navigation on a served repository, not set_content mocks."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlsplit,urljoin,unquote
from collections import Counter
import threading,json,os,shutil,sys,re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
BASELINE=json.loads((ROOT/'bhoc/knowledge-map-baseline.json').read_text())
OUT=ROOT/'knowledge-map-test-results';OUT.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
report={'method':'Local HTTP server with real browser URL navigation','pages':[],'clickRoutes':[],'anchors':[],'errors':[]}
try:
 with sync_playwright() as p:
  executable=os.environ.get('BHOC_CHROMIUM') or shutil.which('chromium')
  opts={'headless':True}
  if executable:opts['executable_path']=executable
  browser=p.chromium.launch(**opts)
  for width in [1440,390]:
   ctx=browser.new_context(viewport={'width':width,'height':900},reduced_motion='reduce')
   ctx.route('**/*',lambda rt:rt.continue_() if rt.request.url.startswith(base) else rt.abort())
   page=ctx.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)))
   for slug,route in BASELINE['routes'].items():
    res=page.goto(base+route,wait_until='load');assert res.status==200,(route,res.status)
    assert page.locator('h1').count()==1,route
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(route,width,'overflow')
    assert page.locator('nav.crumbs strong[aria-current="page"]').count()==1,route
    if slug!='home':
     assert page.locator('.mobile-map nav a[aria-current="page"]').count()==1,(route,'menu location')
     back=page.locator('.back-map');dest=back.get_attribute('href')
     if not back.is_visible():back=page.locator('.chapter-footer a').filter(has_text='All BHOC topics')
     back.click()
     page.wait_for_url('**'+dest)
     assert page.url==base+dest,(route,'return to topic')
     page.go_back(wait_until='load');assert urlsplit(page.url).path==route
     footer=page.locator('.chapter-footer a').evaluate_all('(es)=>es.map(e=>e.getAttribute("href"))')
     for href in footer:
      if not href:continue
      page.goto(base+route,wait_until='load')
      page.locator('.chapter-footer a[href="'+href+'"]').click()
      page.wait_for_url('**'+href)
      assert page.locator('h1').count()==1
      report['clickRoutes'].append({'from':route,'to':href,'tested':'clicked'})
    report['pages'].append({'route':route,'width':width,'status':200,'breadcrumbs':True,'backRoundTrip':slug!='home'})
   # Every actual overview chapter link opens a full page directly, then returns.
   page.goto(base+'/bhoc/',wait_until='load')
   chapter_links=page.locator('main a[href^="/bhoc/"]').evaluate_all('(es)=>es.map(e=>({href:e.getAttribute("href"),id:e.id}))')
   for item in chapter_links:
    if not item['id'] or '#' in item['href']:continue
    page.goto(base+'/bhoc/',wait_until='load');page.locator('#'+item['id']).click()
    page.wait_for_url('**'+item['href'])
    assert page.locator('main').is_visible()
    report['clickRoutes'].append({'from':'/bhoc/#'+item['id'],'to':item['href'],'tested':'clicked'})
   # All former public hub fragments stay usable; none auto-redirect to another article.
   for fragment in BASELINE['originalHubIds']:
    page.goto(base+'/bhoc/#'+fragment,wait_until='load')
    assert page.locator('[id="'+fragment+'"]').count()==1,fragment
    assert urlsplit(page.url).fragment==fragment
    report['anchors'].append({'width':width,'fragment':fragment,'exists':True})
   page.goto(base+'/bhoc/',wait_until='load')
   assert page.locator('.topic-code').count()==14
   assert page.locator('.science-link').count()==4
   assert page.locator('.topic-grid>.legacy-anchor').count()==0,'Legacy anchors create empty grid cells'
   page.screenshot(path=str(OUT/f'published-overview-{width}.png'))
   page.screenshot(path=str(OUT/f'published-overview-{width}-full.png'),full_page=True)
   page.goto(base+'/bhoc/red-blood-cell/',wait_until='load')
   assert BASELINE['bloodGroups']['source']==page.locator('.blood-group-note a').get_attribute('href')
   page.locator('#blood-group-systems').scroll_into_view_if_needed()
   page.screenshot(path=str(OUT/f'published-rbc-blood-groups-{width}.png'))
   if width==390:
    page.evaluate('scrollTo(0,0)');menu=page.locator('.mobile-map').first
    menu.locator('summary').click();assert menu.get_attribute('open') is not None
    current=menu.locator('[aria-current="page"]');assert current.get_attribute('href')=='/bhoc/red-blood-cell/'
    page.keyboard.press('Escape');assert menu.get_attribute('open') is None
    menu.locator('summary').click();menu.locator('a[href="/bhoc/hemoglobin/"]').click()
    page.wait_for_url('**/bhoc/hemoglobin/');assert page.locator('h1').count()==1
   ctx.close()
  ctx=browser.new_context(viewport={'width':390,'height':900},java_script_enabled=False)
  ctx.route('**/*',lambda rt:rt.continue_() if rt.request.url.startswith(base) else rt.abort())
  page=ctx.new_page()
  page.goto(base+'/bhoc/',wait_until='load');page.locator('#erythrocyte-system').click();page.wait_for_url('**/bhoc/red-blood-cell/')
  assert page.locator('.blood-group-note').count()==1
  page.locator('.chapter-footer a[href="/bhoc/#erythrocyte-system"]').click();page.wait_for_url('**/bhoc/#erythrocyte-system')
  ctx.close();browser.close()
 assert not report['errors'],report['errors']
 (OUT/'served-route-checks.json').write_text(json.dumps(report,indent=2))
 print(f'PASS: {len(report["pages"])} served browser renders; {len(report["clickRoutes"])} route observations; {len(report["anchors"])} old-anchor checks; mobile/Escape/current-page indicators; no-JS click/return; no JS errors.')
finally:server.shutdown()
