#!/usr/bin/env python3
"""Final Status Report - RC5"""
from pathlib import Path
import csv
import json

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
OUTPUT_DIR = BASE / "analysis_batches"

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

b004_path = OUTPUT_DIR / "batch_004_toutiao" / "batch004_progress.json"
b004_data = []
if b004_path.exists():
    with open(b004_path, 'r', encoding='utf-8') as f:
        b004_data = json.load(f)
b004_articles = [r for r in b004_data if r.get('status') == 'DOWNLOADED']

# Global ledger
ledger_path = OUTPUT_DIR / "GLOBAL_CORPUS_LEDGER.csv"
with open(ledger_path, 'r', encoding='utf-8') as f:
    ledger_rows = list(csv.DictReader(f))

# Registry
reg_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
with open(reg_path, 'r', encoding='utf-8') as f:
    reg_cids = set(line.split(',')[0].strip().lstrip('\ufeff') for line in f if line.strip())

# Compute stats
global_unique = len(ledger_rows)
logic_analyzable = len([r for r in ledger_rows if r.get('logic_analyzable') == 'True'])
independent_logic = len([r for r in ledger_rows if r.get('independent_logic') == 'True'])
perf_verified = len([r for r in ledger_rows if r.get('performance_verified') == 'True'])

b001_count = len([r for r in ledger_rows if r.get('batch') == 'batch_001'])
b002_count = len([r for r in ledger_rows if r.get('batch') == 'batch_002'])
b003_count = len([r for r in ledger_rows if r.get('batch') == 'batch_003'])
b004_count = len([r for r in ledger_rows if r.get('batch') == 'batch_004'])

print("="*70)
print("FINAL STATUS REPORT - RC5")
print("="*70)
print()
print("=== GLOBAL ===")
print(f"Unique CID Union: {global_unique}")
print(f"Logic Analyzable Unique: {logic_analyzable}/100")
print(f"Independent Logic Observations: {independent_logic}")
print(f"Performance Verified: {perf_verified}")
print()
print("=== BATCH BREAKDOWN ===")
print(f"Batch001: {b001_count} unique")
print(f"Batch002: {b002_count} qualified")
print(f"Batch003: {b003_count} done (9/30 target)")
print(f"Batch004: {b004_count} articles (0/30 target)")
print()
print("=== STATUS ===")
print(f"Douyin Route: COOLDOWN (Rate Limited)")
print(f"Toutiao Route B: FAILED (0/10 found)")
print(f"Manual Seed Required: YES")
print()
print("=== MILESTONES ===")
print(f"Global >= 100: IN_PROGRESS ({logic_analyzable}/100)")
print(f"Batch003 >= 30: IN_PROGRESS ({b003_count}/30)")
print(f"Batch004 >= 40: BLOCKED")
print()
print("=== DELIVERABLES ===")
print("Batch002 V2:")
print("  - CORPUS_CANONICAL_MANIFEST_V2.csv")
print("  - EVIDENCE_FULL_PART_01-06.md (7196 segments)")
print("  - PERFORMANCE_METRICS.csv")
print()
print("Batch003 Interim:")
print("  - CORPUS_CANONICAL_MANIFEST_INTERIM.csv")
print("  - EVIDENCE_FULL_PART_01.md (1142 segments)")
print()
print("Global:")
print("  - GLOBAL_CORPUS_LEDGER.csv")
print("  - GLOBAL_COMPARISON_FEATURES_V2.csv")
print()
print("="*70)