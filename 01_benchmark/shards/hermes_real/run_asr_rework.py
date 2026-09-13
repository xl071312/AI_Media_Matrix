#!/usr/bin/env python3
"""Re-run ASR with quality checks"""
import json
import subprocess
from pathlib import Path
import hashlib

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
TRANSCRIPT_DIR = BASE / "transcripts_v2"
QA_LOG = BASE / "qa_logs"

def get_video_info(video_path):
    """Get video duration and info"""
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration,size,bit_rate",
            "-show_entries", "stream=codec_name,width,height",
            "-of", "json",
            str(video_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return json.loads(result.stdout)
    except Exception as e:
        return None

def calculate_sha256(file_path):
    """Calculate file hash"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def run_asr_with_qa(video_path, content_id):
    """Run ASR and return segments with validation"""
    print(f"  Running ASR for {content_id}...")
    
    try:
        from faster_whisper import WhisperModel
        
        # Load model
        model_path = r"E:/.cache/huggingface/hub/models--Systran--faster-whisper-base/snapshots"
        import os
        snapshots = os.listdir(model_path)
        if snapshots:
            model_path = os.path.join(model_path, snapshots[0])
        
        model = WhisperModel(model_path, device="cpu", compute_type="int8")
        
        # Transcribe
        segments, info = model.transcribe(str(video_path), beam_size=5, language="zh")
        
        # Collect segments
        transcript = []
        for segment in segments:
            transcript.append({
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": segment.text.strip()
            })
        
        # Validate timestamps
        video_info = get_video_info(video_path)
        if video_info and 'format' in video_info:
            duration = float(video_info['format'].get('duration', 0))
            last_ts = transcript[-1]['end'] if transcript else 0
            
            if last_ts > duration + 1:
                print(f"  WARNING: Last timestamp {last_ts}s exceeds duration {duration}s")
            
            # Save QA log
            qa_log = {
                "content_id": content_id,
                "video_duration": duration,
                "asr_duration": last_ts,
                "segment_count": len(transcript),
                "timestamp_valid": last_ts <= duration + 1
            }
            (QA_LOG / f"{content_id}_qa.json").write_text(json.dumps(qa_log, indent=2))
        
        return transcript, True
        
    except Exception as e:
        print(f"  ERROR: {e}")
        return None, False

def main():
    print("=== PHASE 3.1 REWORK: ASR RE-PROCESSING ===\n")
    
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    QA_LOG.mkdir(parents=True, exist_ok=True)
    
    # Target videos
    targets = [
        "7302348364815928612",
        "7647797848847439706",
        "7643008320555568355"
    ]
    
    results = []
    
    for content_id in targets:
        print(f"\n--- {content_id} ---")
        
        video_path = VIDEO_DIR / content_id / "video.mp4"
        if not video_path.exists():
            print(f"  SKIP: Video not found")
            results.append({"id": content_id, "status": "MISSING"})
            continue
        
        # Get video info
        video_info = get_video_info(video_path)
        duration = float(video_info['format']['duration']) if video_info else 0
        file_size = video_path.stat().st_size
        sha256 = calculate_sha256(video_path)
        
        print(f"  Duration: {duration:.2f}s")
        print(f"  Size: {file_size / 1024 / 1024:.2f}MB")
        print(f"  SHA256: {sha256[:16]}...")
        
        # Run ASR
        transcript, success = run_asr_with_qa(video_path, content_id)
        
        if success and transcript:
            # Save transcript
            json_file = TRANSCRIPT_DIR / f"{content_id}_raw.json"
            md_file = TRANSCRIPT_DIR / f"{content_id}_raw.md"
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(transcript, f, indent=2, ensure_ascii=False)
            
            with open(md_file, 'w', encoding='utf-8') as f:
                for seg in transcript:
                    start_min = int(seg['start'] // 60)
                    start_sec = seg['start'] % 60
                    end_min = int(seg['end'] // 60)
                    end_sec = seg['end'] % 60
                    f.write(f"[{start_min:02d}:{start_sec:05.2f} - {end_min:02d}:{end_sec:05.2f}] {seg['text']}\n")
            
            print(f"  ✓ Saved: {len(transcript)} segments")
            results.append({"id": content_id, "status": "PASS", "segments": len(transcript)})
        else:
            print(f"  ✗ FAILED")
            results.append({"id": content_id, "status": "FAIL"})
    
    # Summary
    print(f"\n=== SUMMARY ===")
    passed = sum(1 for r in results if r.get('status') == 'PASS')
    print(f"Processed: {len(results)}")
    print(f"Success: {passed}")
    print(f"Failed: {len(results) - passed}")
    
    # Save results
    with open(BASE / "asr_rework_results.json", 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
