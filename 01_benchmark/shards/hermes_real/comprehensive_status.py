#!/usr/bin/env python3
"""Generate Comprehensive Status Report"""
from pathlib import Path
import json
import csv

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"

# Load data
b002_path = SHARDS / "batch002_final_qa.json"
with open(b002_path, 'r', encoding='utf-8') as f:
    b002_data = json.load(f)
b002_qualified = [r for r in b002_data if r.get('corpus_eligible')]

b003_path = SHARDS / "batch003_progress.json"
with open(b003_path, 'r', encoding='utf-8') as f:
    b003_data = json.load(f)
b003_done = [r for r in b003_data if r.get('status') == 'DONE']
b003_blocked = [r for r in b003_data if r.get('status') == 'BLOCKED']

b004_path = BASE / "analysis_batches" / "batch_004_toutiao" / "batch004_progress.json"
b004_data = []
if b004_path.exists():
    with open(b004_path, 'r', encoding='utf-8') as f:
        b004_data = json.load(f)
b004_articles = [r for r in b004_data if r.get('status') == 'DOWNLOADED']

# Global features
global_path = BASE / "analysis_batches" / "GLOBAL_COMPARISON_FEATURES.csv"
with open(global_path, 'r', encoding='utf-8') as f:
    global_rows = list(csv.DictReader(f))

# Registry
reg_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
with open(reg_path, 'r', encoding='utf-8') as f:
    reg_cids = set(line.split(',')[0].strip().lstrip('\ufeff') for line in f if line.strip())

print("="*70)
print("COMPREHENSIVE STATUS REPORT - DUAL TRACK MODE")
print("="*70)
print()

print("=== BATCH 002 (FROZEN) ===")
print(f"Qualified: {len(b002_qualified)}")
print(f"Evidence Parts: 6 (7196 segments)")
print(f"Status: COMPLETE/FROZEN")
print()

print("=== BATCH 003 (Douyin - COOLDOWN) ===")
print(f"Interim Handoff: 9/9 packaged")
print(f"Total Processed: {len(b003_data)}")
print(f"ASR Complete: {len(b003_done)}")
print(f"Blocked/Deferred: {len(b003_blocked)}")
print(f"Target: 30")
print(f"Gap: {max(0, 30 - len(b003_done))}")
print(f"Status: ACQUISITION_COOLDOWN (Rate Limited)")
print()

print("=== BATCH 004 (Toutiao) ===")
print(f"Articles Downloaded: {len(b004_articles)}")
print(f"Target: 30 articles + 10 videos")
print(f"Status: IN_PROGRESS (Timeout/Blocking)")
print()

print("=== GLOBAL COMPILATION ===")
print(f"Global Qualified Unique: {len(global_rows)}")
print(f"  - Batch002: {len([r for r in global_rows if r.get('batch') == 'batch_002'])}")
print(f"  - Batch003: {len([r for r in global_rows if r.get('batch') == 'batch_003'])}")
print(f"  - Batch004: {len([r for r in global_rows if r.get('batch') == 'batch_004'])}")
print(f"Global Registry CIDs: {len(reg_cids)}")
print()

print("=== MILESTONES ===")
print(f"Global Qualified >= 100: {'ACHIEVED' if len(global_rows) >= 100 else f'IN_PROGRESS ({len(global_rows)}/100)'}")
print(f"Batch003 >= 30: {'ACHIEVED' if len(b003_done) >= 30 else f'IN_PROGRESS ({len(b003_done)}/30)'}")
print(f"Batch004 >= 40: {'ACHIEVED' if len(b004_articles) >= 40 else f'IN_PROGRESS ({len(b004_articles)}/40)'}")
print()

print("=== BLOCKERS ===")
print(f"Douyin Rate Limit: ACTIVE")
print(f"Toutiao Access: TIMEOUT/BLOCKED")
print()

print("="*70)
print("DELIVERABLES GENERATED")
print("="*70)
print()
print("Batch002 V2:")
print("  - CORPUS_CANONICAL_MANIFEST_V2.csv")
print("  - EVIDENCE_FULL_PART_01-06.md (7196 segments)")
print("  - PERFORMANCE_METRICS.csv")
print()
print("Batch003 Interim:")
print("  - CORPUS_CANONICAL_MANIFEST_INTERIM.csv")
print("  - EVIDENCE_FULL_PART_01.md (1142 segments)")
print("  - PERFORMANCE_METRICS_INTERIM.csv")
print()
print("Global:")
print("  - GLOBAL_COMPARISON_FEATURES.csv")
print("  - SAME_TOPIC_PAIR_CANDIDATES.csv")
print()
print("="*70)
print("NEXT ACTIONS")
print("="*70)
print()
print("1. Wait 2-4 hours for Douyin rate limit reset")
print("2. Retry Toutiao with alternative approach")
print("3. Continue Batch003 when cooldown ends")
print("4. Target: 100 global qualified unique")