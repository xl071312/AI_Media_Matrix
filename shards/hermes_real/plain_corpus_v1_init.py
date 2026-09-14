#!/usr/bin/env python3
"""Plain Language Corpus V1: Initialize dedupe tracking and manifest"""
import csv
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")
CORPUS = BASE / "01_benchmark/plain_language_corpus_v1"

# Create directories for individual samples
CORPUS.mkdir(parents=True, exist_ok=True)

# Collect existing content IDs from corpus
existing_ids = set()

# Check existing benchmark data
benchmark_paths = [
    BASE / "01_benchmark/analysis_batches",
    BASE / "01_benchmark/shards/hermes_real",
]

for bp in benchmark_paths:
    if bp.exists():
        for p in bp.rglob("*.json"):
            try:
                import json
                with open(p, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cid = data.get('content_id')
                    if cid:
                        existing_ids.add(str(cid))
            except:
                pass

# Create DEDUPE_REGISTRY.csv
dedupe_path = CORPUS / "PLAIN_LANGUAGE_CORPUS_V1_DUPLICATE_AUDIT.csv"
with open(dedupe_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['content_id', 'platform', 'existing_in_corpus', 'duplicate_status', 'source'])
    for cid in sorted(existing_ids)[:100]:  # First 100 for tracking
        writer.writerow([cid, 'UNKNOWN', True, 'EXISTING', 'corpus_registry'])

print(f"Existing content IDs in corpus: {len(existing_ids)}")
print(f"Dedupe registry created: {dedupe_path}")
print(f"Target: 30 NEW unique videos")
print(f"Corpus directory: {CORPUS}")