import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const siteOrigin='https://bhoctherapeutics.com';
const sitemap=fs.readFileSync(path.join(root,'sitemap.xml'),'utf8');
const locations=[...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map(match=>match[1].replaceAll('&amp;','&'));
const canonicalFiles=new Map();

function read(relative){return fs.readFileSync(path.join(root,relative),'utf8')}
function count(source,pattern){return [...source.matchAll(pattern)].length}
function textLength(value){return value.replace(/&(?:amp|quot|apos|#39);/g,'&').replace(/<[^>]+>/g,'').trim().length}
function pathForUrl(value){
  const url=new URL(value,siteOrigin);
  assert.equal(url.origin,siteOrigin,`${value}: sitemap must use the canonical origin`);
  const pathname=decodeURIComponent(url.pathname).replace(/^\//,'');
  return pathname===''?'index.html':pathname.endsWith('/')?`${pathname}index.html`:pathname;
}
function targetForLocalUrl(value,currentFile){
  const url=new URL(value,`${siteOrigin}/${currentFile}`);
  if(url.origin!==siteOrigin)return null;
  let relative=decodeURIComponent(url.pathname).replace(/^\//,'');
  if(relative==='')relative='index.html';
  else if(relative.endsWith('/'))relative+='index.html';
  return {relative,hash:url.hash};
}

assert.equal(new Set(locations).size,locations.length,'sitemap contains duplicate URLs');
for(const location of locations){
  const relative=pathForUrl(location);
  const absolute=path.join(root,relative);
  assert.ok(fs.existsSync(absolute),`${location}: sitemap target missing at ${relative}`);
  const source=read(relative);
  assert.equal(count(source,/<title>/gi),1,`${relative}: title count`);
  assert.equal(count(source,/<meta\b(?=[^>]*name="description")[^>]*>/gi),1,`${relative}: description count`);
  assert.equal(count(source,/<link\b(?=[^>]*rel="canonical")[^>]*>/gi),1,`${relative}: canonical count`);
  assert.equal(count(source,/<h1\b/gi),1,`${relative}: H1 count`);
  const title=source.match(/<title>([\s\S]*?)<\/title>/i)?.[1]||'';
  const description=source.match(/<meta\b(?=[^>]*name="description")[^>]*content="([^"]*)"[^>]*>/i)?.[1]||'';
  const canonical=source.match(/<link\b(?=[^>]*rel="canonical")[^>]*href="([^"]*)"[^>]*>/i)?.[1]||'';
  assert.ok(textLength(title)>=35&&textLength(title)<=65,`${relative}: title length ${textLength(title)}`);
  assert.ok(textLength(description)>=110&&textLength(description)<=190,`${relative}: description length ${textLength(description)}`);
  assert.equal(canonical,location,`${relative}: canonical does not match sitemap URL`);
  assert.match(source,/<meta\b(?=[^>]*name="robots")[^>]*content="[^"]*index/i,`${relative}: index directive missing`);
  for(const required of ['og:title','og:description','og:url','og:image']){
    assert.ok(source.includes(`property="${required}"`),`${relative}: ${required} missing`);
  }
  assert.ok(source.includes('name="twitter:card" content="summary_large_image"'),`${relative}: large social card missing`);
  for(const block of source.matchAll(/<script type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/gi)){
    assert.doesNotThrow(()=>JSON.parse(block[1]),`${relative}: invalid JSON-LD`);
  }
  for(const image of source.matchAll(/<img\b[^>]*>/gi)){
    assert.match(image[0],/\bwidth="\d+"/i,`${relative}: image width missing`);
    assert.match(image[0],/\bheight="\d+"/i,`${relative}: image height missing`);
  }
  canonicalFiles.set(relative,{title,description,canonical});
}

const titles=new Set();
const descriptions=new Set();
for(const [relative,data] of canonicalFiles){
  assert.ok(!titles.has(data.title),`${relative}: duplicate title`);
  assert.ok(!descriptions.has(data.description),`${relative}: duplicate description`);
  titles.add(data.title);
  descriptions.add(data.description);
}

const redirects={
  'historical-evolution/index.html':'https://bhoctherapeutics.com/bhoc/historical-evolution/',
  'bhoc/history/index.html':'https://bhoctherapeutics.com/bhoc/historical-evolution/',
  'news/prehospital-blood-transfusion-need-2026.html':'https://archiljali.github.io/BHOC-platform/science/prehospital-blood-transfusion-oxygen-delivery.html',
  'news/aabb-patient-blood-management-standards-2026.html':'https://archiljali.github.io/BHOC-platform/science/aabb-rbc-transfusion-thresholds-oxygen-delivery.html',
  'news/hope-nmp-liver-transplantation-2026.html':'https://archiljali.github.io/BHOC-platform/transplant/HOPE-NMP-Liver-Transplantation-2026.html'
};
for(const [relative,target] of Object.entries(redirects)){
  const source=read(relative);
  assert.match(source,/<meta name="robots" content="noindex,follow">/i,`${relative}: migration page must be noindex`);
  assert.ok(source.includes(`<link rel="canonical" href="${target}">`),`${relative}: migration canonical`);
  assert.ok(source.includes('http-equiv="refresh"'),`${relative}: migration refresh`);
  assert.ok(source.includes(target.replace(siteOrigin,''))||source.includes(target),`${relative}: migration target`);
}

const htmlFiles=[];
function walk(directory){
  for(const entry of fs.readdirSync(directory,{withFileTypes:true})){
    if(entry.name.startsWith('.'))continue;
    const absolute=path.join(directory,entry.name);
    if(entry.isDirectory())walk(absolute);
    else if(entry.isFile()&&entry.name.endsWith('.html'))htmlFiles.push(path.relative(root,absolute));
  }
}
walk(root);

let checkedLinks=0;
for(const relative of htmlFiles){
  const source=read(relative);
  for(const match of source.matchAll(/\b(?:href|src)="([^"]+)"/gi)){
    const value=match[1];
    if(/^(?:mailto:|tel:|data:|javascript:)/i.test(value))continue;
    const target=targetForLocalUrl(value,relative);
    if(!target)continue;
    checkedLinks++;
    const absolute=path.join(root,target.relative);
    assert.ok(fs.existsSync(absolute),`${relative}: missing local target ${value}`);
    if(target.hash&&/\.html$/i.test(target.relative)){
      const id=decodeURIComponent(target.hash.slice(1));
      const targetSource=read(target.relative);
      const escaped=id.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
      assert.ok(new RegExp(`\\bid=["']${escaped}["']`).test(targetSource),`${relative}: missing anchor ${value}`);
    }
  }
}

const repositoryText=htmlFiles.map(read).join('\n');
assert.ok(!/hbo2therapeutics\.com/i.test(repositoryText),'forbidden corporate domain found');
assert.ok(!/\$XX|\$X\b|\bX% CAGR\b/.test(repositoryText),'public placeholder market values found');
assert.ok(!sitemap.includes('https://bhoctherapeutics.com/historical-evolution/'),'retired historical URL remains in sitemap');
assert.ok(sitemap.includes('https://bhoctherapeutics.com/bhoc/historical-evolution/'),'canonical historical URL missing from sitemap');
assert.ok(sitemap.includes('https://bhoctherapeutics.com/assets/news/zipline-rwanda-drone-delivery.jpg'),'local drone image missing from sitemap');

console.log(`Passed: ${locations.length} canonical pages, ${Object.keys(redirects).length} migration redirects, ${htmlFiles.length} HTML files and ${checkedLinks} local references.`);
