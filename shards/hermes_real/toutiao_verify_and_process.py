#!/usr/bin/env python3
"""Toutiao Login Verification and Seed Processing"""
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH4_DIR = BASE / "analysis_batches" / "batch_004_toutiao"
SEED_DIR = BATCH4_DIR / "SEED_WAVE_001"

SEED_DIR.mkdir(parents=True, exist_ok=True)

# Seed IDs
SEED_IDS = [
    '7591436947063702022',
    '7652293131710300706',
    '7652914429046178313',
    '7645692141699662362',
    '7674332815097414180'
]

print("=== TOUTIAO SESSION VERIFICATION ===")
print()

# Connect to Chrome
try:
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9224')
    context = browser.contexts[0]
    
    # Check current page
    if context.pages:
        page = context.pages[0]
        current_url = page.url
        print(f"Current URL: {current_url}")
        
        # Check login status
        is_logged_in = False
        try:
            # Look for user elements
            user_el = page.query_selector('[class*="user"], [class*="avatar"], .username')
            if user_el:
                is_logged_in = True
                print(f"User element found: {user_el.text_content()[:50]}")
        except:
            pass
        
        # Check for login prompts
        has_login = False
        try:
            content = page.content()
            if any(x in content for x in ['登录', '扫码', '二维码']):
                has_login = True
        except:
            pass
        
        print(f"Login Status: {'LOGGED_IN' if is_logged_in and not has_login else 'NOT_LOGGED_IN'}")
        print(f"Has Login Prompt: {has_login}")
        
        if is_logged_in and not has_login:
            print()
            print("✓ Authentication confirmed!")
            print("Processing smoke test URLs...")
            print()
            
            # Process smoke tests
            results = []
            success_count = 0
            
            for i, cid in enumerate(SEED_IDS, 1):
                print(f"[{i}/5] {cid}")
                
                page = context.new_page()
                try:
                    url = f'https://www.toutiao.com/article/{cid}/'
                    page.goto(url, timeout=20000)
                    time.sleep(3)
                    
                    # Check content
                    content = page.evaluate('''() => {
                        const titleEl = document.querySelector('.article-title, h1, [class*="title"]');
                        const authorEl = document.querySelector('.author-name, .source');
                        const contentEl = document.querySelector('.article-content, [class*="content"], article');
                        
                        return {
                            title: titleEl ? titleEl.textContent.trim() : '',
                            author: authorEl ? authorEl.textContent.trim() : '',
                            content: contentEl ? contentEl.textContent.trim() : ''
                        };
                    }''')
                    
                    if content['title'] and len(content['content']) >= 300:
                        print(f"  ✓ Title: {content['title'][:50]}...")
                        print(f"  ✓ Content: {len(content['content'])} chars")
                        success_count += 1
                        
                        results.append({
                            'content_id': cid,
                            'status': 'SUCCESS',
                            'title': content['title'],
                            'chars': len(content['content'])
                        })
                    else:
                        print(f"  ✗ Insufficient content")
                        results.append({'content_id': cid, 'status': 'FAIL', 'reason': 'LOW_QUALITY'})
                        
                except Exception as e:
                    print(f"  ✗ Error: {e}")
                    results.append({'content_id': cid, 'status': 'ERROR', 'error': str(e)})
                finally:
                    try: page.close()
                    except: pass
                
                time.sleep(2)
            
            # Summary
            print()
            print(f"{'='*50}")
            print(f"SMOKE TEST RESULTS:")
            print(f"  Success: {success_count}/5")
            print(f"  Route Status: {'PASS' if success_count >= 3 else 'FAIL'}")
            
            # Save results
            output_path = BATCH4_DIR / "smoke_test_results.json"
            output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
            
        else:
            print()
            print("Please complete login in the Chrome window.")
            print("Then run this script again.")
    else:
        print("No pages found. Please open Toutiao in Chrome.")
        
except Exception as e:
    print(f"Error connecting to Chrome: {e}")
    print("Make sure Chrome is running on port 9224.")
