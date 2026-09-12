const fs=require('fs');
const src='assets/bhoc-social-preview-20260905-initiative-logo.png';
const dst='assets/bhoc-historical-evolution-preview-20260912.png';
const page='bhoc/historical-evolution/index.html';
if(!fs.existsSync(src)) throw new Error('Source preview image not found');
fs.copyFileSync(src,dst);
let s=fs.readFileSync(page,'utf8');
const old='https://bhoctherapeutics.com/assets/bhoc-social-preview-20260905-initiative-logo.png?v=20260912-history';
const next='https://bhoctherapeutics.com/assets/bhoc-historical-evolution-preview-20260912.png';
s=s.replaceAll(old,next);
if(!s.includes('property="og:image:secure_url"')){
  s=s.replace(`<meta property="og:image" content="${next}">`,`<meta property="og:image" content="${next}">\n  <meta property="og:image:secure_url" content="${next}">\n  <meta property="og:image:type" content="image/png">`);
}
fs.writeFileSync(page,s);
console.log('Created dedicated Historical Evolution preview asset and updated OG tags');
