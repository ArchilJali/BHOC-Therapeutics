const fs=require('fs');
const file='bhoc/history/index.html';
let s=fs.readFileSync(file,'utf8');

// Replace two direct PubMed links in the narrative with one internal evidence route.
const directLinks=/<p><a class="source-link" href="https:\/\/pubmed\.ncbi\.nlm\.nih\.gov\/1867535\/"[\s\S]*?Quantitative endotoxin control in cell-free hemoglobin production<\/a><\/p>/;
const internalQuality=`<p><a class="source-link" href="https://archiljali.github.io/BHOC-platform/historical-sources/biopure-standing-on-the-shoulders-of-giants/#4-1-manufacturing-quality-is-part-of-the-product">Why manufacturing quality is part of the hemoglobin product</a></p>`;
if(directLinks.test(s)) s=s.replace(directLinks,internalQuality);

// Replace the earlier short Biopure note with a more accurate corporate/regulatory interpretation.
const biopureNote=/<div class="science-note">\s*<h3>Biopure is a different historical case\.<\/h3>[\s\S]*?<\/div>\s*(?=<div class="timeline">)/;
const newNote=`<div class="science-note" id="biopure-company-outcome">
        <h3>Biopure's corporate failure was not a simple technology verdict.</h3>
        <p>The public record shows several things happening at the same time. Co-founder Carl W. Rausch moved from CEO to Vice Chairman and Chief Technology Officer in 2002, with Thomas A. Moore becoming CEO. In 2003 the U.S. human program faced FDA clinical and regulatory setbacks. SEC later brought enforcement actions concerning disclosure of material FDA developments while the company was raising capital. Financing pressure continued and Biopure entered bankruptcy in 2009.</p>
        <p>That history should not be simplified in either direction. Oxyglobin had U.S. and European veterinary authorization, Hemopure had South African human authorization, Biopure had built an industrial manufacturing platform, and the operating assets were later acquired by OPK Biotech. At the same time, real product-specific clinical and regulatory issues remained in the U.S. human program.</p>
        <p>There is no primary-source basis for saying that FDA revoked a Biopure GMP license. SEC filings instead document FDA GMP inspections of Biopure manufacturing facilities and continued manufacturing activity. Our historical reading is therefore that governance, disclosure, regulatory strategy, clinical risk and capital constraints all materially shaped the company's outcome.</p>
        <p><a class="source-link" href="https://archiljali.github.io/BHOC-platform/historical-sources/biopure-standing-on-the-shoulders-of-giants/#6-1-what-failed-at-biopure-technology-governance-regulation-and-capital">Detailed Biopure history: technology, governance, regulation and capital</a></p>
      </div>
      `;
if(biopureNote.test(s)) s=s.replace(biopureNote,newNote);

// If the old note pattern is absent, place the compact interpretation before the Biopure/Oxyglobin regulatory timeline once.
if(!s.includes('id="biopure-company-outcome"')){
  const marker='<div class="timeline">\n        <div class="event"><div class="year">1998</div><div><h3>Oxyglobin</h3>';
  if(s.includes(marker)) s=s.replace(marker,newNote+marker);
}

// Keep primary documents in References & Source Notes, not as repeated body links.
if(!s.includes('SEC Litigation Release No. 19376')){
  const refMarker='<li><a href="https://www.sec.gov/Archives/edgar/data/815508/000119312509180106/d8k.htm"';
  const extra=`<li><a href="https://www.sec.gov/enforcement-litigation/litigation-releases/lr-19376" target="_blank" rel="noopener noreferrer">U.S. SEC. Biopure and executives charged over disclosure of FDA developments. Litigation Release No. 19376, 2005.</a></li>\n        <li><a href="https://www.sec.gov/enforcement-litigation/litigation-releases/lr-19825" target="_blank" rel="noopener noreferrer">U.S. SEC. Biopure corporate settlement and independent compliance review requirement. Litigation Release No. 19825, 2006.</a></li>\n        <li><a href="https://www.sec.gov/Archives/edgar/data/815508/000095013504000426/b49311bce10vk.htm" target="_blank" rel="noopener noreferrer">Biopure SEC filing: biologic manufacturing requirements, GMP inspections and 2002 executive roles.</a></li>\n        `;
  const idx=s.indexOf(refMarker);
  if(idx>=0) s=s.slice(0,idx)+extra+s.slice(idx);
}

s=s.replaceAll('—','-').replaceAll('–','-');
fs.writeFileSync(file,s);
