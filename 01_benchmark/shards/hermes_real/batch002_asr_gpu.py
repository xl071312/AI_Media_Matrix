#!/usr/bin/env python3
"""Batch 002 - ASR with GPU acceleration"""
import json
import time
from pathlib import Path
from faster_whisper import WhisperModel

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
MEDIA_DIR = BASE / "media" / "batch_002_smoke"
TRANSCRIPT_DIR = BASE / "shards" / "hermes_real" / "transcripts_v2"

# Get audio files
audio_files = [p for p in MEDIA_DIR.glob('*.m4a') 
               if not any(x in p.name for x in ['76827', '76828', '76832'])]

print(f"=== BATCH 002 ASR (GPU) ===")
print(f"Audio files: {len(audio_files)}")
print(f"GPU: CUDA available\n")

# Load model once
print("Loading model...")
start = time.time()
model = WhisperModel('Systran/faster-whisper-tiny', device='cuda', compute_type='float16')
print(f"Model loaded in {time.time()-start:.1f}s\n")

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
            print(f"  ✓ Already done: {len(data)} segments")
            results.append({'cid': cid, 'status': 'DONE', 'segments': len(data)})
            continue
    
    # Transcribe
    try:
        start = time.time()
        segments, info = model.transcribe(str(audio_path), beam_size=3, language='zh')
        segs = list(segments)
        elapsed = time.time() - start
        
        # Save
        transcript = [{'start': round(s.start, 2), 'end': round(s.end, 2), 'text': s.text.strip()} for s in segs]
        transcript_path.write_text(json.dumps(transcript, ensure_ascii=False, indent=2), encoding='utf-8')
        
        chars = sum(len(s['text']) for s in transcript)
        print(f"  ✓ Done: {len(segs)} segments, {chars} chars ({elapsed:.1f}s)")
        results.append({'cid': cid, 'status': 'DONE', 'segments': len(segs), 'chars': chars, 'time': elapsed})
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        results.append({'cid': cid, 'status': 'FAILED'})
    
    time.sleep(0.5)

# Summary
done = len([r for r in results if r.get('status') == 'DONE'])
print(f"\n{'='*50}")
print(f"RESULTS: {done}/{len(results)} completed")

# Save
output = TRANSCRIPT_DIR / "batch002_asr_gpu_results.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"Saved to: {output}")