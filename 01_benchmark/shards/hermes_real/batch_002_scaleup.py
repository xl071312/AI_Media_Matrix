#!/usr/bin/env python3
"""
Batch 002 - Scale-Up Data Collection (Fixed)
HERMES Role: DATA ENGINEER ONLY
"""
import json
import csv
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
from collections import Counter

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH_DIR = BASE / "analysis_batches" / "batch_002"
BATCH_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")

# Load selection
with open(SHARDS / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
    selection = {row.get('aweme_id'): row for row in csv.DictReader(f)}

# Load existing CIDs from all batches
existing_cids = set()
for batch in BASE.glob("analysis_batches/batch_*"):
    for s in batch.glob("sample_*"):
        try:
            meta = json.load(open(s / "01_metadata.json"))
            existing_cids.add(meta.get('content_id', ''))
        except:
            pass

def get_duration(path):
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                           "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                          capture_output=True, text=True, timeout=10)
        return float(r.stdout.strip())
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

def run_asr(video_path, cid):
    """Run ASR on single video"""
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("Systran/faster-whisper-base", device="cpu", compute_type="int8")
        segments, info = model.transcribe(str(video_path), beam_size=5, language="zh")
        
        transcript = []
        for seg in segments:
            transcript.append({"start": seg.start, "end": seg.end, "text": seg.text.strip()})
        
        # Save transcript
        (TRANSCRIPT_DIR / f"{cid}_raw.json").write_text(json.dumps(transcript, ensure_ascii=False, indent=2))
        return transcript
    except Exception as e:
        print(f"  ASR failed for {cid}: {e}")
        return None

def create_sample(next_id, cid, row, transcript, duration):
    """Create sample directory with all evidence files"""
    sample_dir = BATCH_DIR / f"sample_{next_id:02d}"
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # Metadata
    vt_raw = row.get('viral_type', '')
    vt = vt_raw.split(';')[0] if ';' in vt_raw else vt_raw
    title = row.get('desc', '')[:150] or 'NULL'
    creator = row.get('nickname', '') or 'NULL'
    topic = row.get('source_keyword', '') or 'NULL'
    role = row.get('sample_role', '') or 'NULL'
    
    meta = {
        "content_id": cid,
        "url": f"https://www.douyin.com/video/{cid}",
        "creator_id": creator,
        "creator_name": creator,
        "title": title,
        "topic": topic,
        "viral_type": vt,
        "sample_role": role,
        "duration_sec": round(duration, 2),
        "capture_time": datetime.now().isoformat(),
        "metadata_source": "MEDIACRAWLER_REAL_CDP"
    }
    (sample_dir / "01_metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    
    # Performance
    likes = int(row.get('liked_count', 0)) if row.get('liked_count') else None
    comments = int(row.get('comment_count', 0)) if row.get('comment_count') else None
    favorites = int(row.get('collected_count', 0)) if row.get('collected_count') else None
    shares = int(row.get('share_count', 0)) if row.get('share_count') else None
    
    perf = {"likes": likes, "comments": comments, "favorites": favorites, "shares": shares}
    if isinstance(likes, int) and likes > 0:
        perf["favorite_like_ratio"] = round(favorites / max(likes, 1), 3) if favorites else None
        perf["share_like_ratio"] = round(shares / max(likes, 1), 3) if shares else None
        perf["comment_like_ratio"] = round(comments / max(likes, 1), 3) if comments else None
    (sample_dir / "02_performance.json").write_text(json.dumps(perf, indent=2, ensure_ascii=False))
    
    # Creator baseline placeholder
    (sample_dir / "03_creator_baseline.json").write_text(json.dumps({
        "status": "NOT_COLLECTED",
        "note": "Requires API access or DOM fallback",
        "creator_id": creator
    }, indent=2, ensure_ascii=False))
    
    # Transcript raw
    (sample_dir / "04_transcript_raw.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
    
    # Transcript markdown
    lines = [f"# Raw Transcript: {cid}", "",
             f"**Source**: ASR Raw Output",
             f"**Status**: UNVERIFIED_RAW_ASR",
             f"**Note**: Complete transcript embedded.", "", "---", ""]
    for j, seg in enumerate(transcript):
        sm, ss = int(seg['start']//60), seg['start']%60
        em, es = int(seg['end']//60), seg['end']%60
        lines.append(f"[S{j+1:04d}] [{sm:02d}:{ss:05.2f}-{em:02d}:{es:05.2f}] {seg['text']}")
    (sample_dir / "05_transcript_raw.md").write_text('\n'.join(lines), encoding='utf-8')
    
    # Metrics
    metrics = calc_metrics(transcript, duration)
    (sample_dir / "06_metrics_basic.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False))
    
    # Top comments placeholder
    with open(sample_dir / "07_top_comments.csv", 'w', encoding='utf-8') as f:
        f.write("comment_id,author,text,likes,reply_count,created_time\n")
        f.write("# To be collected\n")
    
    # Manifest
    video_path = VIDEO_DIR / cid / "video.mp4"
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
    
    return manifest

def main():
    print("=== BATCH 002 - SCALE-UP ===\n")
    
    # Find available samples with video and no existing batch entry
    available = []
    for cid, row in selection.items():
        if cid in existing_cids:
            continue
        video_path = VIDEO_DIR / cid / "video.mp4"
        trans_file = TRANSCRIPT_DIR / f"{cid}_raw.json"
        if video_path.exists():
            available.append({'cid': cid, 'row': row, 'path': video_path, 
                            'has_transcript': trans_file.exists()})
    
    print(f"Available with video: {len(available)}")
    
    # Target: 30 samples with role distribution
    target_roles = {
        'ABSOLUTE_VIRAL': 8,
        'RELATIVE_BREAKOUT': 3,
        'RELATIVE_BREAKOUT_CANDIDATE': 3,
        'SAVE_HEAVY': 4,
        'SHARE_HEAVY': 4,
        'COMMENT_HEAVY': 4,
        'NORMAL_REFERENCE': 4
    }
    
    # Sort by role priority
    selected = []
    role_counts = Counter()
    
    for item in available:
        role = item['row'].get('sample_role', 'UNKNOWN')
        needed = target_roles.get(role, 0)
        current = role_counts.get(role, 0)
        
        if current < needed:
            selected.append(item)
            role_counts[role] = current + 1
        
        if len(selected) >= 30:
            break
    
    # Fill remaining slots
    if len(selected) < 30:
        for item in available:
            if item not in selected:
                selected.append(item)
            if len(selected) >= 30:
                break
    
    print(f"Selected: {len(selected)}")
    print(f"Role distribution:")
    for role, count in role_counts.most_common():
        print(f"  {role}: {count}")
    
    # Process each sample
    processed = 0
    for i, item in enumerate(selected, 1):
        cid = item['cid']
        print(f"\n[{i}/30] Processing {cid}...")
        
        # Get duration
        duration = get_duration(item['path'])
        if not duration:
            print(f"  ✗ Cannot get duration")
            continue
        
        # Check if transcript exists
        trans_file = TRANSCRIPT_DIR / f"{cid}_raw.json"
        if item.get('has_transcript') and trans_file.exists():
            with open(trans_file, 'r', encoding='utf-8') as f:
                transcript = json.load(f)
        else:
            # Run ASR
            transcript = run_asr(item['path'], cid)
            if not transcript:
                continue
            
            # Re-read
            with open(trans_file, 'r', encoding='utf-8') as f:
                transcript = json.load(f)
        
        if not transcript:
            print(f"  ✗ Empty transcript")
            continue
        
        # Create sample
        manifest = create_sample(i, cid, item['row'], transcript, duration)
        print(f"  ✓ {manifest['segment_count']} segments, {manifest['duration_sec']}s")
        processed += 1
        
        if processed >= 30:
            break
    
    print(f"\n=== BATCH 002 STATUS ===")
    print(f"Processed: {processed}/30")
    print(f"Output: {BATCH_DIR}")
    
    # Generate manifest
    samples = sorted(BATCH_DIR.glob("sample_*"))
    if samples:
        rows = []
        for i, s in enumerate(samples, 1):
            meta = json.load(open(s / "01_metadata.json"))
            perf = json.load(open(s / "02_performance.json"))
            manifest = json.load(open(s / "08_evidence_manifest.json"))
            rows.append({
                'analysis_id': f'B002-{i:03d}',
                'content_id': meta['content_id'],
                'viral_type': meta.get('viral_type', 'NULL'),
                'sample_role': meta.get('sample_role', 'NULL'),
                'duration_sec': manifest.get('duration_sec', 0),
                'segment_count': manifest.get('segment_count', 0),
                'media_sha256': manifest.get('media_sha256', ''),
                'transcript_sha256': manifest.get('transcript_sha256', ''),
                'likes': perf.get('likes', 'NULL'),
                'transcript_complete': manifest.get('segment_count', 0) > 0
            })
        
        csv_path = BATCH_DIR / "BATCH_002_EVIDENCE_MANIFEST.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"Manifest: {csv_path}")

if __name__ == "__main__":
    main()
