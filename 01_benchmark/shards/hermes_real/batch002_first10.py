#!/usr/bin/env python3
"""Batch 002 Processing - First 10 candidates"""
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH2_DIR = BASE / "analysis_batches" / "batch_002"
MEDIA_DIR = BASE / "media" / "batch_002_smoke"

# Load candidates
candidates_path = SHARDS / "batch002_candidates.json"
with open(candidates_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
candidates = data['on_topic'][:10]

print(f"=== BATCH 002 - First 10 ===\n")

def extract_cid(raw_cid):
    if raw_cid.startswith('DY_REAL_'):
        return raw_cid.replace('DY_REAL_', '')
    return raw_cid

results = []

for i, cand in enumerate(candidates, 1):
    cid = extract_cid(cand['cid'])
    print(f"\n[{i}/10] {cid}")
    
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    context = browser.contexts[0]
    
    page = context.new_page()
    url = f'https://www.douyin.com/video/{cid}'
    
    try:
        page.goto(url, timeout=25000)
        time.sleep(3)
        
        # Check blocked
        content = page.content()
        blocked = any(x in content for x in ['安全验证', '登录', '二维码'])
        
        if blocked:
            print(f"  ✗ BLOCKED")
            results.append({'cid': cid, 'status': 'BLOCKED'})
            continue
        
        # Get URLs
        perf_urls = page.evaluate('''() => {
            const entries = performance.getEntriesByType('resource');
            return entries.filter(e => e.name.includes('douyinvod'))
                .map(e => e.name.substring(0, 400));
        }''')
        
        video_url = next((u for u in perf_urls if 'media-video' in u), None)
        audio_url = next((u for u in perf_urls if 'media-audio' in u), None)
        
        # Get metadata
        title = page.title().replace(' - 抖音', '').strip()
        
        # Get author from text
        body_text = page.inner_text('body')
        author_match = None
        for line in body_text.split('\n'):
            line = line.strip()
            if line and len(line) < 20 and '粉丝' in page.inner_text(f'[href*="/user/{cid}"]')[:100]:
                # Try to find author link
                pass
        
        # Simple author extraction
        author_links = page.query_selector_all('a[href*="/user/"]')
        author = author_links[0].text_content().strip() if author_links else 'N/A'
        
        print(f"  ✓ Loaded")
        print(f"    Title: {title[:50]}")
        print(f"    Author: {author[:30]}")
        print(f"    Video: {bool(video_url)}, Audio: {bool(audio_url)}")
        
        results.append({
            'cid': cid,
            'title': title,
            'author': author,
            'video_url': video_url,
            'audio_url': audio_url,
            'status': 'OK'
        })
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        results.append({'cid': cid, 'status': f'ERROR: {str(e)[:50]}'})
    finally:
        try:
            page.close()
        except:
            pass
        try:
            browser.close()
        except:
            pass
        try:
            p.stop()
        except:
            pass
    
    time.sleep(0.5)

# Save
output = SHARDS / "batch002_first10.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"\nSaved to: {output}")

ok = sum(1 for r in results if r.get('status') == 'OK')
with_audio = sum(1 for r in results if r.get('audio_url'))
print(f"OK: {ok}/10, With Audio: {with_audio}/10")