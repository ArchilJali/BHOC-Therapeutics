const fs=require('fs');
const file='bhoc/historical-evolution/index.html';
let s=fs.readFileSync(file,'utf8');
const img='https://bhoctherapeutics.com/assets/bhoc-historical-evolution-preview-20260912.png';

s=s.replace('<meta property="og:type" content="article">','<meta property="og:type" content="website">');
if(!s.includes('property="og:image:url"')){
  s=s.replace(`<meta property="og:image" content="${img}">`,`<meta property="og:image" content="${img}">\n  <meta property="og:image:url" content="${img}">`);
}
if(!s.includes('rel="image_src"')){
  s=s.replace('<meta name="theme-color" content="#ffffff">',`<link rel="image_src" href="${img}">\n  <meta itemprop="image" content="${img}">\n  <meta name="twitter:image:src" content="${img}">\n  <meta name="theme-color" content="#ffffff">`);
}
fs.writeFileSync(file,s);
console.log('Hardened Historical Evolution social preview metadata');
