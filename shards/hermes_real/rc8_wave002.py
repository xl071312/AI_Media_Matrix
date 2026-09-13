#!/usr/bin/env python3
"""RC8: Toutiao Wave002 - Discovery + Processing"""
import json
import csv
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
OUTPUT_DIR = BASE / "analysis_batches"
SHARDS = BASE / "shards" / "hermes_real"
SEED_DIR = OUTPUT_DIR / "batch_004_toutiao" / "SEED_WAVE_001"

print("="*70)
print("RC8: Toutiao Wave002 - Discovery and Processing")
print("="*70)
print()

# ============================================================
# 1. Load Existing Ledger and Articles
# ============================================================
print("=== Loading Existing Data ===")
print()

# Load global ledger V3
ledger_path = OUTPUT_DIR / "GLOBAL_CORPUS_LEDGER_V3.csv"
with open(ledger_path, 'r', encoding='utf-8') as f:
    ledger = list(csv.DictReader(f))

existing_cids = set()
for row in ledger:
    cid = row.get('content_id', '')
    if cid:
        existing_cids.add(cid)

print(f"Existing CIDs in ledger: {len(existing_cids)}")

# Load Batch004 articles
b004_articles = {}
for f in SEED_DIR.glob('*.json'):
    with open(f, 'r', encoding='utf-8') as fh:
        try:
            data = json.load(fh)
            cid = data.get('content_id', '')
            if cid:
                b004_articles[cid] = data
        except:
            pass

print(f"Batch004 articles loaded: {len(b004_articles)}")
print()

# ============================================================
# 2. Connect to Existing Chrome (Port 9224)
# ============================================================
print("=== Connecting to Chrome (Port 9224) ===")
print()

try:
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9224')
    context = browser.contexts[0]
    
    # Use existing page or create new one
    page = context.pages[0] if context.pages else context.new_page()
    print(f"✓ Connected. Pages: {len(context.pages)}")
    print()
    
except Exception as e:
    print(f"✗ Error connecting to Chrome: {e}")
    exit(1)

# ============================================================
# 3. Discover Wave002 Candidates from Wave001 Articles
# ============================================================
print("=== Step 1: Discover Wave002 Candidates ===")
print()

candidates = []
candidate_sources = []

# Get candidate URLs from existing articles' recommendation sections
# We'll navigate to a few articles and extract recommended links
articles_to_explore = list(b004_articles.keys())[:5]  # Explore first 5 articles

for i, cid in enumerate(articles_to_explore, 1):
    print(f"[{i}/5] Exploring recommendations from {cid}...")
    
    url = f'https://www.toutiao.com/article/{cid}/'
    page.goto(url, timeout=20000)
    time.sleep(3)
    
    # Extract recommended article links
    recommended = page.evaluate('''() => {
        const links = [];
        // Look for recommendation sections
        const recSections = document.querySelectorAll('[class*="recommend"], [class*="related"], [class*="hot"]');
        recSections.forEach(section => {
            section.querySelectorAll('a[href*="article"]').forEach(a => {
                const href = a.getAttribute('href') || '';
                const title = a.textContent.trim().substring(0, 100);
                // Extract content_id from URL
                const match = href.match(/article\/(\d+)/);
                if (match) {
                    const content_id = match[1];
                    if (!links.some(l => l['content_id'] === content_id)) {
                        links.push({
                            'content_id': content_id,
                            'url': 'https://www.toutiao.com' + href,
                            'title': title,
                            'source': 'recommendation'
                        });
                    }
                }
            });
        });
        
        // Also look for author's other articles
        const authorLinks = document.querySelectorAll('a[href*="user/"], a[href*="author/"]');
        authorLinks.forEach(a => {
            const href = a.getAttribute('href') || '';
            if (href.includes('article')) {
                const match = href.match(/article\/(\d+)/);
                if (match) {
                    const content_id = match[1];
                    const title = a.textContent.trim().substring(0, 100);
                    if (!links.some(l => l['content_id'] === content_id)) {
                        links.push({
                            'content_id': content_id,
                            'url': 'https://www.toutiao.com' + href,
                            'title': title,
                            'source': 'author_page'
                        });
                    }
                }
            }
        });
        
        return links.slice(0, 10);  // Limit to 10 per article
    }''')
    
    for rec in recommended:
        rec_cid = rec.get('content_id', '')
        if rec_cid and rec_cid not in existing_cids and rec_cid not in [c['content_id'] for c in candidates]:
            candidates.append({
                'content_id': rec_cid,
                'url': rec.get('url', ''),
                'title': rec.get('title', '')[:100],
                'source': rec.get('source', 'recommendation'),
                'source_content_id': cid
            })
    
    time.sleep(2)

print()
print(f"Discovered {len(candidates)} unique candidates")
print()

# Save candidates
candidates_path = OUTPUT_DIR / "batch_004_toutiao" / "TOUTIAO_WAVE002_CANDIDATES.csv"
with open(candidates_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['source_content_id', 'candidate_content_id', 'candidate_url', 'discovery_source', 'title_if_visible', 'author_if_visible'])
    writer.writeheader()
    for c in candidates:
        writer.writerow({
            'source_content_id': c.get('source_content_id', ''),
            'candidate_content_id': c.get('content_id', ''),
            'candidate_url': c.get('url', ''),
            'discovery_source': c.get('source', ''),
            'title_if_visible': c.get('title', ''),
            'author_if_visible': ''
        })

