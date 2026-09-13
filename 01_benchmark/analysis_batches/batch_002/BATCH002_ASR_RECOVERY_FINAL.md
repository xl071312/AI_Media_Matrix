# 【Batch002 ASR Recovery RC3】- Final Status

**Date**: 2026-09-10  
**Status**: ASR_COMPLETE (12/12)  
**simulated**: 0

---

## Summary

| Metric | Value |
|--------|-------|
| GPU Present | YES (NVIDIA GTX 750, 2GB) |
| CUDA ASR | FAIL (float16 not supported) |
| ASR Route | **CPU_CHUNKED** |
| Existing Audio | 12 |
| ASR Complete | **12/12** ✓ |
| Transcript Usable | **12/12** ✓ |
| Chunk Failures | 0 |
| Average RTF | ~0.5x |

| Page Verified | 20/30 |
| Media Ready | 12/30 |
| Batch Qualified | 12/30 |

---

## ASR Results

All 12 audio files processed successfully using CPU chunked approach:

| CID | Duration | Segments | Chars | Status |
|-----|----------|----------|-------|--------|
| 7441108716197301519 | 02:09 | 72 | 542 | ✓ |
| 7477191872570477839 | 05:44 | 157 | 1,731 | ✓ |
| 7511664213547519243 | 03:36 | 135 | 1,367 | ✓ |
| 7559914938827803950 | 18:55 | 821 | 6,266 | ✓ |
| 7564348993203948810 | 15:22 | 874 | 5,847 | ✓ |
| 7584407684042165541 | 05:26 | 142 | 1,811 | ✓ |
| 7592567871297932582 | 01:44 | 93 | 540 | ✓ |
| 7599188562650734516 | 11:39 | 400 | 3,195 | ✓ |
| 7600369823520073126 | 06:30 | 281 | 2,175 | ✓ |
| 7647446230122356665 | 03:36 | 145 | 1,066 | ✓ |
| 7666798588350065338 | 03:04 | 89 | 1,116 | ✓ |
| 7673172635974421760 | 03:54 | 164 | 1,452 | ✓ |

**Total**: 12/12 ASR Complete (100%)

---

## Hard QA Checklist

| Check | Target | Current |
|-------|--------|---------|
| NEW UNIQUE | 30 | 12 |
| Cross-Batch Duplicate | 0 | 0 ✓ |
| Primary Topic Assigned | 30 | 12 |
| ON_TOPIC | 30 | 12 |
| SPEECH_PRESENT | 30 | 12 |
| TRANSCRIPT_USABLE | 30 | **12** ✓ |
| Verified Performance >= 24 | >=24 | 12 |
| simulated | 0 | 0 ✓ |

**BATCH002 = COMPLETE**: NOT_YET (need 18 more)

---

## Next Actions

1. Continue page verification for remaining 10 candidates
2. Download media for additional candidates
3. Run ASR on new downloads
4. Target: 30 qualified transcripts

---

**Status**: ASR pipeline fixed. 12/30 qualified. Continuing production.