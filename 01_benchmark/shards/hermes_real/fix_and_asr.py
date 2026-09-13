#!/usr/bin/env python3
"""Fix metadata and run ASR for Batch 001"""
import json
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
OUTPUT_DIR = BASE / "analysis_batches" / "batch_001"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")

# Load all available metadata
with open(SHARDS / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    selection = {row.get('aweme_id'): row for row in reader}

# Also check deep_analysis_batch
with open(SHARDS / "deep_analysis_batch_001.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    deep_analysis = {row.get('aweme_id'): row for row in reader}

# Merge both sources
all_metadata = {}
for cid, row in selection.items():
    all_metadata[cid] = row
for cid, row in deep_analysis.items():
    if cid not in all_metadata:
        all_metadata[cid] = row

print(f"Loaded {len(all_metadata)} metadata entries\n")

# Fix Sample 003
print("=== FIXING SAMPLE 003 ===")
sample_003_dir = OUTPUT_DIR / "sample_003"
cid_003 = "7302348364815928612"

if cid_003 in all_metadata:
    meta_data = all_metadata[cid_003]
    print(f"  Found metadata for {cid_003}")
    
    meta_file = sample_003_dir / "01_metadata.json"
    with open(meta_file) as f:
        meta = json.load(f)
    
    # Restore real values
    if meta.get('title') == 'TBD':
        meta['title'] = meta_data.get('desc', '')[:150]
        print(f"  Restored title")
    
    if meta.get('creator_name') == 'TBD':
        meta['creator_name'] = meta_data.get('nickname', '')
        meta['creator_id'] = meta_data.get('nickname', '')
        print(f"  Restored creator: {meta_data.get('nickname', '')}")
    
    if meta.get('topic') == 'TBD':
        meta['topic'] = meta_data.get('source_keyword', '')
        print(f"  Restored topic: {meta_data.get('source_keyword', '')}")
    
    if meta.get('viral_type') == 'UNKNOWN':
        viral_raw = meta_data.get('viral_type', '')
        meta['viral_type'] = viral_raw.split(';')[0] if ';' in viral_raw else viral_raw
        print(f"  Restored viral type: {meta['viral_type']}")
    
    if meta.get('sample_role') == 'EXTERNAL_DATA':
        meta['sample_role'] = meta_data.get('sample_role', '')
        print(f"  Restored sample role: {meta['sample_role']}")
    
    meta['metadata_source'] = 'MEDIACRAWLER_REAL_CDP'
    meta_file.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    
    # Fix performance
    perf_file = sample_003_dir / "02_performance.json"
    with open(perf_file) as f:
        perf = json.load(f)
    
    likes = int(meta_data.get('liked_count', 0))
    if perf.get('likes', 0) == 0 and likes > 0:
        perf['likes'] = likes
        perf['comments'] = int(meta_data.get('comment_count', 0))
        perf['favorites'] = int(meta_data.get('collected_count', 0))
        perf['shares'] = int(meta_data.get('share_count', 0))
        perf['favorite_like_ratio'] = round(perf['favorites'] / max(perf['likes'], 1), 3)
        perf['share_like_ratio'] = round(perf['shares'] / max(perf['likes'], 1), 3)
        perf['comment_like_ratio'] = round(perf['comments'] / max(perf['likes'], 1), 3)
        perf_file.write_text(json.dumps(perf, indent=2, ensure_ascii=False))
        print(f"  Restored performance: {likes:,} likes")
    
    print(f"  ✓ Sample 003 fixed")
else:
    print(f"  ✗ Metadata not found for {cid_003}")

# Fix Sample 002 role
print("\n=== CHECKING SAMPLE 002 ROLE ===")
sample_002_dir = OUTPUT_DIR / "sample_002"
cid_002 = "7647797848847439706"

meta_file = sample_002_dir / "01_metadata.json"
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
    print(f"  Role OK")

# Run ASR on new videos
print("\n=== RUNNING ASR ON NEW VIDEOS ===")

# Get existing content IDs
existing_ids = set()
for s in OUTPUT_DIR.glob("sample_*"):
    meta = json.load(open(s / "01_metadata.json"))
    existing_ids.add(meta.get('content_id', ''))

print(f"Existing samples: {len(existing_ids)}")

# Find videos needing ASR
videos_to_process = []
for d in sorted(VIDEO_DIR.glob("*/")):
    cid = d.name
    if cid in existing_ids:
        continue
    
    video_path = d / "video.mp4"
    trans_file = TRANSCRIPT_DIR / f"{cid}_raw.json"
    
    if video_path.exists() and not trans_file.exists():
        videos_to_process.append({
            'id': cid,
            'path': video_path,
            'row': all_metadata.get(cid),
            'from_selection': cid in all_metadata
        })

print(f"Videos needing ASR: {len(videos_to_process)}")

# Process first 5
for i, item in enumerate(videos_to_process[:5], 1):
    cid = item['id']
    video_path = item['path']
    
    print(f"\n--- ASR {i}/5: {cid} ---")
    
    try:
        from faster_whisper import WhisperModel
        
        print(f"    Loading model...")
        model = WhisperModel("Systran/faster-whisper-base", device="cpu", compute_type="int8")
        
        print(f"    Transcribing...")
        segments, info = model.transcribe(str(video_path), beam_size=5, language="zh")
        
        transcript = []
        for seg in segments:
            transcript.append({
                "start": seg.start,
                "end": seg.end,
                "text": seg.text.strip()
            })
        
        # Save
        output_file = TRANSCRIPT_DIR / f"{cid}_raw.json"
        output_file.write_text(json.dumps(transcript, ensure_ascii=False, indent=2))
        
        print(f"    ✓ Saved {len(transcript)} segments")
        
        # Create sample directory
        import subprocess
        import hashlib
        
        # Assign segment IDs
        for j, seg in enumerate(transcript):
            seg['segment_id'] = f"S{j+1:04d}"
        
        # Get duration
        try:
            cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
                   "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            duration = float(result.stdout.strip())
        except:
            duration = transcript[-1]['end'] if transcript else 0
        
        # Calculate metrics
        import re
        full_text = ''.join([s['text'] for s in transcript])
        metrics = {
            "duration_sec": round(duration, 2),
            "asr_segment_count": len(transcript),
            "total_chars": len(full_text),
            "chars_per_sec": round(len(full_text) / max(duration, 1), 2),
            "first_person_count": len(re.findall(r'[我咱俺]', full_text)),
            "second_person_count": len(re.findall(r'[你您]', full_text)),
            "number_count": len(re.findall(r'\d+', full_text)),
            "question_marker_count": full_text.count('？') + full_text.count('?'),
            "transcript_sha256": hashlib.sha256(full_text.encode('utf-8')).hexdigest()[:16]
        }
        
        # Get metadata
        row = item['row']
        if row:
            viral_type_raw = row.get('viral_type', '')
            viral_type = viral_type_raw.split(';')[0] if ';' in viral_type_raw else viral_type_raw
            title = row.get('desc', '')[:150]
            creator = row.get('nickname', '')
            topic = row.get('source_keyword', '')
            sample_role = row.get('sample_role', '')
            likes = int(row.get('liked_count', 0))
            comments = int(row.get('comment_count', 0))
            favorites = int(row.get('collected_count', 0))
            shares = int(row.get('share_count', 0))
        else:
            viral_type = 'UNKNOWN'
            title = 'TBD'
            creator = 'TBD'
            topic = 'TBD'
            sample_role = 'EXTERNAL_DATA'
            likes = 0
            comments = 0
            favorites = 0
            shares = 0
        
        # Create sample dir
        existing_samples = sorted(OUTPUT_DIR.glob("sample_*"))
        next_id = len(existing_samples) + 1
        sample_dir = OUTPUT_DIR / f"sample_{next_id:02d}"
        sample_dir.mkdir(parents=True, exist_ok=True)
        
        # Save files
        meta = {
            "content_id": cid,
            "url": f"https://www.douyin.com/video/{cid}",
            "creator_id": creator,
            "creator_name": creator,
            "title": title,
            "topic": topic,
            "viral_type": viral_type,
            "sample_role": sample_role,
            "duration_sec": round(duration, 2),
            "capture_time": datetime.now().isoformat(),
            "metadata_source": "MEDIACRAWLER_REAL_CDP" if row else "EXTERNAL"
        }
        (sample_dir / "01_metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
        
        perf = {
            "likes": likes,
            "comments": comments,
            "favorites": favorites,
            "shares": shares,
            "favorite_like_ratio": round(favorites / max(likes, 1), 3),
            "share_like_ratio": round(shares / max(likes, 1), 3),
            "comment_like_ratio": round(comments / max(likes, 1), 3)
        }
        (sample_dir / "02_performance.json").write_text(json.dumps(perf, indent=2, ensure_ascii=False))
        
        (sample_dir / "03_creator_baseline.json").write_text(json.dumps({
            "status": "NOT_COLLECTED",
            "note": "Requires API access or DOM fallback",
            "creator_id": creator
        }, indent=2, ensure_ascii=False))
        
        (sample_dir / "04_transcript_raw.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
        
        with open(sample_dir / "05_transcript_raw.md", 'w', encoding='utf-8') as f:
            f.write(f"# Raw Transcript: {cid}\n\n**Source**: ASR Raw Output\n**Status**: UNVERIFIED_RAW_ASR\n\n---\n\n")
            for seg in transcript:
                start_min = int(seg['start'] // 60)
                start_sec = seg['start'] % 60
                end_min = int(seg['end'] // 60)
                end_sec = seg['end'] % 60
                f.write(f"[{seg['segment_id']}] [{start_min:02d}:{start_sec:05.2f}-{end_min:02d}:{end_sec:05.2f}] {seg['text']}\n")
        
        (sample_dir / "06_metrics_basic.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False))
        
        with open(sample_dir / "07_top_comments.csv", 'w', encoding='utf-8') as f:
            f.write("comment_id,author,text,likes,reply_count,created_time\n")
            f.write("# To be collected\n")
        
        manifest = {
            "content_id": cid,
            "media_path": str(video_path),
            "media_size_mb": round(video_path.stat().st_size / 1024 / 1024, 2),
            "media_sha256": hashlib.sha256(video_path.read_bytes()).hexdigest()[:16],
            "transcript_sha256": metrics['transcript_sha256'],
            "segment_count": len(transcript),
            "duration_sec": round(duration, 2)
        }
        (sample_dir / "08_evidence_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
        
        print(f"  ✓ Created sample_{next_id:02d}")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")

# Final status
print("\n=== FINAL STATUS ===")
final_samples = sorted(OUTPUT_DIR.glob("sample_*"))
print(f"Total samples: {len(final_samples)}")

if len(final_samples) >= 6:
    print(f"\n✓ Generated enough samples for V4 bundle")
else:
    print(f"\n⚠ Need {6 - len(final_samples)} more samples for V4 bundle")
