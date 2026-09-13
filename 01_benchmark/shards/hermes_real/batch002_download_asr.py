#!/usr/bin/env python3
"""Batch 002 - Download + ASR Pipeline"""
import json
import time
import subprocess
import hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
import urllib.request
import ssl

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
MEDIA_DIR = BASE / "media" / "batch_002_smoke"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"

MEDIA_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

# Load candidates
candidates_path = SHARDS / "batch002_candidates_final.json"
with open(candidates_path, 'r', encoding='utf-8') as f:
    candidates = json.load(f)

print(f"=== BATCH 002 PRODUCTION ===")
print(f"Candidates: {len(candidates)}")
print(f"Target: 30 qualified\n")

def download_cdn_url(url, save_path):
    """Download from CDN URL with auth headers"""
    if save_path.exists() and save_path.stat().st_size > 1000:
        return True
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://www.douyin.com/',
        'Origin': 'https://www.douyin.com'
    })
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            data = resp.read()
            save_path.write_bytes(data)
            return True
    except Exception as e:
        print(f"    Download failed: {e}")
        return False

def get_page_urls(cid):
    """Get video/audio URLs from page via CDP"""
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    context = browser.contexts[0]
    page = context.new_page()
    
    try:
        url = f'https://www.douyin.com/video/{cid}'
        page.goto(url, timeout=20000)
        time.sleep(3)
        
        content = page.content()
        if any(x in content for x in ['安全验证', '登录', '二维码']):
            return None, None, 'BLOCKED'
        
        perf = page.evaluate('''() => {
            const entries = performance.getEntriesByType('resource');
            return entries.filter(e => e.name.includes('douyinvod'))
                .map(e => e.name.substring(0, 600));
        }''')
        
        video_url = next((u for u in perf if 'media-video' in u), None)
        audio_url = next((u for u in perf if 'media-audio' in u), None)
        
        return video_url, audio_url, 'OK'
        
    except Exception as e:
        return None, None, str(e)
    finally:
        try: page.close()
        except: pass
        try: browser.close()
        except: pass
        try: p.stop()
        except: pass

def run_asr(audio_path, output_json):
    """Run faster-whisper ASR"""
    if output_json.exists():
        return json.loads(output_json.read_text(encoding='utf-8'))
    
    # Use existing script
    asr_script = SHARDS / "asr_rc3.py"
    if not asr_script.exists():
        return None
    
    try:
        result = subprocess.run(
            ['python', str(asr_script), str(audio_path), str(output_json)],
            capture_output=True, text=True, timeout=300
        )
        if output_json.exists():
            return json.loads(output_json.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"    ASR error: {e}")
    
    return None

def sha256_file(filepath):
    """Calculate SHA256"""
    h = hashlib.sha256()
    if filepath.exists():
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
    return h.hexdigest()

# Process candidates
results = []
processed = 0

for i, c in enumerate(candidates[:30], 1):
    cid = c['cid']
    print(f"\n[{i}/30] {cid}")
    print(f"  {c['title'][:50]}")
    
    result = {
        'cid': cid,
        'title': c['title'],
        'primary_topic': c.get('primary_topic', 'UNKNOWN'),
        'page_status': 'PENDING',
        'video_url': None,
        'audio_url': None,
        'video_path': None,
        'audio_path': None,
        'asr_ready': False,
        'segments': 0,
        'chars': 0,
        'qualified': False
    }
    
    # Get URLs
    video_url, audio_url, status = get_page_urls(cid)
    result['page_status'] = status
    result['video_url'] = video_url
    result['audio_url'] = audio_url
    
    if status != 'OK':
        print(f"  ✗ {status}")
        results.append(result)
        continue
    
    print(f"  ✓ Video: {bool(video_url)}, Audio: {bool(audio_url)}")
    
    # Download audio if available
    if audio_url:
        audio_path = MEDIA_DIR / f"{cid}.audio.m4a"
        print(f"  Downloading audio...")
        if download_cdn_url(audio_url, audio_path):
            result['audio_path'] = str(audio_path)
            print(f"  ✓ Audio downloaded: {audio_path.stat().st_size / 1024 / 1024:.1f} MB")
        else:
            print(f"  ✗ Audio download failed")
    
    processed += 1
    time.sleep(1)

# Summary
print(f"\n{'='*60}")
print(f"PROCESSED: {processed}/30")
print(f"Results saved to: {SHARDS / 'batch002_production_results.json'}")

output = SHARDS / "batch002_production_results.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))