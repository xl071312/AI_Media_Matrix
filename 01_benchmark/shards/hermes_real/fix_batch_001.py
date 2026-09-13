#!/usr/bin/env python3
"""Fix metadata and run ASR for Batch 001 - CORRECTED"""
import json
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
OUTPUT_DIR = BASE / "analysis_batches" / "batch_001"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")

# Load metadata
with open(SHARDS / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    selection = {row.get('aweme_id'): row for row in reader}

# Check existing samples
print("=== CURRENT SAMPLES ===")
samples = sorted(OUTPUT_DIR.glob("sample_*"))
for s in samples:
    meta_file = s / "01_metadata.json"
    if meta_file.exists():
        with open(meta_file) as f:
            meta = json.load(f)
        print(f"{s.name}: {meta.get('content_id', '?')}")

# Fix Sample 003
print("\n=== FIXING SAMPLE 003 ===")
sample_003_dir = OUTPUT_DIR / "sample_003"
cid_003 = "7302348364815928612"

meta_file = sample_003_dir / "01_metadata.json"
if meta_file.exists():
    with open(meta_file) as f:
        meta = json.load(f)
    
    # Check if we can find this ID anywhere
    found = False
    for cid, row in selection.items():
        if cid == cid_003:
            found = True
            print(f"  Found in selection")
            
            if meta.get('title') == 'TBD':
                meta['title'] = row.get('desc', '')[:150]
            if meta.get('creator_name') == 'TBD':
                meta['creator_name'] = row.get('nickname', '')
                meta['creator_id'] = row.get('nickname', '')
            if meta.get('topic') == 'TBD':
                meta['topic'] = row.get('source_keyword', '')
            if meta.get('viral_type') == 'UNKNOWN':
                viral_raw = row.get('viral_type', '')
                meta['viral_type'] = viral_raw.split(';')[0] if ';' in viral_raw else viral_raw
            if meta.get('sample_role') == 'EXTERNAL_DATA':
                meta['sample_role'] = row.get('sample_role', '')
            meta['metadata_source'] = 'MEDIACRAWLER_REAL_CDP'
            
            meta_file.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
            print(f"  Fixed metadata")
            break
    
    if not found:
        print(f"  Not found in selection - marking as EXTERNAL_DATA")
        meta['sample_role'] = 'EXTERNAL_DATA'
        meta['metadata_source'] = 'EXTERNAL'
        meta_file.write_text(json.dumps(meta, indent=2, ensure_ascii=False))

# Fix Sample 002 role
print("\n=== CHECKING SAMPLE 002 ROLE ===")
sample_002_dir = OUTPUT_DIR / "sample_002"
meta_file = sample_002_dir / "01_metadata.json"

if meta_file.exists():
    with open(meta_file) as f:
        meta = json.load(f)
    
    baseline_file = sample_002_dir / "03_creator_baseline.json"
    has_baseline = False
    if baseline_file.exists():
        with open(baseline_file) as f:
            baseline = json.load(f)
        has_baseline = baseline.get('status') == 'COLLECTED'
    
    current_role = meta.get('sample_role', '')
    print(f"  Current role: {current_role}")
    print(f"  Has baseline: {has_baseline}")
    
    if 'RELATIVE_BREAKOUT' in current_role and 'CANDIDATE' not in current_role and not has_baseline:
        meta['sample_role'] = 'RELATIVE_BREAKOUT_CANDIDATE'
        meta['role_note'] = 'Baseline not available - downgraded to CANDIDATE'
        meta_file.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
        print(f"  Changed to: {meta['sample_role']}")
else:
    print(f"  sample_002 metadata not found")

# Run ASR
print("\n=== RUNNING ASR ===")
existing_ids = set()
for s in samples:
    meta_file = s / "01_metadata.json"
    if meta_file.exists():
        with open(meta_file) as f:
            meta = json.load(f)
        existing_ids.add(meta.get('content_id', ''))

print(f"Existing: {len(existing_ids)}")

# Find videos needing ASR
videos_to_process = []
for d in sorted(VIDEO_DIR.glob("*/")):
    cid = d.name
    if cid in existing_ids:
        continue
    
    video_path = d / "video.mp4"
    trans_file = TRANSCRIPT_DIR / f"{cid}_raw.json"
    
    if video_path.exists() and not trans_file.exists():
        row = selection.get(cid)
        videos_to_process.append({
            'id': cid,
            'path': video_path,
            'row': row,
            'from_selection': cid in selection
        })

print(f"Videos to process: {len(videos_to_process)}")

# Process first 3
for i, item in enumerate(videos_to_process[:3], 1):
    cid = item['id']
    video_path = item['path']
    
    print(f"\n--- ASR {i}/3: {cid} ---")
    
    try:
        from faster_whisper import WhisperModel
        
        model = WhisperModel("Systran/faster-whisper-base", device="cpu", compute_type="int8")
        segments, info = model.transcribe(str(video_path), beam_size=5, language="zh")
        
        transcript = []
        for seg in segments:
            transcript.append({
                "start": seg.start,
                "end": seg.end,
                "text": seg.text.strip()
            })
        
        # Save transcript
        output_file = TRANSCRIPT_DIR / f"{cid}_raw.json"
        output_file.write_text(json.dumps(transcript, ensure_ascii=False, indent=2))
        
        print(f"  ✓ Transcribed {len(transcript)} segments")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")

# Final count
print("\n=== FINAL STATUS ===")
final_samples = sorted(OUTPUT_DIR.glob("sample_*"))
print(f"Total samples: {len(final_samples)}")
