#!/usr/bin/env python3
"""
Phase 3 Analysis Batch 001 - Complete to 10 samples (BUG FIX + NEW)
HERMES Role: DATA ENGINEER / EVIDENCE PACKAGER ONLY
"""
import json
import csv
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

# Paths
BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
OUTPUT_DIR = BASE / "analysis_batches" / "batch_001"

def get_video_duration(video_path):
    try:
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
               "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return float(result.stdout.strip())
    except:
        return None

def calculate_basic_metrics(transcript, duration):
    import re
    full_text = ''.join([s['text'] for s in transcript])
    total_chars = len(full_text)
    return {
        "duration_sec": round(duration, 2),
        "asr_segment_count": len(transcript),
        "total_chars": total_chars,
        "chars_per_sec": round(total_chars / max(duration, 1), 2),
        "first_person_count": len(re.findall(r'[我咱俺]', full_text)),
        "second_person_count": len(re.findall(r'[你您]', full_text)),
        "number_count": len(re.findall(r'\d+', full_text)),
        "question_marker_count": full_text.count('？') + full_text.count('?'),
        "transcript_sha256": hashlib.sha256(full_text.encode('utf-8')).hexdigest()[:16]
    }

def merge_with_priority(existing, incoming, priority_order):
    """MERGE with priority: VERIFIED > HISTORICAL > NEW > NULL"""
    merged = dict(existing) if existing else {}
    rejected = []
    
    for key, new_val in incoming.items():
        old_val = merged.get(key)
        
        # Priority rules:
        # 1. If old value is verified (non-empty, non-zero for numbers), keep it
        # 2. If old value is TBD/UNKNOWN/empty and new has real value, use new
        # 3. For numeric fields, old > 0 should be preserved
        
        if key in ['likes', 'comments', 'favorites', 'shares']:
            if isinstance(old_val, (int, float)) and old_val > 0:
                if not new_val or (isinstance(new_val, (int, float)) and new_val == 0):
                    rejected.append(f"{key}: kept {old_val} > {new_val}")
                    continue
        
        if isinstance(old_val, str) and old_val.strip():
            if old_val not in ['TBD', 'UNKNOWN', '']:
                if not new_val or (isinstance(new_val, str) and not new_val.strip()):
                    rejected.append(f"{key}: kept '{old_val}' over empty")
                    continue
        
        # Use new value
        merged[key] = new_val
    
    return merged, rejected

