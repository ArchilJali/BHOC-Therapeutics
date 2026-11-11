# 11 November 2026 — homepage News freshness and AEO routing review

**Status:** Verified content gap and prepared one bounded, nonpublishing homepage content proposal. This is a CONTENT-01 task artifact on the existing `preview/therapeutics-web-seo-20261104` branch, not a published HTML/CSS edit, a change to approved science, or a new automation.

## Evidence actually inspected

- Current public `main` commit: `bd2f3d9c3495d3e929ad24038075d77fb446a920` (10 Nov 2026). Current `index.html` blob `f6b6fbb3d7061336018def8d6c0405696c9d22dd`; `news/index.html` blob `d711f7f55d4275fef0adeb49eab9d43593578`.
- The homepage `<section id="news">` still leads with 26 October (Carl W. Rausch tribute), then 25 October (1996 tissue oxygenation), 21 October (hemoglobin-dose preprint), then an older introductory preprint. Each is valuable and must remain available. The generic CTA wording `Read the latest news` is now inaccurate for the October items.
- The live `/news/` index displays a **10 November 2026** article first: `/news/scotland-blood-amber-alert-2026/`, followed by the **1 November 2026** LSCO announcement. Both are absent from the homepage's own News selection.
- The new Scotland article exists in the checked current source: `news/scotland-blood-amber-alert-2026/index.html` blob `d449e36f078f4ec5e3b1f97fc168deab57a98bd0`, title `Scotland’s Blood Amber Alert and PBM | BHOC News`, H1 `Scotland’s Blood Amber Alert and the Case for Upgrading the Blood System`, author Archil Jaliashvili, article date 10 Nov, source notice 5 Nov, self-canonical, generic `index,follow`, Yandex-specific `noindex`, NewsArticle JSON-LD, one descriptive image ALT (visual accuracy not independently verified).
- Read-only GitHub Actions [full 11 Nov sitemap verification](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42978500020) checked 81 root + 68 library entries, **137 unique URLs**, all HTTP 200. The [source/root audit](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42978500027) and [UX/source patch tests](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42977767950) also passed. The historic panel still holds 136 pages pending reconciliation; do not report 137 as a Google indexing count.
- Primary external [NHS Fife / Scottish National Blood Transfusion Service notice dated 5 November 2026](https://www.nhsfife.org/news-updates/latest-news/2026/11/blood-donors-urged-to-book-appointments/) confirms an Amber Alert, declining donor attendance, and pressure on Group O blood. It does **not** endorse BHOC or establish investigational oxygen-carrier efficacy.

## Exact bounded content proposal for owner review

Insert **one** date-stamped text-first item as the **first child** of `<section class="home-section" id="news">`, immediately before the existing 26 October tribute block. Do not rewrite or delete the four existing news/featured blocks, their images, hrefs, or approved scientific paragraphs. Use the homepage's existing `home-wrap`, `home-section-head`, `home-eyebrow`, `home-actions` and `home-button` classes; no new framework or CSS necessary.

**Proposed on-page copy (editorial, not yet published):**

> 10 November 2026 · Scotland · Blood supply
>
> **Scotland’s Blood Amber Alert and Patient Blood Management**
>
> Scotland’s blood service has issued an Amber Alert amid pressure on Group O blood stocks. Read our source-linked analysis of donor-blood access and Patient Blood Management; this does not establish BHOC as a clinical alternative.
>
> **Read the 10 November analysis →** [`/news/scotland-blood-amber-alert-2026/`]
>
> **All BHOC news →** [`/news/`]

The message is deliberately **dated**, not an undated `Latest` badge, so it can be preserved as a historical source note if stocks change. No numerical stock claims or treatment recommendations were introduced. `PBM` remains the established name; the newly proposed `function-based PBM` qualifier is not a WHO-endorsed term and is not silently added as a product claim.

**Why this specific change:** The homepage currently directs an arriving research visitor to October stories as its News selection, whereas the live News hub has a 10 Nov operational blood-supply example. One clear contextual link strengthens entry from the BHOC entity page into a dated source-linked question without creating duplicate landing pages. It also keeps the 1 Nov LSCO article accessible through the existing All News link. The user-facing interpretation and scientific wording require the normal editorial review.

## Acceptance tests before any future publication

1. Work against the then-current `main` source, not the divergent old preview homepage snapshot; preserve all current deployed changes, including the independently published mobile-first-screen improvements.
2. The inserted item has a distinct `<h2>`, not another `<h1>`; it links by descriptive text to exactly the verified News canonical and existing News index. No image is required, so ALT is **not applicable** to this proposed text-only card.
3. Do not add new Article schema to the homepage for a card that is merely a pointer; preserve the article's existing NewsArticle JSON-LD at its own canonical.
4. Retain existing historical news entries and their exact href destinations; if the inaccurate `Read the latest news` labels are to be renamed to `Read the October research note`, request a separate small wording review rather than silently rewriting protected text.
5. When preparing a genuine preview patch, test 320×700, 390×844, 768×1024 and 1440×1000, and run `node scripts/check_bhoc_content.mjs`, `node scripts/check_site.mjs`, `node --check navigation-context.js`, `git diff --check`. Respect the 11 Nov source-patch UX-01 test; the News section is below the first-screen hero and must not interfere with its existing CTA dimensions.
6. Do not alter sitemap `lastmod` or homepage update dates until a **real public deployment** occurs. No invented Google index/click/CTR/conversion results. The main-domain Search Console property is unavailable through the connected measurement source.
7. Approval for production merge and deployment remains required by `AGENTS.md`. A content brief, successful read-only audit, or recorded bot cycle does not authorize production publication.

## Work state and next action

CONTENT-01: **source-verified dated brief prepared; owner review pending**. UX-01: a **real, temporary source patch passed in a disposable checkout** today; production still not approved. SEM-01 and the seven owner-priority topic families remain intact; **0 new distinct measured or editorial keyword entries in this audit**. The complete SEO panel should be reconciled from 136 to **137 verified public sitemap pages** with the Scotland URL, leaving Google index verification unknown. No change to Vet, Transplant, Social Desk, AIO, GA4, Yandex policy, scientific source baselines or production `main`.
