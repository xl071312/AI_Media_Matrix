#!/usr/bin/env python3
"""RC6F: Audit existing corpus samples and identify issues"""
import json
import csv
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")
CORPUS = BASE / "01_benchmark/plain_language_corpus_v1"

print("=== RC6F Corpus Audit ===\n")

# Load global registry with canonical normalization
registry = set()
registry_file = BASE / "01_benchmark/GLOBAL_CONTENT_ID_REGISTRY.csv"
if registry_file.exists():
    with open(registry_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row.get('content_id', '')
            if cid:
                # Canonical normalization: strip prefix
                canonical = cid.replace('DY_REAL_', '').replace('DY_REAL_', '').strip()
                if canonical and canonical.isdigit():
                    registry.add(canonical)

print(f"Global registry entries: {len(registry)}")

# Load raw pool candidates
raw_pool = BASE / "01_benchmark/shards/hermes_real/douyin_raw/raw_pool_all.jsonl"
candidates = []
if raw_pool.exists():
    with open(raw_pool, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    cand = json.loads(line)
                    aweme_id = str(cand.get('aweme_id', ''))
                    candidates.append(cand)
                except:
                    pass

print(f"Raw pool candidates: {len(candidates)}")

# Check existing samples
samples = sorted(CORPUS.glob("SAMPLE_*"))
print(f"\nExisting samples: {len(samples)}")

# Audit each sample
audit_results = []
for sample_dir in samples:
    sample_id = sample_dir.name
    meta_path = sample_dir / "01_metadata.json"
    trans_path = sample_dir / "03_transcript_raw.json"
    
    # Load metadata
    meta = {}
    if meta_path.exists():
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    
    content_id = str(meta.get('content_id', ''))
    canonical_id = content_id.replace('DY_REAL_', '').strip()
    
    # Check registry collision
    in_registry = canonical_id in registry if canonical_id.isdigit() else False
    
    # Check transcript
    transcript_ok = False
    transcript_chars = 0
    segments = []
    first30s_available = False
    
    if trans_path.exists():
        with open(trans_path, 'r', encoding='utf-8') as f:
            trans = json.load(f)
        segments = trans.get('segments', [])
        transcript_chars = trans.get('transcript_chars', 0)
        first30s = trans.get('first30s_text', '')
        first30s_available = len(first30s) > 20 if first30s else False
        transcript_ok = transcript_chars > 50 and len(segments) > 0
    
    # Check duration
    duration = meta.get('duration_sec')
    duration_valid = duration is not None and 30 <= duration <= 600
    
    audit_results.append({
        'sample_id': sample_id,
        'content_id': content_id,
        'canonical_id': canonical_id,
        'in_registry': in_registry,
        'transcript_ok': transcript_ok,
        'transcript_chars': transcript_chars,
        'segments_count': len(segments),
        'first30s_available': first30s_available,
        'duration': duration,
        'duration_valid': duration_valid,
        'issues': []
    })
    
    issues = []
    if in_registry:
        issues.append("DUPLICATE_IN_REGISTRY")
    if not transcript_ok:
        issues.append("EMPTY_TRANSCRIPT")
    if not first30s_available:
        issues.append("NO_FIRST30S")
    if not duration_valid:
        issues.append("INVALID_DURATION")
    
    audit_results[-1]['issues'] = issues

# Summary
duplicates = [a for a in audit_results if a['in_registry']]
empty_transcripts = [a for a in audit_results if not a['transcript_ok']]
no_first30s = [a for a in audit_results if not a['first30s_available']]
invalid_duration = [a for a in audit_results if not a['duration_valid']]

print(f"\n=== Audit Summary ===")
print(f"Total samples: {len(audit_results)}")
print(f"Duplicate in registry: {len(duplicates)}")
print(f"Empty/invalid transcript: {len(empty_transcripts)}")
print(f"No first 30s: {len(no_first30s)}")
print(f"Invalid duration: {len(invalid_duration)}")

# List issues
print(f"\n=== Samples with Issues ===")
for a in audit_results:
    if a['issues']:
        print(f"  {a['sample_id']}: {a['canonical_id']} - {', '.join(a['issues'])}")