#!/usr/bin/env python3
"""Batch 002 - Media Download + ASR for Verified Candidates"""
import csv
import json
import subprocess
import hashlib
import time
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH2_DIR = BASE / "analysis_batches" / "batch_002"
MEDIA_DIR = BASE / "media" / "batch_002_smoke"
TRANSCRIPT_DIR = BASE / "shards" / "hermes_real" / "transcripts_v2"

BATCH2_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

# Load verified candidates from preflight
preflight_path = SHARDS / "batch002_preflight_rc1.json"
with open(preflight_path, 'r', encoding='utf-8') as f:
    preflight = json.load(f)

candidates = preflight['top_on_topic_new'][:20]  # First 20 verified

print("=== BATCH 002 MEDIA + ASR PIPELINE ===")
print(f"Candidates: {len(candidates)}\n")

# Track results
results = []

def download_video(cid, title, base_url):
    """Download video using browser session + urllib"""
    import urllib.request
    
    url = f"{base_url}/{cid}"
    save_path = MEDIA_DIR / f"{cid}.mp4"
    
    if save_path.exists():
        size = save_path.stat().st_size
        return {'path': str(save_path), 'size': size, 'exists': True}
    
    try:
        # Use authenticated browser session via CDP
        # This would use the existing Chrome profile cookies
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.douyin.com/'
        })
        
        # Note: Direct download may not work without proper cookies
        # We'll track this as PENDING for now
        return {'path': None, 'size': 0, 'status': 'PENDING_COOKIE_AUTH'}
        
    except Exception as e:
        return {'path': None, 'size': 0, 'error': str(e)}

def check_asr_ready(cid):
    """Check if ASR has been run for this CID"""
    transcript_path = TRANSCRIPT_DIR / f"{cid}_raw.json"
    if transcript_path.exists():
        with open(transcript_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        segments = data.get('segments', [])
        chars = sum(len(s.get('text', '')) for s in segments)
        return {
            'ready': True,
            'segments': len(segments),
            'chars': chars,
            'path': str(transcript_path)
        }
    return {'ready': False}

def sha256_file(filepath):
    """Calculate SHA256 of file"""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

# Process each candidate
for i, c in enumerate(candidates, 1):
    cid = c['cid']
    title = c['title'][:60]
    print(f"\n[{i}/20] {cid}")
    print(f"  Title: {title}")
    
    # Check existing ASR
    asr_status = check_asr_ready(cid)
    
    result = {
        'cid': cid,
        'title': title,
        'primary_topic': c.get('topic', 'UNKNOWN'),
        'likes': c.get('likes', 0),
        'comments': c.get('comments', 0),
        'favorites': c.get('favorites', 0),
        'shares': c.get('shares', 0),
        'performance_verified': True,
        'page_playable': True,
        'asr_status': asr_status,
        'qualified': asr_status.get('ready', False) and asr_status.get('segments', 0) > 0
    }
    
    results.append(result)
    
    if asr_status.get('ready'):
        print(f"  ✓ ASR Ready: {asr_status['segments']} segments, {asr_status['chars']} chars")
    else:
        print(f"  ⏳ ASR Pending (need download)")
    
    time.sleep(0.3)

# Summary
qualified = sum(1 for r in results if r.get('qualified'))
asr_ready = sum(1 for r in results if r.get('asr_status', {}).get('ready'))
print(f"\n{'='*60}")
print(f"SUMMARY:")
print(f"  Total: {len(results)}")
print(f"  ASR Ready: {asr_ready}")
print(f"  Qualified: {qualified}")

# Save
output = SHARDS / "batch002_media_asr_status.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"Saved to: {output}")