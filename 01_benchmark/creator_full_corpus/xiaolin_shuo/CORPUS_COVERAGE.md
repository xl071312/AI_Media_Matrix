# CORPUS_COVERAGE — `xiaolin_shuo` (小Lin说)

> Phase B collection from the Toutiao PRIMARY homepage. Updated 2026-09-18 PT.

## Identity
- creator_id: `xiaolin_shuo`
- display_name: 小Lin说
- primary_platform: toutiao
- homepage: https://www.toutiao.com/c/user/token/MS4wLjABAAAApzhfBgBWoQDePHbhmxcZNZQzTggHQPLBnsl5nzjsrTA/
- author verification: opened article/video pages showed author UI containing `小Lin说`.

## Coverage and cap
| metric | count |
|---|---:|
| unique inventory URLs after homepage deep-scroll + seed merge | 51 |
| inventory articles | 20 |
| inventory videos | 31 |
| opened/reviewed this session (cap 40) | 40 |
| opened articles | 20 |
| opened videos | 20 |
| COMPLETE | 20 |
| NOT_COMPLETE (metadata-only videos) | 18 |
| EXCLUDED | 2 |
| pending due to 40-item cap | 11 |
| failed | 0 |
| excluded.csv rows | 3 |

Homepage tabs surfaced 20 article cards and a video-card set; the merged inventory is a visible-card snapshot, **not full creator history**. The 11 unprocessed URLs remain `PENDING_CAP` in `url_inventory.jsonl`.

## Artifact policy
- Articles: 20 rendered full bodies captured with paragraph breaks in `transcripts/<id>.txt`; matching rendered metadata and paragraph arrays are in `raw/<id>.json`. All 20 are `COMPLETE`.
- Videos: 20 pages opened. Toutiao exposed title/date/metrics/author metadata but no full 文案/字幕 text in the UI. No audio transcription or yt-dlp was used; those videos are `transcript_status=NONE`, `raw_source_status=METADATA_ONLY`, and are not counted COMPLETE.
- Missing metrics remain `NULL`.
- Two black/buffering videos remain `EXCLUDED` in `excluded.csv` and the index; the non-creator Toutiao complaint notice is also retained only in `excluded.csv`.
- No captcha/login wall was encountered; no `xdg-open` was used.

## Files
- `homepage.json`: Toutiao homepage source record
- `url_inventory.jsonl`: 51 deduplicated article/video URLs and processing status
- `corpus_index.csv`: 40 opened/indexed records (20 articles, 18 metadata-only videos, 2 excluded videos)
- `raw/`: 40 JSON records
- `transcripts/`: 20 article transcripts; no video transcript files because full UI text was unavailable
- `excluded.csv`: 3 exclusions
- `failed.csv`: empty (0 failures)
