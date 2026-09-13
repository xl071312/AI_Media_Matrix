#!/usr/bin/env python3
"""Rebuild lost sample files"""
import json
from pathlib import Path

BATCH = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\analysis_batches\batch_001")

# Rebuild sample_002
print("Rebuilding sample_002...")
s2 = BATCH / "sample_002"
s2.mkdir(parents=True, exist_ok=True)

# Metadata (already fixed)
meta2 = {
    "content_id": "7647797848847439706",
    "url": "https://www.douyin.com/video/7647797848847439706",
    "creator_id": "辉***累",
    "creator_name": "辉***累",
    "title": "普通人如何靠卖货翻身 #成长#认知",
    "topic": "副业",
    "viral_type": "COMMENT_HEAVY",
    "sample_role": "RELATIVE_BREAKOUT_CANDIDATE",
    "duration_sec": 170.2,
    "capture_time": "2026-09-09T01:08:57.340739",
    "metadata_source": "MEDIACRAWLER_REAL_CDP",
    "role_note": "Baseline not available - downgraded to CANDIDATE"
}
(s2 / "01_metadata.json").write_text(json.dumps(meta2, indent=2, ensure_ascii=False))

# Performance
perf2 = {
    "likes": 144012,
    "comments": 16989,
    "favorites": 56538,
    "shares": 26515,
    "favorite_like_ratio": 0.393,
    "share_like_ratio": 0.184,
    "comment_like_ratio": 0.118
}
(s2 / "02_performance.json").write_text(json.dumps(perf2, indent=2, ensure_ascii=False))

# Baseline
(s2 / "03_creator_baseline.json").write_text(json.dumps({
    "status": "NOT_COLLECTED",
    "note": "Requires API access or DOM fallback",
    "creator_id": "辉***累"
}, indent=2, ensure_ascii=False))

# Copy transcript from v3
import shutil
v3_sample2 = BATCH.parent / "batch_001_v3_temp" / "sample_002"
if (BATCH.parent / "BATCH_001_ANALYSIS_INPUT_V3.md").exists():
    # Read from V3 bundle
    v3_content = (BATCH / "BATCH_001_ANALYSIS_INPUT_V3.md").read_text(encoding='utf-8')
    # Find sample_002 section
    if "## Sample 2" in v3_content:
        # Extract transcript
        start = v3_content.find("## Sample 2")
        end = v3_content.find("## Sample 3")
        if end == -1:
            end = len(v3_content)
        sample2_content = v3_content[start:end]
        
        # Save transcript files
        # We need to extract the raw transcript
        pass

