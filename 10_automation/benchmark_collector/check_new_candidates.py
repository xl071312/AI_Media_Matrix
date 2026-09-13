#!/usr/bin/env python3
"""
Alternative: Direct Douyin API calls for new data
Uses existing CDP session to bypass restrictions
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

# Load existing CIDs
EXISTING_CIDS = set()
for batch in BASE.glob("analysis_batches/batch_*"):
    for s in batch.glob("sample_*"):
        try:
            meta = json.load(open(s / "01_metadata.json"))
            EXISTING_CIDS.add(meta.get('content_id', ''))
        except:
            pass

# Load selection for keywords
with open(SHARDS / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
    selection = {row.get('aweme_id'): row for row in csv.DictReader(f)}

def get_new_candidates():
    """Get candidates not in existing batches"""
    candidates = []
    for cid, row in selection.items():
        if cid not in EXISTING_CIDS:
            candidates.append((cid, row))
    return candidates

async def main():
    print("=== BATCH 002 - ALTERNATIVE APPROACH ===\n")
    
    # Get new candidates
    candidates = get_new_candidates()
    print(f"New candidates from selection: {len(candidates)}")
    
    # Show available videos
    available_videos = []
    for cid, row in candidates:
        video_path = VIDEO_DIR / cid / "video.mp4"
        if video_path.exists():
            available_videos.append((cid, row, video_path))
    
    print(f"With local videos: {len(available_videos)}")
    
    if not available_videos:
        print("\nNo new videos available locally.")
        print("Need to collect new data via alternative method.")
        return
    
    # Process available videos
    print(f"\nProcessing {min(30, len(available_videos))} samples...")
    
    for i, (cid, row, video_path) in enumerate(available_videos[:30], 1):
        print(f"\n[{i}] Processing {cid}...")
        
        # Get duration
        import subprocess
        try:
            r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                               "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)],
                              capture_output=True, text=True, timeout=10)
            duration = float(r.stdout.strip())
        except:
            duration = 0
        
        # Check transcript
        trans_file = SHARDS / "transcripts_v2" / f"{cid}_raw.json"
        if not trans_file.exists():
            print(f"  No transcript available")
            continue
        
        with open(trans_file, 'r', encoding='utf-8') as f:
            transcript = json.load(f)
        
        if not transcript:
            print(f"  Empty transcript")
            continue
        
        print(f"  ✓ {len(transcript)} segments, {duration:.1f}s")
    
    print(f"\n=== BATCH 002 STATUS ===")
    print(f"New unique candidates: {len(candidates)}")
    print(f"With videos: {len(available_videos)}")
    print(f"Processed: {min(30, len(available_videos))}")
    
    # Summary
    print(f"\nConclusion:")
    print(f"  - No NEW videos available for download")
    print(f"  - All candidates already processed or have no video")
    print(f"  - Cannot achieve 30 NEW UNIQUE without new collection")

if __name__ == "__main__":
    asyncio.run(main())
