# 9 November 2026 — post-PR #104 SEO / AEO / mobile reader-path review

**Site:** https://bhoctherapeutics.com/  
**Status:** verified read-only audit + an additive, unapproved UX/AEO proposal. **No public changes by this bot.**  
**Main SHA audited:** `62b8869d7edcd15f9b2fafd93ef0f3b377668397` (merged direct Applications reading, PR #104).  
**Audit date:** 2026-11-09, approximately 08:47–08:49 UTC.  
**Previous baseline:** 8 Nov (136 pages and mobile H1 y=185 after PR #99). Do not describe the previous baseline as today's result.

## Verified current GitHub Actions results

| Run | Actual scope and result |
|---|---|
| [42588496681](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42588496681) | Read-only main-source + root-sitemap audit, **80/80 HTTP 200**; **162** source HTML files; zero unresolved source-internal links, missing title/description, problematic H1/canonical counts, invalid JSON-LD syntax, duplicate title/description groups, or missing HTML img ALT attributes. Two pages have no optional JSON-LD. |
| [42588496491](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42588496491) | Both actual sitemaps: **80 root + 68 library URL entries, 136 unique page URLs** after overlap; **136/136 HTTP 200**, zero flagged metadata/canonical/H1/JSON-LD/noindex or duplicate-title/description issues. Methodology and privacy have no optional JSON-LD. |
| [42588496511](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42588496511) | Fresh rendered 390×844 and 1440×1000 checks of the seven established URLs; **14 tests, zero runner visual errors, zero measured horizontal overflow or broken images**, **0 reported broken internal anchors**; all four repository checks exit 0. 136/136 pages HTTP 200; Yandex-specific noindex on all 136. |

These are separate read-only reports on published HTML and current-main source, **not** a preview-patch test, Search Console inspection, an ALT semantic-quality proof or a Core Web Vitals / conversion study.

## Measured reader-path state after #104

| Page (mobile 390×844) | Measured H1 top/bottom | Relevant actions or forms |
|---|---|---|
| `/` | **185–289 px** | Science at **481–527**, Technology at **539–585**; existing **Investors & Partners at 922–966**, below first 844px viewport. No first-viewport research-specific action in the verified hero. |
| `/applications/` | **236–377 px** | PR #104's direct clinical-reading route is in place. Existing **"Discuss a research question"** action points to the appropriate research contact topic but is at **7719–7767 px** in this long mobile document. It exists, but is not an initial reader action. |
| `/partners/` | **290–519 px** | First visible main action **"Request authorized access"** at **660–708**. This leads to an enquiry about the **future** protected Business Portal, not directly to the research-topic form. Distinct investor/clinical/manufacturing routes exist lower in the page. |
| `/contact/` | **282–369 px** | The existing form is present (11 elements in rendered audit). The Area of interest select includes "Research collaboration"; no form submitted. |
| `/news/` | **285–334 px** | Current News index is crawlable and working; homepage feature cards still highlight older dated materials, which is an editorial selection to review, not a ranking error. |

**Confirmed source-side route mapping:** `assets/ga4.js` at main blob `468bb559584bbd28bd6debdc9107423c34979f3a` handles `topic=oxygen-delivery-research` (visible topic text) and `interest=research` (Research collaboration selected). The GA4 Measurement ID is **empty**. We did not test actual form submission or analytics delivery, and do not propose sending personal fields to analytics. Source `index.html` blob `f6b6fbb3d7061336018def8d6c0405696c9d22dd` preserves Science and Technology buttons in the hero.

## Specific new UX/AEO decision point

**The research route exists but requires discovery.** The post-#104 Applications update did not remove it; the independent mobile reader path shows it deep in the document. On Partners, an **access-request** CTA may be mistaken for the appropriate first step by a clinical or university research visitor. There is **no measured conversion loss** and no evidence that Google penalizes this arrangement.

**Preferred narrow experiment (preview only; not coded here):** preserve every existing hero control, approved sentence, picture, source link, anchor and old URL. Add one non-promotional tertiary text action directly after the existing two actions in `.hero-copy`:

```html
<a class="hero-research-link" href="/contact/?interest=research&amp;topic=oxygen-delivery-research">Discuss research collaboration →</a>
```

Keep it semantic and keyboard accessible, with a practical 44px touch target; test whether it remains visible and legible at **390×844** and **320×700** without pushing the existing two buttons out of the first viewport. The current runner verifies 390×844 and 1440×1000 only; **320×700 and keyboard traversal are not yet measured**. If the third action crowds the hero, reject it rather than shrinking approved content.

**Alternative if the mobile hero test fails:** strengthen the already-existing Partners clinical-research context with an explicit and accurate AEO answer without changing the "request authorized access" function:

> **How can a research institution discuss collaboration?**  
> Clinical and academic research teams can use the existing BHOC contact form to outline their organisation, the specific oxygen-delivery research question and the proposed scientific collaboration. This is an enquiry pathway, not access to a treatment or a currently operating confidential portal.

Link that answer to `/contact/?interest=research&topic=oxygen-delivery-research`, in the relevant clinical/scientific context. Do not imply active clinical approval, treatment access or an effective investigational product. Scientific and commercial assertions are unchanged.

**Preservation and release gates:** New HTML/CSS patch, if separately approved for preview, must be based on **current main**, not a wholesale copy of the diverged SEO preview branch. Verify one H1, all original URLs/anchors, img ALT/size, mobile and desktop appearance, forms not submitted and the four mandated preservation checks. Do not merge to main without separate owner authorization and verified deployment.

## SEO, AEO, ALT, indexability and semantic scope

- **Technical SEO:** no new flagged root/full sitemap error as of this check. The `/applications/` sitemap `lastmod` is `2026-11-08`, consistent with the recent substantive change; `/partners/` remains `2026-09-10`. Do not adjust lastmod without confirming a real content update.
- **AEO:** this review validates one actual reader-path question, not all 136 page answers. The specific improvement is distinguishing **research collaboration** from **future portal-access requests**, using clear text that matches existing form behavior.
- **ALT:** every audited HTML `img` has an ALT attribute, but not every image/ALT pair was visually checked. Do not mark that separate task complete.
- **Indexing:** Google Search Console's **Therapeutics** property is not present in today's connected Windsor sources (only Evidence Platform and Vet). Actual indexed URLs, position, impressions, clicks and AI citations remain **unknown**; 136 HTTP200 is not 136 indexed pages. Yandex-specific noindex is retained on all 136 and not interpreted as generic/Google noindex.
- **Semantic research:** initial owner priorities (cardiac/complex surgery, dialysis, anesthesia, emergency, prehospital and medical battlefield logistics) remain assigned in `seo-bot/OWNER-PRIORITIES-20261104.md`. This is a UX/technical validation cycle; **new unique keyword candidates = 0**. Do not count existing 1129 keywords again.
- **Source Guard:** live policy checked prior to any new scientific interpretation. This review contains no new external clinical efficacy claims or new evidentiary publication, and none is added to the approved master.

## Next action

After owner review of the two options, test the smallest collaboration-link change **against a fresh copy of current main** in the authorized preview workflow; obtain real 390×844, 320×700, keyboard and form-topic screenshots/readback without submitting a form. Meanwhile maintain the existing SCD and other clinical reading paths from PR #104. No changes to Vet, Transplant, Social Desk, AIO, billing, tracking, credentials or main.
