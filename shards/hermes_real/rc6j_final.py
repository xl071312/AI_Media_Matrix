#!/usr/bin/env python3
"""RC6J: Final report - media unavailable due to access restrictions"""
import json
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix")
SHORTLIST = BASE / "01_benchmark/analysis_batches/rc6i_shortlist/RC6I_VERIFIED_SHORTLIST.csv"
OUTPUT_DIR = BASE / "01_benchmark/analysis_batches/rc6j_full_transcripts"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load PRIMARY
shortlist = list(csv.DictReader(open(SHORTLIST, encoding='utf-8')))
primary = [r for r in shortlist if r.get('tier') == 'PRIMARY']

print(f"PRIMARY samples: {len(primary)}")

# Generate manifest - all TRANSCRIPT_MISSING due to media_unavailable
manifest_rows = []
for sample in primary:
    sample_id = sample.get('sample_id', '')
    manifest_rows.append({
        'sample_id': sample_id,
        'source_url': sample.get('source_url', ''),
        'video_duration': '',
        'media_available': 'NO',
        'media_source': 'NONE',
        'asr_attempted': 'NO',
        'asr_status': 'N/A',
        'transcript_level': 'TRANSCRIPT_MISSING',
        'transcript_start': '',
        'transcript_end': '',
        'coverage_seconds': 0,
        'coverage_ratio': 0,
        'segment_count': 0,
        'raw_char_count': 0,
        'first30_available': sample.get('first30_available', ''),
        'media_sha256': '',
        'transcript_sha256': '',
        'failure_reason': 'MEDIA_UNAVAILABLE - requires CDP or valid cookies',
        'source_commit': 'b599197'
    })
    
    # Create sample directory with metadata
    sample_dir = OUTPUT_DIR / sample_id
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # Save empty transcript
    csv_path = sample_dir / "transcript_raw.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['segment_id', 'start', 'end', 'raw_text'])
    
    # Save meta
    meta = {
        'sample_id': sample_id,
        'media_available': False,
        'transcript_level': 'TRANSCRIPT_MISSING',
        'segment_count': 0,
        'raw_char_count': 0,
        'failure_reason': 'MEDIA_UNAVAILABLE - requires CDP or valid cookies'
    }
    (sample_dir / "transcript_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    
    # Save evidence manifest
    evidence = {
        'sample_id': sample_id,
        'source_url': sample.get('source_url', ''),
        'media_file': None,
        'media_sha256': None,
        'transcript_file': str(csv_path.relative_to(BASE)),
        'transcript_sha256': '',
        'source_commit': 'b599197',
        'source_type': 'RC6J_MEDIA_UNAVAILABLE'
    }
    (sample_dir / "evidence_manifest.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf-8')

# Save manifest CSV
with open(OUTPUT_DIR / "RC6J_PRIMARY_28_TRANSCRIPT_MANIFEST.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=manifest_rows[0].keys())
    writer.writeheader()
    writer.writerows(manifest_rows)

# Generate report
report = f"""# RC6J Primary 28 Transcript Report

**Generated**: {datetime.now().isoformat()}
**Source Commit**: b599197
**Status**: MEDIA_UNAVAILABLE

## Input

PRIMARY = 28

## Media & ASR Stats

MEDIA_AVAILABLE = 0
ASR_ATTEMPTED = 0
ASR_SUCCESS = 0

## Transcript Levels

FULL_TRANSCRIPT = 0
PARTIAL_TRANSCRIPT = 0
FIRST30_ONLY = 0
TRANSCRIPT_MISSING = 28
Total = 28

## Analysis Readiness

FULL_ANALYSIS_READY = 0
PARTIAL_ANALYSIS_READY = 0
HOOK_ONLY_READY = 0
NOT_READY = 28

## Failure Reason

所有28条PRIMARY样本均无法获取媒体文件，原因：
1. CDP端口9223不可用
2. yt-dlp需要有效的Douyin登录Cookie
3. 现有Cookie可能已过期或格式不匹配

## Required Action

需要以下任一条件才能继续：
1. 启动Chrome CDP: chrome --remote-debugging-port=9223
2. 提供有效的Netscape格式Douyin Cookie文件
3. 手动下载28个视频并放入对应目录

## Output

- `01_benchmark/analysis_batches/rc6j_full_transcripts/RC6J_PRIMARY_28_TRANSCRIPT_MANIFEST.csv`
- `01_benchmark/analysis_batches/rc6j_full_transcripts/RC6J_PRIMARY_28_TRANSCRIPT_REPORT.md`
- 28个样本目录（含元数据）

---
*本任务受限于媒体访问。等待CDP或Cookie问题解决后重试。*
"""

(OUTPUT_DIR / "RC6J_PRIMARY_28_TRANSCRIPT_REPORT.md").write_text(report, encoding='utf-8')

print(f"\n=== RC6J COMPLETE ===")
print(f"PRIMARY: 28")
print(f"MEDIA_AVAILABLE: 0")
print(f"TRANSCRIPT_MISSING: 28")
print(f"\nOutput: {OUTPUT_DIR}")
print(f"\nStatus: MEDIA_UNAVAILABLE - 需要CDP或有效Cookie")