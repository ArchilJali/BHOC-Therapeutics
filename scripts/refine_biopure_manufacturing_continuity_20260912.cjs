const fs=require('fs');
const file='bhoc/history/index.html';
let s=fs.readFileSync(file,'utf8');
const re=/<div class="science-note" id="biopure-company-outcome">[\s\S]*?<\/div>/;
const block=`<div class="science-note" id="biopure-company-outcome">
        <h3>Biopure is a different historical case: manufacturing continuity failed, not the existence of the underlying hemoglobin platform.</h3>
        <p>Unlike the discontinued candidates listed above, Biopure had already crossed major regulatory and commercial boundaries. Oxyglobin was authorized in the United States and Europe, Hemopure was authorized for human use in South Africa, and Biopure had built and validated an industrial manufacturing platform.</p>
        <p>The manufacturing record shows repeated operational disruption. Plant expansion and revalidation caused a six-month Cambridge shutdown and major Oxyglobin backorders in 2001-2002; FDA approved the expanded facilities in early 2003. After co-founder Carl W. Rausch moved from CEO to Vice Chairman and Chief Technology Officer in 2002, major workforce and cost reductions in 2003-2004 cut manufacturing capacity so sharply that Biopure reported it could no longer produce enough Oxyglobin to meet demand. The Cambridge site later received an MHRA GMP certificate in 2007. Manufacturing was then suspended again during the severe curtailment of operations that preceded the 2009 bankruptcy.</p>
        <p>The historical record therefore supports a distinction between product technology and company execution. Production capability, staffing, validation, QA/QC discipline and continuity of the manufacturing organization are part of a biologic product. When that system is lost, an authorized technology can disappear from practical use even if the molecule itself has not been invalidated. Available primary records document shutdown, revalidation and loss of operating continuity; they do not establish a formal FDA or MHRA revocation of Biopure's GMP certificate.</p>
      </div>`;
if(!re.test(s)) throw new Error('Biopure block not found');
s=s.replace(re,block);
fs.writeFileSync(file,s);
