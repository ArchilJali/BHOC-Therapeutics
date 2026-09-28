"""Check the shared site shell on representative published routes."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'navigation-test-results' / 'unified-shell'
OUT.mkdir(parents=True, exist_ok=True)
ROUTES = [
    ('/', None, 'home'),
    ('/bhoc/', 'BHOC', 'bhoc'),
    ('/bhoc/definition/', 'BHOC', 'definition'),
    ('/news/us-navy-biopure-hboc-201-2005-resus/', 'News', 'news'),
    ('/news/pandemic-preparedness-oxygen-delivery-resilience/', 'News', 'pandemic'),
    ('/evidence/library/', 'Evidence', 'library'),
    ('/evidence/library/human/health-system-resilience-oxygen-security.html', 'Evidence', 'oxygen-security'),
    ('/evidence/library/science/nitric-oxide-scavenging-hboc-vasoconstriction.html', 'Evidence', 'science'),
    ('/evidence/library/transplant/related/index.html', 'Evidence', 'transplant'),
    ('/evidence/library/veterinary/direct-studies/index.html', 'Evidence', 'veterinary'),
    ('/evidence/library/veterinary/business/BHOC-Veterinary-Concept.htm', 'Evidence', 'legacy'),
]


def check(page, base, route, expected_active, name, screen):
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(base + route, wait_until='domcontentloaded')
    page.locator('body.bhoc-shell-ready').wait_for()
    assert page.locator('.bhoc-shell-header').count() == 1, route
    assert page.locator('.bhoc-shell-footer').count() == 1, route
    assert page.locator('header.bhoc-shell-legacy:visible, footer.bhoc-shell-legacy:visible').count() == 0, route
    assert page.locator('.bhoc-shell-header').is_visible(), route
    assert page.locator('.bhoc-shell-footer').is_visible(), route
    active = page.locator('.bhoc-shell-nav a[aria-current]')
    if expected_active:
        assert active.count() == 1 and active.inner_text() == expected_active, (route, active.all_inner_texts())
        assert page.locator('nav[aria-label="Breadcrumb"]:visible').count() == 1, route
        assert page.locator('.bhoc-shell-trail [aria-current="page"]').count() == 1, route
    else:
        assert active.count() == 0 and page.locator('.bhoc-shell-trail').count() == 0, route
    assert not errors, (route, errors)
    bounds = page.evaluate('''() => {
      const header = document.querySelector('.bhoc-shell-header').getBoundingClientRect();
      const footer = document.querySelector('.bhoc-shell-footer').getBoundingClientRect();
      return {headerRight:header.right,footerRight:footer.right,width:innerWidth};
    }''')
    assert bounds['headerRight'] <= bounds['width'] + 2, (route, bounds)
    assert bounds['footerRight'] <= bounds['width'] + 2, (route, bounds)
    if screen and name in {'home', 'definition', 'news', 'library', 'oxygen-security', 'science'}:
        page.screenshot(path=str(OUT / f'{name}-{screen}.png'))
    return page.locator('.bhoc-shell-footer').inner_text()


server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
thread = Thread(target=server.serve_forever, daemon=True)
thread.start()
base = f'http://127.0.0.1:{server.server_port}'
try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        footer_text = None
        for route, expected, name in ROUTES:
            page = browser.new_page(viewport={'width': 1440, 'height': 900})
            current_footer = check(page, base, route, expected, name, 'desktop')
            assert footer_text is None or current_footer == footer_text, f'Different footer: {route}'
            footer_text = current_footer
            page.close()
        for route, expected, name in [ROUTES[0], ROUTES[2], ROUTES[5], ROUTES[6]]:
            page = browser.new_page(viewport={'width': 390, 'height': 844}, is_mobile=True)
            check(page, base, route, expected, name, 'mobile')
            button = page.locator('.bhoc-shell-menu-button')
            assert button.is_visible(), route
            button.click()
            assert button.get_attribute('aria-expanded') == 'true', route
            assert page.locator('.bhoc-shell-nav').is_visible(), route
            page.close()
        browser.close()
    print(f'PASS: {len(ROUTES)} desktop and 4 mobile pages have one shell, a usable current location and the same footer.')
finally:
    server.shutdown()
