const fs = require('fs');
const file = 'bhoc/history/index.html';
let s = fs.readFileSync(file, 'utf8');

if (!s.includes('.history-visual{')) {
  s = s.replace('</style>', `
    .history-visual{max-width:820px;margin:18px 0 22px;border:1px solid #dfe7ef;border-radius:14px;background:#fff;overflow:hidden}.history-visual img{display:block;width:100%;max-height:360px;object-fit:contain;background:#f7f9fb}.history-visual.photo img{object-fit:cover;max-height:420px}.history-visual.logo img{max-height:120px;padding:24px;box-sizing:border-box;background:#fff}.history-visual figcaption{padding:11px 13px;color:#687683;font-size:10px;line-height:1.55}.history-visual figcaption a{font-weight:800;text-decoration:none}.history-brand-card{max-width:820px;margin:18px 0 22px;border:1px solid #dfe7ef;border-radius:14px;background:linear-gradient(145deg,#ffffff,#f7faff);padding:24px 26px}.history-brand-card .brand-name{font:900 30px/1 Arial,Helvetica,sans-serif;letter-spacing:.07em;color:#142f46}.history-brand-card .brand-sub{margin-top:8px;color:#5e6e7b;font-size:12px;line-height:1.55}.history-brand-card .brand-source{margin-top:11px;font-size:10px;color:#6f7d89}.history-brand-card .brand-source a{font-weight:800;text-decoration:none}@media(max-width:760px){.history-visual{margin:16px 0}.history-visual.photo img{max-height:300px}.history-visual.logo img{max-height:100px;padding:18px}.history-brand-card{padding:20px}.history-brand-card .brand-name{font-size:24px}}
  </style>`);
}

if (!s.includes('id="visual-red-cross"')) {
  const rx = /(<div class="event"><div class="year">1940–1948<\/div><div><h3>Red Cross donor systems scale<\/h3>[\s\S]*?<\/div><\/div>)/;
  const block = `
        <figure class="history-visual photo" id="visual-red-cross">
          <img loading="lazy" decoding="async" src="https://commons.wikimedia.org/wiki/Special:FilePath/Mr.%20Lund%20watching%20the%20testing%20of%20blood%20plasma%208d21195v.jpg" alt="Red Cross blood donor center in Washington DC in 1942, showing blood plasma testing">
          <figcaption>Washington, D.C., District Red Cross blood donor center, June 1942. Photograph by Marjory Collins for the U.S. Office of War Information. Library of Congress FSA/OWI collection; public domain and free to use and reuse. <a href="https://www.loc.gov/item/2017832543/" target="_blank" rel="noopener noreferrer">Source ↗</a></figcaption>
        </figure>`;
  s = s.replace(rx, `$1${block}`);
}

if (!s.includes('id="visual-biopure"')) {
  const rx = /(<div class="event"><div class="year">2001<\/div><div><h3>Hemopure \/ HBOC-201<\/h3>[\s\S]*?<\/div><\/div>)/;
  const block = `
        <figure class="history-visual logo" id="visual-biopure">
          <img loading="lazy" decoding="async" src="https://www.sec.gov/Archives/edgar/data/815508/000119312508035329/g33104img001.jpg" alt="Historical Biopure Corporation logo, developer of Oxyglobin and Hemopure HBOC-201">
          <figcaption>Historical Biopure Corporation identity shown for documentary context. Image source: Biopure Corporation press release filed with the U.S. Securities and Exchange Commission, 21 Feb 2008. BIOPURE, Hemopure and Oxyglobin are third-party historical marks; no affiliation or endorsement is implied. <a href="https://www.sec.gov/Archives/edgar/data/815508/000119312508035329/dex991.htm" target="_blank" rel="noopener noreferrer">SEC source ↗</a></figcaption>
        </figure>`;
  s = s.replace(rx, `$1${block}`);
}

if (!s.includes('id="visual-hemarina"')) {
  const rx = /(<div class="event"><div class="year">2022<\/div><div><h3>HEMO2life CE marking<\/h3>[\s\S]*?<\/div><\/div>)/;
  const block = `
        <aside class="history-brand-card" id="visual-hemarina" aria-label="HEMARINA and HEMO2life historical company identification">
          <div class="brand-name">HEMARINA</div>
          <div class="brand-sub"><strong>HEMO2life® / M101</strong><br>Marine extracellular hemoglobin developed for defined oxygen-support applications in organ preservation.</div>
          <div class="brand-source">Company identification is rendered typographically rather than copying HEMARINA website artwork. HEMARINA states that reproduction of website components requires permission. <a href="https://www.hemarina.com/" target="_blank" rel="noopener noreferrer">Official company source ↗</a> · <a href="https://www.hemarina.com/wp-content/uploads/2022/09/Hemo2life-Instructions-for-Use.pdf" target="_blank" rel="noopener noreferrer">HEMO2life instructions / CE 2022 ↗</a></div>
        </aside>`;
  s = s.replace(rx, `$1${block}`);
}

fs.writeFileSync(file, s);
