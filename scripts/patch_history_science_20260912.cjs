const fs=require('fs');
const file='bhoc/history/index.html';
let s=fs.readFileSync(file,'utf8');

if(!s.includes('.program-table{')){
  s=s.replace('</style>',`.program-table{margin:18px 0;border:1px solid #dce5ed;border-radius:14px;overflow:hidden;background:#fff}.program-row{display:grid;grid-template-columns:1.1fr 1.1fr .75fr 2.3fr;gap:0;border-top:1px solid #e5ebf0}.program-row:first-child{border-top:0}.program-row>div{padding:13px 14px;font-size:12px;line-height:1.48;color:#4e6070}.program-row.head>div{background:#f4f7fa;color:#2c4459;font:800 10px/1.35 Arial,sans-serif;text-transform:uppercase;letter-spacing:.04em}.program-row strong{color:#17344d}.science-note{margin:18px 0;padding:20px 22px;border:1px solid #d7e5ed;border-radius:14px;background:#f8fbfd}.science-note h3{margin:0 0 8px;font-size:19px}.science-note p{margin:7px 0}.context-note{margin:16px 0;padding:15px 18px;border-left:4px solid #0b6c9c;background:#f2f8fc;border-radius:10px}.context-note p{margin:0!important;color:#3f5668!important}.mini-timeline{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:18px 0}.mini-timeline>div{border:1px solid #dde6ed;border-radius:12px;padding:14px;background:#fff}.mini-timeline strong{display:block;color:#f22c26;font:900 12px/1.3 Arial,sans-serif;margin-bottom:6px}.mini-timeline span{display:block;color:#506171;font-size:11px;line-height:1.45}@media(max-width:820px){.program-row{grid-template-columns:1fr}.program-row.head{display:none}.program-row>div{padding:7px 14px}.program-row>div:first-child{padding-top:14px}.program-row>div:last-child{padding-bottom:14px}.mini-timeline{grid-template-columns:1fr 1fr}}@media(max-width:520px){.mini-timeline{grid-template-columns:1fr}}\n</style>`);
}

