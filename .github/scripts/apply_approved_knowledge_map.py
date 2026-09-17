"""Apply verified approved content with two markup-only compatibility fixes.

All immutable sources and decoded output bytes are SHA-256 verified. Metadata
attribute order and a zero-text legacy anchor position are normalized without
rewriting scientific text, metadata values or any destination URL.
"""
from pathlib import Path
import base64,hashlib,html,json,lzma,re,subprocess
ROOT=Path(__file__).resolve().parents[2]
EXPECTED='e5ddac3e50718bba2657ecebbcc95406c572870e4d9637991411602c3a0fc3ef'
BRANCH='preview/bhoc-knowledge-map-release-20260917'
def sha(data):return hashlib.sha256(data).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def safe_path(rel):
 p=(ROOT/rel).resolve()
 if not p.is_relative_to(ROOT) or rel.startswith('.'):raise ValueError('Unexpected output path: '+rel)
 return p
branch=git('branch','--show-current').decode().strip()
assert branch==BRANCH,('Refusing to apply outside preview',branch)
parts=sorted((ROOT/'.github/release-payload').glob('knowledge-map-*.b64'))
assert len(parts)==6,'All six transport parts required'
raw=lzma.decompress(base64.b64decode(''.join(p.read_text().strip() for p in parts),validate=True))
assert sha(raw)==EXPECTED,'Release manifest checksum mismatch; no files changed'
payload=json.loads(raw);base=payload['base']
assert base=='f6cb0101410c4196a2651952bfce946e1082558b'
refs=[]
for source in payload['sources']:
 data=git('show',base+':'+source['path']).decode('utf-8')
 if source.get('transform')=='html-text':
  data=re.sub(r'<(script|style)\b[^>]*>[\s\S]*?</\1>',' ',data,flags=re.I)
  data=' '.join(html.unescape(re.sub(r'<[^>]+>',' ',data)).split())
 assert sha(data.encode())==source['sha256'],('Immutable source mismatch',source['path'])
 refs.append(data)
planned=[]
for output in payload['outputs']:
 text=''.join(op if isinstance(op,str) else refs[op[0]][op[1]:op[1]+op[2]] for op in output['ops'])
 assert sha(text.encode())==output['sha256'],('Output checksum mismatch',output['path'])
 refs.append(text)
 if output['path'].endswith('.html'):
  text=text.replace('<meta content="summary_large_image" name="twitter:card"/>','<meta name="twitter:card" content="summary_large_image">')
 previous_markup_sha=sha(text.encode())
 if output['path']=='bhoc/index.html':
  alias='<span aria-hidden="true" class="legacy-anchor" id="what-bhoc"></span>'
  card='<a class="topic topic-link" href="/bhoc/definition/" id="bhoc-overview">'
  assert text.count(alias)==1 and text.count(card)==1
  text=text.replace(alias,'',1).replace(card,card+alias,1)
 data=text.encode('utf-8');final_sha=sha(data)
 record={**output,'final_sha256':final_sha}
 target=safe_path(output['path']);existing=sha(target.read_bytes()) if target.is_file() else None
 assert existing in (output['before_sha256'],output['sha256'],previous_markup_sha,final_sha),('Source changed; stop rather than overwrite',output['path'])
 planned.append((target,data,record))
for target,data,record in planned:
 target.parent.mkdir(parents=True,exist_ok=True)
 if not target.exists() or target.read_bytes()!=data:target.write_bytes(data)
 print('Approved release:',record['path'],record['final_sha256'])
out=ROOT/'knowledge-map-test-results';out.mkdir(exist_ok=True)
(out/'application-manifest.json').write_text(json.dumps({'base':base,'branch':branch,'releaseManifestSha256':EXPECTED,'deletions':[],'files':[{k:v for k,v in o.items() if k!='ops'} for _,_,o in planned]},indent=2)+'\n')
(out/'application-paths.txt').write_text('\n'.join(o['path'] for _,_,o in planned)+'\n')
print(f'Applied {len(planned)} verified files. No public branch or deployment changed by this script.')
