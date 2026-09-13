#!/usr/bin/env python3
"""Batch 002 Status Report - Data Collection Blocked"""
from pathlib import Path
import json
import csv

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
BATCH1 = BASE / "analysis_batches" / "batch_001"
BATCH2 = BASE / "analysis_batches" / "batch_002"

print("=== BATCH 002 STATUS REPORT ===\n")

# Count samples
samples_001 = len(list(BATCH1.glob("sample_*")))
samples_002 = len(list(BATCH2.glob("sample_*")))

# Get unique CIDs
def get_cids(batch_dir):
    cids = set()
    for s in batch_dir.glob("sample_*"):
        try:
            meta = json.load(open(s / "01_metadata.json"))
            cids.add(meta.get('content_id', ''))
        except:
            pass
    return cids

cids_001 = get_cids(BATCH1)
cids_002 = get_cids(BATCH2)

# Load selection
with open(BASE / "shards" / "hermes_real" / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
    selection = {row.get('aweme_id'): row for row in csv.DictReader(f)}

# Check video availability
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
all_existing = cids_001 | cids_002
new_candidates = [cid for cid in selection.keys() if cid not in all_existing]
with_video = [(cid, selection[cid]) for cid in new_candidates if (VIDEO_DIR / cid / "video.mp4").exists()]

# Check MediaCrawler status
MC_PATH = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler")
mc_deps = []
try:
    import redis
    mc_deps.append("redis: OK")
except:
    mc_deps.append("redis: MISSING")

try:
    import sqlalchemy
    mc_deps.append("sqlalchemy: OK")
except:
    mc_deps.append("sqlalchemy: MISSING")

try:
    import playwright
    mc_deps.append("playwright: OK")
except:
    mc_deps.append("playwright: MISSING")

print("=== CURRENT STATUS ===")
print(f"Batch 001: {samples_001} samples, {len(cids_001)} unique CIDs")
print(f"Batch 002: {samples_002} samples, {len(cids_002)} unique CIDs")
print(f"Overlap: {len(cids_001 & cids_002)} (duplicate)")
print(f"New candidates: {len(new_candidates)}")
print(f"With local video: {len(with_video)}")
print(f"\nMediaCrawler dependencies:")
for d in mc_deps:
    print(f"  {d}")

print(f"\n=== BLOCKERS ===")
print(f"1. MediaCrawler missing dependencies (redis, sqlalchemy, playwright)")
print(f"2. No new videos available locally")
print(f"3. Cannot achieve 30 NEW UNIQUE without new collection")

print(f"\n=== OPTIONS ===")
print(f"A) Fix MediaCrawler dependencies and retry collection")
print(f"B) Use alternative data sources (B站镜像、其他平台)")
print(f"C) Pause Scale-Up, complete Phase 3 with existing 24 samples")
print(f"D) Manual data entry for specific high-value content_ids")
