const fs=require('fs');
const path=require('path');
const root=process.cwd();
const src='bhoc/historical-evolution/index.html';
const dst='historical-evolution/index.html';
const old1='/bhoc/historical-evolution/';
const old2='/bhoc/history/';
const next='/historical-evolution/';
const oldAbs1='https://bhoctherapeutics.com/bhoc/historical-evolution/';
const oldAbs2='https://bhoctherapeutics.com/bhoc/history/';
const nextAbs='https://bhoctherapeutics.com/historical-evolution/';

if(!fs.existsSync(src)) throw new Error('Source article missing');
let article=fs.readFileSync(src,'utf8').replaceAll(oldAbs1,nextAbs).replaceAll(old1,next);
fs.mkdirSync(path.dirname(dst),{recursive:true});
fs.writeFileSync(dst,article);

function walk(dir){const out=[];for(const e of fs.readdirSync(dir,{withFileTypes:true})){if(e.name==='.git'||e.name==='node_modules') continue;const p=path.join(dir,e.name);if(e.isDirectory()) out.push(...walk(p)); else if(e.isFile()&&/\.(html|xml|json|md)$/i.test(e.name)) out.push(p);}return out;}
for(const file of walk(root)){
  if(file===src || file===dst || file.endsWith('scripts/migrate_history_to_root_20260912.cjs')) continue;
  let s=fs.readFileSync(file,'utf8');
  let n=s.replaceAll(oldAbs1,nextAbs).replaceAll(old1,next);
  if(n!==s) fs.writeFileSync(file,n);
}

const redirect=(target)=>`<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>Historical Evolution | BHOC Therapeutics</title>\n<meta name="robots" content="noindex,follow">\n<link rel="canonical" href="${nextAbs}">\n<meta http-equiv="refresh" content="0; url=${target}">\n<script>location.replace('${target}'+location.search+location.hash);<\/script>\n</head>\n<body><p>This page has moved to <a href="${target}">Historical Evolution</a>.</p></body>\n</html>\n`;
fs.writeFileSync(src,redirect(next));
fs.writeFileSync('bhoc/history/index.html',redirect(next));

const sitemap='sitemap.xml';
let sm=fs.readFileSync(sitemap,'utf8');
sm=sm.replaceAll(oldAbs1,nextAbs).replaceAll(oldAbs2,nextAbs);
sm=sm.replace(/(<url><loc>https:\/\/bhoctherapeutics\.com\/historical-evolution\/<\/loc>.*?<\/url>)(?:\s*\1)+/g,'$1');
fs.writeFileSync(sitemap,sm);

console.log('Migrated Historical Evolution to',nextAbs);
