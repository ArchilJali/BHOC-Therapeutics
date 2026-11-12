# 12 November 2026 — new P0 media URL defect after popular-science publication

**Status:** Source-verified SEO/UX/ALT and social-preview regression on current \`main\`. Read-only audit and executable preview-only guard; **not repaired on production**. Do not label a successfully fetched HTML page or existing ALT attribute as proof that its picture displays.

## Current evidence

- Current \`main\` commit when inspected: \`777d9660bfffc24021021b9dc747c34a38229d68\` (12 Nov). Latest GitHub Pages deployment for that SHA: https://github.com/ArchilJali/BHOC-Therapeutics/actions/runs/43173497578 — success. This establishes a deployed commit, **not** successful loading of individual remote images.
- Source 1, [News index](https://github.com/ArchilJali/BHOC-Therapeutics/blob/777d9660bfffc24021021b9dc747c34a38229d68/news/index.html), blob \`38f546afddaa3fcf0ba1cb03e79fa0ccb9274c7a\`: **2 malformed media references** for the popular-science feature: the visible featured-card \`img src\` and the structured-data ItemList image URL.
- Source 2, [11 Nov popular-science article](https://github.com/ArchilJali/BHOC-Therapeutics/blob/777d9660bfffc24021021b9dc747c34a38229d68/news/popular-science-biophysics-bhoc-breakthrough/index.html), blob \`f687535da62936c1966038ccb4a9115d37c84be6\`: **4 malformed media references**: \`og:image\`, \`twitter:image\`, \`NewsArticle.image.url\`, and the visible figure \`img src\`.
- Shared malformed literal:
  \`https://raw.githubusercontent.com/ArchilJali/BHOC-Therapeutics/mainhttps://raw.githubusercontent.com/ArchilJali/BHOC-Therapeutics/main/assets/news/bhoc-biophysics-exact-user-20261111.webp\`
- One News ItemList JSON-LD occurrence additionally prepends \`https://bhoctherapeutics.com\` to that malformed literal. These concatenated URLs are invalid image destinations independently of \`alt\` attribute presence or JSON-LD syntax validity.
- Main \`sitemap.xml\`, blob \`96fe39cc4cb78b54ada549eb2712227f0343ecf1\`, already references the **correct** image URL: \`https://bhoctherapeutics.com/assets/news/bhoc-biophysics-exact-user-20261111.webp\` for the article dated 11 Nov.
- The repository tree at \`main/assets/news/\` includes \`bhoc-biophysics-exact-user-20261111.webp\`, 15,008 bytes, blob \`e5de4b0209c612e8f80d979454d2adef2ec3532c\`. **Presence is not visual confirmation that it is the owner's specified photograph**; the image has not been pixel-inspected. Image dimensions in source and structured data also differ, and should be checked against the actual image file.
- The public News hub retrieved on 12 Nov shows the 11 Nov article as the first featured story, while the homepage's own news blocks remain dated 26/25/21 Oct. The latter is the already logged CONTENT-01 issue, not a newly discovered issue counted again. The public News hub contains an image ALT attribute, but this check does not establish the image loaded.

## Narrow remediation proposal — **preview / approval only**

1. **Verify actual pictured image first.** Open the repository image and compare visually with the owner's 11 Nov reference; identify native pixel dimensions. Do not substitute a generic car or AI illustration.
2. On the **latest main source, not the stale SEO preview HTML snapshot**, replace just those six malformed media URLs with the verified local source. For the \`img src\` on both pages use \`/assets/news/bhoc-biophysics-exact-user-20261111.webp\`; for \`og:image\`, \`twitter:image\`, \`NewsArticle.image.url\`, and the News ItemList image use \`https://bhoctherapeutics.com/assets/news/bhoc-biophysics-exact-user-20261111.webp\`. This is the intended canonical image URL already advertised by the sitemap; confirm the actual file before applying.
3. Preserve the existing human-readable article, 11 Nov date, H1/title, current \`alt\` words (pending image inspection), valid schema content, links, source credits, and all prior stories. Correct image width/height only after measured verification.
4. Run preservation checks \`node scripts/check_bhoc_content.mjs\`, \`node scripts/check_site.mjs\`, \`node --check navigation-context.js\`, \`git diff --check\`. Test visible \`<img>\`, Open Graph and Twitter image URLs and article JSON-LD URL, and ensure they resolve to the same verified image on the deployed site.
5. Update the final canonical article's \`lastmod\` only when a substantive public change is truly deployed. Never declare Google indexing or social cache refresh on the basis of HTTP 200 or a valid schema string alone. Do not edit \`main\` without separate authorization under \`AGENTS.md\`.

## Prevent recurrence

Created a read-only reusable \`seo-bot/media_url_lint.py\` in the existing SEO preview branch, with synthetic self-test. The preview GitHub Actions workflow \`therapeutics-web-seo.yml\` now checks out the current \`main\` and uses that script to record malformed image, social-preview and schema media URLs in \`_seo_output/media-url-integrity.json\`. It preserves the existing source and root audits. A CI outcome may be successful while a *reported* media issue is present: read the media report, not merely the workflow conclusion. Do not classify source-only local images as verified HTTP status; visual semantics and Google indexing remain unknown.

**New keywords:** 0; all 1,129 existing research candidates retained. **Public edits by this SEO bot:** 0. Other BHOC bots, search-crawler policies and approved SEO master untouched.
