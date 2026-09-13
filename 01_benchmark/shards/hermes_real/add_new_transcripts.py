#!/usr/bin/env python3
"""Process new transcripts and add to Batch 001"""
import json
import csv
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
OUTPUT_DIR = BASE / "analysis_batches" / "batch_001"

# Load selection
with open(SHARDS / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    selection = {row.get('aweme_id'): row for row in reader}

# Get existing samples
existing = set()
for s in OUTPUT_DIR.glob("sample_*"):
    meta = json.load(open(s / "01_metadata.json"))
    existing.add(meta.get('content_id', ''))

print(f"Existing samples: {len(existing)}")

# Find new transcripts
new_items = []
for trans_file in sorted(TRANSCRIPT_DIR.glob("*_raw.json")):
    cid = trans_file.name.replace('_raw.json', '')
    if cid in existing:
        continue
    
    video_path = VIDEO_DIR / cid / "video.mp4"
    if video_path.exists():
        row = selection.get(cid)
        new_items.append({
            'id': cid,
            'transcript': trans_file,
            'video': video_path,
            'row': row,
            'from_selection': cid in selection
        })

print(f"New transcripts to process: {len(new_items)}\n")

# Process each
def get_duration(video_path):
    try:
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
               "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return float(result.stdout.strip())
    except:
        return None

def calc_metrics(transcript, duration):
    import re
    full_text = ''.join([s['text'] for s in transcript])
    return {
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

added = 0
for item in new_items:
    cid = item['id']
    transcript = json.load(open(item['transcript'], 'r', encoding='utf-8'))
    video_path = item['video']
    row = item['row']
    
    print(f"\n--- Processing: {cid} ---")
    
    # Assign segment IDs
    for j, seg in enumerate(transcript):
        seg['segment_id'] = f"S{j+1:04d}"
    
    # Get duration
    duration = get_duration(video_path) or (transcript[-1]['end'] if transcript else 0)
    
    # Calculate metrics
    metrics = calc_metrics(transcript, duration)
    
    # Get metadata
    if row:
        viral_type_raw = row.get('viral_type', '')
        viral_type = viral_type_raw.split(';')[0] if ';' in viral_type_raw else viral_type_raw
        title = row.get('desc', '')[:150] or 'NULL'
        creator = row.get('nickname', '') or 'NULL'
        topic = row.get('source_keyword', '') or 'NULL'
        sample_role = row.get('sample_role', '') or 'NULL'
        
        likes = int(row.get('liked_count', 0)) if row.get('liked_count') else "NULL"
        comments = int(row.get('comment_count', 0)) if row.get('comment_count') else "NULL"
        favorites = int(row.get('collected_count', 0)) if row.get('collected_count') else "NULL"
        shares = int(row.get('share_count', 0)) if row.get('share_count') else "NULL"
    else:
        viral_type = "NULL"
        title = "NULL"
        creator = "NULL"
        topic = "NULL"
        sample_role = "EXTERNAL_DATA"
        likes = "NULL"
        comments = "NULL"
        favorites = "NULL"
        shares = "NULL"
    
    # Create sample dir
    existing_samples = sorted(OUTPUT_DIR.glob("sample_*"))
    next_id = len(existing_samples) + 1
    sample_dir = OUTPUT_DIR / f"sample_{next_id:02d}"
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # Save all files
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
        "favorite_like_ratio": round(favorites / max(likes, 1), 3) if isinstance(favorites, int) and isinstance(likes, int) else "NULL",
        "share_like_ratio": round(shares / max(likes, 1), 3) if isinstance(shares, int) and isinstance(likes, int) else "NULL",
        "comment_like_ratio": round(comments / max(likes, 1), 3) if isinstance(comments, int) and isinstance(likes, int) else "NULL"
    }
    (sample_dir / "02_performance.json").write_text(json.dumps(perf, indent=2, ensure_ascii=False))
    
    (sample_dir / "03_creator_baseline.json").write_text(json.dumps({
        "status": "NOT_COLLECTED",
        "note": "Requires API access or DOM fallback",
        "creator_id": creator
    }, indent=2, ensure_ascii=False))
    
    (sample_dir / "04_transcript_raw.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
    
    with open(sample_dir / "05_transcript_raw.md", 'w', encoding='utf-8') as f:
        f.write(f"# Raw Transcript: {cid}\n\n")
        f.write(f"**Source**: ASR Raw Output\n")
        f.write(f"**Status**: UNVERIFIED_RAW_ASR\n\n---\n\n")
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
    
    print(f"  ✓ Sample {next_id:02d} created ({len(transcript)} segs, {duration:.1f}s)")
    added += 1

print(f"\n=== SUMMARY ===")
print(f"Added: {added} samples")

# Final count
final = sorted(OUTPUT_DIR.glob("sample_*"))
print(f"Total: {len(final)} samples")

if len(final) >= 6:
    print(f"\n✓ Target reached (>=6)")
    print(f"  Ready to generate V4 bundle")
else:
    print(f"\n⚠ Need {6 - len(final)} more samples for V4")
