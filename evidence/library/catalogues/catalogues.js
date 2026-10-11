'use strict';
(() => {
 const holder=document.querySelector('#results');if(!holder)return;
 const rows=[...holder.querySelectorAll('.publication')];const $=id=>document.getElementById(id);
 const normal=s=>String(s||'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 const fieldIds=['year','direction','species','journal','product'];
 for(const name of fieldIds){const control=$(name);if(!control)continue;const values=[...new Set(rows.flatMap(r=>(r.dataset[name]||'').split('|')).filter(Boolean))];values.sort(name==='year'?(a,b)=>Number(b)-Number(a):(a,b)=>a.localeCompare(b));for(const value of values){const option=document.createElement('option');option.value=value;option.textContent=value;control.append(option);}}
 for(const value of [...new Set(rows.flatMap(r=>r.dataset.institution.split('|')).filter(Boolean))].sort()){const option=document.createElement('option');option.value=value;$('institutions').append(option);}
 const params=new URLSearchParams(location.search);const controls=['q',...fieldIds,'institution','status','sort'].filter(id=>$(id));for(const id of controls)if(params.has(id))$(id).value=params.get(id);
 let page=1,matching=[];const pageSize=30;
 const hashRow=rows.find(r=>'#'+r.id===location.hash);if(hashRow){$('status').value=hashRow.dataset.status;$('q').value=hashRow.dataset.title;}
 function render(reset=true){if(reset)page=1;const terms=normal($('q').value).trim().split(/\s+/).filter(Boolean);matching=rows.filter(r=>terms.every(t=>normal(r.dataset.search).includes(t))&&fieldIds.every(id=>!$(id)||!$(id).value||r.dataset[id].split('|').includes($(id).value))&&(!$('institution').value||normal(r.dataset.institution).includes(normal($('institution').value)))&&(!$('status').value||r.dataset.status===$('status').value));
 const sort=$('sort').value;matching.sort(sort==='title'?(a,b)=>a.dataset.title.localeCompare(b.dataset.title):sort==='oldest'?(a,b)=>(Number(a.dataset.year)||9999)-(Number(b.dataset.year)||9999):(a,b)=>(Number(b.dataset.year)||0)-(Number(a.dataset.year)||0));
 const pages=Math.max(1,Math.ceil(matching.length/pageSize));page=Math.min(page,pages);for(const row of rows)row.hidden=true;for(const row of matching.slice((page-1)*pageSize,page*pageSize)){row.hidden=false;holder.append(row);}
 $('result-count').textContent=matching.length+' matching '+($('status').value==='fragment'?'source fragments':'records');$('page-label').textContent='Page '+page+' of '+pages;$('previous').disabled=page===1;$('next').disabled=page===pages;$('empty').hidden=matching.length>0;
 const query=new URLSearchParams();for(const id of controls){const value=$(id).value;if(value&&!(id==='status'&&value==='bibliography')&&!(id==='sort'&&value==='newest'))query.set(id,value);}if(!$('status').value)query.set('status','');history.replaceState(null,'',location.pathname+(query.size?'?'+query:'')+location.hash);
 }
 for(const id of controls)$(id).addEventListener(['q','institution'].includes(id)?'input':'change',()=>render());
 $('reset').addEventListener('click',()=>{for(const id of controls)$(id).value=id==='status'?'bibliography':id==='sort'?'newest':'';history.replaceState(null,'',location.pathname);render();});
 $('previous').addEventListener('click',()=>{page--;render(false);$('result-count').scrollIntoView({block:'start'});});$('next').addEventListener('click',()=>{page++;render(false);$('result-count').scrollIntoView({block:'start'});});
 $('export').addEventListener('click',()=>{const cell=s=>'"'+String(s||'').replace(/"/g,'""')+'"';const csv=['Title,Year,Direction,Journal,Status,Source links',...matching.map(r=>[r.dataset.title,r.dataset.year,r.dataset.direction,r.dataset.journal,r.dataset.status,[...r.querySelectorAll('.source-links a:not(.permalink)')].map(a=>a.href).join(' | ')].map(cell).join(','))].join('\r\n');const url=URL.createObjectURL(new Blob(['\uFEFF'+csv],{type:'text/csv;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='BHOC-evidence-'+location.pathname.split('/').pop().replace('.html','')+'.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
 render();if(hashRow)hashRow.scrollIntoView({block:'center'});
})();
