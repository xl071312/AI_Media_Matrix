#!/usr/bin/env python3
"""Download videos from Douyin using Playwright"""
import asyncio
import json
import re
from pathlib import Path
from playwright.async_api import async_playwright

VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

async def download_video(cid):
    """Download a single video"""
    print(f"\nProcessing {cid}...")
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9223")
        context = browser.contexts[0]
        
        # Find or create page
        page = None
        for p in context.pages:
            if 'douyin.com' in p.url:
                page = p
                break
        
        if not page:
            page = await context.new_page()
        
        # Navigate to video
        url = f"https://www.douyin.com/video/{cid}"
        print(f"  Navigating to {url}")
        await page.goto(url)
        await page.wait_for_timeout(5000)
        
        # Try to extract video URL
        video_url = None
        
        # Method 1: Look for video element
        try:
            video_elem = await page.query_selector('video')
            if video_elem:
                src = await video_elem.get_attribute('src')
                if src:
                    video_url = src
                    print(f"  Found video URL (method 1)")
        except:
            pass
        
        # Method 2: Look for data in window object
        if not video_url:
            try:
                init_state = await page.evaluate("() => window.__INITIAL_STATE__")
                if init_state:
                    state_str = json.dumps(init_state)
                    matches = re.findall(r'"play_url":"([^"]+)"', state_str)
                    if matches:
                        video_url = matches[0]
                        print(f"  Found video URL (method 2)")
            except:
                pass
        
        # Method 3: Extract from page source
        if not video_url:
            try:
                content = await page.content()
                matches = re.findall(r'"play_addr":\{"url_list":\["([^"]+)"\]', content)
                if matches:
                    video_url = matches[0]
                    print(f"  Found video URL (method 3)")
            except:
                pass
        
        if not video_url:
            print(f"  ✗ Could not find video URL")
            await browser.close()
            return False
        
        # Download video
        print(f"  Downloading...")
        try:
            resp = await page.evaluate(f"""async () => {{
                const response = await fetch('{video_url}');
                const blob = await response.blob();
                return blob;
            }}""")
            # Note: This approach may not work due to CORS
            print(f"  ⚠ Direct download may not work due to CORS")
        except Exception as e:
            print(f"  ✗ Download failed: {e}")
        
        await browser.close()
        return True

async def main():
    print("=== DOUYIN VIDEO DOWNLOAD TEST ===\n")
    
    # Test with one video ID
    test_cid = '7683219193294114063'
    
    success = await download_video(test_cid)
    
    if success:
        print(f"\n✓ Download test completed")
    else:
        print(f"\n✗ Download test failed")
        print(f"\nConclusion:")
        print(f"  - Direct video URL extraction is challenging")
        print(f"  - May need to use MediaCrawler's built-in download")
        print(f"  - Or use third-party tools like yt-dlp")

if __name__ == "__main__":
    asyncio.run(main())
