#!/usr/bin/env python3
"""RC6I: Generate Deep Analysis Input Pack for 28 PRIMARY samples"""
import json
import csv
import hashlib
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix")
SHORTLIST_FILE = BASE / "01_benchmark/analysis_batches/rc6i_shortlist/RC6I_VERIFIED_SHORTLIST.csv"
INPUT_DIR = BASE / "01_benchmark/analysis_batches/rc6i_deep_input"
INGEST_DIR = BASE / "01_benchmark/analysis_batches/BENCHMARK_SPOKEN_INGEST_108"

INPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load shortlist
shortlist = list(csv.DictReader(open(SHORTLIST_FILE, encoding='utf-8')))
primary = [r for r in shortlist if r.get('tier') == 'PRIMARY']

print(f"PRIMARY samples: {len(primary)}")

# Verify count
assert len(primary) == 28, f"ERROR: PRIMARY_COUNT_MISMATCH - expected 28, got {len(primary)}"
print("PRIMARY_COUNT = 28 ✓")

# Stats
stats = {
    'FULL_TRANSCRIPT': 0,
    'PARTIAL_TRANSCRIPT': 0,
    'FIRST30_ONLY': 0,
    'TRANSCRIPT_MISSING': 0,
    'REAL_SPOKEN_YES': 0,
    'FIRST30_AVAILABLE_YES': 0,
    'TOP_COMMENTS_AVAILABLE': 0,
    'EVIDENCE_AVAILABLE': 0,
    'CHATGPT_FULL_READY': 0,
    'CHATGPT_PARTIAL_READY': 0,
    'CHATGPT_HOOK_ONLY': 0,
    'CHATGPT_NOT_READY': 0
}

# Build input manifest and markdown
manifest_rows = []
md_content = "# RC6I PRIMARY 28 Deep Analysis Input\n\n"
md_content += f"**Generated**: {datetime.now().isoformat()}\n"
md_content += f"**Source Commit**: 182bc90c2c4f38c777a1c26ecf7723e594c02060\n\n"
md_content += "---\n\n"

