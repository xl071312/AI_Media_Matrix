#!/usr/bin/env python3
"""Repack evidence with proper handling of all samples"""
import json
from pathlib import Path
from datetime import datetime
import re

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
BATCH_DIR = BASE / "analysis_batches" / "batch_001"
REPACK_DIR = BATCH_DIR / "repack"
REPACK_DIR.mkdir(parents=True, exist_ok=True)

def main():
    print("=== EVIDENCE REPACK ===\n")
    
    # Get all samples
    samples = sorted(BATCH_DIR.glob("sample_*"))
    
    # Build complete sample list with proper IDs
    all_samples = []
    for s in samples:
        try:
            meta = json.load(open(s / "01_metadata.json"))
            manifest = json.load(open(s / "08_evidence_manifest.json"))
            perf = json.load(open(s / "02_performance.json"))
            
            cid = meta.get('content_id', '')
            if not cid:
                continue
            
            # Check transcript completeness
            trans_file = s / "05_transcript_raw.md"
            embedded_segs = 0
            if trans_file.exists():
                with open(trans_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    embedded_segs = len(re.findall(r'\[S\d{4}\]', content))
            
            all_samples.append({
                'dir': s,
                'id': s.name,
                'cid': cid,
                'meta': meta,
                'manifest': manifest,
                'perf': perf,
                'declared_segs': manifest.get('segment_count', 0),
                'embedded_segs': embedded_segs,
                'transcript_complete': embedded_segs == manifest.get('segment_count', 0) and manifest.get('segment_count', 0) > 0
            })
        except Exception as e:
            print(f"  Error processing {s.name}: {e}")
    
    # Sort by embedded_segs (complete first)
    all_samples.sort(key=lambda x: (-x['embedded_segs'], x['cid']))
    
    # Separate into complete and incomplete
    complete = [s for s in all_samples if s['transcript_complete']]
    incomplete = [s for s in all_samples if not s['transcript_complete']]
    
    print(f"Total samples: {len(all_samples)}")
    print(f"Complete (transcript embedded): {len(complete)}")
    print(f"Incomplete (transcript empty or mismatched): {len(incomplete)}\n")
    
    # First 6 go to V4 bundle (already done)
    # Remaining go to PART_02/03/04
    # Start from index 6
    remaining = [s for s in complete if s['cid'] not in [
        '7546212425998454074', '7647797848847439706', '7302348364815928612',
        '7378948118584282394', '7525683513706810682', '7543846940678589723'
    ]]
    
    print(f"Samples for repack: {len(remaining)}\n")
    
    # Split into parts of 6
    part_size = 6
    parts = []
    for i in range(0, len(remaining), part_size):
        parts.append(remaining[i:i+part_size])
    
    qa_results = []
    global_id = 7
    
    for part_idx, part_samples in enumerate(parts, 2):
        print(f"=== GENERATING PART_0{part_idx} ===")
        
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
            declared_segs = sample_info['declared_segs']
            embedded_segs = sample_info['embedded_segs']
            
            meta = sample_info['meta']
            perf = sample_info['perf']
            manifest = sample_info['manifest']
            
            # Read transcript
            trans_file = s / "05_transcript_raw.md"
            transcript_body = ""
            if trans_file.exists():
                with open(trans_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract body after ---
                    if "---" in content:
                        parts_split = content.split("---", 1)
                        if len(parts_split) > 1:
                            transcript_body = parts_split[1].strip()
                        else:
                            transcript_body = content
                    else:
                        transcript_body = content
            
            # QA check
            qa_pass = embedded_segs == declared_segs and declared_segs > 0
            if not qa_pass:
                part_failures.append(f"{cid}: declared={declared_segs}, embedded={embedded_segs}")
            
            part_embedded += 1 if qa_pass else 0
            part_segments += embedded_segs
            
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
            lines.append(f"- **Embedded Segment Lines**: {embedded_segs}")
            lines.append(f"- **QA Status**: {'PASS' if qa_pass else 'FAIL'}")
            lines.append("")
            lines.append(f"### Raw Timed Transcript")
            lines.append(f"")
            lines.append(f"**Status**: {'UNVERIFIED_RAW_ASR' if qa_pass else 'TRANSCRIPT_EMPTY'}")
            lines.append(f"**Note**: Complete transcript embedded below." if qa_pass else "**Note**: Transcript missing or incomplete.")
            lines.append(f"")
            
            if qa_pass and transcript_body:
                lines.append(transcript_body)
            else:
                lines.append("*TRANSCRIPT_EMPTY - No embedded transcript*")
            
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
            print(f"  ⚠ QA failures: {len(part_failures)}")
    
    # Generate MANIFEST.csv
    print(f"\n=== GENERATING MANIFEST ===")
    
    manifest_rows = []
    for i, sample_info in enumerate(all_samples, 1):
        manifest_rows.append({
            'analysis_id': f'B001-{i:03d}',
            'content_id': sample_info['cid'],
            'viral_type': sample_info['meta'].get('viral_type', 'NULL'),
            'sample_role': sample_info['meta'].get('sample_role', 'NULL'),
            'duration_sec': sample_info['manifest'].get('duration_sec', 0),
            'segment_count': sample_info['manifest'].get('segment_count', 0),
            'media_sha256': sample_info['manifest'].get('media_sha256', ''),
            'transcript_sha256': sample_info['manifest'].get('transcript_sha256', ''),
            'likes': sample_info['perf'].get('likes', 'NULL'),
            'transcript_complete': sample_info['transcript_complete'],
            'packaging_status': 'COMPLETE' if sample_info['transcript_complete'] else 'INCOMPLETE'
        })
    
    import csv
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
    if len(qa_results) >= 3:
        print(f"PART_02: {qa_results[0]['embedded']}/{qa_results[0]['total']} embedded, {qa_results[0]['segments']} segments")
        print(f"PART_03: {qa_results[1]['embedded']}/{qa_results[1]['total']} embedded, {qa_results[1]['segments']} segments")
        print(f"PART_04: {qa_results[2]['embedded']}/{qa_results[2]['total']} embedded, {qa_results[2]['segments']} segments")
    elif len(qa_results) == 2:
        print(f"PART_02: {qa_results[0]['embedded']}/{qa_results[0]['total']} embedded, {qa_results[0]['segments']} segments")
        print(f"PART_03: {qa_results[1]['embedded']}/{qa_results[1]['total']} embedded, {qa_results[1]['segments']} segments")
        print(f"PART_04: 0/0 embedded, 0 segments")
    elif len(qa_results) == 1:
        print(f"PART_02: {qa_results[0]['embedded']}/{qa_results[0]['total']} embedded, {qa_results[0]['segments']} segments")
        print(f"PART_03: 0/0 embedded, 0 segments")
        print(f"PART_04: 0/0 embedded, 0 segments")
    
    transcript_empty = sum(1 for s in all_samples if not s['transcript_complete'])
    print(f"TRANSCRIPT_EMPTY: {transcript_empty}")
    
    all_qa_pass = all(r['qa_pass'] for r in qa_results) if qa_results else False
    print(f"PACKAGING_QA: {'PASS' if all_qa_pass else 'FAIL'}")
    print(f"\nOutput: {REPACK_DIR}")

if __name__ == "__main__":
    main()