const hbocSection=`    <section class="history-section" id="hboc-era">
      <p class="eyebrow">HBOC era</p><h2>Hemoglobin leaves the red cell — and manufacturing becomes part of the biology.</h2>
      <p>Hemoglobin-based oxygen carriers attempted to stabilize hemoglobin outside its natural red-cell environment while retaining oxygen transport. Multiple programs reached human studies and some reached Phase III. The field demonstrated that oxygen transport was possible, but it also showed that <strong>an HBOC is not defined by hemoglobin concentration alone</strong>. Source material, purification, molecular size distribution, oxygen affinity, oxidation rate, nitric-oxide reactivity, heme loss and residual contaminants can materially change biological behavior.</p>

      <div class="science-note">
        <h3>Purity, endotoxin and quality control became measurable design variables.</h3>
        <p>Early cell-free hemoglobin work made it difficult to separate toxicity caused by hemoglobin itself from toxicity caused by contaminants. By 1991, investigators explicitly defined a meaningful “pure hemoglobin” preparation as one free of bacterial endotoxin, red-cell membrane phospholipids and residual proteins or peptides.</p>
        <p>During early production of αα-cross-linked hemoglobin, investigators later reported lipopolysaccharide contamination ranging from approximately <strong>1 to &gt;100 ng/mL</strong> in multiple initial manufacturing samples. Quantitative endotoxin testing allowed contamination sources to be identified and process areas to be made endotoxin-free. Modern oxygen-carrier manufacturing therefore treats bioburden, sterility, endotoxin limits, residual proteins and process consistency as product-critical quality attributes.</p>
        <p><strong>This does not mean endotoxin explains the HBOC failures.</strong> Later clinical safety problems also involved NO scavenging, vasoconstriction, oxidation, methemoglobin, heme release, molecular size and indication-specific risk.</p>
        <p><a class="source-link" href="https://pubmed.ncbi.nlm.nih.gov/1867535/" target="_blank" rel="noopener noreferrer">Quality control of hemoglobin solutions, 1991</a><br><a class="source-link" href="https://pubmed.ncbi.nlm.nih.gov/8259598/" target="_blank" rel="noopener noreferrer">Quantitative endotoxin control in cell-free hemoglobin production</a></p>
      </div>

      <div class="callout"><p><strong>Not all HBOCs are the same.</strong> A 2025 comparative review from academic investigators and FDA-affiliated authors emphasized that clinically tested HBOCs differ substantially in biochemical and biophysical characteristics and that each product must be evaluated on its own formulation, manufacturing, pharmacology, indication and benefit–risk profile.</p></div>

      <h3 style="margin-top:30px">Major discontinued human clinical HBOC programs</h3>
      <p class="disclaimer">This table covers the major discontinued clinical-stage HBOC programs repeatedly documented in comparative reviews. Not every program ended because of a formal FDA rejection: some stopped because of mortality or cardiac safety signals, failed efficacy endpoints, inadequate clinical performance or financing. Hemopure/HBOC-201 is intentionally not listed as a “failed product” because it achieved regulatory approval outside the United States and later continued under successor ownership.</p>
      <div class="program-table" role="table" aria-label="Major discontinued human clinical HBOC programs">
        <div class="program-row head" role="row"><div>Product</div><div>Company</div><div>Stopped</div><div>Why development stopped / regulatory outcome</div></div>
        <div class="program-row" role="row"><div><strong>HemAssist / DCLHb</strong></div><div>Baxter Healthcare</div><div>1998–1999</div><div>Phase III trauma enrollment was terminated after excess mortality. Baxter abandoned development; the product was never approved.</div></div>
        <div class="program-row" role="row"><div><strong>Optro / rHb1.1</strong></div><div>Somatogen → Baxter</div><div>late 1990s</div><div>Recombinant cross-linked Hb development was stopped after hypertensive/vasoconstrictive and other adverse signals; later reviews also identify bacterial endotoxin concerns during development. No marketing approval.</div></div>
        <div class="program-row" role="row"><div><strong>PEG-Hb</strong></div><div>Enzon</div><div>1998</div><div>Phase I was completed and development was halted. This is a discontinued clinical program rather than a documented formal FDA denial.</div></div>
        <div class="program-row" role="row"><div><strong>HemoLink</strong></div><div>Hemosol</div><div>2003</div><div>Clinical development was halted after increased cardiac events emerged in combined analyses. Hemosol entered bankruptcy in 2005; HemoLink did not receive marketing approval.</div></div>
        <div class="program-row" role="row"><div><strong>PolyHeme</strong></div><div>Northfield Laboratories</div><div>2009</div><div>Phase III was completed in 2007. The FDA did not approve the BLA in May 2009 after the trial failed its primary efficacy objective and showed more adverse events. Northfield subsequently entered bankruptcy.</div></div>
        <div class="program-row" role="row"><div><strong>PHP / Hemoximer</strong></div><div>Apex Bioscience / Curacyte</div><div>2011</div><div>Phase III development was terminated after increased mortality and cardiovascular safety concerns. The product had also been explored as an NO scavenger/vasopressor rather than only as an oxygen carrier.</div></div>
        <div class="program-row" role="row"><div><strong>Hemospan / MP4OX</strong></div><div>Sangart</div><div>2015</div><div>Later-stage studies did not meet clinical expectations; development was shelved and Sangart ceased development operations after failing to secure additional funding.</div></div>
      </div>
      <p><a class="source-link" href="https://pmc.ncbi.nlm.nih.gov/articles/PMC11826291/" target="_blank" rel="noopener noreferrer">2025 comparative HBOC safety review</a> <a class="source-link" href="https://pmc.ncbi.nlm.nih.gov/articles/PMC7649120/" target="_blank" rel="noopener noreferrer">Clinical-program status review</a></p>

      <div class="science-note">
        <h3>Biopure is a different historical case.</h3>
        <p>Biopure filed for Chapter 11 protection in 2009 and sold substantially all operating assets to OPK Biotech. That corporate failure should not be described as the end of Hemopure/HBOC-201: the technology and assets later moved through successor ownership, and HBOC-201 continued in regulatory and expanded-access pathways. Oxyglobin had already achieved FDA veterinary approval, while Hemopure had achieved human approval outside the United States.</p>
        <p><a class="source-link" href="https://www.sec.gov/Archives/edgar/data/815508/000119312509180106/d8k.htm" target="_blank" rel="noopener noreferrer">Biopure 2009 SEC asset-sale filing</a></p>
      </div>

      <div class="timeline">
        <div class="event"><div class="year">1998</div><div><h3>Oxyglobin</h3><p>The FDA approved Oxyglobin (hemoglobin glutamer-200, bovine), sponsored by Biopure Corporation, on 12 January 1998 for veterinary use.</p><a class="source-link" href="https://animaldrugsatfda.fda.gov/adafda/app/search/public/document/downloadFoi/3700" target="_blank" rel="noopener noreferrer">FDA NADA 141-067 FOI Summary</a></div></div>
        <div class="event"><div class="year">2001</div><div><h3>Hemopure / HBOC-201</h3><p>South Africa’s Medicines Control Council approved Hemopure for acutely anemic adult surgical patients for the purpose of eliminating, reducing or delaying allogeneic red-cell transfusion. Biopure described the product as an oxygen therapeutic.</p><a class="source-link" href="https://media.corporate-ir.net/media_files/NSD/bpur/reports/ar01/05.htm" target="_blank" rel="noopener noreferrer">Biopure Annual Report 2001</a></div></div>
        <figure class="history-visual logo" id="visual-biopure">
          <img loading="lazy" decoding="async" src="https://www.sec.gov/Archives/edgar/data/815508/000119312508035329/g33104img001.jpg" alt="Historical Biopure Corporation logo, developer of Oxyglobin and Hemopure HBOC-201">
          <figcaption>Historical Biopure Corporation identity shown for documentary context. Image source: Biopure Corporation press release filed with the U.S. Securities and Exchange Commission, 21 Feb 2008. BIOPURE, Hemopure and Oxyglobin are third-party historical marks; no affiliation or endorsement is implied. <a href="https://www.sec.gov/Archives/edgar/data/815508/000119312508035329/dex991.htm" target="_blank" rel="noopener noreferrer">SEC source ↗</a></figcaption>
        </figure>
        <div class="event"><div class="year">2001–2004</div><div><h3>The language changes</h3><p>Scientific literature increasingly described these technologies as <strong>oxygen therapeutics</strong>. In 2004, FDA scientist Abdu Alayash explicitly called “blood substitute” and “artificial blood” misnomers because oxygen carriers do not perform all functions of blood.</p><a class="source-link" href="https://www.nature.com/articles/nrd1307" target="_blank" rel="noopener noreferrer">Nature Reviews Drug Discovery</a></div></div>
      </div>
      <div class="callout"><p><strong>The function-first idea did not begin with BHOC.</strong> The field itself began moving from “blood substitute” toward “oxygen therapeutics” more than two decades ago. BHOC represents a continuation and evolution of that unfinished idea.</p></div>
    </section>`;