print(f"✓ Saved candidates: {candidates_path}")
print()

# ============================================================
# 4. Process Wave002 Candidates
# ============================================================
print("=== Step 2: Process Wave002 Candidates ===")
print()

wave002_dir = OUTPUT_DIR / "batch_004_toutiao" / "SEED_WAVE_002"
wave002_dir.mkdir(parents=True, exist_ok=True)

processed_count = 0
qualified_count = 0
skipped_duplicate = 0
failed_count = 0

# Process up to 30 candidates
for i, candidate in enumerate(candidates[:30], 1):
    cid = candidate['content_id']
    
    # Check duplicate
    if cid in existing_cids:
        print(f"[{i}] {cid} - SKIP (duplicate)")
        skipped_duplicate += 1
        continue
    
    print(f"[{i}] {cid}")
    
    try:
        page.goto(candidate['url'], timeout=20000)
        time.sleep(3)
        
        # Check for blocks
        page_content = page.content()
        if any(x in page_content for x in ['登录', '验证码', '安全验证']):
            print(f"  ✗ LOGIN WALL / CAPTCHA")
            failed_count += 1
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
            failed_count += 1
            continue
        
        if not content['content'] or len(content['content']) < 300:
            print(f"  ✗ LOW QUALITY ({len(content.get('content', ''))} chars)")
            failed_count += 1
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
            'url': candidate['url'],
            'full_text': content['content'],
            'text_chars': len(content['content']),
            'status': 'DOWNLOADED',
            'fulltext_available': True,
            'simulated': 'FALSE',
            'wave': 'WAVE_002'
        }
        
        article_path = wave002_dir / f'{cid}.json'
        article_path.write_text(json.dumps(article_data, ensure_ascii=False, indent=2))
        
        qualified_count += 1
        processed_count += 1
        
    except Exception as e:
        error_type = type(e).__name__
        print(f"  ✗ ERROR: {error_type}")
        failed_count += 1
    finally:
        time.sleep(2)

print()
print("="*60)
print(f"WAVE 002 RESULTS:")
print(f"  Discovered: {len(candidates)}")
print(f"  Processed: {processed_count}")
print(f"  Qualified: {qualified_count}")
print(f"  Skipped (duplicate): {skipped_duplicate}")
print(f"  Failed: {failed_count}")
print()

# ============================================================
# 5. Update Global Ledger
# ============================================================
print("=== Updating Global Ledger ===")
print()

# Load all articles
all_wave002 = []
for f in wave002_dir.glob('*.json'):
    with open(f, 'r', encoding='utf-8') as fh:
        try:
            data = json.load(fh)
            if data.get('content_id'):
                all_wave002.append(data)
        except:
            pass

# Generate V4 ledger
fieldnames = [
    'global_content_key', 'platform', 'content_id', 'batch',
    'unique_valid', 'logic_analyzable', 'logic_exclusion_reason',
    'near_duplicate_group_id', 'independent_observation',
    'performance_verified', 'transcript_usable', 'fulltext_usable',
    'content_type', 'simulated', 'notes'
]

with open(OUTPUT_DIR / "GLOBAL_CORPUS_LEDGER_V4.csv", 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    # Write existing V3 rows
    with open(ledger_path, 'r', encoding='utf-8') as v3:
        for row in csv.DictReader(v3):
            writer.writerow(row)
    
    # Write new Wave002 articles
    for art in all_wave002:
        cid = art.get('content_id', '')
        if not cid:
            continue
        # Skip if already in V3
        if any(r.get('content_id') == cid and r.get('batch') == 'batch_004' for r in ledger):
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
            'notes': 'SEED_WAVE_002'
        })

print(f"✓ Generated GLOBAL_CORPUS_LEDGER_V4.csv")
print()

# ============================================================
# 6. Final Statistics
# ============================================================
print("=== Final Statistics ===")
print()

with open(OUTPUT_DIR / "GLOBAL_CORPUS_LEDGER_V4.csv", 'r', encoding='utf-8') as f:
    v4_rows = list(csv.DictReader(f))

final_unique = len(v4_rows)
final_logic = len([r for r in v4_rows if r.get('logic_analyzable') == 'True'])
final_independent = len([r for r in v4_rows if r.get('independent_observation') == 'True'])
final_perf = len([r for r in v4_rows if r.get('performance_verified') == 'True'])

# Batch breakdown
b001_count = len([r for r in v4_rows if r.get('batch') == 'batch_001'])
b002_count = len([r for r in v4_rows if r.get('batch') == 'batch_002'])
b003_count = len([r for r in v4_rows if r.get('batch') == 'batch_003'])
b004_count = len([r for r in v4_rows if r.get('batch') == 'batch_004'])

print(f"Unique CID Union: {final_unique}")
print(f"Logic Analyzable Unique: {final_logic}/100")
print(f"Independent Logic Observations: {final_independent}")
print(f"Performance Verified: {final_perf}")
print()
print(f"Batch001: {b001_count} unique")
print(f"Block002: {b002_count} qualified")
print(f"Block003: {b003_count} done")
print(f"Block004: {b004_count} articles")
print()

if final_logic >= 100:
    print("="*70)
    print("★ GOAL REACHED: GLOBAL LOGIC >= 100 ★")
    print("="*70)
else:
    print(f"Gap to 100: {100 - final_logic}")

print()

# Close browser
try: p.stop()
except: pass