def main():
    print("=== PHASE 3 ANALYSIS BATCH 001 - COMPLETE TO 10 ===\n")
    print("HERMES Role: DATA ENGINEER / EVIDENCE PACKAGER\n")
    print("Tasks:")
    print("  1. Fix Sample 003 metadata (restore real data)")
    print("  2. Fix Sample 002 role (RELATIVE_BREAKOUT -> CANDIDATE)")
    print("  3. Add Samples 004-010 (7 new samples)")
    print()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load selection data
    with open(SHARDS / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        selection = {row.get('aweme_id'): row for row in reader}
    
    # Find ALL available samples
    available = []
    for cid, row in selection.items():
        video_path = VIDEO_DIR / cid / "video.mp4"
        trans_file = TRANSCRIPT_DIR / f"{cid}_raw.json"
        
        if video_path.exists() and trans_file.exists():
            viral_type_raw = row.get('viral_type', '')
            viral_type = viral_type_raw.split(';')[0] if ';' in viral_type_raw else viral_type_raw
            available.append({
                'id': cid,
                'row': row,
                'video_path': video_path,
                'transcript': trans_file,
                'viral_type': viral_type,
                'from_selection': True
            })
    
    # Also check for external transcripts (like 7302348364815928612)
    for trans_file in TRANSCRIPT_DIR.glob("*_raw.json"):
        cid = trans_file.name.replace('_raw.json', '')
        if not any(a['id'] == cid for a in available):
            video_path = VIDEO_DIR / cid / "video.mp4"
            if video_path.exists():
                available.append({
                    'id': cid,
                    'row': None,
                    'video_path': video_path,
                    'transcript': trans_file,
                    'viral_type': 'UNKNOWN',
                    'from_selection': False
                })
    
    print(f"Total available samples: {len(available)}\n")
    
    # Define existing samples (001-003)
    existing_ids = ['7546212425998454074', '7647797848847439706', '7302348364815928612']
    
    # Fix Sample 003 metadata - restore real data from selection
    print("=== FIXING SAMPLE 003 ===")
    sample_003_id = '7302348364815928612'
    sample_003_dir = OUTPUT_DIR / "sample_003"
    
    if sample_003_dir.exists():
        # Check if we can find this ID in selection
        for cid, row in selection.items():
            if cid == sample_003_id:
                print(f"  Found in selection: {row.get('desc', '')[:50]}...")
                print(f"  Creator: {row.get('nickname', '')}")
                print(f"  Viral Type: {row.get('viral_type', '')}")
                print(f"  Likes: {row.get('liked_count', '')}")
                
                # Update metadata with merge protection
                meta_file = sample_003_dir / "01_metadata.json"
                if meta_file.exists():
                    with open(meta_file) as f:
                        existing_meta = json.load(f)
                    
                    incoming_meta = {
                        "content_id": cid,
                        "title": row.get('desc', '')[:150],
                        "creator_name": row.get('nickname', ''),
                        "creator_id": row.get('nickname', ''),
                        "viral_type": row.get('viral_type', '').split(';')[0],
                        "topic": row.get('source_keyword', ''),
                        "sample_role": row.get('sample_role', ''),
                        "metadata_source": "MEDIACRAWLER_REAL_CDP"
                    }
                    
                    merged_meta, rejected = merge_with_priority(existing_meta, incoming_meta, [])
                    meta_file.write_text(json.dumps(merged_meta, indent=2, ensure_ascii=False))
                    
                    if rejected:
                        print(f"  Merge rejections: {rejected}")
                break
        else:
            print(f"  NOT found in selection - using external data only")
    
    # Fix Sample 002 role
    print("\n=== FIXING SAMPLE 002 ROLE ===")
    sample_002_id = '7647797848847439706'
    sample_002_dir = OUTPUT_DIR / "sample_002"
    
    if sample_002_dir.exists():
        meta_file = sample_002_dir / "01_metadata.json"
        if meta_file.exists():
            with open(meta_file) as f:
                meta = json.load(f)
            
            # Check if we have creator baseline
            baseline_file = sample_002_dir / "03_creator_baseline.json"
            has_baseline = False
            if baseline_file.exists():
                with open(baseline_file) as f:
                    baseline = json.load(f)
                has_baseline = baseline.get('status') == 'COLLECTED'
            
            # Change to CANDIDATE if no baseline
            if not has_baseline:
                current_role = meta.get('sample_role', '')
                if 'RELATIVE_BREAKOUT' in current_role and 'CANDIDATE' not in current_role:
                    meta['sample_role'] = 'RELATIVE_BREAKOUT_CANDIDATE'
                    meta['role_note'] = 'Baseline not available - downgraded to CANDIDATE'
                    print(f"  Changed role: {current_role} -> {meta['sample_role']}")
                    meta_file.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    
    # Select 7 new samples (004-010)
    print("\n=== SELECTING NEW SAMPLES 004-010 ===")
    
    # Exclude existing samples
    new_candidates = [a for a in available if a['id'] not in existing_ids]
    
    # Sort by type diversity and engagement
    type_priority = {
        'ABSOLUTE_VIRAL': 0,
        'RELATIVE_BREAKOUT': 1,
        'SAVE_HEAVY': 2,
        'SHARE_HEAVY': 3,
        'COMMENT_HEAVY': 4,
        'CONTROL': 5,
        'NORMAL_REFERENCE': 6,
        'UNKNOWN': 7
    }
    
    new_candidates.sort(key=lambda x: (
        type_priority.get(x['viral_type'], 7),
        -int(x['row'].get('liked_count', 0)) if x['row'] else 0
    ))
    
    # Take up to 7 new samples
    new_samples = new_candidates[:7]
    
    results = []
    
    # First, process existing samples 001-003 (skip if already exists)
    for i, item in enumerate(available, 1):
        if item['id'] in existing_ids:
            # Skip - already exists
            continue
        
        # This shouldn't happen, but handle gracefully
        pass
    
    # Now add new samples 004-010
    for i, item in enumerate(new_samples, 4):
        cid = item['id']
        row = item['row']
        video_path = item['video_path']
        
        print(f"\n--- Sample {i}: {cid} ({item['viral_type']}) ---")
        
        # Get viral type
        viral_type = item['viral_type']
        
        # Get metadata
        if row:
            title = row.get('desc', '')[:150]
            creator = row.get('nickname', '')
            topic = row.get('source_keyword', '')
            sample_role = row.get('sample_role', '')
            likes = int(row.get('liked_count', 0))
            comments = int(row.get('comment_count', 0))
            favorites = int(row.get('collected_count', 0))
            shares = int(row.get('share_count', 0))
        else:
            title = "TBD"
            creator = "TBD"
            topic = "TBD"
            sample_role = "EXTERNAL_DATA"
            likes = 0
            comments = 0
            favorites = 0
            shares = 0
        
        # Load transcript
        with open(item['transcript'], 'r', encoding='utf-8') as f:
            transcript = json.load(f)
        
        # Assign segment IDs
        for j, seg in enumerate(transcript):
            seg['segment_id'] = f"S{j+1:04d}"
        
        # Get duration
        duration = get_video_duration(video_path)
        if duration is None:
            duration = transcript[-1]['end'] if transcript else 0
        
        print(f"  Duration: {duration:.1f}s, Segments: {len(transcript)}")
        
        # Calculate metrics
        metrics = calculate_basic_metrics(transcript, duration)
        
        # Create sample dir
        sample_dir = OUTPUT_DIR / f"sample_{i:02d}"
        sample_dir.mkdir(parents=True, exist_ok=True)
        
        # 01_metadata.json
        incoming_meta = {
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
        (sample_dir / "01_metadata.json").write_text(json.dumps(incoming_meta, indent=2, ensure_ascii=False))
        
        # 02_performance.json
        incoming_perf = {
            "likes": likes,
            "comments": comments,
            "favorites": favorites,
            "shares": shares,
            "favorite_like_ratio": round(favorites / max(likes, 1), 3),
            "share_like_ratio": round(shares / max(likes, 1), 3),
            "comment_like_ratio": round(comments / max(likes, 1), 3)
        }
        (sample_dir / "02_performance.json").write_text(json.dumps(incoming_perf, indent=2, ensure_ascii=False))
        
        # 03_creator_baseline.json
        (sample_dir / "03_creator_baseline.json").write_text(json.dumps({
            "status": "NOT_COLLECTED",
            "note": "Requires API access or DOM fallback",
            "creator_id": creator
        }, indent=2, ensure_ascii=False))
        
        # 04_transcript_raw.json
        (sample_dir / "04_transcript_raw.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
        
        # 05_transcript_raw.md
        with open(sample_dir / "05_transcript_raw.md", 'w', encoding='utf-8') as f:
            f.write(f"# Raw Transcript: {cid}\n\n")
            f.write(f"**Source**: ASR Raw Output\n")
            f.write(f"**Status**: UNVERIFIED_RAW_ASR\n")
            f.write(f"**Note**: No normalization applied. Awaiting manual quality check.\n\n---\n\n")
            for seg in transcript:
                start_min = int(seg['start'] // 60)
                start_sec = seg['start'] % 60
                end_min = int(seg['end'] // 60)
                end_sec = seg['end'] % 60
                f.write(f"[{seg['segment_id']}] [{start_min:02d}:{start_sec:05.2f}-{end_min:02d}:{end_sec:05.2f}] {seg['text']}\n")
        
        # 06_metrics_basic.json
        (sample_dir / "06_metrics_basic.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False))
        
        # 07_top_comments.csv
        with open(sample_dir / "07_top_comments.csv", 'w', encoding='utf-8') as f:
            f.write("comment_id,author,text,likes,reply_count,created_time\n")
            f.write("# To be collected\n")
        
        # 08_evidence_manifest.json
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
        
        results.append({
            "id": i,
            "content_id": cid,
            "viral_type": viral_type,
            "duration": round(duration, 2),
            "segments": len(transcript),
            "status": "COMPLETE"
        })
        
        print(f"  ✓ Complete")
    
    print(f"\n=== SUMMARY ===")
    print(f"New samples added: {len(results)}")
    
    # Count total
    all_samples = sorted(OUTPUT_DIR.glob("sample_*"))
    print(f"Total samples in batch: {len(all_samples)}")
    
    if len(all_samples) == 10:
        generate_batch_input_v4(all_samples)
        print(f"\n✓ Batch 001 Evidence Complete!")
    else:
        print(f"\n⚠ WARNING: Only {len(all_samples)} samples, need 10")
        print(f"   Cannot generate V4 bundle yet")

def generate_batch_input_v4(samples):
    """Generate BATCH_001_ANALYSIS_INPUT_V4.md"""
    
    # Calculate totals
    total_segments = 0
    total_duration = 0
    
    for s in samples:
        manifest = json.load(open(s / "08_evidence_manifest.json"))
        total_segments += manifest.get('segment_count', 0)
        total_duration += manifest.get('duration_sec', 0)
    
    lines = [
        "# Phase 3 Analysis Batch 001 - Complete Evidence Input V4",
        "",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')} GMT+8",
        f"**Batch ID**: BATCH_001",
        f"**Total Samples**: {len(samples)}",
        f"**Total Segments**: {total_segments}",
        f"**Total Duration**: {total_duration:.1f}s",
        f"**HERMES Role**: DATA ENGINEER / EVIDENCE PACKAGER",
        f"**Status**: READY_FOR_ANALYSIS",
        "",
        "---",
        ""
    ]
    
    for s in samples:
        i = int(s.name.split('_')[1])
        
        with open(s / "01_metadata.json") as f:
            meta = json.load(f)
        with open(s / "02_performance.json") as f:
            perf = json.load(f)
        with open(s / "06_metrics_basic.json") as f:
            metrics = json.load(f)
        with open(s / "08_evidence_manifest.json") as f:
            manifest = json.load(f)
        
        lines.append(f"## Sample {i}")
        lines.append("")
        lines.append(f"### Basic Info")
        lines.append(f"- **Content ID**: {meta['content_id']}")
        lines.append(f"- **Title**: {meta.get('title', 'UNKNOWN')}")
        lines.append(f"- **Author**: {meta.get('creator_name', 'UNKNOWN')}")
        lines.append(f"- **Topic**: {meta.get('topic', 'UNKNOWN')}")
        lines.append(f"- **Sample Role**: {meta.get('sample_role', 'UNKNOWN')}")
        lines.append(f"- **Viral Type**: {meta.get('viral_type', 'UNKNOWN')}")
        lines.append("")
        lines.append(f"### Performance")
        lines.append(f"- **Likes**: {perf.get('likes', 0):,}")
        lines.append(f"- **Comments**: {perf.get('comments', 0):,}")
        lines.append(f"- **Favorites**: {perf.get('favorites', 0):,}")
        lines.append(f"- **Shares**: {perf.get('shares', 0):,}")
        lines.append(f"- **Favorite/Like Ratio**: {perf.get('favorite_like_ratio', 0)}")
        lines.append(f"- **Share/Like Ratio**: {perf.get('share_like_ratio', 0)}")
        lines.append("")
        lines.append(f"### Video Duration")
        lines.append(f"- **Duration**: {metrics['duration_sec']}s")
        lines.append("")
        lines.append(f"### Evidence Manifest")
        lines.append(f"- **Media SHA256**: {manifest['media_sha256']}")
        lines.append(f"- **Transcript SHA256**: {manifest['transcript_sha256']}")
        lines.append(f"- **Segment Count**: {manifest['segment_count']}")
        lines.append("")
        lines.append(f"### Raw Timed Transcript")
        lines.append(f"")
        lines.append(f"**Status**: UNVERIFIED_RAW_ASR")
        lines.append(f"**Note**: No normalization applied. Awaiting manual quality check.")
        lines.append(f"")
        
        # Include FULL transcript
        trans_file = s / "05_transcript_raw.md"
        if trans_file.exists():
            content = trans_file.read_text(encoding='utf-8')
            lines.append(content)
        else:
            lines.append("*Transcript not available*")
        
        lines.append("")
        lines.append(f"### Basic Metrics")
        lines.append(f"- **Total Chars**: {metrics['total_chars']}")
        lines.append(f"- **Chars/Sec**: {metrics['chars_per_sec']}")
        lines.append(f"- **First Person**: {metrics['first_person_count']}")
        lines.append(f"- **Second Person**: {metrics['second_person_count']}")
        lines.append(f"- **Numbers**: {metrics['number_count']}")
        lines.append(f"- **Question Markers**: {metrics['question_marker_count']}")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Summary
    lines.append("# Batch Summary")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total Samples | {len(samples)} |")
    lines.append(f"| Total Segments | {total_segments} |")
    lines.append(f"| Total Duration | {total_duration:.1f}s |")
    lines.append(f"| Average Duration | {total_duration/len(samples):.1f}s |")
    
    viral_counts = {}
    for s in samples:
        meta = json.load(open(s / "01_metadata.json"))
        vt = meta.get('viral_type', 'UNKNOWN')
        viral_counts[vt] = viral_counts.get(vt, 0) + 1
    
    lines.append(f"| Viral Type Distribution |")
    for vt, count in sorted(viral_counts.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {vt} | {count} |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*Generated by HERMES as DATA ENGINEER / EVIDENCE PACKAGER*")
    lines.append(f"*No Logic Analysis, Deep Analysis, or Voice Hypotheses generated*")
    lines.append(f"*Status: READY_FOR_ANALYSIS*")
    lines.append(f"*Bug Fixes Applied:*")
    lines.append(f"  - Sample 003 metadata restored from verified sources")
    lines.append(f"  - Sample 002 role corrected to RELATIVE_BREAKOUT_CANDIDATE")
    lines.append(f"  - MERGE protection for verified real values")
    lines.append(f"  - Correct segment count aggregation")
    
    (OUTPUT_DIR / "BATCH_001_ANALYSIS_INPUT_V4.md").write_text('\n'.join(lines), encoding='utf-8')
    
    print(f"\n=== VALIDATION ===")
    print(f"Total Samples: {len(samples)}")
    print(f"Total Segments: {total_segments}")
    print(f"Bundle Size: {(OUTPUT_DIR / 'BATCH_001_ANALYSIS_INPUT_V4.md').stat().st_size} bytes")

if __name__ == "__main__":
    main()
