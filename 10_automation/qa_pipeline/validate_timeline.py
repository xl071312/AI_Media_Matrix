#!/usr/bin/env python3
"""Validate timeline consistency with video duration"""
import json
import subprocess
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")

def get_video_duration(video_path):
    """Get video duration using ffprobe"""
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(video_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return float(result.stdout.strip())
    except:
        return None

def validate_timeline(content_id, max_allowable_seconds=None):
    """Validate timeline timestamps don't exceed video duration"""
    timeline_file = BASE / "qa_batch_001" / f"sample_{content_id[-1]}" / "07_timeline.md"
    
    if not timeline_file.exists():
        return False, "Timeline file not found"
    
    # Find video file
    video_file = VIDEO_DIR / content_id / "video.mp4"
    if not video_file.exists():
        return False, "Video file not found"
    
    # Get duration
    duration = get_video_duration(video_file)
    if duration is None:
        return False, "Could not get video duration"
    
    # Check timeline for timestamps exceeding duration
    with open(timeline_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract timestamps
    import re
    timestamps = re.findall(r'(\d+):(\d+):(\d+)', content)
    
    max_found = 0
    for h, m, s in timestamps:
        total = int(h) * 3600 + int(m) * 60 + int(s)
        max_found = max(max_found, total)
    
    # Allow 1 second tolerance
    if max_found > duration + 1:
        return False, f"Timeline exceeds duration: max={max_found}s, video={duration}s"
    
    return True, f"OK (duration={duration}s, max_timeline={max_found}s)"

def main():
    print("=== TIMELINE VALIDATION ===\n")
    
    # Validate each sample
    samples = [
        ("7302348364815928612", "sample_01"),
        ("7647797848847439706", "sample_02"),
        ("7643008320555568355", "sample_03"),
    ]
    
    results = []
    for content_id, sample_name in samples:
        print(f"Validating {content_id}...")
        valid, msg = validate_timeline(content_id)
        print(f"  {msg}")
        results.append({"id": content_id, "valid": valid, "message": msg})
    
    # Summary
    passed = sum(1 for r in results if r['valid'])
    print(f"\n=== SUMMARY ===")
    print(f"Passed: {passed}/{len(results)}")
    
    if passed < len(results):
        print("\nAction required: Regenerate timelines with correct timestamps")
    
    return results

if __name__ == "__main__":
    main()
