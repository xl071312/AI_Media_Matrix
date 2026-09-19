# B1 Existing Transcript Inventory SUMMARY

- Generated: 2026-09-19 01:26:48 PT
- Phase: Issue #6 Phase B1 — ORAL CORPUS RESOLUTION GATE
- Scope: existing local files only; **no Douyin yt-dlp**; no fabrication; **no Phase C**
- Inventory JSONL: `/workspace/AI_Media_Matrix/01_benchmark/creator_full_corpus/_aggregate/b1_existing_transcript_inventory.jsonl`
- Total inventory rows (incl. duplicates/mirrors/PARTIAL/REJECT): **313**
- Unique counts dedupe by `(creator_id, BV-or-numeric-id, modality)`; prefer `/workspace/.../01_benchmark/transcripts`.

## Counts per primary creator

| creator_id | display | FULL_SPOKEN | FULL_TEXT (articles) | PARTIAL_SPOKEN |
|---|---|---:|---:|---:|
| `yinhang_xiaojiejie` | 银行小姐姐 | **1** | **0** | 0 |
| `zhinan_caijing` | 直男财经 | **0** | **0** | 0 |
| `wenyifei_jijiu` | 温义飞的急救财经 | **0** | **22** | 0 |
| `hanxiuyun_jingji` | 韩秀云讲经济 | **0** | **0** | 4 |
| `xiaolin_shuo` | 小Lin说 | **0** | **21** | 1 |
| `banfo_xianren` | 硬核的半佛仙人 | **1** | **48** | 1 |
| **TOTAL primary** | | **2** | **91** | |

## Alternate creators (replacement screening)

| creator_id | display | FULL_SPOKEN | FULL_TEXT | PARTIAL_SPOKEN |
|---|---|---:|---:|---:|
| `wushi_caijing` | 巫师财经 | **0** | 2 | 1 |
| `xiapeng` | 夏鹏 | **0** | 0 | 0 |
| `yiming_caijing` | 一鸣财经 | **0** | 0 | 0 |
| `bainian_zhengjing` | 柏年说政经 | **0** | 0 | 0 |

### Top alternate oral candidates (by FULL_SPOKEN then PARTIAL_SPOKEN)
- `wushi_caijing` / 巫师财经: FULL_SPOKEN=0, PARTIAL_SPOKEN=1, FULL_TEXT=2
- `xiapeng` / 夏鹏: FULL_SPOKEN=0, PARTIAL_SPOKEN=0, FULL_TEXT=0
- `yiming_caijing` / 一鸣财经: FULL_SPOKEN=0, PARTIAL_SPOKEN=0, FULL_TEXT=0
- `bainian_zhengjing` / 柏年说政经: FULL_SPOKEN=0, PARTIAL_SPOKEN=0, FULL_TEXT=0

## Honest findings

1. Phase B `creator_full_corpus` Douyin oral COMPLETE remains **0** (银行小姐姐 / 直男财经 / 韩秀云). COMPLETE rows there are Toutiao **articles** only (温义飞 22 / 小Lin说 20 / 半佛 25).
2. After strict FULL filter, primary six have only **2 unique FULL_SPOKEN** pieces:
   - `yinhang_xiaojiejie` — `dy_7668650730379438031` (ASR_CORRECTED)
   - `banfo_xianren` — `bili_BV1T7411W7ca` (ASR raw/normalized; closing 感谢大家的关注)
3. Other spoken AVAILABLE/HAVE rows are PARTIAL (short vs duration / abrupt end) or REJECT (ASR corruption): 韩秀云×4 PARTIAL; 温义飞 `ttv_706847…` REJECT; 小Lin `BV1T54y1H7xF` PARTIAL; 巫师 `BV1ViEg6PESR` PARTIAL; 半佛 `BV1Uq4y1t7of` PARTIAL.
4. `BENCHMARK_SPOKEN_INGEST_108` target hits are PARTIAL_FIRST30 → REJECT for this gate.
5. `rc6j_full_transcripts` inspected = TRANSCRIPT_MISSING.
6. Alternates: **no FULL_SPOKEN** found; 巫师 has PARTIAL_SPOKEN×2 + FULL_TEXT×2 (best oral replacement signal among alternates, still not FULL).

## Likely corpus roots found

- `OK` `/workspace/AI_Media_Matrix/01_benchmark/creator_full_corpus`
- `OK` `/workspace/AI_Media_Matrix/01_benchmark/transcripts`
- `OK` `/workspace/AI_Media_Matrix/transcripts`
- `OK` `/workspace/AI_Media_Matrix/01_benchmark/shards/hermes`
- `OK` `/workspace/AI_Media_Matrix/01_benchmark/shards/hermes/scout_100`
- `OK` `/workspace/AI_Media_Matrix/01_benchmark/shards/hermes/transcripts`
- `OK` `/workspace/AI_Media_Matrix/01_benchmark/shards/grok/transcripts`
- `OK` `/workspace/AI_Media_Matrix/shards/grok/transcripts`
- `OK` `/workspace/AI_Media_Matrix/01_benchmark/article_parallel`
- `OK` `/workspace/AI_Media_Matrix/01_benchmark/toutiao_articles`
- `OK` `/workspace/AI_Media_Matrix/01_benchmark/cross_format_pairs`
- `OK` `/workspace/AI_Media_Matrix/01_benchmark/videos_master.csv`
- `OK` `/tmp/AI_Media_Matrix_handoff/01_benchmark/creator_full_corpus`
- `OK` `/tmp/AI_Media_Matrix_handoff/01_benchmark/analysis_batches/batch_001`
- `OK` `/tmp/AI_Media_Matrix_handoff/01_benchmark/analysis_batches/batch_002`
- `OK` `/tmp/AI_Media_Matrix_handoff/01_benchmark/analysis_batches/batch_003`
- `OK` `/tmp/AI_Media_Matrix_handoff/01_benchmark/analysis_batches/BENCHMARK_SPOKEN_INGEST_108`
- `OK` `/tmp/AI_Media_Matrix_handoff/01_benchmark/analysis_batches/rc6j_full_transcripts`
- `OK` `/tmp/AI_Media_Matrix_handoff/01_benchmark/plain_language_corpus_v1`
- `OK` `/tmp/AI_Media_Matrix_handoff/01_benchmark/plain_language_discovery_rc6h`
- `OK` `/tmp/AI_Media_Matrix_handoff/01_benchmark/shards/hermes_real/transcripts_v2`
- `OK` `/tmp/AI_Media_Matrix_handoff/01_benchmark/shards/hermes`

