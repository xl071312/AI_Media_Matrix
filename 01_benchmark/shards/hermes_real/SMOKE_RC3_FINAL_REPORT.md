# 【Douyin Media Smoke RC3】- Final Report

**Date**: 2026-09-10
**Status**: PARTIAL_PASS (Audio Pipeline Fixed)
**simulated**: 0

---

## Executive Summary

| Metric | Result | Status |
|--------|--------|--------|
| NEW UNIQUE | 3/3 | ✓ PASS |
| PAGE PLAYABLE | 3/3 | ✓ PASS |
| VIDEO TRACK | 3/3 | ✓ PASS |
| AUDIO TRACK | 3/3 | ✓ PASS |
| ASR | 2/3 | ⚠ PARTIAL |
| Verified Performance | 3/3 | ✓ PASS |
| simulated | 0 | ✓ |

**Verdict**: SMOKE_RC3 = **PARTIAL_PASS**

**Key Achievement**: Audio pipeline fixed. Previously downloaded videos were video-only. Now extracting separate audio representation from `media-audio-und-mp4a` or equivalent real audio resource in CDN URLs.

---

## Sample Details

### SMOKE_001: 7683219193294114063
| Field | Value |
|-------|-------|
| Title | 第10集 \| 高中生PC得艾滋的一生 #人生副本 #热门 |
| Author | 剧本人生活馆 |
| Duration | 333s (05:33) |
| Size | 16.5 MB (muxed) |
| Likes | 8.8万 | Comments | 1.3万 | Favorites | 5973 | Shares | 9.3万 |
| Publish | 2026-09-08 19:00 |
| ASR Segments | 267 |
| ASR Chars | 1844 |
| Status | ✓ OK |

### SMOKE_002: 7682806976379620660
| Field | Value |
|-------|-------|
| Title | 第178集 \| 新赛季版本之子，汤姆叔叔的轮椅 |
| Author | 安澜（背锅大王） |
| Duration | 162s (02:42) |
| Size | 122.2 MB (muxed) |
| Likes | 52.8万 | Comments | 5297 | Favorites | 10.1万 | Shares | 7.3万 |
| Publish | 2026-09-07 18:30 |
| ASR Segments | 123 |
| ASR Chars | 907 |
| Status | ✓ OK |

### SMOKE_003: 7682728905966423334
| Field | Value |
|-------|-------|
| Title | 《我的妹妹不可爱》上部-超级加长版 |
| Author | 罗臣臣 |
| Duration | 2828s (47:08) |
| Size | 150.7 MB (muxed) |
| Likes | 72.8万 | Comments | 2.7万 | Favorites | 17.8万 | Shares | 50.4万 |
| Publish | 2026-09-07 03:26 |
| ASR Segments | 36 (60s sample) |
| ASR Chars | 700 |
| Status | ⚠ TIMEOUT (long video) |

---

## Technical Notes

### Audio Pipeline Fix
- **Problem**: Previous download only captured video track (H.265, no audio)
- **Root Cause**: Was extracting only `media-video-*` URLs from performance entries
- **Solution**: Now extracting both `media-video-*` AND `media-audio-*` URLs separately
- **Mux Method**: ffmpeg `-c:v copy -c:a copy` (no re-encoding)
- **Audio Format**: AAC codec in MP4 container (`media-audio-und-mp4a`)

### Download Method
- Route: Browser CDP → Performance Entries → CDN URL extraction
- Separate video and audio streams detected via resource filtering
- Audio extracted from independent CDN URL with mp4a codec

### ASR Results
- Model: Systran/faster-whisper-base (CPU, int8)
- Language: zh (Chinese)
- 2/3 videos completed successfully
- 1 long video (47min) timed out after 600s - partial transcription obtained

---

## Pipeline Status

```
✓ DOM Discovery: PASS
✓ Video Capture: PASS
✓ Separate Audio Capture: PASS
✓ FFmpeg Mux: PASS
✓ ASR (short/medium): PASS
✗ ASR (long video): TIMEOUT
```

---

## Files Generated

```
F:\workspace\AI_Media_Matrix\01_benchmark\
├── media\batch_002_smoke\
│   ├── 7683219193294114063.muxed.mp4 (16.5 MB) ✓
│   ├── 7682806976379620660.muxed.mp4 (122.2 MB) ✓
│   └── 7682728905966423334.muxed.mp4 (150.7 MB) ✓
│
└── shards\hermes_real\
    ├── transcripts_v2\
    │   ├── 7683219193294114063_raw.json (267 segments)
    │   ├── 7682806976379620660_raw.json (123 segments)
    │   └── 7682728905966423334_raw.json (36 segments, 60s sample)
    ├── smoke_rc3_result.json
    └── SMOKE_RC3_FINAL_REPORT.md
```

---

## Batch002 Status

**Topic Gate**: Implemented
- ON_TOPIC candidates: 77
- OFF_TOPIC filtered: 23

**Current Progress**:
- Batch002 Qualified New: 0/30 (RC3 samples marked PIPELINE_SMOKE_ONLY)
- Pipeline ready for production run

**Next Steps**:
1. Open pages via browser for top 30 ON_TOPIC candidates
2. Extract metadata + CDN URLs
3. Download + mux + ASR
4. Target: 30 NEW UNIQUE with transcripts

---

## SMOKE_RC3 Verdict

```
✓ NEW UNIQUE: 3/3
✓ PAGE PLAYABLE: 3/3
✓ VIDEO TRACK: 3/3
✓ AUDIO TRACK: 3/3
⚠ ASR: 2/3 (1 long video timeout)
✓ Verified Performance: 3/3

simulated: 0
Download Route: Browser Network Capture (CDP)
Login Required: NO
MediaCrawler Search: DEGRADED
DOM Discovery: PASS
```

**SMOKE_RC3 = PARTIAL_PASS** (Audio pipeline verified operational)