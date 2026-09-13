#!/usr/bin/env python3
"""Finalize Batch 002 and prepare for Batch 003"""
import json
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH2_DIR = BASE / "analysis_batches" / "batch_002"

# Load final QA
qa_path = SHARDS / "batch002_final_qa.json"
with open(qa_path, 'r', encoding='utf-8') as f:
    qa_data = json.load(f)

qualified = [r for r in qa_data if r.get('corpus_eligible')]
print(f"Batch002 Qualified: {len(qualified)}")

# Load registry
reg_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
import csv
registry = {}
with open(reg_path, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        cid = row.get('content_id', '').strip().lstrip('\ufeff')
        if cid:
            registry[cid] = row

# Check overlap
existing_in_reg = sum(1 for r in qualified if r['content_id'] in registry)
new_to_registry = len(qualified) - existing_in_reg
print(f"Already in registry: {existing_in_reg}")
print(f"New to add: {new_to_registry}")

# Show Batch001 vs Batch002
b001_cids = set()
b002_new_cids = []

for r in qualified:
    cid = r['content_id']
    if cid in registry:
        b001_cids.add(cid)
    else:
        b002_new_cids.append(cid)

print(f"\nBatch001 overlap: {len(b001_cids)}")
print(f"New Batch002 only: {len(b002_new_cids)}")

# Update registry with new CIDs
if b002_new_cids:
    with open(reg_path, 'a', encoding='utf-8') as f:
        for cid in b002_new_cids:
            f.write(f"{cid},BATCH002,BATCH002,douyin,FALSE,CANONICAL,,NEW_UNIQUE,1,batch_002\n")
    print(f"\nAdded {len(b002_new_cids)} new entries to registry")

# Final count
with open(reg_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    final_rows = list(reader)
final_cids = set(r['content_id'] for r in final_rows if r.get('content_id'))
print(f"Final registry unique: {len(final_cids)}")