#!/usr/bin/env python3
"""Consolidate Batch 001 into single folder"""
from pathlib import Path
import shutil
import csv
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
BATCH = BASE / "analysis_batches" / "batch_001"
REPACK = BATCH / "repack"
OUTPUT = BATCH / "BATCH_001_FINAL"
OUTPUT.mkdir(parents=True, exist_ok=True)

def main():
    print("=== CONSOLIDATING BATCH 001 ===\n")
    
    # Copy Evidence V4
    v4 = BATCH / "BATCH_001_ANALYSIS_INPUT_V4.md"
    if v4.exists():
        shutil.copy2(v4, OUTPUT / "BATCH_001_EVIDENCE_PART_01.md")
        print(f"  ✓ BATCH_001_EVIDENCE_PART_01.md")
    
    # Copy Parts 02-04
    for i in [2, 3, 4]:
        p = REPACK / f"BATCH001_EVIDENCE_PART_0{i}.md"
        if p.exists():
            shutil.copy2(p, OUTPUT / f"BATCH_001_EVIDENCE_PART_0{i}.md")
            print(f"  ✓ BATCH_001_EVIDENCE_PART_0{i}.md")
    
    # Copy Manifest
    manifest = BATCH / "CORPUS_CANONICAL_MANIFEST_V1_1.csv"
    if manifest.exists():
        shutil.copy2(manifest, OUTPUT / "CORPUS_CANONICAL_MANIFEST_V1_1.csv")
        print(f"  ✓ CORPUS_CANONICAL_MANIFEST_V1_1.csv")
    
    # Copy Freeze Status
    freeze = BATCH / "BATCH_001_CORPUS_STATUS.txt"
    if freeze.exists():
        shutil.copy2(freeze, OUTPUT / "BATCH_001_CORPUS_STATUS.txt")
        print(f"  ✓ BATCH_001_CORPUS_STATUS.txt")
    
    # Generate summary
    summary = []
    summary.append("# Phase 3 Analysis Batch 001 - Final Deliverable")
    summary.append("")
    summary.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')} GMT+8")
    summary.append(f"**Status**: FROZEN_FOR_LOGIC_RESEARCH")
    summary.append("")
    summary.append("---")
    summary.append("")
    
    # Read manifest stats
    with open(manifest, encoding='utf-8') as f:
        rows = list(csv.DictReader(f)) if manifest.exists() else []
    
    analyzable = sum(1 for r in rows if r.get('logic_analyzable') == 'TRUE')
    verified = sum(1 for r in rows if r.get('performance_verified') == 'TRUE')
    excluded = sum(1 for r in rows if r.get('logic_analyzable') == 'FALSE')
    
    summary.append("## Corpus Summary")
    summary.append("")
    summary.append("| Metric | Value |")
    summary.append("|--------|-------|")
    summary.append(f"| Total Samples | {len(rows)} |")
    summary.append(f"| Logic Analyzable | {analyzable} |")
    summary.append(f"| Verified Performance | {verified} |")
    summary.append(f"| Excluded | {excluded} |")
    summary.append(f"| Near Duplicate Groups | 1 |")
    summary.append("")
    summary.append("## Deliverable Files")
    summary.append("")
    summary.append("1. BATCH_001_EVIDENCE_PART_01.md - Evidence V4 (Samples 1-6)")
    summary.append("2. BATCH_001_EVIDENCE_PART_02.md - Evidence Part 2 (Samples 7-12)")
    summary.append("3. BATCH_001_EVIDENCE_PART_03.md - Evidence Part 3 (Samples 13-18)")
    summary.append("4. BATCH_001_EVIDENCE_PART_04.md - Evidence Part 4 (Samples 19-24)")
    summary.append("5. CORPUS_CANONICAL_MANIFEST_V1_1.csv - Canonical Manifest")
    summary.append("6. BATCH_001_CORPUS_STATUS.txt - Freeze Status")
    summary.append("")
    summary.append("---")
    summary.append("")
    summary.append("*HERMES Role: DATA ENGINEER / EVIDENCE PACKAGER*")
    summary.append("*No Logic Analysis, Deep Analysis, or Voice Hypotheses generated*")
    
    (OUTPUT / "README.md").write_text('\n'.join(summary), encoding='utf-8')
    print(f"  ✓ README.md")
    
    # List final files
    print(f"\n=== FINAL OUTPUT ===")
    print(f"Folder: {OUTPUT}")
    for f in sorted(OUTPUT.iterdir()):
        if f.is_file():
            print(f"  {f.name}: {f.stat().st_size} bytes")
    
    print(f"\nStatus: FROZEN_FOR_LOGIC_RESEARCH")
    print(f"Total files: {len(list(OUTPUT.iterdir()))}")

if __name__ == "__main__":
    main()
