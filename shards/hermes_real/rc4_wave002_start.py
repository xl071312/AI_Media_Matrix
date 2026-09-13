#!/usr/bin/env python3
"""RC4: Wave002 Production - 20 NEW UNIQUE articles with real fulltext"""
import json
import csv
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SRC = BASE / "analysis_batches/batch_004_toutiao"
HANDOFF_W2 = BASE.parent / "handoff/chatgpt/batch_004/wave_002"
GLOBAL_REGISTRY = BASE.parent.parent / "GLOBAL_CONTENT_ID_REGISTRY.csv"

# Load existing Wave001 CIDs to exclude
wave001_cids = set()
for p in (SRC / "SEED_WAVE_001_REFETCH").glob("*.json"):
    wave001_cids.add(p.stem)

# Load global registry
existing_cids = set()
if GLOBAL_REGISTRY.exists():
    with open(GLOBAL_REGISTRY, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_cids.add(row.get('content_id', '').strip())

# Load Wave002 existing
wave002_cids = set()
w2_dir = SRC / "SEED_WAVE_002"
if w2_dir.exists():
    for p in w2_dir.glob("*.json"):
        wave002_cids.add(p.stem)

# Candidates from CSV
candidates = []
cand_file = SRC / "TOUTIAO_WAVE002_CANDIDATES.csv"
if cand_file.exists():
    with open(cand_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row.get('content_id', '').strip()
            title = row.get('title', '')[:80]
            if cid and cid not in wave001_cids and cid not in existing_cids and cid not in wave002_cids:
                candidates.append({'cid': cid, 'title': title})

print(f"Wave002 Production Ready")
print(f"  Wave001 CIDs (excluded): {len(wave001_cids)}")
print(f"  Global Registry CIDs (excluded): {len(existing_cids)}")
print(f"  Wave002 Existing (excluded): {len(wave002_cids)}")
print(f"  New Unique Candidates: {len(candidates)}")
print()
print("Candidates:")
for i, c in enumerate(candidates[:10], 1):
    print(f"  {i}. {c['cid']}: {c['title'][:50]}...")
if len(candidates) > 10:
    print(f"  ... and {len(candidates)-10} more")