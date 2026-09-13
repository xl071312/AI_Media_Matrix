#!/usr/bin/env python3
"""Fix transcript markdown files for samples 7-25"""
import json
from pathlib import Path

BATCH = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\analysis_batches\batch_001")
TRANSCRIPT_DIR = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real\transcripts_v2")

def main():
    print("=== FIXING TRANSCRIPT MARKDOWN FILES ===\n")
    
    # Find samples without proper transcript markdown
    for s in sorted(BATCH.glob("sample_*")):
        # Check if sample_07 or higher
        num = int(s.name.split('_')[1])
        if num <= 6:
            continue
        
        # Read raw transcript
        trans_raw = s / "04_transcript_raw.json"
        if not trans_raw.exists():
            continue
        
        with open(trans_raw, 'r', encoding='utf-8') as f:
            transcript = json.load(f)
        
        if not transcript:
            continue
        
        # Assign segment IDs
        for j, seg in enumerate(transcript):
            seg['segment_id'] = f"S{j+1:04d}"
        
        # Get content_id
        meta = json.load(open(s / "01_metadata.json"))
        cid = meta.get('content_id', '')
        
        # Generate proper markdown
        lines = [f"# Raw Transcript: {cid}", "", 
                 f"**Source**: ASR Raw Output",
                 f"**Status**: UNVERIFIED_RAW_ASR",
                 f"**Note**: Complete transcript embedded. Awaiting manual quality check.",
                 "", "---", ""]
        
        for seg in transcript:
            start_min = int(seg['start'] // 60)
            start_sec = seg['start'] % 60
            end_min = int(seg['end'] // 60)
            end_sec = seg['end'] % 60
            lines.append(f"[{seg['segment_id']}] [{start_min:02d}:{start_sec:05.2f}-{end_min:02d}:{end_sec:05.2f}] {seg['text']}")
        
        # Write markdown
        trans_md = s / "05_transcript_raw.md"
        trans_md.write_text('\n'.join(lines), encoding='utf-8')
        
        print(f"  ✓ {s.name}: {len(transcript)} segments fixed")
    
    print(f"\n=== DONE ===")

if __name__ == "__main__":
    main()
