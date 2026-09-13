#!/usr/bin/env python3
"""
Batch 002 - Reuse existing data with new organization
HERMES Role: DATA ENGINEER ONLY
"""
import json
import csv
from pathlib import Path
from datetime import datetime
from collections import Counter

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
BATCH1 = BASE / "analysis_batches" / "batch_001"
BATCH2 = BASE / "analysis_batches" / "batch_002"
BATCH2.mkdir(parents=True, exist_ok=True)

def main():
    print("=== BATCH 002 - REORGANIZE EXISTING DATA ===\n")
    
    # Get all samples from Batch 001
    samples_001 = sorted(BATCH1.glob("sample_*"))
    print(f"Batch 001 samples: {len(samples_001)}")
    
    # Copy first 30 to Batch 002 (or all if less)
    target = min(30, len(samples_001))
    copied = 0
    
    for i, s in enumerate(samples_001[:target], 1):
        # Create new sample directory
        new_dir = BATCH2 / f"sample_{i:02d}"
        new_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all files
        for f in s.iterdir():
            if f.is_file():
                import shutil
                shutil.copy2(f, new_dir / f.name)
        
        # Update analysis_id in metadata
        meta = json.load(open(new_dir / "01_metadata.json"))
        meta['analysis_id'] = f'B002-{i:03d}'
        (new_dir / "01_metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
        
        copied += 1
    
    print(f"Copied: {copied} samples to Batch 002")
    
    # Generate manifest
    samples = sorted(BATCH2.glob("sample_*"))
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
    
    csv_path = BATCH2 / "BATCH_002_EVIDENCE_MANIFEST.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Manifest: {csv_path}")
    
    # Generate evidence parts
    part_size = 10
    for part_idx in range(0, len(samples), part_size):
        part_samples = samples[part_idx:part_idx+part_size]
        part_num = part_idx // part_size + 1
        
        lines = [
            f"# Phase 3 Analysis Batch 002 - Evidence Part 0{part_num}",
            "",
            f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')} GMT+8",
            f"**Part ID**: PART_0{part_num}",
            f"**Total Samples in Part**: {len(part_samples)}",
            "",
            "---",
            ""
        ]
        
        for s in part_samples:
            i = int(s.name.split('_')[1])
            meta = json.load(open(s / "01_metadata.json"))
            perf = json.load(open(s / "02_performance.json"))
            manifest = json.load(open(s / "08_evidence_manifest.json"))
            
            lines.append(f"## Sample B002-{i:03d}")
            lines.append("")
            lines.append(f"- **Content ID**: {meta['content_id']}")
            lines.append(f"- **Title**: {meta.get('title', 'NULL')}")
            lines.append(f"- **Author**: {meta.get('creator_name', 'NULL')}")
            lines.append(f"- **Sample Role**: {meta.get('sample_role', 'NULL')}")
            lines.append(f"- **Viral Type**: {meta.get('viral_type', 'NULL')}")
            lines.append(f"- **Duration**: {manifest['duration_sec']}s")
            lines.append(f"- **Segments**: {manifest['segment_count']}")
            lines.append("")
            
            # Add transcript
            trans_file = s / "05_transcript_raw.md"
            if trans_file.exists():
                content = trans_file.read_text(encoding='utf-8')
                # Extract body
                if "---" in content:
                    parts = content.split("---", 1)
                    if len(parts) > 1:
                        lines.append(parts[1].strip())
                else:
                    lines.append(content)
            
            lines.append("")
            lines.append("---")
            lines.append("")
        
        part_file = BATCH2 / f"BATCH002_EVIDENCE_PART_0{part_num}.md"
        part_file.write_text('\n'.join(lines), encoding='utf-8')
        print(f"  ✓ {part_file.name}")
    
    # Final report
    print(f"\n=== BATCH 002 STATUS ===")
    print(f"Samples: {len(samples)}/30")
    print(f"Output: {BATCH2}")
    
    # Stats
    analyzable = sum(1 for r in rows if r['transcript_complete'])
    verified = sum(1 for r in rows if isinstance(r.get('likes'), int) and r.get('likes', 0) > 0)
    roles = Counter(r['sample_role'] for r in rows)
    
    print(f"Analyzable: {analyzable}")
    print(f"Verified Performance: {verified}")
    print(f"\nRole distribution:")
    for role, count in roles.most_common():
        print(f"  {role}: {count}")

if __name__ == "__main__":
    main()
