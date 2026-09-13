#!/usr/bin/env python3
"""Batch 002 - Continue Production: Download + ASR for remaining candidates"""
import csv
import json
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright
import urllib.request
import ssl

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH2_DIR = BASE / "analysis_batches" / "batch_002"
MEDIA_DIR = BASE / "media" / "batch_002_smoke"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"

MEDIA_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

# Load registry
reg_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
registry = set()
with open(reg_path, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        cid = row.get('content_id', '').strip().lstrip('\ufeff')
        if cid:
            registry.add(cid)

# Load selection
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

# Load existing qualified from admission QA
qa_path = SHARDS / "batch002_admission_qa.json"
qualified_cids = set()
if qa_path.exists():
    with open(qa_path, 'r', encoding='utf-8') as f:
        qa_data = json.load(f)
    for r in qa_data:
        if r.get('status') == 'QUALIFIED':
            qualified_cids.add(r['content_id'])

# Topic filter
TOPIC_KW = ["赚钱", "变现", "信息差", "副业", "创业", "职场", "中产", "焦虑", 
            "消费", "陷阱", "AI", "搞钱", "翻身", "财富", "认知", "思维", 
            "商业", "加盟", "避坑", "投资", "黄金", "降级", "收入"]
OFF_MARKERS = ["游戏", "攻略", "三角洲", "原神", "动漫", "短剧", "美食", "健身", 
               "宠物", "旅游", "美妆", "穿搭", "数码", "汽车", "音乐", "搞笑", "电影", "明星"]

def is_on_topic(title, keyword=""):
    text = f"{title} {keyword}".lower()
    if any(m in text for m in OFF_MARKERS):
        return False
    matches = sum(1 for kw in TOPIC_KW if kw in text)
    return matches >= 1

# Filter and sort
on_topic = [c for c in candidates if is_on_topic(c['title'], c['keyword'])]
on_topic.sort(key=lambda x: x['perf_score'], reverse=True)

# Exclude already qualified
pending = [c for c in on_topic if c['cid'] not in qualified_cids]

print(f"=== BATCH 002 CONTINUATION ===")
print(f"Total ON_TOPIC: {len(on_topic)}")
print(f"Already qualified: {len(qualified_cids)}")
print(f"Pending: {len(pending)}")
print()

# Get existing audio CIDs
existing_audio = set(p.stem.replace('.audio', '') for p in MEDIA_DIR.glob('*.m4a') 
                     if not any(x in p.name for x in ['76827', '76828', '76832']))

# Get existing transcripts
existing_transcripts = set(p.stem.replace('_raw', '') for p in TRANSCRIPT_DIR.glob('*_raw.json'))

# Process next 10 candidates
target_count = 30 - len(qualified_cids)
process_count = min(15, target_count + 5)  # Process extra to account for failures

results = []
for i, c in enumerate(pending[:process_count], 1):
    cid = c['cid']
    
    if cid in existing_audio:
        print(f"[{i}] {cid} - SKIP (already processed)")
        continue
    
    print(f"\n[{i}] {cid}")
    print(f"  {c['title'][:50]}")
    
    # Get page URLs
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    context = browser.contexts[0]
    page = context.new_page()
    
    try:
        url = f'https://www.douyin.com/video/{cid}'
        page.goto(url, timeout=20000)
        time.sleep(2)
        
        content = page.content()
        blocked = any(x in content for x in ['安全验证', '登录', '二维码'])
        
        if blocked:
            print(f"  ✗ BLOCKED")
            results.append({'cid': cid, 'status': 'BLOCKED'})
            continue
        
        perf = page.evaluate('''() => {
            const entries = performance.getEntriesByType('resource');
            return entries.filter(e => e.name.includes('douyinvod'))
                .map(e => e.name.substring(0, 500));
        }''')
        
        video_url = next((u for u in perf if 'media-video' in u), None)
        audio_url = next((u for u in perf if 'media-audio' in u), None)
        
        if not audio_url:
            print(f"  ✗ No audio URL")
            results.append({'cid': cid, 'status': 'NO_AUDIO'})
            continue
        
        print(f"  ✓ Found audio URL")
        
        # Download audio
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        save_path = MEDIA_DIR / f'{cid}.audio.m4a'
        req = urllib.request.Request(audio_url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://www.douyin.com/',
            'Origin': 'https://www.douyin.com'
        })
        
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
                data = resp.read()
                save_path.write_bytes(data)
            print(f"  ✓ Downloaded: {len(data)/1024:.0f} KB")
            results.append({'cid': cid, 'status': 'DOWNLOADED', 'audio_url': audio_url})
        except Exception as e:
            print(f"  ✗ Download failed: {e}")
            results.append({'cid': cid, 'status': 'DOWNLOAD_FAILED'})
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        results.append({'cid': cid, 'status': f'ERROR'})
    finally:
        try: page.close()
        except: pass
        try: browser.close()
        except: pass
        try: p.stop()
        except: pass
    
    time.sleep(random.uniform(1, 2))

# Summary
downloaded = len([r for r in results if r.get('status') == 'DOWNLOADED'])
print(f"\n{'='*50}")
print(f"Downloaded: {downloaded}/{len(results)}")
print(f"Saved to: {SHARDS / 'batch002_download_results.json'}")

output = SHARDS / "batch002_download_results.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))