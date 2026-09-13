#!/usr/bin/env python3
"""
Phase 3 Analysis Batch 001 - Evidence Preparation
HERMES Role: DATA ENGINEER / EVIDENCE PACKAGER
"""
import json
import csv
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
TRANSCRIPT_DIR = BASE / "transcripts_v2"
QA_BATCH = BASE / "qa_batch_004"
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
OUTPUT_DIR = BASE.parent.parent / "01_benchmark" / "analysis_batches" / "batch_001"

def get_video_duration(video_path):
    """Get video duration using ffprobe"""
    try:
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
               "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return float(result.stdout.strip())
    except:
        return None

def calculate_basic_metrics(transcript, duration):
    """Calculate ONLY deterministic basic metrics"""
    full_text = ''.join([s['text'] for s in transcript])
    total_chars = len(full_text)
    
    # Deterministic counts only
    first_person = len(__import__('re').findall(r'[我咱俺]', full_text))
    second_person = len(__import__('re').findall(r'[你您]', full_text))
    number_count = len(__import__('re').findall(r'\d+', full_text))
    
    # Question markers (deterministic)
    question_markers = full_text.count('？') + full_text.count('?')
    
    return {
        "duration_sec": round(duration, 2),
        "asr_segment_count": len(transcript),
        "total_chars": total_chars,
        "chars_per_sec": round(total_chars / max(duration, 1), 2),
        "first_person_count": first_person,
        "second_person_count": second_person,
        "number_count": number_count,
        "question_marker_count": question_markers,
        "transcript_sha256": hashlib.sha256(full_text.encode('utf-8')).hexdigest()[:16]
    }

