const fs=require('fs');
const path=require('path');
const root=process.cwd();
const oldPath='/bhoc/history/';
const newPath='/bhoc/historical-evolution/';
const oldAbs='https://bhoctherapeutics.com/bhoc/history/';
const newAbs='https://bhoctherapeutics.com/bhoc/historical-evolution/';

function walk(dir){
  const out=[];
  for(const e of fs.readdirSync(dir,{withFileTypes:true})){
    if(e.name==='.git'||e.name==='node_modules') continue;
    const p=path.join(dir,e.name);
    if(e.isDirectory()) out.push(...walk(p));
    else if(e.isFile() && /\.(html|xml|json|md|txt|js|cjs|css)$/i.test(e.name)) out.push(p);
  }
  return out;
}

const oldFile=path.join(root,'bhoc/history/index.html');
if(!fs.existsSync(oldFile)) throw new Error('Old history page not found');
let article=fs.readFileSync(oldFile,'utf8');
article=article.replaceAll(oldAbs,newAbs).replaceAll(oldPath,newPath);
article=article.replaceAll('Historical Evolution | From Bloodletting to Oxygen Therapeutics','Historical Evolution | From Bloodletting to Oxygen Therapeutics');
const newDir=path.join(root,'bhoc/historical-evolution');
fs.mkdirSync(newDir,{recursive:true});
fs.writeFileSync(path.join(newDir,'index.html'),article);

for(const file of walk(root)){
  if(file===oldFile || file.endsWith('scripts/migrate_history_to_historical_evolution_20260912.cjs')) continue;
  let s=fs.readFileSync(file,'utf8');
  let n=s.replaceAll(oldAbs,newAbs).replaceAll(oldPath,newPath);
  if(n!==s) fs.writeFileSync(file,n);
}

const redirect=`<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>Historical Evolution | BHOC Therapeutics</title>\n<meta name="robots" content="noindex,follow">\n<link rel="canonical" href="${newAbs}">\n<meta http-equiv="refresh" content="0; url=${newPath}">\n<script>location.replace('${newPath}'+location.search+location.hash);<\/script>\n</head>\n<body>\n<p>This page has moved to <a href="${newPath}">Historical Evolution</a>.</p>\n</body>\n</html>\n`;
fs.writeFileSync(oldFile,redirect);

const sitemap=path.join(root,'sitemap.xml');
let sm=fs.readFileSync(sitemap,'utf8');
if(!sm.includes(newAbs)) throw new Error('New Historical Evolution URL missing from sitemap after replacement');
fs.writeFileSync(sitemap,sm);

for(const file of walk(root)){
  if(file===oldFile || file.endsWith('scripts/migrate_history_to_historical_evolution_20260912.cjs')) continue;
  const s=fs.readFileSync(file,'utf8');
  if(s.includes(oldAbs)||s.includes(oldPath)) throw new Error('Old history URL remains in '+path.relative(root,file));
}
console.log('Historical Evolution migrated to',newPath,'with legacy redirect retained.');
