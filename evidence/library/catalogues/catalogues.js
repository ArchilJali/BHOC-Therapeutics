'use strict';
(() => {
 const holder=document.getElementById('results');if(!holder)return;
 const relocated=document.getElementById(decodeURIComponent(location.hash.slice(1)));
 if(relocated?.hasAttribute('data-record-redirect')){location.replace(relocated.querySelector('a').href);return;}
 const context=holder.closest('[data-view]')||document.body,prefix=context.dataset.queryPrefix||'';
 const rows=[...holder.querySelectorAll('.publication')],$=id=>document.getElementById(id);
 // Keep the five-collection aggregate only for the unfiltered overview.
 const collectionMetrics=[...context.querySelectorAll('[data-metric="collectionEntries"]')].map(metric=>{
  const label=metric.parentElement.querySelector('span');
  metric.setAttribute('aria-live','polite');
  return {metric,total:metric.textContent,label,labelText:label?.textContent||''};
 });
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
 const originalParams=new URLSearchParams(location.search),params=prefix?new URLSearchParams([...originalParams].filter(([key])=>key.startsWith(prefix)).map(([key,value])=>[key.slice(prefix.length),value])):originalParams,controls=['q',...fields,'author','institution','sort'];
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
 const requestedPage=Number(params.get('page'));
 let legacyScope=params.get('scope')||'',page=Number.isSafeInteger(requestedPage)&&requestedPage>0?requestedPage:1,matching=[],pageSize=24;
 const fragment=decodeURIComponent(location.hash.slice(1));
 const hashRow=rows.find(r=>r.id===fragment||list(r,'legacy').includes(fragment));
 if(hashRow){$('q').value=hashRow.dataset.title;page=1;}
 if(controls.some(id=>$(id).closest('#advanced')&&$(id).value&&!(context.dataset.view==='all'&&id==='catalogue')))$('advanced').open=true;
 function render(reset=true){
  if(reset)page=1;const terms=normal($('q').value).split(/\s+/).filter(Boolean);
  if(context.dataset.view==='all')document.querySelectorAll('[data-catalogue-filter]').forEach(link=>{if(link.dataset.catalogueFilter===$('catalogue').value)link.setAttribute('aria-current','page');else link.removeAttribute('aria-current');});
  if($('combined-applications'))$('combined-applications').hidden=$('catalogue').value!=='product';
  matching=rows.filter(r=>terms.every(t=>normal(r.dataset.search).includes(t))&&fields.every(id=>!$(id).value||($(id).value==='__other__'?!list(r,id).length:list(r,id).includes($(id).value)))&&(!$('author').value||normal(r.dataset.author).includes(normal($('author').value)))&&(!$('institution').value||($('institution').value==='__other__'?!list(r,'institution').length:normal(r.dataset.institution).includes(normal($('institution').value))))&&(!legacyScope||(legacyScope==='core'?r.dataset.scope==='core':r.dataset.scope!=='core')));
  const filtered=Boolean(terms.length||legacyScope||fields.some(id=>$(id).value)||normal($('author').value)||normal($('institution').value));
  matching.sort($('sort').value==='title'?(a,b)=>a.dataset.title.localeCompare(b.dataset.title):$('sort').value==='oldest'?(a,b)=>(Number(a.dataset.year)||9999)-(Number(b.dataset.year)||9999):(a,b)=>(Number(b.dataset.year)||0)-(Number(a.dataset.year)||0));
  const pages=Math.max(1,Math.ceil(matching.length/pageSize));page=Math.max(1,Math.min(page,pages));
  rows.forEach(r=>r.hidden=true);matching.slice((page-1)*pageSize,page*pageSize).forEach(r=>{r.hidden=false;holder.append(r);});
  const start=matching.length?(page-1)*pageSize+1:0,end=Math.min(page*pageSize,matching.length);
  $('result-count').textContent=(context.dataset.view==='all'?(filtered?`${matching.length} matching publications · `:''):`${matching.length} of ${rows.length} publication records · `)+`Showing ${start}–${end} · Page ${page} of ${pages}`;
  $('page-label').textContent=`Page ${page} of ${pages}`;$('previous').disabled=page===1;$('next').disabled=page===pages;$('empty').hidden=matching.length>0;
  $('page-numbers').replaceChildren();$('page-numbers').closest('nav').hidden=pages===1;
  const numbered=pages<=7?Array.from({length:pages},(_,i)=>i+1):page<=4?[1,2,3,4,5,pages]:page>=pages-3?[1,pages-4,pages-3,pages-2,pages-1,pages]:[1,page-1,page,page+1,pages];
  numbered.forEach((number,index)=>{
   if(index&&number>numbered[index-1]+1){const gap=document.createElement('span');gap.className='page-gap';gap.textContent='…';gap.setAttribute('aria-hidden','true');$('page-numbers').append(gap);}
   const button=document.createElement('button');button.type='button';button.dataset.page=number;button.textContent=number;button.setAttribute('aria-label',`Page ${number}`);if(number===page)button.setAttribute('aria-current','page');$('page-numbers').append(button);
  });
  const stats={records:matching.length,groups:unique(matching.flatMap(r=>list(r,context.dataset.group))).size,institutions:unique(matching.flatMap(r=>list(r,'institution'))).size,journals:unique(matching.map(r=>r.dataset.journal)).size};
  for(const [key,value] of Object.entries(stats))context.querySelectorAll('[data-metric="'+key+'"]').forEach(metric=>{metric.textContent=value;});
  for(const {metric,total,label,labelText} of collectionMetrics){
   metric.textContent=filtered?matching.length:total;
   if(label)label.textContent=filtered?'Publication records in this selection':labelText;
  }
  const query=prefix?new URLSearchParams([...new URLSearchParams(location.search)].filter(([key])=>!key.startsWith(prefix))):new URLSearchParams();for(const id of controls){const value=$(id).value;if(value&&!(id==='sort'&&value==='newest'))query.set(prefix+id,value);}if(legacyScope)query.set(prefix+'scope',legacyScope);
  if(page>1)query.set(prefix+'page',page);
  history.replaceState(null,'',location.pathname+(query.size?'?'+query:'')+location.hash);
 }
 for(const id of controls)$(id).addEventListener(['q','author','institution'].includes(id)?'input':'change',()=>render());
 if(context.dataset.view==='all')document.querySelectorAll('[data-catalogue-filter]').forEach(link=>link.addEventListener('click',event=>{if(event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;event.preventDefault();$('catalogue').value=link.dataset.catalogueFilter;render();}));
 $('reset').addEventListener('click',()=>{controls.forEach(id=>$(id).value=id==='sort'?'newest':'');legacyScope='';if(!prefix)history.replaceState(null,'',location.pathname);render();});
 $('previous').addEventListener('click',()=>{page--;render(false);$('result-count').scrollIntoView({block:'start'});});
 $('next').addEventListener('click',()=>{page++;render(false);$('result-count').scrollIntoView({block:'start'});});
 $('page-numbers').addEventListener('click',event=>{const button=event.target.closest('button[data-page]');if(!button||Number(button.dataset.page)===page)return;page=Number(button.dataset.page);render(false);$('page-numbers').querySelector('[aria-current]').focus({preventScroll:true});$('result-count').scrollIntoView({block:'start'});});
 $('export').addEventListener('click',()=>{const cell=s=>'"'+String(s||'').replace(/"/g,'""')+'"';const csv=['Title,Year,Catalogue,Application,Authors,Journal,Author institutions,Species or model,Source links',...matching.map(r=>[r.dataset.title,r.dataset.year,labels[r.dataset.catalogue],r.dataset.application,r.dataset.author,r.dataset.journal,r.dataset.institution,r.dataset.species,[...r.querySelectorAll('.source-links a:not(.permalink)')].map(a=>a.href).join(' | ')].map(cell).join(','))].join('\r\n');const url=URL.createObjectURL(new Blob(['\uFEFF'+csv],{type:'text/csv;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='BHOC-'+context.dataset.view+'-publications.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
 render(false);
 const anchors={institutionSearch:'institution',authorInput:'author',journalInput:'journal',scopeSelect:'catalogue'};
 const target=hashRow||$(anchors[fragment]||fragment);if(target){if(target.closest('#advanced'))$('advanced').open=true;target.scrollIntoView({block:'center'});}
})();
