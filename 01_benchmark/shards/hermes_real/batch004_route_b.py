#!/usr/bin/env python3
"""Batch 004 Toutiao - Route B: Google/Bing Search Discovery"""
import json
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH4_DIR = BASE / "analysis_batches" / "batch_004_toutiao"
MEDIA_DIR = BASE / "media" / "batch_004_toutiao"

BATCH4_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Load existing results
existing_path = BATCH4_DIR / "batch004_progress.json"
existing_results = []
if existing_path.exists():
    with open(existing_path, 'r', encoding='utf-8') as f:
        existing_results = json.load(f)
done_cids = set(r.get('content_id', '') for r in existing_results)

print(f"=== BATCH 004 TOUTIAO - ROUTE B (SEARCH) ===")
print(f"Already done: {len(done_cids)}")
print()

# Topic definitions
TOPIC_QUERIES = [
    ("site:toutiao.com 赚钱思维 认知", "赚钱逻辑"),
    ("site:toutiao.com 副业变现 方法", "能力变现"),
    ("site:toutiao.com 普通人收入 翻身", "普通人收入"),
    ("site:toutiao.com 职场升职 加薪", "职场收入"),
    ("site:toutiao.com AI赚钱 副业", "AI赚钱"),
    ("site:toutiao.com 创业失败 教训", "创业失败"),
    ("site:toutiao.com 信息差 认知", "信息差"),
    ("site:toutiao.com 消费主义 陷阱", "消费认知"),
    ("site:toutiao.com 中产返贫 焦虑", "中产焦虑"),
    ("site:toutiao.com 财富思维 商业", "赚钱逻辑"),
]

results = list(existing_results)
processed = 0
success_count = 0

for i, (query, topic) in enumerate(TOPIC_QUERIES, 1):
    print(f"[{i}] Query: {query[:50]}...")
    
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    context = browser.contexts[0]
    page = context.new_page()
    
    try:
        # Use Google search
        search_url = f'https://www.google.com/search?q={query}'
        page.goto(search_url, timeout=20000)
        time.sleep(3)
        
        # Extract Toutiao article links
        articles = page.evaluate('''() => {
            const links = document.querySelectorAll('a[href*="toutiao.com"]');
            return Array.from(links).slice(0, 10).map(a => ({
                href: a.href,
                text: a.textContent.trim().substring(0, 80)
            }));
        }''')
        
        # Filter unique CIDs
        found_cids = set()
        for art in articles:
            href = art['href']
            if href and 'toutiao.com' in href:
                # Extract ID from various URL patterns
                parts = href.split('/')
                for part in parts:
                    if part.isdigit() and len(part) >= 10:
                        found_cids.add(part)
                        break
        
        print(f"  Found {len(found_cids)} unique CIDs")
        
        # Process each CID
        for cid in list(found_cids)[:3]:
            if cid in done_cids:
                continue
            
            print(f"    Processing: {cid}")
            
            # Try direct article URL
            article_url = f'https://www.toutiao.com/article/{cid}/'
            page.goto(article_url, timeout=20000)
            time.sleep(3)
            
            # Check for blocks
            page_content = page.content()
            blocked = any(x in page_content for x in ['登录', '验证码', '安全验证', '登陆'])
            
            if blocked:
                print(f"    ✗ Blocked")
                results.append({
                    'content_id': cid,
                    'platform': 'toutiao',
                    'content_type': 'ARTICLE',
                    'status': 'ACCESS_DEFERRED',
                    'reason': 'BLOCKED'
                })
                continue
            
            # Extract content
            content = page.evaluate('''() => {
                const titleEl = document.querySelector('.article-title, h1, .title, [class*="title"]');
                const authorEl = document.querySelector('.author-name, .source, [class*="author"]');
                const contentEl = document.querySelector('.article-content, .content, [class*="content"], article');
                const dateEl = document.querySelector('.publish-time, time, [class*="time"]');
                
                return {
                    title: titleEl ? titleEl.textContent.trim() : '',
                    author: authorEl ? authorEl.textContent.trim() : '',
                    content: contentEl ? contentEl.textContent.trim() : '',
                    date: dateEl ? dateEl.textContent.trim() : ''
                };
            }''')
            
            if not content['title']:
                print(f"    ✗ No title")
                continue
            
            if not content['content'] or len(content['content']) < 500:
                print(f"    ✗ Insufficient content ({len(content['content'])} chars)")
                continue
            
            print(f"    ✓ Title: {content['title'][:50]}...")
            print(f"    ✓ Content: {len(content['content'])} chars")
            
            # Save article data
            article_data = {
                'content_id': cid,
                'platform': 'toutiao',
                'content_type': 'ARTICLE',
                'title': content['title'],
                'author': content['author'],
                'publish_time': content['date'],
                'primary_topic': topic,
                'url': article_url,
                'full_text': content['content'],
                'text_chars': len(content['content']),
                'status': 'DOWNLOADED',
                'full_text_available': True
            }
            
            # Save to JSON file
            article_path = MEDIA_DIR / f'{cid}.json'
            article_path.write_text(json.dumps(article_data, ensure_ascii=False, indent=2))
            
            results.append({
                'content_id': cid,
                'platform': 'toutiao',
                'content_type': 'ARTICLE',
                'title': content['title'],
                'primary_topic': topic,
                'status': 'DOWNLOADED',
                'text_chars': len(content['content']),
                'full_text_available': True
            })
            
            done_cids.add(cid)
            processed += 1
            success_count += 1
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
    finally:
        try: page.close()
        except: pass
        try: browser.close()
        except: pass
        try: p.stop()
        except: pass
    
    time.sleep(random.uniform(3, 5))
    
    # Save progress
    if processed % 3 == 0:
        output = BATCH4_DIR / "batch004_progress.json"
        output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"  Progress saved ({len(results)} total, {success_count} success)")

# Summary
articles_downloaded = len([r for r in results if r.get('status') == 'DOWNLOADED'])
blocked = len([r for r in results if r.get('status') == 'ACCESS_DEFERRED'])

print(f"\n{'='*50}")
print(f"BATCH 004 TOUTIAO - ROUTE B RESULTS:")
print(f"  Total processed: {len(results)}")
print(f"  Articles downloaded: {articles_downloaded}")
print(f"  Blocked/Deferred: {blocked}")
print(f"  Success rate: {articles_downloaded/max(len(results),1):.0%}")
print(f"  Target: 30 articles")

output = BATCH4_DIR / "batch004_progress.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"Saved to: {output}")