# 11 November 2026 — fresh-main UX-01 source patch verification and SEO coverage

**Status:** Source patch tested successfully in an ephemeral GitHub Actions checkout of `main`; **not committed to the public website or to the divergent preview HTML/CSS**. Owner approval remains necessary before any production merge. No other BHOC bots or master SEO files changed.

## Verified inputs and scope

- Current `main` SHA during test: `bd2f3d9c3495d3e929ad24038075d77fb446a920`. Existing preview branch was divergent by 28/22 commits at the start of this cycle; do not copy its stale `index.html` or `homepage.css` over current main.
- Full read-only audit: [GitHub Actions 42977703295](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42977703295). Two sitemaps: 81 root + 68 library, **137 unique pages**, 137 HTTP 200. No missing titles, meta descriptions, canonical mismatches, non-single H1, invalid JSON-LD, Google noindex or duplicate metadata found. This is **one more live canonical page** than the 136 in the prior stored panel.
- Source/root audit: [GitHub Actions 42977703346](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42977703346): 81 root URLs HTTP 200; 163 source HTML files; no unresolved internal source targets or missing ALT attributes observed.
- Full UX and **actual source-patch test**: [GitHub Actions 42977767950](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42977767950), artifact `bhoc-therapeutics-seo-ux-review`, folder `ux01-source-patch/`. Both isolated prototype and real temporary source modification passed. Fourteen regular visual checks found no overflow, broken images or broken internal anchors.

## New page reconciled

- `https://bhoctherapeutics.com/news/scotland-blood-amber-alert-2026/`
- Title: `Scotland’s Blood Amber Alert and PBM | BHOC News`
- H1: `Scotland’s Blood Amber Alert and the Case for Upgrading the Blood System`
- A dated page in the current /news/ index; HTTP 200 and self-canonical at 2026-11-11T07:12:47Z. One image with ALT and intrinsic dimensions present; two syntactically valid JSON-LD blocks. Generic robots index,follow; Yandex-specific noindex. Keyword/ALT visual quality and exact Google indexing still unverified. This is a **newly audited page**, not a new page created by the SEO bot.

## First actual source-patch test

A dedicated test script `seo-bot/ux01_source_patch_check.py` runs only in an isolated disposable checkout of **fresh main**. It adds one `Discuss research collaboration` text link after the existing Science and Technology actions in the homepage hero, and minimal responsive CSS, then saves a unified diff and before/after screenshots in the GitHub Actions artifact. It **does not write those HTML/CSS changes to GitHub**. Source screenshots and test data are reproducible in the run linked above.

| Viewport | Research link bottom | Viewport height | Outcome |
|---|---:|---:|---|
| 320 × 700 | 678 px | 700 px | 22 px remaining; passes source-patch lab test; actual browser chrome still relevant |
| 390 × 844 | 636 px | 844 px | Visible on first screen |
| 768 × 1024 | 1233 px | 1024 px | Below fold |
| 1440 × 1000 | 1033 px | 1000 px | Below fold |

**All four repository preservation checks passed:** `check_bhoc_content.mjs`, `check_site.mjs`, `node --check navigation-context.js`, and `git diff --check`. The test also preserved one H1, existing image attributes, existing Science/Technology actions, all old anchor destinations and no horizontal overflow. It verified the linked **Contact** URL selects `Research collaboration` and displays `Topic: Oxygen delivery research`. **No form was submitted.**

This upgrades UX-01 from an isolated DOM-injection concept to a **passing temporary source-level change with reproducible patch and rendered screenshots**. It does not prove site speed, conversion, Google ranking, accessibility on every phone, or a completed/approved source merge.

## Candidate semantics — owner terminology update

Owner's working terminology on 11 Nov is **Patient Blood Management (PBM): a Function-Based Approach / Function-based PBM**, not a separate `PBFM` brand. Any candidate changes are research language only and should enrich the existing perioperative/PBM intent, not generate a duplicate doorway page. WHO's PBM guidance is a source for the established **PBM** framework, **not a WHO endorsement of the proposed function-based qualifier or of BHOC**. Do not cite it as BHOC efficacy evidence or override live Source Guard. Keywords are editorial candidates, not measured search queries.

Existing route for the intent: `/applications/#perioperative-oxygen-delivery`. Candidate reader question: **How does the clinical goal of oxygen delivery complement conventional PBM measures of anemia, blood loss and transfusion use?** No changes to existing public scientific wording have been made.

## Remaining limits and next action

Google Search Console data for `bhoctherapeutics.com` is still unavailable from the connected properties. HTTP 200 and inclusion in sitemap do not establish Google indexing, rankings, AI citations or Search Console impressions. The verified Yandex-specific noindex on 137 audited pages is not to be silently removed. ALT **attribute presence** is confirmed; exact visual accuracy of every image is not.

Next owner-reviewed implementation task: reconcile the fresh-main source diff from this successful run with the existing long-divergent preview branch, validate the resulting actual preview source again across 320/390/768/1440 breakpoints, and request explicit production approval before merging. Preserve all existing approved content and original links.

**Production changes by this SEO bot: 0.**
