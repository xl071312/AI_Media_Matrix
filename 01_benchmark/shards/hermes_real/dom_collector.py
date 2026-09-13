#!/usr/bin/env python3
"""
Phase 3 DOM-Based Fallback Collector
Uses real Chrome browser via CDP to scrape Douyin data
when APIs are blocked by ArgusSecurityPlugin
"""
import json
import csv
import time
import urllib.request
from pathlib import Path
from datetime import datetime

BASE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
DOM_SEARCH_DIR = BASE / "douyin_dom_search"
CREATOR_BASELINE_DIR = BASE / "creator_baseline_dom"
DEEP_BATCH_FILE = BASE / "deep_analysis_batch_001.csv"

# Chrome CDP endpoint
CDP_URL = "http://127.0.0.1:9222"

def check_cdp():
    """Check if CDP is accessible"""
    try:
        req = urllib.request.Request(f"{CDP_URL}/json/version")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            return True, data.get("Browser", "")
    except Exception as e:
        return False, str(e)

def get_pages():
    """Get all open pages"""
    try:
        req = urllib.request.Request(f"{CDP_URL}/json")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except:
        return []

def execute_js(page_id, js_code, timeout=30):
    """Execute JavaScript on a page via CDP"""
    import websocket
    
    # Get page WebSocket URL
    pages = get_pages()
    ws_url = None
    for p in pages:
        if p.get('id') == page_id:
            ws_url = p.get('webSocketDebuggerUrl')
            break
    
    if not ws_url:
        return None, "Page not found"
    
    try:
        ws = websocket.create_connection(ws_url, timeout=timeout, 
                                          header=["Origin: http://127.0.0.1:9222"])
        
        # Enable required domains
        ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
        ws.recv()
        
        # Execute JS
        ws.send(json.dumps({
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {
                "expression": js_code,
                "returnByValue": True
            }
        }))
        
        result = ws.recv()
        ws.close()
        
        response = json.loads(result)
        if 'result' in response and 'result' in response['result']:
            return response['result']['result'].get('value'), None
        elif 'error' in response:
            return None, response['error'].get('message', str(response['error']))
        return None, "Unknown error"
    except Exception as e:
        return None, str(e)

def search_douyin_keyword_dom(keyword, max_results=10):
    """Search Douyin via DOM scraping"""
    print(f"\n=== SEARCHING: {keyword} ===")
    
    # Check CDP first
    cdp_ok, chrome_ver = check_cdp()
    if not cdp_ok:
        print(f"  CDP not available: {chrome_ver}")
        return []
    
    print(f"  CDP OK: {chrome_ver}")
    
    # Navigate to search page
    search_url = f"https://www.douyin.com/search/{keyword}?type=video"
    
    # Find or create a page for navigation
    pages = get_pages()
    main_page = None
    for p in pages:
        if 'douyin.com' in p.get('url', '') and p.get('type') == 'page':
            main_page = p
            break
    
    if not main_page:
        # Try to use the jingxuan page
        for p in pages:
            if p.get('type') == 'page' and 'douyin.com' in p.get('url', ''):
                main_page = p
                break
    
    if not main_page:
        print("  No suitable page found. Please navigate to douyin.com first.")
        return []
    
    print(f"  Using page: {main_page.get('title')}")
    
    # Navigate to search
    page_id = main_page.get('id')
    
    # Execute navigation via CDP
    nav_js = f"""
    (function() {{
        window.location.href = '{search_url}';
        return 'Navigated to search';
    }})()
    """
    
    result, error = execute_js(page_id, nav_js)
    if error:
        print(f"  Navigation error: {error}")
        return []
    
    print(f"  Navigating... waiting for results")
    time.sleep(5)  # Wait for page to load
    
    # Extract video data from DOM
    extract_js = """
    (function() {
        var videos = [];
        var cards = document.querySelectorAll('[class*="feed-item"], [class*="aweme"], [class*="video-card"], a[href*="/video/"]');
        
        cards.forEach(function(card) {
            var link = card.querySelector('a[href*="/video/"]') || card.closest('a[href*="/video/"]');
            if (!link) return;
            
            var url = link.href;
            var match = url.match(/\\/video\\/(\\d+)/);
            if (!match) return;
            
            var aweme_id = match[1];
            
            // Try to get title
            var titleEl = card.querySelector('[class*="title"], [class*="desc"], [class*="text"]');
            var title = titleEl ? titleEl.textContent.trim() : '';
            
            // Try to get stats
            var stats = card.querySelectorAll('[class*="like"], [class*="comment"], [class*="play"]');
            var likes = '', comments = '';
            stats.forEach(function(s) {
                var text = s.textContent.trim();
                if (text.includes('赞') || text.includes('likes')) likes = text;
                if (text.includes('评论')) comments = text;
            });
            
            videos.push({
                aweme_id: aweme_id,
                url: url,
                title: title.substring(0, 100),
                likes_raw: likes,
                comments_raw: comments,
                captured_at: new Date().toISOString()
            });
        });
        
        return JSON.stringify(videos.slice(0, {max_results}));
    })()
    """
    
    result, error = execute_js(page_id, extract_js)
    if error:
        print(f"  Extraction error: {error}")
        return []
    
    try:
        videos = json.loads(result) if result else []
        print(f"  Found {len(videos)} videos")
        return videos
    except:
        print(f"  Failed to parse result: {result}")
        return []

