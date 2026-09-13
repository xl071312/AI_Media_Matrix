#!/usr/bin/env python3
"""
Batch 002 Scale-Up Status Report
HERMES Role: DATA ENGINEER ONLY
"""
from pathlib import Path
import json
import csv

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
BATCH1 = BASE / "analysis_batches" / "batch_001"
BATCH2 = BASE / "analysis_batches" / "batch_002"
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
REGISTRY = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"

print("=== BATCH 002 SCALE-UP STATUS REPORT ===\n")

# Count samples
samples_001 = len(list(BATCH1.glob("sample_*")))
samples_002 = len(list(BATCH2.glob("sample_*")))

# Get unique CIDs
def get_unique_cids(batch_dir):
    cids = set()
    for s in batch_dir.glob("sample_*"):
        try:
            meta = json.load(open(s / "01_metadata.json"))
            cids.add(meta.get('content_id', ''))
        except:
            pass
    return cids

cids_001 = get_unique_cids(BATCH1)
cids_002 = get_unique_cids(BATCH2)
overlap = cids_001 & cids_002

# Check registry
registry_rows = 0
if REGISTRY.exists():
    with open(REGISTRY, encoding='utf-8') as f:
        registry_rows = len(list(csv.DictReader(f)))

# Check videos
total_videos = len(list(VIDEO_DIR.glob("*")))
new_candidates = 0
try:
    with open(BASE / "shards" / "hermes_real" / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
        selection = {row.get('aweme_id'): row for row in csv.DictReader(f)}
    all_existing = cids_001 | cids_002
    new_candidates = sum(1 for cid in selection if cid not in all_existing and (VIDEO_DIR / cid / "video.mp4").exists())
except:
    pass

# Check MediaCrawler status
mc_status = "FAILED"
mc_reasons = []
try:
    import redis
    mc_status = "PARTIAL"
except:
    mc_reasons.append("redis: MISSING")

try:
    import sqlalchemy
except:
    mc_reasons.append("sqlalchemy: MISSING")

# Check CDP
import socket
cdp_port = 9223
cdp_available = False
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex(('127.0.0.1', cdp_port))
    cdp_available = (result == 0)
    sock.close()
except:
    pass

print("=== CURRENT STATUS ===")
print(f"Batch 001: {samples_001} samples, {len(cids_001)} unique CIDs")
print(f"Batch 002: {samples_002} samples, {len(cids_002)} unique CIDs")
print(f"Overlap (duplicates): {len(overlap)}")
print(f"Registry entries: {registry_rows}")
print(f"Total videos: {total_videos}")
print(f"New candidates with video: {new_candidates}")
print(f"\nMediaCrawler: {mc_status}")
if mc_reasons:
    for r in mc_reasons:
        print(f"  - {r}")
print(f"CDP port {cdp_port}: {'AVAILABLE' if cdp_available else 'NOT AVAILABLE'}")

print(f"\n=== BLOCKERS ===")
print(f"1. MediaCrawler CDP connection failed (port 9223 not accessible)")
print(f"2. No new videos available locally (all 24 already in batches)")
print(f"3. Cannot achieve target of 30 NEW UNIQUE without new collection")

print(f"\n=== OPTIONS ===")
print(f"A) Start Chrome with --remote-debugging-port=9223 and retry MediaCrawler")
print(f"B) Use alternative data sources (Bilibili, XHS mirrors)")
print(f"C) Pause Scale-Up, complete Phase 3 with existing 24 samples")
print(f"D) Manual data entry for specific high-value content_ids from selection")

print(f"\n=== HERMES ROLE CONFIRMATION ===")
print(f"Role: DATA ENGINEER / EVIDENCE PACKAGER")
print(f"Status: NO LOGIC ANALYSIS GENERATED")
print(f"Status: NO DEEP ANALYSIS GENERATED")
print(f"Status: WAITING_FOR_LAN_DECISION")
