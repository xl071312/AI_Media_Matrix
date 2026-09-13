#!/usr/bin/env python3
"""RC6C: Create wave_003_real with source-backed articles only"""
import json
import hashlib
import csv
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")
SRC = BASE / "01_benchmark/analysis_batches/batch_004_toutiao/SEED_WAVE_003"
HANDOFF = BASE / "handoff/chatgpt/batch_004/wave_003_real"
REAL_DIR = BASE / "handoff/chatgpt/batch_004/wave_003_real"
INVALID_DIR = BASE / "handoff/chatgpt/batch_004/wave_003_invalid_rc6b"

# Create directories
REAL_DIR.mkdir(parents=True, exist_ok=True)

# Already quarantined items from invalid batch
QUARANTINE_PATH = INVALID_DIR / "INVALID_MANIFEST.csv"
quarantined = set()
if QUARANTINE_PATH.exists():
    with open(QUARANTINE_PATH, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            quarantined.add(row['content_id'])

print(f"Quarantined items: {len(quarantined)}")

# Remaining items in wave_003 that are NOT quarantined
existing = []
for p in (BASE / "handoff/chatgpt/batch_004/wave_003").glob("*.json"):
    cid = p.stem
    if cid not in quarantined and cid != "DISCOVERY_LOG" and cid != "FULLTEXT_QA" and cid != "TOPIC_GATE":
        existing.append(cid)

print(f"Existing non-quarantined: {len(existing)}")

# Move valid items to wave_003_real and create proper files
for cid in existing:
    src_path = BASE / "handoff/chatgpt/batch_004/wave_003" / f"{cid}.json"
    dst_path = REAL_DIR / f"{cid}.json"
    if src_path.exists():
        import shutil
        shutil.copy2(str(src_path), str(dst_path))
        print(f"Copied: {cid}")

print(f"\nCreated {len(existing)} items in wave_003_real")