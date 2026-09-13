#!/usr/bin/env python3
"""RC7: Use Existing Page for Article Collection"""
import json
import csv
from pathlib import Path
from playwright.sync_api import sync_playwright
import time as t

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
OUTPUT_DIR = BASE / "analysis_batches"
SEED_DIR = OUTPUT_DIR / "batch_004_toutiao" / "SEED_WAVE_001"

print("="*70)
print("RC7: Article Collection via Existing Page")
print("="*70)
print()

# ============================================================
# 1. Connect and Use Existing Page
# ============================================================
print("=== Connecting to Chrome (Port 9224) ===")
print()

p = sync_playwright().start()
browser = p.chromium.connect_over_cdp('http://127.0.0.1:9224')
context = browser.contexts[0]

# Use existing page
existing_page = context.pages[0] if context.pages else None
print(f"Existing pages: {len(context.pages)}")

# ============================================================
# 2. Process Remaining 17 Articles
# ============================================================
print()
print("=== Processing Remaining 17 Articles ===")
print()

ALL_SEEDS = [
    '7591436947063702022', '7652293131710300706', '7652914429046178313',
    '7645692141699662362', '7674332815097414180', '7610800331743707700',
    '7636648275394822719', '7599942867901071906', '7626084420197401140',
    '7665187044485906946', '7649646067054576147', '7651163686538658344',
    '7682745433508069888', '7644625679841067560', '7653685852405350948',
    '7655054577745674795', '7606730984955904531', '7641201117593895464',
    '7611009791036588590', '7605955836908814858'
]

DONE_CIDS = set()
for f in SEED_DIR.glob('*.json'):
    with open(f, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
        DONE_CIDS.add(data.get('content_id', ''))

REMAINING = [cid for cid in ALL_SEEDS if cid not in DONE_CIDS]
print(f"Already saved: {len(DONE_CIDS)}")
print(f"Remaining to process: {len(REMAINING)}")
print()

success_count = 0
failure_reasons = {}

for i, cid in enumerate(REMAINING, 1):
    print(f"[{i}/{len(REMAINING)}] {cid}")
    
    try:
        # Navigate existing page to new URL
        url = f'https://www.toutiao.com/article/{cid}/'
        existing_page.goto(url, timeout=20000)
        t.sleep(4)  # Longer wait for page load
        
        # Check for blocks
        page_content = existing_page.content()
        if any(x in page_content for x in ['登录', '验证码', '安全验证']):
            print(f"  ✗ LOGIN WALL / CAPTCHA")
            failure_reasons['BLOCKED'] = failure_reasons.get('BLOCKED', 0) + 1
            continue
        
        # Extract content from the page
        content = existing_page.evaluate('''() => {
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
    
    t.sleep(2)

print()
print("="*60)
print(f"RESULTS:")
print(f"  Success: {success_count}/{len(REMAINING)}")
print(f"  Failures: {failure_reasons}")
print()
print(f"TOTAL SAVED: {len(DONE_CIDS)}/{len(ALL_SEEDS)}")
print()

# ============================================================
# 3. Generate Updated Ledger V3
# ============================================================
print("=== GENERATING GLOBAL_CORPUS_LEDGER_V3 ===")

# Load existing V2 ledger
ledger_v2_path = OUTPUT_DIR / "GLOBAL_CORPUS_LEDGER_V2.csv"
with open(ledger_v2_path, 'r', encoding='utf-8') as f:
    ledger_v2 = list(csv.DictReader(f))

# Load all articles
all_articles = []
for f in SEED_DIR.glob('*.json'):
    with open(f, 'r', encoding='utf-8') as fh:
        try:
            data = json.load(fh)
            all_articles.append(data)
        except:
            pass

# Generate V3
fieldnames = [
    'global_content_key', 'platform', 'content_id', 'batch',
    'unique_valid', 'logic_analyzable', 'logic_exclusion_reason',
    'near_duplicate_group_id', 'independent_observation',
    'performance_verified', 'transcript_usable', 'fulltext_usable',
    'content_type', 'simulated', 'notes'
]

with open(OUTPUT_DIR / "GLOBAL_CORPUS_LEDGER_V3.csv", 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    # Write existing V2 rows
    for row in ledger_v2:
        writer.writerow(row)
    
    # Write new Batch004 articles
    for art in all_articles:
        cid = art.get('content_id', '')
        if not cid:
            continue
        # Skip if already in V2
        if any(r.get('content_id') == cid and r.get('batch') == 'batch_004' for r in ledger_v2):
            continue
        
        writer.writerow({
            'global_content_key': f"TOUTIAO:{cid}",
            'platform': 'toutiao',
            'content_id': cid,
            'batch': 'batch_004',
            'unique_valid': True,
            'logic_analyzable': True,
            'logic_exclusion_reason': '',
            'near_duplicate_group_id': '',
            'independent_observation': True,
            'performance_verified': False,
            'transcript_usable': 'FALSE',
            'fulltext_usable': 'TRUE',
            'content_type': 'ARTICLE',
            'simulated': 'FALSE',
            'notes': 'SEED_WAVE_001'
        })

print(f"✓ Generated GLOBAL_CORPUS_LEDGER_V3.csv")

# Compute final stats
with open(OUTPUT_DIR / "GLOBAL_CORPUS_LEDGER_V3.csv", 'r', encoding='utf-8') as f:
    v3_rows = list(csv.DictReader(f))

final_unique = len(v3_rows)
final_logic = len([r for r in v3_rows if r.get('logic_analyzable') == 'True'])
final_independent = len([r for r in v3_rows if r.get('independent_observation') == 'True'])
final_perf = len([r for r in v3_rows if r.get('performance_verified') == 'True'])

print()
print("=== FINAL STATISTICS ===")
print(f"Unique CID Union: {final_unique}")
print(f"Logic Analyzable Unique: {final_logic}/100")
print(f"Independent Logic Observations: {final_independent}")
print(f"Performance Verified: {final_perf}")
print()
print(f"Gap to 100: {100 - final_logic}")
print()
print("="*70)

# Close browser
try: p.stop()
except: pass