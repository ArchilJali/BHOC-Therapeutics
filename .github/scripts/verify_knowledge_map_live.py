"""Verify the public release, not just a local build. Read-only HTTP/browser audit."""
from pathlib import Path
from urllib.parse import urljoin,urlsplit,unquote
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess,time,urllib.request,re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
ORIGIN='https://bhoctherapeutics.com'
BASE='f6cb0101410c4196a2651952bfce946e1082558b'
OUT=ROOT/'knowledge-map-live-results';OUT.mkdir(exist_ok=True)
baseline=json.loads((ROOT/'bhoc/knowledge-map-baseline.json').read_text())
report={'origin':ORIGIN,'verifiedAtUTC':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'publicPages':[],'oldRoutes':[],'internalCrossSiteLinks':[],'browser':[],'errors':[]}

def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'BHOC-Release-Verification/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=35) as response:return response.status,response.read().decode('utf-8'),response.url

def metadata(raw):
 s=BeautifulSoup(raw,'html.parser')
 return {'title':s.title.get_text() if s.title else '', 'meta':sorted((m.get('name',''),m.get('property',''),m.get('content','')) for m in s.select('head meta')),'canonical':[m.get('href') for m in s.select('head link[rel=canonical]')]}

def ready():
 status,body,_=get(ORIGIN+'/bhoc/?release='+report['commit'][:12])
 return status==200 and 'data-bhoc-knowledge-map="published"' in body and '/bhoc/red-blood-cell/' in body
