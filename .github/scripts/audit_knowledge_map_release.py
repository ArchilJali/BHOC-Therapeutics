"""Independent preservation audit against the immutable pre-migration Git source."""
from pathlib import Path
import subprocess,json,hashlib,collections
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2]
BASE='f6cb0101410c4196a2651952bfce946e1082558b'
OUT=ROOT/'knowledge-map-test-results';OUT.mkdir(exist_ok=True)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def soup(raw):return BeautifulSoup(raw,'html.parser')
def meta(s):
 return {'title':s.title.get_text() if s.title else '',
         'meta':sorted((x.get('name',''),x.get('property',''),x.get('content','')) for x in s.select('head meta')),
         'canonical':[x.get('href') for x in s.select('head link[rel=canonical]')]}
files=git('ls-tree','-r','--name-only',BASE).decode().splitlines()
missing=[f for f in files if not (ROOT/f).is_file()]
assert not missing,('Previously tracked files missing',missing)
known=json.loads((ROOT/'bhoc/knowledge-map-baseline.json').read_text())
newpages={rel:soup((ROOT/rel).read_text()) for rel in known['pages']}
oldcanon=[];unchanged=[];preserved=[]
for rel in files:
 if not rel.endswith('.html'):continue
 raw=git('show',BASE+':'+rel)
 before=soup(raw)
 if not before.select('head link[rel=canonical]'):continue
 if '/preview/' in '/'+rel or rel.startswith('preview-'):continue
 after=soup((ROOT/rel).read_bytes())
 assert meta(before)==meta(after),('Original metadata changed',rel)
 if rel not in ['bhoc/index.html','bhoc/historical-evolution/index.html']:
  assert (ROOT/rel).read_bytes()==raw,('Unrelated canonical page changed',rel)
  unchanged.append(rel)
 else:preserved.append(rel)
 oldcanon.append(rel)
# Every old historical anchor, table entry, list item and illustration survives.
history_old=soup(git('show',BASE+':bhoc/historical-evolution/index.html'))
history_new=newpages['bhoc/historical-evolution/index.html']
assert {e['id'] for e in history_old.select('[id]')}.issubset({e['id'] for e in history_new.select('[id]')}),'Historical fragment ID lost'
for tag in ['td','th','li','blockquote','figcaption']:
 norm=lambda s:' '.join(s.get_text(' ',strip=True).split())
 previous=collections.Counter(norm(x) for x in history_old.select('main '+tag))
 current=collections.Counter(norm(x) for x in history_new.select('main '+tag))
 assert not (previous-current),('Historical content lost',tag,previous-current)
images=lambda s:collections.Counter((i.get('src'),i.get('alt')) for i in s.select('main img'))
assert not(images(history_old)-images(history_new)),'Historical illustration lost'
# Breadcrumb structured data and actual visible return navigation for every full chapter.
for rel,s in newpages.items():
 assert len(s.select('h1'))==1,rel
 for block in s.select('script[type="application/ld+json"]'):json.loads(block.string or block.get_text())
 if rel!='bhoc/index.html':
  schema=' '.join(b.get_text() for b in s.select('script[type="application/ld+json"]'))
  assert 'BreadcrumbList' in schema,(rel,'missing breadcrumb schema')
  assert s.select_one('.crumbs') and s.select_one('.chapter-footer') and s.select_one('.back-map'),(rel,'missing return navigation')
 titles=[p.title.get_text() for p in newpages.values()]
 assert len(titles)==len(set(titles)),'Duplicate chapter titles'
report={'base':BASE,'oldTrackedFilesPreserved':len(files),'oldCanonicalPagesMetadataPreserved':oldcanon,'unrelatedCanonicalPagesByteIdentical':unchanged,'redesignedPagesMetadataPreserved':preserved,'historicalIllustrationsPreserved':sum(images(history_old).values()),'historicalTablesListsQuotesPreserved':True,'chapterBreadcrumbsAndReturnsPresent':True,'allJSONLDParsed':True,'duplicateChapterTitles':False,'newFullChapterPages':len(newpages)-2,'deletedFiles':[]}
(OUT/'preservation-and-seo.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS independent audit:',len(files),'old files retained;',len(oldcanon),'existing canonical metadata sets identical; all old historical anchors/illustrations/list/table content retained; complete chapter breadcrumbs and returns.')