def get_creator_profile_dom(sec_user_id):
    """Get creator profile via DOM scraping"""
    print(f"\n=== GETTING CREATOR: {sec_user_id} ===")
    
    cdp_ok, _ = check_cdp()
    if not cdp_ok:
        return None
    
    # Navigate to creator page
    profile_url = f"https://www.douyin.com/user/{sec_user_id}"
    
    pages = get_pages()
    main_page = None
    for p in pages:
        if p.get('type') == 'page' and 'douyin.com' in p.get('url', ''):
            main_page = p
            break
    
    if not main_page:
        print("  No page available")
        return None
    
    page_id = main_page.get('id')
    
    # Navigate
    nav_js = f"""
    (function() {{
        window.location.href = '{profile_url}';
        return 'Navigated';
    }})()
    """
    
    result, error = execute_js(page_id, nav_js)
    if error:
        print(f"  Nav error: {error}")
        return None
    
    print(f"  Waiting for profile to load...")
    time.sleep(5)
    
    # Extract profile and videos
    extract_js = """
    (function() {
        var data = {
            profile: {},
            videos: []
        };
        
        // Try to get profile info
        var nameEl = document.querySelector('[class*="nickname"], [class*="name"], [class*="user-info"]');
        if (nameEl) data.profile.name = nameEl.textContent.trim();
        
        // Get follower count
        var stats = document.querySelectorAll('[class*="follower"], [class*="fans"]');
        stats.forEach(function(s) {
            if (!data.profile.followers && s.textContent.includes('粉丝')) {
                data.profile.followers = s.textContent.trim();
            }
        });
        
        // Get videos
        var cards = document.querySelectorAll('[class*="aweme"], [class*="video-item"], article');
        cards.forEach(function(card) {
            var link = card.querySelector('a[href*="/video/"]');
            if (!link) return;
            
            var url = link.href;
            var match = url.match(/\\/video\\/(\\d+)/);
            if (!match) return;
            
            var aweme_id = match[1];
            
            var titleEl = card.querySelector('[class*="title"], [class*="desc"]');
            var title = titleEl ? titleEl.textContent.trim() : '';
            
            var likeEl = card.querySelector('[class*="like-count"], [class*="digg"]');
            var likes = likeEl ? likeEl.textContent.trim() : '';
            
            data.videos.push({
                aweme_id: aweme_id,
                url: url,
                title: title.substring(0, 100),
                likes: likes,
                captured_at: new Date().toISOString()
            });
        });
        
        return JSON.stringify(data);
    })()
    """
    
    result, error = execute_js(page_id, extract_js)
    if error:
        print(f"  Extract error: {error}")
        return None
    
    try:
        data = json.loads(result) if result else {}
        print(f"  Found {len(data.get('videos', []))} videos")
        return data
    except:
        return None

def main():
    print("=== PHASE 3 DOM FALLBACK COLLECTOR ===\n")
    
    # Check CDP
    cdp_ok, chrome_ver = check_cdp()
    if not cdp_ok:
        print(f"CDP NOT AVAILABLE: {chrome_ver}")
        print("\nPlease start Chrome with:")
        print('chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\workspace\\AI_Media_Matrix\\browser_profiles\\douyin_benchmark_v2"')
        return
    
    print(f"CDP OK: {chrome_ver}")
    
    # Test 1: Search
    print("\n--- TEST 1: SEARCH ---")
    search_results = search_douyin_keyword_dom("赚钱逻辑", max_results=5)
    
    if search_results:
        # Save results
        output_file = DOM_SEARCH_DIR / "test_search.jsonl"
        with open(output_file, 'w', encoding='utf-8') as f:
            for v in search_results:
                f.write(json.dumps(v, ensure_ascii=False) + '\n')
        print(f"  Saved {len(search_results)} results to {output_file}")
    
    # Test 2: Creator Profile
    print("\n--- TEST 2: CREATOR PROFILE ---")
    # Use a known creator from our data
    creator_data = get_creator_profile_dom("MS4wLjABAAAAf9C6bAkw10bndnBb6OF4Q28AQf2bXdQ0kRut0dIJJOM")
    
    if creator_data:
        output_file = CREATOR_BASELINE_DIR / "test_creator.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(creator_data, f, indent=2, ensure_ascii=False)
        print(f"  Saved to {output_file}")
    
    print("\n=== TESTS COMPLETE ===")

if __name__ == "__main__":
    main()
