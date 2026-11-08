# 8 November 2026 — live SEO, mobile-first-viewport and collaboration-path reassessment

**Status:** verified **read-only** measurements, with a narrow unapproved CTA proposal.  
**Scope:** BHOC Therapeutics only. **Public changes by this bot: 0. New unique keyword candidates: 0.**  
**Source `main` SHA:** `c15a70b456786d99eb54da70fc8c83892f1d0400` (2026-11-08 06:41 UTC).  
**Trigger:** the separately merged PR [#99](https://github.com/ArchilJali/BHOC-Therapeutics/pull/99), `Fix mobile homepage overflow and reading order` (2026-11-08 06:41 UTC), and its successful Pages deployment. This is not an SEO-bot publication.  
**Checked:** 2026-11-08 07:46–07:47 UTC.

## Evidence: fresh live audits

- [Read-only root sitemap + source audit, run 42460157380](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42460157380), checked 07:46:41 UTC, main SHA above: **80/80** public root-sitemap pages HTTP 200; no flagged missing title/description, canonical count, H1 count, JSON-LD syntax or noindex-in-sitemap; no duplicate title/description groups; **162** source HTML files; zero unresolved source-internal links; zero pages with images missing an ALT attribute. Exactly two root-sitemap pages without optional JSON-LD; not a critical error.
- [Read-only both-sitemap audit, run 42460157402](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42460157402), checked 07:46:40 UTC: **80 + 68 sitemap URL entries**, deduplicated to **136 canonical intended pages**; **136/136 HTTP 200**; no reported metadata, canonical, H1-count, syntax, noindex or duplicate-title/description issues. JSON-LD is absent on the methodology and privacy pages; structured data is optional there.
- [Fresh rendered desktop/mobile + SEO audit, run 42460157401](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42460157401), checked from 07:47 UTC: **136/136 HTTP 200**, **14 successful screenshot/viewport tests** over the same seven routes at desktop **1440×1000** and mobile **390×844**. No measured horizontal overflow, broken image, missing ALT attribute, missing intrinsic image dimensions or broken in-page fragment in this sample. **Yandex-specific noindex remains on all 136 checked pages**; do not remove. There is no corresponding generic/Google noindex detected in this sample.

Audit evidence includes screenshots `screenshots/home-mobile-top.png`, `screenshots/partners-mobile-top.png`, `screenshots/contact-mobile-top.png` in the run artifact, plus `visual.json` and `summary.json`.

### UX-01 before versus after — concrete change

| Measurement | 4 Nov baseline | 8 Nov after PR #99 | Interpretation |
| --- | ---: | ---: | --- |
| Mobile homepage H1 top (390×844) | y=897 px | **y=185 px** | The H1 is now visible in the first viewport; this part of UX-01 is **observed improved by PR #99**, not by this bot. |
| Mobile homepage H1 bottom | not separately retained in task baseline | **y=289 px** | Full main heading is visible. |
| First two homepage education actions | first Science CTA y=1177 px in prior audit | **Science y=481–527; Technology y=539–585** | Both usable 46px-tall actions are now above the 844px fold. |
| Mobile horizontal overflow | none reported on 4 Nov | **none, scrollWidth=390** | No new overflow observed. |
| Immediate research-collaboration action | not above fold | **not above fold**; hero Partners action at y=922–966 | Remaining UX-01/UX-02 opportunity; no measured conversion loss or SEO penalty assumed. |
| Desktop H1 | y=568 in old baseline | **y=626** | Desktop appearance shifted; inspect design, don't automatically treat later position as a defect. |

The mobile screenshot confirms the H1, Precision Oxygen Therapeutics definition, Science and Technology links, and start of the retained mission block are visibly readable. Mobile `/partners/` displays its title, a red `Request authorized access` link and Evidence Platform link. Mobile `/contact/` shows the actual research/partner message form with Name, Email, Organisation and Area of interest fields; **the form already exists**. No form was submitted.

## SEO/AEO/ALT and crawlability conclusions

1. **SEO technical baseline still healthy** across all 136 sitemap pages. No claim that each was indexed or ranking. This is an audit of served HTML and selected rendered layouts, not Search Console URL Inspection or field Core Web Vitals.
2. **AEO**: mobile first-viewport explanation is now easier to find; the existing path `BHOC definition → Science/Technology → Evidence → Contact` is discoverable. This audit does not establish comprehensive editorial AEO review, answer quality in all 136 pages or generative-search citation.
3. **ALT**: missing ALT attributes were not detected, but **semantic/visual accuracy of all 74+ image occurrences has not been individually inspected**. Only screenshot appearance on selected seven routes was observed. No new alt claims or image replacements.
4. **Indexing**: Google Search Console property for `bhoctherapeutics.com` remains unavailable through current linked Windsor sources; the exposed properties are Evidence Platform and bhocvet.com. Actual Google indexing = **unknown**, not 136/136. No search volume, KD, rankings, clicks, conversions or AI mentions were verified.
5. **Yandex**: Yandex-specific `noindex` remains an explicit owner-policy decision; none was removed.
6. **News freshness**: homepage visually features older dated items while the news hub has a newer 1 Nov 2026 item. This is a **selection/editorial review**, not an automatic error: keep original source dates and do not reorder without content review. The homepage sitemap `lastmod` and displayed update date may also merit reconciliation after identifying materially updated content, but **do not automatically overwrite lastmod for cosmetic changes**.

## Narrow next change proposal — preview only

**UX-01 partially resolved**: H1 and two educational links are now in the first viewport. Do **not** apply the obsolete 5 Nov wholesale mobile DOM-reordering proposal: PR #99 already changed the live source. Remaining objective is a clearer research-collaboration route without changing product claims or hiding current links.

**Proposal A (preferred for evaluation):** In the current mobile hero, retain both Science and Technology buttons unchanged, and **test** a small tertiary link `Discuss research collaboration` to `/contact/?topic=oxygen-delivery-research`, near the existing two actions. The current `assets/ga4.js` recognizes this topic for the form; its `GA4_MEASUREMENT_ID` is blank and no tracking should be activated. Check whether the third link fits at 390×844 and 320×700 without reducing legibility or hiding other content. **No source patch has been made.**

**Proposal B:** Retain current hero and feature the research link at the existing Partners card/context, strengthening anchor wording and links; use this if adding a third first-viewport control worsens mobile hierarchy. Verify the real form route and do not promise direct access to an unfinished partner portal.

**Acceptance:** owner editorial approval for a preview-only patch, source/DOM comparison against `main` at its then-current SHA, screenshot & keyboard checks, and `check_bhoc_content`, `check_site`, `node --check navigation-context.js`, `git diff --check`. No merge without explicit authorization.

## Research topics and status

Heart/cardiac surgery, complex surgery, dialysis, anaesthesia/anesthesia, emergency, prehospital/HEMS and battlefield medical logistics remain in the existing `OWNER-PRIORITIES-20261104.md` queue. Six renal-anemia/dialysis candidates added 7 Nov remain valid; **no distinct new candidate was discovered or added on 8 Nov**, and no duplicate search terms were counted as progress. No clinical or veterinary efficacy interpretation was added in this technical review.

## Preservation and next checkpoint

- Existing scientific text, source destinations, News items, original images, ALT and all `main` files: unchanged by this bot.
- `preview/therapeutics-web-seo-20261104` contains only a new audit request and this dated review; its HTML/CSS **must not** be merged over newer production changes.
- Production changes by this bot: **0**. Vet, Transplant, Social Desk, AIO, permissions and billing untouched.
- Next highest-value task: after checking owner's current UX/content choice, prepare a bounded current-main-based preview patch for the collaboration link, or move to editorial News freshness review without editing already approved text.
