#!/usr/bin/env python3
"""One-time, user-approved news addition. Existing source pages are not rewritten."""
from pathlib import Path
import hashlib
import html
import io
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path('.')
DATE = '2026-10-24'
BASE = 'https://bhoctherapeutics.com'
SLUG = 'harvard-business-school-biopure-case-1998'
ROUTE = '/news/' + SLUG + '/'
URL = BASE + ROUTE
HISTORY = '/evidence/library/historical-sources/harvard-business-school-biopure-1998/'
ASSET = '/assets/news/harvard-biopure-1998-editorial.jpg'
TITLE = "Harvard Business School's Biopure Case Joins the BHOC Archive"
DESCRIPTION = "A short introduction to John T. Gourville's 1998 Biopure case, the Oxyglobin and Hemopure launch question, and BHOC's historical source record."
ALT = "AI-generated editorial illustration of the 1998 Harvard Business School Biopure case, with Oxyglobin and Hemopure titles. Not an archival photograph or the original case cover."
CAPTION = 'AI-generated editorial illustration for BHOC, not an archival photograph or the original Harvard case cover. No Harvard affiliation or endorsement is implied.'
SOURCE_URL = 'https://d2jqrm6oza8nb6.cloudfront.net/datasets/f3f7b514-33d3-4527-8d8e-097e32cd79cf.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiY2M1M2M1MGI1ZjY1ZWE2ZiIsImJ1Y2tldCI6InJ1bndheS1kYXRhc2V0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTc5MjkyMTk5NX0.2vXVvT7cj2wFiOTFI5HF5ZOvDgvqjaxFu_UCUx2bwb0'
SOURCE_SHA256 = 'da9685fbf855dffa2b2975523fed4e119ce00b2a38d115fcdf2a8acb0062b0c4'

def read(path):
    return (ROOT / path).read_text(encoding='utf-8')

def write(path, text):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8')

def replace_once(text, old, new):
    assert text.count(old) == 1, 'Expected one insertion marker: ' + old[:90]
    return text.replace(old, new, 1)

def compact(data):
    return json.dumps(data, ensure_ascii=False, separators=(',', ':'))

def esc(text):
    return html.escape(text, quote=True)

source_note = read(HISTORY.lstrip('/') + 'index.html')
assert 'John T. Gourville' in source_note and '598150' in source_note
assert 'harvard-biopure-1998' in read('evidence/library/historical-sources/index.html')

# Copy the exact user-approved illustration to durable, first-party hosting.
with urllib.request.urlopen(SOURCE_URL, timeout=60) as response:
    raw = response.read(8_000_001)
assert len(raw) <= 8_000_000
assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, 'Unexpected illustration bytes'
image = Image.open(io.BytesIO(raw))
assert image.size == (1672, 940)
asset = ROOT / ASSET.lstrip('/')
asset.parent.mkdir(parents=True, exist_ok=True)
image.convert('RGB').save(asset, 'JPEG', quality=90, optimize=True, progressive=True)
print('Illustration saved:', asset, asset.stat().st_size, 'bytes')

# Reuse an existing news article's exact site shell, typography and width.
template = read('news/biopure-carl-rausch-david-judelson-2001-press-archive/index.html')
body_start = re.search(r'<body\b[^>]*>', template)
main_start = re.search(r'<main\b[^>]*>', template)
assert body_start and main_start and '</main>' in template
body_prefix = template[body_start.start():main_start.start()]
body_suffix = template[template.index('</main>') + len('</main>'):]
styles = '\n'.join(re.findall(r'<style\b[^>]*>.*?</style>', template, re.S))
style_links = '\n'.join(re.findall(r'<link\b[^>]*rel="stylesheet"[^>]*>', template))
scripts = '\n'.join(re.findall(r'<script\b[^>]*\bsrc="[^"]+"[^>]*>\s*</script>', template))
assert '.article-shell{max-width:1060px' in styles
identity_match = re.search(r'<script type="application/ld\+json" data-bhoc-identity>(.*?)</script>', template, re.S)
assert identity_match
identity = json.loads(identity_match.group(1))
for node in identity['@graph']:
    if node.get('@type') == 'WebPage':
        node.update({'@id': URL + '#webpage', 'url': URL, 'name': TITLE, 'datePublished': DATE, 'dateModified': DATE})

