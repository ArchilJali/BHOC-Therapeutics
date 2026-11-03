#!/usr/bin/env python3
"""Unify existing Science pages without rewriting their scientific body text."""
from pathlib import Path
from urllib.parse import urljoin
from collections import Counter
from copy import deepcopy
from bs4 import BeautifulSoup
import json, re, html

BASE='https://bhoctherapeutics.com'
DIR='/evidence/library/science/'
DATE='2026-11-03'
ASSET='/evidence/library/assets/science-20261103'
DATA={
'oxygen-delivery-potency.html': (
'Oxygen Delivery Potency, L-TOF & RBC Storage | BHOC',
'Explore oxygen delivery potency, the L-TOF metric, red blood cell storage and hemoglobin oxygen carriers, with the original study and related evidence.',
'oxygen delivery potency, L-TOF, red blood cell storage, oxygen dissociation curve, hemoglobin-based oxygen carriers, tissue oxygenation',
'What is oxygen delivery potency?',
'Oxygen delivery potency describes the functional oxygen-transfer capacity of a blood product under defined test conditions. The L-TOF (Lung-to-Tissue Oxygen Flux) framework compares oxygen loading and unloading rather than relying on hemoglobin concentration alone.'),
'nitric-oxide-scavenging-hboc-vasoconstriction.html': (
'Nitric Oxide Scavenging, HBOCs & Microcirculation | BHOC',
'Read source-linked evidence on nitric oxide scavenging, hemoglobin-based oxygen carriers, vascular tone, microcirculation and effective tissue oxygenation.',
'nitric oxide scavenging, HBOC vasoconstriction, hemoglobin-based oxygen carriers, hypoxic vasodilation, microcirculation, tissue oxygenation',
'How are nitric oxide and tissue oxygenation connected?',
'The cited research connects hemoglobin-linked nitric oxide bioactivity, vascular tone and microcirculatory blood flow. It distinguishes the capacity to carry oxygen from effective delivery of that oxygen to tissues.'),
'aabb-rbc-transfusion-thresholds-oxygen-delivery.html': (
'RBC Transfusion Thresholds & Oxygen Delivery | BHOC',
'Explore the AABB review of red blood cell transfusion thresholds, restrictive and liberal strategies, clinical context and oxygen-delivery function.',
'red blood cell transfusion threshold, RBC transfusion, restrictive transfusion, liberal transfusion, oxygen delivery, AABB review',
'Why does clinical context matter when comparing transfusion thresholds?',
'The reviewed trials compare restrictive and liberal red blood cell transfusion strategies in different patient groups. This analysis examines clinical context, hemoglobin characteristics, oxygen-delivery function and blood product availability.'),
'pregnancy-sickle-cell-oxygen-delivery.html': (
'Sickle Cell Disease in Pregnancy: Transfusion & Oxygen | BHOC',
'Explore TAPS2 evidence on sickle cell disease in pregnancy, prophylactic transfusion, HbS reduction and oxygen-carrying capacity, with source links.',
'sickle cell disease pregnancy, prophylactic transfusion, TAPS2, HbS reduction, oxygen carrying capacity, sickle cell oxygen delivery',
'What does TAPS2 examine in sickle cell disease and pregnancy?',
'TAPS2 examines prophylactic transfusion in pregnancy with sickle cell disease. The analysis distinguishes reducing HbS, increasing oxygen-carrying capacity and assessing defined maternal or fetal outcomes.'),
'prehospital-blood-transfusion-oxygen-delivery.html': (
'Prehospital Blood Transfusion & Oxygen Delivery | BHOC',
'Read the PHBTC framework on prehospital blood transfusion, hemorrhagic shock, physiological assessment, oxygen delivery and time to treatment.',
'prehospital blood transfusion, hemorrhagic shock, oxygen delivery, emergency medical services, PHBTC, prehospital resuscitation',
'What connects prehospital blood transfusion with oxygen delivery?',
'The PHBTC framework examines hemorrhagic-shock physiology, restoration of oxygen delivery and time to treatment. This analysis separates the physiological aim from the measurements available in the field.'),
'sepsis-microcirculation-tissue-oxygenation-bhoc.html': (
'Sepsis, Microcirculation & Tissue Oxygenation | BHOC',
'Explore inflammation, sepsis, endothelial dysfunction, microcirculation and tissue oxygenation, with source-linked context for hemoglobin oxygen carriers.',
'sepsis microcirculation, tissue oxygenation, tissue hypoxia, endothelial dysfunction, oxygen delivery, hemoglobin oxygen carriers',
'Why can tissue oxygenation be impaired during severe inflammation?',
'The reviewed physiology links inflammation, endothelial dysfunction, edema and disturbed microcirculation with impaired oxygen transport from blood to tissues. The analysis follows oxygen delivery beyond blood oxygen content alone.'),
'enzyme-converted-type-o-whole-blood.html': (
'Enzyme-Converted Type O Whole Blood: Evidence | BHOC',
'Explore enzyme-converted type O whole blood research: A-antigen reduction, compatibility, red-cell survival, storage and oxygen-delivery questions.',
'enzyme converted type O whole blood, universal donor blood, blood group compatibility, red blood cell survival, oxygen delivery',
'What is enzyme-converted type O whole blood?',
'This experimental approach uses enzymes to reduce A-antigen structures in type A blood. The swine-model study addresses compatibility; the analysis separately examines red-cell survival, storage and oxygen-delivery questions.'),
'nobel-foundations-oxygen-metabolism-physiology.html': (
'Oxygen & Metabolism: Nobel Scientific Foundations | BHOC',
'Explore Nobel-recognized discoveries in capillary circulation, cellular respiration, metabolism, nitric oxide and oxygen sensing, with original sources.',
'oxygen sensing, cellular respiration, oxygen metabolism, microcirculation, nitric oxide, hypoxia inducible factor, Nobel physiology',
'Which discoveries underpin oxygen-delivery science?',
'Nobel-recognized work on capillary regulation, cellular respiration, metabolism, nitric oxide and oxygen sensing explains why tissue oxygen delivery involves more than the oxygen content of blood.'),
'rbc-unit-hemoglobin-dose-variability.html': (
'RBC Hemoglobin Dose: Why One Unit Is Not a Fixed Dose | BHOC',
'Explore hemoglobin dose variability in red blood cell units, component standards, stored RBC function and interpretation of transfusion responses.',
'hemoglobin dose, red blood cell unit, RBC hemoglobin content, packed red blood cells, transfusion response, oxygen delivery potency',
'Does one RBC unit contain a fixed hemoglobin dose?',
'No. Component volume, hemoglobin concentration and processing vary. This commentary reviews why a unit count does not establish the hemoglobin mass transfused or the resulting tissue oxygen delivery.'),
'hypoxic-rbc-storage-kidney-oxygen-delivery.html': (
'Hypoxic RBC Storage & Kidney Oxygen Delivery | BHOC',
'Explore ex vivo human-kidney evidence on hypoxic red blood cell storage, oxygen handling and organ perfusion, with the original study and related science.',
'hypoxic RBC storage, red blood cell storage, kidney oxygen delivery, organ perfusion, tissue oxygenation, hypoxic blood storage',
'What does hypoxic red blood cell storage research measure?',
'The cited ex vivo human-kidney study examines how red-cell storage conditions relate to organ oxygen handling. The analysis separates measured perfusion findings from wider clinical conclusions.'),
'index.html': (
'Oxygen Delivery & Hemoglobin Carrier Research | BHOC Science',
'Explore source-linked research on oxygen delivery, hemoglobin-based oxygen carriers, RBC transfusion, nitric oxide, microcirculation and tissue oxygenation.',
'oxygen delivery research, hemoglobin-based oxygen carriers, BHOC, Biological Hemoglobin Oxygen Carrier, tissue oxygenation, red blood cell transfusion, microcirculation',
'What does the BHOC Science library cover?',
'Source-linked studies and analyses on hemoglobin-based oxygen carriers (HBOCs), oxygen transport, red blood cell transfusion, nitric oxide, microcirculation and tissue oxygenation within Precision Oxygen Therapeutics.')}

