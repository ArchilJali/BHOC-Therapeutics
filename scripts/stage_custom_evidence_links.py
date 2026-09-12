from pathlib import Path

root=Path('.')
replacements={
  'https://archiljali.github.io/BHOC-platform/':'https://evidence.bhoctherapeutics.com/',
  'https://archiljali.github.io/BHOC-platform':'https://evidence.bhoctherapeutics.com',
  'https://archiljali.github.io/BHOC-VET-platform/':'https://evidence.bhocvet.com/',
  'https://archiljali.github.io/BHOC-VET-platform':'https://evidence.bhocvet.com',
}
exts={'.html','.css','.js','.json','.xml','.md','.txt'}
changed=[]
for p in root.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in exts or '.git' in p.parts or 'node_modules' in p.parts:
        continue
    try:
        s=p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    t=s
    for old,new in replacements.items():
        t=t.replace(old,new)
    if t!=s:
        p.write_text(t,encoding='utf-8')
        changed.append(str(p))
print('\n'.join(changed))
