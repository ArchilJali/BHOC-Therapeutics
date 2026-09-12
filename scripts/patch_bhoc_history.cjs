const fs=require('fs');
const file='bhoc/index.html';
let html=fs.readFileSync(file,'utf8');
const old=`  <section class="content-section bhoc-anchor" id="history">
    <div class="section-copy"><p class="eyebrow">Historical and regulatory anchors</p><h2>Hemopure, HBOC-201, Oxyglobin and Biopure</h2><p><strong>Hemopure (HBOC-201)</strong> and <strong>Oxyglobin</strong> are central to the scientific, clinical, veterinary, regulatory and manufacturing history of polymerized bovine hemoglobin oxygen carriers developed by Biopure. These names remain important evidence-discovery terms and historical anchors for understanding what has already been demonstrated, what limitations were identified and what next-generation development must address.</p><p>References to Hemopure, HBOC-201, Oxyglobin, Biopure and other third-party technologies are provided for scientific and historical context and do not imply ownership, affiliation or approval of BHOC for their indications.</p></div>
  </section>`;
const next=`  <section class="content-section bhoc-anchor" id="history">
    <div class="section-copy"><p class="eyebrow">Historical Perspective</p><h2>From Bloodletting to Oxygen Therapeutics.</h2><p>For centuries, medicine removed blood to treat disease. Then it learned to replace blood to save life, identify compatibility, build donor systems and search for artificial blood and blood substitutes. The history of HBOCs, Hemopure, HBOC-201, Oxyglobin, Biopure, Perftoran and newer oxygen-carrier applications shows how the scientific question gradually moved from replacing blood as a whole toward understanding and supporting specific biological functions.</p><p>The full historical essay follows that evolution from the first transfusions and Landsteiner's blood-group discovery through blood banking, HIV-era safety, artificial oxygen carriers, HBOC lessons, donor-system constraints, modern EMS and the function-first BHOC framework.</p><p><a class="button" href="/bhoc/history/">Read: From Bloodletting to Oxygen Therapeutics →</a></p><p style="margin-top:10px;color:#6d7a86;font-size:11px"><strong>Added 12 Sep 2026</strong> · Source-linked historical essay</p><p style="margin-top:14px"><small>References to Hemopure, HBOC-201, Oxyglobin, Biopure and other third-party technologies are provided for scientific and historical context and do not imply ownership, affiliation or approval of BHOC for their indications.</small></p></div>
  </section>`;
if(html.includes(next)){console.log('BHOC history hub already patched');process.exit(0)}
if(!html.includes(old))throw new Error('Expected BHOC history block not found');
html=html.replace(old,next);
fs.writeFileSync(file,html);
console.log('Patched BHOC history hub');
