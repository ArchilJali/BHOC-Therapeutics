# Approved knowledge-map release — 17 Sep 2026

The user explicitly approved the separate 14-topic overview and full chapter draft, plus a short blood-group note and internal source link in 07.2. This authorization supersedes the earlier continuous-hub-only presentation requirement below. It does not authorize deleting scientific text, breaking old anchors/URLs, changing unrelated SEO, publishing the pending Natanson analysis, or opening the closed standalone artificial-blood draft.

- Preserve every published source paragraph and original source destination; full chapters now live at the routes in `bhoc/knowledge-map-baseline.json`.
- Preserve `/bhoc/`, `/bhoc/historical-evolution/`, existing sitemap entries, and existing fragment IDs as overview destinations.
- The RBC blood-group note is grounded in the internal Blood Groups History reference: 49 systems and 400 antigens in the August 2026 release. Do not present this as a real-time registry count.
- `node scripts/check_bhoc_content.mjs` now dispatches to the protected multi-page source and route audit. Do not regenerate its baseline to conceal a failed preservation check.
- Production deployment requires a verified GitHub write and successful Pages deployment. Preparing files is not publication.

## Earlier preservation instructions (retained for provenance)

# BHOC Therapeutics — content preservation rules

These rules apply to every file in this repository.

## Non-loss rule

- Approved BHOC content must be restored from Git history or a protected baseline, never recreated from memory.
- Design, colour, navigation, SEO, routing, or layout work does not authorize deleting, hiding, shortening, rewriting, or moving approved text.
- The approved visual and information architecture for `/bhoc/` is the continuous morning hub from commit `f223aea` (16 Sep 2026), not a set of shortened standalone fragments.
- Sections 01 and 02 must remain inside that continuous hub together with the overview, quick-definition cards, knowledge map, and surrounding explanatory context.
- Section 03 `Artificial Blood & Blood Substitute` is a closed draft: it must not appear in the hub map, top chapter route, or reading sequence. Its direct route remains `noindex,nofollow` and shows only `In development` until the user explicitly approves publication.
- Every other published chapter, including 05 `Evolution & adaptation`, must remain fully visible; 03 is the only closed chapter.
- Preserve the approved text and links for the other visible sections. Status or publication changes require explicit user approval.

## Required workflow

1. Work on a `preview/*` branch and record the starting commit.
2. Compare every requested change against the protected morning state before editing.
3. Keep public `main` unchanged until the user explicitly authorizes publication.
4. Before presenting or publishing, run:
   - `node scripts/check_bhoc_content.mjs`
   - `node scripts/check_site.mjs`
   - `node --check navigation-context.js`
   - `git diff --check`
5. Report separately what was preserved, restored, and intentionally hidden.

## Evidence rule

- Scientific and commercial BHOC claims must come from the user's approved repository-backed sources and approved BHOC materials.
- Do not add external claims or interpretations without explicit approval.
