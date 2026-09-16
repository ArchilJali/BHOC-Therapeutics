# BHOC Therapeutics — content preservation rules

These rules apply to every file in this repository.

## Non-loss rule

- Approved BHOC content must be restored from Git history or a protected baseline, never recreated from memory.
- Design, colour, navigation, SEO, routing, or layout work does not authorize deleting, hiding, shortening, rewriting, or moving approved text.
- The approved visual and information architecture for `/bhoc/` is the continuous morning hub from commit `f223aea` (16 Sep 2026), not a set of shortened standalone fragments.
- Sections 01 and 02 must remain inside that continuous hub together with the overview, quick-definition cards, knowledge map, and surrounding explanatory context.
- Section 03 `Artificial Blood & Blood Substitute` is a closed draft: it must not appear in the hub map, top chapter route, or reading sequence. Its direct route remains `noindex,nofollow` and shows only `In development` until the user explicitly approves publication.
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
