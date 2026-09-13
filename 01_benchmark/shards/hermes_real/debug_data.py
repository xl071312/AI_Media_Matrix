#!/usr/bin/env python3
"""Debug: Check all available data"""
from pathlib import Path
import csv

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")

print("=== DEBUG: DATA AVAILABILITY ===\n")

# Load selection
with open(SHARDS / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    selection = {row.get('aweme_id'): row for row in reader}

print(f"Selection entries: {len(selection)}")

# Check all three IDs
check_ids = ['7302348364815928612', '7546212425998454074', '7647797848847439706']

for cid in check_ids:
    print(f"\n--- {cid} ---")
    
    # Check in selection
    if cid in selection:
        print(f"  In selection: YES")
        row = selection[cid]
        print(f"  Title: {row.get('desc', '')[:50]}...")
        print(f"  Viral Type: {row.get('viral_type', '')}")
        print(f"  Likes: {row.get('liked_count', '')}")
    else:
        print(f"  In selection: NO")
    
    # Check transcript
    trans_file = TRANSCRIPT_DIR / f"{cid}_raw.json"
    if trans_file.exists():
        print(f"  Transcript: YES ({trans_file.stat().st_size} bytes)")
    else:
        print(f"  Transcript: NO")
    
    # Check video
    video_path = VIDEO_DIR / cid / "video.mp4"
    if video_path.exists():
        print(f"  Video: YES ({video_path.stat().st_size / 1024 / 1024:.1f} MB)")
    else:
        print(f"  Video: NO")
    
    # Check both
    if trans_file.exists() and video_path.exists():
        print(f"  STATUS: AVAILABLE ✓")
    else:
        print(f"  STATUS: INCOMPLETE ✗")
