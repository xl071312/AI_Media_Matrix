#!/usr/bin/env python3
"""Toutiao Seed Processing - After Login Confirmation"""
import json
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH4_DIR = BASE / "analysis_batches" / "batch_004_toutiao"
MEDIA_DIR = BASE / "media" / "batch_004_toutiao"
SEED_DIR = BATCH4_DIR / "SEED_WAVE_001"

SEED_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Load existing results
existing_path = BATCH4_DIR / "batch004_progress.json"
existing_results = []
if existing_path.exists():
    with open(existing_path, 'r', encoding='utf-8') as f:
        existing_results = json.load(f)
done_cids = set(r.get('content_id', '') for r in existing_results)

print(f"=== TOUTIAO SEED PROCESSING (Authenticated) ===")
print(f"Already done: {len(done_cids)}")
print()

# Seed IDs
SEED_IDS = [
    '7591436947063702022',
    '7652293131710300706',
    '7652914429046178313',
    '7645692141699662362',
    '7674332815097414180',
    '7610800331743707700',
    '7636648275394822719',
    '7599942867901071906',
    '7626084420197401140',
    '7665187044485906946',
    '7649646067054576147',
    '7651163686538658344',
    '7682745433508069888',
    '7644625679841067560',
    '7653685852405350948',
    '7655054577745674795',
    '7606730984955904531',
    '7641201117593895464',
    '7611009791036588590',
    '7605955836908814858'
]

results = list(existing_results)
processed = 0
success_count = 0

# Connect to existing Chrome
print("Connecting to Chrome on port 9224...")
p = sync_playwright().start()
browser = p.chromium.connect_over_cdp('http://127.0.0.1:9224')
context = browser.contexts[0]

for i, cid in enumerate(SEED_IDS, 1):
    if cid in done_cids:
        continue
    
    print(f"[{i}/20] {cid}")
    
    page = context.new_page()
    
    try:
        article_url = f'https://www.toutiao.com/article/{cid}/'
        page.goto(article_url, timeout=20000)
        time.sleep(3)
        
        # Check for blocks
        page_content = page.content()
        blocked = any(x in page_content for x in ['登录', '验证码', '安全验证'])
        
        if blocked:
            print(f"  ✗ LOGIN REQUIRED")
            results.append({'content_id': cid, 'status': 'ACCESS_DEFERRED', 'reason': 'LOGIN'})
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
        
        if not content['title'] or not content['content'] or len(content['content']) < 300:
            print(f"  ✗ LOW QUALITY")
            results.append({'content_id': cid, 'status': 'LOW_QUALITY'})
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
            'url': article_url,
            'full_text': content['content'],
            'text_chars': len(content['content']),
            'status': 'DOWNLOADED'
        }
        
        article_path = SEED_DIR / f'{cid}.json'
        article_path.write_text(json.dumps(article_data, ensure_ascii=False, indent=2))
        
        results.append({
            'content_id': cid,
            'platform': 'toutiao',
            'content_type': 'ARTICLE',
            'title': content['title'],
            'status': 'DOWNLOADED',
            'text_chars': len(content['content'])
        })
        
        done_cids.add(cid)
        processed += 1
        success_count += 1
        
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        results.append({'content_id': cid, 'status': 'ERROR', 'error': str(e)})
    finally:
        try: page.close()
        except: pass
    
    time.sleep(random.uniform(2, 3))

# Summary
articles_downloaded = len([r for r in results if r.get('status') == 'DOWNLOADED'])
print(f"\n{'='*50}")
print(f"RESULTS:")
print(f"  Downloaded: {articles_downloaded}")
print(f"  Target: 20")
print(f"  Success Rate: {articles_downloaded/20:.0%}")

output = BATCH4_DIR / "batch004_progress.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"Saved to: {output}")

try: p.stop()
except: pass
