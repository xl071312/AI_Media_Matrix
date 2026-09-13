#!/usr/bin/env python3
"""Batch 002 - Process 5 candidates with proper rate limiting"""
import json
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"

# Load registry
reg_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
registry = set()
with open(reg_path, 'r', encoding='utf-8') as f:
    for row in __import__('csv').DictReader(f):
        cid = row.get('content_id', '').strip().lstrip('\ufeff')
        if cid:
            registry.add(cid)

# Load selection
sel_path = SHARDS / "douyin_benchmark_selection.csv"
candidates = []
with open(sel_path, 'r', encoding='utf-8-sig') as f:
    for row in __import__('csv').DictReader(f):
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
            'perf': float(row.get('performance_score', 0)),
            'role': row.get('sample_role', ''),
            'viral': row.get('viral_type', ''),
            'likes': int(row.get('liked_count', 0)),
            'comments': int(row.get('comment_count', 0)),
            'favorites': int(row.get('collected_count', 0)),
            'shares': int(row.get('share_count', 0))
        })

# Topic filter
TOPIC_KW = ["赚钱", "变现", "信息差", "副业", "创业", "职场", "中产", "焦虑", 
            "消费", "陷阱", "AI", "搞钱", "翻身", "财富", "认知", "思维", 
            "商业", "加盟", "避坑", "投资", "黄金", "降级", "收入"]
OFF_MARKERS = ["游戏", "攻略", "三角洲", "原神", "动漫", "短剧", "美食", "健身", 
               "宠物", "旅游", "美妆", "穿搭", "数码", "汽车", "音乐", "搞笑", "电影", "明星"]

on_topic = []
for c in candidates:
    text = f"{c['title']} {c['keyword']}".lower()
    if any(m in text for m in OFF_MARKERS):
        continue
    matches = sum(1 for kw in TOPIC_KW if kw in text)
    if matches >= 1:
        on_topic.append(c)

print(f"ON_TOPIC candidates: {len(on_topic)}")

# Process first 5 with longer delays
results = []
for i, c in enumerate(on_topic[:5], 1):
    cid = c['cid']
    print(f"\n[{i}/5] {cid}")
    
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    context = browser.contexts[0]
    page = context.new_page()
    
    try:
        url = f'https://www.douyin.com/video/{cid}'
        page.goto(url, timeout=20000)
        time.sleep(3)
        
        content = page.content()
        blocked = any(x in content for x in ['安全验证', '登录', '二维码'])
        
        if blocked:
            print(f"  ✗ BLOCKED")
            results.append({'cid': cid, 'status': 'BLOCKED', **c})
            continue
        
        perf = page.evaluate('''() => {
            const entries = performance.getEntriesByType('resource');
            return entries.filter(e => e.name.includes('douyinvod'))
                .map(e => e.name.substring(0, 500));
        }''')
        
        video_url = next((u for u in perf if 'media-video' in u), None)
        audio_url = next((u for u in perf if 'media-audio' in u), None)
        
        title = page.title().replace(' - 抖音', '').strip()
        
        print(f"  ✓ OK | Video: {bool(video_url)} | Audio: {bool(audio_url)}")
        
        results.append({
            'cid': cid,
            'status': 'OK',
            'title': title,
            'video_url': video_url,
            'audio_url': audio_url,
            **c
        })
        
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        results.append({'cid': cid, 'status': f'ERROR', **c})
    finally:
        page.close()
        browser.close()
        p.stop()
    
    # Longer delay between requests
    delay = random.uniform(4, 8)
    print(f"  Waiting {delay:.1f}s...")
    time.sleep(delay)

# Save
output = SHARDS / "batch002_v3_results.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"\nSaved: {output}")
print(f"OK: {sum(1 for r in results if r.get('status')=='OK')}")
print(f"With Audio: {sum(1 for r in results if r.get('audio_url'))}")
