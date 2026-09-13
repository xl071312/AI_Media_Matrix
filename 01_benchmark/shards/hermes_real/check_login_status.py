#!/usr/bin/env python3
"""Check browser login status and debug MediaCrawler"""
import asyncio
import json
import urllib.request
from playwright.async_api import async_playwright

async def check_login_status():
    """Check if browser is logged into Douyin"""
    print("=== CHECKING LOGIN STATUS ===\n")
    
    # Connect to existing CDP
    url = "http://127.0.0.1:9223/json"
    try:
        resp = urllib.request.urlopen(url, timeout=5)
        tabs = json.loads(resp.read().decode())
        print(f"Available tabs: {len(tabs)}")
        for tab in tabs[:3]:
            print(f"  - {tab.get('title', 'N/A')}: {tab.get('url', 'N/A')[:60]}...")
    except Exception as e:
        print(f"Cannot connect to CDP: {e}")
        return
    
    # Find Douyin tab
    douyin_tab = None
    for tab in tabs:
        if 'douyin.com' in tab.get('url', ''):
            douyin_tab = tab
            break
    
    if not douyin_tab:
        print("\nNo Douyin tab found. Opening Douyin...")
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9223")
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            page = await context.new_page()
            await page.goto("https://www.douyin.com")
            await asyncio.sleep(3)
            
            # Check if logged in
            current_url = page.url
            title = await page.title()
            print(f"Current URL: {current_url}")
            print(f"Page title: {title}")
            
            # Check for login prompt
            login_found = await page.locator('.login-modal, [class*="login"], .login-box').count()
            print(f"Login modal found: {login_found > 0}")
            
            # Check cookies for session
            cookies = await context.cookies()
            douyin_cookies = [c for c in cookies if 'douyin' in c.get('domain', '')]
            print(f"Douyin cookies: {len(douyin_cookies)}")
            
            if douyin_cookies:
                session_ids = [c.name for c in douyin_cookies if 'session' in c.name.lower()]
                print(f"Session cookies: {session_ids}")
            
            await browser.close()
    else:
        print(f"\nFound Douyin tab: {douyin_tab.get('url', 'N/A')[:80]}...")
        
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9223")
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            page = context.pages[0] if context.pages else await context.new_page()
            
            # Check current URL
            current_url = page.url
            print(f"Current URL: {current_url}")
            
            # Check for login indicators
            try:
                # Try to find user info (indicates logged in)
                user_info = await page.locator('.user-info, [class*="user-name"], .avatar').count()
                print(f"User info elements: {user_info}")
                
                # Try to find search results
                search_results = await page.locator('.video-item, [class*="video"], .result-item').count()
                print(f"Video result elements: {search_results}")
                
                # Check cookies
                cookies = await context.cookies()
                douyin_cookies = [c for c in cookies if 'douyin' in c.get('domain', '')]
                print(f"Douyin cookies: {len(douyin_cookies)}")
                
                # Check for specific session cookies
                session_cookies = ['sessionid', 'session_id', 'ttwid', 'csrftoken']
                found_sessions = [c.name for c in douyin_cookies if any(s in c.name.lower() for s in session_cookies)]
                print(f"Session cookies found: {found_sessions}")
                
                if len(found_sessions) >= 2:
                    print("\n✓ Login status: LOGGED IN")
                else:
                    print("\n⚠ Login status: MAYBE NOT LOGGED IN")
                    print("  Please ensure you're logged into Douyin in the browser")
                    
            except Exception as e:
                print(f"Error checking status: {e}")
            
            await browser.close()

if __name__ == "__main__":
    asyncio.run(check_login_status())
