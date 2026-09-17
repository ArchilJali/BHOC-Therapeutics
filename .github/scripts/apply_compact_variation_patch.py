from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[2]

def replace(path, old, new, count=1):
    p=ROOT/path; s=p.read_text()
    if old not in s: raise SystemExit(f'Expected text not found in {path}: {old[:90]}')
    p.write_text(s.replace(old,new,count))

# Overview: keep all approved routes/content, only tighten copy and add the future veterinary branch.
replace('bhoc/index.html','<span><strong>14</strong> topics</span>','<span><strong>15</strong> topics</span>')
old='''<article class="topic pending" id="human-variation"><div class="topic-meta"><span class="topic-code">09</span><span class="topic-status">In development</span></div><div class="topic-copy"><h3>Human Variation</h3><p>Hemoglobin variants and blood-group systems remain distinct.</p></div><div class="topic-end"><span>Detailed chapter not yet available</span><span aria-hidden="true" class="arrow">→</span></div><div class="paired-links"><a href="https://archiljali.github.io/BHOC-platform/human/BHOC-Human-index.html" rel="noopener noreferrer" target="_blank">Existing human evidence hub ↗</a></div></article>'''
new='''<article class="topic pending" id="human-variation"><div class="topic-meta"><span class="topic-code">09.1</span><span class="topic-status">In development</span></div><div class="topic-copy"><h3>Human Variation</h3><p>Hemoglobin variants, population genetics and blood-group systems remain distinct layers of human biology.</p></div><div class="topic-end"><span>Detailed chapter not yet available</span><span aria-hidden="true" class="arrow">→</span></div><div class="paired-links"><a href="https://archiljali.github.io/BHOC-platform/human/BHOC-Human-index.html" rel="noopener noreferrer" target="_blank">Existing human evidence hub ↗</a></div></article><a class="topic topic-link animal-variation" href="https://bhocvet.com/" id="animal-variation" target="_blank" rel="noopener noreferrer"><div class="topic-meta"><span class="topic-code">09.2</span><span class="topic-status">In development · BHOC Veterinary</span></div><div class="topic-copy"><h3>Animal Variation</h3><p>Species-specific hemoglobin biology, blood groups and oxygen-delivery adaptation will be developed within BHOC Veterinary.</p></div><div class="topic-end"><span>Open BHOC Veterinary ↗</span><span aria-hidden="true" class="arrow">→</span></div></a>'''
replace('bhoc/index.html',old,new)

# Approximately 15–20% tighter overview cards, with slightly larger titles.
css_repls={
'.content-group{margin:0 0 32px;scroll-margin-top:25px}':'.content-group{margin:0 0 26px;scroll-margin-top:25px}',
'.group-heading{display:flex;gap:13px;align-items:baseline;margin:0 0 16px}':'.group-heading{display:flex;gap:13px;align-items:baseline;margin:0 0 12px}',
'.topic{display:flex;flex-direction:column;min-height:164px;padding:19px 21px 16px;':'.topic{display:flex;flex-direction:column;min-height:136px;padding:15px 17px 13px;',
'.topic-meta{display:flex;align-items:center;gap:9px;margin-bottom:9px;':'.topic-meta{display:flex;align-items:center;gap:9px;margin-bottom:7px;',
'.topic h3{margin:0;color:var(--navy);font-size:18px;line-height:1.23;':'.topic h3{margin:0;color:var(--navy);font-size:20px;line-height:1.18;',
'.topic p{font-size:12px;line-height:1.55;margin:8px 0 13px;':'.topic p{font-size:11.5px;line-height:1.45;margin:6px 0 10px;',
'.row-topic{grid-column:1/-1;min-height:103px;':'.row-topic{grid-column:1/-1;min-height:88px;',
'gap:12px;padding-block:17px;background:#f9fbfd':'gap:12px;padding-block:14px;background:#f9fbfd',
'.row-topic h3{font-size:19px}':'.row-topic h3{font-size:20px}',
'.system-topic{grid-column:1/-1;padding:20px 22px;min-height:0}':'.system-topic{grid-column:1/-1;padding:16px 18px;min-height:0}',
'.system-topic h3{font-size:21px}':'.system-topic h3{font-size:22px}',
'.system-top p{margin:6px 0 17px}':'.system-top p{margin:5px 0 12px}',
'padding:13px 0;color:var(--navy);font-size:13px;min-height:77px':'padding:10px 0;color:var(--navy);font-size:13px;min-height:66px',
'.nobel-topic{grid-column:1/-1;min-height:100px}':'.nobel-topic{grid-column:1/-1;min-height:86px}',
'@media(min-width:1250px){.topic-grid .topic:not(.row-topic):not(.system-topic){min-height:156px}}':'@media(min-width:1250px){.topic-grid .topic:not(.row-topic):not(.system-topic){min-height:136px}}',
'.topic{padding:17px 18px;min-height:0}.topic h3{font-size:19px}.topic p{font-size:12px;margin:7px 0 12px}':'.topic{padding:15px 16px;min-height:0}.topic h3{font-size:20px}.topic p{font-size:11.5px;margin:6px 0 10px}'
}
for a,b in css_repls.items(): replace('bhoc/knowledge-map.css',a,b)
css=ROOT/'bhoc/knowledge-map.css'
s=css.read_text()
if '.animal-variation{' not in s:
    s += '\n/* Compact overview refinement + future animal-variation route. */\n.animal-variation{background:#f3f8f4;border-color:#d7e5da}.animal-variation .topic-code{color:#28724b}.animal-variation .topic-status{color:#557867}.animal-variation .topic-end{color:#28724b}.animal-variation:hover{background:#eef6f0;border-color:#b9d3c0}\n'
