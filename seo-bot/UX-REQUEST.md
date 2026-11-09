# UX-01 / UX-02 / NAV-01 — targeted live recheck after Applications PR #104

**Request date:** 2026-11-09. **Status:** meaningful read-only measurement request; no production publication or new SEO bot. **Approved science:** unchanged.
**Current main** checked before request: `62b8869d7edcd15f9b2fafd93ef0f3b377668397` (8 Nov 18:17 UTC), "Open clinical reading directly from Applications (#104)". GitHub Pages deployment run 42509259579 and site validation run 42509259699 reported success. Earlier UX assessment (8 Nov) used main `c15a70b456786d99eb54da70fc8c83892f1d0400`; never confuse the two.
**Branch used only for owner audit:** `preview/therapeutics-web-seo-20261104`; this branch is not safe to merge wholesale over newer main. It has an established research/audit history.

## New question, new evidence, not repeated reporting

Applications navigation and clinical reading changed in production after the last Therapeutics SEO audit. The first-screen mobile problem was partly resolved by PR #99 on 8 Nov: H1 top y=185 at 390×844; Science and Technology actions were visible at y=481–585, whereas the Partners action appeared lower (y≈922). The 8 Nov finding is a dated baseline, **not** a live measurement of the post-PR #104 site. The updated Applications layout should be checked for navigation/reader-path regressions; separately, research collaboration still has no clearly labelled dedicated first-screen homepage action in the current main `index.html`.

Verified **current main source**, without editing it:
- `index.html` blob `f6b6fbb3d7061336018def8d6c0405696c9d22dd`: `.hero-copy .home-actions` contains exactly the two educational actions to `/science/` and `/technology/`. `.hero-partners-link` links to `/partners/` from the earlier hero-message block, not a dedicated research contact action. Existing header includes Contact and Partners.
- `contact/index.html`: contact form really exists and has an "Area of interest" option "Research collaboration". No form was submitted. `assets/ga4.js` blob `468bb559584bbd28bd6debdc9107423c34979f3a` recognizes `topic=oxygen-delivery-research` and `interest=research` to display the topic and pre-select research. Its `GA4_MEASUREMENT_ID = ''` remains deliberately blank; do not enable or invent an ID.
- `partners/index.html`: the primary "Request authorized access" link is for access to a **future** protected Business Portal. The page also includes investor, regional and clinical/manufacturing partnership invitations. Research participants may need clearer distinction between "discuss research" and "request confidential access." No promised current portal access.
- `applications/index.html` main now includes direct clinical reading changes following #104; do not revert or duplicate SCD/SCA links.

## Read-only tests requested from existing GitHub Actions

1. Re-run the existing `therapeutics-ux-review.yml` with current main and public pages. Record the current main SHA, check time and workflow run URL. Verify mobile 390×844 and desktop 1440×1000 on seven established routes, with focus on the homepage Science/Technology CTAs, research-path discoverability, /applications/ reading links, /partners/ research wording, /contact/ form presence and News. Save screenshots; no form submission.
2. Independently run the existing `therapeutics-library-seo.yml` across both live sitemap files, counting only direct `url/loc` entries (not image:loc); verify all intended canonical HTTP, title, description, H1, JSON-LD syntax, duplicate metadata and generic noindex. Observe changes since the 8 Nov 136-page baseline, without assuming number of pages in advance. Yandex-specific noindex must remain untouched.
3. Check old/new internal navigation for an obvious research collaboration path and inspect if meaningful text/image appears above mobile fold; no CSS or DOM changes by this request. The provided runner does not test 320×700, keyboard traversal, interaction conversions, Search Console indexing, AEO answer quality or visual accuracy of every ALT. Do not report those as measured.

## Narrow preview change to consider after measurements (not yet implemented)

Aim: let a prospective academic/clinical investigator find a research-specific enquiry route without displacing Science and Technology or confusing research with investor-portal access.

**Option A — tertiary plain text link:** in the current-main homepage `.hero-copy` after the existing `.home-actions`, consider an additional accessible link with the neutral label **"Discuss research collaboration"** and href `/contact/?interest=research&topic=oxygen-delivery-research`. Keep existing buttons, all approved texts, images and anchors unchanged. Test actual 390×844 AND 320×700, tap/focus target, mobile viewport height and form topic/area preselection with no submission. Avoid pretending it fits above fold without a screenshot. If link displaces approved first-screen information, reject Option A.

**Option B — context-specific research link:** if Option A fails the mobile hierarchy, propose a research-specific link within existing /partners/ clinical context and a reader-relevant Applications→evidence→contact journey. Preserve investor and portal links. Use the established form, not a new form or fictitious business portal.

Implementation must be based on the **newest** main source, and remain a targeted preview proposal until owner approval and all required preservation checks. A documentation commit in this preview branch is not live HTML/CSS. No change to approved science or to Vet/Transplant/Social/AIO.

## Prior test and source history retained

- 4 Nov corrected baseline: run 41812742704, 134 pages, 14 viewport tests, homepage mobile H1 y=897.
- 8 Nov post-PR #99: UX run 42460157401, full sitemap run 42460157402; 136 pages, 14 viewport tests, H1 y=185, no reported horizontal overflow; no demonstrated conversion gain.
- 8 Nov review: `seo-bot/reviews/2026-11-08-mobile-first-viewport-live-reassessment.md`. Do not apply the obsolete 5 Nov wholesale DOM-reordering proposal.
- 9 Nov new trigger: this document is a substantive new review request in response to PR #104, not an empty trigger.

**Public changes by the BHOC Therapeutics SEO bot: 0.** Actual Google indexing, rankings, search volume, field CWV, AEO mentions and individual image-ALT accuracy remain unmeasured. All published clinical texts and protected baselines remain as-is.
