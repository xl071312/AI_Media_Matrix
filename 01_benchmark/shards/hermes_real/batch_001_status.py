#!/usr/bin/env python3
"""
Phase 3 Analysis Batch 001 - Final Status with ASR Options
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
    print("=== PHASE 3 ANALYSIS BATCH 001 - FINAL STATUS ===\n")
    
    # Current samples
    samples = sorted(OUTPUT_DIR.glob("sample_*"))
    print(f"Current samples: {len(samples)}")
    
    # Available data
    transcripts = len(list(TRANSCRIPT_DIR.glob("*_raw.json")))
    videos = len(list(VIDEO_DIR.glob("*/")))
    both = sum(1 for v in VIDEO_DIR.glob("*/") if (TRANSCRIPT_DIR / f"{v.name}_raw.json").exists())
    need_asr = videos - both
    
    print(f"\nData availability:")
    print(f"  Videos: {videos}")
    print(f"  Transcripts: {transcripts}")
    print(f"  Both: {both}")
    print(f"  Need ASR: {need_asr}")
    
    print(f"\n=== CURRENT BATCH STATUS ===")
    print(f"Samples: {len(samples)}/10")
    print(f"Gap: {10 - len(samples)} samples needed")
    
    print(f"\n=== OPTIONS ===")
    print(f"1. Use existing 3 samples (READY_FOR_ANALYSIS)")
    print(f"2. Run ASR on {need_asr} videos to get more samples")
    print(f"3. Request additional data collection")
    
    # Check if faster-whisper is available
    try:
        import whisper
        print(f"\nwhisper available: YES")
    except:
        print(f"\nwhisper available: NO")
    
    try:
        from faster_whisper import WhisperModel
        print(f"faster-whisper available: YES")
    except:
        print(f"faster-whisper available: NO")
    
    print(f"\n=== RECOMMENDATION ===")
    print(f"Run ASR on {min(need_asr, 7)} videos to reach 10 samples")
    print(f"This will generate raw transcripts for additional samples")

if __name__ == "__main__":
    main()
