#!/usr/bin/env python3
"""Batch 003 - Start Production with Different Topic Focus"""
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
BATCH3_DIR = BASE / "analysis_batches" / "batch_003"
MEDIA_DIR = BASE / "media" / "batch_003_smoke"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"

# Create dirs
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
BATCH3_DIR.mkdir(parents=True, exist_ok=True)

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

# Batch002 qualified CIDs to exclude
b002_path = SHARDS / "batch002_final_qa.json"
b002_cids = set()
if b002_path.exists():
    with open(b002_path, 'r', encoding='utf-8') as f:
        b002_data = json.load(f)
    for r in b002_data:
        if r.get('corpus_eligible'):
            b002_cids.add(r['content_id'])

print(f"=== BATCH 003 PRODUCTION ===")
print(f"Registry size: {len(registry)}")
print(f"Batch002 CIDs: {len(b002_cids)}")
print()

# Topic keywords for Batch003 focus
# Prioritize: 能力变现, 普通人收入, 职场收入, 信息差, AI赚钱, 商业思维, 创业失败, 消费认知
PRIORITY_TOPICS = {
    '能力变现': ['变现', '副业', '技能', '个人成长', '时间管理'],
    '普通人收入': ['收入', '工资', '月薪', '年薪', '普通人', '翻身', '逆袭'],
    '职场收入': ['职场', '打工', '升职', '加薪', '跳槽', '面试'],
    '信息差': ['信息差', '认知', '思维', '知识', '茧房', '差距'],
    'AI赚钱': ['AI', '人工智能', '豆包', 'ChatGPT', '大模型'],
    '商业思维': ['商业', '生意', '模式', '盈利', '赛道'],
    '创业失败': ['失败', '踩坑', '避坑', '教训', '反思'],
    '消费认知': ['消费观', '理性消费', '省钱', '存钱', '财务自由'],
}
OFF_MARKERS = ['游戏', '攻略', '三角洲', '原神', '动漫', '短剧', '美食', '健身', 
               '宠物', '旅游', '美妆', '穿搭', '数码', '汽车', '音乐', '搞笑', '电影', '明星']

def classify_batch003_priority(title, keyword=""):
    text = f"{title} {keyword}".lower()
    for m in OFF_MARKERS:
        if m in text:
            return None, 0  # OFF_TOPIC
    
    max_priority = 0
    best_topic = None
    for topic, keywords in PRIORITY_TOPICS.items():
        match_count = sum(1 for kw in keywords if kw in text)
        if match_count > max_priority:
            max_priority = match_count
            best_topic = topic
    
    return best_topic, max_priority

# Filter and rank candidates
priority_candidates = []
for c in candidates:
    if c['cid'] in b002_cids:
        continue
    
    topic, priority = classify_batch003_priority(c['title'], c['keyword'])
    if topic and priority > 0:
        priority_candidates.append({**c, 'topic': topic, 'priority': priority})

# Sort by priority (higher priority topics first), then by performance
priority_candidates.sort(key=lambda x: (-x['priority'], -x['perf_score']))

print(f"Priority candidates: {len(priority_candidates)}")
print()

# Load ASR model
model = WhisperModel('Systran/faster-whisper-tiny', device='cpu', compute_type='int8')
print("Model loaded\n")

results = []
qualified_count = 0

for i, c in enumerate(priority_candidates[:25], 1):
    cid = c['cid']
    
    if cid in registry:
        continue
    
    print(f"[{i}] {cid} - {c['topic']} (priority={c['priority']})")
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
        
        # Transcribe
        try:
            segs, info = model.transcribe(str(save_path), beam_size=1, language='zh', vad_filter=True)
            all_segs = list(segs)
            
            # Save
            transcript = [{'start': round(s.start, 2), 'end': round(s.end, 2), 'text': s.text.strip()} for s in all_segs]
            transcript_path.write_text(json.dumps(transcript, ensure_ascii=False, indent=2), encoding='utf-8')
            
            chars = sum(len(s['text']) for s in transcript)
            print(f"  ✓ ASR: {len(all_segs)} segs, {chars} chars")
            results.append({'cid': cid, 'status': 'DONE', 'topic': c['topic'], 'segments': len(all_segs), 'chars': chars})
            qualified_count += 1
            
        except Exception as e:
            print(f"  ✗ ASR error: {e}")
            results.append({'cid': cid, 'status': f'ASR_ERROR'})
        
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
print(f"BATCH 003 RESULTS:")
print(f"  Processed: {len(results)}")
print(f"  Qualified: {done}")
print(f"  Saved to: {SHARDS / 'batch003_initial_results.json'}")

output = SHARDS / "batch003_initial_results.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
