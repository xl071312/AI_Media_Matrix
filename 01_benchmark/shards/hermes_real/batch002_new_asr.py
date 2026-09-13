#!/usr/bin/env python3
"""Batch 002 - Run ASR on newly downloaded audios"""
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from faster_whisper import WhisperModel

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
MEDIA_DIR = BASE / "media" / "batch_002_smoke"
TRANSCRIPT_DIR = BASE / "shards" / "hermes_real" / "transcripts_v2"
ASR_TEMP = BASE / "shards" / "hermes_real" / "asr_temp"

ASR_TEMP.mkdir(parents=True, exist_ok=True)

# Get newly downloaded audio files (not in first 12)
existing_cids = {'7441108716197301519', '7477191872570477839', '7511664213547519243',
                 '7559914938827803950', '7564348993203948810', '7584407684042165541',
                 '7592567871297932582', '7599188562650734516', '7600369823520073126',
                 '7647446230122356665', '7666798588350065338', '7673172635974421760'}

new_audio_files = []
for audio_path in MEDIA_DIR.glob('*.m4a'):
    cid = audio_path.stem.replace('.audio', '')
    if cid not in existing_cids and not any(x in cid for x in ['76827', '76828', '76832']):
        new_audio_files.append((cid, audio_path))

print(f"=== BATCH 002 NEW ASR ===")
print(f"New audio files: {len(new_audio_files)}")
print()

# Load model once
print("Loading model...")
model = WhisperModel('Systran/faster-whisper-tiny', device='cpu', compute_type='int8')
print("Model loaded\n")

results = []
for i, (cid, audio_path) in enumerate(new_audio_files, 1):
    transcript_path = TRANSCRIPT_DIR / f'{cid}_raw.json'
    
    # Skip if already done
    if transcript_path.exists():
        with open(transcript_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list) and len(data) > 0:
            print(f"[{i}/{len(new_audio_files)}] {cid} - SKIP (already done)")
            results.append({'cid': cid, 'status': 'DONE', 'segments': len(data)})
            continue
    
    print(f"[{i}/{len(new_audio_files)}] {cid} - Processing...")
    
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
    
    # Chunk processing
    chunk_length = 240  # 4 minutes
    chunk_dir = ASR_TEMP / cid
    chunk_dir.mkdir(parents=True, exist_ok=True)
    
    # Split audio
    chunk_files = []
    for start_time in range(0, int(duration), chunk_length):
        chunk_path = chunk_dir / f'chunk_{start_time//chunk_length:03d}.wav'
        subprocess.run(
            ['ffmpeg', '-y', '-ss', str(start_time), '-t', str(chunk_length),
             '-i', str(audio_path), '-ar', '16000', '-ac', '1',
             '-c:a', 'pcm_s16le', str(chunk_path)],
            capture_output=True, timeout=60
        )
        chunk_files.append((start_time // chunk_length, start_time, chunk_path))
    
    # Transcribe each chunk
    all_segments = []
    for chunk_idx, chunk_start, chunk_path in chunk_files:
        try:
            segs, info = model.transcribe(str(chunk_path), beam_size=1, language='zh', vad_filter=True)
            local_segs = list(segs)
            
            # Adjust timestamps
            for s in local_segs:
                s.start += chunk_start
                s.end += chunk_start
            
            all_segments.extend(local_segs)
            
        except Exception as e:
            print(f"    Chunk {chunk_idx} failed: {e}")
    
    # Save
    transcript = [{'start': round(s.start, 2), 'end': round(s.end, 2), 'text': s.text.strip()} for s in all_segments]
    transcript_path.write_text(json.dumps(transcript, ensure_ascii=False, indent=2), encoding='utf-8')
    
    chars = sum(len(s['text']) for s in transcript)
    print(f"  ✓ Done: {len(all_segments)} segs, {chars} chars")
    results.append({'cid': cid, 'status': 'DONE', 'segments': len(all_segments), 'chars': chars})
    
    time.sleep(0.5)

# Summary
done = len([r for r in results if r.get('status') == 'DONE'])
print(f"\n{'='*50}")
print(f"New ASR complete: {done}/{len(new_audio_files)}")

# Save
output = TRANSCRIPT_DIR / "batch002_new_asr_results.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"Saved to: {output}")