def main():
    print("=== PHASE 3 ANALYSIS BATCH 001 - EVIDENCE PREPARATION ===\n")
    print("HERMES Role: DATA ENGINEER / EVIDENCE PACKAGER\n")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load selection data
    with open(BASE / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        selection = list(reader)
    
    # Select 10 samples with diversity
    # Mix of viral types, different creators, different topics
    selected_ids = [
        "7533123064641506579",  # ABSOLUTE_VIRAL - 职场
        "7351254246710463755",  # ABSOLUTE_VIRAL - 职场  
        "7525683513706810682",  # ABSOLUTE_VIRAL - 财富认知
        "7647797848847439706",  # RELATIVE_BREAKOUT - 副业
        "7218880148861390118",  # RELATIVE_BREAKOUT - 普通人收入
        "7546212425998454074",  # ABSOLUTE_VIRAL - 能力变现
        "7643008320555568355",  # CONTROL - 投资认知
        "7652683577976491273",  # CONTROL - 能力变现
        "7629438426090296251",  # CONTROL - 创业失败
        "7539166936341515520"   # CONTROL - 消费陷阱
    ]
    
    results = []
    
    for i, content_id in enumerate(selected_ids, 1):
        print(f"\n--- Processing Sample {i}: {content_id} ---")
        
        # Find in selection
        sample_data = None
        for row in selection:
            if row.get('aweme_id') == content_id:
                sample_data = row
                break
        
        if not sample_data:
            print(f"  SKIP: Not in selection")
            continue
        
        # Check video exists
        video_path = VIDEO_DIR / content_id / "video.mp4"
        if not video_path.exists():
            print(f"  SKIP: Video not found")
            continue
        
        # Check transcript exists
        trans_file = TRANSCRIPT_DIR / f"{content_id}_raw.json"
        if not trans_file.exists():
            print(f"  SKIP: No transcript")
            continue
        
        # Load transcript
        with open(trans_file, 'r', encoding='utf-8') as f:
            transcript = json.load(f)
        
        # Assign segment IDs
        for j, seg in enumerate(transcript):
            seg['segment_id'] = f"S{j+1:04d}"
        
        # Get video duration
        duration = get_video_duration(video_path)
        if duration is None:
            duration = transcript[-1]['end'] if transcript else 0
        
        print(f"  Duration: {duration:.1f}s, Segments: {len(transcript)}")
        
        # Calculate basic metrics
        metrics = calculate_basic_metrics(transcript, duration)
        
        # Create sample directory
        sample_dir = OUTPUT_DIR / f"sample_{i:02d}"
        sample_dir.mkdir(parents=True, exist_ok=True)
        
        # 01_metadata.json
        meta = {
            "content_id": content_id,
            "aweme_id": content_id,
            "url": f"https://www.douyin.com/video/{content_id}",
            "creator_id": sample_data.get('nickname', ''),
            "creator_name": sample_data.get('nickname', ''),
            "title": sample_data.get('desc', '')[:100],
            "topic": sample_data.get('source_keyword', ''),
            "viral_type": sample_data.get('viral_type', ''),
            "sample_role": sample_data.get('sample_role', ''),
            "duration_sec": round(duration, 2),
            "capture_time": datetime.now().isoformat(),
            "metadata_source": "MEDIACRAWLER_REAL_CDP"
        }
        (sample_dir / "01_metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
        
        # 02_performance.json
        perf = {
            "likes": int(sample_data.get('liked_count', 0)),
            "comments": int(sample_data.get('comment_count', 0)),
            "favorites": int(sample_data.get('collected_count', 0)),
            "shares": int(sample_data.get('share_count', 0)),
            "favorite_like_ratio": round(int(sample_data.get('collected_count', 0)) / max(int(sample_data.get('liked_count', 1)), 1), 3),
            "share_like_ratio": round(int(sample_data.get('share_count', 0)) / max(int(sample_data.get('liked_count', 1)), 1), 3),
            "comment_like_ratio": round(int(sample_data.get('comment_count', 0)) / max(int(sample_data.get('liked_count', 1)), 1), 3)
        }
        (sample_dir / "02_performance.json").write_text(json.dumps(perf, indent=2, ensure_ascii=False))
        
        # 03_creator_baseline.json (placeholder - will be filled if available)
        baseline = {
            "status": "NOT_COLLECTED",
            "note": "Creator baseline requires API access or DOM fallback"
        }
        (sample_dir / "03_creator_baseline.json").write_text(json.dumps(baseline, indent=2, ensure_ascii=False))
        
        # 04_transcript_raw.json
        (sample_dir / "04_transcript_raw.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
        
        # 05_transcript_normalized.md
        with open(sample_dir / "05_transcript_normalized.md", 'w', encoding='utf-8') as f:
            f.write(f"# Normalized Transcript: {content_id}\n\n")
            f.write(f"**Note**: Raw ASR output. Awaiting manual quality check.\n\n---\n\n")
            for seg in transcript:
                start_min = int(seg['start'] // 60)
                start_sec = seg['start'] % 60
                end_min = int(seg['end'] // 60)
                end_sec = seg['end'] % 60
                f.write(f"[{seg['segment_id']}] [{start_min:02d}:{start_sec:05.2f} - {end_min:02d}:{end_sec:05.2f}] {seg['text']}\n")
        
        # 06_metrics_basic.json
        (sample_dir / "06_metrics_basic.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False))
        
        # 07_top_comments.csv (placeholder)
        with open(sample_dir / "07_top_comments.csv", 'w', encoding='utf-8') as f:
            f.write("comment_id,author,text,likes,reply_count,created_time\n")
            f.write("# Top comments to be collected separately\n")
        
        # 08_evidence_manifest.json
        manifest = {
            "content_id": content_id,
            "media_path": str(video_path),
            "media_size_mb": round(video_path.stat().st_size / 1024 / 1024, 2),
            "media_sha256": hashlib.sha256(video_path.read_bytes()).hexdigest()[:16],
            "transcript_sha256": metrics['transcript_sha256'],
            "segment_count": len(transcript),
            "duration_sec": round(duration, 2),
            "evidence_bindings": {
                "video_to_transcript": "via_content_id",
                "transcript_to_metrics": "computed",
                "performance_to_sample": "direct"
            }
        }
        (sample_dir / "08_evidence_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
        
        results.append({
            "id": i,
            "content_id": content_id,
            "viral_type": sample_data.get('viral_type', ''),
            "duration": round(duration, 2),
            "segments": len(transcript),
            "status": "COMPLETE"
        })
        
        print(f"  ✓ Complete")
    
    print(f"\n=== SUMMARY ===")
    print(f"Processed: {len(results)}/10")
    for r in results:
        print(f"  {r['id']}: {r['content_id']} ({r['viral_type']}) - {r['duration']}s")
    
    # Generate batch input file
    generate_batch_input(results)
    
    print(f"\n✓ Phase 3 Analysis Batch 001 Evidence Ready!")

def generate_batch_input(results):
    """Generate BATCH_001_ANALYSIS_INPUT.md"""
    lines = [
        "# Phase 3 Analysis Batch 001 - Evidence Input",
        "",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')} GMT+8",
        f"**Batch ID**: BATCH_001",
        f"**Total Samples**: {len(results)}",
        f"**HERMES Role**: DATA ENGINEER / EVIDENCE PACKAGER",
        "",
        "---",
        ""
    ]
    
    for r in results:
        sample_dir = OUTPUT_DIR / f"sample_{r['id']:02d}"
        
        # Load metadata
        meta_file = sample_dir / "01_metadata.json"
        perf_file = sample_dir / "02_performance.json"
        metrics_file = sample_dir / "06_metrics_basic.json"
        transcript_file = sample_dir / "05_transcript_normalized.md"
        manifest_file = sample_dir / "08_evidence_manifest.json"
        
        if not meta_file.exists():
            continue
        
        with open(meta_file) as f:
            meta = json.load(f)
        with open(perf_file) as f:
            perf = json.load(f)
        with open(metrics_file) as f:
            metrics = json.load(f)
        with open(manifest_file) as f:
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
        lines.append("")
        lines.append(f"### Video Duration")
        lines.append(f"- **Duration**: {metrics['duration_sec']}s")
        lines.append("")
        lines.append(f"### Evidence Manifest")
        lines.append(f"- **Media SHA256**: {manifest['media_sha256']}")
        lines.append(f"- **Transcript SHA256**: {manifest['transcript_sha256']}")
        lines.append(f"- **Segment Count**: {manifest['segment_count']}")
        lines.append("")
        lines.append(f"### Timed Transcript")
        lines.append("")
        
        # Include full transcript
        if transcript_file.exists():
            content = transcript_file.read_text(encoding='utf-8')
            # Skip header
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
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Total Samples | {len(results)} |")
    
    viral_counts = {}
    for r in results:
        vt = r['viral_type']
        viral_counts[vt] = viral_counts.get(vt, 0) + 1
    
    lines.append("| Viral Type Distribution |")
    for vt, count in viral_counts.items():
        lines.append(f"| {vt} | {count} |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*Generated by HERMES as DATA ENGINEER / EVIDENCE PACKAGER*")
    lines.append(f"*Status: READY_FOR_ANALYSIS*")
    
    (OUTPUT_DIR / "BATCH_001_ANALYSIS_INPUT.md").write_text('\n'.join(lines), encoding='utf-8')

if __name__ == "__main__":
    main()