# For now, use the transcript from transcripts_v2
TRANSCRIPT_DIR = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real\transcripts_v2")
trans_file = TRANSCRIPT_DIR / "7647797848847439706_raw.json"
if trans_file.exists():
    with open(trans_file) as f:
        transcript = json.load(f)
    (s2 / "04_transcript_raw.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
    
    # Save markdown
    with open(s2 / "05_transcript_raw.md", 'w', encoding='utf-8') as f:
        f.write(f"# Raw Transcript: 7647797848847439706\n\n")
        f.write(f"**Source**: ASR Raw Output\n")
        f.write(f"**Status**: UNVERIFIED_RAW_ASR\n\n---\n\n")
        for seg in transcript:
            start_min = int(seg['start'] // 60)
            start_sec = seg['start'] % 60
            end_min = int(seg['end'] // 60)
            end_sec = seg['end'] % 60
            f.write(f"[{seg['segment_id']}] [{start_min:02d}:{start_sec:05.2f}-{end_min:02d}:{end_sec:05.2f}] {seg['text']}\n")
    
    # Metrics
    import hashlib
    import re
    full_text = ''.join([s['text'] for s in transcript])
    metrics = {
        "duration_sec": 170.2,
        "asr_segment_count": len(transcript),
        "total_chars": len(full_text),
        "chars_per_sec": round(len(full_text) / 170.2, 2),
        "first_person_count": len(re.findall(r'[我咱俺]', full_text)),
        "second_person_count": len(re.findall(r'[你您]', full_text)),
        "number_count": len(re.findall(r'\d+', full_text)),
        "question_marker_count": full_text.count('？') + full_text.count('?'),
        "transcript_sha256": hashlib.sha256(full_text.encode('utf-8')).hexdigest()[:16]
    }
    (s2 / "06_metrics_basic.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False))
    
    # Top comments
    with open(s2 / "07_top_comments.csv", 'w', encoding='utf-8') as f:
        f.write("comment_id,author,text,likes,reply_count,created_time\n")
        f.write("# To be collected\n")
    
    # Manifest
    import hashlib
    from pathlib import Path
    video_path = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos\7647797848847439706\video.mp4")
    manifest = {
        "content_id": "7647797848847439706",
        "media_path": str(video_path),
        "media_size_mb": round(video_path.stat().st_size / 1024 / 1024, 2),
        "media_sha256": hashlib.sha256(video_path.read_bytes()).hexdigest()[:16],
        "transcript_sha256": metrics['transcript_sha256'],
        "segment_count": len(transcript),
        "duration_sec": 170.2
    }
    (s2 / "08_evidence_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    
    print("  ✓ Sample 002 rebuilt")

# Rebuild sample_003
print("Rebuilding sample_003...")
s3 = BATCH / "sample_003"
s3.mkdir(parents=True, exist_ok=True)

# Metadata (already fixed)
meta3 = {
    "content_id": "7302348364815928612",
    "url": "https://www.douyin.com/video/7302348364815928612",
    "creator_id": "UNKNOWN",
    "creator_name": "UNKNOWN",
    "title": "UNKNOWN - External data, not in selection",
    "topic": "UNKNOWN",
    "viral_type": "EXTERNAL_DATA",
    "sample_role": "EXTERNAL_DATA",
    "duration_sec": 205.37,
    "capture_time": "2026-09-09T01:08:57.581336",
    "metadata_source": "EXTERNAL"
}
(s3 / "01_metadata.json").write_text(json.dumps(meta3, indent=2, ensure_ascii=False))

# Performance
perf3 = {
    "likes": 0,
    "comments": 0,
    "favorites": 0,
    "shares": 0,
    "favorite_like_ratio": 0.0,
    "share_like_ratio": 0.0,
    "comment_like_ratio": 0.0,
    "note": "Performance data not available - external data source"
}
(s3 / "02_performance.json").write_text(json.dumps(perf3, indent=2, ensure_ascii=False))

# Baseline
(s3 / "03_creator_baseline.json").write_text(json.dumps({
    "status": "NOT_AVAILABLE",
    "note": "External data source - no baseline available"
}, indent=2, ensure_ascii=False))

# Transcript
trans_file = TRANSCRIPT_DIR / "7302348364815928612_raw.json"
if trans_file.exists():
    with open(trans_file) as f:
        transcript = json.load(f)
    (s3 / "04_transcript_raw.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
    
    with open(s3 / "05_transcript_raw.md", 'w', encoding='utf-8') as f:
        f.write(f"# Raw Transcript: 7302348364815928612\n\n")
        f.write(f"**Source**: ASR Raw Output\n")
        f.write(f"**Status**: UNVERIFIED_RAW_ASR\n")
        f.write(f"**Note**: External data source - metadata not available\n\n---\n\n")
        for seg in transcript:
            start_min = int(seg['start'] // 60)
            start_sec = seg['start'] % 60
            end_min = int(seg['end'] // 60)
            end_sec = seg['end'] % 60
            f.write(f"[{seg['segment_id']}] [{start_min:02d}:{start_sec:05.2f}-{end_min:02d}:{end_sec:05.2f}] {seg['text']}\n")
    
    # Metrics
    import hashlib
    import re
    full_text = ''.join([s['text'] for s in transcript])
    metrics = {
        "duration_sec": 205.37,
        "asr_segment_count": len(transcript),
        "total_chars": len(full_text),
        "chars_per_sec": round(len(full_text) / 205.37, 2),
        "first_person_count": len(re.findall(r'[我咱俺]', full_text)),
        "second_person_count": len(re.findall(r'[你您]', full_text)),
        "number_count": len(re.findall(r'\d+', full_text)),
        "question_marker_count": full_text.count('？') + full_text.count('?'),
        "transcript_sha256": hashlib.sha256(full_text.encode('utf-8')).hexdigest()[:16]
    }
    (s3 / "06_metrics_basic.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False))
    
    with open(s3 / "07_top_comments.csv", 'w', encoding='utf-8') as f:
        f.write("comment_id,author,text,likes,reply_count,created_time\n")
        f.write("# To be collected\n")
    
    video_path = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos\7302348364815928612\video.mp4")
    manifest = {
        "content_id": "7302348364815928612",
        "media_path": str(video_path),
        "media_size_mb": round(video_path.stat().st_size / 1024 / 1024, 2),
        "media_sha256": hashlib.sha256(video_path.read_bytes()).hexdigest()[:16],
        "transcript_sha256": metrics['transcript_sha256'],
        "segment_count": len(transcript),
        "duration_sec": 205.37
    }
    (s3 / "08_evidence_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    
    print("  ✓ Sample 003 rebuilt")

print("\n=== REBUILD COMPLETE ===")
samples = sorted(BATCH.glob("sample_*"))
print(f"Total samples: {len(samples)}")
