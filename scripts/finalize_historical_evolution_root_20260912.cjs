const fs=require('fs');
const path=require('path');
const ROOT=process.cwd();
const source='bhoc/historical-evolution/index.html';
const target='historical-evolution/index.html';
const newPath='/historical-evolution/';
const newAbs='https://bhoctherapeutics.com/historical-evolution/';
const oldPaths=['/bhoc/historical-evolution/','/bhoc/history/'];
const oldAbs=['https://bhoctherapeutics.com/bhoc/historical-evolution/','https://bhoctherapeutics.com/bhoc/history/'];

if(!fs.existsSync(source)) throw new Error('Source Historical Evolution article not found');
let article=fs.readFileSync(source,'utf8');
for(const u of oldAbs) article=article.replaceAll(u,newAbs);
for(const p of oldPaths) article=article.replaceAll(p,newPath);
fs.mkdirSync(path.dirname(target),{recursive:true});
fs.writeFileSync(target,article);

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

for(const file of walk(ROOT)){
  if(file===source || file==='bhoc/history/index.html') continue;
  let s=fs.readFileSync(file,'utf8');
  let n=s;
  for(const u of oldAbs) n=n.replaceAll(u,newAbs);
  for(const p of oldPaths) n=n.replaceAll(p,newPath);
  if(n!==s) fs.writeFileSync(file,n);
}

const redirect=`<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>Historical Evolution | BHOC Therapeutics</title>\n<meta name="robots" content="noindex,follow">\n<link rel="canonical" href="${newAbs}">\n<meta http-equiv="refresh" content="0; url=${newPath}">\n<script>location.replace('${newPath}'+location.search+location.hash);<\/script>\n</head>\n<body><p>This page has moved to <a href="${newPath}">Historical Evolution</a>.</p></body>\n</html>\n`;
fs.writeFileSync(source,redirect);
fs.writeFileSync('bhoc/history/index.html',redirect);

let sm=fs.readFileSync('sitemap.xml','utf8');
for(const u of oldAbs) sm=sm.replaceAll(u,newAbs);
const lines=sm.split('\n');
let seen=false;
sm=lines.filter(line=>{
  if(line.includes(`<loc>${newAbs}</loc>`)){
    if(seen) return false;
    seen=true;
  }
  return true;
}).join('\n');
fs.writeFileSync('sitemap.xml',sm);

const final=fs.readFileSync(target,'utf8');
if(!final.includes(`<link rel="canonical" href="${newAbs}">`)) throw new Error('Canonical not updated');
if(!final.includes(`<meta property="og:url" content="${newAbs}">`)) throw new Error('OG URL not updated');
if(!final.includes('property="og:image"')) throw new Error('OG image missing');
if(!sm.includes(`<loc>${newAbs}</loc>`)) throw new Error('Sitemap missing root Historical Evolution');
console.log('Final Historical Evolution canonical:',newAbs);