s=s.replace(/    <section class="history-section" id="hboc-era">[\s\S]*?    <\/section>\n\n    <section class="history-section" id="oxygen-science">/, hbocSection+'\n\n    <section class="history-section" id="oxygen-science">');

const oxygenAndHemarina=`    <section class="history-section" id="oxygen-science">
      <p class="eyebrow">1998 → 2019</p><h2>Nitric oxide and cellular oxygen sensing change what “oxygen delivery” means.</h2>
      <div class="timeline">
        <div class="event"><div class="year">1998 Nobel</div><div><h3>Nitric oxide and vascular signaling</h3><p>Robert F. Furchgott, Louis J. Ignarro and Ferid Murad received the Nobel Prize for discoveries concerning nitric oxide as a signaling molecule in the cardiovascular system. This established NO as a central regulator of vascular tone and blood flow.</p><a class="source-link" href="https://www.nobelprize.org/prizes/medicine/1998/press-release/" target="_blank" rel="noopener noreferrer">Nobel Prize 1998</a><br><a class="source-link" href="https://archiljali.github.io/BHOC-platform/science/nitric-oxide-scavenging-hboc-vasoconstriction.html">BHOC evidence: NO scavenging &amp; vasoconstriction</a></div></div>
        <div class="event"><div class="year">2001</div><div><h3>Red cells emerge as active participants in flow regulation</h3><p>Pawloski, Hess and Stamler reported in <em>Nature</em> that deoxygenation of red cells can trigger export of hemoglobin-derived NO bioactivity, proposing a mechanism that couples hemoglobin oxygen saturation to vasodilatory signaling. This work helped shift the red blood cell from a purely passive oxygen container toward a model in which it can also participate in matching perfusion to metabolic oxygen demand.</p><p>Subsequent work supports the broader concept of <strong>RBC-mediated hypoxic vasodilation</strong>, but the exact molecular route remains debated. Proposed pathways include S-nitrosohemoglobin/S-nitrosothiol signaling, deoxyhemoglobin-mediated nitrite reduction and ATP release that stimulates endothelial NO production. It is therefore too strong to say that oxygen delivery absolutely “requires hemoglobin to bind NO” through one single pathway.</p><a class="source-link" href="https://www.nature.com/articles/35054560" target="_blank" rel="noopener noreferrer">Pawloski, Hess &amp; Stamler, Nature 2001</a></div></div>
        <div class="event"><div class="year">2019 Nobel</div><div><h3>Cells sense oxygen availability</h3><p>William G. Kaelin Jr., Sir Peter J. Ratcliffe and Gregg L. Semenza received the Nobel Prize for discoveries of how cells sense and adapt to oxygen availability. This is not validation of any specific oxygen carrier; it is fundamental evidence that oxygen availability is a regulated cellular variable, not simply a blood concentration measurement.</p><a class="source-link" href="https://www.nobelprize.org/prizes/medicine/2019/press-release/The/" target="_blank" rel="noopener noreferrer">Nobel Prize 2019</a><br><a class="source-link" href="https://archiljali.github.io/BHOC-platform/science/nobel-foundations-oxygen-metabolism-physiology.html">BHOC Nobel foundations: oxygen metabolism &amp; physiology</a></div></div>
      </div>
      <div class="callout"><p><strong>The red cell is not only an oxygen container.</strong> Modern physiology supports a feedback model in which falling oxygen saturation can help generate signals that increase local perfusion, coupling oxygen carriage with vascular regulation. The exact biochemical pathway is still under active scientific debate.</p></div>
      <div class="science-note">
        <h3>Where does the flow regulation occur?</h3>
        <p>Small arteries and arterioles are classically the primary resistance vessels controlling inflow into capillary beds. Signals generated downstream can be conducted upstream and alter arteriolar tone. Capillaries should not be described as completely passive, however: pericytes can locally alter capillary diameter and RBC distribution in several tissues.</p>
        <p>For the article, the scientifically safer conclusion is: <strong>system-level oxygen delivery depends on dynamic regulation of vascular resistance, predominantly upstream at the arteriolar level, with additional local control within the capillary network.</strong></p>
        <p><a class="source-link" href="https://pmc.ncbi.nlm.nih.gov/articles/PMC4435689/" target="_blank" rel="noopener noreferrer">Arterioles as primary resistance vessels</a><br><a class="source-link" href="https://pmc.ncbi.nlm.nih.gov/articles/PMC9796134/" target="_blank" rel="noopener noreferrer">Pericytes and capillary flow regulation</a></p>
      </div>
    </section>

    <section class="history-section" id="defined-function-oxygen-carriers">
      <p class="eyebrow">Defined-function oxygen-carrier applications</p><h2>HEMARINA: oxygen-carrier function moves into organ preservation.</h2>
      <p>HEMARINA belongs here as a separate oxygen-carrier development pathway, not inside the Nobel Prize timeline. Its importance to this historical narrative is that the technology was applied to a defined oxygenation problem rather than framed as replacement of the entire blood system.</p>
      <div class="timeline">
        <div class="event"><div class="year">2007</div><div><h3>HEMARINA founded</h3><p>HEMARINA was founded in France and developed M101, an extracellular hemoglobin derived from the marine worm <em>Arenicola marina</em>.</p><a class="source-link" href="https://www.hemarina.com/" target="_blank" rel="noopener noreferrer">HEMARINA</a></div></div>
        <div class="event"><div class="year">2020</div><div><h3>HEMO2life first-in-human kidney results</h3><p>The OXYOP multicenter study reported first-in-human use of M101 in kidney preservation. Fifty-eight donors were included; no immunological, allergic or prothrombotic effects were reported, and secondary endpoints showed encouraging renal-recovery signals.</p><a class="source-link" href="https://pubmed.ncbi.nlm.nih.gov/32012441/" target="_blank" rel="noopener noreferrer">First-in-human OXYOP study</a></div></div>
        <div class="event"><div class="year">2022</div><div><h3>HEMO2life CE marking</h3><p>HEMARINA announced CE marking for HEMO2life as a Class III medical device for use as an additive to organ-preservation solutions, allowing European market access for kidney-graft preservation.</p><a class="source-link" href="https://www.hemarina.com/wp-content/uploads/2022/09/Press-release-Hemarina-30092022-1.pdf" target="_blank" rel="noopener noreferrer">HEMARINA CE-mark press release</a><br><a class="source-link" href="https://archiljali.github.io/BHOC-platform/transplant/Transplant-index.html">BHOC Transplantation Evidence Hub</a></div></div>
        <aside class="history-brand-card" id="visual-hemarina" aria-label="HEMARINA and HEMO2life historical company identification">
          <div class="brand-name">HEMARINA</div>
          <div class="brand-sub"><strong>HEMO2life® / M101</strong><br>Marine extracellular hemoglobin developed for defined oxygen-support applications in organ preservation.</div>
          <div class="brand-source">Company identification is rendered typographically rather than copying HEMARINA website artwork. <a href="https://www.hemarina.com/" target="_blank" rel="noopener noreferrer">Official company source ↗</a> · <a href="https://www.hemarina.com/wp-content/uploads/2022/09/Hemo2life-Instructions-for-Use.pdf" target="_blank" rel="noopener noreferrer">HEMO2life instructions / CE 2022 ↗</a></div>
        </aside>
      </div>
    </section>`;

