#!/usr/bin/env python3
"""Batch 002 Production - Careful Processing with Rate Limiting"""
import csv
import json
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH2_DIR = BASE / "analysis_batches" / "batch_002"
MEDIA_DIR = BASE / "media" / "batch_002_smoke"

BATCH2_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Load registry
reg_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
registry = set()
with open(reg_path, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        cid = row.get('content_id', '').strip().lstrip('\ufeff')
        if cid:
            registry.add(cid)

# Load selection and filter
sel_path = SHARDS / "douyin_benchmark_selection.csv"
candidates = []
with open(sel_path, 'r', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        raw_cid = row.get('content_id', row.get('aweme_id', '')).strip().lstrip('\ufeff')
        if raw_cid.startswith('DY_REAL_'):
            raw_cid = raw_cid[8:]
        raw_cid = raw_cid.strip()
        
        if raw_cid in registry:
            continue
        
        candidates.append({
            'cid': raw_cid,
            'title': row.get('desc', '')[:100],
            'keyword': row.get('source_keyword', ''),
            'perf_score': float(row.get('performance_score', 0)),
            'likes': int(row.get('liked_count', 0)),
            'comments': int(row.get('comment_count', 0)),
            'favorites': int(row.get('collected_count', 0)),
            'shares': int(row.get('share_count', 0))
        })

print(f"Total candidates after dedupe: {len(candidates)}")

# Topic filter
TOPIC_KW = ["赚钱", "变现", "信息差", "副业", "创业", "职场", "中产", "焦虑", 
            "消费", "陷阱", "AI", "搞钱", "翻身", "财富", "认知", "思维", 
            "商业", "加盟", "避坑", "投资", "黄金", "降级", "收入"]
OFF_MARKERS = ["游戏", "攻略", "三角洲", "原神", "动漫", "短剧", "美食", "健身", 
               "宠物", "旅游", "美妆", "穿搭", "数码", "汽车", "音乐", "搞笑"]

on_topic = []
for c in candidates:
    text = f"{c['title']} {c['keyword']}".lower()
    if any(m in text for m in OFF_MARKERS):
        continue
    matches = sum(1 for kw in TOPIC_KW if kw in text)
    if matches >= 1:
        on_topic.append(c)

print(f"ON_TOPIC candidates: {len(on_topic)}")

# Process in smaller batches with delays
results = []
processed_cids = set()

def get_page_data(cid):
    """Get page data with retry"""
    for attempt in range(3):
        try:
            p = sync_playwright().start()
            browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
            context = browser.contexts[0]
            page = context.new_page()
            
            url = f'https://www.douyin.com/video/{cid}'
            page.goto(url, timeout=20000)
            time.sleep(2)
            
            content = page.content()
            blocked = any(x in content for x in ['安全验证', '登录', '二维码'])
            
            if blocked:
                page.close()
                browser.close()
                p.stop()
                if attempt < 2:
                    time.sleep(random.uniform(3, 6))
                    continue
                return {'cid': cid, 'status': 'BLOCKED'}
            
            # Get URLs
            perf = page.evaluate('''() => {
                const entries = performance.getEntriesByType('resource');
                return entries.filter(e => e.name.includes('douyinvod'))
                    .map(e => e.name.substring(0, 500));
            }''')
            
            video_url = next((u for u in perf if 'media-video' in u), None)
            audio_url = next((u for u in perf if 'media-audio' in u), None)
            
            title = page.title().replace(' - 抖音', '').strip()
            
            result = {
                'cid': cid,
                'status': 'OK',
                'title': title,
                'video_url': video_url,
                'audio_url': audio_url,
                'page_loaded': True
            }
            
            page.close()
            browser.close()
            p.stop()
            return result
            
        except Exception as e:
            try: page.close()
            except: pass
            try: browser.close()
            except: pass
            try: p.stop()
            except: pass
            
            if attempt < 2:
                time.sleep(random.uniform(2, 4))
    
    return {'cid': cid, 'status': f'ERROR'}

print("\nProcessing candidates...")
print("=" * 60)

for i, c in enumerate(on_topic[:30], 1):
    cid = c['cid']
    if cid in processed_cids:
        continue
    
    print(f"\n[{i}/30] {cid}")
    print(f"  {c['title'][:50]}")
    
    data = get_page_data(cid)
    data.update(c)
    
    if data.get('status') == 'OK':
        print(f"  ✓ OK | Video: {bool(data.get('video_url'))} | Audio: {bool(data.get('audio_url'))}")
        results.append(data)
        processed_cids.add(cid)
    else:
        print(f"  ✗ {data.get('status')}")
        results.append(data)
    
    # Rate limiting: 2-4 seconds between requests
    delay = random.uniform(2, 4)
    time.sleep(delay)

# Save progress
output = SHARDS / "batch002_production_v2.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))

# Summary
ok = sum(1 for r in results if r.get('status') == 'OK')
with_audio = sum(1 for r in results if r.get('audio_url'))
blocked = sum(1 for r in results if r.get('status') == 'BLOCKED')

print(f"\n{'=' * 60}")
print(f"SUMMARY:")
print(f"  Processed: {len(results)}")
print(f"  OK: {ok}")
print(f"  Blocked: {blocked}")
print(f"  With Audio: {with_audio}")
print(f"  Saved to: {output}")