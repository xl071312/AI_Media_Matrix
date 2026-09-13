#!/usr/bin/env python3
"""Batch 004 Toutiao - Seed Wave 001: Direct URL Production"""
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

# Create dirs
SEED_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Load existing results
existing_path = BATCH4_DIR / "batch004_progress.json"
existing_results = []
if existing_path.exists():
    with open(existing_path, 'r', encoding='utf-8') as f:
        existing_results = json.load(f)
done_cids = set(r.get('content_id', '') for r in existing_results)

print(f"=== BATCH 004 TOUTIAO - SEED WAVE 001 ===")
print(f"Already done: {len(done_cids)}")
print()

# Seed IDs provided by main analysis model
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
failure_reasons = {}

# First 5 for smoke test
smoke_ids = SEED_IDS[:5]
all_ids = SEED_IDS

print(f"Seed IDs total: {len(all_ids)}")
print(f"Smoke test: {len(smoke_ids)}")
print()

def extract_toutiao_content(page, cid):
    """Extract content from Toutiao article page"""
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
    return content

def check_page_blocked(page):
    """Check if page is blocked by login/captcha"""
    content = page.content()
    blocked_signals = ['登录', '登陆', '验证码', '安全验证', '手机号', '扫码']
    return any(sig in content for sig in blocked_signals)

for i, cid in enumerate(all_ids, 1):
    if cid in done_cids:
        print(f"[{i}/{len(all_ids)}] {cid} - SKIP (already done)")
        continue
    
    is_smoke = cid in smoke_ids
    print(f"[{i}/{len(all_ids)}] {cid} {'(SMOKE)' if is_smoke else ''}")
    
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    context = browser.contexts[0]
    page = context.new_page()
    
    try:
        # Construct direct URL
        article_url = f'https://www.toutiao.com/article/{cid}/'
        
        # Open page
        page.goto(article_url, timeout=20000)
        time.sleep(3)
        
        # Check for blocks
        if check_page_blocked(page):
            print(f"  ✗ LOGIN WALL / CAPTCHA")
            failure_reasons['BLOCKED'] = failure_reasons.get('BLOCKED', 0) + 1
            results.append({
                'content_id': cid,
                'platform': 'toutiao',
                'content_type': 'ARTICLE',
                'status': 'ACCESS_DEFERRED',
                'reason': 'LOGIN_WALL'
            })
            continue
        
        # Extract content
        content = extract_toutiao_content(page, cid)
        
        if not content['title']:
            print(f"  ✗ NO TITLE")
            failure_reasons['NO_TITLE'] = failure_reasons.get('NO_TITLE', 0) + 1
            results.append({
                'content_id': cid,
                'platform': 'toutiao',
                'content_type': 'ARTICLE',
                'status': 'EMPTY_DOM'
            })
            continue
        
        if not content['content'] or len(content['content']) < 300:
            print(f"  ✗ INSUFFICIENT CONTENT ({len(content.get('content', ''))} chars)")
            failure_reasons['LOW_QUALITY'] = failure_reasons.get('LOW_QUALITY', 0) + 1
            results.append({
                'content_id': cid,
                'platform': 'toutiao',
                'content_type': 'ARTICLE',
                'status': 'LOW_QUALITY',
                'text_chars': len(content.get('content', ''))
            })
            continue
        
        print(f"  ✓ Title: {content['title'][:60]}...")
        print(f"  ✓ Content: {len(content['content'])} chars")
        print(f"  ✓ Author: {content['author'][:30] if content['author'] else 'N/A'}")
        
        # Save article data
        article_data = {
            'content_id': cid,
            'platform': 'toutiao',
            'content_type': 'ARTICLE',
            'title': content['title'],
            'author': content['author'],
            'creator_id': '',  # Will extract if available
            'publish_time': content['date'],
            'url': article_url,
            'full_text': content['content'],
            'text_chars': len(content['content']),
            'status': 'DOWNLOADED',
            'fulltext_available': True
        }
        
        # Save to JSON file
        article_path = SEED_DIR / f'{cid}.json'
        article_path.write_text(json.dumps(article_data, ensure_ascii=False, indent=2))
        
        results.append({
            'content_id': cid,
            'platform': 'toutiao',
            'content_type': 'ARTICLE',
            'title': content['title'],
            'author': content['author'],
            'status': 'DOWNLOADED',
            'text_chars': len(content['content']),
            'fulltext_available': True
        })
        
        done_cids.add(cid)
        processed += 1
        success_count += 1
        
    except Exception as e:
        error_type = type(e).__name__
        print(f"  ✗ ERROR: {error_type}")
        failure_reasons[error_type] = failure_reasons.get(error_type, 0) + 1
        results.append({
            'content_id': cid,
            'platform': 'toutiao',
            'content_type': 'ARTICLE',
            'status': 'ERROR',
            'error': str(e)
        })
    finally:
        try: page.close()
        except: pass
        try: browser.close()
        except: pass
        try: p.stop()
        except: pass
    
    time.sleep(random.uniform(2, 4))
    
    # Save progress
    if processed % 5 == 0:
        output = BATCH4_DIR / "batch004_progress.json"
        output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"  Progress saved ({len(results)} total, {success_count} success)")

