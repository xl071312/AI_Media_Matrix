#!/usr/bin/env python3
"""Add missing sample 7302348364815928612 to Batch 001"""
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
OUTPUT_DIR = BASE / "analysis_batches" / "batch_001"

# Target: 7302348364815928612
TARGET_ID = "7302348364815928612"

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
    print("=== ADDING MISSING SAMPLE TO BATCH 001 ===\n")
    
    # Check if sample exists
    trans_file = TRANSCRIPT_DIR / f"{TARGET_ID}_raw.json"
    video_path = VIDEO_DIR / TARGET_ID / "video.mp4"
    
    if not trans_file.exists():
        print(f"ERROR: Transcript not found for {TARGET_ID}")
        return
    
    if not video_path.exists():
        print(f"ERROR: Video not found for {TARGET_ID}")
        return
    
    print(f"Found: {TARGET_ID}")
    
    # Load transcript
    with open(trans_file, 'r', encoding='utf-8') as f:
        transcript = json.load(f)
    
    # Assign segment IDs
    for j, seg in enumerate(transcript):
        seg['segment_id'] = f"S{j+1:04d}"
    
    # Get duration
    duration = get_video_duration(video_path)
    if duration is None:
        duration = transcript[-1]['end'] if transcript else 0
    
    print(f"Duration: {duration:.1f}s, Segments: {len(transcript)}")
    
    # Calculate metrics
    metrics = calculate_basic_metrics(transcript, duration)
    
    # Create sample dir (sample_03)
    sample_dir = OUTPUT_DIR / "sample_03"
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # Load selection data for metadata
    import csv
    with open(SHARDS / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        selection = {row.get('aweme_id'): row for row in reader}
    
    row = selection.get(TARGET_ID, {})
    
    # 01_metadata.json
    meta = {
        "content_id": TARGET_ID,
        "url": f"https://www.douyin.com/video/{TARGET_ID}",
        "creator_id": row.get('nickname', ''),
        "creator_name": row.get('nickname', ''),
        "title": row.get('desc', '')[:150],
        "topic": row.get('source_keyword', ''),
        "viral_type": row.get('viral_type', '').split(';')[0],
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
    (sample_dir / "03_creator_baseline.json").write_text(json.dumps({
        "status": "NOT_COLLECTED",
        "note": "Requires API access or DOM fallback"
    }, indent=2, ensure_ascii=False))
    
    # 04_transcript_raw.json
    (sample_dir / "04_transcript_raw.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
    
    # 05_transcript_normalized.md
    with open(sample_dir / "05_transcript_normalized.md", 'w', encoding='utf-8') as f:
        f.write(f"# Normalized Transcript: {TARGET_ID}\n\n---\n\n")
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
        "content_id": TARGET_ID,
        "media_path": str(video_path),
        "media_size_mb": round(video_path.stat().st_size / 1024 / 1024, 2),
        "media_sha256": hashlib.sha256(video_path.read_bytes()).hexdigest()[:16],
        "transcript_sha256": metrics['transcript_sha256'],
        "segment_count": len(transcript),
        "duration_sec": round(duration, 2)
    }
    (sample_dir / "08_evidence_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    
    print(f"✓ Sample 03 added")
    
    # Now regenerate batch input with all 3 samples
    regenerate_batch_input()
    
    print(f"\n✓ Batch 001 now has 3 samples")

def regenerate_batch_input():
    """Regenerate BATCH_001_ANALYSIS_INPUT_V2.md with all samples"""
    import csv
    
    # Load all samples
    samples = sorted(OUTPUT_DIR.glob("sample_*"))
    results = []
    
    for s in samples:
        meta_file = s / "01_metadata.json"
        if meta_file.exists():
            with open(meta_file) as f:
                meta = json.load(f)
            results.append({
                'id': int(s.name.split('_')[1]),
                'content_id': meta['content_id'],
                'viral_type': meta['viral_type'],
                'duration': meta['duration_sec'],
                'segments': meta.get('asr_segment_count', 0)
            })
    
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
        lines.append(f"- **Viral Type**: {meta['viral_type']}")
        lines.append("")
        lines.append(f"### Performance")
        lines.append(f"- **Likes**: {perf['likes']:,}")
        lines.append(f"- **Comments**: {perf['comments']:,}")
        lines.append(f"- **Favorites**: {perf['favorites']:,}")
        lines.append(f"- **Shares**: {perf['shares']:,}")
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
        
        trans_file = sample_dir / "05_transcript_normalized.md"
        if trans_file.exists():
            content = trans_file.read_text(encoding='utf-8')
            lines.append(content)
        
        lines.append("")
        lines.append(f"### Basic Metrics")
        lines.append(f"- **Total Chars**: {metrics['total_chars']}")
        lines.append(f"- **Chars/Sec**: {metrics['chars_per_sec']}")
        lines.append(f"- **First Person**: {metrics['first_person_count']}")
        lines.append(f"- **Second Person**: {metrics['second_person_count']}")
        lines.append(f"- **Numbers**: {metrics['number_count']}")
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
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*Generated by HERMES as DATA ENGINEER / EVIDENCE PACKAGER*")
    lines.append(f"*Status: READY_FOR_ANALYSIS*")
    
    (OUTPUT_DIR / "BATCH_001_ANALYSIS_INPUT_V2.md").write_text('\n'.join(lines), encoding='utf-8')

if __name__ == "__main__":
    main()
