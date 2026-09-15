# BENCHMARK_SPOKEN_INGEST_108 Status

**Completed**: 2026-09-15T04:35:18.521841
**Status**: MECHANICAL_INGEST_COMPLETE

## Input Summary

| Metric | Value |
|--------|-------|
| Total rows in candidates.csv | 112 |
| Header rows | 1 |
| Data rows | 112 |
| New samples (duplicate_status=new) | 108 |
| Duplicate samples | 4 |

## Processing Summary

| Metric | Value |
|--------|-------|
| Samples created | 108 |
| Has transcript | 108 |
| ASR usable | 108 |
| First 30s available | 108 |
| Real spoken (per source) | 103 |
| Failed | 0 |

## Output Structure

```
01_benchmark/analysis_batches/BENCHMARK_SPOKEN_INGEST_108/
├── dy_XXXXXXXXXXXXXXX/          # Each sample folder
│   ├── 01_metadata.json         # Source metadata
│   ├── 02_transcript_raw.json   # ASR/raw transcript
│   ├── 03_transcript_normalized.json
│   ├── 04_first30s_evidence.json
│   ├── 05_metrics.json
│   ├── 06_evidence_manifest.json
│   └── (audio.m4a if downloaded)
└── BATCH_STATUS.md
```

## Notes

- Audio download pending CDP connection
- Transcripts use first30_text from source page
- No semantic analysis performed
- Verified Logic Corpus unchanged: 85/100
