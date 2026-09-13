#!/usr/bin/env python3
"""
Continue ASR to get more samples for Batch 001
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

def run_asr(video_path, output_dir):
    """Run faster-whisper ASR on video"""
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
        
        output_file = output_dir / f"{video_path.parent.name}_raw.json"
        output_file.write_text(json.dumps(transcript, ensure_ascii=False, indent=2))
        
        print(f"    ✓ Saved {len(transcript)} segments")
        return transcript
    except Exception as e:
        print(f"    ✗ Error: {e}")
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

def get_video_duration(video_path):
    try:
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
               "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return float(result.stdout.strip())
    except:
        return None

def main():
    print("=== CONTINUING ASR FOR BATCH 001 ===\n")
    
    # Load selection
    with open(SHARDS / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        selection = {row.get('aweme_id'): row for row in reader}
    
    # Find current samples in batch
    existing_samples = sorted(OUTPUT_DIR.glob("sample_*"))
    existing_ids = set()
    for s in existing_samples:
        meta = json.load(open(s / "01_metadata.json"))
        existing_ids.add(meta.get('content_id', ''))
    
    print(f"Existing samples: {len(existing_ids)}")
    
    # Find videos needing ASR
    videos_needing_asr = []
    for d in sorted(VIDEO_DIR.glob("*/")):
        cid = d.name
        if cid in existing_ids:
            continue
        
        video_path = d / "video.mp4"
        trans_file = TRANSCRIPT_DIR / f"{cid}_raw.json"
        
        if video_path.exists() and not trans_file.exists():
            if cid in selection:
                videos_needing_asr.append({
                    'id': cid,
                    'path': video_path,
                    'row': selection[cid],
                    'from_selection': True
                })
            else:
                videos_needing_asr.append({
                    'id': cid,
                    'path': video_path,
                    'row': None,
                    'from_selection': False
                })
    
    print(f"Videos needing ASR: {len(videos_needing_asr)}")
    print(f"Target: {10 - len(existing_ids)} more samples\n")
    
    # Run ASR on up to 7 videos
    target_count = min(7, len(videos_needing_asr))
    new_transcripts = []
    
    for i, item in enumerate(videos_needing_asr[:target_count], 1):
        cid = item['id']
        video_path = item['path']
        
        print(f"\n--- ASR {i}/{target_count}: {cid} ---")
        
        transcript = run_asr(video_path, TRANSCRIPT_DIR)
        
        if transcript:
            new_transcripts.append({
                'id': cid,
                'transcript': transcript,
                'row': item['row'],
                'from_selection': item['from_selection']
            })
    
    print(f"\n=== ASR COMPLETE ===")
    print(f"New transcripts: {len(new_transcripts)}")
    
    if len(new_transcripts) > 0:
        create_new_samples(new_transcripts, len(existing_samples) + 1)
    else:
        print("No new transcripts generated")

def create_new_samples(new_transcripts, start_id):
    """Create sample directories for new transcripts"""
    print("\n=== CREATING NEW SAMPLES ===\n")
    
    for i, item in enumerate(new_transcripts, start_id):
        cid = item['id']
        transcript = item['transcript']
        row = item['row']
        
        print(f"\n--- Sample {i}: {cid} ---")
        
        # Assign segment IDs
        for j, seg in enumerate(transcript):
            seg['segment_id'] = f"S{j+1:04d}"
        
        # Get duration
        video_path = VIDEO_DIR / cid / "video.mp4"
        duration = get_video_duration(video_path) or (transcript[-1]['end'] if transcript else 0)
        
        print(f"  Duration: {duration:.1f}s, Segments: {len(transcript)}")
        
        # Calculate metrics
        metrics = calculate_basic_metrics(transcript, duration)
        
        # Create sample dir
        sample_dir = OUTPUT_DIR / f"sample_{i:02d}"
        sample_dir.mkdir(parents=True, exist_ok=True)
        
        # Get metadata
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
        
        print(f"  ✓ Complete")
    
    # Generate final bundle
    generate_final_bundle()

def generate_final_bundle():
    """Generate BATCH_001_ANALYSIS_INPUT_V4.md"""
    samples = sorted(OUTPUT_DIR.glob("sample_*"))
    
    print(f"\n=== GENERATING FINAL BUNDLE ===\n")
    print(f"Total samples: {len(samples)}")
    
    if len(samples) < 10:
        print(f"⚠ Cannot generate V4 bundle - need 10 samples")
        return
    
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
    
    (OUTPUT_DIR / "BATCH_001_ANALYSIS_INPUT_V4.md").write_text('\n'.join(lines), encoding='utf-8')
    
    print(f"\n✓ Bundle V4 generated!")
    print(f"Size: {(OUTPUT_DIR / 'BATCH_001_ANALYSIS_INPUT_V4.md').stat().st_size} bytes")

if __name__ == "__main__":
    main()
