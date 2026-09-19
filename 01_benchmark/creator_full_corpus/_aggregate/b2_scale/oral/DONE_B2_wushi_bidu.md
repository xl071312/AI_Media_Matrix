# DONE B2 Phase B2 — wushi_caijing + bidu

Generated: 2026-09-19 12:37:30 PT

## Success criteria
- bidu (毕导) PASS >= 50: **50** (FAIL=7)
- wushi_caijing (巫师财经) PASS >= 50: **51** (FAIL=4)

PASS definition: `pass=true` AND `spoken_chars_nospace>=200` AND `transcript_completeness=FULL_SPOKEN`

## Sample URLs (3 each)

### bidu
- https://www.youtube.com/watch?v=-8RLg3epEIc
- https://www.youtube.com/watch?v=-ZBxFmVquvg
- https://www.youtube.com/watch?v=152w4-Vnp80

### wushi_caijing
- https://www.youtube.com/watch?v=-McZ6nbGRUM
- https://www.youtube.com/watch?v=2Y8fCRSZwY4
- https://www.youtube.com/watch?v=2oFB24-8_X4

## Blockers / fails
- bidu fails: 7 (ultra-short/low-speech; some early yt-dlp JS-runtime download errors)
- wushi fails: 4 (spoken_chars_nospace < 200)

### bidu fail sample
```json
[
  {
    "video_id": "9obyJ6qhZvs",
    "chars": 103,
    "error": ""
  },
  {
    "video_id": "A9o6V0bs1p4",
    "chars": 0,
    "error": ""
  },
  {
    "video_id": "WhF4_8W1tUA",
    "chars": 0,
    "error": "nload failed: \" + (r.stderr[-800:] if r else \"\"))\nRuntimeError: download failed: WARNING: [youtube] No supported JavaScript runtime could be found. Only deno is"
  },
  {
    "video_id": "ZyeRjo1rY1k",
    "chars": 6,
    "error": ""
  },
  {
    "video_id": "bpHah1Wryzc",
    "chars": 0,
    "error": "nload failed: \" + (r.stderr[-800:] if r else \"\"))\nRuntimeError: download failed: WARNING: [youtube] No supported JavaScript runtime could be found. Only deno is"
  }
]
```

### wushi fail sample
```json
[
  {
    "video_id": "DQD24Nwg1Go",
    "chars": 134,
    "error": ""
  },
  {
    "video_id": "JCiyKb3swZ0",
    "chars": 193,
    "error": ""
  },
  {
    "video_id": "kHHBqvWN3oU",
    "chars": 95,
    "error": ""
  },
  {
    "video_id": "ns0m-fHn03w",
    "chars": 154,
    "error": ""
  }
]
```

## Notes
- Platform: youtube; tag: AUX_ORAL (never Douyin PRIMARY; no Bilibili new ingest)
- ASR: faster-whisper **base** int8 (captions preferred when available)
- Ingest fixes: `--js-runtimes node`; `--video-id=` for leading-dash IDs
- Queues short-first; wavs deleted after ingest
- Progress: `oral/_progress_wushi_bidu.log`