schema = {'@context':'https://schema.org','@graph':[
    {'@type':'NewsArticle','@id':URL+'#article','headline':TITLE,'description':DESCRIPTION,
     'datePublished':DATE+'T10:00:00+04:00','dateModified':DATE+'T10:00:00+04:00','inLanguage':'en',
     'articleSection':'Historical Sources','mainEntityOfPage':{'@id':URL+'#webpage'},
     'author':{'@id':BASE+'/#archil-jaliashvili'},'publisher':{'@id':BASE+'/#organization'},
     'image':[{'@type':'ImageObject','url':BASE+ASSET,'width':1672,'height':940,'caption':CAPTION}],
     'citation':[BASE+HISTORY],'isAccessibleForFree':True,
     'keywords':['Biopure','Harvard Business School','John T. Gourville','Oxyglobin','Hemopure','oxygen therapeutics history']},
    {'@type':'BreadcrumbList','itemListElement':[
        {'@type':'ListItem','position':1,'name':'BHOC Therapeutics','item':BASE+'/'},
        {'@type':'ListItem','position':2,'name':'News','item':BASE+'/news/'},
        {'@type':'ListItem','position':3,'name':'Harvard Business School Biopure case','item':URL}]}]}
head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Biopure's Harvard Business School Case | BHOC News</title>
<meta name="description" content="{esc(DESCRIPTION)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="yandex" content="noindex">
<meta name="author" content="Archil Jaliashvili">
<link rel="author" href="https://orcid.org/0009-0006-4712-4942">
<link rel="canonical" href="{URL}">
<meta property="og:site_name" content="BHOC Therapeutics">
<meta property="og:type" content="article">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(TITLE)}">
<meta property="og:description" content="{esc(DESCRIPTION)}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{BASE+ASSET}">
<meta property="og:image:secure_url" content="{BASE+ASSET}">
<meta property="og:image:width" content="1672">
<meta property="og:image:height" content="940">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:alt" content="{esc(ALT)}">
<meta property="article:published_time" content="{DATE}">
<meta property="article:modified_time" content="{DATE}">
<meta property="article:section" content="Historical Sources">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(TITLE)}">
<meta name="twitter:description" content="{esc(DESCRIPTION)}">
<meta name="twitter:image" content="{BASE+ASSET}">
<meta name="twitter:image:alt" content="{esc(ALT)}">
<script type="application/ld+json">{compact(schema)}</script>
<script type="application/ld+json" data-bhoc-identity>{compact(identity)}</script>
{style_links}
{styles}
{scripts}
</head>
'''
main = f'''<main class="article-shell" id="main">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">BHOC Therapeutics</a><span>›</span><a href="/news/">News</a><span>›</span><span aria-current="page">Biopure: the 1998 Harvard case</span></nav>
<div class="article-kicker">Historical sources · Biopure</div>
<h1>{esc(TITLE)}</h1>
<p class="deck">Oxyglobin, Hemopure and a product-launch decision that became a business teaching case in 1998.</p>
<div class="meta"><span>By <a href="/archil-jaliashvili/">Archil Jaliashvili</a></span><time datetime="{DATE}">24 October 2026</time><span>Historical case: 1998</span></div>
<figure class="article-image"><img src="{ASSET}" width="1672" height="940" alt="{esc(ALT)}" loading="eager" fetchpriority="high" decoding="async"><figcaption>{esc(CAPTION)}</figcaption></figure>
<div class="article-body">
<p>BHOC has added a source record for <cite>Biopure Corp.</cite>, John T. Gourville's Harvard Business School case published on 29 May 1998.</p>
<p>The case examines a practical decision: launch Oxyglobin for veterinary use, or wait while Hemopure was still being developed for human use? One concern was whether the veterinary product's price would shape expectations for the later human product.</p>
<p>This adds the commercial side of oxygen-carrier development to our historical archive: launch timing, pricing and decisions made before the outcome of human development was known.</p>
<p>Our <a href="{HISTORY}">historical source record</a> includes the case details, the official publisher link and related Biopure documents. It links the 1998 teaching case with the later company reports without treating them as the same type of evidence.</p>
<div class="status">Educational business history, not a clinical study or a Harvard endorsement of BHOC. The full copyrighted case is available through its publisher; it is not reproduced here.</div>
<div class="actions"><a class="primary" href="{HISTORY}">Read the historical source record →</a><a href="/evidence/library/historical-sources/">Historical Sources →</a><a href="/news/">Back to News →</a></div>
</div>
</main>'''
assert not (ROOT / ROUTE.lstrip('/') / 'index.html').exists(), 'News route already exists'
write(ROUTE.lstrip('/')+'index.html', head+body_prefix+main+body_suffix)

index_path = 'news/index.html'
index = read(index_path)
assert f'id="{SLUG}"' not in index
card = f'''\n<article class="news-card featured historical-archive-card" id="{SLUG}">
<div class="news-media news-photo" style="min-height:0;align-self:center;background:#f7fafc"><a href="{ROUTE}" aria-label="Read the Harvard Business School Biopure case news"><img src="{ASSET}" alt="{esc(ALT)}" width="1672" height="940" loading="eager" fetchpriority="high" decoding="async" style="width:100%;height:auto;min-height:0;max-height:none;object-fit:contain"></a></div>
<div class="news-copy"><div class="news-meta"><time datetime="{DATE}">24 October 2026</time><span>Historical sources · Biopure · Business history</span></div><h2><a href="{ROUTE}" style="color:inherit;text-decoration:none">{esc(TITLE)}</a></h2><p class="news-summary-text">Oxyglobin, Hemopure and a product-launch decision: a short introduction to John T. Gourville's 1998 teaching case and the new BHOC historical source record.</p><div class="news-actions"><a class="news-action primary" href="{ROUTE}">Read the news →</a><a class="news-action" href="{HISTORY}">Historical source record →</a></div><div class="news-note">Business history, not clinical evidence. AI-generated editorial illustration.</div></div></article>\n'''
index = replace_once(index, '<div class="news-feed">', '<div class="news-feed">'+card)
first_schema = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', index, re.S)
assert first_schema
feed_data = json.loads(first_schema.group(2))
feed_found = False
for node in feed_data.get('@graph', []):
    if node.get('@type') == 'CollectionPage' and node.get('url') == BASE+'/news/':
        node['dateModified'] = DATE
    if node.get('@type') == 'ItemList' and node.get('@id') == BASE+'/news/#news-feed':
        items = node['itemListElement']
        assert not any(item.get('url') == URL for item in items)
        items.insert(0, {'@type':'ListItem','url':URL,'name':TITLE,'position':1})
        for i, item in enumerate(items, 1):
            item['position'] = i
        node['numberOfItems'] = len(items)
        feed_found = True
