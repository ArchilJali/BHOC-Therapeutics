# BHOC Therapeutics — dialysis/renal-anemia SEO/AEO research draft
**Review date:** 7 November 2026  
**Status:** substantive editorial brief and proposed *additive* copy; **not published, not approved for merge**  
**Site:** bhoctherapeutics.com; human/clinical research education only  
**Authority:** existing approved master at `main/seo/BHOC-SEO-Keywords.md` and page-intent map. This document adds proposals without changing either authority or the established clinical narrative.

## Why this is a distinct content gap

Checked `main` source on 7 November at SHA `f4a131789a321ff512414dc849238d42542ada28`; page `applications/severe-anemia-oxygen-delivery/index.html`, blob `98658f27a5b8003c0929794262eea0af8e181c98`.

Existing canonical target: https://bhoctherapeutics.com/applications/severe-anemia-oxygen-delivery/#renal-anemia. Existing title: **Severe Anemia and Oxygen-Delivery Evidence | BHOC**. Existing H1: **Severe anemia: the oxygen-delivery question**.

The current renal-anemia subsection contains two concise paragraphs distinguishing isolated-kidney perfusion, transplant-recipient anemia and long-term dialysis, and explicitly states that BHOC has *not* been established as a therapy for chronic renal anemia or as a dialysis replacement. Both adjacent links route to transplant-specific pages, not to foundational CKD-anemia education. This correctly sets boundaries but does not yet answer how renal anemia differs from oxygen saturation changes during dialysis, or what a scientific oxygen-delivery assessment would measure.

Do **not** create a new thin dialysis landing page, duplicate the transplant site, replace approved copy, or change the H1, canonical, metadata, old fragment ID or existing links. Do **not** change medical claims without clinical/editorial approval.

## New, deduplicated candidate questions

The following six editorial query candidates were compared literally with all **1,123 entries** in the existing panel on 7 November. None was an exact existing phrase; they are related intents for **one** existing human-use page, not six new pages, and have **unmeasured** search volume, KD or ranking.

| Candidate English query | Reader need | Proposed owner |
| --- | --- | --- |
| renal anemia versus intradialytic hypoxemia | Distinguish chronic blood oxygen-carrying capacity from a change in oxygenation during dialysis | Therapeutics · #renal-anemia |
| dialysis anemia versus oxygen saturation | Understand why Hb concentration and SpO2 are not equivalent measurements | Therapeutics · #renal-anemia |
| hemodialysis oxygen delivery research endpoints | Determine what measurements belong in an oxygen-delivery research question | Therapeutics · #renal-anemia |
| KDIGO 2026 anemia guideline dialysis oxygen transport | Place contemporary CKD-anemia guidance in context without implying approval of BHOC | Therapeutics · #renal-anemia |
| dialysis blood loss and renal anemia | Understand the multifactorial causes of CKD anemia | Therapeutics · #renal-anemia |
| renal anemia erythropoietin and oxygen transport | Explain the EPO–red-cell–oxygen-carrying relationship | Therapeutics · #renal-anemia |

These are **editorial candidates** motivated by verified institutional vocabulary, not actual measured Google queries. US/UK forms (anemia/anaemia, hemodialysis/haemodialysis) belong to the same intent. Do not add an independent page per spelling. Do not present these candidates as added to the approved master.

## Proposed AEO heading and draft, for scientific and owner review

Proposed placement: **inside the existing** `<section id="renal-anemia">`, *after* the two approved paragraphs and *before* the original link list. The draft below is not in the public page.

### How are anemia, oxygen saturation and dialysis different research questions?

Chronic kidney disease can reduce the production of erythropoietin, the hormone that supports red-cell formation. Iron availability, inflammation, shortened red-cell lifespan and blood loss can also contribute to anemia. Hemoglobin concentration describes an important part of blood oxygen-carrying capacity. Oxygen saturation is a different measurement: it describes the proportion of available hemoglobin binding sites occupied by oxygen, not the total hemoglobin mass or oxygen delivered to tissues.

When studying oxygen transport during hemodialysis, the research question should state which quantity is being assessed. Hemoglobin concentration, arterial oxygen saturation, blood flow, oxygen extraction and tissue-perfusion measurements describe different steps in the transport pathway. A change in one measure should not automatically be interpreted as a change in patient outcomes or as evidence that any particular oxygen-carrier formulation is effective.

The **KDIGO 2026 Clinical Practice Guideline for Anemia in Chronic Kidney Disease** covers people with CKD, including dialysis and transplant recipients. It is a clinical guideline on the management of anemia, **not evidence of BHOC efficacy, safety, approval or availability**. BHOC-related work in this area remains a research question requiring product-specific experiments, safety evaluation and appropriate clinical evidence.

### Suggested contextual references
- National Institute of Diabetes and Digestive and Kidney Diseases (NIDDK): https://www.niddk.nih.gov/health-information/kidney-disease/anemia — causal context of CKD-associated anemia; no statement on BHOC.
- Kidney Disease: Improving Global Outcomes (KDIGO), **2026** guideline overview: https://kdigo.org/guidelines/anemia-in-ckd/ — guideline scope and current publication status; no product endorsement.
- Internal already-published physiology: https://bhoctherapeutics.com/bhoc/circulation-vascular-control/ — systemic oxygen delivery, blood flow and oxygen content.
- Internal existing scope boundary: https://bhoctherapeutics.com/applications/severe-anemia-oxygen-delivery/#renal-anemia — approved renal-anemia paragraphs remain intact.

### Review and implementation restrictions

1. Check the exact institutional source wording and citation date before any public edit; source-screening was performed against the live BHOC Source Guard on 7 November, with no flagged KDIGO/NIDDK organizational or named-chair match. This is an eligibility check, **not** clinical validation.
2. Retain the current treatment boundary verbatim. The proposed text is informative and does not provide treatment thresholds, doses, individual treatment advice, product acquisition, administration or manufacturing instructions.
3. Keep existing title, meta description, canonical, H1 and JSON-LD. No automatic FAQPage schema: short questions in the visible text do not establish rich-result eligibility.
4. New image is **not needed**. No meaningful `img` in this proposed text; image ALT status is **not_applicable**, not a failure.
5. If approved, add the two institutional links as descriptive citations and the internal oxygen-physiology link, without displacing the existing two transplantation links.
6. Because `preview/therapeutics-web-seo-20261104` diverged from current `main` by 14 commits on each side as checked 7 November, do **not** paste this into its stale HTML source. Reconcile current main into an approved preview branch first and run preservation checks, link checks, visual comparison and `git diff --check`; production merge requires owner authorization.

## Adjacent hygiene confirmed today

A 6 November review had correctly identified an outdated `lastmod=2026-09-12` for the materially revised Blood Groups History guide. **It has now been corrected in current main**: `evidence/library/sitemap.xml`, blob `55f13b121e69b400f9a2150f781bb4d217d0c319`, lists `2026-11-06` for that URL. No new fix is necessary; report the earlier defect as resolved by a separate production update, **not as a bot publication**. This is a repository check, not proof of Google indexing.

Current `assets/ga4.js` still has a blank measurement ID; no tracking settings, consent or form submissions were modified. The existing Contact and Partners pages are intact. The user-facing mobile UX-01 brief remains unimplemented; no contradictory claim about a verified new screenshot should be made.

## Next safe action

After editorial and source review, prepare a branch-reconciled preview-only *additive* HTML patch to the renal-anemia section, retaining all approved text, IDs, and the existing transplants-specific references. A later run can verify desktop/mobile layout. **Production changes in this cycle: zero.**
