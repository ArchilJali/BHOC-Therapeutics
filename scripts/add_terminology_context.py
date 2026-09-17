"""Apply requested terminology context without changing other sections or routes."""
from pathlib import Path
from collections import Counter
import html, json, re, subprocess

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / 'bhoc/index.html'
BASE = ROOT / 'bhoc/content-baseline.json'
CHECK = ROOT / 'scripts/check_bhoc_content.mjs'
START = 'ce270a3bedf10b33150677f4087473eb7580523a'
MARKER = 'data-terminology-context="20260917"'

ADDITION = '''</p>
      <div class="terminology-context" data-terminology-context="20260917">
        <p><strong>A mindset shaped by its time.</strong> The blood-replacement approach reflected the clinical priorities, scientific knowledge and technological tools available during early development. As that knowledge evolved, advances in vascular biology, oxygen sensing, microcirculation and protein engineering provided a stronger foundation for reconsidering the question. Some of these discoveries are recognized by <a href="https://archiljali.github.io/BHOC-platform/science/nobel-foundations-oxygen-metabolism-physiology.html" target="_blank" rel="noopener noreferrer">Nobel Prizes</a>. For BHOC, the question is no longer whether one product can reproduce blood, but which oxygen-delivery function needs support and under which physiological conditions. These discoveries inform that question; they do not validate a particular product.</p>
        <p><strong>The marketing trap.</strong> &ldquo;Artificial blood&rdquo; was a powerful shortcut: simple, memorable and easy to communicate. In our view, that clarity came at a cost. It encouraged expectations of replacing the whole blood system rather than supporting a defined biological function. As regulatory evaluation developed alongside these technologies, the broad label also risked obscuring the product-specific questions: which formulation, which indication, which physiological endpoint and which evidence?</p>
        <p><strong>The class-effect problem.</strong> We challenge the assumption that results from different early HBOC products can be treated as a single, permanent verdict on every hemoglobin-based oxygen carrier. Our criticism concerns that generalization, not the need to examine the findings for each tested product. In our view, broad replacement expectations and class-wide interpretations damaged confidence in an entire field and helped turn limitations of particular products and trial settings into presumed limits of the whole approach.</p>
        <p><strong>Biopure illustrates why the distinction matters.</strong> Among the major historical HBOC programs covered in our archive, Biopure followed a distinct regulatory and real-world path. Oxyglobin obtained veterinary authorizations in the United States and Europe, while Hemopure reached human-use authorization in South Africa. Their product-specific approvals and use are documented in our <a href="/bhoc/historical-evolution/#hboc-era">historical and regulatory record</a>. They should not be collapsed into the same history as candidates that never reached those milestones.</p>
        <p><strong>Reassessment is already under way.</strong> In recent years, <a href="https://archiljali.github.io/BHOC-platform/human/BHOC-Human-search.html?q=Blood%20Component%20Requirements&amp;year=2022" target="_blank" rel="noopener noreferrer">further analyses</a> and <a href="/bhoc/historical-evolution/#hboc-era">comparative reviews</a> have provided a basis for revisiting earlier conclusions about HBOCs and how they are applied across different products. We believe this reassessment should distinguish molecular design, formulation, clinical context and physiological endpoints, rather than treat all hemoglobin-based oxygen carriers as a single, uniform class. Revisiting broad class-wide conclusions does not mean dismissing product-specific safety findings.</p>
      </div>
      <p>'''

FOLLOW = '''
    <div class="terminology-followups" aria-label="Related terminology and vascular-control work">
      <div class="terminology-pending" id="class-effect-review" role="note" aria-labelledby="class-effect-review-title">
        <strong id="class-effect-review-title">Historical Misinterpretation of the HBOC Class Effect</strong>
        <span>In development &middot; Critical review of the Natanson paper. Analysis not yet published.</span>
      </div>
      <a class="terminology-concept" href="https://archiljali.github.io/BHOC-platform/concepts-hypotheses/size-compartmentalization-vascular-control.html" target="_blank" rel="noopener noreferrer">
        <strong>Vasoconstriction: an architecture-and-control hypothesis</strong>
        <span>Archil Jaliashvili &middot; Research Concept / Hypothesis &nearr;</span>
      </a>
    </div>
'''

CSS = '''
  <style id="terminology-context-style">
    #terminology .terminology-context p{margin-top:20px;margin-bottom:20px}
    #terminology .terminology-context a{text-decoration:underline;text-underline-offset:3px}
    #terminology .terminology-followups{max-width:880px;display:grid;gap:12px;margin-top:24px}
    #terminology .terminology-pending,#terminology .terminology-concept{display:block;padding:16px 18px;border:1px solid #d7e4f4;border-radius:10px;font:400 14px/1.55 Arial,Helvetica,sans-serif}
    #terminology .terminology-followups strong{display:block;font-size:15px;line-height:1.45}
    #terminology .terminology-followups span{display:block;margin-top:5px;font-size:13px}
    #terminology .terminology-pending{background:#f2f5f8;color:#596b7a;border-style:dashed;cursor:default}
    #terminology .terminology-concept{background:#fff;color:#173765;text-decoration:none}
    #terminology .terminology-concept:hover strong{text-decoration:underline}
    #terminology .terminology-concept:focus-visible{outline:2px solid #d82d2a;outline-offset:3px}
  </style>
'''

