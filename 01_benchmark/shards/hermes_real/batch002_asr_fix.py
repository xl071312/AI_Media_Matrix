#!/usr/bin/env python3
"""Batch 002 - Fix ASR processing with correct API"""
import json
import time
import subprocess
from pathlib import Path
from faster_whisper import WhisperModel

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
MEDIA_DIR = BASE / "media" / "batch_002_smoke"
TRANSCRIPT_DIR = BASE / "shards" / "hermes_real" / "transcripts_v2"

# Get all audio files
all_audio = [p.stem.replace('.audio', '') for p in MEDIA_DIR.glob('*.m4a') 
             if not any(x in p.name for x in ['76827', '76828', '76832'])]

print(f"=== BATCH 002 ASR FIX ===")
print(f"Total audio files: {len(all_audio)}")
print()

# Load model once
model = WhisperModel('Systran/faster-whisper-tiny', device='cpu', compute_type='int8')
print("Model loaded\n")

results = []
for i, cid in enumerate(sorted(all_audio), 1):
    audio_path = MEDIA_DIR / f'{cid}.audio.m4a'
    transcript_path = TRANSCRIPT_DIR / f'{cid}_raw.json'
    
    # Skip if already done
    if transcript_path.exists():
        with open(transcript_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list) and len(data) > 0:
            print(f"[{i}/{len(all_audio)}] {cid} - SKIP (already done)")
            results.append({'cid': cid, 'status': 'DONE', 'segments': len(data)})
            continue
    
    print(f"[{i}/{len(all_audio)}] {cid} - Processing...")
    
    # Get duration
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)],
            capture_output=True, text=True, timeout=10
        )
        duration = float(result.stdout.strip())
    except:
        duration = 0
    
    print(f"  Duration: {duration:.1f}s")
    
    # Transcribe whole file (no offset)
    try:
        segs, info = model.transcribe(str(audio_path), beam_size=1, language='zh', vad_filter=True)
        all_segs = list(segs)
        
        # Save
        transcript = [{'start': round(s.start, 2), 'end': round(s.end, 2), 'text': s.text.strip()} for s in all_segs]
        transcript_path.write_text(json.dumps(transcript, ensure_ascii=False, indent=2), encoding='utf-8')
        
        chars = sum(len(s['text']) for s in transcript)
        print(f"  ✓ Done: {len(all_segs)} segs, {chars} chars")
        results.append({'cid': cid, 'status': 'DONE', 'segments': len(all_segs), 'chars': chars})
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        results.append({'cid': cid, 'status': 'FAILED', 'error': str(e)})
    
    time.sleep(0.5)

# Summary
done = len([r for r in results if r.get('status') == 'DONE'])
print(f"\n{'='*50}")
print(f"ASR complete: {done}/{len(all_audio)}")