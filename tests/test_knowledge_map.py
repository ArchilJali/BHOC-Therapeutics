"""Local Chromium renders plus static route checks; no live deployment testing."""
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json,os,shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'knowledge-map-test-results';OUT.mkdir(exist_ok=True)
b=json.loads((ROOT/'bhoc/knowledge-map-baseline.json').read_text())
checks=[];errors=[]
css=(ROOT/'bhoc/knowledge-map.css').read_text();js=(ROOT/'bhoc/knowledge-map.js').read_text()
def source(route):
    s=BeautifulSoup((ROOT/(route.lstrip('/')+'index.html')).read_text(),'html.parser')
    for x in s.select('script[src],link[rel=stylesheet]'):x.decompose()
    style=s.new_tag('style');style.string=css;s.head.append(style)
    script=s.new_tag('script');script.string=js;s.body.append(script)
    return str(s)
with sync_playwright() as p:
    executable=os.environ.get('BHOC_CHROMIUM') or shutil.which('chromium')
    options={'headless':True,'args':['--no-sandbox']}
    if executable:options['executable_path']=executable
    browser=p.chromium.launch(**options)
    for width in [1440,390]:
        c=browser.new_context(viewport={'width':width,'height':900},reduced_motion='reduce')
        c.route('**/*',lambda rt:rt.abort())
        page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        for slug,route in b['routes'].items():
            page.set_content(source(route),wait_until='domcontentloaded');page.wait_for_timeout(45)
            assert page.locator('main').is_visible(),slug
            assert page.locator('h1').count()==1,(slug,'h1')
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(slug,width,'overflow')
            if slug=='home':
                assert page.locator('.topic-code').count()==14
                assert page.locator('.science-link').count()==4
                assert page.locator('#class-effect-review a').count()==0
                assert page.locator('#erythrocyte-system').get_attribute('href')=='/bhoc/red-blood-cell/'
                page.screenshot(path=str(OUT/f'overview-{width}.png'))
                page.screenshot(path=str(OUT/f'overview-{width}-full.png'),full_page=True)
            if slug=='rbc':
                assert '49 human blood-group systems and 400 antigens' in page.locator('.blood-group-note').inner_text()
                assert page.locator('.blood-group-note a').get_attribute('href')==b['bloodGroups']['source']
                page.screenshot(path=str(OUT/f'rbc-{width}.png'))
                page.locator('#blood-group-systems').scroll_into_view_if_needed()
                page.screenshot(path=str(OUT/f'rbc-blood-groups-{width}.png'))
                if width==390:
                    page.evaluate('scrollTo(0,0)')
                    menu=page.locator('.mobile-map').first
                    menu.locator('summary').click();assert menu.get_attribute('open') is not None
                    page.keyboard.press('Escape');assert menu.get_attribute('open') is None
            if slug!='home':assert page.locator('.back-map').get_attribute('href').startswith('/bhoc/#')
            checks.append({'width':width,'route':route,'visible':True,'noHorizontalOverflow':True,'backToMapHrefPresent':True})
        c.close()
    c=browser.new_context(viewport={'width':390,'height':900},java_script_enabled=False)
    c.route('**/*',lambda rt:rt.abort());page=c.new_page()
    for slug in ('home','rbc','history'):
        page.set_content(source(b['routes'][slug]),wait_until='domcontentloaded')
        assert page.locator('main').is_visible()
    c.close();browser.close()
assert not errors,errors
report={'method':'Chromium page.set_content with inline local CSS/JS. Navigation to URLs is blocked by this runtime; link destinations validated statically, not by live requests. External illustrations not fetched.','checks':checks,'browserErrors':errors,'additionalChecks':['14 topic cards','four direct science links','mobile contents and Escape','three no-JavaScript renders','dated source-linked blood-group note'],'productionChanged':False}
(OUT/'browser-checks.json').write_text(json.dumps(report,indent=2))
print('PASS: 28 desktop/mobile renders; mobile menu/Escape; three no-JS renders; blood-group note; no JavaScript errors or horizontal overflow. URLs checked separately by static audit.')
