# UX-01 / SEO audit request — 8 November 2026

**Scope:** independent, read-only verification of the live BHOC Therapeutics site after the separately merged mobile fix, PR #99. **Status:** pending measurement, not a claim of UX-01 completion. **Owner:** existing BHOC Therapeutics — Web SEO bot. **Publication authorization:** none; main remains untouched by this request.

## Why a new audit is warranted

The previous mobile baseline from 4 Nov (run 41812742704, 390 × 844) recorded H1 top at **y=897 px** and the first main-content Science action at **y=1177 px**. This is a layout/hierarchy observation, not a proven conversion or ranking effect.

Current `main` commit `c15a70b456786d99eb54da70fc8c83892f1d0400` dated 2026-11-08 06:41 UTC includes PR #99 `Fix mobile homepage overflow and reading order`, merged at 06:41 UTC and followed by shared-navigation integration. The GitHub Pages deployment for that commit completed successfully. The prior SEO-bot preview branch (07 Nov) is **not** the deployed site. Compare the live published change to the dated baseline before preparing additional HTML/CSS changes. Do not recreate the old proposal blindly.

## Requested read-only measurements

1. Run existing `seo-bot/ux_review.py` from this preview branch against **current public site and current main** using the existing `therapeutics-ux-review.yml`; record run ID, source SHA and UTC checked_at. Render 390×844 and 1440×1000 for existing seven routes and preserve original screenshots; test 320×700 if the runner supports it, otherwise record that it was not tested.
2. For homepage, inspect visible current **H1 bounding box y**, definition/primary-action placement, graphic order, and the visible navigation. Determine whether PR #99 solves horizontal overflow only, reading order, or also the first-screen discoverability of the category/CTA. Compare to baseline. Do not infer UX/SEO improvement from a passing CI check alone.
3. Verify no measured horizontal overflow, broken images, omitted scientific text, hidden links or new H1 duplication. Check click paths homepage → evidence and homepage → partners/contact without submitting contact forms or enabling analytics.
4. Check existing News and homepage recent-news cards after the live update. Treat source publication dates separately from sitemap `lastmod`. Do not automatically reorder approved news or call an older item a new event.
5. Run both actual live sitemaps with the already configured read-only full-sitemap audit; report deduplicated **page** URLs excluding `image:loc`, HTTP/canonical/title/description/H1/JSON-LD syntax and duplicate metadata. Do not call those checks Google indexing, ALT semantic accuracy or field Core Web Vitals.
6. Record explicitly the unverified work: main-domain Search Console indexing, conversion events, search-volume/KD, AI citations, visually reviewed ALT, and treatment claims. Yandex-only noindex must remain separate and unchanged.

## Follow-up gate

If the current production mobile change has already solved the UX-01 first-screen problem, mark it **observed fixed by PR #99, not implemented by the SEO bot** after screenshot evidence. If not, prepare a **new narrow preview proposal based on today's current main**, preserving every existing word, image, anchor, routing destination and approved clinical/evidence text. Do not change main or merge this older bot branch. Prefer meaningful existing page improvements; never add duplicate landing pages to raise keyword counts.

Research priorities heart/cardiac surgery, major surgery, dialysis, anesthesia/anaesthesia, emergency/prehospital and medical battlefield logistics remain in `seo-bot/OWNER-PRIORITIES-20261104.md`. This request does **not** change their status or the approved SEO master.

**No publication / no new automation / no Vet, Transplant, Social Desk or AIO mutations.**
