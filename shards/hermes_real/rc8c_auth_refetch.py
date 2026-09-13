#!/usr/bin/env python3
"""RC8C: Toutiao Authenticated Refetch Recovery - Check Login Status"""
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
OUTPUT_DIR = BASE / "analysis_batches"
SEED_DIR = OUTPUT_DIR / "batch_004_toutiao" / "SEED_WAVE_001"
REFETCH_DIR = OUTPUT_DIR / "batch_004_toutiao" / "SEED_WAVE_001_REFETCH"

print("="*70)
print("RC8C: Toutiao Auth Refetch Recovery")
print("="*70)
print()

# ============================================================
# 1. Check Chrome Status
# ============================================================
print("=== Step 1: Check Chrome Status ===")
print()

try:
    import urllib.request
    r = urllib.request.urlopen('http://127.0.0.1:9224/json', timeout=5)
    tabs = json.load(r)
    print(f"✓ Chrome running on port 9224")
    print(f"  Open tabs: {len(tabs)}")
    
    # Check if toutiao is open
    toutiao_tabs = [t for t in tabs if 'toutiao.com' in t.get('url', '')]
    if toutiao_tabs:
        print(f"  Toutiao tabs: {len(toutiao_tabs)}")
        for t in toutiao_tabs:
            print(f"    - {t.get('title', '')[:50]}")
    else:
        print("  No Toutiao tab open")
    print()
    
except Exception as e:
    print(f"✗ Chrome not running: {e}")
    print()
    print("=== ACTION REQUIRED: Start Chrome ===")
    print()
    print("Please run:")
    print('start chrome --remote-debugging-port=9224 --user-data-dir="F:/workspace/AI_Media_Matrix/browser_profiles/toutiao_benchmark_v1" "https://www.toutiao.com/"')
    exit(0)

# ============================================================
# 2. Connect to Chrome and Check Auth Status
# ============================================================
print("=== Step 2: Check Authentication Status ===")
print()

try:
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9224')
    context = browser.contexts[0]
    
    # Use existing page or create new one
    page = context.pages[0] if context.pages else context.new_page()
    
    # Navigate to toutiao home to check auth
    page.goto('https://www.toutiao.com/', timeout=15000)
    time.sleep(3)
    
    # Check if logged in by looking for "退出登录" (logout) button
    is_logged_in = False
    try:
        logout_btn = page.locator('text=退出登录').first
        if logout_btn.is_visible(timeout=2000):
            is_logged_in = True
    except:
        pass
    
    # Also check for login button
    has_login = False
    try:
        login_btn = page.locator('text=登录').first
        if login_btn.is_visible(timeout=2000):
            has_login = True
    except:
        pass
    
    print(f"Authentication Status:")
    print(f"  Logged In: {is_logged_in}")
    print(f"  Has Login Button: {has_login}")
    print()
    
    if not is_logged_in and has_login:
        print("=== STATUS: WAITING_FOR_LAN_LOGIN ===")
        print()
        print("【Toutiao Login Required】")
        print()
        print("Chrome: OPEN")
        print("Profile: toutiao_benchmark_v1")
        print("Port: 9224")
        print("Manual Login: REQUIRED")
        print("Waiting: YES")
        print()
        print("Please complete login in the Chrome window.")
        print("Then notify HERMES to continue.")
        print()
        
        # Save status
        status_path = OUTPUT_DIR / "batch_004_toutiao" / "TOUTIAO_LOGIN_STATUS.md"
        with open(status_path, 'w', encoding='utf-8') as f:
            f.write("# Toutiao Login Status\n\n")
            f.write("**Status**: WAITING_FOR_LAN_LOGIN\n")
            f.write("**Chrome Port**: 9224\n")
            f.write("**Profile**: toutiao_benchmark_v1\n")
            f.write("**Action Required**: Manual login needed\n\n")
        
        print(f"Status saved to: {status_path}")
        
        try: p.stop()
        except: pass
        exit(0)
    
    print("✓ Authentication verified")
    print()
    
except Exception as e:
    print(f"✗ Error checking auth: {e}")
    try: p.stop()
    except: pass
    exit(1)

# ============================================================
# 3. AUTH SMOKE TEST
# ============================================================
print("=== Step 3: AUTH SMOKE TEST ===")
print()

smoke_cid = "7591436947063702022"
smoke_url = f"https://www.toutiao.com/article/{smoke_cid}/"

print(f"Testing: {smoke_cid}")
print(f"URL: {smoke_url}")
print()