CSS=r'''/* BHOC Science — shared reading and catalogue design, 3 November 2026. */
:root{--science-ink:#263440;--science-navy:#102f49;--science-teal:#087a76;--science-link:#175b91;--science-muted:#586a78;--science-line:#dce5eb;--science-wash:#f5f7f9;--science-soft:#edf6f5}
html{scroll-behavior:smooth;scroll-padding-top:100px}
body.science-page{margin:0;padding:0;background:var(--science-wash);color:var(--science-ink);font:16px/1.5 Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
.science-page *, .science-page *:before,.science-page *:after{box-sizing:border-box}
body.science-page main.bhoc-science{width:calc(100% - 40px)!important;max-width:1180px!important;margin:18px auto 28px!important;padding:0!important;min-width:0;color:var(--science-ink)}
.science-page .science-content{padding:24px 30px;background:#fff;border:1px solid var(--science-line);border-radius:12px}
.bhoc-science :where(.container,.article,.evidence-article,.policy-body,.section,.hero,.topic-shell){width:auto;max-width:none;margin:0;padding:0;background:transparent;border:0;box-shadow:none;min-width:0}
.bhoc-science :where(h1,h2,h3,h4){color:var(--science-navy);text-align:left;text-wrap:pretty;border:0;padding:0;letter-spacing:-.025em}
.bhoc-science h1{font-size:clamp(28px,3.2vw,42px);line-height:1.16;margin:0 0 12px;font-weight:750;max-width:1060px}
.bhoc-science h2{font-size:clamp(21px,2.1vw,26px);line-height:1.25;margin:24px 0 10px;scroll-margin-top:100px}
.bhoc-science h3{font-size:18px;line-height:1.3;margin:18px 0 8px}
.bhoc-science h4{font-size:16px;line-height:1.35;margin:14px 0 6px}
.bhoc-science p,.bhoc-science li{font-size:16px;line-height:1.5;color:var(--science-ink)}
.bhoc-science p{margin:8px 0 11px}.bhoc-science li{margin:5px 0}.bhoc-science ul,.bhoc-science ol{margin:8px 0 14px;padding-left:24px}
.bhoc-science a{color:var(--science-link);text-underline-offset:3px;overflow-wrap:anywhere}.bhoc-science a:hover{text-decoration:underline}.bhoc-science a:focus-visible,.bhoc-science button:focus-visible,.bhoc-science summary:focus-visible{outline:3px solid var(--science-teal);outline-offset:3px}
.bhoc-science :where(.lead,.subtitle,.policy-deck){font-size:17px;line-height:1.45;color:var(--science-muted);margin:10px 0 16px}
.bhoc-science :where(.eyebrow,.policy-kicker,.science-eyebrow){font-size:11px;font-weight:750;text-transform:uppercase;letter-spacing:.1em;color:var(--science-teal);margin:0 0 7px}
.bhoc-science :where(.paper-meta,.meta,.policy-meta,.footnote,.names){font-size:13px;line-height:1.45;color:var(--science-muted)}
.bhoc-science .policy-meta{display:flex;gap:8px 18px;flex-wrap:wrap;margin:10px 0 18px}
.bhoc-science :where(.highlight-box,.concept-box,.note,.callout,.questions,.logic,.quote,.evidence-boundary){background:var(--science-soft);border:1px solid #d4e8e5;border-left:3px solid var(--science-teal);border-radius:8px;padding:13px 17px;margin:14px 0;color:var(--science-ink);font-size:15px;line-height:1.5}
.bhoc-science :where(.highlight-box,.concept-box,.note,.callout,.questions,.logic,.quote) p:last-child{margin-bottom:0}
.bhoc-science .science-answer{background:var(--science-soft);border-left:3px solid var(--science-teal);border-radius:0 8px 8px 0;padding:14px 18px;margin:16px 0}
.bhoc-science .science-answer h2{font-size:18px;margin:0 0 7px;letter-spacing:-.015em}.bhoc-science .science-answer p{margin:0;font-size:15px;line-height:1.5}
.bhoc-science .science-toc{background:#f8fafb;border:1px solid var(--science-line);border-radius:8px;padding:10px 14px;margin:14px 0 20px}.bhoc-science .science-toc summary{cursor:pointer;font-size:14px;font-weight:700;color:var(--science-navy)}.bhoc-science .science-toc ol{columns:2;column-gap:30px;margin:10px 0 4px;font-size:14px}.bhoc-science .science-toc li{font-size:14px;break-inside:avoid}
.bhoc-science :where(.metric-grid,.metrics,.grid,.grid-3){display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,210px),1fr));gap:12px;margin:14px 0}.bhoc-science .metric{background:#f8fafb;border:1px solid var(--science-line);border-radius:8px;padding:13px}.bhoc-science .metric strong{display:block;font-size:24px;line-height:1.2;color:var(--science-teal)}.bhoc-science .metric span{display:block;margin-top:5px;font-size:14px;line-height:1.4}
.bhoc-science :where(.badge,.pill,.tag){display:inline-block;background:var(--science-soft);color:var(--science-teal);border-radius:5px;padding:4px 7px;font-size:12px;margin:0 5px 5px 0}
.bhoc-science :where(.science-table-wrap,.rbc-table-wrap,.table-wrap){max-width:100%;overflow-x:auto;margin:14px 0;border:1px solid var(--science-line);border-radius:8px;overscroll-behavior-x:contain}
.bhoc-science table{width:100%;border-collapse:collapse;margin:0;font-size:14px;line-height:1.45;text-align:left;background:#fff}.bhoc-science caption{text-align:left;color:var(--science-muted);padding:10px 12px;font-size:13px}.bhoc-science td,.bhoc-science th{padding:10px 12px;border-bottom:1px solid var(--science-line);vertical-align:top;overflow-wrap:anywhere}.bhoc-science th{background:#f0f4f7;color:var(--science-navy);font-weight:650}.bhoc-science tr:last-child td{border-bottom:0}
.bhoc-science img{max-width:100%;height:auto}.bhoc-science figure{margin:16px 0}.bhoc-science figure img,.bhoc-science .hero>img{display:block;width:auto;max-height:380px;object-fit:contain;margin:auto;border-radius:8px}.bhoc-science figcaption{font-size:13px;line-height:1.45;color:var(--science-muted);margin-top:8px}.bhoc-science .policy-hero img{width:100%;max-height:360px;object-fit:contain;background:#f8fafb}
.bhoc-science .policy-grid{display:block}.bhoc-science .policy-aside{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;border-top:1px solid var(--science-line);padding-top:16px;margin-top:22px}.bhoc-science .policy-aside section{min-width:0}.bhoc-science .policy-aside h2{font-size:18px;margin-top:0}.bhoc-science .rbc-toc{display:none}
.bhoc-science .topic-shell{border-top:1px solid var(--science-line);margin-top:22px;padding-top:16px}.bhoc-science .topic-shell h2{font-size:21px}.bhoc-science .topic-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:14px}.bhoc-science .topic-card{padding:14px;border:1px solid var(--science-line);border-radius:8px}
.bhoc-science .science-related{margin-top:24px;padding-top:18px;border-top:1px solid var(--science-line)}.bhoc-science .science-related h2{font-size:20px;margin:0 0 10px}.bhoc-science .science-related ul{display:flex;flex-wrap:wrap;gap:8px 20px;list-style:none;padding:0;margin:0}.bhoc-science .science-related li{font-size:14px;margin:0}
.bhoc-science .science-revision{font-size:12px;color:var(--science-muted);margin:20px 0 0}
/* Directory: no narrow reading column or vacant sidebar. */
.bhoc-science .knowledge-hero{background:#fff;border:1px solid var(--science-line);border-top:3px solid var(--science-teal);border-radius:10px;padding:22px 26px;margin:0 0 14px;text-align:left}.bhoc-science .knowledge-hero:before{display:none}.bhoc-science .knowledge-hero h1{max-width:1000px;margin:0 0 10px;font-size:clamp(28px,3.1vw,40px)}.bhoc-science .knowledge-hero>p{max-width:none;font-size:16px;margin:8px 0}
.bhoc-science .knowledge-actions{display:flex;flex-wrap:wrap;justify-content:flex-start;gap:8px 16px;margin-top:12px}.bhoc-science .knowledge-actions a{font-size:14px;font-weight:650}
.bhoc-science .knowledge-grid{display:block;margin:18px 0}.bhoc-science .knowledge-card{padding:0;border:0;background:none;box-shadow:none}.bhoc-science .knowledge-card>h2{margin:0 0 12px}.bhoc-science .science-cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.bhoc-science .paper-card{border:1px solid var(--science-line);border-top:3px solid #c9dfdf;border-radius:10px;padding:17px 19px;background:#fff;margin:0;min-width:0}.bhoc-science .paper-card h3{font-size:19px;margin:0 0 8px;line-height:1.3}.bhoc-science .paper-card h3 a{color:var(--science-navy);text-decoration:none}.bhoc-science .paper-card p{font-size:14px;line-height:1.45;margin:7px 0}.bhoc-science .paper-card .paper-meta{font-size:12.5px;color:var(--science-muted)}.bhoc-science .paper-links{display:flex;flex-wrap:wrap;gap:7px 14px;margin-top:11px}.bhoc-science .paper-links a{font-size:13px;font-weight:650}
.bhoc-science .science-side{margin:16px 0 0}.bhoc-science .context-box{padding:15px 19px;background:#eaf1f5;border:1px solid var(--science-line);border-radius:8px}.bhoc-science .context-box h2{font-size:20px;margin:3px 0 7px}.bhoc-science .context-box p{font-size:14px;line-height:1.45;margin:6px 0}.bhoc-science .context-box a{font-size:14px}
.bhoc-science .nobel-feature{display:flex;align-items:center;gap:16px;background:#fff;border:1px solid var(--science-line);padding:14px 19px;border-radius:10px;text-decoration:none;margin:14px 0}.bhoc-science .nobel-feature-medal{flex:0 0 62px;width:62px;height:62px}.bhoc-science .nobel-feature-medal img{width:62px;height:62px;object-fit:contain}.bhoc-science .nobel-feature small{display:block;font-size:11px;color:var(--science-teal);text-transform:uppercase;font-weight:700}.bhoc-science .nobel-feature strong{display:block;font-size:18px;color:var(--science-navy)}.bhoc-science .nobel-feature p{font-size:13px;margin:4px 0}.bhoc-science .nobel-link{font-size:13px;font-weight:650}
.bhoc-science .science-feed-tools{display:flex;align-items:center;flex-wrap:wrap;gap:10px;margin:12px 0;padding:12px 15px;background:#fff;border:1px solid var(--science-line);border-radius:8px}.bhoc-science .science-feed-tools label{flex:1 1 280px;font-size:13px;font-weight:650}.bhoc-science .science-feed-tools input{display:block;width:100%;margin-top:4px;padding:9px 11px;border:1px solid #b9cad6;border-radius:6px;font:inherit;font-size:16px;min-height:42px}.bhoc-science .science-feed-summary{font-size:13px;color:var(--science-muted)}.bhoc-science .science-feed-page{display:flex;justify-content:center;align-items:center;flex-wrap:wrap;gap:8px;margin:18px 0}.bhoc-science .science-feed-page a,.bhoc-science .science-feed-page span{min-height:42px;padding:9px 14px;border:1px solid var(--science-line);border-radius:7px;background:#fff;font-size:14px}.bhoc-science .science-feed-page [aria-current=page]{background:var(--science-navy);color:white;border-color:var(--science-navy)}
.bhoc-science .embedded-catalogue{padding:20px 22px;background:#fff;border:1px solid var(--science-line);border-radius:10px;margin-top:20px}.bhoc-science .embedded-catalogue>h2{margin:0 0 9px}.bhoc-science .embedded-catalogue .publication{padding:15px 0}.bhoc-science .embedded-catalogue .publication h3{font-size:17px;line-height:1.35}.bhoc-science .embedded-catalogue .publication p{font-size:14px}.bhoc-science .evidence-metrics{margin:14px 0}.bhoc-science .evidence-metrics strong{color:var(--science-teal)}.bhoc-science .filter-grid label{min-width:0}.bhoc-science .filter-grid select{max-width:100%}
/* Scientific history keeps its native accessible details/timeline. */
.bhoc-science.science-foundations .hero{display:grid;grid-template-columns:95px minmax(0,1fr);gap:20px;align-items:start}.bhoc-science .medal img{width:95px}.bhoc-science .tags{display:flex;gap:8px;flex-wrap:wrap;font-size:11px;color:var(--science-teal)}.bhoc-science .quickgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:16px 0}.bhoc-science .quickitem{background:#f6f8fa;border:1px solid var(--science-line);border-radius:7px;padding:10px}.bhoc-science .quickitem b{display:block;color:var(--science-teal);font-size:18px}.bhoc-science .quickitem strong{font-size:12px;line-height:1.35;display:block}.bhoc-science .workarea{display:block}.bhoc-science .year-item{border:1px solid var(--science-line);border-radius:8px;margin:10px 0;background:#fff}.bhoc-science .year-summary{display:flex;gap:15px;align-items:center;padding:13px 16px;cursor:pointer;color:var(--science-navy);font-weight:650}.bhoc-science .yr{color:var(--science-teal);font-size:21px}.bhoc-science .chev{margin-left:auto}.bhoc-science .year-body{padding:0 16px 15px}.bhoc-science .year-head{display:flex;gap:15px;align-items:center}.bhoc-science .bigyear{font-size:28px;color:var(--science-teal);font-weight:700}.bhoc-science .cols{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:15px}.bhoc-science .col p{font-size:14px}.bhoc-science .side{margin-top:16px}.bhoc-science .side-card{background:#f6f8fa;padding:16px;border-radius:8px}
.science-fallback-header{background:#fff;border-bottom:1px solid var(--science-line);padding:14px max(20px,calc((100% - 1180px)/2));display:flex;align-items:center;justify-content:space-between;gap:18px}.science-fallback-header>a{font-size:24px;font-weight:800;text-decoration:none;color:var(--science-navy)}.science-fallback-header>a span{color:#e73936}.science-fallback-header small{font-size:9px;letter-spacing:.12em;display:block}.science-fallback-header nav{display:flex;gap:15px;flex-wrap:wrap}.science-fallback-header nav a{font-size:13px;color:var(--science-navy)}
.science-page .bhoc-evidence-links,.science-page .topic-guide-link{max-width:1180px;margin:15px auto;padding:0 20px;font-size:13px;display:flex;flex-wrap:wrap;gap:12px}.science-page .bhoc-evidence-links a,.science-page .topic-guide-link a{color:var(--science-link)}
.science-page .skip{position:absolute;top:-100px;left:12px}.science-page .skip:focus{top:12px;background:#fff;padding:10px;z-index:9999}.bhoc-science [hidden]{display:none!important}.bhoc-science template{display:none!important}
@media(max-width:760px){body.science-page main.bhoc-science{width:calc(100% - 24px)!important;margin:12px auto 20px!important}.science-page .science-content{padding:19px 18px}.bhoc-science .science-cards{grid-template-columns:1fr}.bhoc-science .knowledge-hero{padding:20px}.bhoc-science .embedded-catalogue{padding:18px 16px}.bhoc-science .quickgrid{grid-template-columns:repeat(2,minmax(0,1fr))}.bhoc-science .policy-aside{grid-template-columns:1fr}.bhoc-science .science-toc ol{columns:1}.bhoc-science .cols{grid-template-columns:1fr}.bhoc-science table{min-width:520px}.bhoc-science .nobel-feature{align-items:flex-start}.science-fallback-header{flex-wrap:wrap}.bhoc-science.science-foundations .hero{grid-template-columns:1fr}.bhoc-science .medal-wrap{display:none}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{scroll-behavior:auto!important}}
@media print{.bhoc-shell-header,.bhoc-shell-footer,.science-fallback-header,.science-feed-tools,.science-feed-page,.science-toc{display:none!important}body.science-page{background:#fff}body.science-page main.bhoc-science{width:100%!important;max-width:none!important}.science-page .science-content{padding:0;border:0}.bhoc-science .science-table-wrap{overflow:visible}.bhoc-science table{min-width:0}.bhoc-science a{color:inherit}}
'''
JS=r'''/* Search is progressive enhancement; each publication page is crawlable HTML. */
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
'''

