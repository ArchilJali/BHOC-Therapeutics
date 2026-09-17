"""Static and browser checks for the user-authorized navigation change."""
import json, os, subprocess, threading
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / 'bhoc/navigation.json').read_text())
ids = [item['id'] for item in config['sections']]
soup = BeautifulSoup((ROOT / 'bhoc/index.html').read_text(), 'html.parser')
assert [a['href'] for a in soup.select('.bhoc-subnav a')] == ['#' + x for x in ids]
assert all(soup.find(id=x) for x in ids)
assert len(ids) == len(set(ids))
assert soup.select_one('#terminology h2').get_text() == config['terminologyTitle']
assert not (ROOT / 'bhoc/artificial-blood-blood-substitute/index.html').exists()
assert '/bhoc/artificial-blood-blood-substitute/' not in (ROOT / 'sitemap.xml').read_text()
original = subprocess.check_output(['git', 'show', '89ddd34c464278a79528f5be3c1776b0fc9af256:bhoc/index.html'], cwd=ROOT, text=True)
old = BeautifulSoup(original, 'html.parser')
preserved_terminology = BeautifulSoup(str(soup.select_one('#terminology')), 'html.parser')
for added in preserved_terminology.select('.terminology-context, .terminology-followups'):
    added.decompose()
normalize_text = lambda text: ' '.join(text.split())
assert normalize_text(' '.join(p.get_text() for p in old.select('#terminology p:not(.eyebrow)'))) == normalize_text(' '.join(p.get_text() for p in preserved_terminology.select('p:not(.eyebrow)')))
assert len(soup.select('.terminology-context > p')) == 5
assert not soup.select('#class-effect-review a, #class-effect-review button, #class-effect-review [tabindex]')
assert 'In development' in soup.select_one('#class-effect-review').get_text()
assert soup.select_one('.terminology-concept')['href'].endswith('size-compartmentalization-vascular-control.html')
for item in ids:
    if item != 'terminology':
        assert str(old.find(id=item)) == str(soup.find(id=item)), item
print('PASS static: 12 valid routes; approved content unchanged; draft remains closed')

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}'
shots = ROOT / 'navigation-test-results'
shots.mkdir(exist_ok=True)
checks = []
with sync_playwright() as p:
    options = {'headless': True}
    if os.environ.get('BHOC_CHROMIUM'):
        options['executable_path'] = os.environ['BHOC_CHROMIUM']
    browser = p.chromium.launch(**options)
    for width in [1440, 375]:
        context = browser.new_context(viewport={'width': width, 'height': 900}, reduced_motion='reduce')
        context.route('**/*', lambda route: route.continue_() if route.request.url.startswith(base) else route.abort())
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        for item in ids:
            page.goto(base + '/bhoc/#' + item)
            page.wait_for_timeout(180)
            assert page.locator('.bhoc-subnav a[aria-current]').count() == 1, item
            assert page.locator('.bhoc-subnav a[aria-current]').get_attribute('href') == '#' + item, item
            target_top = page.locator('#' + item).bounding_box()['y']
            nav_bottom = page.locator('.bhoc-subnav').bounding_box()['y'] + page.locator('.bhoc-subnav').bounding_box()['height']
            assert target_top >= nav_bottom - 2, (item, target_top, nav_bottom)
            checks.append(f'{width}px: #{item}, correct active item and unobscured anchor')
        page.goto(base + '/bhoc/#terminology')
        page.wait_for_timeout(180)
        if width == 375:
            toggle = page.locator('.bhoc-contents-toggle')
            assert toggle.is_visible()
            assert toggle.get_attribute('aria-expanded') == 'false'
            toggle.click()
            assert toggle.get_attribute('aria-expanded') == 'true'
            assert page.locator('.bhoc-subnav-inner').is_visible()
            page.screenshot(path=str(shots / 'mobile-contents.png'))
            page.keyboard.press('Escape')
            assert toggle.get_attribute('aria-expanded') == 'false'
            toggle.click()
            page.locator('.bhoc-subnav a[href="#why-bhoc"]').click()
            page.wait_for_timeout(180)
            assert toggle.get_attribute('aria-expanded') == 'false'
            assert page.locator('.bhoc-subnav a[aria-current]').get_attribute('href') == '#why-bhoc'
            page.goto(base + '/bhoc/#terminology')
            page.wait_for_timeout(180)
        page.screenshot(path=str(shots / f'terminology-{width}.png'))
        page.locator('#terminology').screenshot(path=str(shots / f'terminology-full-{width}.png'))
        assert page.locator('.bhoc-subnav').evaluate('(e) => e.scrollWidth <= e.clientWidth + 1')
        page.goto(base + '/bhoc/historical-evolution/')
        page.wait_for_timeout(180)
        assert page.locator('.bhoc-subnav a[aria-current]').get_attribute('data-bhoc-path') == '/bhoc/historical-evolution/'
        target = 'https://bhoctherapeutics.com/science/?from=test#mechanism'
        page.evaluate('(url) => sessionStorage.setItem("bhocNavigationReturn", JSON.stringify({url,label:"Science",time:Date.now()}))', target)
        page.goto(base + '/bhoc/#terminology')
        page.wait_for_timeout(180)
        assert page.locator('[data-bhoc-return]').get_attribute('href') == target
        assert page.locator('.bhoc-context-actions button').inner_text() == '← Back'
        assert not errors, errors
        context.close()
    context = browser.new_context(viewport={'width': 375, 'height': 900}, java_script_enabled=False)
    context.route('**/*', lambda route: route.continue_() if route.request.url.startswith(base) else route.abort())
    page = context.new_page()
    page.goto(base + '/bhoc/#terminology')
    assert page.locator('.bhoc-subnav a[href="#terminology"]').is_visible()
    assert page.locator('#terminology h2').is_visible()
    assert not page.locator('.bhoc-contents-toggle').is_visible()
    context.close()
    browser.close()
server.shutdown()
print('PASS browsers: 24 deep links; desktop/mobile; mobile menu; Escape; history return; no-JavaScript fallback; no JavaScript errors')
(shots / 'checks.json').write_text(json.dumps({'checks':checks,'additional':['mobile menu','Escape','direct return URL','history page','no JavaScript fallback']}, indent=2))
