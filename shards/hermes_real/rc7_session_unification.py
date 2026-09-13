#!/usr/bin/env python3
"""RC7: Verify Existing 3 Articles and Fix Session Unification"""
import json
import csv
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
OUTPUT_DIR = BASE / "analysis_batches"
SEED_DIR = OUTPUT_DIR / "batch_004_toutiao" / "SEED_WAVE_001"

print("="*70)
print("RC7: Toutiao Session Unification + Verification")
print("="*70)
print()

# ============================================================
# 1. Verify Existing 3 Articles
# ============================================================
print("=== STEP 1: VERIFY EXISTING 3 ARTICLES ===")
print()

EXISTING_ARTICLES = [
    '7591436947063702022',
    '7652293131710300706',
    '7652914429046178313'
]

verification_results = []
passed_count = 0

for cid in EXISTING_ARTICLES:
    article_path = SEED_DIR / f'{cid}.json'
    
    if not article_path.exists():
        print(f"[FAIL] {cid}: File not found")
        verification_results.append({'content_id': cid, 'status': 'NOT_FOUND'})
        continue
    
    with open(article_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check requirements
    checks = {
        'title_exists': bool(data.get('title')),
        'full_text_exists': bool(data.get('full_text')),
        'chars_positive': data.get('text_chars', 0) > 0,
        'fulltext_usable': data.get('fulltext_available', False),
        'simulated_zero': data.get('simulated', 'FALSE') == 'FALSE'
    }
    
    all_pass = all(checks.values())
    if all_pass:
        passed_count += 1
        print(f"[PASS] {cid}: All checks passed")
        print(f"       Title: {data.get('title', '')[:50]}...")
        print(f"       Chars: {data.get('text_chars', 0)}")
    else:
        print(f"[FAIL] {cid}: { [k for k,v in checks.items() if not v] }")
    
    verification_results.append({
        'content_id': cid,
        'status': 'PASSED' if all_pass else 'FAILED',
        'checks': checks
    })

print()
print(f"Verification Result: {passed_count}/{len(EXISTING_ARTICLES)} PASSED")
print()

# ============================================================
# 2. Connect to Existing Chrome (Port 9224)
# ============================================================
print("=== STEP 2: CONNECT TO EXISTING CHROME (PORT 9224) ===")
print()

try:
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9224')
    context = browser.contexts[0]
    
    # Check current page
    if context.pages:
        page = context.pages[0]
        current_url = page.url
        print(f"Current URL: {current_url}")
        
        # Check auth status
        is_authenticated = False
        try:
            user_el = page.query_selector('[class*="user"], [class*="avatar"], .username')
            if user_el:
                is_authenticated = True
                print(f"User element found: {user_el.text_content()[:30]}")
        except:
            pass
        
        # Check for login prompts
        has_login_prompt = False
        try:
            content = page.content()
            if any(x in content for x in ['登录', '扫码', '二维码', '手机号']):
                has_login_prompt = True
        except:
            pass
        
        authenticated_session = is_authenticated and not has_login_prompt
        print(f"Authenticated Session: {authenticated_session}")
        print()
        
        if authenticated_session:
            print("✓ SESSION_UNIFICATION = PASS")
            session_status = "PASS"
        else:
            print("✗ SESSION_UNIFICATION = FAIL - Not authenticated")
            session_status = "FAIL"
    else:
        print("No pages found in context")
        session_status = "FAIL"
        
except Exception as e:
    print(f"Error connecting to Chrome: {e}")
    session_status = "FAIL"
    p = None

print()

# ============================================================
# 3. Process Remaining 17 Articles
# ============================================================
print("=== STEP 3: PROCESS REMAINING 17 ARTICLES ===")
print()

if session_status == "FAIL":
    print("Session unification failed. Cannot proceed with remaining articles.")
    print("Stopping RC7 execution.")
else:
    # Remaining seeds
    ALL_SEEDS = [
        '7591436947063702022', '7652293131710300706', '7652914429046178313',
        '7645692141699662362', '7674332815097414180', '7610800331743707700',
        '7636648275394822719', '7599942867901071906', '7626084420197401140',
        '7665187044485906946', '7649646067054576147', '7651163686538658344',
        '7682745433508069888', '7644625679841067560', '7653685852405350948',
        '7655054577745674795', '7606730984955904531', '7641201117593895464',
        '7611009791036588590', '7605955836908814858'
    ]
    
    DONE_CIDS = set(EXISTING_ARTICLES)
    REMAINING = [cid for cid in ALL_SEEDS if cid not in DONE_CIDS]
    
    print(f"Already saved: {len(DONE_CIDS)}")
    print(f"Remaining to process: {len(REMAINING)}")
    print()
    
    success_count = 0
    failure_reasons = {}
    
    for i, cid in enumerate(REMAINING, 1):
        print(f"[{i}/{len(REMAINING)}] {cid}")
        
        page = context.new_page()
        
        try:
            url = f'https://www.toutiao.com/article/{cid}/'
            page.goto(url, timeout=20000)
            
            import time
            time.sleep(3)
            
            # Check for blocks
            page_content = page.content()
            if any(x in page_content for x in ['登录', '验证码', '安全验证']):
                print(f"  ✗ LOGIN WALL / CAPTCHA")
                failure_reasons['BLOCKED'] = failure_reasons.get('BLOCKED', 0) + 1
                continue
            
            # Extract content
            content = page.evaluate('''() => {
                const titleEl = document.querySelector('.article-title, h1, [class*="title"]');
                const authorEl = document.querySelector('.author-name, .source, [class*="author"]');
                const contentEl = document.querySelector('.article-content, [class*="content"], article');
                const dateEl = document.querySelector('.publish-time, time');
                
                return {
                    title: titleEl ? titleEl.textContent.trim() : '',
                    author: authorEl ? authorEl.textContent.trim() : '',
                    content: contentEl ? contentEl.textContent.trim() : '',
                    date: dateEl ? dateEl.textContent.trim() : ''
                };
            }''')
            
            if not content['title']:
                print(f"  ✗ NO TITLE")
                failure_reasons['NO_TITLE'] = failure_reasons.get('NO_TITLE', 0) + 1
                continue
            
            if not content['content'] or len(content['content']) < 300:
                print(f"  ✗ LOW QUALITY ({len(content.get('content', ''))} chars)")
                failure_reasons['LOW_QUALITY'] = failure_reasons.get('LOW_QUALITY', 0) + 1
                continue
            
            print(f"  ✓ Title: {content['title'][:50]}...")
            print(f"  ✓ Content: {len(content['content'])} chars")
            
            # Save article
            article_data = {
                'content_id': cid,
                'platform': 'toutiao',
                'content_type': 'ARTICLE',
                'title': content['title'],
                'author': content['author'],
                'publish_time': content['date'],
                'url': url,
                'full_text': content['content'],
                'text_chars': len(content['content']),
                'status': 'DOWNLOADED',
                'fulltext_available': True,
                'simulated': 'FALSE'
            }
            
            article_path = SEED_DIR / f'{cid}.json'
            article_path.write_text(json.dumps(article_data, ensure_ascii=False, indent=2))
            
            success_count += 1
            DONE_CIDS.add(cid)
            
        except Exception as e:
            error_type = type(e).__name__
            print(f"  ✗ ERROR: {error_type}")
            failure_reasons[error_type] = failure_reasons.get(error_type, 0) + 1
        finally:
            try: page.close()
            except: pass
        
        import time as t
        t.sleep(2)
    
    print()
    print("="*60)
    print(f"REMAINING ARTICLES PROCESSED:")
    print(f"  Success: {success_count}/{len(REMAINING)}")
    print(f"  Failures: {failure_reasons}")
    print()
    print(f"TOTAL SAVED: {len(DONE_CIDS)}/{len(ALL_SEEDS)}")
    
    # Close browser
    try: p.stop()
    except: pass

print()
print("="*70)
print("RC7 EXECUTION COMPLETE")
print("="*70)