s=s.replace(/    <section class="history-section" id="oxygen-science">[\s\S]*?    <\/section>\n\n    <section class="history-section" id="system-pressure">/, oxygenAndHemarina+'\n\n    <section class="history-section" id="system-pressure">');

if(!s.includes('Adams and Lundy proposed the “10/30 rule”')){
  s=s.replace('      <p class="eyebrow">Modern transfusion medicine</p><h2>More blood earlier. Less donor blood when safely possible. Less reliance on one number.</h2>',`      <p class="eyebrow">Modern transfusion medicine</p><h2>More blood earlier. Less donor blood when safely possible. Less reliance on one number.</h2>
      <div class="mini-timeline" aria-label="Evolution of transfusion thresholds">
        <div><strong>1942</strong><span>Adams and Lundy proposed the “10/30 rule”: Hb around 10 g/dL or Hct around 30% became a widely used practical transfusion trigger.</span></div>
        <div><strong>1988</strong><span>NIH consensus challenged the idea that one universal laboratory threshold should determine transfusion.</span></div>
        <div><strong>1999</strong><span>The TRICC trial accelerated the move toward restrictive transfusion by comparing a 7 g/dL strategy with a 10 g/dL strategy in critically ill patients.</span></div>
        <div><strong>2023</strong><span>AABB guidance recommends considering transfusion below 7 g/dL for many hemodynamically stable adults, with 7.5–8 g/dL thresholds in selected contexts.</span></div>
      </div>
      <div class="context-note"><p><strong>Important distinction:</strong> these restrictive thresholds apply principally to hemodynamically stable patients. They should not be presented as the decision rule for uncontrolled hemorrhage or shock, where physiology, active bleeding, perfusion and clinical context can dominate before a laboratory hemoglobin value is available or informative.</p></div>`);
}

