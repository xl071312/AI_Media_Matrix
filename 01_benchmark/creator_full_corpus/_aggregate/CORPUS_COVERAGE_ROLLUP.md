# CORPUS_COVERAGE_ROLLUP — Issue #6 Phase B

Updated: 2026-09-19T02:23:50.347029+00:00

## Gate
Lan/ChatGPT ACCEPT on B0.1 (comment 5738138018). HERMES mechanical collection only.
**No Phase C / Voice Profile / new 口播稿 in this delivery.**

## Per-creator snapshot
| creator_id | display | primary | visible_works (UI) | inventory | opened/raw | COMPLETE fulltext/transcript | excluded | failed | coverage gap |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| yinhang_xiaojiejie | 银行小姐姐 | Douyin | 518 | 61 | 15–16 | **0** | 0 | 16 | Douyin spoken transcript blocked (no 文案 panel; yt-dlp 403) |
| zhinan_caijing | 直男财经 | Douyin | 1422 | 57 | 15 | **0** | 0 | 0 | Same Douyin spoken blocker |
| wenyifei_jijiu | 温义飞的急救财经 | Toutiao(+DY seeds) | ~20 TT articles visible | 37 | 37 | **22** (articles) | 6 | 0 | DY homepage blank this session; 15 videos retained NONE |
| hanxiuyun_jingji | 韩秀云讲经济 | Douyin | 1588 | 177 | 30 | **0** | 0 | 0 | Same Douyin spoken blocker |
| xiaolin_shuo | 小Lin说 | Toutiao | homepage card slice | 51 | 40 | **20** (articles) | 3 | 0 | Videos no full 文案; 11 URLs pending cap |
| banfo_xianren | 硬核的半佛仙人 | Toutiao | 12 cards after scroll | 25 | 25 | **25** (articles) | 2 | 0 | Articles only — not for spoken particle/rhythm stats |


## Totals
- COMPLETE fulltext/transcript files: **67** (= 25+20+22 Toutiao articles)
- Douyin spoken COMPLETE: **0** across 银行小姐姐 / 直男财经 / 韩秀云讲经济
- Honest gap: Douyin full spoken transcripts require a media path beyond current UI+yt-dlp (403 / no copyable 文案 panel)

## Paths
Root: `01_benchmark/creator_full_corpus/<creator_id>/`
Each: `corpus_index.csv`, `raw/`, `transcripts/`, `excluded.csv`, `CORPUS_COVERAGE.md` (+ `url_inventory.jsonl`, `failed.csv` where used)
