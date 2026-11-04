# BHOC Therapeutics — SEO and UX operating plan

Review date: 4 November 2026. Scope: https://bhoctherapeutics.com/ only.
This document is a review/prioritization layer, NOT a second keyword master and NOT permission to publish. Keep seo/BHOC-SEO-Keywords.md and seo/page-keyword-map.md authoritative. Read current AGENTS.md and seo-bot/RUNBOOK.md before work. Automatic main publication remains OFF. Preserve approved text, images, source destinations, protected baselines, access settings, and other bots.

## Verified baseline

Audit: https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/41812742704
Artifact: bhoc-therapeutics-seo-ux-review, ID 13313700759.
Audit version 1.1; checked 2026-11-04T10:14:18.250319+00:00.
Inspected main SHA: dc6b18acf9672d3362e07e6e9eda6006faaf5da1.

- Root sitemap: 78 page URLs. Library sitemap: 67. Deduplicated HTML pages: 134; all HTTP 200.
- No missing title/description, canonical mismatch, non-single H1, invalid JSON-LD, duplicate title/description groups, missing img alt attributes, missing img width/height attributes, or broken anchors among the checked sitemap targets were detected by this audit.
- All 134 inspected HTML documents contain a Yandex-specific noindex meta tag. Ordinary robots/Google noindex was not found in this sample. Do not change this policy automatically.
- Seven routes were rendered at 1440x1000 desktop and 390x844 mobile: /, /bhoc/, /science/, /applications/, /partners/, /contact/, /news/. Fourteen tests completed; no measured horizontal overflow or broken images in these samples.
- Four repository checks returned 0: check_bhoc_content.mjs; check_site.mjs; node --check navigation-context.js; git diff --check. These checked the recorded main source, not a redesigned page.
- Mobile homepage H1 starts at y=897; first main-content Science CTA starts at y=1177, below an 844px viewport. Desktop equivalents are y=568 and y=880. This is a hierarchy hypothesis to test, not a measured conversion loss. Navigation already contains a Partners link; do not claim it is absent.
- Homepage recent-news cards feature 26/25/21 October materials while /news/ includes a 1 November 2026 article. Preserve historical material and original dates; synchronize the recent-news selection.
- A contact form already exists. assets/ga4.js includes generate_lead and topic/campaign context but GA4_MEASUREMENT_ID is deliberately empty. GA4 initialization through this script is off. Ahrefs analytics is present separately. Do not claim the site has no analytics, invent a stream ID, or send a test enquiry without authorization.

Limitations: no field Core Web Vitals, Search Console indexing/positions/impressions/clicks, search volume/KD, conversion outcomes, backlink metrics, or AI mentions measured. This is not a clinical efficacy review. A successful HTTP/metadata audit is not proof of search visibility or rich-result eligibility.

The first exploratory UX run 41812044338 used a recursive loc selector that also counted image sitemap assets. Its 176-URL metadata totals are superseded by the corrected version 1.1 above. Image locations must never be classified as HTML-page defects. The valid desktop/mobile screenshots were independently reproduced in the corrected run.

## Candidate-map assessment

The dated research snapshot contains 957 distinct literal phrases: 821 assigned to Therapeutics, 118 to Transplant, 18 to Vet. Original sources: 489 retained master phrases and 468 editorial additions. These are not measured Google queries. All demand/performance fields remain null. Within the 821 Therapeutics phrases, 606 carry original P1, 181 P2, 34 P3. That is too broad an execution priority.

Use the following 48 already-recorded phrases in eight review groups as a first focus set, not 48 new articles. There are no newly discovered keywords in this prioritization pass. The proposal changes routing for eight selected phrases relative to the dated snapshot, but does not change the approved master/map. Group spelling variants and synonyms under the same intent. Broad words such as blood and oxygenation remain contextual vocabulary, not automatic new landing pages. Detailed Vet and Transplant work stays with those separate bots.

### 01 — Entity and definition
Target: /bhoc/ (Precision Oxygen Therapeutics category phrase belongs primarily to /).
Phrases: BHOC; Biological Hemoglobin Oxygen Carrier; what does BHOC mean; BHOC meaning in oxygen research; BHOC and HBOC terminology; Precision Oxygen Therapeutics.
Improve the overview-to-definition journey. Preserve /bhoc/definition/ as the deeper scope chapter, not a duplicate definition index.

### 02 — Technology and boundaries
Target: /technology/.
Phrases: cell-free hemoglobin oxygen carrier; hemoglobin oxygen carrier; hemoglobin-based oxygen carrier; hemoglobin outside red blood cells; cellular and acellular oxygen transport; BHOC technology.
Explain architecture, development status and source access. Do not turn historical product findings into current BHOC outcomes.

### 03 — Saturation, content and delivery
Target: /science/, with links to the appropriate existing detailed scientific pages.
Phrases: oxygen saturation versus oxygen content; oxygen saturation versus oxygen delivery; oxygen carrying capacity versus saturation; oxygen content and cardiac output; hemoglobin concentration versus tissue oxygen; functional oxygen delivery endpoints.
Check existing coverage before proposing another URL. Preserve the Nobel feature first. Educational explanations require scientific source review before publication.

### 04 — Hemoglobin and affinity
Target: /bhoc/hemoglobin/.
Phrases: P50 hemoglobin meaning; hemoglobin oxygen affinity explained; Bohr effect and oxygen unloading; Haldane effect explained; oxygen loading versus unloading; oxygen affinity versus oxygen delivery.
Prepare short sourced answers and contextual links, not separate US/UK spelling pages.

