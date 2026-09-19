# PHASE_B_DELIVERY_DRAFT — Issue #6 Lan report (10 fields)

> Draft only. Metrics from EXISTING Phase B corpus files (no browse, no invented numbers).
> Drafted: 2026-09-18 19:15 PT
> Commit SHA: **TBD**
> Issue comment link: **TBD**

---

## 1. Visible works (homepage / grid snapshot)

| creator | visible_works |
|---|---|
| yinhang_xiaojiejie | **518** (Douyin homepage UI) |
| zhinan_caijing | **1422** (Douyin homepage UI) |
| wenyifei_jijiu | **20** Toutiao article URLs after deep-scroll + 文章 tab |
| hanxiuyun_jingji | **n/a** — homepage UI works count not yet captured (**RUNNING/pending**) |
| xiaolin_shuo | **n/a** as single UI total; visible-card inventory after scroll = 51 URLs (20 articles + 31 videos) |
| banfo_xianren | **12** Toutiao homepage cards at end-scroll |

Caveat: visible_works ≠ obtainable full corpus.

## 2. Collected (inventory / opened)

| creator | inventory | opened this Phase B pass | raw/ on disk |
|---|---:|---:|---:|
| yinhang_xiaojiejie | 61 | 15 | 15 JSON (+1 ytdlp.log) |
| zhinan_caijing | 57 | 15 | 15 |
| wenyifei_jijiu | 37 | 22 article full bodies (15 video rows retained non-COMPLETE) | 37 |
| hanxiuyun_jingji | 30 (B0.1 seed only) | **0** | **0** — **RUNNING/pending** |
| xiaolin_shuo | 51 | 40 (cap) | 40 |
| banfo_xianren | 25 | 25 | 25 |

## 3. COMPLETE

| creator | COMPLETE | note |
|---|---:|---|
| yinhang_xiaojiejie | **0** | Douyin spoken |
| zhinan_caijing | **0** | Douyin spoken |
| wenyifei_jijiu | **22** | all Toutiao articles |
| hanxiuyun_jingji | **0** | still PENDING / **RUNNING** |
| xiaolin_shuo | **20** | all Toutiao articles |
| banfo_xianren | **25** | all Toutiao articles |
| **Bank COMPLETE total** | **67** | |

**Mark clearly:** Douyin spoken COMPLETE=0 across bank / zhinan / (hanxiuyun still 0). Toutiao article COMPLETE solid for banfo / xiaolin / wenyifei.

## 4. Full transcript / fulltext count

| creator | transcripts/ files | index transcript_status FULLTEXT/FULL |
|---|---:|---:|
| yinhang_xiaojiejie | 0 | 0 |
| zhinan_caijing | 0 | 0 |
| wenyifei_jijiu | 22 | 22 FULLTEXT |
| hanxiuyun_jingji | 0 | 0 |
| xiaolin_shuo | 20 | 20 FULL |
| banfo_xianren | 25 | 25 FULLTEXT |
| **Total fulltext files** | **67** | |

## 5. Excluded (data rows in excluded.csv)

| creator | excluded |
|---|---:|
| yinhang_xiaojiejie | 0 |
| zhinan_caijing | 0 |
| wenyifei_jijiu | 6 (5 wrong_author + 1 login_prompt; B0.1) |
| hanxiuyun_jingji | 0 |
| xiaolin_shuo | 3 (2 black/buffering video + 1 non-creator notice) |
| banfo_xianren | 2 (1 HTTP 404 + 1 author mismatch 潘乱) |
| **Total** | **11** |

## 6. Failed (data rows in failed.csv)

| creator | failed |
|---|---:|
| yinhang_xiaojiejie | **16** (15 ui_transcript no_full_caption_panel + 1 yt-dlp_audio HTTP 403) |
| zhinan_caijing | 0 |
| wenyifei_jijiu | 0 |
| hanxiuyun_jingji | 0 |
| xiaolin_shuo | 0 |
| banfo_xianren | 0 |
| **Total** | **16** |

## 7. Coverage gaps

1. **Douyin spoken gap (critical):** `yinhang_xiaojiejie` and `zhinan_caijing` opened 15 seeds each with raw metadata saved but **COMPLETE=0** — UI exposes no full 文案/字幕 panel; yinhang also blocked on yt-dlp 403. No transcript files invented.
2. **hanxiuyun_jingji RUNNING/pending:** raw=0, transcripts=0, COMPLETE=0; 30 index rows remain `B01_VERIFIED_PENDING_FULLTEXT`. Do not report as delivered COMPLETE.
3. **Video non-COMPLETE on Toutiao mix creators:** wenyifei 15 Douyin/video rows NONE; xiaolin 20 videos METADATA_ONLY / not COMPLETE; 11 xiaolin URLs still PENDING_CAP.
4. **Inventory ≠ history:** all homepage inventories are loadable visible segments only (yinhang 61 of 518 UI works; zhinan 57 of 1422; banfo 12 end-scroll cards + seeds).
5. **wenyifei Douyin homepage:** session showed blank/shell works grid — Douyin expansion blocked this pass.

## 8. Paths

```
01_benchmark/creator_full_corpus/
  PHASE_B_STATUS.md
  PHASE_B_PLAN.md
  PHASE_B_CREATOR_IDS.md
  _aggregate/CORPUS_COVERAGE_ROLLUP.md
  _aggregate/PHASE_B_DELIVERY_DRAFT.md
  yinhang_xiaojiejie/{CORPUS_COVERAGE.md,corpus_index.csv,excluded.csv,failed.csv,raw/,transcripts/,url_inventory.jsonl}
  zhinan_caijing/...
  wenyifei_jijiu/...
  hanxiuyun_jingji/...
  xiaolin_shuo/...
  banfo_xianren/...
```

## 9. Commit SHA

**TBD**

## 10. Issue comment

**TBD** (Issue #6 comment link after post)

---

## One-line bank verdict (for Lan skim)

Toutiao article bank is delivery-ready (banfo 25 + xiaolin 20 + wenyifei 22 = **67 COMPLETE fulltext**). Douyin spoken bank is **not** (yinhang/zhinan COMPLETE=0; hanxiuyun still **RUNNING** with raw=0).
