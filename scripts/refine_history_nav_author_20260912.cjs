const fs=require('fs');

// 1) Put Historical Evolution of Understanding first in Explore BHOC.
const hub='bhoc/index.html';
let h=fs.readFileSync(hub,'utf8');
const oldNav='<nav class="bhoc-subnav" aria-label="BHOC page sections"><div class="bhoc-subnav-inner"><span class="subnav-title">Explore BHOC</span><a href="#bhoc-overview">Overview</a><a href="#why-bhoc">Why BHOC</a><a href="#terminology">Terminology</a><a href="#hemoglobin-system">Hemoglobin System</a><a href="#molecular-core">Hemoglobin</a><a href="#erythrocyte-system">RBC</a><a href="#circulation-control">Circulation</a><a href="#tissue-control">Tissue</a><a href="#species-adaptation">Species</a><a href="#human-variation">Human Variation</a><a href="#evidence-map">Evidence</a><a href="#history">Historical Evolution</a></div></nav>';
const newNav='<nav class="bhoc-subnav" aria-label="BHOC page sections"><div class="bhoc-subnav-inner"><span class="subnav-title">Explore BHOC</span><a href="#history">Historical Evolution of Understanding</a><a href="#bhoc-overview">Overview</a><a href="#why-bhoc">Why BHOC</a><a href="#terminology">Terminology</a><a href="#hemoglobin-system">Hemoglobin System</a><a href="#molecular-core">Hemoglobin</a><a href="#erythrocyte-system">RBC</a><a href="#circulation-control">Circulation</a><a href="#tissue-control">Tissue</a><a href="#species-adaptation">Species</a><a href="#human-variation">Human Variation</a><a href="#evidence-map">Evidence</a></div></nav>';
if(!h.includes(oldNav)) throw new Error('BHOC subnav block not found');
h=h.replace(oldNav,newNav);
fs.writeFileSync(hub,h);

// 2) Make author/date block modest and dates clearly visible.
const page='bhoc/history/index.html';
let s=fs.readFileSync(page,'utf8');
s=s.replace(
'.author-card{margin:22px 0 8px;border:1px solid #dce5ed;border-radius:16px;padding:20px;background:#fff}.author-card h2{margin:5px 0 7px}.author-card p{margin:6px 0;color:#4c5e6e;line-height:1.6}.record{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}.record time{padding:4px 8px;border-radius:999px;background:#eef3f7;color:#5f6d79;font:800 9px/1.3 Arial,sans-serif;text-transform:uppercase;letter-spacing:.05em}.record time:first-child{background:#e7f6f8;color:#0d718a}',
'.author-card{margin:18px 0 6px;border-top:1px solid #dce5ed;border-bottom:1px solid #e8edf1;padding:14px 0;background:transparent}.author-card .eyebrow{margin-bottom:3px;font-size:8px}.author-card h2{margin:2px 0 4px;font-size:16px;font-weight:800}.author-card p{margin:4px 0;color:#5b6b78;font-size:11px;line-height:1.5}.author-card .author-link{font-size:10.5px}.article-dates{margin-top:8px!important;color:#3f5262!important;font-size:10px!important}.article-dates strong{font-weight:800}.copyright-line{margin-top:7px!important;color:#7a8791!important;font-size:9px!important;letter-spacing:.01em}'
);
const oldAuthor=`<section class="author-card" aria-labelledby="author-title">
      <p class="eyebrow">Author</p><h2 id="author-title">Archil Jaliashvili</h2>
      <p>BHOC Therapeutics · Biological Hemoglobin Oxygen Carrier · Precision Oxygen Therapeutics</p>
      <p>This article is part of the BHOC public scientific knowledge architecture. It connects primary historical sources, modern transfusion evidence and the development of oxygen therapeutics without treating historical products as equivalent to BHOC.</p>
      <p><a href="https://www.linkedin.com/in/archil-jaliashvili-bhoc/" target="_blank" rel="noopener noreferrer">Archil Jaliashvili on LinkedIn ↗</a></p>
      <div class="record"><time datetime="2026-09-12">Added 12 Sep 2026</time><time datetime="2026-09-12">Last updated 12 Sep 2026</time></div>`;
const newAuthor=`<section class="author-card" aria-labelledby="author-title">
      <p class="eyebrow">Author</p><h2 id="author-title">Archil Jaliashvili</h2>
      <p>BHOC Therapeutics · Biological Hemoglobin Oxygen Carrier · Precision Oxygen Therapeutics</p>
      <p>This article is part of the BHOC public scientific knowledge architecture. It connects primary historical sources, modern transfusion evidence and the development of oxygen therapeutics without treating historical products as equivalent to BHOC.</p>
      <p class="author-link"><a href="https://www.linkedin.com/in/archil-jaliashvili-bhoc/" target="_blank" rel="noopener noreferrer">Archil Jaliashvili on LinkedIn ↗</a></p>
      <p class="article-dates"><strong>Published:</strong> 12 Sep 2026 · <strong>Last updated:</strong> 12 Sep 2026</p>
      <p class="copyright-line">© 2026 Archil Jaliashvili / BHOC Therapeutics. All rights reserved.</p>`;
if(!s.includes(oldAuthor)) throw new Error('Author block not found');
s=s.replace(oldAuthor,newAuthor);
s=s.replaceAll('—','-').replaceAll('–','-');
fs.writeFileSync(page,s);
