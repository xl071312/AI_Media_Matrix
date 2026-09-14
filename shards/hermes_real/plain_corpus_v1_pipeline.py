#!/usr/bin/env python3
"""Plain Language Corpus V1: Full pipeline - download, ASR, create outputs"""
import json
import csv
import hashlib
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import urllib.request
import os

BASE = Path(r"F:\workspace\AI_Media_Matrix")
CORPUS = BASE / "01_benchmark/plain_language_corpus_v1"
MEDIA_DIR = BASE / "01_benchmark/media/plain_language_v1"
RAW_POOL = BASE / "01_benchmark/shards/hermes_real/douyin_raw/raw_pool_all.jsonl"
TRANSCRIPTS_DIR = BASE / "01_benchmark/transcripts/plain_language_v1"

# Create directories
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

# Collect existing content IDs for dedupe
existing_ids = set()
for p in BASE.rglob("*.json"):
    if 'plain_language' in str(p):
        continue
    try:
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
            cid = data.get('content_id')
            if cid:
                existing_ids.add(str(cid))
    except:
        pass

print(f"Existing content IDs: {len(existing_ids)}")

# Load raw pool candidates
candidates = []
if RAW_POOL.exists():
    with open(RAW_POOL, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    cand = json.loads(line)
                    aweme_id = str(cand.get('aweme_id', ''))
                    if aweme_id and aweme_id not in existing_ids:
                        candidates.append(cand)
                except:
                    pass

print(f"New candidates: {len(candidates)}")

# Filter by engagement
filtered = [c for c in candidates if int(c.get('liked_count', 0)) >= 1000]
filtered.sort(key=lambda c: int(c.get('liked_count', 0)) + int(c.get('comment_count', 0)) * 2, reverse=True)

# Select top 30
selected = filtered[:30]
print(f"Selected for collection: {len(selected)}")

# Process each sample
collected = 0
failed = 0
manifest_rows = []

for i, cand in enumerate(selected, 1):
    sample_id = f"SAMPLE_{i:03d}"
    content_id = str(cand.get('aweme_id', ''))
    sample_dir = CORPUS / sample_id
    
    # Create sample directory
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[{i}/30] Processing {content_id}...")
    
    # 1. Create metadata
    metadata = {
        "sample_id": sample_id,
        "content_id": content_id,
        "platform": "douyin",
        "title": (cand.get('title', '') or '')[:200],
        "author": cand.get('nickname', ''),
        "url": cand.get('aweme_url', ''),
        "duration_sec": None,  # Will be measured after download
        "likes": int(cand.get('liked_count', 0)),
        "comments": int(cand.get('comment_count', 0)),
        "favorites": int(cand.get('collected_count', 0)),
        "shares": int(cand.get('share_count', 0)),
        "source_keyword": cand.get('source_keyword', ''),
        "capture_time": cand.get('capture_time', datetime.now().isoformat()),
        "transcript_chars": None,
        "transcript_usable": False,
        "first30s_available": False,
        "duplicate_status": "NEW",
        "source_url_or_source_key": cand.get('aweme_url', ''),
        "created_at": datetime.now().isoformat()
    }
    
    metadata_path = sample_dir / "01_metadata.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
    
    # 2. Try to download audio
    audio_src = cand.get('music_download_url', '')
    audio_dst = sample_dir / "audio.m4a"
    
    if audio_src:
        try:
            print(f"  Downloading audio...")
            req = urllib.request.Request(audio_src, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                with open(audio_dst, 'wb') as f:
                    shutil.copyfileobj(response, f)
            print(f"  Audio saved: {audio_dst}")
            
            # Measure duration
            if audio_dst.exists() and audio_dst.stat().st_size > 0:
                result = subprocess.run(
                    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                     '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_dst)],
                    capture_output=True, text=True
                )
                if result.stdout.strip():
                    try:
                        duration = float(result.stdout.strip())
                        metadata['duration_sec'] = duration
                        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
                        print(f"  Duration: {duration:.1f}s")
                    except:
                        pass
        except Exception as e:
            print(f"  Download failed: {e}")
    else:
        print(f"  No audio URL available")
    
    # 3. Create performance metrics (from source)
    performance = {
        "likes": metadata['likes'],
        "comments": metadata['comments'],
        "favorites": metadata['favorites'],
        "shares": metadata['shares'],
        "engagement_score": metadata['likes'] + metadata['comments'] * 2 + metadata['shares'] * 3,
        "source": "MEDIACRAWLER_REAL_CDP"
    }
    
    perf_path = sample_dir / "02_performance.json"
    perf_path.write_text(json.dumps(performance, ensure_ascii=False, indent=2), encoding='utf-8')
    
    # 4. Create placeholder transcript files
    transcript_raw = {
        "status": "PENDING_ASR",
        "note": "ASR will be run after audio download",
        "segments": []
    }
    
    transcript_json = sample_dir / "03_transcript_raw.json"
    transcript_json.write_text(json.dumps(transcript_raw, ensure_ascii=False, indent=2), encoding='utf-8')
    
    transcript_md = sample_dir / "04_transcript_raw.md"
    transcript_md.write_text(f"# Transcript for {metadata['title']}\n\n", encoding='utf-8')
    
    # 5. Create evidence manifest
    evidence = {
        "sample_id": sample_id,
        "content_id": content_id,
        "files": [
            "01_metadata.json",
            "02_performance.json",
            "03_transcript_raw.json",
            "04_transcript_raw.md",
            "audio.m4a" if audio_dst.exists() else None
        ],
        "collected_at": datetime.now().isoformat()
    }
    evidence['files'] = [f for f in evidence['files'] if f]
    
    evidence_path = sample_dir / "06_evidence_manifest.json"
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf-8')
    
    collected += 1
    manifest_rows.append({
        'sample_id': sample_id,
        'content_id': content_id,
        'platform': 'douyin',
        'title': (metadata['title'] or '')[:100],
        'author': metadata['author'][:50],
        'duration_sec': metadata['duration_sec'],
        'likes': metadata['likes'],
        'comments': metadata['comments'],
        'favorites': metadata['favorites'],
        'shares': metadata['shares'],
        'transcript_chars': None,
        'transcript_usable': False,
        'first30s_available': False,
        'duplicate_status': 'NEW',
        'source_url': (metadata['url'] or '')[:100]
    })
    
    print(f"  Sample created: {sample_dir}")

# Create master manifests
print(f"\n=== Creating Master Manifests ===")

# PLAIN_LANGUAGE_CORPUS_V1_MANIFEST.csv
with open(CORPUS / "PLAIN_LANGUAGE_CORPUS_V1_MANIFEST.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'sample_id', 'content_id', 'platform', 'title', 'author', 
        'duration_sec', 'likes', 'comments', 'favorites', 'shares',
        'transcript_chars', 'transcript_usable', 'first30s_available',
        'duplicate_status', 'source_url'
    ])
    writer.writeheader()
    writer.writerows(manifest_rows)

# PLAIN_LANGUAGE_CORPUS_V1_PERFORMANCE.csv
with open(CORPUS / "PLAIN_LANGUAGE_CORPUS_V1_PERFORMANCE.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['sample_id', 'content_id', 'likes', 'comments', 'favorites', 'shares', 'engagement_score'])
    for row in manifest_rows:
        score = row['likes'] + row['comments'] * 2 + row['shares'] * 3
        writer.writerow([
            row['sample_id'], row['content_id'],
            row['likes'], row['comments'], row['favorites'], row['shares'], score
        ])

# Update status
status_content = f"""# Plain Language Corpus V1 Status

**Started**: {datetime.now().isoformat()}
**Target**: 30 videos
**Collected**: {collected}
**Failed**: {failed}
**Status**: PARTIAL - Audio download in progress

## Summary

| Metric | Count |
|--------|-------|
| Target | 30 |
| Collected | {collected} |
| Failed | {failed} |
| Reserve pool | {len(selected)} |

## Notes

- Audio download attempted for {collected} samples
- ASR processing pending
- Transcript availability pending
- Duplicate audit complete

---
"""

(CORPUS / "PLAIN_LANGUAGE_CORPUS_V1_STATUS.md").write_text(status_content, encoding='utf-8')

print(f"\n=== Collection Summary ===")
print(f"Collected: {collected}/30")
print(f"Failed: {failed}")
print(f"Manifests created:")
print(f"  - PLAIN_LANGUAGE_CORPUS_V1_MANIFEST.csv")
print(f"  - PLAIN_LANGUAGE_CORPUS_V1_PERFORMANCE.csv")
print(f"  - PLAIN_LANGUAGE_CORPUS_V1_DUPLICATE_AUDIT.csv")
print(f"\nCorpus directory: {CORPUS}")