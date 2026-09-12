const fs=require('fs');

const hist='bhoc/history/index.html';
let s=fs.readFileSync(hist,'utf8');

const replacements=[
  ['<p class="eyebrow">Historical Perspective</p>','<p class="eyebrow">Historical Evolution</p>'],
  [' · Historical Perspective</div>',' · Historical Evolution</div>'],
  ['"name":"Historical Perspective","item":"https://bhoctherapeutics.com/bhoc/history/"','"name":"Historical Evolution","item":"https://bhoctherapeutics.com/bhoc/history/"'],
  ['"alternativeHeadline":"A Historical Perspective on Blood, Transfusion, Artificial Blood, HBOCs and the Evolution Toward Function"','"alternativeHeadline":"The Evolution of Blood Transfusion, HBOCs and Oxygen Therapeutics"'],
  ['For centuries, medicine removed blood to treat disease. Then it learned to replace blood to save life. Then came blood groups, blood banking, donor systems, artificial blood and blood substitutes. Today the question is changing again: not only how to replace blood, but which biological function must be restored first.','Medicine spent centuries treating disease by removing blood. Transfusion reversed that logic. Blood groups, blood banking and donor systems followed, then artificial blood, blood substitutes and HBOCs. The modern question is narrower: which function is failing, and what has to be restored first?'],
  ['<p class="eyebrow">In Brief</p><h2 id="brief-title">The history is a sequence of changing questions.</h2>','<p class="eyebrow">In Brief</p><h2 id="brief-title">What changed over time.</h2>'],
  ['Medicine first learned that blood could be removed, then that it could be transfused, then that donor and recipient compatibility mattered, and finally how to collect, test, store and distribute blood at scale.','The key steps were practical: transfuse blood, understand compatibility, store it safely, test it and build donor systems that could work at scale.'],
  ['The twentieth century added another ambition: create artificial blood or blood substitutes that could reduce dependence on donor blood. Some technologies failed, some reached late-stage clinical development, and a small number reached regulatory or clinical use.','The twentieth century added a second problem: could oxygen transport be supported without depending entirely on donor red cells? That led to perfluorocarbon products, artificial-blood programs and HBOCs. Results were mixed.'],
  ['At the same time, transfusion medicine itself moved away from a universal “10/30” trigger toward more restrictive and individualized decisions, while emergency medicine increasingly relies on physiology and symptoms when laboratory values are unavailable or too slow.','Transfusion practice also changed. The old 10/30 rule gave way to more restrictive and individualized decisions. In emergency medicine, physiology and signs of shock may matter before a laboratory hemoglobin result is available.'],
  ['<p><strong>The trajectory leads to a different question: not only how to replace blood, but which function is failing and which function must be restored first.</strong></p>','<p><strong>The practical question is no longer only how to replace blood. It is also which function is failing and what needs to be restored first.</strong></p>'],
  ['<p class="eyebrow">1937 → 1985</p><h2>Blood becomes infrastructure, then biological risk becomes visible.</h2>','<p class="eyebrow">1937 to 1985</p><h2>Blood banking scales, and infectious risk becomes impossible to ignore.</h2>'],
  ['<p class="eyebrow">HBOC era</p><h2>Hemoglobin leaves the red cell — and manufacturing becomes part of the biology.</h2>','<p class="eyebrow">HBOC era</p><h2>When hemoglobin leaves the red cell, manufacturing becomes part of the biology.</h2>'],
  ['<p class="eyebrow">Modern transfusion medicine</p><h2>More blood earlier. Less donor blood when safely possible. Less reliance on one number.</h2>','<p class="eyebrow">Modern transfusion medicine</p><h2>Transfusion decisions became more selective and more dependent on clinical context.</h2>'],
  ['The direction is clear: move blood closer to the patient and earlier in the resuscitation timeline.','These programs move blood closer to the patient and earlier in resuscitation.'],
  ['<p class="eyebrow">1998 → 2019</p>','<p class="eyebrow">1998 to 2019</p>'],
  ['<p class="eyebrow">Ancient medicine → 1818</p>','<p class="eyebrow">Ancient medicine to 1818</p>']
];
for(const [a,b] of replacements){ if(s.includes(a)) s=s.replaceAll(a,b); }

// User preference: no long dashes in this article. Keep standard hyphens only.
s=s.replaceAll('—','-').replaceAll('–','-');
fs.writeFileSync(hist,s);

const hub='bhoc/index.html';
let h=fs.readFileSync(hub,'utf8');
h=h.replace('<a href="#history">History</a>','<a href="#history">Historical Evolution</a>');
h=h.replace('<div class="section-copy"><p class="eyebrow">Historical Perspective</p><h2>From Bloodletting to Oxygen Therapeutics.</h2>','<div class="section-copy"><p class="eyebrow">Historical Evolution</p><h2>Evolution of Blood Transfusion and Oxygen Therapeutics.</h2>');
h=h.replace('The full historical essay follows that evolution from the first transfusions and Landsteiner\'s blood-group discovery through blood banking, HIV-era safety, artificial oxygen carriers, HBOC lessons, donor-system constraints, modern EMS and the function-first BHOC framework.','The full article follows the main steps from early transfusion and Landsteiner\'s blood-group discovery to blood banking, HIV-era safety, artificial oxygen carriers, HBOC development, donor-system constraints, modern EMS and the BHOC function-first framework.');
h=h.replaceAll('—','-').replaceAll('–','-');
fs.writeFileSync(hub,h);
