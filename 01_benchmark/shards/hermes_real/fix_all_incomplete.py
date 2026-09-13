#!/usr/bin/env python3
"""Fix all incomplete samples"""
import json
import hashlib
from pathlib import Path
from datetime import datetime

BATCH = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\analysis_batches\batch_001")

def fix_sample(sample_dir):
    """Add missing metrics and manifest"""
    if (sample_dir / "06_metrics_basic.json").exists() and (sample_dir / "08_evidence_manifest.json").exists():
        return None
    
    trans_file = sample_dir / "04_transcript_raw.json"
    if not trans_file.exists():
        return None
    
    with open(trans_file, 'r', encoding='utf-8') as f:
        transcript = json.load(f)
    
    meta_file = sample_dir / "01_metadata.json"
    if meta_file.exists():
        with open(meta_file) as f:
            meta = json.load(f)
        cid = meta.get('content_id', '')
    else:
        return None
    
    if not cid:
        return None
    
    duration = transcript[-1]['end'] if transcript else 0
    
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
    
    (sample_dir / "06_metrics_basic.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False))
    
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
    
    return metrics

# Find and fix incomplete samples
incomplete = []
for s in sorted(BATCH.glob("sample_*")):
    if not (s / "06_metrics_basic.json").exists() or not (s / "08_evidence_manifest.json").exists():
        incomplete.append(s)

print(f"Found {len(incomplete)} incomplete samples\n")

for sample_dir in incomplete:
    print(f"Fixing {sample_dir.name}...")
    metrics = fix_sample(sample_dir)
    if metrics:
        print(f"  ✓ {metrics['asr_segment_count']} segments")
    else:
        print(f"  ✗ Failed")

# Final verification
print("\n=== FINAL STATUS ===")
samples = sorted(BATCH.glob("sample_*"))
complete = sum(1 for s in samples if (s/"06_metrics_basic.json").exists() and (s/"08_evidence_manifest.json").exists())
print(f"Complete samples: {complete}/{len(samples)}")

if complete >= 10:
    print(f"\n✓ Target reached (>=10 samples)")
    print(f"  Ready for final V4 bundle")
