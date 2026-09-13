#!/usr/bin/env python3
"""Batch 004 Toutiao - Alternative Collection Strategy"""
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

print(f"=== BATCH 004 TOUTIAO (ALT STRATEGY) ===")
print(f"Already done: {len(done_cids)}")
print()

# Topic definitions for searching
TOPIC_QUERIES = [
    # 赚钱逻辑
    ("赚钱思维", "赚钱逻辑"),
    ("副业赚钱", "赚钱逻辑"),
    ("认知升级", "赚钱逻辑"),
    # 能力变现
    ("技能变现", "能力变现"),
    ("副业收入", "能力变现"),
    # 普通人收入
    ("普通人翻身", "普通人收入"),
    ("逆袭故事", "普通人收入"),
    # 职场收入
    ("职场加薪", "职场收入"),
    ("升职技巧", "职场收入"),
    # AI赚钱
    ("AI副业", "AI赚钱"),
    ("ChatGPT赚钱", "AI赚钱"),
    # 创业失败
    ("创业失败", "创业失败"),
    ("避坑指南", "创业失败"),
    # 信息差
    ("信息差", "信息差"),
    ("认知差距", "信息差"),
    # 消费认知
    ("消费主义", "消费认知"),
    ("存钱方法", "消费认知"),
    # 中产焦虑
    ("中产返贫", "中产焦虑"),
    ("财务自由", "赚钱逻辑"),
]

results = list(existing_results)
processed = 0

for i, (query, topic) in enumerate(TOPIC_QUERIES, 1):
    print(f"[{i}] Query: {query} (Topic: {topic})")
    
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    context = browser.contexts[0]
    page = context.new_page()
    
    try:
        # Try Toutiao search page
        search_url = f'https://so.toutiao.com/search?keyword={query}&source=input'
        page.goto(search_url, timeout=20000)
        time.sleep(3)
        
        # Try to get article results
        articles = page.evaluate('''() => {
            const items = document.querySelectorAll('.search-result-item, .result-item, [class*="result"]');
            return Array.from(items).slice(0, 5).map(item => ({
                title: item.querySelector('.title, h3, [class*="title"]')?.textContent.trim() || '',
                href: item.querySelector('a[href*="toutiao.com"]')?.href || '',
                author: item.querySelector('.author, [class*="author"]')?.textContent.trim() || ''
            }));
        }''')
        
        # If no results, try feed page
        if not articles or not any(a['href'] for a in articles):
            feed_url = 'https://www.toutiao.com'
            page.goto(feed_url, timeout=20000)
            time.sleep(3)
            
            articles = page.evaluate('''() => {
                const links = document.querySelectorAll('a[href*="/a"]');
                return Array.from(links).slice(0, 10).map(a => ({
                    title: a.textContent.trim().substring(0, 100),
                    href: a.href,
                    author: ''
                }));
            }''')
        
        # Filter valid articles
        valid_articles = []
        for art in articles:
            if art['href'] and 'toutiao.com' in art['href']:
                # Extract ID from URL
                cid_match = art['href'].split('/')[-1].replace('.html', '').replace('article/', '')
                if cid_match.isdigit() and len(cid_match) >= 10:
                    valid_articles.append({
                        'cid': cid_match,
                        'title': art['title'],
                        'href': art['href'],
                        'topic': topic
                    })
        
        print(f"  Found {len(valid_articles)} valid articles")
        
        # Process each article
        for art in valid_articles[:2]:
            cid = art['cid']
            if cid in done_cids:
                continue
            
            print(f"    Processing: {cid}")
            
            # Get article content
            page.goto(art['href'], timeout=20000)
            time.sleep(2)
            
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
            
            # Save article data
            article_data = {
                'content_id': cid,
                'platform': 'toutiao',
                'content_type': 'ARTICLE',
                'title': content['title'],
                'author': content['author'],
                'publish_time': content['date'],
                'primary_topic': art['topic'],
                'url': art['href'],
                'full_text': content['content'],
                'text_chars': len(content['content']),
                'status': 'DOWNLOADED'
            }
            
            # Save to JSON file
            article_path = MEDIA_DIR / f'{cid}.json'
            article_path.write_text(json.dumps(article_data, ensure_ascii=False, indent=2))
            
            results.append({
                'content_id': cid,
                'platform': 'toutiao',
                'content_type': 'ARTICLE',
                'title': content['title'],
                'primary_topic': art['topic'],
                'status': 'DOWNLOADED',
                'text_chars': len(content['content'])
            })
            
            done_cids.add(cid)
            processed += 1
            print(f"    ✓ Downloaded: {len(content['content'])} chars")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
    finally:
        try: page.close()
        except: pass
        try: browser.close()
        except: pass
        try: p.stop()
        except: pass
    
    time.sleep(random.uniform(2, 4))
    
    # Save progress
    if processed % 3 == 0:
        output = BATCH4_DIR / "batch004_progress.json"
        output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"  Progress saved ({len(results)} total)")

# Summary
articles_downloaded = len([r for r in results if r.get('status') == 'DOWNLOADED'])
print(f"\n{'='*50}")
print(f"BATCH 004 TOUTIAO RESULTS:")
print(f"  Total processed: {len(results)}")
print(f"  Articles downloaded: {articles_downloaded}")
print(f"  Target: 30 articles + 10 videos")

output = BATCH4_DIR / "batch004_progress.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"Saved to: {output}")