### 05 — Anemia and oxygen transport
Target: /applications/severe-anemia-oxygen-delivery/.
Phrases: oxygen delivery in anemia; anemia versus hypoxemia; normal oxygen saturation with anemia; oxygen-carrying capacity in anemia; acute versus chronic anemia oxygen delivery; anemia research functional endpoints.
Deepen the existing educational page. No individualized treatment, acquisition, dosing or administration guidance.

### 06 — EMS research
Evidence target: /evidence/library/clinical/prehospital-ems.html.
Phrases: prehospital oxygen delivery; EMS blood program logistics; HEMS blood availability; rural EMS blood access; EMS and blood bank collaboration; prehospital oxygen delivery research.
Strengthen corporate Applications-to-evidence and relevant News links. Do not edit the mirrored evidence page as the authoritative source. Keep medical logistics separate from tactical operations.

### 07 — Availability and logistics
Target: /applications/donor-blood-availability/; military/disaster medical logistics stays at /applications/military-disaster-medicine/.
Phrases: blood shortage causes; hospital blood supply resilience; blood availability in rural hospitals; blood cold chain logistics; blood product transport vibration research; last mile blood delivery.
Link existing permanent explanations and dated source-linked news. Do not create thin pages for every logistics synonym.

### 08 — Research collaboration
Target: /partners/.
Phrases: BHOC research partnership; oxygen transport research collaboration; precision oxygen therapeutics research partners; translational oxygen research collaboration; biotechnology research partnership; institutional oxygen research collaboration.
Clarify research questions, partner contribution and the next step through the existing contact form. Do not imply immediate access to a portal described as still being prepared.

## Execution queue

| ID | Priority | Recorded status | Next action and completion condition |
|---|---|---|---|
| UX-01 | P1 | Brief prepared | Prepare a bounded first-screen preview with definition and two clear actions visible at 390x844. Preserve all approved text and assets. Any reordering needs owner approval before production. Capture desktop/mobile and run preservation checks. |
| SEM-01 | P1 | Focus set selected | Reconcile the eight groups with the actual master and current routing before any edits; do not confuse editorial priority with volume/KD. |
| MEAS-01 | P1 | Verified data source needed | Inspect an existing authorized GA4/Search Console source if available; verify real event delivery and appropriate analytics settings. Do not change billing, permissions, consent settings or invent IDs. Do not send contact names, email, organization or message contents to analytics. |
| CONTENT-01 | P2 | Proposed | Derive homepage latest-news cards from one actually-published news list; keep dates and historical items intact. |
| TRUST-01 | P2 | Editorial review needed | Propose nearby labels for development objective, historical evidence, preprint or hypothesis. Keep product/species/evidence scope explicit. No automatic rewriting of approved claims. |
| UX-02 | P2 | Brief prepared | Clarify Partners CTA as a research conversation via the existing form; no promise of immediate access to an unfinished portal. |
| NAV-01 | P2 | Proposed | Test definition -> specific reader question -> evidence -> contact paths. Preserve all routes, accessibility and old anchors; simplify duplicate navigation only through reviewed preview. |
| TECH-01 | P2 | Unmeasured | Obtain actual field or separately labeled lab performance evidence before image/font/CSS optimizations. No invented PageSpeed or CWV score. |
| POLICY-01 | P2 | Owner decision | Confirm whether Yandex exclusion is intentional. Do not remove the directive automatically or treat it as Google exclusion. |
| BOT-01 | P2 | Runner configured | Maintain this independent queue, dated runs and honest statuses. No duplicate scheduler, native Sites claim, or changes to Vet/Transplant/Social/AIO. |

## Prepared homepage brief — not implemented

Goal: help a new research visitor understand the entity and reach the right evidence or collaboration path in the first viewport.
Keep the approved existing main headline and all longer explanatory material. Test its placement alongside a concise entity label and smaller supporting image, without deleting content. Proposed additional neutral supporting sentence: “Explore the science, evidence and research questions behind cell-free hemoglobin-based oxygen delivery.” Proposed action labels: “Explore the evidence” and “Discuss research collaboration”. Link to existing /evidence/ and /contact/ routes with existing topic handling where appropriate. Current research/development status should be clear near the relevant statement; scientific wording requires source/owner review.
No new page, new medical claim, public copy change or production deployment has occurred in this review.

## Repeating work

Read current main rules/master/map, RUNBOOK, this plan and recorded task history. Complete or advance one useful queue item, saving a real draft or bounded proposal, not just another recommendation list. Research additional phrases only where an actual unanswered reader question is identified; 5–15 candidates is an optional ceiling, not a quota. Never manufacture search metrics or article demand.

The read-only visual workflow is .github/workflows/therapeutics-ux-review.yml; runner seo-bot/ux_review.py. It checks current main and live pages, not preview website modifications. Request fresh visual inspection after a relevant live change or for a useful periodic review, normally weekly; do not produce empty commits merely to simulate activity. Use the latest actual run and artifact. A meaningful seo-bot/UX-REQUEST.md describing the changed page/question can trigger it on this branch. Keep direct url/loc sitemap parsing, distinct visible-shell inspection, source SHA, timestamp and limitations.

Use fresh file SHA/branch concurrency protection. Save actual status transitions and source references, without private business records or stop-list identities in this public repository. Research, draft, preview, approved and published are distinct statuses. Only separately authorized, verified deployment could ever be called published. Keep ordinary no-change runs quiet; report meaningful new findings or a concrete blocker in Russian.

## Primary SEO guidance consulted

- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- https://developers.google.com/search/docs/crawling-indexing/special-tags
- https://developers.google.com/search/docs/fundamentals/get-started-developers

Google's guidance favors helpful original content and crawlable, logical structure. A larger meta-keywords list does not improve Google indexing or ranking. Do not produce mass content solely to fill keyword coverage.