## FULL exemplars (best canonical path)

### yinhang_xiaojiejie — 银行小姐姐
- FULL_SPOKEN (1102 chars, douyin): `/workspace/AI_Media_Matrix/01_benchmark/transcripts/dy_7668650730379438031.spoken.txt`
  - url: https://www.douyin.com/video/7668650730379438031
- FULL_TEXT unique: **0**

### zhinan_caijing — 直男财经
- FULL_SPOKEN: _(none)_
- FULL_TEXT unique: **0**

### wenyifei_jijiu — 温义飞的急救财经
- FULL_SPOKEN: _(none)_
- FULL_TEXT unique: **22**
  - (2581 chars): `/workspace/AI_Media_Matrix/01_benchmark/creator_full_corpus/wenyifei_jijiu/transcripts/7669656437597012521.txt`
  - (2291 chars): `/workspace/AI_Media_Matrix/01_benchmark/creator_full_corpus/wenyifei_jijiu/transcripts/7669655912588411398.txt`
  - (2276 chars): `/workspace/AI_Media_Matrix/01_benchmark/creator_full_corpus/wenyifei_jijiu/transcripts/7675621509875925530.txt`

### hanxiuyun_jingji — 韩秀云讲经济
- FULL_SPOKEN: _(none)_
- FULL_TEXT unique: **0**
- PARTIAL_SPOKEN unique: 4
  - (545 chars): `/workspace/AI_Media_Matrix/01_benchmark/transcripts/ttv_7649742313967452687.spoken.txt`
  - (512 chars): `/workspace/AI_Media_Matrix/01_benchmark/transcripts/ttv_7641649664470549044.spoken.txt`
  - (370 chars): `/workspace/AI_Media_Matrix/01_benchmark/transcripts/ttv_7670628806587056703.spoken.txt`

### xiaolin_shuo — 小Lin说
- FULL_SPOKEN: _(none)_
- FULL_TEXT unique: **21**
  - (18681 chars): `/workspace/AI_Media_Matrix/01_benchmark/creator_full_corpus/xiaolin_shuo/transcripts/7589552775277707802.txt`
  - (15395 chars): `/workspace/AI_Media_Matrix/01_benchmark/creator_full_corpus/xiaolin_shuo/transcripts/7602231271872135680.txt`
  - (14370 chars): `/workspace/AI_Media_Matrix/01_benchmark/creator_full_corpus/xiaolin_shuo/transcripts/7583045663101829632.txt`
- PARTIAL_SPOKEN unique: 1
  - (2007 chars): `/workspace/AI_Media_Matrix/01_benchmark/transcripts/bili_BV1T54y1H7xF_normalized.md`

### banfo_xianren — 硬核的半佛仙人
- FULL_SPOKEN (2384 chars, bilibili): `/workspace/AI_Media_Matrix/01_benchmark/transcripts/bili_BV1T7411W7ca_normalized.md`
  - url: https://www.bilibili.com/video/BV1T7411W7ca/
- FULL_TEXT unique: **48**
  - (11047 chars): `/workspace/AI_Media_Matrix/01_benchmark/creator_full_corpus/banfo_xianren/transcripts/7682757634528674347.txt`
  - (7343 chars): `/workspace/AI_Media_Matrix/01_benchmark/transcripts/bili_BV1kV411r7HE.full.txt`
  - (6997 chars): `/workspace/AI_Media_Matrix/01_benchmark/transcripts/backlog_dig_338932_alipay.full.txt`
- PARTIAL_SPOKEN unique: 1
  - (2304 chars): `/workspace/AI_Media_Matrix/01_benchmark/transcripts/bili_BV1Uq4y1t7of_normalized.md`

### wushi_caijing — 巫师财经
- FULL_SPOKEN: _(none)_
- FULL_TEXT unique: **2**
  - (6249 chars): `/workspace/AI_Media_Matrix/01_benchmark/toutiao_articles/7639365611172151843.md`
  - (565 chars): `/workspace/AI_Media_Matrix/01_benchmark/toutiao_articles/tta_7574305587593232906.md`
- PARTIAL_SPOKEN unique: 1
  - (3409 chars): `/workspace/AI_Media_Matrix/01_benchmark/transcripts/bili_BV1ViEg6PESR_normalized.md`

### xiapeng — 夏鹏
- FULL_SPOKEN: _(none)_
- FULL_TEXT unique: **0**

### yiming_caijing — 一鸣财经
- FULL_SPOKEN: _(none)_
- FULL_TEXT unique: **0**

### bainian_zhengjing — 柏年说政经
- FULL_SPOKEN: _(none)_
- FULL_TEXT unique: **0**
