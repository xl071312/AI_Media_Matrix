#!/usr/bin/env python3
"""Process all pending ASR for Batch 002"""
import json
import subprocess
import time
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
MEDIA_DIR = BASE / "media" / "batch_002_smoke"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"
ASR_SCRIPT = SHARDS / "asr_rc3.py"

print("=== BATCH 002 ASR PROCESSING ===\n")

# Get audio files to process
audio_files = [p for p in MEDIA_DIR.glob('*.m4a') 
               if not any(x in p.name for x in ['76827', '76828', '76832'])]

print(f"Audio files to process: {len(audio_files)}\n")

results = []
for i, audio_path in enumerate(audio_files, 1):
    cid = audio_path.stem.replace('.audio', '')
    transcript_path = TRANSCRIPT_DIR / f'{cid}_raw.json'
    
    print(f"[{i}/{len(audio_files)}] {cid}")
    
    # Check if already done
    if transcript_path.exists():
        with open(transcript_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list) and len(data) > 0:
            segs = len(data)
            chars = sum(len(s.get('text', '')) for s in data)
            print(f"  ✓ Already processed: {segs} segs, {chars} chars")
            results.append({'cid': cid, 'status': 'DONE', 'segments': segs, 'chars': chars})
            continue
    
    # Run ASR
    try:
        result = subprocess.run(
            ['python', str(ASR_SCRIPT), str(audio_path), str(transcript_path)],
            capture_output=True, text=True, timeout=180
        )
        
        if transcript_path.exists():
            with open(transcript_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                segs = len(data)
                chars = sum(len(s.get('text', '')) for s in data)
                print(f"  ✓ ASR done: {segs} segs, {chars} chars")
                results.append({'cid': cid, 'status': 'DONE', 'segments': segs, 'chars': chars})
            else:
                print(f"  ✗ Empty result")
                results.append({'cid': cid, 'status': 'EMPTY'})
        else:
            print(f"  ✗ Failed")
            results.append({'cid': cid, 'status': 'FAILED'})
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        results.append({'cid': cid, 'status': f'ERROR'})
    
    # Brief delay
    time.sleep(0.5)

# Summary
done = len([r for r in results if r.get('status') == 'DONE'])
print(f"\n{'='*50}")
print(f"RESULTS: {done}/{len(results)} completed")

# Save
output = SHARDS / "batch002_asr_results.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"Saved to: {output}")