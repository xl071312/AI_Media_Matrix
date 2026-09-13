#!/usr/bin/env python3
"""Run ASR on downloaded videos"""
import json
import subprocess
from pathlib import Path
import os

BASE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
VIDEO_DIR = Path(r"C:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
TRANSCRIPT_DIR = BASE / "transcripts"

def run_asr(video_path, content_id):
    """Run faster-whisper ASR"""
    print(f"  Running ASR: {content_id}")
    
    try:
        # Use faster-whisper with base model
        cmd = [
            "python", "-m", "faster_whisper.transcribe",
            str(video_path),
            "--model_size", "base",
            "--output_format", "json",
            "--output_dir", str(TRANSCRIPT_DIR),
            "--word_timestamps", "true",
            "--device", "cpu"
        ]
        
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if proc.returncode == 0:
            # Find output file
            output_files = list(TRANSCRIPT_DIR.glob(f"{content_id}_*.json"))
            if output_files:
                return str(output_files[0]), "PASS"
        
        # Check for errors
        if "cuda" in proc.stderr.lower() or "gpu" in proc.stderr.lower():
            return None, "GPU_NOT_AVAILABLE"
            
        return None, "ASR_FAILED"
        
    except FileNotFoundError:
        return None, "WHISPER_NOT_INSTALLED"
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"
    except Exception as e:
        return None, f"ERROR: {str(e)}"

def main():
    print("=== ASR PROCESSING ===\n")
    
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find videos
    video_dirs = list(VIDEO_DIR.glob("*/video.mp4"))
    print(f"Found {len(video_dirs)} videos\n")
    
    results = []
    
    for i, video_path in enumerate(video_dirs[:10], 1):  # Process first 10
        content_id = video_path.parent.name
        print(f"[{i}/{min(10, len(video_dirs))}] {content_id}")
        
        # Check if already processed
        existing = list(TRANSCRIPT_DIR.glob(f"{content_id}_*.json"))
        if existing:
            print(f"  ✓ Already processed")
            results.append({"id": content_id, "status": "EXISTING"})
            continue
        
        transcript_file, status = run_asr(video_path, content_id)
        
        if status == "PASS":
            print(f"  ✓ ASR complete: {transcript_file}")
            results.append({"id": content_id, "status": "PASS", "file": transcript_file})
        else:
            print(f"  ✗ {status}")
            results.append({"id": content_id, "status": status})
        
        # Rate limit
        import time
        time.sleep(2)
    
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
