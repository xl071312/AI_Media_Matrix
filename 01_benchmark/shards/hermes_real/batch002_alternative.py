#!/usr/bin/env python3
"""
Batch 002 - Alternative Data Collection
Uses DOM scraping via CDP to get new video data
HERMES Role: DATA ENGINEER ONLY
"""
import asyncio
import json
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH_DIR = BASE / "analysis_batches" / "batch_002"
BATCH_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"

# Load existing CIDs
EXISTING_CIDS = set()
for batch in BASE.glob("analysis_batches/batch_*"):
    for s in batch.glob("sample_*"):
        try:
            meta = json.load(open(s / "01_metadata.json"))
            EXISTING_CIDS.add(meta.get('content_id', ''))
        except:
            pass

# Load selection
with open(SHARDS / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
    selection = {row.get('aweme_id'): row for row in csv.DictReader(f)}

def get_new_candidates():
    """Get candidates not in existing batches"""
    candidates = []
    for cid, row in selection.items():
        if cid not in EXISTING_CIDS:
            candidates.append((cid, row))
    return candidates

async def scrape_via_browser(cid, row):
    """Try to get metadata via browser (if not already downloaded)"""
    # This is a placeholder - actual implementation would use browser automation
    # For now, we'll just check if video exists
    video_path = VIDEO_DIR / cid / "video.mp4"
    if video_path.exists():
        return {'has_video': True, 'path': str(video_path)}
    return {'has_video': False}

async def main():
    print("=== BATCH 002 - ALTERNATIVE APPROACH ===\n")
    
    # Get new candidates
    candidates = get_new_candidates()
    print(f"New candidates from selection: {len(candidates)}")
    
    # Check which have videos
    with_video = []
    without_video = []
    for cid, row in candidates:
        video_path = VIDEO_DIR / cid / "video.mp4"
        if video_path.exists():
            with_video.append((cid, row, video_path))
        else:
            without_video.append((cid, row))
    
    print(f"With local videos: {len(with_video)}")
    print(f"Without videos: {len(without_video)}")
    
    # Show first few without videos
    if without_video:
        print(f"\nFirst 5 without videos:")
        for cid, row in without_video[:5]:
            print(f"  {cid}: {row.get('nickname', 'N/A')}")
    
    # Summary
    print(f"\n=== BUDGET ANALYSIS ===")
    print(f"Batch 001 unique: {len(EXISTING_CIDS)}")
    print(f"Available for Batch 002: {len(with_video)}")
    print(f"Need for target (30): {30 - len(with_video)}")
    
    if len(with_video) >= 30:
        print(f"\n✓ Can proceed with {len(with_video)} samples")
    else:
        print(f"\n✗ Cannot reach target of 30 new unique")
        print(f"  Options:")
        print(f"  1. Run MediaCrawler to download {30 - len(with_video)} more videos")
        print(f"  2. Use Bilibili mirror data")
        print(f"  3. Extend to Batch 003/004 for remaining")

if __name__ == "__main__":
    asyncio.run(main())
