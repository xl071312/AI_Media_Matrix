# ORAL_CORPUS_GATE_V1 — Issue #6 Phase B1

Generated: 2026-09-19 08:27 UTC

## Verdict

**GATE_STATUS: NOT_PASSED**

Phase C / Voice Profile / 新口播稿：**禁止进入**。

机械采集真实性保留（文章 COMPLETE 与「口播拿不到就记 0」均已接受），但当前 **可用完整口播语料不足以支撑口语学习主线**。

## Gate thresholds vs actual

| Threshold | Required | Actual | Pass? |
|---|---|---|---|
| Modality layered (spoken ≠ article) | yes | yes — articles tagged `ARTICLE_TEXT` / `usable_for_spoken=NO` | YES |
| Creators with usable FULL spoken | ≥4 | **2** (银行小姐姐 1, 半佛 AUX 1) | **NO** |
| FULL_SPOKEN across ≥4 creators | ≥60 | **2** unique FULL_SPOKEN on named roster | **NO** |
| Creator fingerprint floor | FULL_SPOKEN ≥20 | **0** creators | **NO** |
| Replace if oral role still <10 | yes | 银行/直男/韩秀云全部 <10；替换池亦无 ≥10 的具名候选 | **OPEN** |

## Final creator roster (B1 freeze for acceptance)

| creator_id | display | seat | FULL_SPOKEN | COMPLETE_TEXT | PRIMARY_ORAL | AUX_ORAL | gate_tier | replace? |
|---|---|---|---:|---:|---:|---:|---|---|
| yinhang_xiaojiejie | 银行小姐姐 | ORAL_PRIMARY | 1 | 0 | 1 | 0 | ORAL_INSUFFICIENT | YES |
| zhinan_caijing | 直男财经 | ORAL_PRIMARY | 0 | 0 | 0 | 0 | ORAL_INSUFFICIENT | YES |
| wenyifei_jijiu | 温义飞的急救财经 | TEXT_PRIMARY | 0 | 22 | 0 | 0 | TEXT_ARGUMENT_OK | NO |
| hanxiuyun_jingji | 韩秀云讲经济 | ORAL_PRIMARY | 0 | 0 | 0 | 0 | ORAL_INSUFFICIENT | YES |
| xiaolin_shuo | 小Lin说 | TEXT_PRIMARY | 0 | 20 | 0 | 0 | TEXT_ARGUMENT_OK | NO |
| banfo_xianren | 硬核的半佛仙人 | TEXT_PRIMARY | 1 | 25 | 0 | 1 | TEXT_ARGUMENT_OK | NO |

**COMPLETE_TEXT total = 67** (22+20+25) — Phase B accepted Toutiao articles; **must not** be used for filler / pause / oral-rhythm stats.

**FULL_SPOKEN total on roster = 2** (douyin×1 + bilibili AUX×1).

## PRIMARY / AUX_ORAL distribution

- PRIMARY_ORAL (Douyin): 银行小姐姐 **1**
- AUX_ORAL (Bilibili public/local ASR): 半佛 **1**
- PARTIAL spoken retained but **not counted as FULL**: 韩秀云×4, 小Lin说×1, 半佛×1, 巫师财经×1
- TEXT_ARGUMENT_CORPUS: 温义飞 22 / 小Lin说 20 / 半佛 25

## Replacement screening (B1-4)

See `b1_replacement_screening.csv`.

| Candidate | FULL_SPOKEN | Note |
|---|---:|---|
| 巫师财经 | 0 (PARTIAL bili×1) | style-fit OK; **not replace-ready** |
| 夏鹏 / 一鸣财经 / 柏年说政经 | 0 | no FULL on disk |
| Batch001/002 + plain_language ASR pool | ~30+ FULL ASR bodies | **creator names MASKED** — cannot seat as named roster without re-ID + consent path |

**Conclusion:** oral seats (银行/直男/韩秀云) are **REPLACE_REQUIRED**, but **no named replacement currently clears FULL_SPOKEN≥10**. Next unblock (post-acceptance) must be: (a) public CC harvest without login wall, or (b) re-identify masked benchmark ASR creators who already have FULL transcripts.

## What was reused (B1-1)

- Phase B `creator_full_corpus` article COMPLETE for 温义飞/小Lin说/半佛
- `01_benchmark/transcripts` + shards existing spoken files
- Batch001/002 / plain_language / BENCHMARK_SPOKEN_INGEST_108 scanned; first30-only and TRANSCRIPT_MISSING rejected

## What was NOT done (hard rules)

- No repeated yt-dlp Douyin 403 path
- No login-wall bypass
- No treating articles as spoken
- No Phase C / Voice Profile / new 口播稿

## Public caption attempt (B1-2/3)

- Bilibili HTTP API returned **412** without browser session
- Browser public-CC pass dispatched in parallel; if it adds FULL CC files, refresh this gate before any Phase C ask
- Until then: AUX_ORAL remains the single banfo BV already on disk

## Artifacts

- `_aggregate/oral_corpus_gate.csv`
- `_aggregate/corpus_manifest_sha256.csv`
- `_aggregate/b1_replacement_screening.csv`
- `_aggregate/b1_existing_transcript_inventory.jsonl`
- `_aggregate/b1_existing_inventory_SUMMARY.md`
- `_aggregate/ORAL_CORPUS_GATE_V1.md` (this file)

## Stop

B1 mechanical resolution complete for acceptance. Awaiting Lan / ChatGPT decision on roster replace vs further public-CC collection. **No Phase C.**
