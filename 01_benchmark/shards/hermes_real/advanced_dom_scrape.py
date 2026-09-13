#!/usr/bin/env python3
"""Advanced Douyin DOM scraping with wait for dynamic content"""
import asyncio
import json
import re
from playwright.async_api import async_playwright

async def scrape_douyin_videos():
    """Scrape Douyin videos from jingxuan page"""
    print("=== ADVANCED DOUYIN SCRAPING ===\n")
    
    async with async_playwright() as p:
        # Connect to existing CDP
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9223")
        context = browser.contexts[0]
        
        # Find Douyin tab
        douyin_page = None
        for page in context.pages:
            if 'douyin.com' in page.url:
                douyin_page = page
                break
        
        if not douyin_page:
            douyin_page = await context.new_page()
            await douyin_page.goto("https://www.douyin.com/jingxuan")
        
        print(f"Current URL: {douyin_page.url}")
        
        # Wait for content to load
        print("Waiting for page content...")
        await douyin_page.wait_for_timeout(5000)
        
        # Try multiple extraction methods
        video_ids = set()
        
        # Method 1: Extract from window.__INITIAL_STATE__
        try:
            initial_state = await douyin_page.evaluate("() => window.__INITIAL_STATE__")
            if initial_state:
                state_str = json.dumps(initial_state)
                ids = re.findall(r'"aweme_id":"(\d+)"', state_str)
                video_ids.update(ids)
                print(f"Method 1 (INITIAL_STATE): {len(ids)} IDs")
        except Exception as e:
            print(f"Method 1 failed: {e}")
        
        # Method 2: Extract from window.__INIT_DATA__
        try:
            init_data = await douyin_page.evaluate("() => window.__INIT_DATA__")
            if init_data:
                data_str = json.dumps(init_data)
                ids = re.findall(r'"aweme_id":"(\d+)"', data_str)
                video_ids.update(ids)
                print(f"Method 2 (INIT_DATA): {len(ids)} IDs")
        except Exception as e:
            print(f"Method 2 failed: {e}")
        
        # Method 3: Extract from all JSON in page
        try:
            content = await douyin_page.content()
            ids = re.findall(r'"aweme_id":"(\d+)"', content)
            video_ids.update(ids)
            print(f"Method 3 (page content): {len(ids)} IDs")
        except Exception as e:
            print(f"Method 3 failed: {e}")
        
        # Method 4: Look for video elements
        try:
            videos = await douyin_page.query_selector_all('[data-e2e="feed-item"], .feed-item, [class*="video"]')
            print(f"Method 4 (DOM elements): {len(videos)} elements")
            
            for i, video in enumerate(videos[:10]):
                try:
                    href = await video.get_attribute('href')
                    if href:
                        # Extract ID from URL
                        match = re.search(r'/video/(\d+)', href)
                        if match:
                            video_ids.add(match.group(1))
                except:
                    pass
        except Exception as e:
            print(f"Method 4 failed: {e}")
        
        # Remove existing CIDs
        EXISTING_CIDS = {'7546212425998454074', '7647797848847439706', '7302348364815928612',
                        '7378948118584282394', '7525683513706810682', '7543846940678589723',
                        '7591984049339256177', '7599692006406786358', '7600594940562173553',
                        '7600957703851148773', '7601271873183404410', '7605619626101298353',
                        '7612226417060793640', '7615062854701905509', '7615498586105512443',
                        '7616716621441157861', '7617784493907141530', '7623019373322049125',
                        '7637328690322049125', '7660665426599452089', '7672991243072616697',
                        '7680569771779521482', '7680857899472843515', '7682791681556548883'}
        
        new_ids = [cid for cid in video_ids if cid not in EXISTING_CIDS]
        
        print(f"\n=== RESULTS ===")
        print(f"Total unique IDs found: {len(video_ids)}")
        print(f"New unique candidates: {len(new_ids)}")
        
        if new_ids:
            print(f"\nFirst 10 new IDs:")
            for cid in new_ids[:10]:
                print(f"  {cid}")
        
        await browser.close()
        return new_ids[:20]  # Return up to 20 new IDs

if __name__ == "__main__":
    new_ids = asyncio.run(scrape_douyin_videos())
    print(f"\nFinal: {len(new_ids)} new unique video IDs")