def serialized(s):
    return chr(10).join(line.rstrip() for line in str(s).splitlines()).rstrip().replace('content="summary_large_image" name="twitter:card"','name="twitter:card" content="summary_large_image"')
def fragment(source):return BeautifulSoup(source,'html.parser')
def add_fragment(parent,source):
    for e in list(fragment(source).contents):parent.append(e)
def text(el):return el.get_text(' ',strip=True)
def semantic_fingerprint(main):
    return Counter(text(e) for e in main.select('p,li,td,th,figcaption') if not e.find_parent(['nav','template']) and text(e))
def meta(s,key,value,prop=False):
    attr='property' if prop else 'name'
    found=s.head.find_all('meta',attrs={attr:key})
    tag=found[0] if found else s.new_tag('meta',attrs={attr:key});tag['content']=value
    if not found:s.head.append(tag)
    for extra in found[1:]:extra.decompose()
def structured(s,identifier,data):
    for old in s.select('#'+identifier):old.decompose()
    tag=s.new_tag('script',attrs={'type':'application/ld+json','id':identifier})
    tag.string=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/');s.head.append(tag)
def absolute_links(s,path):
    for el in s.select('[href],[src]'):
        for attr in ('href','src'):
            val=el.get(attr)
            if val and not val.startswith(('#','mailto:','tel:','data:','javascript:','http:','https:','//')):
                u=urljoin(BASE+'/'+str(path),val);el[attr]=u[len(BASE):] if u.startswith(BASE) else u