try:
    page.goto(smoke_url, timeout=20000)
    time.sleep(3)
    
    # Check for login wall
    page_content = page.content()
    is_login_wall = any(x in page_content for x in ['登录', '验证码', '安全验证', '请先登录'])
    
    # Extract content
    content = page.evaluate('''() => {
        const selectors = [
            '.article-content',
            '[class*="article-content"]',
            '[class*="content"] article',
            'article',
            '.text-content',
            'main article',
            '#articleContent',
            '.article_body'
        ];
        
        let contentEl = null;
        for (const sel of selectors) {
            const el = document.querySelector(sel);
            if (el && el.textContent.trim().length > 100) {
                contentEl = el;
                break;
            }
        }
        
        if (!contentEl) {
            contentEl = document.querySelector('main') || document.querySelector('[role="main"]');
        }
        
        return {
            title: document.querySelector('h1, .article-title')?.textContent.trim() || '',
            author: document.querySelector('.author-name, .source')?.textContent.trim() || '',
            content: contentEl ? contentEl.textContent.trim() : '',
            hasLoginWall: document.querySelector('.login-modal, [class*="login"]') !== null
        };
    }''')
    
    title = content.get('title', '')
    author = content.get('author', '')
    body_text = content.get('content', '')
    has_login_wall = content.get('hasLoginWall', False) or is_login_wall
    
    # Clean body text
    lines = [l.strip() for l in body_text.split('\n') if l.strip()]
    cleaned_lines = []
    for line in lines:
        # Skip non-article content
        if any(x in line for x in ['登录', '评论', '相关推荐', '查看更多', '举报', '分享', '收藏', '点赞']):
            continue
        if len(line) < 5 and any(x in line for x in ['关注', '推荐', '热点', '视频']):
            continue
        cleaned_lines.append(line)
    
    clean_text = '\n'.join(cleaned_lines)
    text_chars = len(clean_text)
    paragraph_count = len([l for l in cleaned_lines if l])
    
    print(f"Result:")
    print(f"  Title: {title[:50]}...")
    print(f"  Author: {author or 'NULL'}")
    print(f"  Body Chars: {text_chars}")
    print(f"  Paragraphs: {paragraph_count}")
    print(f"  Login Wall: {has_login_wall}")
    print()
    
    # Determine smoke result
    if has_login_wall or text_chars < 200:
        print("=== AUTH_BODY_SMOKE: FAIL ===")
        print()
        print("Reason: Login wall detected or insufficient body text")
        print()
        
        status_path = OUTPUT_DIR / "batch_004_toutiao" / "AUTH_SMOKE_STATUS.md"
        with open(status_path, 'w', encoding='utf-8') as f:
            f.write("# Auth Smoke Test Status\n\n")
            f.write("**Status**: FAIL\n")
            f.write(f"**CID**: {smoke_cid}\n")
            f.write(f"**Login Wall**: {has_login_wall}\n")
            f.write(f"**Body Chars**: {text_chars}\n")
            f.write(f"**Required**: >= 200\n\n")
            f.write("Action: Check Chrome authentication session\n")
        
        try: p.stop()
        except: pass
        exit(0)
    
    print("=== AUTH_BODY_SMOKE: PASS ===")
    print()
    
    # Save smoke result
    smoke_result = {
        'content_id': smoke_cid,
        'page_title': title,
        'body_selector_used': 'main article',
        'body_text_chars': text_chars,
        'paragraph_count': paragraph_count,
        'status': 'PASS'
    }
    
    smoke_path = OUTPUT_DIR / "batch_004_toutiao" / "AUTH_SMOKE_RESULT.json"
    with open(smoke_path, 'w', encoding='utf-8') as f:
        json.dump(smoke_result, f, ensure_ascii=False, indent=2)
    
    print(f"Smoke result saved to: {smoke_path}")
    print()
    
except Exception as e:
    print(f"✗ Smoke test error: {e}")
    try: p.stop()
    except: pass
    exit(1)

# ============================================================
# 4. Refetch All 20 Articles
# ============================================================
print("=== Step 4: Refetch All 20 Articles ===")
print()

REFETCH_DIR.mkdir(parents=True, exist_ok=True)

# Load original article list
articles_to_refetch = []
for f in sorted(SEED_DIR.glob('*.json')):
    with open(f, 'r', encoding='utf-8') as fh:
        try:
            data = json.load(fh)
            cid = data.get('content_id', '')
            if cid:
                articles_to_refetch.append({
                    'content_id': cid,
                    'title': data.get('title', ''),
                    'author': data.get('author', ''),
                    'url': data.get('url', '')
                })
        except:
            pass

