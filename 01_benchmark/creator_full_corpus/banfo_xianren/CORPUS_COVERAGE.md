# CORPUS_COVERAGE — `banfo_xianren`（硬核的半佛仙人）

> Phase B mechanical full-text collection (HERMES). Updated 2026-09-18 PT.
> Articles only; no style analysis, spoken-particle statistics, or ASR fabrication.

## Identity / homepage
- creator_id: `banfo_xianren`
- homepage UI name: `半佛仙人本仙人`
- homepage: https://www.toutiao.com/c/user/token/MS4wLjABAAAA5X0VBPDBZMEMapObds7t3Z_5K6V61i3zNDYgSd6uPlM/
- UI metrics observed: 58.4万 粉丝; 133.7万 获赞
- author match rule: visible author must contain `半佛`; collected pages showed `半佛仙人本仙人`.

## Coverage counts
| measure | count |
|---|---:|
| homepage visible cards after deep-scroll | 12 |
| unique inventory URLs | 25 |
| opened | 25 |
| COMPLETE | 25 |
| excluded | 2 |
| failed | 0 |
| videos in inventory | 0 |
| articles in inventory | 25 |

## Collection notes
- Homepage deep-scroll was taken to the end; the final 12 visible cards yielded no new cards after the end-scroll check.
- Two additional article URLs were added from the homepage scroll (`source=homepage_scroll`); the other 23 inventory rows are the B0.1 seed (`B01_SEED`). Inventory is de-duplicated by URL.
- Every inventory URL was opened. Each collected article has visible page-open proof, author match, a non-title-only full body in `transcripts/<id>.txt`, and metadata in `raw/<id>.json`.
- Metrics remain `NULL` where the page/seed did not expose them. No video caption or ASR work was needed.
- Existing B0.1 exclusions retained in `excluded.csv`: one HTTP 404/nonexistent page and one author mismatch (`潘乱`). No new exclusions or failures.
- No captcha or login wall was encountered.

## Artifact/status conventions
- `transcript_status=FULLTEXT`
- `raw_source_status=VISIBLE_DOM`
- `complete_status=COMPLETE` only after page open + author match + substantial full body saved.
- `transcripts/` contains paragraph-separated article body text; `raw/` contains per-URL JSON metadata.

## Honest gap note
This is a mechanical snapshot of the homepage-visible slice plus the B0.1 seed, not a claim of the creator's complete historical archive. Toutiao homepage pagination/filter behavior and unrendered or removed works may leave older content outside this inventory.
