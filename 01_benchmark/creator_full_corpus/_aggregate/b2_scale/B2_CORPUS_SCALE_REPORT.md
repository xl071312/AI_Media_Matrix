# B2_CORPUS_SCALE_REPORT — Issue #6 Phase B2

Written: 2026-09-19T12:38:19.140628+00:00

## Gate
Phase B1.1 ACCEPT. Phase B2 CORPUS SCALE-OUT + TRANSCRIPT QA.
**No Phase C / Voice Profile / new 口播稿.**

## Final 6-person core roster
1. 巫师财经 (`wushi_caijing`) — AUX_ORAL (replaces 银行小姐姐 oral slot)
2. 毕导 (`bidu`) — AUX_ORAL (replaces 直男财经 oral slot)
3. 老师好我叫何同学 (`hetongxue`) — AUX_ORAL (replaces 韩秀云讲经济 oral slot)
4. 小Lin说 (`xiaolin_shuo`) — TEXT + **4th AUX_ORAL**
5. 温义飞的急救财经 (`wenyifei_jijiu`) — TEXT
6. 硬核的半佛仙人 (`banfo_xianren`) — TEXT

Replaced oral slots retained as historical `REPLACED_ORAL_SLOT` evidence (do not delete).

## 4th oral creator
**小Lin说** — YouTube channel `UCilwQlk62k1z7aUEZPOB6yw`; proof 3/3 PASS then scaled to ≥30 FULL_SPOKEN. Tag `AUX_ORAL`; TEXT identity kept.

## FULL_SPOKEN counts
| creator | FULL_SPOKEN | target | tag |
|---|---:|---:|---|
| 巫师财经 | 51 | ≥50 | AUX_ORAL |
| 毕导 | 50 | ≥50 | AUX_ORAL |
| 老师好我叫何同学 | 50 | ≥50 | AUX_ORAL |
| 小Lin说 | 30 | ≥30 | AUX_ORAL |
| **Total** | **181** | ≥180 / ≥4 creators | |

Gate spoken: **PASS**

## COMPLETE_TEXT counts
| creator | COMPLETE_TEXT | role |
|---|---:|---|
| 温义飞的急救财经 | 55 | TEXT |
| 小Lin说 | 31 | TEXT (+ oral) |
| 硬核的半佛仙人 | 77 | TEXT |
| **Total** | **163** | ≥120 |

Gate text: **PASS**

## Transcript QA (5 random / creator)
Sampled videos reviewed on head / mid / tail windows for leak, digits/names, and spoken connectors (其实/然后/但是/你看/我觉得/啊/呢/吧).

| metric | count |
|---|---:|
| QA sample size | 20 |
| spoken_marker_eligible=YES | 11 |
| spoken_marker_eligible=NO | 9 |
| manual_qa PASS | 11 |
| manual_qa PASS_LOGIC_ONLY / RESTRICTED | 9 |

Policy: YouTube auto-captions and tiny ASR → `spoken_marker_eligible=NO` (logic OK). faster-whisper **base** samples with connectors in ≥2 windows → YES. Unsamped base ASR rows marked `YES_UNSAMPLED` pending deeper fingerprint work.

## Artifacts
- `_aggregate/B2_CORPUS_SCALE_REPORT.md`
- `_aggregate/b2_oral_manifest.csv`
- `_aggregate/b2_transcript_qa.csv`
- `_aggregate/b2_text_manifest.csv`
- `_aggregate/corpus_manifest_sha256.csv` (updated)
- oral bodies under `_aggregate/b2_scale/oral/<creator_id>/`

## Blockers
- Bilibili in-env still **412**; oral scale used YouTube captions/ASR only (AUX_ORAL).
- Douyin spoken still blocked (403 / no 文案) — not revisited for replaced creators.
- Some ultra-short bidu clips failed <200 chars ASR density.
- TEXT discovery required Toutiao search + author-matched `info/v2` (no-login homepage list empty).

## Stop
Waiting Lan/ChatGPT acceptance. **Do not enter Phase C.**
