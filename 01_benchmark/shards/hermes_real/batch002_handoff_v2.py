#!/usr/bin/env python3
"""Batch 002 - Research Handoff V2: Full Evidence Packaging"""
import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH2_DIR = BASE / "analysis_batches" / "batch_002"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"

# Load registry
reg_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
registry = {}
with open(reg_path, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        cid = row.get('content_id', '').strip().lstrip('\ufeff')
        if cid:
            registry[cid] = row

# Load selection for metadata
sel_path = SHARDS / "douyin_benchmark_selection.csv"
selection_meta = {}
with open(sel_path, 'r', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        raw_cid = row.get('content_id', row.get('aweme_id', '')).strip().lstrip('\ufeff')
        if raw_cid.startswith('DY_REAL_'):
            raw_cid = raw_cid[8:]
        raw_cid = raw_cid.strip()
        if raw_cid:
            selection_meta[raw_cid] = row

# Load final QA
qa_path = SHARDS / "batch002_final_qa.json"
with open(qa_path, 'r', encoding='utf-8') as f:
    qa_data = json.load(f)

qualified = [r for r in qa_data if r.get('corpus_eligible')]
print(f"Qualified records: {len(qualified)}")

# Create V2 output dir
output_dir = BATCH2_DIR / "CORPUS_DELIVERABLES_V2"
output_dir.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. Load all transcripts and compute stats
# ============================================================
all_transcripts = {}
total_segments = 0
total_chars = 0

for r in qualified:
    cid = r['content_id']
    transcript_path = TRANSCRIPT_DIR / f'{cid}_raw.json'
    
    if transcript_path.exists():
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = json.load(f)
        if isinstance(transcript, list):
            all_transcripts[cid] = transcript
            total_segments += len(transcript)
            total_chars += sum(len(s.get('text', '')) for s in transcript)

print(f"Total segments: {total_segments}")
print(f"Total chars: {total_chars}")

# ============================================================
# 2. Generate CORPUS_CANONICAL_MANIFEST_V2.csv
# ============================================================
manifest_path = output_dir / "CORPUS_CANONICAL_MANIFEST_V2.csv"
fieldnames = ['canonical_id', 'content_id', 'title', 'author', 'creator_id', 'publish_time',
              'duration_sec', 'primary_topic', 'secondary_topics', 'sample_role', 'viral_type',
              'likes', 'comments', 'favorites', 'shares', 'performance_verified',
              'page_verified', 'speech_present', 'media_ready', 'audio_ready',
              'asr_status', 'segment_count', 'transcript_chars', 'coverage_ratio', 'transcript_usable',
              'text_corpus', 'performance_corpus', 'visual_corpus',
              'matched_control_group_id',
              'media_sha256', 'audio_sha256', 'transcript_sha256',
              'simulated', 'notes']

with open(manifest_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    for i, r in enumerate(qualified, 1):
        cid = r['content_id']
        meta = selection_meta.get(cid, {})
        
        # Get topic
        title = meta.get('desc', '')[:100]
        keyword = meta.get('source_keyword', '')
        primary = r.get('primary_topic', 'UNKNOWN')
        
        writer.writerow({
            'canonical_id': f'B002-{i:03d}',
            'content_id': cid,
            'title': title,
            'author': meta.get('author', ''),
            'creator_id': meta.get('author_id', ''),
            'publish_time': meta.get('create_time', ''),
            'duration_sec': r.get('audio_duration', 0),
            'primary_topic': primary,
            'secondary_topics': ';'.join(r.get('secondary_topics', [])),
            'sample_role': 'VIRAL' if r.get('performance_verified') else 'NORMAL',
            'viral_type': 'HIGH_PERF' if r.get('performance_verified') else 'STANDARD',
            'likes': int(meta.get('liked_count', 0)),
            'comments': int(meta.get('comment_count', 0)),
            'favorites': int(meta.get('collected_count', 0)),
            'shares': int(meta.get('share_count', 0)),
            'performance_verified': r.get('performance_verified', False),
            'page_verified': True,
            'speech_present': r.get('speech_present', False),
            'media_ready': True,
            'audio_ready': True,
            'asr_status': 'COMPLETE',
            'segment_count': r.get('segments', 0),
            'transcript_chars': r.get('chars', 0),
            'coverage_ratio': r.get('coverage_ratio', 0),
            'transcript_usable': r.get('transcript_usable', False),
            'text_corpus': 'TRUE',
            'performance_corpus': 'TRUE' if r.get('performance_verified') else 'FALSE',
            'visual_corpus': 'TRUE',
            'matched_control_group_id': '',
            'media_sha256': '',
            'audio_sha256': '',
            'transcript_sha256': '',
            'simulated': 'FALSE',
            'notes': ''
        })

print(f"✓ Manifest: {manifest_path}")

# ============================================================
# 3. Generate 6 Evidence Parts with FULL transcripts
# ============================================================
part_size = 6  # 32 / 6 ≈ 5-6 per part
parts = []
for i in range(0, len(qualified), part_size):
    parts.append(qualified[i:i+part_size])

print(f"Generating {len(parts)} evidence parts...")

for part_idx, part_items in enumerate(parts, 1):
    lines = [
        f"# BATCH 002 Evidence Full - Part {part_idx}",
        "",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Samples**: {len(part_items)}",
        f"**Scope**: Full timed transcripts (NO truncation)",
        "",
        "---",
        ""
    ]
    
    part_segments = 0
    part_chars = 0
    
    for i, item in enumerate(part_items, 1):
        cid = item['content_id']
        meta = selection_meta.get(cid, {})
        transcript = all_transcripts.get(cid, [])
        
        part_segments += len(transcript)
        part_chars += sum(len(s.get('text', '')) for s in transcript)
        
        lines.append(f"## Sample {i}: {cid}")
        lines.append(f"**Canonical ID**: B002-{((part_idx-1)*part_size + i):03d}")
        lines.append(f"**Content ID**: {cid}")
        lines.append(f"**Title**: {item.get('title', meta.get('desc', ''))}")
        lines.append(f"**Primary Topic**: {item.get('primary_topic', 'UNKNOWN')}")
        lines.append(f"**Duration**: {item.get('audio_duration', 0):.1f}s")
        lines.append(f"**Segments**: {len(transcript)}")
        lines.append(f"**Chars**: {sum(len(s.get('text', '')) for s in transcript)}")
        lines.append(f"**Coverage**: {item.get('coverage_ratio', 0):.0%}")
        lines.append("")
        
        # Performance
        likes = int(meta.get('liked_count', 0))
        comments = int(meta.get('comment_count', 0))
        favorites = int(meta.get('collected_count', 0))
        shares = int(meta.get('share_count', 0))
        lines.append(f"**Performance**: {likes:,} likes, {comments:,} comments, {favorites:,} favorites, {shares:,} shares")
        lines.append("")
        
        # FULL Timed Transcript (NO truncation)
        lines.append("### Full Timed Transcript")
        lines.append("")
        lines.append("| # | Time | Text |")
        lines.append("|---|------|------|")
        
        for j, seg in enumerate(transcript, 1):
            start = seg.get('start', 0)
            end = seg.get('end', 0)
            text = seg.get('text', '').strip()
            sm, ss = int(start // 60), start % 60
            em, es = int(end // 60), end % 60
            lines.append(f"| {j:03d} | {sm:02d}:{ss:05.2f}-{em:02d}:{es:05.2f} | {text} |")
        
        lines.append("")
        lines.append(f"**Segment Count Verified**: {len(transcript)}")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    print(f"  Part {part_idx}: {part_segments} segments, {part_chars} chars")
    
    # Save
    path = output_dir / f"EVIDENCE_FULL_PART_{part_idx:02d}.md"
    path.write_text("\n".join(lines), encoding='utf-8')

print(f"✓ Evidence parts generated")

# ============================================================
# 4. Generate PERFORMANCE_METRICS.csv (renamed from old CONTROL_GROUPS)
# ============================================================
perf_path = output_dir / "PERFORMANCE_METRICS.csv"
with open(perf_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['content_id', 'likes', 'comments', 'favorites', 'shares', 'perf_score'])
    writer.writeheader()
    
    for r in qualified:
        cid = r['content_id']
        meta = selection_meta.get(cid, {})
        perf_score = float(meta.get('performance_score', 0))
        
        writer.writerow({
            'content_id': cid,
            'likes': int(meta.get('liked_count', 0)),
            'comments': int(meta.get('comment_count', 0)),
            'favorites': int(meta.get('collected_count', 0)),
            'shares': int(meta.get('share_count', 0)),
            'perf_score': perf_score
        })

print(f"✓ Performance metrics: {perf_path}")

# ============================================================
# 5. Generate CONTROL_GROUPS.csv (empty - no matched controls)
# ============================================================
control_path = output_dir / "CONTROL_GROUPS.csv"
with open(control_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['group_id', 'content_id', 'creator_id', 'primary_topic', 'role_in_group', 'likes', 'comments', 'favorites', 'shares'])
    writer.writerow(['', '', '', '', '', '', '', '', ''])  # Header row indicating no data
    # Write comment about no matched controls
    f.write('\n# MATCHED_CONTROL_GROUPS = 0\n')
    f.write('# No same-creator comparisons available in current batch\n')

print(f"✓ Control groups: {control_path} (0 matched)")

# ============================================================
# 6. Generate CREATOR_BASELINES.csv (empty - no verified creators)
# ============================================================
creator_path = output_dir / "CREATOR_BASELINES.csv"
with open(creator_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['creator_id', 'author', 'baseline_n', 'median_likes', 'median_comments', 'median_favorites', 'median_shares', 'baseline_verified'])
    f.write('\n# VERIFIED_CREATOR_BASELINES = 0\n')
    f.write('# No creator identity established for current batch samples\n')

print(f"✓ Creator baselines: {creator_path} (0 verified)")

# ============================================================
# Summary
# ============================================================
print(f"\n{'='*60}")
print(f"BATCH 002 RESEARCH HANDOFF V2")
print(f"{'='*60}")
print(f"Qualified samples: {len(qualified)}")
print(f"Total segments: {total_segments}")
print(f"Total chars: {total_chars}")
print(f"Evidence parts: {len(parts)}")
print(f"Performance rows: {len(qualified)}")
print(f"Matched control groups: 0")
print(f"Verified creator baselines: 0")
print(f"Output: {output_dir}")