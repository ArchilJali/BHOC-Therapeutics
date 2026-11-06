# BHOC Therapeutics — Post-publication SEO/AEO check (6 November 2026)

**Status:** reviewed technical evidence; editorial recommendations only. **Production edits:** 0. **Authority:** approved SEO master and page-intent map in `main`; this file is a research note, not a replacement master. **Public source commit:** `b299ac69c2855390d798c666a1356467ecab3af8` (6 Nov 2026, 06:53:38 UTC). The preservation rules of `AGENTS.md` remain in force.

## Fresh, executed full-sitemap verification

- GitHub Actions run [42180466487](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42180466487), successful, 2026-11-06T07:22:42.817567Z. Existing read-only full-sitemap workflow updated to trigger on substantive `seo-bot/**` preview changes; it writes no public pages.
- Root sitemap: **80 page URLs**. Evidence-library sitemap: **68 page URLs**. **12 overlaps; 136 unique canonical URLs** after deduplication. The **two additional URLs** relative to the actual 4 November 134-page artifact are **the sickle-cell compatibility evidence brief and /privacy/**. The blood-groups-history route was already in the baseline and was materially **updated**, not newly introduced. `image:loc` does not count as a page.
- **136/136 HTTP 200**, and no detected missing title/description, mismatched canonical, non-single H1, invalid JSON-LD, unintended generic `noindex` or duplicate title/description groups. HTTP and HTML checks do **not** prove Google indexing, AEO citation, search position, rich-result eligibility, or Core Web Vitals.
- Two pages lack JSON-LD blocks: `/evidence/library/catalogues/methodology.html` and `/privacy/`. This is a non-critical enhancement consideration, **not** proof of an SEO failure.
- Connected Windsor Search Console exposes only Evidence Platform and Vet properties, **not** the Therapeutics domain; consequently `google_index_verified=null` for newly reviewed pages. Existing Yandex-specific `noindex` policy remains unchanged.
- The read-only full-sitemap workflow does **not** visually inspect or verify ALT wording across all pages. It does not inspect PDF contents or check every external document destination. Carry forward prior dated image-attribute baseline, not a claim that ALT review is complete.

## New evidence brief and updated blood-group guide

| Route | Intended user question | HTTP | Title / description / H1 / canonical | Structured data | Image ALT |
|---|---|---|---|---|---|
| `/evidence/library/clinical/sickle-cell-transfusion-compatibility.html` | Why can red-cell antigen mismatches persist for repeatedly transfused people with sickle cell disease? | 200 | Present and self-referential; one H1 | JSON-LD present, valid syntax | No `img` elements; **not applicable** |
| `/evidence/library/real-world-evidence/blood-groups-history/` | What do the 49 blood-group systems mean for red-cell compatibility, and how do blood components differ? | 200 | Present and self-referential; one H1 | JSON-LD present, valid syntax | No `img` elements; **not applicable** |

Both pages are included in the latest evidence sitemap and have contextual internal links. The compatibility article contains the additional link to the new English-language blood-group reference; the definition hub also links to the reference. Do not duplicate scientific text in a new SEO page.

The clinical study cited by the new sickle cell brief, DOI **10.1016/j.brci.2026.100059**, was screened against the live owner Source Guard on 6 November: **no owner-stop match** found for the verified seven-author record. This is only a source-eligibility screen, **not** an assessment of scientific validity or proof of BHOC benefit.

## Other new URL: Privacy Notice

The second newly sitemap-listed URL, **/privacy/**, returned HTTP 200 with a unique title and description, self-canonical, one H1, and a truthful sitemap `lastmod=2026-11-05`. It has no JSON-LD, which is optional for a privacy notice. It should not be confused with a scientific/news page or pushed into an Article schema. No Google-indexing status was verified.

## Specific new issue: stale sitemap lastmod after a material update

The blood-groups-history page was materially changed in [main commit b299ac69](https://github.com/ArchilJali/BHOC-Therapeutics/commit/b299ac69c2855390d798c666a1356467ecab3af8) on **6 November**, including a newly linked four-page reference PDF and additional explanation. Yet the audited **library sitemap still reports `<lastmod>2026-09-12</lastmod>`** for that page. The newly added sickle cell article appropriately reports `2026-11-06`.

**Proposed fix (not applied):** in the authoritative sitemap-generation source for `/evidence/library/sitemap.xml`, set blood-groups-history `lastmod` to **2026-11-06**, reflecting the material content change. Preserve the historical release date **August 2026** in the page body; do not conflate data release date with webpage modification. Validate the generated sitemap and the deployed URL after owner-authorized publication. Do not hand-edit an evidence mirror if it has an upstream canonical generator. The reference PDF is present in the repository commit; its live delivery and its detailed text were not separately validated in this SEO run.

ISBT date-context check: the official [ISBT Working Party](https://www.isbtweb.org/isbt-working-parties/rcibgt.html) presents 49 systems and 400 antigens in its dated working-party figures. The live [ISBT registry](https://blooddatabase.isbtweb.org/database) displays 49 systems and 401 antigen records in the fetched listing. The BHOC article correctly distinguishes a **dated release count** from the evolving registry. Do not silently replace dated historical numbers.

## Bounded AEO improvement to prepare, not yet approved

1. On the existing compatibility page, retain the measured cohort figures, limitations, source/DOI and distinctions between donor-antigen exposure and patient clinical outcomes. One concise reader answer near the heading may explicitly distinguish **ABO/RhD compatibility**, broader red-cell antigen matching and subsequent alloimmunization risk. No promise that an investigational oxygen carrier solves that risk.
2. On the blood-groups-history page, keep a clearly dated one-sentence explanation of why **RBC antigen groups** are not the same concept as leukocyte HLA, platelet HPA/HLA or plasma compatibility. The current four-page educational PDF is the deeper reference; no separate thin landing page.
3. Link the two pages contextually from their relevant scientific/evidence hubs, only where an actual reader question warrants it. Keep one canonical owner per intent. Review any surrounding claims against source guard and approved content before a publish request.
4. Do not add decorative photos solely to fill an ALT counter. Text-only reference pages correctly have image-ALT status `not_applicable`.

## Existing UX-01 queue preserved

Homepage first-viewport implementation brief is already present at `seo-bot/UX-01-first-viewport-implementation.md`. **Do not patch `index.html` / `homepage.css` in this stale preview blindly**: the preview is now **13 main commits behind and 12 commits ahead**, as measured on 6 Nov, with more recent live navigation, SCD and blood-group work. Preserve those main changes and reconcile the branch before any DOM/CSS implementation. The dated mobile H1 position from 4 Nov is a lab snapshot, not a fresh 6 Nov conversion measurement. The next UX work remains prototype, accessible visual comparisons and required preservation checks before any owner-authorized merge.

## Next non-publishing steps

- Keep this evidence-backed `lastmod` discrepancy in the pending site-maintenance queue.
- Obtain an authoritative Google Search Console view for the main domain to distinguish discovered/crawled/indexed states; do not substitute `site:` search as an exact measure.
- In a future approved preview, test UX-01 against current `main` (390×844, 320×700, tablet, desktop), preserving all copy/images/anchors. Existing `assets/ga4.js` has a blank Measurement ID; do not invent one or submit contact forms.
