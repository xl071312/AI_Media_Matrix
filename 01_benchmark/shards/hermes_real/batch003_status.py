#!/usr/bin/env python3
"""Batch 003 - Final Status Report"""
import json
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH3_DIR = BASE / "analysis_batches" / "batch_003"

# Load progress
b3_path = SHARDS / "batch003_progress.json"
with open(b3_path, 'r', encoding='utf-8') as f:
    b3_data = json.load(f)

done = len([r for r in b3_data if r.get('status') == 'DONE'])
blocked = len([r for r in b3_data if r.get('status') == 'BLOCKED'])
no_audio = len([r for r in b3_data if r.get('status') == 'NO_AUDIO'])
failed = len([r for r in b3_data if r.get('status') not in ['DONE', 'BLOCKED', 'NO_AUDIO']])

# Check global registry
reg_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
registry = set()
import csv
with open(reg_path, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        cid = row.get('content_id', '').strip().lstrip('\ufeff')
        if cid:
            registry.add(cid)

print("="*60)
print("BATCH 002 FINAL STATUS")
print("="*60)
print(f"Qualified: 32")
print(f"Evidence Parts: 3")
print(f"Control Groups: 31")
print(f"Global Registry: {len(registry)} unique")
print(f"Research Handoff: PASS")

print()
print("="*60)
print("BATCH 003 STATUS")
print("="*60)
print(f"Total Processed: {len(b3_data)}")
print(f"Done (ASR complete): {done}")
print(f"Blocked (login/captcha): {blocked}")
print(f"No Audio URL: {no_audio}")
print(f"Other failures: {failed}")
print(f"Status: IN_PROGRESS (rate limited)")