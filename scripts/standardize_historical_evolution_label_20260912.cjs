const fs=require('fs');
const path=require('path');
const root=process.cwd();

function walk(dir){
  const out=[];
  for(const e of fs.readdirSync(dir,{withFileTypes:true})){
    if(e.name==='.git'||e.name==='node_modules') continue;
    const p=path.join(dir,e.name);
    if(e.isDirectory()) out.push(...walk(p));
    else if(e.isFile() && /\.(html|xml|json|md)$/i.test(e.name)) out.push(p);
  }
  return out;
}

for(const file of walk(root)){
  let s=fs.readFileSync(file,'utf8');
  let next=s.replaceAll('Historical Evolution of Understanding','Historical Evolution');
  if(next!==s) fs.writeFileSync(file,next);
}

const history='bhoc/history/index.html';
let h=fs.readFileSync(history,'utf8');
h=h.replace('<title>History of Blood Transfusion, HBOCs & Oxygen Therapeutics | BHOC</title>','<title>Historical Evolution | Blood Transfusion, HBOCs & Oxygen Therapeutics | BHOC</title>');
h=h.replace('<meta property="og:title" content="From Bloodletting to Oxygen Therapeutics">','<meta property="og:title" content="Historical Evolution | From Bloodletting to Oxygen Therapeutics">');
h=h.replace('<meta name="twitter:title" content="From Bloodletting to Oxygen Therapeutics">','<meta name="twitter:title" content="Historical Evolution | From Bloodletting to Oxygen Therapeutics">');
fs.writeFileSync(history,h);

const hub='bhoc/index.html';
let b=fs.readFileSync(hub,'utf8');
b=b.replace('aria-label="Open the full historical article From Bloodletting to Oxygen Therapeutics"','aria-label="Open Historical Evolution: From Bloodletting to Oxygen Therapeutics"');
fs.writeFileSync(hub,b);

const sitemap='sitemap.xml';
let sm=fs.readFileSync(sitemap,'utf8');
sm=sm.replace('<url><loc>https://bhoctherapeutics.com/bhoc/history/</loc><lastmod>2026-09-12</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>','<url><loc>https://bhoctherapeutics.com/bhoc/history/</loc><lastmod>2026-09-12</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>');
fs.writeFileSync(sitemap,sm);