print(f"Articles to refetch: {len(articles_to_refetch)}")
print()

success_count = 0
fail_count = 0
empty_count = 0
login_wall_count = 0

for i, art in enumerate(articles_to_refetch, 1):
    cid = art['content_id']
    url = art['url']
    
    print(f"[{i}/{len(articles_to_refetch)}] {cid}")
    
    try:
        page.goto(url, timeout=20000)
        time.sleep(2)
        
        # Extract content
        content = page.evaluate('''() => {
            const selectors = [
                '.article-content',
                '[class*="article-content"]',
                'article',
                '.text-content',
                'main article',
                '.article_body'
            ];
            
            let contentEl = null;
            for (const sel of selectors) {
                const el = document.querySelector(sel);
                if (el && el.textContent.trim().length > 100) {
                    contentEl = el;
                    break;
                }
            }
            
            if (!contentEl) {
                contentEl = document.querySelector('main') || document.querySelector('[role="main"]');
            }
            
            return {
                title: document.querySelector('h1, .article-title')?.textContent.trim() || '',
                author: document.querySelector('.author-name, .source')?.textContent.trim() || '',
                date: document.querySelector('.publish-time, time')?.textContent.trim() || '',
                content: contentEl ? contentEl.textContent.trim() : ''
            };
        }''')
        
        # Check for login wall
        page_content = page.content()
        if any(x in page_content for x in ['登录', '验证码', '安全验证']):
            print(f"  LOGIN WALL")
            login_wall_count += 1
            continue
        
        title = content.get('title', '')
        author = content.get('author', '')
        pub_date = content.get('date', '')
        body_text = content.get('content', '')
        
        # Clean body text
        lines = [l.strip() for l in body_text.split('\n') if l.strip()]
        cleaned_lines = []
        for line in lines:
            if any(x in line for x in ['登录', '评论', '相关推荐', '查看更多', '举报', '分享', '收藏', '点赞']):
                continue
            if len(line) < 5 and any(x in line for x in ['关注', '推荐', '热点', '视频']):
                continue
            cleaned_lines.append(line)
        
        clean_text = '\n'.join(cleaned_lines)
        text_chars = len(clean_text)
        paragraph_count = len([l for l in cleaned_lines if l])
        
        # Validate
        if text_chars < 200:
            print(f"  SHORT TEXT ({text_chars} chars)")
            empty_count += 1
            continue
        
        print(f"  ✓ {text_chars} chars, {paragraph_count} paras")
        
        # Save
        article_data = {
            'content_id': cid,
            'platform': 'toutiao',
            'content_type': 'ARTICLE',
            'title': title,
            'author': author,
            'publish_time': pub_date,
            'url': url,
            'full_text': clean_text,
            'text_chars': text_chars,
            'paragraph_count': paragraph_count,
            'status': 'DOWNLOADED',
            'fulltext_available': True,
            'simulated': 'FALSE',
            'wave': 'WAVE_001_REFETCH',
            'refetch_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        output_path = REFETCH_DIR / f'{cid}.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(article_data, f, ensure_ascii=False, indent=2)
        
        success_count += 1
        
    except Exception as e:
        error_type = type(e).__name__
        print(f"  ERROR: {error_type}")
        fail_count += 1
    finally:
        time.sleep(1)

print()
print("="*60)
print(f"REFETCH RESULTS:")
print(f"  Total: {len(articles_to_refetch)}")
print(f"  Success: {success_count}")
print(f"  Login Wall: {login_wall_count}")
print(f"  Empty/Short: {empty_count}")
print(f"  Error: {fail_count}")
print()

# ============================================================
# 5. Final Report
# ============================================================
print("=== Final Status ===")
print()

# Load refetched articles
refetched_articles = []
for f in sorted(REFETCH_DIR.glob('*.json')):
    with open(f, 'r', encoding='utf-8') as fh:
        try:
            data = json.load(fh)
            if data.get('content_id') and data.get('fulltext_available'):
                refetched_articles.append(data)
        except:
            pass

total_chars = sum([a.get('text_chars', 0) for a in refetched_articles])

print(f"Refetched Articles: {len(refetched_articles)}/20")
print(f"Total Text Chars: {total_chars}")
print(f"Average Chars/Article: {total_chars // max(1, len(refetched_articles))}")
print()

if len(refetched_articles) >= 18:
    print("✓ BATCH004_FULLTEXT_RECOVERY: PASS")
else:
    print(f"⚠ PARTIAL: {len(refetched_articles)}/20 articles recovered")

print()

# Close browser
try: p.stop()
except: pass
