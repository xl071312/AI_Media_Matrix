# CORPUS_COVERAGE — `wenyifei_jijiu`（温义飞的急救财经）

> Phase B update: 2026-09-18 PT. Toutiao-first; no style analysis.

## Identity / homepages
- creator_id: `wenyifei_jijiu`
- Toutiao: https://www.toutiao.com/c/user/token/MS4wLjABAAAA92PXnGCa5PoJxO09OYd14kXBGpRWWHrXJWrmRbiAPXd1RDV10NIzqJlpiPXsv3_j/
- Douyin: https://www.douyin.com/user/MS4wLjABAAAAPc9V-v4o3BdxwccbI5sPhAF-UPPk86Pkql0L9mHAJDY

## Coverage counts
| metric | count |
|---|---:|
| visible Toutiao creator article URLs after deep-scroll + 文章 tab | 20 |
| total unique inventory rows (Toutiao + B0.1 Douyin seeds) | 37 |
| opened pages with full article body | 22 |
| COMPLETE — article | 22 |
| COMPLETE — video | 0 |
| total COMPLETE | 22 |
| excluded (pre-existing B0.1 wrong-author/login records) | 6 |
| failed.csv rows | 0 |
| video rows retained but not COMPLETE | 15 |

Target of total COMPLETE >=20 was met with 22 article COMPLETE records.

## Toutiao collection
- Performed homepage deep-scroll, then opened the `文章` works tab and captured the visible creator article grid.
- 20 unique creator article URLs were inventoried from the works grid; 2 additional B0.1 seed articles were opened and merged. Each opened article had visible author identity `温义飞的急救财经` and a readable body.
- Full visible paragraph body was saved to `transcripts/<id>.txt`; page/title/author/URL and observed metrics/status were saved to `raw/<id>.json`.
- Missing metrics remain `NULL`; no estimates were added.

## Douyin collection / blocker
- Exact homepage URL from `homepage.json` was attempted.
- The page rendered only an empty/shell accessibility tree and then blank/no works grid; the logged-in works content was not reachable in this session. Existing B0.1 Douyin URLs were retained in the merged inventory.
- No `yt-dlp` was used.
- Douyin video rows are explicitly `transcript_status=NONE`, `complete_status=NOT_COMPLETE_FULLTEXT_UNAVAILABLE`; raw B0.1 proof metadata is retained. No video was promoted to COMPLETE because full 文案/字幕 text was not exposed.

## COMPLETE article artifacts
- 22 `transcripts/*.txt` full-body captures and matching `raw/*.json` records are present.
- COMPLETE article IDs include the 20 URLs observed in the Phase B Toutiao works grid plus B0.1 seed articles `7446304569308545570` and `7506434546527650356` (with `7685196005968527914` overlapping the grid).

## Exclusions / failures
- `excluded.csv` retains 6 B0.1 records: 5 wrong-author and 1 login-prompt record. No new ad/repost/irrelevant creator content was identified.
- `failed.csv` remains empty: no page-level failure was recorded for the 22 opened articles.

## Honest gap / blockers
- The corpus is article-complete for all 22 visible Toutiao creator articles captured here, but not video-complete. Fifteen retained video rows lack full UI-exposed transcript text and therefore remain non-COMPLETE by rule.
- Douyin homepage works-grid expansion could not be verified because the session exposed only a blank/shell state; additional Douyin coverage requires a reachable logged-in works grid or a later session.
