# B2 Phase B2 Oral Scale-Out — DONE

## Results (PT ~2026-09-19 12:11)
| Creator | ID | Proof | FULL_SPOKEN PASS | Target | Status |
|---|---|---|---|---|---|
| 老师好我叫何同学 | hetongxue | n/a | **50** | >=50 | PASS |
| 小Lin说 | xiaolin_shuo | **3/3** (>=2/3) | **30** | >=30 after proof | PASS |

## Proof (xiaolin)
- File: `oral/xiaolin_shuo/PROOF_3.md`
- T7z71yENz94, AJLe1AEgz5M, KosgUhdAL5w — all PASS via youtube_public_caption
- Channel verified: UCilwQlk62k1z7aUEZPOB6yw
- Scaled with tag `AUX_ORAL`, TEXT identity `xiaolin_shuo`

## Blockers / notes
- hetongxue `rpOI910KgJU` (piano/music): ASR chars=0 → FAIL (skipped; not needed for target)
- hetongxue `-NkxRoyHuzY`: argparse leading-dash bug in batch (`--video-id` form); fixed via `--video-id=` and manual ingest → PASS
- hetongxue `bCGJwdPJ9Lc`: ASR exception mid-run (rc=1); skipped; target reached via later vids
- Captions-first path dominant; ASR fallback (faster-whisper **base**) used when no usable zh captions
- Batches stopped at target (`TARGET_REACHED`); no endless overshoot
- Progress log: `oral/_progress_hetongxue_xiaolin.log`