try:
 for attempt in range(36):
  try:
   if ready():break
  except Exception as error:print('Deployment not observable yet:',type(error).__name__)
  if attempt==35:raise AssertionError('Public overview did not reach the approved release during verification')
  time.sleep(10)
 print('Public overview exposes the approved multi-page release.')
 public={}
 for rel in baseline['pages']:
  route='/'+rel.removesuffix('index.html')
  status,body,final=get(ORIGIN+route+'?release='+report['commit'][:12])
  local=(ROOT/rel).read_text()
  assert status==200,(route,status)
  assert metadata(body)==metadata(local),(route,'public metadata does not match release')
  s=BeautifulSoup(body,'html.parser');expected=BeautifulSoup(local,'html.parser')
  norm=lambda e:' '.join(e.get_text(' ',strip=True).split())
  assert norm(s.select_one('main'))==norm(expected.select_one('main')),(route,'public text differs')
  assert [a.get('href') for a in s.select('main a')]==[a.get('href') for a in expected.select('main a')],(route,'public links differ')
  for block in s.select('script[type="application/ld+json"]'):json.loads(block.get_text())
  public[route]=s
  report['publicPages'].append({'route':route,'status':status,'metadataMatches':True,'fullMainTextMatches':True,'linksMatch':True,'structuredDataParses':True})
 for asset in ['/bhoc/knowledge-map.css','/bhoc/knowledge-map.js']:
  status,body,_=get(ORIGIN+asset+'?release='+report['commit'][:12])
  assert status==200 and body==(ROOT/asset.lstrip('/')).read_text(),(asset,'stale asset')
 oldmap=subprocess.check_output(['git','show',BASE+':sitemap.xml'],cwd=ROOT,text=True)
 oldurls=re.findall(r'<loc>(.*?)</loc>',oldmap)
 for url in oldurls:
  status,body,_=get(url)
  assert status==200,(url,'old indexed route unavailable')
  report['oldRoutes'].append({'url':url,'status':status})
 status,sitemap,_=get(ORIGIN+'/sitemap.xml?release='+report['commit'][:12])
 assert all('<loc>'+url+'</loc>' in sitemap for url in oldurls),'Old sitemap entry lost on public site'
 assert all('<loc>'+item['canonical']+'</loc>' in sitemap for item in baseline['pages'].values()),'New chapter absent from public sitemap'
 for fragment in baseline['originalHubIds']:assert public['/bhoc/'].find(id=fragment),('Old public anchor lost',fragment)
 oldhistory=BeautifulSoup(subprocess.check_output(['git','show',BASE+':bhoc/historical-evolution/index.html'],cwd=ROOT,text=True),'html.parser')
 assert {e['id'] for e in oldhistory.select('[id]')}.issubset({e['id'] for e in public['/bhoc/historical-evolution/'].select('[id]')}),'Old historical anchor missing on public site'
 # Verify owned-platform destinations independently of external papers and DOI servers.
 destinations=set()
 for s in public.values():
  for a in s.select('main a[href]'):
   u=urlsplit(urljoin(ORIGIN,a['href']))
   if u.hostname in ['archiljali.github.io','bhocvet.com']:
    destinations.add(u._replace(fragment='').geturl())
 def owned(url):
  try:
   status,body,final=get(url)
   return {'url':url,'status':status,'finalURL':final,'ok':status==200}
  except Exception as error:return {'url':url,'ok':False,'error':str(error)}
 with ThreadPoolExecutor(max_workers=4) as pool:report['internalCrossSiteLinks']=list(pool.map(owned,sorted(destinations)))
 # Actual browser navigation from overview to every chapter and back at both sizes.
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  for width in [1440,390]:
   ctx=browser.new_context(viewport={'width':width,'height':900},reduced_motion='reduce')
   ctx.route('**/*',lambda rt:rt.continue_() if urlsplit(rt.request.url).hostname=='bhoctherapeutics.com' else rt.abort())
   page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   for slug,route in baseline['routes'].items():
    r=page.goto(ORIGIN+route,wait_until='load');assert r.status==200,(route,width)
    assert page.locator('h1').count()==1 and page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(route,'layout')
    assert page.locator('.crumbs strong[aria-current="page"]').count()==1,(route,'breadcrumb')
    if slug!='home':
     footer=page.locator('.chapter-footer a').filter(has_text='All BHOC topics')
     destination=footer.get_attribute('href');footer.click();page.wait_for_url('**'+destination)
     assert urlsplit(page.url).path=='/bhoc/'
    report['browser'].append({'route':route,'width':width,'status':200,'breadcrumbs':True,'returnClick':slug!='home','noOverflow':True})
   page.goto(ORIGIN+'/bhoc/');page.screenshot(path=str(OUT/f'live-overview-{width}.png'));page.screenshot(path=str(OUT/f'live-overview-{width}-full.png'),full_page=True)
   page.locator('#erythrocyte-system').click();page.wait_for_url('**/bhoc/red-blood-cell/')
   page.locator('#blood-group-systems').scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'live-rbc-blood-groups-{width}.png'))
   assert baseline['bloodGroups']['source']==page.locator('.blood-group-note a').get_attribute('href')
   if width==390:
    page.evaluate('scrollTo(0,0)');menu=page.locator('.mobile-map').first;menu.locator('summary').click()
    assert menu.locator('a[aria-current="page"]').get_attribute('href')=='/bhoc/red-blood-cell/'
    page.keyboard.press('Escape');assert menu.get_attribute('open') is None
   assert not errors,errors
   ctx.close()
  ctx=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':900})
  page=ctx.new_page();page.goto(ORIGIN+'/bhoc/');page.locator('#erythrocyte-system').click();page.wait_for_url('**/bhoc/red-blood-cell/')
  page.locator('.chapter-footer a').filter(has_text='All BHOC topics').click();page.wait_for_url('**/bhoc/#erythrocyte-system')
  report['noJavaScriptClickAndReturn']=True;ctx.close();browser.close()
 report['coreReleaseVerified']=True
 failures=[x for x in report['internalCrossSiteLinks'] if not x['ok']]
 report['ownedLinkWarnings']=failures
 print('PASS public deployment:',len(report['publicPages']),'full pages;',len(report['oldRoutes']),'old indexed URLs;',len(report['browser']),'desktop/mobile browser renders and return paths; sitemap/metadata/old anchors preserved.')
 if failures:print('OWNED DESTINATION WARNINGS:',json.dumps(failures))
except Exception as error:
 report['coreReleaseVerified']=False;report['errors'].append(str(error));raise
finally:
 (OUT/'live-verification.json').write_text(json.dumps(report,indent=2)+'\n')
