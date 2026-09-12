const fs=require('fs');
const file='bhoc/history/index.html';
let s=fs.readFileSync(file,'utf8');

s=s.replace(
  '<p class="eyebrow">Defined-function oxygen-carrier applications</p><h2>HEMARINA: oxygen-carrier function moves into organ preservation.</h2>\n      <p>HEMARINA belongs here as a separate oxygen-carrier development pathway, not inside the Nobel Prize timeline. Its importance to this historical narrative is that the technology was applied to a defined oxygenation problem rather than framed as replacement of the entire blood system.</p>',
  '<p class="eyebrow">New-generation biological hemoglobin carrier</p><h2>HEMARINA: nature shows that hemoglobin is not one uniform molecular architecture.</h2>\n      <p>HEMARINA belongs here as a new-generation biological hemoglobin-carrier pathway based on M101, the naturally extracellular hemoglobin of the marine worm <em>Arenicola marina</em>. Unlike the approximately 64 kDa tetrameric human hemoglobin molecule, M101 is a giant extracellular hemoglobin of about 3.6 MDa, organized as a hexagonal-bilayer macromolecular assembly approximately 15 × 25 nm in size and capable of binding up to 156 oxygen molecules when saturated. Its scientific importance is not that all hemoglobins behave the same, but the opposite: nature has evolved very different hemoglobin architectures for oxygen transport. Molecular size, quaternary structure, oxygen affinity, redox behavior and whether hemoglobin normally functions inside or outside a cell can differ profoundly. M101 therefore provides a strong biological example that hemoglobin-based oxygen carriers should be understood and evaluated as distinct molecular systems, not as one uniform class.</p>'
);

s=s.replace(
  '<div class="event"><div class="year">2007</div><div><h3>HEMARINA founded</h3><p>HEMARINA was founded in France and developed M101, an extracellular hemoglobin derived from the marine worm <em>Arenicola marina</em>.</p><a class="source-link" href="https://www.hemarina.com/" target="_blank" rel="noopener noreferrer">HEMARINA</a></div></div>',
  '<div class="event"><div class="year">2007</div><div><h3>HEMARINA founded</h3><p>HEMARINA was founded in France around M101, the naturally extracellular hemoglobin of <em>Arenicola marina</em>. Its unusually large native molecular assembly provides a fundamentally different biological architecture from vertebrate intracellular hemoglobin and became the basis for HEMARINA oxygen-carrier products.</p><a class="source-link" href="https://www.hemarina.com/" target="_blank" rel="noopener noreferrer">HEMARINA</a></div></div>'
);

// Remove the internal Manufacturing Quality link from the historical narrative.
s=s.replace(/\n\s*<p><a class="source-link" href="https:\/\/archiljali\.github\.io\/BHOC-platform\/historical-sources\/biopure-standing-on-the-shoulders-of-giants\/#4-1-manufacturing-quality-is-part-of-the-product">Why manufacturing quality is part of the hemoglobin product<\/a><\/p>/,'');

// Replace the long corporate/regulatory block with a concise management/manufacturing interpretation.
const biopure=/<div class="science-note" id="biopure-company-outcome">[\s\S]*?<\/div>/;
const replacement=`<div class="science-note" id="biopure-company-outcome">
        <h3>Biopure is a different historical case: the corporation failed, but the underlying hemoglobin technology did not disappear.</h3>
        <p>Oxyglobin had U.S. and European veterinary authorization, Hemopure had South African human authorization, and Biopure had demonstrated industrial-scale manufacturing. In 2002 co-founder Carl W. Rausch moved from CEO to Vice Chairman and Chief Technology Officer. The company then passed through plant expansion and revalidation, major cost and workforce reductions, and loss of manufacturing capacity. In 2004 Biopure reported that these reductions left it unable to manufacture enough Oxyglobin to meet demand.</p>
        <p>For this historical comparison, that distinction matters. Unlike programs in which the candidate itself disappeared after an unsuccessful clinical program, Biopure's later collapse was also a management, manufacturing-continuity and execution problem around an already authorized technology platform. This does not erase the product-specific clinical and regulatory problems in the U.S. human program, but the failure of the corporation should not be presented as identical to failure of the underlying hemoglobin technology.</p>
      </div>`;
if(biopure.test(s)) s=s.replace(biopure,replacement);

// Remove litigation-oriented SEC references added in the previous edit.
s=s.replace(/\s*<li><a href="https:\/\/www\.sec\.gov\/enforcement-litigation\/litigation-releases\/lr-19376"[\s\S]*?<\/li>/g,'');
s=s.replace(/\s*<li><a href="https:\/\/www\.sec\.gov\/enforcement-litigation\/litigation-releases\/lr-19825"[\s\S]*?<\/li>/g,'');

fs.writeFileSync(file,s);
