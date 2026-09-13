#!/usr/bin/env python3
"""
Phase 3 Analysis Evidence Repack - No ASR, Only Packaging
Split remaining samples into PART_02/03/04 with embedded transcripts
"""
import json
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
BATCH_DIR = BASE / "analysis_batches" / "batch_001"
REPACK_DIR = BATCH_DIR / "repack"
REPACK_DIR.mkdir(parents=True, exist_ok=True)

def main():
    print("=== EVIDENCE REPACK - NO ASR ===\n")
    
    # Load all samples
    samples = sorted(BATCH_DIR.glob("sample_*"))
    
    # Deduplicate by content_id, keep order
    seen_ids = set()
    unique_samples = []
    for s in samples:
        try:
            meta = json.load(open(s / "01_metadata.json"))
            cid = meta.get('content_id', '')
            if cid and cid not in seen_ids:
                seen_ids.add(cid)
                unique_samples.append(s)
        except:
            continue
    
    print(f"Total unique samples: {len(unique_samples)}")
    
    # Find which samples have complete data (01-08 files + transcript)
    complete_samples = []
    empty_transcript = []
    
    for s in unique_samples:
        manifest = json.load(open(s / "08_evidence_manifest.json")) if (s / "08_evidence_manifest.json").exists() else None
        if not manifest:
            continue
        
        seg_count = manifest.get('segment_count', 0)
        trans_file = s / "05_transcript_raw.md"
        
        if seg_count == 0 or not trans_file.exists():
            empty_transcript.append({
                'dir': s,
                'cid': manifest.get('content_id', ''),
                'seg_count': seg_count
            })
        else:
            # Check if transcript has content
            with open(trans_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Count [Sxxxx] lines
                import re
                segment_lines = len(re.findall(r'\[S\d{4}\]', content))
            
            if segment_lines > 0:
                complete_samples.append({
                    'dir': s,
                    'cid': manifest.get('content_id', ''),
                    'seg_count': seg_count,
                    'embedded_lines': segment_lines
                })
            else:
                empty_transcript.append({
                    'dir': s,
                    'cid': manifest.get('content_id', ''),
                    'seg_count': seg_count
                })
    
    print(f"Complete samples: {len(complete_samples)}")
    print(f"Empty transcripts: {len(empty_transcript)}")
    
    # First 6 samples already in V4 bundle (samples 1-6 from original)
    # Remaining samples go to PART_02/03/04
    # Find the starting index (skip first 6 which are in V4)
    start_index = 6  # 0-indexed, so skip first 6
    
    if start_index >= len(complete_samples):
        print("\nAll complete samples already in V4 bundle")
        return
    
    remaining = complete_samples[start_index:]
    print(f"Remaining to package: {len(remaining)}")
    
    # Split into groups of 6
    part_size = 6
    parts = []
    for i in range(0, len(remaining), part_size):
        parts.append(remaining[i:i+part_size])
    
    print(f"Will generate {len(parts)} parts\n")
    
    # Generate each part
    global_id = 7  # Start after first 6
    qa_results = []
    
    for part_idx, part_samples in enumerate(parts, 2):
        print(f"\n=== GENERATING PART_0{part_idx} ===")
        
        part_filename = f"BATCH001_EVIDENCE_PART_0{part_idx}.md"
        part_path = REPACK_DIR / part_filename
        
        lines = [
            "# Phase 3 Analysis Batch 001 - Evidence Part 0" + str(part_idx),
            "",
            f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')} GMT+8",
            f"**Part ID**: PART_0{part_idx}",
            f"**Total Samples in Part**: {len(part_samples)}",
            f"**HERMES Role**: DATA ENGINEER / EVIDENCE PACKAGER",
            f"**Status**: READY_FOR_ANALYSIS",
            "",
            "---",
            ""
        ]
        
        part_embedded = 0
        part_segments = 0
        part_failures = []
        
        for sample_info in part_samples:
            s = sample_info['dir']
            cid = sample_info['cid']
            declared_segs = sample_info['seg_count']
            
            # Read metadata
            meta = json.load(open(s / "01_metadata.json"))
            perf = json.load(open(s / "02_performance.json"))
            manifest = json.load(open(s / "08_evidence_manifest.json"))
            
            # Read transcript
            trans_file = s / "05_transcript_raw.md"
            with open(trans_file, 'r', encoding='utf-8') as f:
                transcript_content = f.read()
            
            # Extract transcript body (skip header)
            if "---" in transcript_content:
                parts_split = transcript_content.split("---", 1)
                if len(parts_split) > 1:
                    transcript_body = parts_split[1].strip()
                else:
                    transcript_body = transcript_content
            else:
                transcript_body = transcript_content
            
            # Count embedded segments
            import re
            embedded_lines = len(re.findall(r'\[S\d{4}\]', transcript_body))
            
            # QA check
            qa_pass = embedded_lines == declared_segs
            if not qa_pass:
                part_failures.append(f"{cid}: declared={declared_segs}, embedded={embedded_lines}")
            
            part_embedded += 1 if qa_pass else 0
            part_segments += embedded_lines
            
            # Add to bundle
            lines.append(f"## Sample B001-{global_id:03d}")
            lines.append("")
            lines.append(f"### Basic Info")
            lines.append(f"- **Analysis ID**: B001-{global_id:03d}")
            lines.append(f"- **Content ID**: {meta['content_id']}")
            lines.append(f"- **Title**: {meta.get('title', 'NULL')}")
            lines.append(f"- **Author**: {meta.get('creator_name', 'NULL')}")
            lines.append(f"- **Topic**: {meta.get('topic', 'NULL')}")
            lines.append(f"- **Sample Role**: {meta.get('sample_role', 'NULL')}")
            lines.append(f"- **Viral Type**: {meta.get('viral_type', 'NULL')}")
            lines.append("")
            lines.append(f"### Performance")
            for k in ['likes', 'comments', 'favorites', 'shares']:
                v = perf.get(k, 'NULL')
                if isinstance(v, int):
                    lines.append(f"- **{k.capitalize()}**: {v:,}")
                else:
                    lines.append(f"- **{k.capitalize()}**: {v}")
            lines.append("")
            lines.append(f"### Video Duration")
            lines.append(f"- **Duration**: {manifest['duration_sec']}s")
            lines.append("")
            lines.append(f"### Evidence Manifest")
            lines.append(f"- **Media SHA256**: {manifest['media_sha256']}")
            lines.append(f"- **Transcript SHA256**: {manifest['transcript_sha256']}")
            lines.append(f"- **Declared Segment Count**: {manifest['segment_count']}")
            lines.append(f"- **Embedded Segment Lines**: {embedded_lines}")
            lines.append(f"- **QA Status**: {'PASS' if qa_pass else 'FAIL'}")
            lines.append("")
            lines.append(f"### Raw Timed Transcript")
            lines.append(f"")
            lines.append(f"**Status**: UNVERIFIED_RAW_ASR")
            lines.append(f"**Note**: Complete transcript embedded below.")
            lines.append(f"")
            lines.append(transcript_body)
            lines.append("")
            lines.append("---")
            lines.append("")
            
            global_id += 1
        
        # Part summary
        lines.append(f"# Part 0{part_idx} Summary")
        lines.append("")
        lines.append(f"| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Total Samples | {len(part_samples)} |")
        lines.append(f"| Embedded Samples | {part_embedded} |")
        lines.append(f"| Total Segments | {part_segments} |")
        if part_failures:
            lines.append(f"| QA Failures | {len(part_failures)} |")
            for f in part_failures:
                lines.append(f"- {f}")
        else:
            lines.append(f"| QA Failures | 0 |")
        lines.append(f"| PACKAGING_QA | {'PASS' if not part_failures else 'FAIL'} |")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(f"*Generated by HERMES as DATA ENGINEER / EVIDENCE PACKAGER*")
        lines.append(f"*No Logic Analysis, Deep Analysis, or Voice Hypotheses generated*")
        lines.append(f"*Status: READY_FOR_ANALYSIS*")
        
        # Write part file
        part_path.write_text('\n'.join(lines), encoding='utf-8')
        
        qa_results.append({
            'part': part_idx,
            'total': len(part_samples),
            'embedded': part_embedded,
            'segments': part_segments,
            'failures': len(part_failures),
            'qa_pass': not part_failures
        })
        
        print(f"  ✓ {part_filename}: {part_embedded}/{len(part_samples)} embedded, {part_segments} segments")
        if part_failures:
            print(f"  ⚠ QA failures: {part_failures}")
    
    # Generate MANIFEST.csv
    print(f"\n=== GENERATING MANIFEST ===")
    
    manifest_rows = []
    for i, sample_info in enumerate(unique_samples, 1):
        s = sample_info['dir']
        cid = sample_info['cid']
        manifest = json.load(open(s / "08_evidence_manifest.json"))
        meta = json.load(open(s / "01_metadata.json"))
        perf = json.load(open(s / "02_performance.json"))
        
        # Check if transcript is complete
        trans_file = s / "05_transcript_raw.md"
        transcript_complete = False
        if trans_file.exists():
            with open(trans_file, 'r', encoding='utf-8') as f:
                content = f.read()
                import re
                seg_count = len(re.findall(r'\[S\d{4}\]', content))
                transcript_complete = seg_count > 0
        
        manifest_rows.append({
            'analysis_id': f'B001-{i:03d}',
            'content_id': cid,
            'viral_type': meta.get('viral_type', 'NULL'),
            'sample_role': meta.get('sample_role', 'NULL'),
            'duration_sec': manifest.get('duration_sec', 0),
            'segment_count': manifest.get('segment_count', 0),
            'media_sha256': manifest.get('media_sha256', ''),
            'transcript_sha256': manifest.get('transcript_sha256', ''),
            'likes': perf.get('likes', 'NULL'),
            'transcript_complete': transcript_complete,
            'packaging_status': 'COMPLETE' if transcript_complete else 'INCOMPLETE'
        })
    
    # Write CSV
    csv_path = REPACK_DIR / "BATCH001_EVIDENCE_MANIFEST.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'analysis_id', 'content_id', 'viral_type', 'sample_role',
            'duration_sec', 'segment_count', 'media_sha256', 'transcript_sha256',
            'likes', 'transcript_complete', 'packaging_status'
        ])
        writer.writeheader()
        writer.writerows(manifest_rows)
    
    print(f"  ✓ {csv_path}")
    
    # Final report
    print(f"\n=== FINAL REPORT ===")
    print(f"PART_02: {qa_results[0]['embedded']}/{qa_results[0]['total']} embedded, {qa_results[0]['segments']} segments")
    print(f"PART_03: {qa_results[1]['embedded']}/{qa_results[1]['total']} embedded, {qa_results[1]['segments']} segments")
    print(f"PART_04: {qa_results[2]['embedded']}/{qa_results[2]['total']} embedded, {qa_results[2]['segments']} segments")
    print(f"TRANSCRIPT_EMPTY: {len(empty_transcript)}")
    print(f"PACKAGING_QA: {'PASS' if all(r['qa_pass'] for r in qa_results) else 'FAIL'}")
    print(f"\nOutput directory: {REPACK_DIR}")

if __name__ == "__main__":
    main()
