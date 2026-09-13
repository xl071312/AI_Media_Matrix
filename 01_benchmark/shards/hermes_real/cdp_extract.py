#!/usr/bin/env python3
"""
Use CDP to extract video data directly from the current browser page
"""
import json
import urllib.request
import urllib.parse
import time

CDP_PORT = 9222

def get_pages():
    """Get all open pages"""
    req = urllib.request.Request(f"http://127.0.0.1:{CDP_PORT}/json")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def execute_cdp(page_id, method, params=None):
    """Execute CDP command on a page"""
    import websocket
    # Get websocket URL
    pages = get_pages()
    page_url = None
    for p in pages:
        if p.get('id') == page_id:
            page_url = p.get('webSocketDebuggerUrl')
            break
    
    if not page_url:
        return None
    
    ws = websocket.create_connection(page_url, timeout=30)
    
    # Enable Page domain
    ws.send(json.dumps({
        "id": 1,
        "method": "Page.enable"
    }))
    ws.recv()
    
    # Execute script
    ws.send(json.dumps({
        "id": 2,
        "method": "Runtime.evaluate",
        "params": params or {"expression": "document.title"}
    }))
    
    result = ws.recv()
    ws.close()
    
    return json.loads(result)

def extract_video_data_from_page():
    """Extract video data from current Douyin page"""
    pages = get_pages()
    
    for page in pages:
        if 'douyin.com' in page.get('url', ''):
            print(f"Found Douyin page: {page.get('title')}")
            print(f"URL: {page.get('url')}")
            
            # Try to extract video cards
            js_code = """
            (function() {
                var videos = [];
                // Try to find video elements
                var cards = document.querySelectorAll('.cursor-pointer, [class*="card"], [class*="video"]');
                cards.forEach(function(card) {
                    var title = card.querySelector('.text') || card.querySelector('[class*="title"]');
                    var stats = card.querySelectorAll('[class*="count"], [class*="like"], [class*="comment"]');
                    if (title) {
                        videos.push({
                            title: title.textContent,
                            stats: Array.from(stats).map(s => s.textContent)
                        });
                    }
                });
                return JSON.stringify(videos.slice(0, 20));
            })()
            """
            
            try:
                result = execute_cdp(page.get('id'), "Runtime.evaluate", {
                    "expression": js_code
                })
                
                if result and 'result' in result:
                    data = result['result'].get('result', {})
                    if 'value' in data:
                        print(f"Extracted: {data['value'][:500]}...")
                        return data['value']
            except Exception as e:
                print(f"Error: {e}")
    
    return None

if __name__ == "__main__":
    print("=== CDP PAGE EXTRACTION ===\n")
    
    pages = get_pages()
    print(f"Open pages: {len(pages)}\n")
    
    for p in pages:
        print(f"- {p.get('title', 'N/A')}: {p.get('url', 'N/A')}")
    
    print("\nAttempting to extract video data...")
    data = extract_video_data_from_page()
    
    if data:
        print(f"\nSuccess! Got {len(data)} items")
    else:
        print("\nNo data extracted. Trying alternative methods...")