css.write_text(s)

# Keep the Animal Variation route visible inside chapter mobile navigation without duplicating 12 static files.
js=ROOT/'bhoc/knowledge-map.js'; s=js.read_text()
needle="const pagePath = value => new URL(value, currentURL).pathname.replace(/\\/index\\.html$/, '/');\n"
insert=needle+'''for (const nav of document.querySelectorAll('.mobile-map nav[aria-label="All BHOC topics"]')) {\n  if (!nav.querySelector('[data-animal-variation]')) {\n    const human = [...nav.children].find(el => /09\\s*·\\s*Human Variation|09\\.1\\s*·\\s*Human Variation/.test(el.textContent || ''));\n    if (human) {\n      if (/^09\\s*·/.test(human.textContent || '')) human.textContent = (human.textContent || '').replace(/^09\\s*·/, '09.1 ·');\n      const animal = document.createElement('a'); animal.href='https://bhocvet.com/'; animal.target='_blank'; animal.rel='noopener noreferrer'; animal.dataset.animalVariation='true'; animal.textContent='09.2 · Animal Variation · BHOC Veterinary ↗';\n      human.insertAdjacentElement('afterend', animal);\n    }\n  }\n}\n'''
if '[data-animal-variation]' not in s:
    if needle not in s: raise SystemExit('knowledge-map.js insertion point missing')
    js.write_text(s.replace(needle,insert,1))

# Update only the overview text fingerprint. Existing source-paragraph and URL protections remain unchanged.
bp=ROOT/'bhoc/knowledge-map-baseline.json'; b=json.loads(bp.read_text())
html=(ROOT/'bhoc/index.html').read_text()
# mirror scripts/check_knowledge_map.py main-text normalization
from html.parser import HTMLParser
class MainText(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.active=False; self.skip=0; self.parts=[]
    def handle_starttag(self,t,a):
        if t in ('script','style'): self.skip+=1
        if t=='main': self.active=True
    def handle_endtag(self,t):
        if t in ('script','style'): self.skip=max(0,self.skip-1)
        if t=='main': self.active=False
    def handle_data(self,d):
        if self.active and not self.skip:self.parts.append(d)
p=MainText();p.feed(html); norm=' '.join(' '.join(x.strip() for x in p.parts if x.strip()).split())
b['pages']['bhoc/index.html']['textSha256']=hashlib.sha256(norm.encode()).hexdigest()
bp.write_text(json.dumps(b,indent=2)+'\n')

for path in ['tests/test_knowledge_map.py','tests/test_knowledge_map_routes.py']:
    p=ROOT/path;s=p.read_text();s=s.replace("locator('.topic-code').count()==14","locator('.topic-code').count()==15")
    s=s.replace("'14 topic cards'","'15 topic cards'")
    p.write_text(s)
print('Applied compact-card + Human/Animal Variation patch; no canonical, title, description, sitemap or chapter source text changed.')
