/* Original Science directory appearance; exactly five featured publications per page. */
(()=>{'use strict';
 const root=document.querySelector('[data-science-feed]');if(!root)return;
 const base='/evidence/library/science/',size=5,params=new URLSearchParams(location.search);
 const grid=root.querySelector('.science-cards'),input=root.querySelector('[data-science-search]'),status=root.querySelector('[data-science-status]'),pager=root.querySelector('.science-feed-page');
 const template=document.getElementById('science-all-articles');if(!grid||!input||!template||!pager)return;
 const all=[...template.content.querySelectorAll('article.paper-card')];
 const urlFor=(n,q)=>{const u=new URL(n===1?base:base+'page/'+n+'/',location.origin);if(q)u.searchParams.set('q',q);return u.pathname+u.search;};
 const legacy=Number(params.get('page'));
 if(legacy>0&&location.pathname.replace(/index\.html$/,'')===base){
   params.delete('page');const n=Math.min(Math.max(1,Math.trunc(legacy)),Math.ceil(all.length/size));
   location.replace((n===1?base:base+'page/'+n+'/')+(params.size?'?'+params:'')+location.hash);return;
 }
 const readPage=()=>Number(location.pathname.match(/\/page\/(\d+)\//)?.[1]||1);
 function render(n,q,update){
   const needle=q.toLowerCase().trim(),matches=needle?all.filter(c=>c.textContent.toLowerCase().includes(needle)):all;
   const total=Math.max(1,Math.ceil(matches.length/size));n=Math.min(Math.max(1,n),total);
   const start=(n-1)*size,selected=matches.slice(start,start+size);
   grid.replaceChildren(...selected.map(c=>c.cloneNode(true)));
   status.textContent=matches.length?(start+1)+'–'+(start+selected.length)+' of '+matches.length+' publications':'No matching publications';
   if(!matches.length){const p=document.createElement('p');p.className='science-feed-empty';p.textContent='No featured publication matches this search.';grid.append(p);}
   pager.replaceChildren();
   for(let p=1;p<=total;p++){const a=document.createElement('a');a.href=urlFor(p,q);a.textContent='Page '+p;a.dataset.page=String(p);if(p===n)a.setAttribute('aria-current','page');pager.append(a);}
   pager.hidden=total===1;
   if(update)history.replaceState(null,'',urlFor(n,q)+location.hash);
 }
 input.value=params.get('q')||'';render(readPage(),input.value,false);
 input.addEventListener('input',()=>render(1,input.value,true));
 window.addEventListener('popstate',()=>{input.value=new URLSearchParams(location.search).get('q')||'';render(readPage(),input.value,false);});
})();
