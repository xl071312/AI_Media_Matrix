#!/usr/bin/env python3
"""RC8B: Re-fetch Batch004 Articles with Real Content using Authenticated Chrome"""
import json
import csv
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
OUTPUT_DIR = BASE / "analysis_batches"
SEED_DIR = OUTPUT_DIR / "batch_004_toutiao" / "SEED_WAVE_001"
REFETCH_DIR = OUTPUT_DIR / "batch_004_toutiao" / "SEED_WAVE_001_REFETCH"

print("="*70)
print("RC8B: Re-fetch Batch004 Articles with Real Content")
print("="*70)
print()

# ============================================================
# 1. Connect to Existing Chrome (Port 9224)
# ============================================================
print("=== Connecting to Authenticated Chrome ===")
print()

try:
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9224')
    context = browser.contexts[0]
    page = context.pages[0] if context.pages else context.new_page()
    print("✓ Connected to Chrome on port 9224")
    print()
except Exception as e:
    print(f"✗ Error connecting to Chrome: {e}")
    exit(1)

# ============================================================
# 2. Load Existing Article List
# ============================================================
print("=== Loading Article List ===")
print()

articles_to_refetch = []
for f in sorted(SEED_DIR.glob('*.json')):
    with open(f, 'r', encoding='utf-8') as fh:
        try:
            data = json.load(fh)
            cid = data.get('content_id', '')
            if cid and len(data.get('full_text', '')) < 100:  # Needs refetch
                articles_to_refetch.append({
                    'content_id': cid,
                    'title': data.get('title', ''),
                    'author': data.get('author', ''),
                    'url': data.get('url', '')
                })
        except:
            pass

print(f"Articles needing refetch: {len(articles_to_refetch)}")
print()

# ============================================================
# 3. Re-fetch Each Article
# ============================================================
print("=== Re-fetching Articles ===")
print()

REFETCH_DIR.mkdir(parents=True, exist_ok=True)

success_count = 0
fail_count = 0
empty_body_count = 0