assert feed_found
index = index[:first_schema.start(2)] + compact(feed_data) + index[first_schema.end(2):]
write(index_path, index)

updates_path = 'news/knowledge-updates/index.html'
updates = read(updates_path)
update_id = 'harvard-biopure-news-20261024'
assert update_id not in updates
entry = f'''\n<article class="timeline-item" id="{update_id}"><div class="timeline-date"><time datetime="{DATE}">24 Oct 2026</time><span>News · Historical sources</span></div><div class="timeline-copy"><h2>Biopure Harvard case: illustrated news added</h2><p>Published a short news introduction to the 1998 Harvard Business School Biopure case, with the approved editorial illustration and an internal link to the existing historical source record.</p><div class="timeline-links"><a href="{ROUTE}">Read the news →</a><a href="{HISTORY}">Historical source record →</a></div></div></article>\n'''
marker = '<section class="timeline" aria-label="October 2026 BHOC knowledge updates">'
updates = replace_once(updates, marker, marker+entry)
updates = re.sub(r'"dateModified":"[^"]+"', '"dateModified":"'+DATE+'"', updates, count=1)
write(updates_path, updates)

sitemap_path = 'sitemap.xml'
sitemap = read(sitemap_path)
assert URL not in sitemap and '</urlset>' in sitemap
for changed_url in [BASE+'/news/', BASE+'/news/knowledge-updates/']:
    pattern = r'(<url>\s*<loc>'+re.escape(changed_url)+r'</loc>\s*<lastmod>)[^<]*(</lastmod>)'
    sitemap, count = re.subn(pattern, lambda m:m.group(1)+DATE+m.group(2), sitemap)
    assert count == 1, 'Expected sitemap entry: '+changed_url
sitemap_entry = f'  <url><loc>{URL}</loc><lastmod>{DATE}</lastmod><image:image><image:loc>{BASE+ASSET}</image:loc><image:title>{esc(TITLE)}</image:title><image:caption>{esc(CAPTION)}</image:caption></image:image></url>\n'
sitemap = replace_once(sitemap, '</urlset>', sitemap_entry+'</urlset>')
ET.fromstring(sitemap)
write(sitemap_path, sitemap)

# Check local references and structured data for the new page.
new_page = read(ROUTE.lstrip('/')+'index.html')
for js in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', new_page, re.S):
    json.loads(js)
for target in re.findall(r'(?:href|src)="(/[^"?#]*)', new_page):
    p = ROOT / html.unescape(target).lstrip('/')
    assert p.exists() or (p/'index.html').exists(), 'Missing local reference: '+target
assert new_page.count('<h1>') == 1
assert read(HISTORY.lstrip('/')+'index.html') == source_note, 'Historical source changed unexpectedly'
print('Prepared news, image, News feed, Knowledge Updates and sitemap. Historical record preserved.')
