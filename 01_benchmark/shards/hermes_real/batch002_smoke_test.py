#!/usr/bin/env python3
"""
Batch 002 - Smoke Test with 3 NEW UNIQUE videos
Download media, run ASR, create samples
HERMES Role: DATA ENGINEER ONLY
"""
import asyncio
import json
import csv
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH2 = BASE / "analysis_batches" / "batch_002"
BATCH2.mkdir(parents=True, exist_ok=True)
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"

# New unique IDs from DOM scraping
NEW_CIDS = ['7683219193294114063', '7682806976379620660', '7682728905966423334']

def get_duration(path):
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                           "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                          capture_output=True, text=True, timeout=10)
        return float(r.stdout.strip())
    except:
        return None

def calc_metrics(transcript, duration):
    import re
    full_text = ''.join([s['text'] for s in transcript])
    return {
        "duration_sec": round(duration, 2),
        "asr_segment_count": len(transcript),
        "total_chars": len(full_text),
        "chars_per_sec": round(len(full_text) / max(duration, 1), 2),
        "first_person_count": len(re.findall(r'[我咱俺]', full_text)),
        "second_person_count": len(re.findall(r'[你您]', full_text)),
        "number_count": len(re.findall(r'\d+', full_text)),
        "question_marker_count": full_text.count('？') + full_text.count('?'),
        "transcript_sha256": hashlib.sha256(full_text.encode('utf-8')).hexdigest()[:16]
    }

async def run_asr(video_path, cid):
    """Run ASR on single video"""
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("Systran/faster-whisper-base", device="cpu", compute_type="int8")
        segments, info = model.transcribe(str(video_path), beam_size=5, language="zh")
        
        transcript = []
        for seg in segments:
            transcript.append({"start": seg.start, "end": seg.end, "text": seg.text.strip()})
        
        (TRANSCRIPT_DIR / f"{cid}_raw.json").write_text(json.dumps(transcript, ensure_ascii=False, indent=2))
        return transcript
    except Exception as e:
        print(f"  ASR failed: {e}")
        return None

def create_sample(next_id, cid, transcript, duration):
    """Create complete sample directory"""
    sample_dir = BATCH2 / f"sample_{next_id:02d}"
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # Metadata (from DOM - limited info)
    meta = {
        "content_id": cid,
        "url": f"https://www.douyin.com/video/{cid}",
        "creator_id": "DOM_SCRAPED",
        "creator_name": "DOM_SCRAPED",
        "title": "DOM_SCRAPED",
        "topic": "DOM_SCRAPED",
        "viral_type": "UNKNOWN",
        "sample_role": "NEW_COLLECTED",
        "duration_sec": round(duration, 2),
        "capture_time": datetime.now().isoformat(),
        "metadata_source": "DOM_SCRAPED"
    }
    (sample_dir / "01_metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    
    # Performance (not available from DOM)
    perf = {"likes": None, "comments": None, "favorites": None, "shares": None}
    (sample_dir / "02_performance.json").write_text(json.dumps(perf, indent=2, ensure_ascii=False))
    
    # Creator baseline
    (sample_dir / "03_creator_baseline.json").write_text(json.dumps({
        "status": "NOT_COLLECTED",
        "note": "DOM scraping only - no API access",
        "creator_id": "DOM_SCRAPED"
    }, indent=2, ensure_ascii=False))
    
    # Transcript raw
    (sample_dir / "04_transcript_raw.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
    
    # Transcript markdown
    lines = [f"# Raw Transcript: {cid}", "",
             f"**Source**: ASR Raw Output",
             f"**Status**: UNVERIFIED_RAW_ASR",
             f"**Note**: Complete transcript embedded.", "", "---", ""]
    for j, seg in enumerate(transcript):
        sm, ss = int(seg['start']//60), seg['start']%60
        em, es = int(seg['end']//60), seg['end']%60
        lines.append(f"[S{j+1:04d}] [{sm:02d}:{ss:05.2f}-{em:02d}:{es:05.2f}] {seg['text']}")
    (sample_dir / "05_transcript_raw.md").write_text('\n'.join(lines), encoding='utf-8')
    
    # Metrics
    metrics = calc_metrics(transcript, duration)
    (sample_dir / "06_metrics_basic.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False))
    
    # Top comments placeholder
    with open(sample_dir / "07_top_comments.csv", 'w', encoding='utf-8') as f:
        f.write("comment_id,author,text,likes,reply_count,created_time\n")
        f.write("# To be collected\n")
    
    # Manifest
    video_path = VIDEO_DIR / cid / "video.mp4"
    manifest = {
        "content_id": cid,
        "media_path": str(video_path),
        "media_size_mb": round(video_path.stat().st_size / 1024 / 1024, 2) if video_path.exists() else 0,
        "media_sha256": hashlib.sha256(video_path.read_bytes()).hexdigest()[:16] if video_path.exists() else '',
        "transcript_sha256": metrics['transcript_sha256'],
        "segment_count": len(transcript),
        "duration_sec": round(duration, 2)
    }
    (sample_dir / "08_evidence_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    
    return manifest

async def main():
    print("=== BATCH 002 - SMOKE TEST (3 NEW UNIQUE) ===\n")
    
    results = {'new_unique': 0, 'media': 0, 'transcript': 0, 'performance': 0}
    
    for i, cid in enumerate(NEW_CIDS, 1):
        print(f"\n[{i}/3] Processing {cid}...")
        
        # Check if video exists
        video_path = VIDEO_DIR / cid / "video.mp4"
        if not video_path.exists():
            print(f"  ✗ Video not found locally")
            continue
        
        print(f"  ✓ Video found: {video_path.stat().st_size / 1024 / 1024:.1f} MB")
        results['media'] += 1
        
        # Get duration
        duration = get_duration(video_path)
        if not duration:
            print(f"  ✗ Cannot get duration")
            continue
        
        print(f"  ✓ Duration: {duration:.1f}s")
        
        # Run ASR
        transcript = await run_asr(video_path, cid)
        if not transcript or len(transcript) == 0:
            print(f"  ✗ Empty transcript")
            continue
        
        print(f"  ✓ ASR: {len(transcript)} segments")
        results['transcript'] += 1
        
        # Create sample
        manifest = create_sample(i, cid, transcript, duration)
        print(f"  ✓ Sample created")
        results['new_unique'] += 1
        
        # Note: performance not available from DOM scraping
        print(f"  ⚠ Performance: NULL (DOM scraping limitation)")
    
    # Smoke test results
    print(f"\n=== SMOKE TEST RESULTS ===")
    print(f"NEW UNIQUE: {results['new_unique']}/3")
    print(f"MEDIA: {results['media']}/3")
    print(f"TRANSCRIPT: {results['transcript']}/3")
    print(f"PERFORMANCE: {results['performance']}/3")
    print(f"simulated: 0")
    
    if results['new_unique'] == 3 and results['media'] == 3 and results['transcript'] == 3:
        print(f"\n✓ SMOKE TEST PASSED (partial - no performance data)")
        print(f"  Next: Try to get performance via DOM or API")
    else:
        print(f"\n✗ SMOKE TEST FAILED")

if __name__ == "__main__":
    asyncio.run(main())
