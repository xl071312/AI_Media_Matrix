#!/usr/bin/env python3
"""Direct Douyin DOM scraping as fallback"""
import asyncio
import json
import csv
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH2 = BASE / "analysis_batches" / "batch_002"
BATCH2.mkdir(parents=True, exist_ok=True)
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

async def scrape_via_dom():
    """Scrape Douyin directly via Playwright"""
    print("=== DOM SCRAPING FALLBACK ===\n")
    
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        # Connect to existing CDP
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9223")
        context = browser.contexts[0]
        
        # Find or create Douyin tab
        douyin_page = None
        for page in context.pages:
            if 'douyin.com' in page.url:
                douyin_page = page
                break
        
        if not douyin_page:
            douyin_page = await context.new_page()
            await douyin_page.goto("https://www.douyin.com")
            await asyncio.sleep(3)
        
        print(f"Current URL: {douyin_page.url}")
        
        # Try to get video data from page
        try:
            # Look for video data in page source
            content = await douyin_page.content()
            
            # Try to find video IDs in JSON data
            import re
            # Look for aweme_id patterns
            aweme_ids = re.findall(r'"aweme_id":"(\d+)"', content)
            unique_ids = list(set(aweme_ids))
            
            print(f"Found {len(unique_ids)} unique video IDs from page")
            
            # Filter to new unique candidates
            new_candidates = [cid for cid in unique_ids if cid not in EXISTING_CIDS]
            print(f"New unique candidates: {len(new_candidates)}")
            
            # Show first 10
            for cid in new_candidates[:10]:
                print(f"  {cid}")
            
            # Check if we have videos locally
            local_videos = [(cid, VIDEO_DIR / cid / "video.mp4") 
                           for cid in new_candidates[:20] 
                           if (VIDEO_DIR / cid / "video.mp4").exists()]
            
            print(f"\nWith local videos: {len(local_videos)}")
            
            if local_videos:
                # Process first 3 as smoke test
                for i, (cid, video_path) in enumerate(local_videos[:3], 1):
                    print(f"\n[{i}/3] Processing {cid}...")
                    
                    # Get metadata from selection
                    row = selection.get(cid, {})
                    
                    # Run ASR
                    duration = None
                    try:
                        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                           "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)],
                                          capture_output=True, text=True, timeout=10)
                        duration = float(r.stdout.strip())
                    except:
                        pass
                    
                    # Check transcript
                    trans_file = TRANSCRIPT_DIR / f"{cid}_raw.json"
                    if trans_file.exists():
                        with open(trans_file, 'r', encoding='utf-8') as f:
                            transcript = json.load(f)
                    else:
                        print(f"  No transcript available")
                        continue
                    
                    print(f"  ✓ {len(transcript)} segments, {duration:.1f}s")
                    
                print(f"\n✓ Smoke test completed")
            else:
                print("\n⚠ No local videos for new candidates")
                print("Need to download videos first")
            
        except Exception as e:
            print(f"Error scraping: {e}")
            import traceback
            traceback.print_exc()
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_via_dom())
