# Oxyglobin literature and official registry release

User authorized publication on 31 October 2026 with SEO and AEO included.
Source review: 30 October. Registry API recheck: 31 October (Asia/Tbilisi).
Starting main commit: `4f2c655c05497ae8483e8be39cb34ec724b31e98`.

## Search intent and destinations

| Intent | Canonical destination | Scope |
| --- | --- | --- |
| Oxyglobin publications / HBOC-301 evidence | `/evidence/library/veterinary/Vet-03-publication-BHOC-Oxyglobin.html` | Existing overview; 23 source-linked additions and classifications |
| Hemopure registered clinical trials / HBOC-201 NCT records | `/evidence/library/human/registered-clinical-studies.html` | Nine human registry records, separately classified by official study type |
| Oxyglobin animal clinical studies / FDA EMA documents | `/evidence/library/veterinary/Vet-fda-ema.html#registered-veterinary-studies` | Existing regulatory page; scoped zero-result NCT search and actual veterinary study sources |

## Implemented discoverability

- Static readable content, one H1, descriptive section headings and stable anchors.
- Distinct titles, descriptions, canonical URLs and Open Graph/Twitter metadata.
- Human registry page linked from Human index, search, FDA expanded access,
  Oxyglobin overview, animal regulatory page and Evidence Library home.
- Both sitemaps include the new canonical page; only changed pages receive a new lastmod.
- Existing robots policy permits these pages. The internal `/seo/` directory stays excluded.
- CollectionPage, ItemList, Dataset and BreadcrumbList JSON-LD describe the
  visible records; verified site author/publisher identities are reused.
- Downloadable human CSV/JSON and exact API query audit. Animal scope is a separate JSON.

## Answer clarity and scientific boundaries

- Lead with nine records: six Interventional and three Expanded Access.
- Five Phase 2 records, four randomized; never label all nine as RCTs.
- Show record status, last update and status-verification dates independently.
- Explain UNKNOWN and stale invitation status. Do not advertise recruitment.
- Keep veterinary Oxyglobin/glutamer-200 distinct from human Hemopure/glutamer-250.
- Zero exact-alias ClinicalTrials.gov results is not a global veterinary-registry census.
- FDA NADA 141-067 is an approval application, not a trial registration identifier.
- Registry entries are not added to publication counts. No unverified trial/article
  crosswalk or independent trial total is invented.
- Existing scientific paragraphs, links and catalogue record objects are preserved.
- Publication counter 970 → 993; distinct public records 651 → 674.

Google's current AI search guidance supports crawlable, internally linked text
and structured data matching visible content. It does not require a special
AI schema or AI text file and does not guarantee indexing or inclusion.
Primary reference checked: https://developers.google.com/search/docs/appearance/ai-features

## Rebuild and validation

Run the literature import only when incorporating its approved source file,
then build_evidence_catalogues.py, sync_evidence_overviews.py and finally
build_registered_study_pages.py. The last step retains the separate registry
pages, current descriptions, navigation and sitemap dates after rebuilding.

Required repository checks and catalogue validation must pass before publication.
Verify a successful GitHub Pages deployment and live canonical pages before
describing the release as published. Inclusion in search/AI answers remains
controlled by the search providers.
