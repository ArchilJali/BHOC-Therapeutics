const fs=require('fs');
const file='bhoc/history/index.html';
let s=fs.readFileSync(file,'utf8');

// Tighten vertical rhythm while keeping the long-form article readable.
s=s.replace('.history-section{scroll-margin-top:70px;padding:28px 0;', '.history-section{scroll-margin-top:70px;padding:22px 0;');
s=s.replace('.event{display:grid;grid-template-columns:132px minmax(0,1fr);gap:25px;padding:20px 0;', '.event{display:grid;grid-template-columns:132px minmax(0,1fr);gap:22px;padding:15px 0;');
s=s.replace('.callout{margin:22px 0;padding:25px 27px;', '.callout{margin:16px 0;padding:20px 22px;');
s=s.replace('.trend-grid,.stats-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:20px 0}', '.trend-grid,.stats-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:15px 0}');
s=s.replace('.author-card{margin:30px 0 10px;', '.author-card{margin:22px 0 8px;');
s=s.replace('.author-card{margin:22px 0 8px;border:1px solid #dce5ed;border-radius:16px;padding:24px', '.author-card{margin:22px 0 8px;border:1px solid #dce5ed;border-radius:16px;padding:20px');
s=s.replace('.history-visual{max-width:820px;margin:18px 0 22px;', '.history-visual{max-width:820px;margin:14px 0 18px;');
s=s.replace('.program-table{margin:18px 0;', '.program-table{margin:14px 0;');
s=s.replace('.science-note{margin:18px 0;padding:20px 22px;', '.science-note{margin:14px 0;padding:17px 19px;');
s=s.replace('.brief{margin:24px 0;border:1px solid #d9e7ef;border-radius:16px;background:#f8fcfd;padding:24px 26px}', '.brief{margin:18px 0;border:1px solid #d9e7ef;border-radius:16px;background:#f8fcfd;padding:20px 22px}');
s=s.replace('.history-nav{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0 28px}', '.history-nav{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0 20px}');

if(!s.includes('.regulatory-grid{')){
  s=s.replace('</style>', `.regulatory-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:16px 0}.regulatory-card{border:1px solid #dce5ed;border-radius:14px;padding:18px 19px;background:#fff}.regulatory-card h3{margin:3px 0 10px;font-size:20px}.regulatory-card ul{margin:8px 0 0;padding-left:18px}.regulatory-card li{margin:7px 0;color:#4d6070;font-size:12.5px;line-height:1.5}.internal-links{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.internal-links a{display:inline-block;padding:6px 9px;border:1px solid #d7e2eb;border-radius:999px;text-decoration:none;font:800 10px/1.2 Arial,sans-serif;color:#0b377f;background:#f9fbfd}.internal-links a:hover{border-color:#f22c26;color:#f22c26}.military-note{margin:14px 0;padding:17px 19px;border:1px solid #d8e5ed;border-radius:14px;background:#f7fbfd}.military-note h3{margin:0 0 8px;font-size:19px}.military-note p{margin:7px 0!important}@media(max-width:760px){.regulatory-grid{grid-template-columns:1fr}.regulatory-card{padding:16px}.internal-links{gap:6px}}\n</style>`);
}

s=s.replace('A source-linked historical perspective from bloodletting and early transfusion to blood groups, donor systems, artificial blood, HBOCs, Hemopure, Oxyglobin, HEMO2life and BHOC oxygen therapeutics.', 'A source-linked history of blood transfusion, Hemopure, Oxyglobin, HBOCs, FDA and EMA milestones, military trauma research and the evolution toward BHOC oxygen therapeutics.');

const marker='      <div class="callout"><p><strong>The function-first idea did not begin with BHOC.</strong>';
if(!s.includes(marker)) throw new Error('Insertion marker not found');