s=s.replace('~14 min read','~17 min read');

if(!s.includes('Feola M, Simoni J, Canizaro PC. Quality control of hemoglobin solutions')){
  s=s.replace('      </ol>\n    </section>',`        <li><a href="https://pubmed.ncbi.nlm.nih.gov/1867535/" target="_blank" rel="noopener noreferrer">Feola M, Simoni J, Canizaro PC. Quality control of hemoglobin solutions: purity before modification. Artificial Organs. 1991.</a></li>
        <li><a href="https://pubmed.ncbi.nlm.nih.gov/8259598/" target="_blank" rel="noopener noreferrer">Production of modified crosslinked cell-free hemoglobin for human use: quantitative determination of endotoxin contamination.</a></li>
        <li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC11826291/" target="_blank" rel="noopener noreferrer">Jahr JS et al. Hemoglobin-based oxygen carriers: biochemical, biophysical differences, and safety. Transfusion. 2025.</a></li>
        <li><a href="https://pubmed.ncbi.nlm.nih.gov/10573278/" target="_blank" rel="noopener noreferrer">Sloan EP et al. DCLHb in severe traumatic hemorrhagic shock. JAMA. 1999.</a></li>
        <li><a href="https://pubmed.ncbi.nlm.nih.gov/19228496/" target="_blank" rel="noopener noreferrer">PolyHeme USA multicenter Phase III trauma trial.</a></li>
        <li><a href="https://www.nature.com/articles/35054560" target="_blank" rel="noopener noreferrer">Pawloski JR, Hess DT, Stamler JS. Export by red blood cells of nitric oxide bioactivity. Nature. 2001.</a></li>
        <li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC6441278/" target="_blank" rel="noopener noreferrer">Nitric oxide, vasodilation and the red blood cell: mechanisms and continuing debate.</a></li>
        <li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC4435689/" target="_blank" rel="noopener noreferrer">The dynamic structure of arterioles: primary resistance vessels and tissue perfusion.</a></li>
        <li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC9796134/" target="_blank" rel="noopener noreferrer">The coronary capillary bed and pericyte regulation of capillary blood flow.</a></li>
      </ol>\n    </section>`);
}

fs.writeFileSync(file,s);
