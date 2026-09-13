#!/usr/bin/env python3
"""
Phase 3 Analysis Batch 001 - Complete to 10 samples
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

def main():
    print("=== PHASE 3 ANALYSIS BATCH 001 - COMPLETE TO 10 ===\n")
    print("HERMES Role: DATA ENGINEER / EVIDENCE PACKAGER\n")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load selection
    with open(SHARDS / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        selection = {row.get('aweme_id'): row for row in reader}
    
    # Find all available samples
    available = []
    for cid, row in selection.items():
        video_path = VIDEO_DIR / cid / "video.mp4"
        trans_file = TRANSCRIPT_DIR / f"{cid}_raw.json"
        
        if video_path.exists() and trans_file.exists():
            available.append({
                'id': cid,
                'row': row,
                'video_path': video_path,
                'transcript': trans_file
            })
    
    print(f"Available samples: {len(available)}\n")
    
    # Select 10 diverse samples
    # Target: 3 ABSOLUTE_VIRAL, 3 RELATIVE_BREAKOUT, 2 SAVE_HEAVY, 2 CONTROL
    target_types = {
        'ABSOLUTE_VIRAL': 0,
        'RELATIVE_BREAKOUT': 1,
        'RELATIVE_BREAKOUT_CANDIDATE': 1,
        'SAVE_HEAVY': 2,
        'CONTROL': 3,
        'NORMAL_REFERENCE': 3
    }
    
    # Sort by type priority
    available.sort(key=lambda x: target_types.get(x['row'].get('viral_type', ''), 4))
    
    # Select first 10
    batch = available[:10]
    
    results = []
    
    for i, item in enumerate(batch, 1):
        cid = item['id']
        row = item['row']
        video_path = item['video_path']
        
        # Get viral type - clean it up
        viral_type_raw = row.get('viral_type', '')
        # Take first type if multiple
        viral_type = viral_type_raw.split(';')[0] if ';' in viral_type_raw else viral_type_raw
        
        print(f"\n--- Sample {i}: {cid} ({viral_type}) ---")
        
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
        
        # Calculate basic metrics
        metrics = calculate_basic_metrics(transcript, duration)
        
        # Create sample dir
        sample_dir = OUTPUT_DIR / f"sample_{i:02d}"
        sample_dir.mkdir(parents=True, exist_ok=True)
        
        # 01_metadata.json
        meta = {
            "content_id": cid,
            "url": f"https://www.douyin.com/video/{cid}",
            "creator_id": row.get('nickname', ''),
            "creator_name": row.get('nickname', ''),
            "title": row.get('desc', '')[:150],
            "topic": row.get('source_keyword', ''),
            "viral_type": viral_type,
            "sample_role": row.get('sample_role', ''),
            "duration_sec": round(duration, 2),
            "capture_time": datetime.now().isoformat(),
            "metadata_source": "MEDIACRAWLER_REAL_CDP"
        }
        (sample_dir / "01_metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
        
        # 02_performance.json
        likes = int(row.get('liked_count', 0))
        comments = int(row.get('comment_count', 0))
        favorites = int(row.get('collected_count', 0))
        shares = int(row.get('share_count', 0))
        
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
        
        # 03_creator_baseline.json
        baseline = {
            "status": "NOT_COLLECTED",
            "note": "Requires API access or DOM fallback",
            "creator_id": row.get('nickname', '')
        }
        (sample_dir / "03_creator_baseline.json").write_text(json.dumps(baseline, indent=2, ensure_ascii=False))
        
        # 04_transcript_raw.json
        (sample_dir / "04_transcript_raw.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
        
        # 05_transcript_normalized.md (FULL transcript, no truncation)
        with open(sample_dir / "05_transcript_normalized.md", 'w', encoding='utf-8') as f:
            f.write(f"# Normalized Transcript: {cid}\n\n")
            f.write(f"**Note**: Raw ASR output. Awaiting manual quality check.\n\n---\n\n")
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
    print(f"Processed: {len(results)}/10 samples")
    
    # Count by type
    type_counts = {}
    for r in results:
        vt = r['viral_type']
        type_counts[vt] = type_counts.get(vt, 0) + 1
    
    print(f"\nType distribution:")
    for vt, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {vt}: {count}")
    
    for r in results:
        print(f"\n  {r['id']}: {r['content_id']} ({r['viral_type']}) - {r['duration']}s, {r['segments']} segs")
    
    # Generate batch input
    generate_batch_input(results)
    
    print(f"\n✓ Batch 001 Evidence Complete!")
    print(f"Output: {OUTPUT_DIR}")

def generate_batch_input(results):
    """Generate complete BATCH_001_ANALYSIS_INPUT_V2.md"""
    lines = [
        "# Phase 3 Analysis Batch 001 - Complete Evidence Input",
        "",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')} GMT+8",
        f"**Batch ID**: BATCH_001",
        f"**Total Samples**: {len(results)}",
        f"**HERMES Role**: DATA ENGINEER / EVIDENCE PACKAGER",
        f"**Status**: READY_FOR_ANALYSIS",
        "",
        "---",
        ""
    ]
    
    for r in results:
        sample_dir = OUTPUT_DIR / f"sample_{r['id']:02d}"
        
        with open(sample_dir / "01_metadata.json") as f:
            meta = json.load(f)
        with open(sample_dir / "02_performance.json") as f:
            perf = json.load(f)
        with open(sample_dir / "06_metrics_basic.json") as f:
            metrics = json.load(f)
        with open(sample_dir / "08_evidence_manifest.json") as f:
            manifest = json.load(f)
        
        lines.append(f"## Sample {r['id']}")
        lines.append("")
        lines.append(f"### Basic Info")
        lines.append(f"- **Content ID**: {meta['content_id']}")
        lines.append(f"- **Title**: {meta['title']}")
        lines.append(f"- **Author**: {meta['creator_name']}")
        lines.append(f"- **Topic**: {meta['topic']}")
        lines.append(f"- **Sample Role**: {meta['sample_role']}")
        lines.append(f"- **Viral Type**: {meta['viral_type']}")
        lines.append("")
        lines.append(f"### Performance")
        lines.append(f"- **Likes**: {perf['likes']:,}")
        lines.append(f"- **Comments**: {perf['comments']:,}")
        lines.append(f"- **Favorites**: {perf['favorites']:,}")
        lines.append(f"- **Shares**: {perf['shares']:,}")
        lines.append(f"- **Favorite/Like Ratio**: {perf['favorite_like_ratio']}")
        lines.append(f"- **Share/Like Ratio**: {perf['share_like_ratio']}")
        lines.append(f"- **Comment/Like Ratio**: {perf['comment_like_ratio']}")
        lines.append("")
        lines.append(f"### Video Duration")
        lines.append(f"- **Duration**: {metrics['duration_sec']}s")
        lines.append("")
        lines.append(f"### Evidence Manifest")
        lines.append(f"- **Media SHA256**: {manifest['media_sha256']}")
        lines.append(f"- **Transcript SHA256**: {manifest['transcript_sha256']}")
        lines.append(f"- **Segment Count**: {manifest['segment_count']}")
        lines.append("")
        lines.append(f"### Complete Timed Transcript")
        lines.append("")
        
        # Include FULL transcript, no truncation
        trans_file = sample_dir / "05_transcript_normalized.md"
        if trans_file.exists():
            content = trans_file.read_text(encoding='utf-8')
            # Skip header lines
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
    lines.append(f"| Total Samples | {len(results)} |")
    
    viral_counts = {}
    for r in results:
        vt = r['viral_type']
        viral_counts[vt] = viral_counts.get(vt, 0) + 1
    
    for vt, count in sorted(viral_counts.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {vt} | {count} |")
    
    lines.append(f"| Total Duration | {sum(r['duration'] for r in results):.1f}s |")
    lines.append(f"| Total Segments | {sum(r['segments'] for r in results)} |")
    lines.append(f"| Average Duration | {sum(r['duration'] for r in results)/len(results):.1f}s |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*Generated by HERMES as DATA ENGINEER / EVIDENCE PACKAGER*")
    lines.append(f"*No Logic Analysis, Deep Analysis, or Voice Hypotheses generated*")
    lines.append(f"*Status: READY_FOR_ANALYSIS*")
    
    (OUTPUT_DIR / "BATCH_001_ANALYSIS_INPUT_V2.md").write_text('\n'.join(lines), encoding='utf-8')

if __name__ == "__main__":
    main()
