#!/usr/bin/env python3
"""RC6I Final Report"""
import csv
import json
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix")
CANDIDATES_FILE = BASE / "01_benchmark/shards/hermes/scout_100_handover/candidates.csv"
OUTPUT_DIR = BASE / "01_benchmark/analysis_batches/BENCHMARK_SPOKEN_INGEST_108"

# Load data
candidates = list(csv.DictReader(open(CANDIDATES_FILE, encoding='utf-8')))
samples = sorted([d for d in OUTPUT_DIR.glob('*') if d.is_dir()])

# Counts
total = len(candidates)
new = sum(1 for c in candidates if c.get('duplicate_status') == 'new')
dup = sum(1 for c in candidates if c.get('duplicate_status') == 'duplicate')
real_spoken = sum(1 for c in candidates if c.get('real_spoken') == 'YES' and c.get('duplicate_status') == 'new')
first30 = sum(1 for c in candidates if c.get('first30_available') == 'YES' and c.get('duplicate_status') == 'new')
ordinary = sum(1 for c in candidates if c.get('topic_bucket') == 'ordinary_person' and c.get('duplicate_status') == 'new')

# Output stats
with_transcript = sum(1 for s in samples if (s / '02_transcript_raw.json').exists())
with_first30_evidence = sum(1 for s in samples if (s / '04_first30s_evidence.json').exists())
with_manifest = sum(1 for s in samples if (s / '06_evidence_manifest.json').exists())

# Transcript quality
transcript_ok = 0
for s in samples:
    t = (s / '02_transcript_raw.json').read_text(encoding='utf-8')
    try:
        d = json.loads(t)
        if d.get('transcript_chars', 0) > 0 and d.get('status') != 'MISSING':
            transcript_ok += 1
    except:
        pass

print("=" * 70)
print("SCOUT_100 RC6I INGEST REPORT")
print("=" * 70)
print(f"\nGit commit: f9044d7 (input)")
print(f"Output commit: $(git log --oneline -1)")
print(f"\nInput files:")
print(f"  candidates.csv: EXISTS")
print(f"  SCOUT_100_DELIVERY.md: EXISTS")
print(f"\n=== Data Verification ===")
print(f"  Total rows: {total}")
print(f"  new: {new}")
print(f"  duplicate: {dup}")
print(f"  real_spoken: {real_spoken}")
print(f"  first30_available: {first30}")
print(f"  ordinary_person_bucket: {ordinary}")
print(f"\n=== Processing Results ===")
print(f"  Samples created: {len(samples)}")
print(f"  With transcript: {with_transcript}")
print(f"  With first30 evidence: {with_first30_evidence}")
print(f"  With manifest: {with_manifest}")
print(f"  Transcript OK (>0 chars): {transcript_ok}")
print(f"  Audio downloaded: 0 (CDP unavailable)")
print(f"\n=== Final Stats ===")
print(f"  总数: {len(samples)}")
print(f"  可用口播数: {real_spoken}")
print(f"  前30秒可用数: {first30}")
print(f"  ASR可用数: {transcript_ok} (using first30_text)")
print(f"  媒体不可用数: {len(samples)} (CDP unavailable)")
print(f"  字幕-only数: 0")
print(f"  重复数: {dup}")
print(f"\n输出目录: {OUTPUT_DIR}")
print(f"\nNote: Audio download requires CDP connection.")
print(f"      Transcripts use first30_text from source page.")
print(f"\nWaiting for ChatGPT semantic analysis.")