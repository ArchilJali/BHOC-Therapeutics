"""Read-only owner audit: public HTML, rendered layouts, and repository checks.
No publishing, forms, private accounts, search-engine scraping or clinical analysis.
"""
import argparse
import collections
import concurrent.futures
import datetime
import json
import shutil
import subprocess
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

BASE = 'https://bhoctherapeutics.com'
UA = 'BHOC-Owner-SEO-UX-Audit/1.1'

def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        p = urllib.parse.urlsplit(newurl)
        if p.scheme != 'https' or p.hostname not in ('bhoctherapeutics.com', 'www.bhoctherapeutics.com') or p.username:
            raise urllib.error.HTTPError(req.full_url, code, 'Out-of-scope redirect', headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def get(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.build_opener(SafeRedirect()).open(req, timeout=25) as r:
            return r.status, r.read(4000000).decode('utf-8', 'replace'), r.url, r.headers.get('X-Robots-Tag', ''), r.headers.get('Content-Type', '')
    except urllib.error.HTTPError as e:
        return e.code, '', url, str(e), ''
    except Exception as e:
        return None, '', url, str(e), ''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='source')
    parser.add_argument('--out', default='output')
    args = parser.parse_args()
    source, out = Path(args.source), Path(args.out)
    for folder in ['screenshots', 'sources', 'live']:
        (out / folder).mkdir(parents=True, exist_ok=True)
    started = stamp()
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
    for name in ['AGENTS.md', 'README.md', 'seo/BHOC-SEO-Keywords.md', 'seo/page-keyword-map.md', 'homepage.css', 'unified-shell.css', 'unified-shell.js', 'assets/ga4.js']:
        src = source / name
        if src.is_file():
            dest = out / 'sources' / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dest)
    shutil.copyfile(__file__, out / 'sources' / 'audit-runner.py')
    rs, rt, _, _, _ = get(BASE + '/robots.txt')
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(rt.splitlines())
    (out / 'robots.txt').write_text(rt)
    maps, urls = {}, set()
    for route in ['/sitemap.xml', '/evidence/library/sitemap.xml']:
        code, text, _, err, _ = get(BASE + route)
        found = []
        if code == 200:
            root = ET.fromstring(text)
            # Only direct url/loc entries: image:loc is an image, not an HTML page.
            found = [e.text for e in root.findall('{*}url/{*}loc') if e.text and urllib.parse.urlsplit(e.text).hostname == 'bhoctherapeutics.com']
            urls.update(found)
        maps[route] = {'status': code, 'urls': found, 'error': err if code != 200 else None}
        (out / ('root-sitemap.xml' if route == '/sitemap.xml' else 'library-sitemap.xml')).write_text(text)
    if not urls:
        raise RuntimeError('No page URLs discovered; audit cannot be reported as successful.')
    page_ids = {}
    def audit(url):
        d = {'url': url, 'checked_at': stamp(), 'issues': []}
        if rs == 200 and not rp.can_fetch(UA, url):
            return dict(d, status=None, issues=['robots_disallow'])
        code, text, final, robots_header, content_type = get(url)
        d.update(status=code, final_url=final, content_type=content_type)
        if code != 200:
            return dict(d, issues=['fetch_or_http'], error=robots_header)
        if 'html' not in content_type.lower():
            return dict(d, issues=['non_html_in_page_sitemap'])
        soup = BeautifulSoup(text, 'html.parser')
        def meta(name):
            return [x.get('content', '') for x in soup.find_all('meta', attrs={'name': name})]
        title = soup.title.get_text(' ', strip=True) if soup.title else ''
        desc = meta('description')
        canon = [x.get('href', '') for x in soup.find_all('link', rel='canonical')]
        h1 = [x.get_text(' ', strip=True) for x in soup.find_all('h1')]
        robots = meta('robots') + meta('googlebot') + [robots_header]
        imgs = soup.find_all('img')
        blocks = soup.find_all('script', type='application/ld+json')
        invalid = 0
        for block in blocks:
            try:
                json.loads(block.get_text())
            except ValueError:
                invalid += 1
        page_ids[url] = {x['id'] for x in soup.find_all(id=True)} | {x['name'] for x in soup.find_all('a', attrs={'name': True})}
        links = [{'url': urllib.parse.urljoin(url, a['href']), 'text': a.get_text(' ', strip=True)} for a in soup.find_all('a', href=True) if urllib.parse.urlsplit(urllib.parse.urljoin(url, a['href'])).hostname == 'bhoctherapeutics.com']
        d.update(title=title, description=desc, canonical=canon, h1=h1, robots=robots, yandex=meta('yandex'), word_count=len((soup.find('main') or soup).get_text(' ', strip=True).split()), jsonld_blocks=len(blocks), invalid_jsonld=invalid, images=len(imgs), missing_alt=sum(not x.has_attr('alt') for x in imgs), empty_alt=sum(x.get('alt') == '' for x in imgs), missing_image_dimensions=sum(not(x.get('width') and x.get('height')) for x in imgs), internal_links=links)
        if not title: d['issues'].append('missing_title')
        if not any(desc): d['issues'].append('missing_description')
        if canon != [url]: d['issues'].append('canonical_review')
        if len(h1) != 1: d['issues'].append('h1_count')
        if 'noindex' in ' '.join(robots).lower(): d['issues'].append('noindex')
        if invalid: d['issues'].append('invalid_jsonld')
        return d
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        pages = list(pool.map(audit, sorted(urls)[:250]))
    duplicates = {}
    for field in ['title', 'description']:
        groups = collections.defaultdict(list)
        for page in pages:
            value = page.get(field, '')
            value = ' '.join(value) if isinstance(value, list) else value
            if value: groups[value.casefold()].append(page['url'])
        duplicates[field] = [x for x in groups.values() if len(x) > 1]
    anchors = []
    for page in pages:
        for link in page.get('internal_links', []):
            target, frag = urllib.parse.urldefrag(link['url'])
            frag = urllib.parse.unquote(frag)
            if frag and target in page_ids and frag not in page_ids[target]:
                anchors.append({'source': page['url'], 'target': link['url']})
    visual = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for mode, width, height in [('desktop', 1440, 1000), ('mobile', 390, 844)]:
            context = browser.new_context(viewport={'width': width, 'height': height}, device_scale_factor=1, is_mobile=(mode == 'mobile'), has_touch=(mode == 'mobile'), user_agent=UA)
            for route in ['/', '/bhoc/', '/science/', '/applications/', '/partners/', '/contact/', '/news/']:
                slug = route.strip('/').replace('/', '-') or 'home'
                page = context.new_page()
                try:
                    response = page.goto(BASE + route, wait_until='networkidle', timeout=45000)
                    page.wait_for_timeout(700)
                    data = page.evaluate('''() => {
                      const rect=e=>{if(!e)return null;const r=e.getBoundingClientRect();return {text:e.innerText?.trim().slice(0,180),top:Math.round(r.top),bottom:Math.round(r.bottom),height:Math.round(r.height),width:Math.round(r.width),fontSize:getComputedStyle(e).fontSize}};
                      const visible=e=>e.getBoundingClientRect().height>0&&getComputedStyle(e).visibility!=="hidden";
                      return {title:document.title,viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight,h1:rect(document.querySelector('h1')),header:rect([...document.querySelectorAll('header,[role="banner"]')].find(visible)),actions:[...document.querySelectorAll('main a')].filter(e=>visible(e)&&(e.matches('.home-button,.button,.btn')||/contact|partner|research|evidence|science/i.test(e.innerText))).slice(0,25).map(e=>({...rect(e),href:e.getAttribute('href')})),brokenImages:[...document.images].filter(i=>i.complete&&!i.naturalWidth).map(i=>i.getAttribute('src')),forms:[...document.forms].map(f=>({action:f.action,fieldCount:f.elements.length}))};
                    }''')
                    data.update(url=BASE+route, mode=mode, status=response.status if response else None, checked_at=stamp())
                    page.screenshot(path=str(out/'screenshots'/f'{slug}-{mode}-top.png'))
                    page.screenshot(path=str(out/'screenshots'/f'{slug}-{mode}-full.jpg'), full_page=True, type='jpeg', quality=65)
                    (out/'live'/f'{slug}-{mode}.txt').write_text(page.locator('body').inner_text())
                    if mode == 'desktop': (out/'live'/f'{slug}.html').write_text(page.content())
                    visual.append(data)
                except Exception as e:
                    visual.append({'url': BASE+route, 'mode': mode, 'error': str(e)})
                finally:
                    page.close()
            context.close()
        browser.close()
    checks = []
    for command in [['node','scripts/check_bhoc_content.mjs'],['node','scripts/check_site.mjs'],['node','--check','navigation-context.js'],['git','diff','--check']]:
        try:
            r = subprocess.run(command, cwd=source, capture_output=True, text=True, timeout=90)
            checks.append({'command':' '.join(command),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
        except Exception as e:
            checks.append({'command':' '.join(command),'error':str(e)})
    summary = {'audit_version':'1.1','checked_at':started,'source_main_sha':sha,'sitemaps':{k:{'status':v['status'],'count':len(v['urls'])} for k,v in maps.items()},'unique_urls_discovered':len(urls),'unique_urls_checked':len(pages),'http_counts':dict(collections.Counter(str(x.get('status')) for x in pages)),'issue_counts':dict(collections.Counter(i for x in pages for i in x['issues'])),'duplicate_title_groups':len(duplicates['title']),'duplicate_description_groups':len(duplicates['description']),'missing_alt_total':sum(x.get('missing_alt',0) for x in pages),'missing_image_dimensions_total':sum(x.get('missing_image_dimensions',0) for x in pages),'yandex_noindex_pages':sum('noindex' in ' '.join(x.get('yandex',[])).lower() for x in pages),'broken_internal_anchor_occurrences':len(anchors),'visual_tests':len(visual),'visual_errors':sum('error' in x for x in visual),'overflow':[{'url':x['url'],'mode':x['mode']} for x in visual if x.get('scrollWidth',0)>x.get('viewport',0)+1],'production_changes':0,'limitations':['Only direct sitemap url/loc entries count as pages; image:loc assets are excluded.','Read-only public HTML and rendered-layout audit; no search volume, Google indexing, rankings, conversion analytics or field Core Web Vitals measured.','No clinical efficacy review; no forms submitted.']}
    for name, data in [('summary.json',summary),('pages.json',pages),('visual.json',visual),('sitemaps.json',maps),('duplicates.json',duplicates),('anchors.json',anchors),('checks.json',checks)]:
        (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2))
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
