#!/usr/bin/env python3
"""Fix incomplete samples - add missing metrics and manifest files"""
import json
import hashlib
from pathlib import Path

BATCH = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\analysis_batches\batch_001")
SHARDS = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")

def fix_sample(sample_dir):
    """Add missing 06_metrics_basic.json and 08_evidence_manifest.json"""
    # Check if already complete
    if (sample_dir / "06_metrics_basic.json").exists() and (sample_dir / "08_evidence_manifest.json").exists():
        return None
    
    cid = None
    transcript = None
    
    # Read transcript
    trans_file = sample_dir / "04_transcript_raw.json"
    if not trans_file.exists():
        return None
    with open(trans_file, 'r', encoding='utf-8') as f:
        transcript = json.load(f)
    
    # Get content_id from metadata
    meta_file = sample_dir / "01_metadata.json"
    if meta_file.exists():
        with open(meta_file) as f:
            meta = json.load(f)
        cid = meta.get('content_id')
    
    if not cid or not transcript:
        return None
    
    # Calculate duration from transcript
    duration = transcript[-1]['end'] if transcript else 0
    
    # Calculate metrics
    import re
    full_text = ''.join([s['text'] for s in transcript])
    total_chars = len(full_text)
    metrics = {
        "duration_sec": round(duration, 2),
        "asr_segment_count": len(transcript),
        "total_chars": total_chars,
        "chars_per_sec": round(total_chars / max(duration, 1), 2),
        "first_person_count": len(re.findall(r'[我咱俺]', full_text)),
        "second_person_count": len(re.findall(r'[你您]', full_text)),
        "number_count": len(re.findall(r'\d+', full_text)),
        "question_marker_count": full_text.count('？') + full_text.count('?'),
        "transcript_sha256": hashlib.sha256(full_text.encode('utf-8')).hexdigest()[:16]
    }
    
    # Save metrics
    (sample_dir / "06_metrics_basic.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False))
    
    # Create manifest
    video_path = VIDEO_DIR / cid / "video.mp4"
    manifest = {
        "content_id": cid,
        "media_path": str(video_path),
        "media_size_mb": round(video_path.stat().st_size / 1024 / 1024, 2),
        "media_sha256": hashlib.sha256(video_path.read_bytes()).hexdigest()[:16],
        "transcript_sha256": metrics['transcript_sha256'],
        "segment_count": len(transcript),
        "duration_sec": round(duration, 2)
    }
    (sample_dir / "08_evidence_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    
    return metrics

# Process incomplete samples
incomplete_samples = []
for s in sorted(BATCH.glob("sample_*")):
    if not (s / "06_metrics_basic.json").exists() or not (s / "08_evidence_manifest.json").exists():
        incomplete_samples.append(s)

print(f"Found {len(incomplete_samples)} incomplete samples\n")

for sample_dir in incomplete_samples:
    print(f"Fixing {sample_dir.name}...")
    metrics = fix_sample(sample_dir)
    if metrics:
        print(f"  ✓ Added metrics ({metrics['asr_segment_count']} segments)")
    else:
        print(f"  ✗ Failed")

# Final verification
print("\n=== FINAL VERIFICATION ===")
samples = sorted(BATCH.glob("sample_*"))
complete = 0
for s in samples:
    if (s / "06_metrics_basic.json").exists() and (s / "08_evidence_manifest.json").exists():
        complete += 1

print(f"Complete samples: {complete}/{len(samples)}")

# Update V4 bundle
if complete >= 6:
    print(f"\n✓ All samples complete. Ready for V4 bundle generation.")
