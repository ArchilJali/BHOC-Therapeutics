/* Search is progressive enhancement; each publication page is crawlable HTML. */
(()=>{'use strict';
 const root=document.querySelector('[data-science-feed]');
 if(root){
  const base='/evidence/library/science/';const params=new URLSearchParams(location.search);
  const legacy=Number(params.get('page'));
  if(location.pathname.replace(/index\.html$/,'')===base && legacy>1){params.delete('page');location.replace(base+'page/'+Math.min(legacy,Number(root.dataset.pages))+'/'+(params.size?'?'+params:'')+location.hash);return;}
  const grid=root.querySelector('.science-cards'),template=document.getElementById('science-all-articles'),input=root.querySelector('[data-science-search]'),status=root.querySelector('[data-science-status]'),pager=root.querySelector('.science-feed-page');
  const original=grid.innerHTML;
  const apply=()=>{const q=input.value.toLowerCase().trim();if(!q){grid.innerHTML=original;status.textContent=root.dataset.status;if(pager)pager.hidden=false;return;}
   const cards=[...template.content.querySelectorAll('.paper-card')].filter(card=>card.textContent.toLowerCase().includes(q));grid.replaceChildren(...cards.map(card=>card.cloneNode(true)));status.textContent=cards.length+' matching analyses';if(pager)pager.hidden=true;
   if(!cards.length){const p=document.createElement('p');p.textContent='No featured analysis matches this search. Search the complete research catalogue below for more publications.';grid.append(p);}
  };
  input?.addEventListener('input',apply);if(params.get('q')){input.value=params.get('q');apply();}
 }
 const reveal=()=>{let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}const el=document.getElementById(id);if(el){let d=el.closest('details');while(d){d.open=true;d=d.parentElement?.closest('details');}}};
 reveal();window.addEventListener('hashchange',reveal);
})();
