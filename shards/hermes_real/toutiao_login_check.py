#!/usr/bin/env python3
"""Wait for Toutiao login and verify session"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# Check if Chrome is running on port 9224
def check_chrome_running():
    try:
        import urllib.request
        req = urllib.request.Request('http://127.0.0.1:9224/json')
        with urllib.request.urlopen(req, timeout=5) as resp:
            return True
    except:
        return False

print("=== TOUTIAO LOGIN CHECK ===")
print()

# Wait for Chrome to start
print("Waiting for Chrome to start on port 9224...")
for i in range(10):
    if check_chrome_running():
        print(f"Chrome detected on port 9224")
        break
    print(f"  Attempt {i+1}/10 - waiting...")
    time.sleep(2)
else:
    print("Chrome not detected. Please ensure Chrome is running.")
    exit(1)

# Connect and check page
print()
print("Connecting to Chrome...")
p = sync_playwright().start()
browser = p.chromium.connect_over_cdp('http://127.0.0.1:9224')

try:
    context = browser.contexts[0]
    pages = context.pages
    
    if pages:
        page = pages[0]
        current_url = page.url
        print(f"Current URL: {current_url}")
        
        # Check if logged in (look for user elements)
        is_logged_in = False
        try:
            # Look for user avatar or name
            user_elements = page.query_selector_all('.user-avatar, .username, [class*="user"], [class*="avatar"]')
            if user_elements:
                is_logged_in = True
                print(f"Found user elements: {len(user_elements)}")
        except:
            pass
        
        # Check for login prompts
        has_login_prompt = False
        try:
            login_text = page.content()
            if any(x in login_text for x in ['登录', '扫码', '二维码', '手机号']):
                has_login_prompt = True
        except:
            pass
        
        print()
        print(f"Login Status: {'LOGGED_IN' if is_logged_in and not has_login_prompt else 'NOT_LOGGED_IN'}")
        print(f"Has Login Prompt: {has_login_prompt}")
        
        if is_logged_in and not has_login_prompt:
            print()
            print("✓ Authenticated session confirmed!")
            print("Ready to process seeds...")
        else:
            print()
            print("Please complete login in the Chrome window.")
            print("Then run this script again.")
    
    else:
        print("No pages found. Please ensure Toutiao is open in Chrome.")
        
finally:
    try: p.stop()
    except: pass
