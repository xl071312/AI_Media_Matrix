#!/usr/bin/env python3
"""Batch 003 - Continue production (parallel with Batch002 V2)"""
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

MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Load registry
reg_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
registry = set()
with open(reg_path, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        cid = row.get('content_id', '').strip().lstrip('\ufeff')
        if cid:
            registry.add(cid)

# Load existing progress
existing_path = SHARDS / "batch003_progress.json"
existing_results = {}
if existing_path.exists():
    with open(existing_path, 'r', encoding='utf-8') as f:
        existing_results = json.load(f)
done_cids = set(r['cid'] for r in existing_results if r.get('status') == 'DONE')

print(f"=== BATCH 003 CONTINUATION ===")
print(f"Registry size: {len(registry)}")
print(f"Already done: {len(done_cids)}")
print()

# Load selection - get candidates NOT in registry and NOT done
sel_path = SHARDS / "douyin_benchmark_selection.csv"
candidates = []
with open(sel_path, 'r', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        raw_cid = row.get('content_id', row.get('aweme_id', '')).strip().lstrip('\ufeff')
        if raw_cid.startswith('DY_REAL_'):
            raw_cid = raw_cid[8:]
        raw_cid = raw_cid.strip()
        if raw_cid in registry or raw_cid in done_cids:
            continue
        candidates.append({
            'cid': raw_cid,
            'title': row.get('desc', '')[:100],
            'keyword': row.get('source_keyword', ''),
            'perf_score': float(row.get('performance_score', 0)),
        })

print(f"New candidates: {len(candidates)}")
print()

# Load model
model = WhisperModel('Systran/faster-whisper-tiny', device='cpu', compute_type='int8')
print("Model loaded\n")

results = list(existing_results)
processed = 0

for i, c in enumerate(candidates[:15], 1):  # Process 15 more
    cid = c['cid']
    
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
        time.sleep(3)
        
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
            results.append({'cid': cid, 'status': 'DONE', 'segments': len(all_segs), 'chars': chars})
            
            # Update registry
            registry.add(cid)
            
        except Exception as e:
            print(f"  ✗ ASR error: {e}")
            results.append({'cid': cid, 'status': f'ASR_ERROR'})
        
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
    
    time.sleep(random.uniform(2, 4))
    
    # Save progress
    if processed % 3 == 0:
        output = SHARDS / "batch003_progress.json"
        output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"  Progress saved ({len(results)} total)")

# Summary
done = len([r for r in results if r.get('status') == 'DONE'])
blocked = len([r for r in results if r.get('status') == 'BLOCKED'])
no_audio = len([r for r in results if r.get('status') == 'NO_AUDIO'])

print(f"\n{'='*50}")
print(f"BATCH 003 RESULTS:")
print(f"  Total: {len(results)}")
print(f"  DONE: {done}")
print(f"  BLOCKED: {blocked}")
print(f"  NO_AUDIO: {no_audio}")

output = SHARDS / "batch003_progress.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"Saved to: {output}")