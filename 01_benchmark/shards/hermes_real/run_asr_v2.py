#!/usr/bin/env python3
"""Run ASR on extracted audio files"""
import json
import subprocess
from pathlib import Path
import os

BASE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
VIDEO_DIR = Path(r"C:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
AUDIO_DIR = BASE / "audio"
TRANSCRIPT_DIR = BASE / "transcripts"

def extract_audio(video_path, audio_path):
    """Extract audio from video"""
    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vn", "-acodec", "copy",
        str(audio_path)
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode == 0

def run_whisper_asr(audio_path, content_id):
    """Run whisper ASR"""
    # Try faster-whisper first
    try:
        from faster_whisper import WhisperModel
        
        # Find model path
        model_path = r"E:/.cache/huggingface/hub/models--Systran--faster-whisper-base/snapshots"
        import os
        if os.path.exists(model_path):
            snapshots = os.listdir(model_path)
            if snapshots:
                model_path = os.path.join(model_path, snapshots[0])
        
        print(f"    Loading model from: {model_path}")
        model = WhisperModel(model_path, device="cpu", compute_type="int8")
        
        print(f"    Transcribing...")
        segments, info = model.transcribe(str(audio_path), beam_size=5)
        
        # Collect segments
        transcript = []
        for segment in segments:
            transcript.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })
        
        # Save JSON
        json_file = TRANSCRIPT_DIR / f"{content_id}_raw.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, indent=2, ensure_ascii=False)
        
        # Save MD
        md_file = TRANSCRIPT_DIR / f"{content_id}_raw.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            for seg in transcript:
                start_min = int(seg['start'] // 60)
                start_sec = seg['start'] % 60
                end_min = int(seg['end'] // 60)
                end_sec = seg['end'] % 60
                f.write(f"[{start_min:02d}:{start_sec:05.2f} - {end_min:02d}:{end_sec:05.2f}] {seg['text']}\n")
        
        return True, len(transcript)
        
    except Exception as e:
        return False, str(e)

def main():
    print("=== ASR PROCESSING ===\n")
    
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find videos with audio
    video_files = list(VIDEO_DIR.glob("*/video.mp4"))
    print(f"Found {len(video_files)} videos\n")
    
    results = []
    
    for i, video_path in enumerate(video_files[:5], 1):  # Process first 5
        content_id = video_path.parent.name
        audio_path = AUDIO_DIR / f"{content_id}.m4a"
        
        print(f"[{i}/5] {content_id}")
        
        # Check if already processed
        if (TRANSCRIPT_DIR / f"{content_id}_raw.json").exists():
            print(f"  ✓ Already processed")
            results.append({"id": content_id, "status": "EXISTING"})
            continue
        
        # Extract audio
        print(f"  Extracting audio...")
        if not extract_audio(video_path, audio_path):
            print(f"  ✗ Audio extraction failed")
            results.append({"id": content_id, "status": "AUDIO_FAIL"})
            continue
        
        # Run ASR
        print(f"  Running ASR...")
        success, result = run_whisper_asr(audio_path, content_id)
        
        if success:
            print(f"  ✓ ASR complete: {result} segments")
            results.append({"id": content_id, "status": "PASS", "segments": result})
        else:
            print(f"  ✗ ASR failed: {result}")
            results.append({"id": content_id, "status": "FAIL", "error": result})
        
        # Clean up audio
        if audio_path.exists():
            audio_path.unlink()
    
    # Save results
    output = BASE / "asr_results.json"
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Summary
    passed = sum(1 for r in results if r.get('status') == 'PASS')
    print(f"\n=== SUMMARY ===")
    print(f"Processed: {len(results)}")
    print(f"Success: {passed}")
    print(f"Failed: {len(results) - passed}")

if __name__ == "__main__":
    main()