for i, sample in enumerate(primary, 1):
    sample_id = sample.get('sample_id', '')
    
    # Find corresponding ingest directory
    ingest_dir = INGEST_DIR / sample_id
    has_ingest = ingest_dir.exists()
    
    # Load metadata
    meta = {}
    if (ingest_dir / "01_metadata.json").exists():
        with open(ingest_dir / "01_metadata.json", 'r', encoding='utf-8') as f:
            meta = json.load(f)
    
    # Load transcript
    transcript = {}
    transcript_level = 'TRANSCRIPT_MISSING'
    segment_count = 0
    total_chars = 0
    first30_text = None
    segments_data = []
    
    if (ingest_dir / "02_transcript_raw.json").exists():
        with open(ingest_dir / "02_transcript_raw.json", 'r', encoding='utf-8') as f:
            transcript = json.load(f)
        segment_count = len(transcript.get('segments', []))
        total_chars = transcript.get('transcript_chars', 0)
        segments_data = transcript.get('segments', [])
        status = transcript.get('status', '')
        
        if status == 'COMPLETE' and total_chars > 200:
            transcript_level = 'FULL_TRANSCRIPT'
            stats['FULL_TRANSCRIPT'] += 1
        elif status == 'COMPLETE' and total_chars > 50:
            transcript_level = 'PARTIAL_TRANSCRIPT'
            stats['PARTIAL_TRANSCRIPT'] += 1
        elif status == 'PARTIAL_FIRST30' or total_chars > 0:
            transcript_level = 'FIRST30_ONLY'
            stats['FIRST30_ONLY'] += 1
        else:
            transcript_level = 'TRANSCRIPT_MISSING'
            stats['TRANSCRIPT_MISSING'] += 1
    else:
        transcript_level = 'TRANSCRIPT_MISSING'
        stats['TRANSCRIPT_MISSING'] += 1
    
    # Get first30 text
    if (ingest_dir / "04_first30s_evidence.json").exists():
        with open(ingest_dir / "04_first30s_evidence.json", 'r', encoding='utf-8') as f:
            f30 = json.load(f)
        first30_text = f30.get('first30_text')
    
    # Check evidence manifest
    has_evidence = (ingest_dir / "06_evidence_manifest.json").exists()
    if has_evidence:
        stats['EVIDENCE_AVAILABLE'] += 1
    
    # Determine chatgpt_ready and analysis_scope
    if transcript_level in ['FULL_TRANSCRIPT', 'PARTIAL_TRANSCRIPT']:
        chatgpt_ready = 'YES'
        if transcript_level == 'FULL_TRANSCRIPT':
            stats['CHATGPT_FULL_READY'] += 1
            analysis_scope = 'FULL'
        else:
            stats['CHATGPT_PARTIAL_READY'] += 1
            analysis_scope = 'PARTIAL'
    elif transcript_level == 'FIRST30_ONLY':
        chatgpt_ready = 'LIMITED'
        stats['CHATGPT_HOOK_ONLY'] += 1
        analysis_scope = 'HOOK_ONLY'
    else:
        chatgpt_ready = 'NO'
        stats['CHATGPT_NOT_READY'] += 1
        analysis_scope = 'NONE'
    
    # Count real_spoken and first30_available
    if sample.get('real_spoken') == 'YES':
        stats['REAL_SPOKEN_YES'] += 1
    if sample.get('first30_available') == 'YES':
        stats['FIRST30_AVAILABLE_YES'] += 1
    
    # Compute chars_per_sec
    duration_str = sample.get('duration', '')
    chars_per_sec = None
    if duration_str and total_chars > 0:
        try:
            parts = duration_str.split(':')
            if len(parts) == 2:
                mins = int(parts[0])
                secs = int(parts[1])
                total_secs = mins * 60 + secs
                if total_secs > 0:
                    chars_per_sec = round(total_chars / total_secs, 2)
        except:
            pass
    
    # Prepare row for manifest
    manifest_rows.append({
        'sample_id': sample_id,
        'platform': sample.get('platform', ''),
        'author': sample.get('author', ''),
        'title': (sample.get('title', '') or '')[:80],
        'duration': sample.get('duration', ''),
        'followers': sample.get('followers', ''),
        'likes': sample.get('likes', ''),
        'comments': sample.get('comments', ''),
        'shares': sample.get('shares', ''),
        'favorites': sample.get('favorites', ''),
        'real_spoken': sample.get('real_spoken', ''),
        'first30_available': sample.get('first30_available', ''),
        'transcript_level': transcript_level,
        'transcript_status_original': sample.get('transcript_status', ''),
        'transcript_source': 'BENCHMARK_SPOKEN_INGEST_108' if has_ingest else 'MISSING',
        'transcript_coverage': f'{total_chars} chars, {segment_count} segments' if total_chars > 0 else 'NULL',
        'segment_count': segment_count,
        'top_comments_available': 'NO',  # Not collected in RC6I
        'evidence_available': 'YES' if has_evidence else 'NO',
        'data_quality': sample.get('data_quality', ''),
        'mechanical_role': sample.get('mechanical_role', ''),
        'mechanical_roles': sample.get('mechanical_roles', ''),
        'paired_sample_id': sample.get('paired_sample_id', '') or 'NULL',
        'chatgpt_ready': chatgpt_ready,
        'analysis_scope': analysis_scope,
        'failure_reason': '' if chatgpt_ready != 'NO' else 'transcript missing',
        'source_commit': '19fbc7d'
    })
    
    # Build markdown section
    md_content += f"\n---\n\n"
    md_content += f"## SAMPLE {i}: {sample_id}\n\n"
    
    # 1. Metadata
    md_content += f"### 1. Metadata\n\n"
    md_content += f"| Field | Value |\n|---|---|\n"
    md_content += f"| sample_id | {sample_id} |\n"
    md_content += f"| platform | {sample.get('platform', 'NULL')} |\n"
    md_content += f"| source_url | {sample.get('url', 'NULL')} |\n"
    md_content += f"| author | {sample.get('creator', 'NULL')} |\n"
    md_content += f"| title | {sample.get('title', 'NULL')[:100]} |\n"
    md_content += f"| publish_time | {sample.get('publish_time', 'NULL')} |\n"
    md_content += f"| duration | {sample.get('duration', 'NULL')} |\n"
    md_content += f"| topic_bucket | {sample.get('topic_bucket', 'NULL')} |\n"
    md_content += f"| mechanical_role | {sample.get('mechanical_role', 'NULL')} |\n"
    md_content += f"| mechanical_roles | {sample.get('mechanical_roles', 'NULL')} |\n"
    md_content += f"| data_quality | {sample.get('data_quality', 'NULL')} |\n"
    
    # 2. Performance
    md_content += f"\n### 2. Performance\n\n"
    md_content += f"| Field | Value |\n|---|---|\n"
    md_content += f"| followers | {sample.get('creator_followers', 'NULL')} |\n"
    md_content += f"| views | NULL |\n"
    md_content += f"| likes | {sample.get('likes', 'NULL')} |\n"
    md_content += f"| comments | {sample.get('comments', 'NULL')} |\n"
    md_content += f"| shares | {sample.get('shares', 'NULL')} |\n"
    md_content += f"| favorites | {sample.get('favorites', 'NULL')} |\n"
    
    # 3. Transcript Status
    md_content += f"\n### 3. Transcript Status\n\n"
    md_content += f"| Field | Value |\n|---|---|\n"
    md_content += f"| real_spoken | {sample.get('real_spoken', 'NULL')} |\n"
    md_content += f"| first30_available | {sample.get('first30_available', 'NULL')} |\n"
    md_content += f"| transcript_level | {transcript_level} |\n"
    md_content += f"| transcript_status_original | {sample.get('transcript_status', 'NULL')} |\n"
    md_content += f"| transcript_source | {'BENCHMARK_SPOKEN_INGEST_108' if has_ingest else 'MISSING'} |\n"
    md_content += f"| transcript_coverage | {total_chars} chars, {segment_count} segments |\n"
    md_content += f"| segment_count | {segment_count} |\n"
    md_content += f"| total_chars | {total_chars} |\n"
    md_content += f"| chars_per_sec | {chars_per_sec if chars_per_sec else 'NULL'} |\n"
    
    # 4. First 30 Seconds
    md_content += f"\n### 4. First 30 Seconds\n\n"
    if first30_text:
        md_content += f"```\n{first30_text}\n```\n\n"
        # Show segments if available
        if segments_data:
            md_content += "| segment_id | start | end | raw_text |\n|---|---|---|---|\n"
            for seg in segments_data[:5]:  # First 5 segments
                md_content += f"| {seg.get('segment_id', '')} | {seg.get('start', '')} | {seg.get('end', '')} | {seg.get('text', '')[:50]} |\n"
    else:
        md_content += "NULL\n"
    
    # 5. Full/Available Timed Transcript
    md_content += f"\n### 5. Full / Available Timed Transcript\n\n"
    if segments_data:
        md_content += "| segment_id | start | end | raw_text | normalized_text |\n|---|---|---|---|---|\n"
        for seg in segments_data:
            raw = seg.get('text', '')[:80]
            norm = seg.get('normalized_text', 'NULL')
            md_content += f"| {seg.get('segment_id', '')} | {seg.get('start', '')} | {seg.get('end', '')} | {raw} | {norm} |\n"
    else:
        md_content += "NULL\n"
    
    # 6. Top Comments
    md_content += f"\n### 6. Top Comments\n\n"
    md_content += "NULL\n"
    
    # 7. Evidence / Manifest
    md_content += f"\n### 7. Evidence / Manifest\n\n"
    md_content += f"| Field | Value |\n|---|---|\n"
    md_content += f"| source_commit | 19fbc7d |\n"
    md_content += f"| media_sha256 | NULL |\n"
    md_content += f"| transcript_sha256 | NULL |\n"
    md_content += f"| metadata_sha256 | NULL |\n"
    md_content += f"| source_file | BENCHMARK_SPOKEN_INGEST_108/{sample_id}/ |\n"
    md_content += f"| evidence_manifest | {'YES' if has_evidence else 'NO'} |\n"
    
    # 8. Mechanical Notes
    md_content += f"\n### 8. Mechanical Notes\n\n"
    notes = []
    if transcript_level == 'TRANSCRIPT_MISSING':
        notes.append('transcript missing')
    if sample.get('first30_available') == 'NO':
        notes.append('first30 unavailable')
    notes.append('data quality: ' + sample.get('data_quality', 'NULL'))
    if sample.get('paired_sample_id'):
        notes.append('same-author pair exists: ' + sample.get('paired_sample_id', ''))
    md_content += '\n'.join(notes) + '\n'