def snap():
    return json.loads(subprocess.check_output(['node',str(CHECK),'--snapshot'],cwd=ROOT,text=True))

def links(text):
    return Counter(html.unescape(x) for x in re.findall(r'<a\b[^>]*\bhref="([^"]*)"',text))

source = HUB.read_text()
if MARKER in source:
    print('Terminology context is already applied; no changes.')
    raise SystemExit(0)
subprocess.run(['node',str(CHECK)],cwd=ROOT,check=True)
before = snap()
pattern = re.compile(r'<section\b[^>]*\bid="terminology"[^>]*>[\s\S]*?</section>')
m = pattern.search(source)
assert m, 'Approved terminology section missing'
old = m.group()
split = ' BHOC Therapeutics retains these expressions'
assert old.count(split) == 1, 'Unexpected source text; stop rather than overwrite'
new = old.replace(split, ADDITION + 'BHOC Therapeutics retains these expressions',1)
new = new.replace('\n</section>', FOLLOW + '\n</section>',1)
assert new != old and MARKER in new
assert not (links(old) - links(new)), 'Original terminology links lost'
updated = source[:m.start()] + new + source[m.end():]
assert 'id="terminology-context-style"' not in updated
updated = updated.replace('</head>',CSS + '</head>',1)
updated = updated.replace('"dateModified":"2026-09-15"','"dateModified":"2026-09-17"')
updated = updated.replace('First published 10 Sep 2026 · Updated 15 Sep 2026 · Version 26.09.15','First published 10 Sep 2026 · Updated 17 Sep 2026 · Version 26.09.17')
assert not (links(source) - links(updated)), 'Original page links lost'
HUB.write_text(updated)
after = snap()
for ident in before['sections']:
    if ident != 'terminology':
        assert before['sections'][ident] == after['sections'][ident], f'Other content changed: {ident}'
baseline = json.loads(BASE.read_text())
baseline['sections']['terminology'] = after['sections']['terminology']
baseline['approvedTerminologyContext'] = {
    'startingCommit': START,
    'scope': 'User-requested history, marketing framing and BHOC class-effect critique; Nobel, product-history and author-concept internal links; inactive future Natanson-review notice.',
    'boundaries': '2022 identifies the stored HBOC-201 paper, not an asserted start of the entire reassessment; no worldwide exclusive approval claim; no new Natanson analysis; other 11 section fingerprints unchanged.'
}
BASE.write_text(json.dumps(baseline,indent=2)+'\n')
subprocess.run(['node',str(CHECK)],cwd=ROOT,check=True)
print('Preserved: all original anchor destinations and 11 other protected text/link fingerprints; original introductory and positioning text.')
print('Added: 5 contextual paragraphs and internal source/concept links. Natanson review remains non-clickable; standalone draft stays unpublished.')

# Continue requiring original text verbatim while allowing the explicitly requested additions.
tests = ROOT / 'tests/test_bhoc_navigation.py'
original_test = tests.read_text()
old_assertion = "assert [p.get_text() for p in old.select('#terminology p:not(.eyebrow)')] == [p.get_text() for p in soup.select('#terminology p:not(.eyebrow)')]"
new_assertion = '''preserved_terminology = BeautifulSoup(str(soup.select_one('#terminology')), 'html.parser')
for added in preserved_terminology.select('.terminology-context, .terminology-followups'):
    added.decompose()
normalize_text = lambda text: ' '.join(text.split())
assert normalize_text(' '.join(p.get_text() for p in old.select('#terminology p:not(.eyebrow)'))) == normalize_text(' '.join(p.get_text() for p in preserved_terminology.select('p:not(.eyebrow)')))
assert len(soup.select('.terminology-context > p')) == 5
assert not soup.select('#class-effect-review a, #class-effect-review button, #class-effect-review [tabindex]')
assert 'In development' in soup.select_one('#class-effect-review').get_text()
assert soup.select_one('.terminology-concept')['href'].endswith('size-compartmentalization-vascular-control.html')'''
assert old_assertion in original_test, 'Unexpected preservation test; stop'
updated_test = original_test.replace(old_assertion,new_assertion)
shot = "        page.screenshot(path=str(shots / f'terminology-{width}.png'))"
assert shot in updated_test
updated_test = updated_test.replace(shot, shot + "\n        page.locator('#terminology').screenshot(path=str(shots / f'terminology-full-{width}.png'))")
tests.write_text(updated_test)
print('Browser regression retains original wording and checks requested context, inactive placeholder and exact hypothesis link.')
