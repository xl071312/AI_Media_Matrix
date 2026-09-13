#!/usr/bin/env python3
"""Batch 002 Processing - Open pages, check topic, get metadata"""
import json
import csv
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
import time

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH2_DIR = BASE / "analysis_batches" / "batch_002"
BATCH2_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR = BASE / "media" / "batch_002_smoke"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Load candidates
candidates_path = SHARDS / "batch002_candidates.json"
with open(candidates_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
candidates = data['on_topic'][:30]  # Target 30

print(f"=== BATCH 002 PROCESSING ===")
print(f"Candidates: {len(candidates)}")
print(f"Output: {BATCH2_DIR}\n")

def extract_cid(raw_cid):
    """Extract numeric content_id from DY_REAL_xxx format"""
    if raw_cid.startswith('DY_REAL_'):
        return raw_cid.replace('DY_REAL_', '')
    return raw_cid

def get_page_metadata(cid):
    """Get metadata from page via CDP"""
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    context = browser.contexts[0]
    
    page = context.new_page()
    url = f'https://www.douyin.com/video/{cid}'
    
    try:
        page.goto(url, timeout=30000)
        time.sleep(4)
        
        # Check for blocks
        content = page.content()
        block_indicators = ['安全验证', '登录', '二维码', '扫码', '验证码']
        blocked = any(ind in content for ind in block_indicators)
        
        if blocked:
            page.close()
            browser.close()
            p.stop()
            return {'blocked': True}
        
        # Get video element
        video = page.query_selector('video')
        has_video = video is not None
        
        # Get performance entries for CDN URLs
        perf_urls = page.evaluate('''() => {
            const entries = performance.getEntriesByType('resource');
            return entries
                .filter(e => e.name.includes('douyinvod'))
                .map(e => e.name.substring(0, 400));
        }''')
        
        # Extract video and audio URLs
        video_url = None
        audio_url = None
        for url in perf_urls:
            if 'media-video' in url and not video_url:
                video_url = url
            if 'media-audio' in url and not audio_url:
                audio_url = url
        
        # Get metadata from page
        title = page.evaluate('''() => {
            const h1 = document.querySelector('h1');
            return h1 ? h1.textContent.trim() : document.title.replace(' - 抖音', '');
        }''')
        
        author = page.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('a[href*="/user/"]'));
            return links.length > 0 ? links[0].textContent.trim() : 'N/A';
        }''')
        
        # Get stats
        stats = page.evaluate('''() => {
            const getText = (ref) => {
                const el = document.querySelector(`[ref="${ref}"]`);
                return el ? el.textContent.trim() : 'N/A';
            };
            return {
                likes: getText('e13'),
                comments: getText('e14'),
                favorites: getText('e15'),
                shares: getText('e16')
            };
        }''')
        
        result = {
            'cid': cid,
            'url': url,
            'page_loaded': True,
            'blocked': False,
            'has_video': has_video,
            'video_url': video_url,
            'audio_url': audio_url,
            'title': title,
            'author': author,
            'stats': stats
        }
        
        page.close()
        browser.close()
        p.stop()
        return result
        
    except Exception as e:
        print(f"  Error: {e}")
        page.close()
        browser.close()
        p.stop()
        return {'cid': cid, 'error': str(e)}

def main():
    results = []
    
    for i, cand in enumerate(candidates, 1):
        cid = extract_cid(cand['cid'])
        print(f"\n[{i}/30] {cid}")
        print(f"  Title: {cand['title'][:60]}")
        print(f"  Keyword: {cand['source_keyword']}")
        
        meta = get_page_metadata(cid)
        results.append(meta)
        
        if meta.get('blocked'):
            print(f"  ✗ BLOCKED")
        elif meta.get('error'):
            print(f"  ✗ ERROR: {meta['error']}")
        else:
            print(f"  ✓ Loaded: has_video={meta.get('has_video')}")
            print(f"    Title: {meta.get('title', 'N/A')[:60]}")
            print(f"    Author: {meta.get('author', 'N/A')}")
            print(f"    Video URL: {bool(meta.get('video_url'))}")
            print(f"    Audio URL: {bool(meta.get('audio_url'))}")
        
        # Small delay between requests
        time.sleep(1)
    
    # Save results
    output_path = SHARDS / "batch002_page_check.json"
    output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\nSaved to: {output_path}")
    
    # Summary
    loaded = sum(1 for r in results if r.get('page_loaded') and not r.get('blocked'))
    with_audio = sum(1 for r in results if r.get('audio_url'))
    print(f"\nSummary: {loaded}/{len(results)} loaded, {with_audio}/{len(results)} with audio")
    
    return results

if __name__ == "__main__":
    main()