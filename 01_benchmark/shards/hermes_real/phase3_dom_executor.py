#!/usr/bin/env python3
"""Phase 3 DOM Fallback Executor - Creator Baseline + Video Access"""
import json
import asyncio
import urllib.request
from pathlib import Path
from datetime import datetime
import re

BASE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
VIDEO_DIR = Path(r"C:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
CREATOR_DIR = BASE / "creator_baseline_dom"
TRANSCRIPT_DIR = BASE / "transcripts"
ANALYSIS_DIR = BASE / "analysis"

async def execute_js(page_id, js_code, timeout=30):
    """Execute JavaScript on a page via CDP"""
    import websockets
    
    try:
        # Get pages
        req = urllib.request.Request("http://127.0.0.1:9223/json")
        with urllib.request.urlopen(req, timeout=10) as resp:
            pages = json.loads(resp.read().decode())
        
        # Find target page
        ws_url = None
        for p in pages:
            if p.get('id') == page_id:
                ws_url = p.get('webSocketDebuggerUrl')
                break
        
        if not ws_url:
            return None, "Page not found"
        
        async with websockets.connect(ws_url, origin="http://127.0.0.1:9223", max_size=10*1024*1024) as ws:
            # Enable Runtime
            await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
            await asyncio.wait_for(ws.recv(), timeout=5)
            
            # Execute JS
            await ws.send(json.dumps({
                "id": 2,
                "method": "Runtime.evaluate",
                "params": {"expression": js_code, "returnByValue": True}
            }))
            
            resp = await asyncio.wait_for(ws.recv(), timeout=timeout)
            data = json.loads(resp)
            
            if 'result' in data and 'result' in data['result']:
                return data['result']['result'].get('value'), None
            elif 'result' in data and 'exceptionDetails' in data['result']:
                return None, data['result']['exceptionDetails'].get('text', 'Unknown error')
            return None, str(data.get('error', 'Unknown'))
            
    except Exception as e:
        return None, str(e)

def get_main_page():
    """Get the main Douyin page"""
    try:
        req = urllib.request.Request("http://127.0.0.1:9223/json")
        with urllib.request.urlopen(req, timeout=10) as resp:
            pages = json.loads(resp.read().decode())
        
        for p in pages:
            if p.get('type') == 'page' and 'douyin.com' in p.get('url', ''):
                return p
        return None
    except:
        return None

async def scrape_creator_page(page_id, sec_user_id):
    """Scrape creator profile page"""
    print(f"  Scraping creator: {sec_user_id}")
    
    # Navigate to creator page
    nav_js = f"""
    (function() {{
        window.location.href = 'https://www.douyin.com/user/{sec_user_id}';
        return 'navigated';
    }})()
    """
    
    result, error = await execute_js(page_id, nav_js)
    if error:
        return None, error
    
    # Wait for page load
    await asyncio.sleep(5)
    
    # Extract video data
    extract_js = """
    (function() {
        var data = {videos: []};
        
        // Find video cards
        var cards = document.querySelectorAll('[class*="aweme-item"], [class*="video-item"], article, .feed-item');
        
        cards.forEach(function(card) {
            var link = card.querySelector('a[href*="/video/"]');
            if (!link) return;
            
            var url = link.href;
            var match = url.match(/\\/video\\/(\\d+)/);
            if (!match) return;
            
            // Get title
            var titleEl = card.querySelector('[class*="title"], [class*="desc"], [class*="text"]');
            var title = titleEl ? titleEl.textContent.trim() : '';
            
            // Get likes
            var likeEl = card.querySelector('[class*="like"], [class*="digg"]');
            var likes = '';
            if (likeEl) {
                likes = likeEl.textContent.trim();
            }
            
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
    
    result, error = await execute_js(page_id, extract_js)
    if error:
        return None, error
    
    try:
        return json.loads(result), None
    except:
        return None, "Parse error"

async def check_video_page(page_id, aweme_id):
    """Check if video page is accessible"""
    print(f"  Checking video: {aweme_id}")
    
    # Navigate to video page
    nav_js = f"""
    (function() {{
        window.location.href = 'https://www.douyin.com/video/{aweme_id}';
        return 'navigated';
    }})()
    """
    
    result, error = await execute_js(page_id, nav_js)
    if error:
        return None, error
    
    await asyncio.sleep(3)
    
    # Check video playback and captions
    check_js = """
    (function() {
        var video = document.querySelector('video');
        var caption = document.querySelector('[class*="caption"], [class*="subtitle"], [class*="desc"]');
        
        return JSON.stringify({
            video_exists: !!video,
            video_duration: video ? video.duration : 0,
            caption_available: !!caption,
            caption_text: caption ? caption.textContent.substring(0, 300) : ''
        });
    })()
    """
    
    result, error = await execute_js(page_id, check_js)
    return result, error

def main():
    print("=" * 60)
    print("PHASE 3 DOM FALLBACK EXECUTOR")
    print("=" * 60)
    
    # Get main page
    main_page = get_main_page()
    if not main_page:
        print("No Douyin page found. Please navigate to douyin.com in Benchmark Chrome.")
        return
    
    page_id = main_page.get('id')
    print(f"\nUsing page: {main_page.get('title')}")
    
    # Load deep batch to get targets
    deep_batch_file = BASE / "deep_analysis_batch_001.csv"
    if not deep_batch_file.exists():
        print("Deep batch file not found")
        return
    
    import csv
    with open(deep_batch_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        deep_batch = list(reader)
    
    print(f"Deep batch: {len(deep_batch)} records\n")
    
    # Test 1: Creator Baseline (target: 5)
    print("=== TEST 1: CREATOR BASELINE ===\n")
    
    creators_tested = 0
    for record in deep_batch[:10]:
        if creators_tested >= 5:
            break
        
        nickname = record.get('nickname', '')
        url = record.get('url', '')
        
        # Extract sec_user_id
        match = re.search(r'/user/([^/?]+)', url)
        if not match:
            continue
        
        sec_user_id = match.group(1)
        
        async def test_creator():
            return await scrape_creator_page(page_id, sec_user_id)
        
        result, error = asyncio.run(test_creator())
        
        if result and result.get('videos'):
            videos = result['videos']
            print(f"  ✓ {nickname}: {len(videos)} videos found")
            
            # Save
            output_file = CREATOR_DIR / f"{sec_user_id}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            creators_tested += 1
        else:
            print(f"  ✗ {nickname}: {error}")
    
    print(f"\nCreator Baseline: {creators_tested}/5\n")
    
    # Test 2: Video Page Access (target: 5)
    print("=== TEST 2: VIDEO PAGE ACCESS ===\n")
    
    videos_tested = 0
    for record in deep_batch[:10]:
        if videos_tested >= 5:
            break
        
        aweme_id = record.get('aweme_id', '')
        
        async def test_video():
            return await check_video_page(page_id, aweme_id)
        
        result, error = asyncio.run(test_video())
        
        if result:
            data = json.loads(result)
            if data.get('video_exists'):
                print(f"  ✓ {aweme_id}: video accessible, duration={data.get('video_duration', 0)}s")
                videos_tested += 1
            else:
                print(f"  ✗ {aweme_id}: video element not found")
        else:
            print(f"  ✗ {aweme_id}: {error}")
    
    print(f"\nVideo Pages Accessible: {videos_tested}/5\n")
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Creator Baseline: {creators_tested}/5")
    print(f"Video Pages: {videos_tested}/5")
    print(f"Videos Downloaded: {len(list(VIDEO_DIR.glob('*/')))}")
    
    # Save checkpoint
    checkpoint = {
        "phase": "PHASE_3_IN_PROGRESS",
        "timestamp": datetime.now().isoformat(),
        "creator_baseline_done": creators_tested,
        "video_pages_accessible": videos_tested,
        "videos_downloaded": len(list(VIDEO_DIR.glob('*/'))),
        "argus_blocked": True,
        "fallback_active": True
    }
    
    with open(BASE / "phase3_dom_checkpoint.json", 'w') as f:
        json.dump(checkpoint, f, indent=2)
    
    print(f"\nCheckpoint saved")

if __name__ == "__main__":
    main()
