const fs=require('fs');
const path=require('path');
const root=process.cwd();
const canonical='/bhoc/historical-evolution/';
const canonicalAbs='https://bhoctherapeutics.com/bhoc/historical-evolution/';
const accidental='/historical-evolution/';
const accidentalAbs='https://bhoctherapeutics.com/historical-evolution/';
const articleSrc='historical-evolution/index.html';
const articleDst='bhoc/historical-evolution/index.html';

if(!fs.existsSync(articleSrc)) throw new Error('Accidental root article is missing');
let article=fs.readFileSync(articleSrc,'utf8');
article=article.replaceAll(accidentalAbs,canonicalAbs).replaceAll(accidental,canonical);
fs.mkdirSync(path.dirname(articleDst),{recursive:true});
fs.writeFileSync(articleDst,article);

function walk(dir){
  const out=[];
  for(const e of fs.readdirSync(dir,{withFileTypes:true})){
    if(e.name==='.git'||e.name==='node_modules'||e.name==='historical-evolution') continue;
    const p=path.join(dir,e.name);
    if(e.isDirectory()) out.push(...walk(p));
    else if(e.isFile() && /\.(html|xml|json|md|txt)$/i.test(e.name)) out.push(p);
  }
  return out;
}
for(const file of walk(root)){
  if(file===articleDst) continue;
  let s=fs.readFileSync(file,'utf8');
  let n=s.replaceAll(accidentalAbs,canonicalAbs).replaceAll(accidental,canonical);
  if(n!==s) fs.writeFileSync(file,n);
}

const old='bhoc/history/index.html';
const redirect=`<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>Historical Evolution | BHOC Therapeutics</title>\n<meta name="robots" content="noindex,follow">\n<link rel="canonical" href="${canonicalAbs}">\n<meta http-equiv="refresh" content="0; url=${canonical}">\n<script>location.replace('${canonical}'+location.search+location.hash);<\/script>\n</head>\n<body><p>This page has moved to <a href="${canonical}">Historical Evolution</a>.</p></body>\n</html>\n`;
fs.writeFileSync(old,redirect);

fs.rmSync('historical-evolution',{recursive:true,force:true});

const sm=fs.readFileSync('sitemap.xml','utf8');
if(!sm.includes(canonicalAbs)) throw new Error('Canonical Historical Evolution URL missing from sitemap');
if(sm.includes(accidentalAbs)) throw new Error('Accidental root Historical Evolution URL remains in sitemap');

for(const file of walk(root)){
  const s=fs.readFileSync(file,'utf8');
  if(s.includes(accidentalAbs)||s.includes('href="/historical-evolution/')||s.includes('content="/historical-evolution/')){
    throw new Error('Accidental root URL remains in '+path.relative(root,file));
  }
}
console.log('Restored single canonical Historical Evolution URL:',canonicalAbs);