for i, art in enumerate(articles_to_refetch, 1):
    cid = art['content_id']
    url = art['url']
    
    print(f"[{i}/{len(articles_to_refetch)}] {cid}")
    
    try:
        # Navigate to article
        page.goto(url, timeout=30000)
        time.sleep(3)  # Wait for page load
        
        # Check for login wall
        page_content = page.content()
        if any(x in page_content for x in ['登录', '验证码', '安全验证', '请先登录']):
            print(f"  ✗ LOGIN WALL")
            fail_count += 1
            continue
        
        # Extract content using JavaScript
        content = page.evaluate('''() => {
            // Try multiple selectors for article content
            const selectors = [
                '.article-content',
                '[class*="article-content"]',
                '[class*="content"] article',
                'article',
                '.text-content',
                '[class*="text-content"]',
                'main article',
                '#articleContent',
                '.article_body',
                '[class*="article-body"]'
            ];
            
            let contentEl = null;
            for (const sel of selectors) {
                const el = document.querySelector(sel);
                if (el && el.textContent.trim().length > 200) {
                    contentEl = el;
                    break;
                }
            }
            
            // Fallback: get main content area
            if (!contentEl) {
                contentEl = document.querySelector('main') || 
                           document.querySelector('[role="main"]') ||
                           document.querySelector('.main');
            }
            
            if (contentEl) {
                return {
                    title: document.querySelector('h1, .article-title, [class*="title"]')?.textContent.trim() || '',
                    author: document.querySelector('.author-name, .source, [class*="author"]')?.textContent.trim() || '',
                    date: document.querySelector('.publish-time, time')?.textContent.trim() || '',
                    content: contentEl.textContent.trim()
                };
            }
            
            return {
                title: document.querySelector('h1')?.textContent.trim() || '',
                author: '',
                date: '',
                content: ''
            };
        }''')
        
        title = content.get('title', '')
        author = content.get('author', '')
        pub_date = content.get('date', '')
        body_text = content.get('content', '')
        
        # Clean up content - remove navigation, sidebar, footer
        # Keep only the main article text
        lines = body_text.split('\n')
        cleaned_lines = []
        in_article = False
        article_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Skip common non-article patterns
            if any(x in line for x in ['登录', '评论', '相关推荐', '查看更多', '举报', '分享', '收藏', '点赞']):
                continue
            # Skip short UI elements
            if len(line) < 10 and any(x in line for x in ['关注', '推荐', '热点', '视频', '财经']):
                continue
            article_lines.append(line)
        
        body_text = '\n'.join(article_lines)
        
        # Validate content
        text_chars = len(body_text)
        
        if text_chars < 100:
            print(f"  ✗ EMPTY BODY ({text_chars} chars)")
            empty_body_count += 1
            continue
        
        print(f"  ✓ Title: {title[:40]}...")
        print(f"  ✓ Content: {text_chars} chars, {len([l for l in body_text.split(chr(10)) if l.strip()])} paragraphs")
        
        # Save refetched article
        article_data = {
            'content_id': cid,
            'platform': 'toutiao',
            'content_type': 'ARTICLE',
            'title': title,
            'author': author,
            'publish_time': pub_date,
            'url': url,
            'full_text': body_text,
            'text_chars': text_chars,
            'paragraph_count': len([l for l in body_text.split('\n') if l.strip()]),
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
        print(f"  ✗ ERROR: {error_type}")
        fail_count += 1
    finally:
        time.sleep(2)

print()
print("="*60)
print(f"REFETCH RESULTS:")
print(f"  Total needed: {len(articles_to_refetch)}")
print(f"  Success: {success_count}")
print(f"  Failed (login wall): {fail_count}")
print(f"  Empty body: {empty_body_count}")
print()

# ============================================================
# 4. Generate Updated Manifest
# ============================================================
print("=== Generating Updated Manifest ===")
print()

# Load all refetched articles
refetched_articles = []
for f in sorted(REFETCH_DIR.glob('*.json')):
    with open(f, 'r', encoding='utf-8') as fh:
        try:
            data = json.load(fh)
            if data.get('content_id') and data.get('fulltext_available'):
                refetched_articles.append(data)
        except:
            pass

print(f"Loaded {len(refetched_articles)} refetched articles")
print()

# Generate manifest
manifest_path = OUTPUT_DIR / "batch_004_toutiao" / "CORPUS_CANONICAL_MANIFEST_V3.csv"
with open(manifest_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'content_id', 'platform', 'content_type', 'title', 'author',
        'publish_time', 'url', 'status', 'logic_analyzable', 'fulltext_available',
        'text_chars', 'paragraph_count', 'wave', 'simulated', 'refetch_status'
    ])
    writer.writeheader()
    
    for art in refetched_articles:
        writer.writerow({
            'content_id': art.get('content_id', ''),
            'platform': 'toutiao',
            'content_type': 'ARTICLE',
            'title': art.get('title', '')[:100],
            'author': art.get('author', '') or 'NULL',
            'publish_time': art.get('publish_time', '') or 'NULL',
            'url': art.get('url', ''),
            'status': art.get('status', 'DOWNLOADED'),
            'logic_analyzable': 'PENDING_MODEL_REVIEW',  # As per RC8B requirement
            'fulltext_available': 'TRUE' if art.get('text_chars', 0) > 0 else 'FALSE',
            'text_chars': art.get('text_chars', 0),
            'paragraph_count': art.get('paragraph_count', 0),
            'wave': art.get('wave', 'WAVE_001_REFETCH'),
            'simulated': 'FALSE',
            'refetch_status': 'SUCCESS'
        })

print(f"✓ Generated: {manifest_path.name}")
print()

# ============================================================
# 5. Final Statistics
# ============================================================
print("=== Final Statistics ===")
print()

total_chars = sum([a.get('text_chars', 0) for a in refetched_articles])
total_paragraphs = sum([a.get('paragraph_count', 0) for a in refetched_articles])

print(f"Refetched Articles: {len(refetched_articles)}/20")
print(f"Total Text Chars: {total_chars}")
print(f"Total Paragraphs: {total_paragraphs}")
print(f"Average Chars/Article: {total_chars // max(1, len(refetched_articles))}")
print()

if len(refetched_articles) == 20:
    print("✓ ALL 20 ARTICLES SUCCESSFULLY REFETCHED")
else:
    print(f"⚠ PARTIAL SUCCESS: {len(refetched_articles)}/20")

print()

# Close browser
try: p.stop()
except: pass

print("="*70)
