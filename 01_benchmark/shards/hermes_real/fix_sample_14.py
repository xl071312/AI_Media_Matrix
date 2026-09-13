#!/usr/bin/env python3
"""Fix sample_14 - add missing metrics and manifest"""
import json
import hashlib
from pathlib import Path

BATCH = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\analysis_batches\batch_001")
sample_dir = BATCH / "sample_14"

# Read existing files
with open(sample_dir / "01_metadata.json") as f:
    meta = json.load(f)
with open(sample_dir / "02_performance.json") as f:
    perf = json.load(f)
with open(sample_dir / "04_transcript_raw.json") as f:
    transcript = json.load(f)

cid = meta.get('content_id', '')
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
from datetime import datetime
video_path = Path(f"F:\\workspace\\AI_Media_Matrix\\10_automation\\benchmark_collector\\MediaCrawler\\data\\douyin\\videos\\{cid}\\video.mp4")
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

print(f"Fixed sample_14: {cid}")
print(f"  Segments: {len(transcript)}")
print(f"  Duration: {duration:.2f}s")
print(f"  Total chars: {total_chars}")
print(f"  Metrics saved")
print(f"  Manifest saved")
