# BHOC Therapeutics — content preservation rules

These rules apply to every file in this repository.

## Non-loss rule

- Existing approved content is the source of truth. Restore it from Git history or the protected baseline; never recreate it from memory.
- A request about design, navigation, colour, layout, SEO, links, or routing does **not** authorize deleting, hiding, shortening, rewriting, replacing, or moving existing text.
- Never remove or change an existing paragraph, claim, source link, internal route, anchor ID, page, or completion status unless the user explicitly approves that exact change.
- Additions must be additive. If new material conflicts with old material, stop and ask instead of overwriting either version.
- Never infer that an `In development` section is complete. Never mark a loaded section as unfinished. Status changes require explicit user approval.

## Protected BHOC Authority Hub state

- Loaded: 01, 02, 04, 06, 07, 08.
- In development: 03 `Artificial Blood & Blood Substitute`, 05 `Evolution & adaptation`.
- In-development routes remain visible and usable, but their dedicated pages remain `noindex` until explicitly approved as complete.
- Every numbered section has both a preserved hub section and a dedicated route:
  - 01 `/bhoc/what-is-bhoc/`
  - 02 `/bhoc/why-bhoc/`
  - 03 `/bhoc/artificial-blood-blood-substitute/`
  - 04 `/bhoc/oxygen-regulation/`
  - 05 `/bhoc/evolution-adaptation/`
  - 06 `/bhoc/hemoglobin-outside-red-blood-cell/`
  - 07 `/bhoc/what-makes-bhoc-different/`
  - 08 `/bhoc/precision-oxygen-therapeutics/`
- Every dedicated page must retain the complete approved hub-section text and links. Loaded pages are full pages, not summaries. In-development pages must show all approved material available to date while retaining their `In development` label and `noindex` policy; status must never be used to hide existing information.
- The BHOC map cards, the section-level page links, the previous/next controls and the top BHOC route bar must keep these routes connected. The current route must remain visibly highlighted.
- The protected text, links, routes, and statuses are recorded in `bhoc/content-baseline.json`.
- Do not edit that baseline merely to make a failing check pass. Update it only after the user explicitly approves every corresponding content or status change.

## Required workflow

1. Work on a `preview/*` branch. Record the starting commit before editing.
2. Compare the requested change against the last approved state before modifying files.
3. Keep public `main` and the live site unchanged until the user explicitly authorizes publication.
4. Before presenting or publishing, run:
   - `node scripts/check_bhoc_content.mjs`
   - `node scripts/check_site.mjs`
   - `node --check navigation-context.js`
   - `git diff --check`
5. Report separately what was preserved, what was added, and what—if anything—was intentionally changed.

## Evidence rule

- Scientific and commercial BHOC claims must use the user's approved repository-backed sources and approved BHOC materials.
- Do not introduce external claims into BHOC content without the user's explicit approval.