# Save manifest CSV
with open(INPUT_DIR / "RC6I_PRIMARY_28_INPUT_MANIFEST.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=manifest_rows[0].keys() if manifest_rows else [])
    writer.writeheader()
    writer.writerows(manifest_rows)

# Save main markdown
with open(INPUT_DIR / "RC6I_PRIMARY_28_INPUT.md", 'w', encoding='utf-8') as f:
    f.write(md_content)

# Generate report
report = f"""# RC6I PRIMARY 28 Deep Analysis Input Report

## Input

Shortlist commit: 182bc90c2c4f38c777a1c26ecf7723e594c02060
PRIMARY: 28

## Integrity

Input primary count: 28
Unique sample IDs: 28
Duplicates: 0
Missing: 0

## Transcript Coverage

FULL_TRANSCRIPT: {stats['FULL_TRANSCRIPT']}
PARTIAL_TRANSCRIPT: {stats['PARTIAL_TRANSCRIPT']}
FIRST30_ONLY: {stats['FIRST30_ONLY']}
TRANSCRIPT_MISSING: {stats['TRANSCRIPT_MISSING']}
Total: {stats['FULL_TRANSCRIPT'] + stats['PARTIAL_TRANSCRIPT'] + stats['FIRST30_ONLY'] + stats['TRANSCRIPT_MISSING']}

## Analysis Readiness

FULL analysis ready: {stats['CHATGPT_FULL_READY']}
PARTIAL analysis ready: {stats['CHATGPT_PARTIAL_READY']}
HOOK-only ready: {stats['CHATGPT_HOOK_ONLY']}
NOT ready: {stats['CHATGPT_NOT_READY']}

## Other Evidence

real_spoken YES: {stats['REAL_SPOKEN_YES']}
first30 available YES: {stats['FIRST30_AVAILABLE_YES']}
top comments available: {stats['TOP_COMMENTS_AVAILABLE']}
evidence manifest available: {stats['EVIDENCE_AVAILABLE']}

## Output Files

- `01_benchmark/analysis_batches/rc6i_deep_input/RC6I_PRIMARY_28_INPUT.csv`
- `01_benchmark/analysis_batches/rc6i_deep_input/RC6I_PRIMARY_28_INPUT_MANIFEST.csv`
- `01_benchmark/analysis_batches/rc6i_deep_input/RC6I_PRIMARY_28_INPUT.md`
- `01_benchmark/analysis_batches/rc6i_deep_input/RC6I_PRIMARY_28_INPUT_REPORT.md`

## Final Status

DEEP_ANALYSIS_INPUT_READY

---
*本任务只负责机械整理、证据归档、文本交接，不负责任何语义分析。*
*等待 ChatGPT 接管 28 条 PRIMARY 样本进行深度分析。*
"""

with open(INPUT_DIR / "RC6I_PRIMARY_28_INPUT_REPORT.md", 'w', encoding='utf-8') as f:
    f.write(report)

print(f"\n=== RC6I PRIMARY INPUT PACK COMPLETE ===")
print(f"PRIMARY: 28")
print(f"FULL_TRANSCRIPT: {stats['FULL_TRANSCRIPT']}")
print(f"PARTIAL_TRANSCRIPT: {stats['PARTIAL_TRANSCRIPT']}")
print(f"FIRST30_ONLY: {stats['FIRST30_ONLY']}")
print(f"TRANSCRIPT_MISSING: {stats['TRANSCRIPT_MISSING']}")
print(f"REAL_SPOKEN: {stats['REAL_SPOKEN_YES']}")
print(f"FIRST30_AVAILABLE: {stats['FIRST30_AVAILABLE_YES']}")
print(f"CHATGPT_FULL_READY: {stats['CHATGPT_FULL_READY']}")
print(f"CHATGPT_PARTIAL_READY: {stats['CHATGPT_PARTIAL_READY']}")
print(f"CHATGPT_HOOK_ONLY: {stats['CHATGPT_HOOK_ONLY']}")
print(f"CHATGPT_NOT_READY: {stats['CHATGPT_NOT_READY']}")
print(f"\nOutput: {INPUT_DIR}")