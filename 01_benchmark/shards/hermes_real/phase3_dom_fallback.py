#!/usr/bin/env python3
"""
Phase 3 DOM Fallback Executor
- Creator Baseline via DOM scraping
- Video page access check
- Transcript extraction
"""
import json
import csv
import time
import urllib.request
from pathlib import Path
from datetime import datetime
import subprocess

BASE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
MC_DIR = Path(r"C:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler")
CREATOR_BASELINE_DIR = BASE / "creator_baseline_dom"
MEDIA_DIR = BASE / "media_raw"
TRANSCRIPT_DIR = BASE / "transcripts"
ANALYSIS_DIR = BASE / "analysis"

# Targets
TARGET_CREATOR_BASELINE = 5
TARGET_TRANSCRIPTS = 3
TARGET_DEEP_ANALYSIS = 3

def load_deep_batch():
    """Load deep analysis batch"""
    records = []
    with open(BASE / "deep_analysis_batch_001.csv", 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.lstrip('\ufeff'): v for k, v in row.items()}
            records.append(clean_row)
    return records

def load_new_search_results():
    """Load new search results from today"""
    results = []
    new_file = MC_DIR / "data" / "douyin" / "jsonl" / "search_contents_2026-09-07.jsonl"
    if new_file.exists():
        with open(new_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        results.append(json.loads(line))
                    except:
                        pass
    return results

def get_cdp_pages():
    """Get all open pages via CDP"""
    try:
        req = urllib.request.Request("http://127.0.0.1:9222/json")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except:
        return []

def execute_js_on_page(page_id, js_code):
    """Execute JavaScript on a specific page"""
    try:
        import websocket
        pages = get_cdp_pages()
        ws_url = None
        for p in pages:
            if p.get('id') == page_id:
                ws_url = p.get('webSocketDebuggerUrl')
                break
        
        if not ws_url:
            return None, "Page not found"
        
        ws = websocket.create_connection(ws_url, timeout=30,
                                          header=["Origin: http://127.0.0.1:9222"])
        
        ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
        ws.recv()
        
        ws.send(json.dumps({
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {"expression": js_code, "returnByValue": True}
        }))
        
        result = ws.recv()
        ws.close()
        
        data = json.loads(result)
        if 'result' in data and 'result' in data['result']:
            return data['result']['result'].get('value'), None
        return None, str(data.get('error', 'unknown'))
    except Exception as e:
        return None, str(e)

def navigate_and_scrape_creator(page_id, sec_user_id):
    """Navigate to creator page and scrape data"""
    print(f"  Scraping creator: {sec_user_id}")
    
    # Navigate to creator page
    nav_js = f"""
    (function() {{
        window.location.href = 'https://www.douyin.com/user/{sec_user_id}';
        return 'navigated';
    }})()
    """
    
    result, error = execute_js_on_page(page_id, nav_js)
    if error:
        return None, error
    
    time.sleep(5)  # Wait for page load
    
    # Extract video data
    extract_js = """
    (function() {
        var data = {videos: [], profile: {}};
        
        // Try to get profile info
        var nameEl = document.querySelector('[class*="nickname"], [class*="user-name"]');
        if (nameEl) data.profile.name = nameEl.textContent.trim();
        
        // Get videos
        var cards = document.querySelectorAll('[class*="aweme-item"], [class*="video-item"], article');
        cards.forEach(function(card) {
            var link = card.querySelector('a[href*="/video/"]');
            if (!link) return;
            
            var url = link.href;
            var match = url.match(/\\/video\\/(\\d+)/);
            if (!match) return;
            
            var titleEl = card.querySelector('[class*="title"], [class*="desc"]');
            var title = titleEl ? titleEl.textContent.trim() : '';
            
            var likeEl = card.querySelector('[class*="like-count"], [class*="digg-count"]');
            var likes = likeEl ? likeEl.textContent.trim() : '';
            
            data.videos.push({
                aweme_id: match[1],
                url: url,
                title: title.substring(0, 100),
                likes: likes
            });
        });
        
        return JSON.stringify(data);
    })()
    """
    
    result, error = execute_js_on_page(page_id, extract_js)
    if error:
        return None, error
    
    try:
        return json.loads(result), None
    except:
        return None, "Parse error"

def navigate_and_check_video(page_id, aweme_id):
    """Navigate to video page and check accessibility"""
    print(f"  Checking video: {aweme_id}")
    
    nav_js = f"""
    (function() {{
        window.location.href = 'https://www.douyin.com/video/{aweme_id}';
        return 'navigated';
    }})()
    """
    
    result, error = execute_js_on_page(page_id, nav_js)
    if error:
        return None, error
    
    time.sleep(3)
    
    # Check if video is playing
    check_js = """
    (function() {
        var video = document.querySelector('video');
        var caption = document.querySelector('[class*="caption"], [class*="subtitle"]');
        return JSON.stringify({
            video_exists: !!video,
            video_playable: video ? !video.paused : false,
            caption_available: !!caption,
            caption_text: caption ? caption.textContent.substring(0, 200) : ''
        });
    })()
    """
    
    result, error = execute_js_on_page(page_id, check_js)
    return result, error

def run_asr_on_video(video_path, content_id):
    """Run ASR on downloaded video"""
    print(f"  Running ASR: {content_id}")
    
    # Check if whisper or faster-whisper is available
    try:
        # Try faster-whisper first
        cmd = [
            "python", "-m", "faster_whisper.transcribe",
            str(video_path),
            "--model_size", "base",
            "--output_format", "json",
            "--output_dir", str(TRANSCRIPT_DIR),
            "--word_timestamps", "true"
        ]
        
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if proc.returncode == 0:
            # Find output file
            output_files = list(TRANSCRIPT_DIR.glob(f"{content_id}_*.json"))
            if output_files:
                return str(output_files[0]), "PASS"
        
        # Try normal whisper
        cmd = [
            "python", "-m", "whisper",
            str(video_path),
            "--model", "base",
            "--output_format", "json",
            "--output_dir", str(TRANSCRIPT_DIR),
            "--word_timespans", "true"
        ]
        
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if proc.returncode == 0:
            output_files = list(TRANSCRIPT_DIR.glob(f"{content_id}_*.json"))
            if output_files:
                return str(output_files[0]), "PASS"
        
        return None, "ASR_FAILED"
        
    except FileNotFoundError:
        return None, "WHISPER_NOT_INSTALLED"
    except Exception as e:
        return None, f"ERROR: {str(e)}"

def main():
    print("=" * 60)
    print("PHASE 3 DOM FALLBACK EXECUTOR")
    print("=" * 60)
    
    # Load data
    deep_batch = load_deep_batch()
    new_search = load_new_search_results()
    
    print(f"\nDeep Batch: {len(deep_batch)} records")
    print(f"New Search Results: {len(new_search)} records")
    
    # Get CDP pages
    pages = get_cdp_pages()
    main_page = None
    for p in pages:
        if p.get('type') == 'page' and 'douyin.com' in p.get('url', ''):
            main_page = p
            break
    
    if not main_page:
        print("\nNo Douyin page found. Please navigate to douyin.com in Benchmark Chrome.")
        return
    
    print(f"\nUsing page: {main_page.get('title')}")
    page_id = main_page.get('id')
    
    # Step 1: Collect Creator Baselines (target: 5)
    print("\n=== STEP 1: CREATOR BASELINE ===")
    creator_done = 0
    unique_creators = set()
    
    for record in deep_batch[:10]:  # Test first 10
        creator = record.get('nickname', '')
        if creator not in unique_creators:
            unique_creators.add(creator)
            # Try to get sec_user_id from URL
            url = record.get('url', '')
            import re
            match = re.search(r'/user/([^/]+)', url)
            if match:
                sec_user_id = match.group(1)
                result, error = navigate_and_scrape_creator(page_id, sec_user_id)
                
                if result and result.get('videos'):
                    print(f"  ✓ {creator}: {len(result['videos'])} videos found")
                    creator_done += 1
                    
                    # Save
                    output_file = CREATOR_BASELINE_DIR / f"{sec_user_id}.json"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
                    
                    if creator_done >= TARGET_CREATOR_BASELINE:
                        break
                else:
                    print(f"  ✗ {creator}: {error}")
    
    print(f"\nCreator Baseline: {creator_done}/{TARGET_CREATOR_BASELINE}")
    
    # Step 2: Check Video Pages (target: 5)
    print("\n=== STEP 2: VIDEO PAGE ACCESS ===")
    video_done = 0
    
    for record in deep_batch[:10]:
        aweme_id = record.get('aweme_id', '')
        result, error = navigate_and_check_video(page_id, aweme_id)
        
        if result and 'video_exists' in result:
            data = json.loads(result)
            if data.get('video_exists'):
                print(f"  ✓ {aweme_id}: video accessible")
                video_done += 1
            else:
                print(f"  ✗ {aweme_id}: video not found")
        else:
            print(f"  ✗ {aweme_id}: {error}")
        
        if video_done >= 5:
            break
    
    print(f"\nVideo Pages Accessible: {video_done}/5")
    
    # Step 3: Run ASR on downloaded videos (target: 3)
    print("\n=== STEP 3: ASR TRANSCRIPT ===")
    transcript_done = 0
    
    # Find downloaded videos
    video_dirs = list(MC_DIR.glob("data/douyin/videos/*/video.mp4"))
    
    for video_path in video_dirs[:10]:
        content_id = video_path.parent.name
        
        # Check if already processed
        if (TRANSCRIPT_DIR / f"{content_id}_raw.json").exists():
            print(f"  ✓ {content_id}: already processed")
            transcript_done += 1
            continue
        
        print(f"  Processing: {content_id}")
        transcript_file, status = run_asr_on_video(video_path, content_id)
        
        if status == "PASS":
            print(f"  ✓ {content_id}: ASR complete")
            transcript_done += 1
        else:
            print(f"  ✗ {content_id}: {status}")
        
        if transcript_done >= TARGET_TRANSCRIPTS:
            break
    
    print(f"\nTimed Transcripts: {transcript_done}/{TARGET_TRANSCRIPTS}")
    
    # Save checkpoint
    checkpoint = {
        "phase": "PHASE_3_IN_PROGRESS",
        "timestamp": datetime.now().isoformat(),
        "creator_baseline_done": creator_done,
        "video_pages_accessible": video_done,
        "timed_transcript_done": transcript_done,
        "deep_analysis_done": 0,
        "placeholder_upgraded": transcript_done,
        "argus_blocked": True,
        "blockers": ["CREATOR_API: ArgusSecurityPlugin", "DETAIL_API: ArgusSecurityPlugin"],
        "data_counts": {
            "raw_pool_old": 414,
            "raw_pool_new": len(new_search),
            "total_raw": 414 + len(new_search),
            "videos_downloaded": len(list(MC_DIR.glob("data/douyin/videos/*/"))),
            "simulated": 0
        }
    }
    
    with open(BASE / "phase3_dom_checkpoint.json", 'w') as f:
        json.dump(checkpoint, f, indent=2, ensure_ascii=False)
    
    print(f"\nCheckpoint saved to phase3_dom_checkpoint.json")
    print(f"\n=== SUMMARY ===")
    print(f"Creator Baseline: {creator_done}/{TARGET_CREATOR_BASELINE}")
    print(f"Video Pages: {video_done}/5")
    print(f"Timed Transcripts: {transcript_done}/{TARGET_TRANSCRIPTS}")
    print(f"Placeholder Upgraded: {transcript_done}")

if __name__ == "__main__":
    main()
