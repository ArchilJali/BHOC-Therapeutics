# 10 November 2026 — verified responsive research CTA prototype

**Status:** Tested in an isolated browser by DOM injection only. Not a source patch, not published, not owner-approved for production. Main SHA observed: 62b8869d7edcd15f9b2fafd93ef0f3b377668397. No changes to protected text or other BHOC bots.

## Actual new test

[GitHub Actions UX run 42774863916](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42774863916) completed successfully. In its bhoc-therapeutics-seo-ux-review artifact, the research-cta-prototype directory contains result.json and before/after screenshots for 320×700, 390×844 and 1440×1000.

The experiment inserted a third, accessible plain text link after the two existing education actions in the home hero, using a 44-pixel touch/focus target. No published file or approved text was modified.

| Viewport | Original Science / Technology actions | Added research link | Horizontal overflow |
| --- | --- | --- | --- |
| 320×700 | y=539–586 / 598–644, unchanged | y=651–695 (only 5px before fold) | None |
| 390×844 | y=481–527 / 539–585, unchanged | y=592–636 | None |
| 1440×1000 | both y=938–982, unchanged | y=989–1033, below fold | None |

All three viewports passed DOM integrity tests: one H1, existing education controls preserved and unmoved, image count unchanged, exactly one added link, correct target, keyboard focus and no overflow. The 320×700 case is borderline because the link ends 5px above the bottom; do not infer that it is visible above actual mobile browser chrome or across all handsets. The desktop link is below the first viewport.

**Proposed source addition after the existing .hero-copy .home-actions (not yet applied):**

~~~html
<a class="hero-research-link" href="/contact/?interest=research&amp;topic=oxygen-delivery-research">Discuss research collaboration →</a>
~~~

**Scoped CSS tested in the browser, not in the repository homepage stylesheet:**

~~~css
.hero-copy .hero-research-link {
  display:inline-flex; align-items:center; min-height:44px;
  margin-top:7px; padding:8px 0;
  color:#0b377f; font-size:13px; font-weight:700;
  text-decoration:underline; text-underline-offset:3px;
}
.hero-copy .hero-research-link:focus-visible {
  outline:2px solid #d52321; outline-offset:3px;
}
~~~

The existing Contact destination returned HTTP 200. Its Area of interest preselected **Research collaboration** and showed **Topic: Oxygen delivery research**. No form was filled or submitted; GA4 remained disabled. These are observed behaviors, not inferred conversion improvements.

## Today's verified technical state

- [Full sitemap run 42774832408](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42774832408): 80 root plus 68 evidence-library entries, 136 unique public page URLs; all HTTP 200. Zero detected title/description/H1/canonical/JSON-LD syntax/noindex or duplicate metadata issues. The two pages without optional JSON-LD are methodology and privacy.
- [Source/root run 42774832503](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42774832503) completed successfully; see its artifact for source paths and checks.
- [Combined live UX run 42774863916](https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/42774863916): 136 HTTP 200; 14 established rendered tests with no reported overflow, broken images or broken anchors. No missing ALT attributes or intrinsic dimensions, but actual ALT semantics have not all been visually inspected. Yandex-specific noindex remains on all 136.
- Fresh Windsor connection check shows Search Console only for Evidence Platform and bhocvet.com, not the human domain. Google indexing, queries, CTR, conversions and AI citations remain **unknown**, not zero. No field CWV measured.
- No new unique keyword candidates this UI experiment; retain the previous total of 1129.

## Next step

This measured browser prototype is a candidate for a minimal, source-based preview implementation against **fresh main**, not against the old divergent preview homepage snapshot. Preserve all source text, images, anchors and Science/Technology links; test 320×700 with browser chrome or smaller screen to address the 5px clearance. Run mandatory preservation checks and visually compare before any proposed production publication. If cramped, use the preexisting Partners contextual research-answer alternative.

**Production changes by this bot: 0.** Existing other bots, SEO master, closed draft, sitemap and publisher settings were not changed.