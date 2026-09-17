(() => { 'use strict';
const details = [...document.querySelectorAll('.mobile-map')];
const currentURL = new URL(/^https?:/.test(location.href) ? location.href : (document.querySelector('link[rel=canonical]')?.href || 'https://bhoctherapeutics.com/bhoc/'));
const pagePath = value => new URL(value, currentURL).pathname.replace(/\/index\.html$/, '/');
for (const a of document.querySelectorAll('.mobile-map nav a[href]')) {
  const url = new URL(a.getAttribute('href'), currentURL);
  if (url.origin === currentURL.origin && !url.hash && pagePath(url.href) === pagePath(currentURL.href)) a.setAttribute('aria-current', 'page');
}
document.querySelectorAll('.crumbs strong').forEach(e => e.setAttribute('aria-current','page'));

document.addEventListener('click', event => {const a=event.target.closest('.mobile-map a'); if(a)a.closest('details').open=false;});
document.addEventListener('keydown', event => {if(event.key==='Escape')details.forEach(d=>{if(d.open){d.open=false;d.querySelector('summary')?.focus();}});});
const links=[...document.querySelectorAll('.article-side .toc a[href^="#"]')];
const entries=links.map(a=>({a,el:document.getElementById(decodeURIComponent(a.hash.slice(1)))})).filter(x=>x.el);
let queued=false;
const update=()=>{queued=false;let active=entries[0];for(const x of entries){if(x.el.getBoundingClientRect().top<=125)active=x;}
for(const x of entries){if(x===active)x.a.setAttribute('aria-current','location');else x.a.removeAttribute('aria-current');}};
const queue=()=>{if(!queued){queued=true;requestAnimationFrame(update);}};
window.addEventListener('scroll',queue,{passive:true});window.addEventListener('hashchange',queue);queue();
})();