# ============================================================
# Summary
# ============================================================
articles_downloaded = len([r for r in results if r.get('status') == 'DOWNLOADED'])
blocked = len([r for r in results if r.get('status') == 'ACCESS_DEFERRED'])
errors = len([r for r in results if r.get('status') == 'ERROR'])
low_quality = len([r for r in results if r.get('status') == 'LOW_QUALITY'])

print(f"\n{'='*60}")
print(f"BATCH 004 SEED WAVE 001 RESULTS:")
print(f"{'='*60}")
print(f"Total processed: {len(results)}")
print(f"Articles downloaded: {articles_downloaded}")
print(f"Blocked/Deferred: {blocked}")
print(f"Errors: {errors}")
print(f"Low Quality: {low_quality}")
print()
print(f"Failure reasons: {failure_reasons}")
print()

# Smoke test result
smoke_success = sum(1 for r in results[:5] if r.get('status') == 'DOWNLOADED')
print(f"Smoke test (first 5): {smoke_success}/5 SUCCESS")
print(f"Toutiao Seed Route: {'PASS' if smoke_success >= 3 else 'FAIL'}")
print()

# Save final results
output = BATCH4_DIR / "batch004_progress.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"Saved to: {output}")

# Generate status report
status_lines = [
    "# 【Batch 004 Toutiao - Seed Wave 001 Status】",
    "",
    f"**Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}",
    f"**Route**: Direct URL (Seed IDs)",
    f"**Status**: {'PASS' if smoke_success >= 3 else 'FAIL'}",
    "",
    "---",
    "",
    "## Summary",
    "",
    f"| Metric | Value |",
    f"|--------|-------|",
    f"| Total Processed | {len(results)} |",
    f"| Downloaded | {articles_downloaded} |",
    f"| Blocked | {blocked} |",
    f"| Errors | {errors} |",
    f"| Low Quality | {low_quality} |",
    f"| Success Rate | {articles_downloaded/max(len(results),1):.0%} |",
    "",
    "## Smoke Test",
    "",
    f"- First 5 seeds: {smoke_success}/5 success",
    f"- Route Status: {'PASS' if smoke_success >= 3 else 'FAIL'}",
    "",
    "## Failure Analysis",
    "",
    f"{json.dumps(failure_reasons, indent=2, ensure_ascii=False)}",
    "",
    "---",
    "",
    "## Next Steps",
    "",
    f"- If PASS: Continue with remaining {len(all_ids) - smoke_success} seeds",
    f"- If FAIL: Generate manual seed request",
    ""
]

status_path = SEED_DIR / "SEED_WAVE_001_STATUS.md"
status_path.write_text("\n".join(status_lines), encoding='utf-8')
print(f"Status saved to: {status_path}")
