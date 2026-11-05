# UX-01 — First-viewport implementation specification (preview-only)

**Reviewed:** 2026-11-05 · BHOC Therapeutics human/corporate website.
**Status:** Implementation-ready design brief / not an implemented HTML or CSS patch.
**Scope:** Only the homepage hero `<section class="home-hero" id="hero">`.
**Production edits:** 0. **Owner review before merge:** required.
**Source baseline:** `main` commit `dc6b18acf9672d3362e07e6e9eda6006faaf5da1`; `index.html` blob `b241e0bf30ec67d37af962d06a857e6b7e53885c`; `homepage.css` blob `366c960a1c262a4dfeb1f828dc61100e1326b2fa`.

## Verified gap

The corrected read-only browser audit dated 2026-11-04T10:14:18Z (GitHub Actions run 41812742704) measured the mobile homepage at **390×844**. The main H1 begins at y=897 px and the first main-content Science CTA at y=1177 px. This means the mobile first viewport does not contain the defining H1 or the reader action. No horizontal overflow or broken images were recorded in the tested set. The result is a layout/hierarchy issue, **not** proof of lost conversions or a Google ranking penalty.

Live homepage reading on 2026-11-05 confirmed that the current desktop/source content opens with the mission section and large RBC illustration, followed by H1 `Blood is a system. Oxygen delivery is a function.`, a short Precision Oxygen Therapeutics definition, and links to Science and Technology. Source `homepage.css` contains the mobile declaration `.hero-visual{order:-1}`, which deliberately puts the large image before the `.hero-message`; the `.hero-bottom` containing the H1 follows this entire first section.

Observed routes:
- Homepage: https://bhoctherapeutics.com/
- Evidence: https://bhoctherapeutics.com/evidence/
- Science: https://bhoctherapeutics.com/science/
- Technology: https://bhoctherapeutics.com/technology/
- Partners: https://bhoctherapeutics.com/partners/
- Contact: https://bhoctherapeutics.com/contact/

Partners already has separate collaboration links, and Contact already contains a message form. Do **not** claim these features are missing or send a trial submission. The business portal described by Partners is being prepared; do not imply instant portal access.

## Concrete implementation proposal

**Mobile reading order**: verified existing brand/navigation and BHOC quick guide → **unchanged existing H1** → existing `Precision Oxygen Therapeutics.` accent and existing descriptive paragraph → two immediate actions → the existing `One Oxygen. One Biology. One BHOC System.` mission text, biodiversity-mark description and graphic → existing RBC/BHOC comparison image → existing comparison cards and blood-group information.

To avoid a visual-only order differing from document/keyboard order, use a *semantic DOM refactor* of the hero, rather than CSS `order:-1` applied to keyboard-focusable elements. One bounded `.hero-stage` grid can hold the existing `.hero-copy`, `.hero-message`, `.hero-visual` and `.compare-grid`, while `.compatibility-note` remains afterward. Source order should follow the mobile order. Use CSS grid template areas for the approved desktop appearance and a single-column order on narrow screens.

Do not remove or shorten any existing scientific, species, historical, explanatory or compatibility text. Keep every image, ALT, `width`, `height`, `srcset` and `sizes`, existing inbound routes and all IDs/anchors. Preserve exactly one H1. The current motto H2 should remain visible after the H1 on mobile. The desktop brand presentation must remain visually equivalent.

**Two actions to test, subject to editorial approval:**
1. Primary: `Explore the evidence` → `/evidence/`. This is a route to substantiation, not a claim of approval.
2. Secondary: `Discuss research collaboration` → `/contact/?topic=oxygen-delivery-research`. The `assets/ga4.js` topic map recognizes `oxygen-delivery-research` for a contact context; the form is already present. Test that the query context is displayed and that no personal data are emitted to analytics. Do not submit a form.

The existing `/science/` and `/technology/` links must remain available; they can be retained as additional less prominent links in the hero or in the immediately adjacent section, subject to a review of link sequence. Do not delete them.

## Acceptance checks before asking for production permission

1. Create the proposed DOM/CSS change **only in the existing preview branch**. Keep the old version as a side-by-side comparison; record file SHAs and affected lines. Do not change `main`.
2. On **390×844**, verify by screenshot that the complete H1 and two primary actions appear above the bottom of the first viewport, with minimum 44 px practical tap targets, correct keyboard order and no overlay. Also verify **320×700** for legible text and no horizontal scrolling; if both actions cannot fit at 320×700, retain a readable first action and don't hide the second.
3. On **1440×1000** and a tablet-width viewport, verify no regressions in the current visual hierarchy, no missing hero image, no overlap/overflow and no layout shift caused by missing image dimensions. These are lab-layout checks, not field Core Web Vitals.
4. Verify exactly one H1, unchanged approved substantive copy, all existing anchors, image ALT, canonical and JSON-LD, accessible nav focus, and links to `/science/`, `/technology/`, `/evidence/` and `/contact/`.
5. Check `assets/ga4.js`: currently `GA4_MEASUREMENT_ID = ''`; do not create an ID, turn on tracking, or transmit names, emails, organizations or message text. Do not count form availability as a confirmed measured conversion.
6. On preview source, require exit code 0 from `node scripts/check_bhoc_content.mjs`, `node scripts/check_site.mjs`, `node --check navigation-context.js` and `git diff --check`. Run actual preview-rendered screenshot comparisons before proposing merge; a read-only workflow pointing at `main` does **not** test a preview patch.
7. Mark complete only after preview tests and an explicit owner approval to merge, followed by a verified production deployment. No Google-indexing or conversion improvement can be claimed from this brief.

## Adjacent, separate work

- **SEM-01**: Current homepage primary category remains `Precision Oxygen Therapeutics`; `/bhoc/` owns the BHOC definition; `/technology/` owns technology; do not generate redundant pages.
- **UX-02**: `/partners/` and `/contact/` already exist. Keep collaboration-path wording accurate; protected portal remains future-tense.
- **CONTENT-01**: Source read on 2026-11-05 confirms News leads with a **1 November 2026** LSCO article. The older homepage recent-news selection should be synchronized after editorial/source review, without changing historical dates.

**Verified primary references:**
- https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/41812742704
- https://github.com/ArchilJali/BHOC-Therapeutics/blob/main/index.html
- https://github.com/ArchilJali/BHOC-Therapeutics/blob/main/homepage.css
- https://bhoctherapeutics.com/
- https://bhoctherapeutics.com/partners/
- https://bhoctherapeutics.com/contact/
