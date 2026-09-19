# PHASE_B_PLAN — Issue #6 Full Corpus

> Scaffolded: 2026-09-18 PT (HERMES)
> Work root: `/workspace/AI_Media_Matrix/01_benchmark/creator_full_corpus/`
> Gate: Lan ACCEPT Phase B0.1 (2026-09-19T01:32Z PT source comment) — full corpus collection only.
> Forbidden until Phase B验收: Phase C deep style / Voice Profile / new口播稿.
> **Do not modify** `videos_master.csv`, `creators.csv`, or `topic_clusters*`.

## Goal
Build per-creator full corpus trees with index, raw artifacts, transcripts, exclusions, and coverage docs — seeded from B0.1 COMPLETE proofs, then expanded via homepage deep collection.

## Roster (canonical IDs)
See `PHASE_B_CREATOR_IDS.md`. Alias: CREATOR_SELECTION `dy_银行小姐姐` → `yinhang_xiaojiejie`.

## Per-creator layout
```
<creator_id>/
  corpus_index.csv
  raw/
  transcripts/
  excluded.csv
  failed.csv
  CORPUS_COVERAGE.md
  url_inventory.jsonl
```

### corpus_index.csv columns
`creator_id,platform,title,url,publish_time,likes,comments,favorites,shares,duration_or_word_count,discovery_mode,transcript_status,raw_source_status,content_type,is_ad,is_repost,is_irrelevant,complete_status,notes`

- discovery_mode: `B01_SEED` (this seed) | `CREATOR_FULL_CORPUS` (later expansion)
- Seed defaults: transcript_status=`PENDING`, raw_source_status=`PENDING`, complete_status=`B01_VERIFIED_PENDING_FULLTEXT`
- Missing metrics = `NULL` (never invent)

## Phase B workstreams
1. **Seed (DONE in scaffold):** Import B0.1 COMPLETE rows → corpus_index + url_inventory.
2. **Expand:** Deep-scroll creator homepages; append new URLs with discovery_mode=`CREATOR_FULL_CORPUS`.
3. **Raw capture:** Download video/audio or article HTML into `raw/`; set raw_source_status.
4. **Fulltext:** faster-whisper for video; DOM/article extract for toutiao articles → `transcripts/`.
5. **QC:** Flag is_ad / is_repost / is_irrelevant; move rejects to excluded.csv; hard failures → failed.csv.
6. **Coverage:** Keep CORPUS_COVERAGE.md + `_aggregate/CORPUS_COVERAGE_ROLLUP.md` current.

## Tooling
- Local venv: `creator_full_corpus/.venv` with `faster-whisper` + `yt-dlp`
- No browse in this scaffold turn; collection agents may browse later under Phase B rules.

## Caveats carried from B0.1
- `wenyifei_jijiu`: BELOW_20_DOCUMENTED (18 COMPLETE); keep_all_three — do not replace.
- `banfo_xianren`: articles-only oral口播 caveat.
- Douyin login fragility (zhinan / wenyifei).
