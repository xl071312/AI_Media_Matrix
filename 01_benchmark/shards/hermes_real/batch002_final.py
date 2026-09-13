#!/usr/bin/env python3
"""Batch 002 - Final Production: Download + ASR to reach 30"""
import csv
import json
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright
import urllib.request
import ssl
from faster_whisper import WhisperModel
import subprocess

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
MEDIA_DIR = BASE / "media" / "batch_002_smoke"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"

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

# Load qualified CIDs
qa_path = SHARDS / "batch002_all_qa.json"
qualified_cids = set()
if qa_path.exists():
    with open(qa_path, 'r', encoding='utf-8') as f:
        qa_data = json.load(f)
    for r in qa_data:
        if r.get('corpus_eligible'):
            qualified_cids.add(r['content_id'])

print(f"=== BATCH 002 FINAL PRODUCTION ===")
print(f"Qualified so far: {len(qualified_cids)}")
print(f"Need: 30")
print(f"Still need: {max(0, 30 - len(qualified_cids))}")
print()

# Get existing processed CIDs
existing_audio = set(p.stem.replace('.audio', '') for p in MEDIA_DIR.glob('*.m4a') 
                     if not any(x in p.name for x in ['76827', '76828', '76832']))
existing_transcripts = set(p.stem.replace('_raw', '') for p in TRANSCRIPT_DIR.glob('*_raw.json'))

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

# Filter pending
pending = [c for c in candidates if c['cid'] not in qualified_cids and is_on_topic(c['title'], c['keyword'])]
pending.sort(key=lambda x: x['perf_score'], reverse=True)

print(f"ON_TOPIC pending: {len(pending)}")
print()

# Load model once
model = WhisperModel('Systran/faster-whisper-tiny', device='cpu', compute_type='int8')
print("Model loaded\n")

results = []
processed = 0

for i, c in enumerate(pending[:20], 1):  # Process up to 20 more
    cid = c['cid']
    
    if cid in existing_transcripts:
        continue
    
    print(f"[{i}] {cid}")
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
        except Exception as e:
            print(f"  ✗ Download failed: {e}")
            results.append({'cid': cid, 'status': 'DOWNLOAD_FAILED'})
            continue
        
        # Run ASR
        transcript_path = TRANSCRIPT_DIR / f'{cid}_raw.json'
        
        # Get duration
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                 '-of', 'default=noprint_wrappers=1:nokey=1', str(save_path)],
                capture_output=True, text=True, timeout=10
            )
            duration = float(result.stdout.strip())
        except:
            duration = 0
        
        print(f"  Duration: {duration:.1f}s")
        
        # Chunk processing
        chunk_length = 240
        all_segments = []
        
        for start_time in range(0, int(duration), chunk_length):
            try:
                segs, info = model.transcribe(str(save_path), beam_size=1, language='zh', 
                                              vad_filter=True, offset=start_time, duration=chunk_length)
                local_segs = list(segs)
                for s in local_segs:
                    s.start += start_time
                    s.end += start_time
                all_segments.extend(local_segs)
            except Exception as e:
                print(f"    Chunk at {start_time}s failed: {e}")
        
        # Save
        transcript = [{'start': round(s.start, 2), 'end': round(s.end, 2), 'text': s.text.strip()} for s in all_segments]
        transcript_path.write_text(json.dumps(transcript, ensure_ascii=False, indent=2), encoding='utf-8')
        
        chars = sum(len(s['text']) for s in transcript)
        print(f"  ✓ ASR: {len(all_segments)} segs, {chars} chars")
        results.append({'cid': cid, 'status': 'DONE', 'segments': len(all_segments), 'chars': chars})
        
        processed += 1
        
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
done = len([r for r in results if r.get('status') == 'DONE'])
print(f"\n{'='*50}")
print(f"New processed: {done}")
print(f"Total qualified now: {len(qualified_cids) + done}")
print(f"Target: 30")

# Save
output = SHARDS / "batch002_final_results.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))