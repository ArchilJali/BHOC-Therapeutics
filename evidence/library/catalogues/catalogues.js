'use strict';
(() => {
 const holder=document.getElementById('results');if(!holder)return;
 const rows=[...holder.querySelectorAll('.publication')],$=id=>document.getElementById(id);
 const normal=s=>String(s||'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
 const list=(row,key)=>(row.dataset[key]||'').split('|').filter(Boolean);
 const unique=values=>new Set(values.filter(Boolean).map(normal));
 const fields=['year','application','species','journal','product','direction','organ','evidence','catalogue','site','collection'].filter(id=>$(id));
 const labels={product:'Oxyglobin & Hemopure Evidence',oxygen:'Oxygen Diffusion & Microcirculation',related:'Related Scientific Articles'};
 for(const name of fields){
  const values=[...new Set(rows.flatMap(r=>list(r,name)))];values.sort(name==='year'?(a,b)=>Number(b)-Number(a):(a,b)=>a.localeCompare(b));
  for(const value of values){const option=document.createElement('option');option.value=value;option.textContent=(name==='catalogue'?labels[value]:value)+' ('+rows.filter(r=>list(r,name).includes(value)).length+')';$(name).append(option);}
  if(rows.some(r=>!list(r,name).length)&&!['catalogue','application'].includes(name)){const option=document.createElement('option');option.value='__other__';option.textContent='Not specified';$(name).append(option);}
 }
 for(const value of [...new Set(rows.flatMap(r=>list(r,'institution')))].sort()){const option=document.createElement('option');option.value=value;$('institutions').append(option);}
 for(const value of [...new Set(rows.flatMap(r=>String(r.dataset.author).split(/[,;]/).map(s=>s.trim()).filter(s=>s&&!/^et al\.?$/i.test(s))))].sort()){const option=document.createElement('option');option.value=value;$('authors').append(option);}
 const params=new URLSearchParams(location.search),controls=['q',...fields,'author','institution','sort'];
 if(params.has('group')&&!params.has('evidence'))params.set('evidence',params.get('group'));
 if(params.has('direction')&&!$('direction')&&$('application'))params.set('application',params.get('direction'));
 const speciesAliases={'Canine':'Canine (Dog)','Feline':'Feline (Cat)','Equine':'Equine (Horse)','Porcine':'Porcine (Pig)','Ovine':'Ovine (Sheep)','Avian':'Avian (Bird)','__exotic__':'Other animal','__other_models__':'In vitro / laboratory'};
 if(speciesAliases[params.get('species')])params.set('species',speciesAliases[params.get('species')]);
 const productParam=params.get('product')||'';if(/hemopure|201/i.test(productParam))params.set('product','Hemopure');else if(/oxyglobin|301|hb-200/i.test(productParam))params.set('product','Oxyglobin');
 for(const id of controls)if(params.has(id)){
  let value=params.get(id);const el=$(id);
  if(el.tagName==='SELECT'&&![...el.options].some(o=>o.value===value)){
   const match=[...el.options].find(o=>normal(o.value)===normal(value));
   if(match)value=match.value;else if(id!=='sort'){const option=document.createElement('option');option.value=value;option.textContent=value;el.append(option);}
  }
  el.value=value;
 }
 let legacyScope=params.get('scope')||'',page=1,matching=[],pageSize=24;
 const fragment=decodeURIComponent(location.hash.slice(1));
 const hashRow=rows.find(r=>r.id===fragment||list(r,'legacy').includes(fragment));
 if(hashRow)$('q').value=hashRow.dataset.title;
 if(controls.some(id=>$(id).closest('#advanced')&&$(id).value))$('advanced').open=true;
 function render(reset=true){
  if(reset)page=1;const terms=normal($('q').value).split(/\s+/).filter(Boolean);
  matching=rows.filter(r=>terms.every(t=>normal(r.dataset.search).includes(t))&&fields.every(id=>!$(id).value||($(id).value==='__other__'?!list(r,id).length:list(r,id).includes($(id).value)))&&(!$('author').value||normal(r.dataset.author).includes(normal($('author').value)))&&(!$('institution').value||($('institution').value==='__other__'?!list(r,'institution').length:normal(r.dataset.institution).includes(normal($('institution').value))))&&(!legacyScope||(legacyScope==='core'?r.dataset.scope==='core':r.dataset.scope!=='core')));
  matching.sort($('sort').value==='title'?(a,b)=>a.dataset.title.localeCompare(b.dataset.title):$('sort').value==='oldest'?(a,b)=>(Number(a.dataset.year)||9999)-(Number(b.dataset.year)||9999):(a,b)=>(Number(b.dataset.year)||0)-(Number(a.dataset.year)||0));
  const pages=Math.max(1,Math.ceil(matching.length/pageSize));page=Math.min(page,pages);
  rows.forEach(r=>r.hidden=true);matching.slice((page-1)*pageSize,page*pageSize).forEach(r=>{r.hidden=false;holder.append(r);});
  const start=matching.length?(page-1)*pageSize+1:0,end=Math.min(page*pageSize,matching.length);
  $('result-count').textContent=`${matching.length} of ${rows.length} publication records · Showing ${start}–${end}`;
  $('page-label').textContent=`Page ${page} of ${pages}`;$('previous').disabled=page===1;$('next').disabled=page===pages;$('empty').hidden=matching.length>0;
  const stats={records:matching.length,groups:unique(matching.flatMap(r=>list(r,document.body.dataset.group))).size,institutions:unique(matching.flatMap(r=>list(r,'institution'))).size,journals:unique(matching.map(r=>r.dataset.journal)).size};
  for(const [key,value] of Object.entries(stats))document.querySelector('[data-metric="'+key+'"]').textContent=value;
  const query=new URLSearchParams();for(const id of controls){const value=$(id).value;if(value&&!(id==='sort'&&value==='newest'))query.set(id,value);}if(legacyScope)query.set('scope',legacyScope);
  history.replaceState(null,'',location.pathname+(query.size?'?'+query:'')+location.hash);
 }
 for(const id of controls)$(id).addEventListener(['q','author','institution'].includes(id)?'input':'change',()=>render());
 $('reset').addEventListener('click',()=>{controls.forEach(id=>$(id).value=id==='sort'?'newest':'');legacyScope='';history.replaceState(null,'',location.pathname);render();});
 $('previous').addEventListener('click',()=>{page--;render(false);$('result-count').scrollIntoView({block:'start'});});
 $('next').addEventListener('click',()=>{page++;render(false);$('result-count').scrollIntoView({block:'start'});});
 $('export').addEventListener('click',()=>{const cell=s=>'"'+String(s||'').replace(/"/g,'""')+'"';const csv=['Title,Year,Catalogue,Application,Authors,Journal,Author institutions,Species or model,Source links',...matching.map(r=>[r.dataset.title,r.dataset.year,labels[r.dataset.catalogue],r.dataset.application,r.dataset.author,r.dataset.journal,r.dataset.institution,r.dataset.species,[...r.querySelectorAll('.source-links a:not(.permalink)')].map(a=>a.href).join(' | ')].map(cell).join(','))].join('\r\n');const url=URL.createObjectURL(new Blob(['\uFEFF'+csv],{type:'text/csv;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='BHOC-'+document.body.dataset.view+'-publications.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
 render();
 const anchors={institutionSearch:'institution',authorInput:'author',journalInput:'journal',scopeSelect:'catalogue'};
 const target=hashRow||$(anchors[fragment]||fragment);if(target){if(target.closest('#advanced'))$('advanced').open=true;target.scrollIntoView({block:'center'});}
})();
