#!/usr/bin/env python3
"""Batch 002 ASR Recovery RC3 - GPU or CPU Chunked"""
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
MEDIA_DIR = BASE / "media" / "batch_002_smoke"
TRANSCRIPT_DIR = BASE / "shards" / "hermes_real" / "transcripts_v2"
ASR_TEMP = BASE / "shards" / "hermes_real" / "asr_temp"

# Create dirs
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
ASR_TEMP.mkdir(parents=True, exist_ok=True)

# Load checkpoint
checkpoint_path = TRANSCRIPT_DIR / "asr_checkpoint.jsonl"
checkpoint = {}
if checkpoint_path.exists():
    with open(checkpoint_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                record = json.loads(line)
                checkpoint[record['content_id']] = record

print("=== BATCH 002 ASR RECOVERY RC3 ===")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Detect GPU
import torch
cuda_available = torch.cuda.is_available()
print(f"CUDA available: {cuda_available}")
if cuda_available:
    gpu_name = torch.cuda.get_device_name(0)
    gpu_mem = torch.cuda.get_device_properties(0).total_memory / 1024**3
    print(f"GPU: {gpu_name}")
    print(f"VRAM: {gpu_mem:.1f} GB")
print()

# Try GPU smoke test
asr_device = "cpu"
asr_route = "CPU_CHUNKED"
gpu_smoke_passed = False

if cuda_available:
    print("Testing GPU ASR...")
    try:
        from faster_whisper import WhisperModel
        
        # Test with tiny model on GPU
        model = WhisperModel('Systran/faster-whisper-tiny', device='cuda', compute_type='float16')
        
        # Test transcription on short audio
        test_audio = list(MEDIA_DIR.glob('*.m4a'))[0] if list(MEDIA_DIR.glob('*.m4a')) else None
        if test_audio:
            print(f"Test audio: {test_audio.name}")
            start = time.time()
            segments, info = model.transcribe(str(test_audio), beam_size=1, language='zh', vad_filter=True)
            segs = list(segments)
            elapsed = time.time() - start
            
            if len(segs) > 0:
                print(f"✓ GPU smoke passed: {len(segs)} segments in {elapsed:.1f}s")
                asr_device = "cuda"
                asr_route = "GPU"
                gpu_smoke_passed = True
                
                # Keep model loaded
                gpu_model = model
            else:
                print("✗ GPU smoke failed: no segments")
        else:
            print("✗ No test audio found")
    except Exception as e:
        print(f"✗ GPU smoke failed: {e}")
        gpu_model = None
else:
    print("GPU not available, using CPU")

print(f"\nASR Route: {asr_route}")
print()

# Get audio files
audio_files = [p for p in MEDIA_DIR.glob('*.m4a') 
               if not any(x in p.name for x in ['76827', '76828', '76832'])]

print(f"Audio files to process: {len(audio_files)}")
print()

# Process each audio
results = []
chunk_failures = 0

for i, audio_path in enumerate(audio_files, 1):
    cid = audio_path.stem.replace('.audio', '')
    transcript_path = TRANSCRIPT_DIR / f'{cid}_raw.json'
    
    # Skip if already done
    if transcript_path.exists():
        with open(transcript_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list) and len(data) > 0:
            print(f"[{i}/{len(audio_files)}] {cid} - SKIP (already done)")
            results.append({'cid': cid, 'status': 'DONE', 'segments': len(data)})
            continue
    
    print(f"[{i}/{len(audio_files)}] {cid} - Processing...")
    
    # Get audio duration
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
    
    # Decide route
    if asr_route == "GPU" and gpu_smoke_passed:
        # GPU route
        try:
            start = time.time()
            segments, info = gpu_model.transcribe(str(audio_path), beam_size=1, language='zh', vad_filter=True)
            segs = list(segments)
            elapsed = time.time() - start
            
            # Save
            transcript = [{'start': round(s.start, 2), 'end': round(s.end, 2), 'text': s.text.strip()} for s in segs]
            transcript_path.write_text(json.dumps(transcript, ensure_ascii=False, indent=2), encoding='utf-8')
            
            chars = sum(len(s['text']) for s in transcript)
            print(f"  ✓ GPU: {len(segs)} segs, {chars} chars ({elapsed:.1f}s)")
            results.append({'cid': cid, 'status': 'DONE', 'segments': len(segs), 'chars': chars, 'time': elapsed, 'device': 'cuda'})
            
            # Update checkpoint
            checkpoint[cid] = {
                'content_id': cid,
                'status': 'DONE',
                'segments': len(segs),
                'chars': chars,
                'elapsed_sec': elapsed,
                'device': 'cuda',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"  ✗ GPU error: {e}")
            results.append({'cid': cid, 'status': 'FAILED', 'error': str(e)})
            checkpoint[cid] = {
                'content_id': cid,
                'status': 'FAILED',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    else:
        # CPU chunked route
        try:
            # Split audio into chunks
            chunk_dir = ASR_TEMP / cid
            chunk_dir.mkdir(parents=True, exist_ok=True)
            
            # Use ffmpeg to split
            chunk_length = 240  # 4 minutes
            chunk_files = []
            
            # Get actual duration
            probe_result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                 '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)],
                capture_output=True, text=True, timeout=10
            )
            audio_duration = float(probe_result.stdout.strip())
            
            # Split into chunks
            chunk_idx = 0
            for start_time in range(0, int(audio_duration), chunk_length):
                chunk_path = chunk_dir / f'chunk_{chunk_idx:03d}.wav'
                subprocess.run(
                    ['ffmpeg', '-y', '-ss', str(start_time), '-t', str(chunk_length),
                     '-i', str(audio_path), '-ar', '16000', '-ac', '1',
                     '-c:a', 'pcm_s16le', str(chunk_path)],
                    capture_output=True, timeout=30
                )
                chunk_files.append((chunk_idx, start_time, chunk_path))
                chunk_idx += 1
            
            # Transcribe each chunk
            from faster_whisper import WhisperModel
            cpu_model = WhisperModel('Systran/faster-whisper-tiny', device='cpu', compute_type='int8')
            
            all_segments = []
            chunk_results = []
            
            for chunk_idx, chunk_start, chunk_path in chunk_files:
                try:
                    segs, info = cpu_model.transcribe(str(chunk_path), beam_size=1, language='zh', vad_filter=True)
                    local_segs = list(segs)
                    
                    # Adjust timestamps
                    for s in local_segs:
                        s.start += chunk_start
                        s.end += chunk_start
                    
                    all_segments.extend(local_segs)
                    chunk_results.append({
                        'chunk_id': chunk_idx,
                        'start_sec': chunk_start,
                        'status': 'DONE',
                        'segments': len(local_segs)
                    })
                    
                except Exception as e:
                    print(f"    Chunk {chunk_idx} failed: {e}")
                    chunk_results.append({
                        'chunk_id': chunk_idx,
                        'start_sec': chunk_start,
                        'status': 'FAILED',
                        'error': str(e)
                    })
                    chunk_failures += 1
            
            # Save combined transcript
            transcript = [{'start': round(s.start, 2), 'end': round(s.end, 2), 'text': s.text.strip()} for s in all_segments]
            transcript_path.write_text(json.dumps(transcript, ensure_ascii=False, indent=2), encoding='utf-8')
            
            chars = sum(len(s['text']) for s in transcript)
            print(f"  ✓ CPU: {len(all_segments)} segs, {chars} chars")
            results.append({'cid': cid, 'status': 'DONE', 'segments': len(all_segments), 'chars': chars, 'chunks': len(chunk_files)})
            
            checkpoint[cid] = {
                'content_id': cid,
                'status': 'DONE',
                'segments': len(all_segments),
                'chars': chars,
                'chunks': len(chunk_files),
                'chunk_failures': chunk_failures,
                'device': 'cpu',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"  ✗ CPU error: {e}")
            results.append({'cid': cid, 'status': 'FAILED', 'error': str(e)})
            checkpoint[cid] = {
                'content_id': cid,
                'status': 'FAILED',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

# Save checkpoint
with open(checkpoint_path, 'w', encoding='utf-8') as f:
    for cid, record in checkpoint.items():
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

# Summary
done = len([r for r in results if r.get('status') == 'DONE'])
failed = len([r for r in results if r.get('status') == 'FAILED'])

print(f"\n{'='*60}")
print(f"RESULTS:")
print(f"  Total: {len(results)}")
print(f"  Done: {done}")
print(f"  Failed: {failed}")
print(f"  Chunk failures: {chunk_failures}")
print(f"  ASR Route: {asr_route}")
print(f"  Device: {asr_device}")
print(f"\nSaved checkpoint to: {checkpoint_path}")