if(!s.includes('id="hemopure-oxyglobin-regulatory"')){
const block=`      <div class="science-note" id="hemopure-oxyglobin-regulatory">
        <p class="eyebrow">Regulatory and real-world milestones</p>
        <h3>Hemopure and Oxyglobin crossed different regulatory boundaries.</h3>
        <p>These records matter because they separate the history of a technology from the history of a single regulatory jurisdiction. Human Hemopure and veterinary Oxyglobin did not follow the same pathway.</p>
      </div>
      <div class="regulatory-grid">
        <article class="regulatory-card">
          <p class="eyebrow">Hemopure / HBOC-201</p>
          <h3>Human-use history</h3>
          <ul>
            <li><strong>South Africa, 2001:</strong> Hemopure received marketing authorization for acutely anemic adult surgical patients to eliminate, reduce or delay allogeneic red-cell transfusion.</li>
            <li><strong>South Africa, 2006:</strong> Biopure reported its first commercial Hemopure sales for human use. Fiscal-year revenue was reported as $37,000.</li>
            <li><strong>Russia, 2010 to 2015:</strong> Hemopure was registered as Гемопюр®, registration ЛП-000011. The historical registration expired in 2015.</li>
            <li><strong>United States:</strong> Hemopure is not FDA-approved for routine marketing. FDA Expanded Access has provided a pathway for qualifying patients with life-threatening anemia when standard transfusion is not available or suitable.</li>
            <li><strong>Europe:</strong> Hemopure has no EMA human marketing authorization. Published experience includes clinical studies and named-patient or compassionate-use treatment in Europe.</li>
          </ul>
          <div class="internal-links">
            <a href="https://archiljali.github.io/BHOC-platform/human/BHOC-Human-index.html">BHOC Human Use status ↗</a>
            <a href="https://archiljali.github.io/BHOC-platform/historical-sources/">BHOC Historical Sources ↗</a>
            <a href="https://archiljali.github.io/BHOC-platform/historical-sources/biopure-standing-on-the-shoulders-of-giants/">Biopure history ↗</a>
          </div>
        </article>
        <article class="regulatory-card">
          <p class="eyebrow">Oxyglobin</p>
          <h3>Veterinary approval and commercial use</h3>
          <ul>
            <li><strong>United States, 12 Jan 1998:</strong> FDA approved Oxyglobin, hemoglobin glutamer-200 (bovine), under NADA 141-067 for anemic dogs.</li>
            <li><strong>European Union, 29 Nov 1999:</strong> Oxyglobin received EU marketing authorization, EU/2/99/015. The EMA regulatory record remains available and was updated in October 2025.</li>
            <li><strong>Commercial experience:</strong> by 2002, Biopure reported more than 115,000 Oxyglobin units sold following U.S. and European authorization.</li>
          </ul>
          <div class="internal-links">
            <a href="https://archiljali.github.io/BHOC-platform/veterinary/Vet-fda-ema.html">Oxyglobin FDA and EMA records ↗</a>
            <a href="https://archiljali.github.io/BHOC-platform/veterinary/Vet-FDA-registry.html">FDA NADA 141-067 record ↗</a>
            <a href="https://archiljali.github.io/BHOC-platform/historical-sources/biopure-annual-report-2002/">Biopure 2002 source note ↗</a>
          </div>
        </article>
      </div>
      <div class="military-note">
        <p class="eyebrow">Military trauma research</p>
        <h3>U.S. Navy and Department of Defense support</h3>
        <p>In 2003, the U.S. Naval Medical Research Center signed a Cooperative Research and Development Agreement with Biopure for the proposed RESUS out-of-hospital trauma program. Biopure also reported Navy collaboration on preclinical next-generation HBOC work under the Hematomimetics Program. By 2008, company filings reported $22.5 million in U.S. congressional Department of Defense appropriations for Hemopure trauma development, including $16 million to the Navy and $6.5 million to the Army. This documents historical research support; it is not a current military endorsement or regulatory approval.</p>
        <div class="internal-links">
          <a href="https://archiljali.github.io/BHOC-platform/historical-sources/biopure-annual-report-2002/">BHOC source note: Biopure 2002 ↗</a>
          <a href="https://archiljali.github.io/BHOC-platform/social-media/linkedin/">BHOC LinkedIn archive: Navy collaboration ↗</a>
        </div>
      </div>
`;
s=s.replace(marker,block+marker);
}

if(!s.includes('Interference of bovine hemoglobin-based oxygen carrier-201')){
  const refMarker='        <li><a href="https://pubmed.ncbi.nlm.nih.gov/19228496/" target="_blank" rel="noopener noreferrer">PolyHeme USA multicenter Phase III trauma trial.</a></li>';
  const refs=`        <li><a href="https://onlinelibrary.wiley.com/doi/full/10.1111/ijlh.14146" target="_blank" rel="noopener noreferrer">Bronkhorst-van der Helm et al. Interference of bovine hemoglobin-based oxygen carrier-201 (Hemopure) on four hematology analyzers. 2023. Regulatory and compassionate-use context.</a></li>\n        <li><a href="https://www.ema.europa.eu/en/medicines/veterinary/EPAR/oxyglobin" target="_blank" rel="noopener noreferrer">European Medicines Agency. Oxyglobin, EU veterinary marketing-authorisation record.</a></li>\n        <li><a href="https://www.sec.gov/Archives/edgar/data/815508/000095013508000384/b68316bce10vk.htm" target="_blank" rel="noopener noreferrer">Biopure Corporation. SEC filing documenting Navy NMRC CRADA, Department of Defense appropriations and first Hemopure commercial sales. 2008 filing.</a></li>\n`;
  if(s.includes(refMarker)) s=s.replace(refMarker,refMarker+'\n'+refs);
}

s=s.replace('This historical perspective is part of the BHOC public scientific and strategic knowledge architecture. It is designed to connect primary historical sources, modern transfusion evidence and the evolution of oxygen-therapeutic thinking without presenting historical technologies as equivalent to BHOC.', 'This article is part of the BHOC public scientific knowledge architecture. It connects primary historical sources, modern transfusion evidence and the development of oxygen therapeutics without treating historical products as equivalent to BHOC.');
s=s.replace('← Understand BHOC', '← BHOC: What It Really Is & Why It Exists');

if(!s.includes('<meta name="author" content="Archil Jaliashvili">')) throw new Error('Author meta missing');
if(!s.includes('Archil Jaliashvili')) throw new Error('Visible/schema authorship missing');

s=s.replaceAll('—','-').replaceAll('–','-');
fs.writeFileSync(file,s);
