#!/usr/bin/env python3
"""Generate BATCH_001_ANALYSIS_INPUT_V4.md"""
import json
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\analysis_batches\batch_001")

def main():
    samples = sorted(OUTPUT_DIR.glob("sample_*"))
    
    if len(samples) < 6:
        print(f"Need at least 6 samples, have {len(samples)}")
        return
    
    print(f"=== GENERATING V4 BUNDLE ===\n")
    print(f"Samples: {len(samples)}")
    
    # Calculate totals
    total_segments = 0
    total_duration = 0
    verified_perf = 0
    
    for s in samples:
        manifest = json.load(open(s / "08_evidence_manifest.json"))
        perf = json.load(open(s / "02_performance.json"))
        total_segments += manifest.get('segment_count', 0)
        total_duration += manifest.get('duration_sec', 0)
        likes = perf.get('likes', 0)
        if isinstance(likes, int) and likes > 0:
            verified_perf += 1
    
    lines = [
        "# Phase 3 Analysis Batch 001 - Complete Evidence Input V4",
        "",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')} GMT+8",
        f"**Batch ID**: BATCH_001",
        f"**Total Samples**: {len(samples)}",
        f"**Total Segments**: {total_segments}",
        f"**Total Duration**: {total_duration:.1f}s",
        f"**Verified Performance**: {verified_perf}/{len(samples)}",
        f"**HERMES Role**: DATA ENGINEER / EVIDENCE PACKAGER",
        f"**Status**: READY_FOR_ANALYSIS (PARTIAL)",
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
        lines.append(f"- **Title**: {meta.get('title', 'NULL')}")
        lines.append(f"- **Author**: {meta.get('creator_name', 'NULL')}")
        lines.append(f"- **Topic**: {meta.get('topic', 'NULL')}")
        lines.append(f"- **Sample Role**: {meta.get('sample_role', 'NULL')}")
        lines.append(f"- **Viral Type**: {meta.get('viral_type', 'NULL')}")
        lines.append("")
        lines.append(f"### Performance")
        likes = perf.get('likes', 'NULL')
        comments = perf.get('comments', 'NULL')
        favorites = perf.get('favorites', 'NULL')
        shares = perf.get('shares', 'NULL')
        lines.append(f"- **Likes**: {likes:,}" if isinstance(likes, int) else f"- **Likes**: {likes}")
        lines.append(f"- **Comments**: {comments:,}" if isinstance(comments, int) else f"- **Comments**: {comments}")
        lines.append(f"- **Favorites**: {favorites:,}" if isinstance(favorites, int) else f"- **Favorites**: {favorites}")
        lines.append(f"- **Shares**: {shares:,}" if isinstance(shares, int) else f"- **Shares**: {shares}")
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
    lines.append(f"| Verified Performance | {verified_perf}/{len(samples)} |")
    
    viral_counts = {}
    for s in samples:
        meta = json.load(open(s / "01_metadata.json"))
        vt = meta.get('viral_type', 'NULL')
        viral_counts[vt] = viral_counts.get(vt, 0) + 1
    
    lines.append(f"| Viral Type Distribution |")
    for vt, count in sorted(viral_counts.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {vt} | {count} |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*Generated by HERMES as DATA ENGINEER / EVIDENCE PACKAGER*")
    lines.append(f"*No Logic Analysis, Deep Analysis, or Voice Hypotheses generated*")
    lines.append(f"*Status: READY_FOR_ANALYSIS (PARTIAL)*")
    lines.append(f"*Data Engineering Applied:*")
    lines.append(f"  - ASR completed for all available videos")
    lines.append(f"  - Metadata restored where available")
    lines.append(f"  - NULL used for missing performance data")
    lines.append(f"  - Correct segment count aggregation")
    
    output = OUTPUT_DIR / "BATCH_001_ANALYSIS_INPUT_V4.md"
    output.write_text('\n'.join(lines), encoding='utf-8')
    
    print(f"\n✓ Bundle V4 generated!")
    print(f"Size: {output.stat().st_size} bytes")
    print(f"\n=== VALIDATION ===")
    print(f"Total Samples: {len(samples)}")
    print(f"Total Segments: {total_segments}")
    print(f"Verified Performance: {verified_perf}/{len(samples)}")

if __name__ == "__main__":
    main()
