#!/usr/bin/env python3
"""RC6F: Repair corpus by collecting truly new samples"""
import json
import csv
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
import urllib.request

BASE = Path(r"F:\workspace\AI_Media_Matrix")
CORPUS = BASE / "01_benchmark/plain_language_corpus_v1"
MEDIA_DIR = BASE / "01_benchmark/media/plain_language_v1"
RAW_POOL = BASE / "01_benchmark/shards/hermes_real/douyin_raw/raw_pool_all.jsonl"

# Create directories
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Load global registry with canonical normalization
registry = set()
registry_file = BASE / "01_benchmark/GLOBAL_CONTENT_ID_REGISTRY.csv"
if registry_file.exists():
    with open(registry_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row.get('content_id', '')
            if cid:
                canonical = cid.replace('DY_REAL_', '').strip()
                if canonical and canonical.isdigit():
                    registry.add(canonical)

print(f"Registry entries: {len(registry)}")

# Load existing corpus IDs to avoid
existing_ids = set()
for p in CORPUS.glob("SAMPLE_*/*/01_metadata.json"):
    try:
        with open(p, 'r', encoding='utf-8') as f:
            meta = json.load(f)
            cid = str(meta.get('content_id', ''))
            canonical = cid.replace('DY_REAL_', '').strip()
            if canonical:
                existing_ids.add(canonical)
    except:
        pass

print(f"Existing corpus IDs: {len(existing_ids)}")

# Load raw pool and filter
candidates = []
if RAW_POOL.exists():
    with open(RAW_POOL, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    cand = json.loads(line)
                    aweme_id = str(cand.get('aweme_id', ''))
                    canonical = aweme_id.replace('DY_REAL_', '').strip()
                    
                    # Skip if in registry or existing corpus
                    if canonical in registry or canonical in existing_ids:
                        continue
                    
                    # Check engagement
                    liked = int(cand.get('liked_count', 0))
                    if liked < 5000:
                        continue
                    
                    candidates.append(cand)
                except:
                    pass

print(f"New candidates (not in registry): {len(candidates)}")

# Sort by engagement
candidates.sort(key=lambda c: int(c.get('liked_count', 0)) + int(c.get('comment_count', 0)) * 2, reverse=True)

# Select top 30
selected = candidates[:30]
print(f"Selected for collection: {len(selected)}")

# Collect samples
collected = 0
for i, cand in enumerate(selected, 1):
    sample_id = f"RC6F_{i:03d}"
    content_id = str(cand.get('aweme_id', ''))
    sample_dir = CORPUS / sample_id
    
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[{i}/30] Processing {content_id}...")
    
    # Download audio
    audio_src = cand.get('music_download_url', '')
    audio_dst = sample_dir / "audio.m4a"
    
    if audio_src:
        try:
            req = urllib.request.Request(audio_src, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                with open(audio_dst, 'wb') as f:
                    import shutil
                    shutil.copyfileobj(response, f)
            print(f"  Audio downloaded: {audio_dst.stat().st_size} bytes")
        except Exception as e:
            print(f"  Download failed: {e}")
            continue
    else:
        print(f"  No audio URL")
        continue
    
    # Get duration
    duration = None
    if audio_dst.exists():
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_dst)],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            try:
                duration = float(result.stdout.strip())
            except:
                pass
    
    # Create metadata
    metadata = {
        "sample_id": sample_id,
        "content_id": content_id,
        "canonical_content_id": content_id.replace('DY_REAL_', '').strip(),
        "platform": "douyin",
        "title": (cand.get('title', '') or '')[:200],
        "author": cand.get('nickname', ''),
        "url": cand.get('aweme_url', ''),
        "duration_sec": duration,
        "likes": int(cand.get('liked_count', 0)),
        "comments": int(cand.get('comment_count', 0)),
        "favorites": int(cand.get('collected_count', 0)),
        "shares": int(cand.get('share_count', 0)),
        "source_keyword": cand.get('source_keyword', ''),
        "capture_time": cand.get('capture_time', datetime.now().isoformat()),
        "transcript_chars": 0,
        "transcript_usable": False,
        "first30s_available": False,
        "duplicate_status": "NEW",
        "source_url_or_source_key": cand.get('aweme_url', ''),
        "created_at": datetime.now().isoformat()
    }
    
    (sample_dir / "01_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
    
    # Create performance
    performance = {
        "likes": metadata['likes'],
        "comments": metadata['comments'],
        "favorites": metadata['favorites'],
        "shares": metadata['shares'],
        "engagement_score": metadata['likes'] + metadata['comments'] * 2 + metadata['shares'] * 3,
        "source": "MEDIACRAWLER_REAL_CDP"
    }
    (sample_dir / "02_performance.json").write_text(
        json.dumps(performance, ensure_ascii=False, indent=2), encoding='utf-8')
    
    # Create placeholder transcript
    transcript = {
        "status": "PENDING_ASR",
        "note": "ASR to be run after collection",
        "segments": [],
        "transcript_chars": 0
    }
    (sample_dir / "03_transcript_raw.json").write_text(
        json.dumps(transcript, ensure_ascii=False, indent=2), encoding='utf-8')
    
    (sample_dir / "04_transcript_raw.md").write_text(
        f"# Transcript: {metadata['title']}\n\n**Status**: Pending ASR\n", encoding='utf-8')
    
    evidence = {
        "sample_id": sample_id,
        "content_id": content_id,
        "files": ["01_metadata.json", "02_performance.json", "03_transcript_raw.json", 
                  "04_transcript_raw.md", "audio.m4a" if audio_dst.exists() else None],
        "collected_at": datetime.now().isoformat()
    }
    evidence['files'] = [f for f in evidence['files'] if f]
    (sample_dir / "06_evidence_manifest.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf-8')
    
    collected += 1
    print(f"  Collected: duration={duration}")

print(f"\n=== Collection Summary ===")
print(f"Collected: {collected}/30")
print(f"Corpus directory: {CORPUS}")