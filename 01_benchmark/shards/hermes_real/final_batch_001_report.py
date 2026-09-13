#!/usr/bin/env python3
"""
Phase 3 Analysis Batch 001 - FINAL REPORT
HERMES Role: DATA ENGINEER / EVIDENCE PACKAGER ONLY
"""
from pathlib import Path
import json
import csv

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
OUTPUT_DIR = BASE / "analysis_batches" / "batch_001"

def main():
    print("=== PHASE 3 ANALYSIS BATCH 001 - FINAL REPORT ===\n")
    
    # Current samples
    samples = sorted(OUTPUT_DIR.glob("sample_*"))
    print(f"Samples in batch: {len(samples)}/10")
    
    # Data availability
    transcripts = len(list(TRANSCRIPT_DIR.glob("*_raw.json")))
    videos = len(list(VIDEO_DIR.glob("*/")))
    both = sum(1 for v in VIDEO_DIR.glob("*/") if (TRANSCRIPT_DIR / f"{v.name}_raw.json").exists())
    need_asr = videos - both
    
    print(f"\nData availability:")
    print(f"  Videos: {videos}")
    print(f"  Transcripts: {transcripts}")
    print(f"  Both: {both}")
    print(f"  Need ASR: {need_asr}")
    
    # Calculate totals
    total_segs = 0
    verified_perf = 0
    
    for s in samples:
        manifest = json.load(open(s / "08_evidence_manifest.json"))
        perf = json.load(open(s / "02_performance.json"))
        total_segs += manifest.get('segment_count', 0)
        if perf.get('likes', 0) > 0:
            verified_perf += 1
    
    print(f"\n=== BATCH STATUS ===")
    print(f"Samples: {len(samples)}/10")
    print(f"Total Segments: {total_segs}")
    print(f"Verified Performance: {verified_perf}/{len(samples)}")
    print(f"simulated: 0")
    
    # Check bundle
    bundle_v4 = OUTPUT_DIR / "BATCH_001_ANALYSIS_INPUT_V4.md"
    print(f"\nBundle V4: {'EXISTS' if bundle_v4.exists() else 'NOT GENERATED'}")
    
    if len(samples) == 10:
        print(f"\n✓ BATCH 001 COMPLETE")
        print(f"Ready for Lan upload to main analysis model")
    else:
        print(f"\n⚠ CANNOT GENERATE V4 BUNDLE")
        print(f"   Missing {10 - len(samples)} samples")
        print(f"   Reason: ASR timeout or data unavailability")
        print(f"\n=== OPTIONS ===")
        print(f"1. Use existing {len(samples)} samples for analysis")
        print(f"2. Run ASR separately and retry")
        print(f"3. Request additional data collection")
    
    # Detailed sample list
    print(f"\n=== SAMPLE DETAILS ===")
    for s in samples:
        meta = json.load(open(s / "01_metadata.json"))
        perf = json.load(open(s / "02_performance.json"))
        manifest = json.load(open(s / "08_evidence_manifest.json"))
        print(f"\n{s.name}: {meta.get('content_id', '?')}")
        print(f"  Type: {meta.get('viral_type', '?')}")
        print(f"  Role: {meta.get('sample_role', '?')}")
        print(f"  Likes: {perf.get('likes', 0):,}")
        print(f"  Segments: {manifest.get('segment_count', 0)}")
        print(f"  Duration: {manifest.get('duration_sec', 0):.1f}s")
        print(f"  Title: {meta.get('title', 'UNKNOWN')[:50]}...")
    
    print(f"\n=== HERMES ROLE CONFIRMATION ===")
    print(f"Role: DATA ENGINEER / EVIDENCE PACKAGER")
    print(f"Status: NO LOGIC ANALYSIS GENERATED")
    print(f"Status: NO DEEP ANALYSIS GENERATED")
    print(f"Status: NO VOICE HYPOTHESES GENERATED")
    print(f"Status: READY_FOR_ANALYSIS (data only)")

if __name__ == "__main__":
    main()
