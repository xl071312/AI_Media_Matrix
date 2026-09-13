#!/usr/bin/env python3
"""RC6D: Initialize gapfill_100 with dedupe tracking"""
import csv
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")
GAPFILL = BASE / "handoff/chatgpt/gapfill_100"
TOUTIAO = GAPFILL / "toutiao"

# Create directories
TOUTIAO.mkdir(parents=True, exist_ok=True)
(GAPFILL / "douyin").mkdir(parents=True, exist_ok=True)

# Collect all known CIDs for dedupe
import json
known_ids = set()

# All batches
for batch_dir in [
    BASE / "01_benchmark/analysis_batches/batch_001",
    BASE / "01_benchmark/analysis_batches/batch_002",
    BASE / "01_benchmark/analysis_batches/batch_003",
    BASE / "01_benchmark/analysis_batches/batch_004_toutiao/SEED_WAVE_001_REFETCH",
    BASE / "01_benchmark/analysis_batches/batch_004_toutiao/SEED_WAVE_002",
    BASE / "handoff/chatgpt/batch_004/wave_003_invalid_rc6b",
]:
    if batch_dir.exists():
        for p in batch_dir.glob("*.json"):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cid = data.get('content_id', '')
                    if cid:
                        known_ids.add(cid)
            except:
                # Try using filename as CID
                cid = p.stem
                if cid.isdigit():
                    known_ids.add(cid)

print(f"Known CIDs for dedupe: {len(known_ids)}")

# Create PREFETCH_DEDUPE.csv
dedupe_path = GAPFILL / "PREFETCH_DEDUPE.csv"
with open(dedupe_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['content_id', 'found_in', 'status', 'discovered_at'])
    # Write header info
    writer.writerow(['', f'Total known: {len(known_ids)}', 'TRACKING', ''])

print(f"Created {dedupe_path}")
print(f"Known IDs sample: {list(known_ids)[:5]}")