def normalize_schema(s,url,title,desc,keywords,is_index):
    # Only editorial page nodes, never nested bibliography/citation records.
    def visit(obj):
        if isinstance(obj,list):
            for x in obj:visit(x)
        elif isinstance(obj,dict):
            typ=obj.get('@type',[]);types=[typ] if isinstance(typ,str) else typ
            if any(t in types for t in ('TechArticle','Article','ScholarlyArticle','NewsArticle','WebPage','CollectionPage')):
                obj.update(name=title,description=desc,url=url)
                if 'headline' in obj:obj['headline']=title.split(' | ')[0]
                if '@id' in obj and '#webpage' in obj['@id']:obj['@id']=url+'#webpage'
                if not is_index and any(t in types for t in ('TechArticle','Article','ScholarlyArticle','NewsArticle')):
                    obj['dateModified']=DATE;obj['keywords']=[v.strip() for v in keywords.split(',')]
            if '@graph' in obj:visit(obj['@graph'])
    for sc in s.select('script[type="application/ld+json"]'):
        try:
            j=json.loads(sc.string or sc.get_text());visit(j);sc.string=json.dumps(j,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/')
        except (ValueError,TypeError):raise ValueError('Malformed existing structured data: '+url)
    crumbs=[{'@type':'ListItem','position':1,'name':'BHOC Therapeutics','item':BASE+'/'},{'@type':'ListItem','position':2,'name':'Scientific evidence','item':BASE+DIR}]
    if not is_index:crumbs.append({'@type':'ListItem','position':3,'name':text(s.h1),'item':url})
    for sc in list(s.select('script[data-seo-breadcrumbs]')):sc.decompose()
    structured(s,'science-breadcrumb-schema',{'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':crumbs})

paths=sorted(Path('evidence/library/science').glob('*.html'))+[Path('science/rbc-unit-hemoglobin-dose-variability.html'),Path('science/hypoxic-rbc-storage-kidney-oxygen-delivery.html')]
report=[]
for path in paths:
    source=path.read_text()
    if 'data-science-refresh="20261103"' in source:continue
    s=BeautifulSoup(source,'html.parser');main=s.find('main');assert main is not None,path
    before=semantic_fingerprint(main)
    is_index=path.name=='index.html';title,desc,keywords,question,answer=DATA[path.name]
    url=BASE+('/'+str(path) if not is_index else DIR)
    absolute_links(s,path)
    for el in list(s.find_all('style')):el.decompose()
    for el in list(s.select('link[rel=stylesheet]')):
        if 'unified-shell.css' not in el.get('href','') and not(is_index and '/catalogues/catalogues.css' in el.get('href','')):el.decompose()
    for el in s.select('[style]'):del el['style']
    for sc in list(s.find_all('script')):
        src=sc.get('src','')
        if any(term in src for term in ('navigation-context.js','/navigation.js')) or (is_index and not src and re.search(r'PAGE_SIZE\s*=\s*5',sc.get_text())):sc.decompose()
    if not any('unified-shell.js' in t.get('src','') for t in s.find_all('script')):s.head.append(s.new_tag('script',src='/unified-shell.js?v=20261011-shell5',defer=''))
    s.head.append(s.new_tag('link',rel='stylesheet',href=ASSET+'.css'));s.head.append(s.new_tag('script',src=ASSET+'.js',defer=''))
    for el in list(s.select('body>header,body>.bhoc-guide,body>.brand-network')):el.decompose()
    header=fragment('<header class="science-fallback-header"><a href="/" aria-label="BHOC Therapeutics home">BH<span>O</span>C<small>THERAPEUTICS</small></a><nav aria-label="Primary navigation"><a href="/science/">Science</a><a href="/technology/">Technology</a><a href="/applications/">Applications</a><a href="/evidence/library/catalogues/">Evidence</a><a href="/news/">News</a><a href="/contact/">Contact</a></nav></header>').header
    s.body.insert(0,header);s.body['class']=['science-page'];s.body['data-science-refresh']='20261103'
    main['id']='main';main['class']=['bhoc-science','science-directory' if is_index else 'science-article']
    if 'nobel-' in path.name:main['class'].append('science-foundations')
    for e in list(main.select('nav.breadcrumbs,nav.breadcrumb,nav.policy-crumbs,div.crumbs,div.breadcrumb')):e.decompose()
    if not is_index:
        wrapper=s.new_tag('div',attrs={'class':'science-content'})
        for e in list(main.contents):wrapper.append(e.extract())
        main.append(wrapper)
    h1=main.find('h1');assert h1 is not None,path
    if is_index:h1.string='Oxygen Delivery & Hemoglobin Carrier Research'
    anchor=h1.find_next_sibling()
    if not anchor or anchor.name!='p':anchor=h1
    summary=fragment('<section class="science-answer" aria-labelledby="science-key-answer"><h2 id="science-key-answer">'+html.escape(question)+'</h2><p>'+html.escape(answer)+'</p></section>').section
    if not is_index:anchor.insert_after(summary)
    if not is_index and 'nobel-' not in path.name:
        headings=[h for h in main.find_all('h2') if h is not summary.h2 and not h.find_parent('aside')]
        used={e.get('id') for e in s.select('[id]')}
        for i,h in enumerate(headings,1):
            if not h.get('id'):
                slug=re.sub('[^a-z0-9]+','-',text(h).lower()).strip('-') or 'section-'+str(i)
                if slug in used:slug+='-'+str(i)
                h['id']=slug;used.add(slug)
        toc='<details class="science-toc"><summary>In this article</summary><ol>'+''.join('<li><a href="#'+html.escape(h['id'])+'">'+html.escape(text(h))+'</a></li>' for h in headings)+'</ol></details>'
        summary.insert_after(fragment(toc).details)
    for table in list(main.find_all('table')):
        if not table.find_parent(class_=['science-table-wrap','rbc-table-wrap','table-wrap']):
            wrap=s.new_tag('div',attrs={'class':'science-table-wrap','role':'region','tabindex':'0','aria-label':text(table.caption) if table.caption else 'Scientific data table'});table.wrap(wrap)
        for th in table.select('thead th'):th['scope']='col'
    for img in main.find_all('img'):
        img['decoding']='async'
        if img.get('fetchpriority')!='high':img['loading']='lazy'
    s.title.string=title
    for key,value in [('description',desc),('keywords',keywords),('twitter:title',title),('twitter:description',desc)]:meta(s,key,value)
    for key,value in [('og:title',title),('og:description',desc),('og:url',url)]:meta(s,key,value,True)
    canon=s.head.select_one('link[rel=canonical]');assert canon is not None,path;canon['href']=url
    normalize_schema(s,url,title,desc,keywords,is_index)
    if not is_index:
        citations=list(dict.fromkeys(a['href'] for a in main.select('a[href]') if any(d in a['href'] for d in ('doi.org/','pubmed.ncbi.nlm.nih.gov/','nobelprize.org/'))))
        found_article=False
        for sc in s.select('script[type="application/ld+json"]'):
            j=json.loads(sc.string or sc.get_text())
            def enrich(obj):
                global found_article
                if isinstance(obj,list):
                    for x in obj:enrich(x)
                elif isinstance(obj,dict):
                    typ=obj.get('@type');types=[typ] if isinstance(typ,str) else typ or []
                    if any(t in types for t in ('Article','TechArticle','ScholarlyArticle','NewsArticle')):
                        obj['abstract']=answer;obj['mainEntityOfPage']={'@id':url+'#webpage'};obj.setdefault('citation',citations);found_article=True
                    if '@graph' in obj:enrich(obj['@graph'])
            enrich(j);sc.string=json.dumps(j,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/')
        if not found_article:
            structured(s,'science-article-schema',{'@context':'https://schema.org','@type':'TechArticle','headline':text(h1),'url':url,'description':desc,'abstract':answer,'inLanguage':'en','dateModified':DATE,'author':{'@id':BASE+'/#archil-jaliashvili'},'publisher':{'@id':BASE+'/#organization'},'mainEntityOfPage':{'@id':url+'#webpage'},'citation':citations,'keywords':[x.strip() for x in keywords.split(',')]})
        related=[('Oxygen delivery potency','oxygen-delivery-potency.html'),('Nitric oxide and microcirculation','nitric-oxide-scavenging-hboc-vasoconstriction.html'),('RBC transfusion thresholds','aabb-rbc-transfusion-thresholds-oxygen-delivery.html')]
        links=''.join('<li><a href="'+DIR+u+'">'+label+'</a></li>' for label,u in related if u!=path.name)
        add_fragment(main.select_one('.science-content'),'<nav class="science-related" aria-label="Related scientific evidence"><h2>Explore related science</h2><ul><li><a href="'+DIR+'">All scientific analyses</a></li>'+links+'<li><a href="/evidence/library/catalogues/related.html">Complete research catalogue</a></li></ul></nav><p class="science-revision">Page layout and discovery metadata updated <time datetime="'+DATE+'">3 November 2026</time>. Original scientific content and source links retained.</p>')
    after=semantic_fingerprint(main);lost=before-after
    assert not lost,(path,'Original scientific text changed',dict(lost))
    path.write_text(serialized(s)+'\n')
    report.append({'path':str(path),'preserved_text_blocks':sum(before.values()),'title':title,'keywords':keywords,'canonical':url})

# Real HTML pagination, with support for the previous ?page=2 address.
p=Path('evidence/library/science/index.html');s=BeautifulSoup(p.read_text(),'html.parser')
if not s.select_one('[data-science-feed]'):
    feed=s.select_one('.knowledge-card');cards=[e.extract() for e in list(feed.select('article.paper-card'))]
    assert len(cards)>=8,len(cards)
    for card in cards:
        h=card.find('h3');a=next((a for a in card.select('.paper-links a[href]') if a['href'].startswith('/')),None)
        if a and not h.find('a'):
            t=text(h);h.clear();link=s.new_tag('a',href=a['href']);link.string=t;h.append(link)
    total=len(cards);size=6;pages=(total+size-1)//size
    feed['data-science-feed']='';feed['data-pages']=str(pages)
    grid=s.new_tag('div',attrs={'class':'science-cards'});feed.append(grid)
    template=s.new_tag('template',id='science-all-articles')
    for card in cards:template.append(deepcopy(card))
    feed.append(template)
    tools=fragment('<div class="science-feed-tools"><label>Search all featured analyses<input type="search" data-science-search placeholder="Topic, study, author or DOI"/></label><span class="science-feed-summary" data-science-status aria-live="polite"></span></div>').div
    grid.insert_before(tools)
    pager=s.new_tag('nav',attrs={'class':'science-feed-page','aria-label':'Scientific analysis pages'})
    for n in range(1,pages+1):
        a=s.new_tag('a',href=DIR if n==1 else DIR+'page/'+str(n)+'/');a.string='Page '+str(n);a['data-page']=str(n);pager.append(a)
    grid.insert_after(pager)
    snapshots=[]
    for n in range(1,pages+1):
        page=BeautifulSoup(str(s),'html.parser');pagefeed=page.select_one('[data-science-feed]');pagegrid=page.select_one('.science-cards');selected=cards[(n-1)*size:n*size]
        for card in selected:pagegrid.append(deepcopy(card))
        status=f'{(n-1)*size+1}–{min(n*size,total)} of {total} featured analyses'
        pagefeed['data-status']=status;page.select_one('[data-science-status]').string=status
        page.select_one('.science-feed-page [data-page="'+str(n)+'"]')['aria-current']='page'
        url=BASE+DIR+('' if n==1 else 'page/'+str(n)+'/')
        if n>1:
            title='Oxygen Delivery Research — Page '+str(n)+' | BHOC Science';page.title.string=title
            desc='Page '+str(n)+' of BHOC scientific analyses: prehospital transfusion, tissue oxygenation, oxygen delivery potency, nitric oxide and microcirculation research.'
            meta(page,'description',desc);meta(page,'og:description',desc,True);meta(page,'twitter:description',desc)
            meta(page,'og:title',title,True);meta(page,'twitter:title',title);meta(page,'og:url',url,True)
            page.head.select_one('link[rel=canonical]')['href']=url
            normalize_schema(page,url,title,desc,DATA['index.html'][2],True)
            page.h1.append(' — Page '+str(n))
        structured(page,'science-featured-schema',{'@context':'https://schema.org','@type':'ItemList','@id':url+'#featured','name':'Featured scientific analyses','numberOfItems':len(selected),'itemListElement':[{'@type':'ListItem','position':(n-1)*size+i+1,'name':text(c.h3),'url':BASE+c.h3.a['href']} for i,c in enumerate(selected) if c.h3.a]})
        destination=p if n==1 else p.parent/'page'/str(n)/'index.html';destination.parent.mkdir(parents=True,exist_ok=True);destination.write_text(serialized(page)+'\n');snapshots.append((str(destination),url))
    report.append({'pagination':snapshots,'featured_articles':total,'page_size':size})

Path('evidence/library/assets/science-20261103.css').parent.mkdir(parents=True,exist_ok=True)
Path('evidence/library/assets/science-20261103.css').write_text(CSS.strip()+'\n')
Path('evidence/library/assets/science-20261103.js').write_text(JS.strip()+'\n')
urls={BASE+DIR if p.name=='index.html' else BASE+'/'+str(p) for p in paths};urls.add(BASE+DIR+'page/2/')
for sitemap in [Path('sitemap.xml'),Path('evidence/library/sitemap.xml')]:
    if not sitemap.exists():continue
    source=sitemap.read_text()
    for url in urls:
        pattern=r'<url>\s*<loc>'+re.escape(url)+r'</loc>[\s\S]*?</url>';m=re.search(pattern,source)
        if m:
            old=m.group(0);new=re.sub(r'<lastmod>.*?</lastmod>','<lastmod>'+DATE+'</lastmod>',old)
            if '<lastmod>' not in new:new=new.replace('</url>','<lastmod>'+DATE+'</lastmod></url>')
            source=source.replace(old,new,1)
        elif url.endswith('/page/2/'):
            source=source.replace('</urlset>','<url><loc>'+url+'</loc><lastmod>'+DATE+'</lastmod></url>\n</urlset>')
    sitemap.write_text(source)
report_path=Path('/tmp/bhoc-science/change-report.json');report_path.parent.mkdir(parents=True,exist_ok=True);report_path.write_text(json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps(report,indent=2,ensure_ascii=False))
