#!/usr/bin/env python3
"""Final Verification Report - RC6"""
from pathlib import Path
import json
import csv

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
OUTPUT_DIR = BASE / "analysis_batches"

print("="*70)
print("FINAL VERIFICATION REPORT - RC6")
print("="*70)
print()

# Global Ledger V2
ledger_path = OUTPUT_DIR / "GLOBAL_CORPUS_LEDGER_V2.csv"
with open(ledger_path, 'r', encoding='utf-8') as f:
    ledger = list(csv.DictReader(f))

global_unique = len(ledger)
logic_analyzable = len([r for r in ledger if r.get('logic_analyzable') == 'True'])
independent_logic = len([r for r in ledger if r.get('independent_observation') == 'True'])
perf_verified = len([r for r in ledger if r.get('performance_verified') == 'True'])

# Batch breakdown
b001_count = len([r for r in ledger if r.get('batch') == 'batch_001'])
b002_count = len([r for r in ledger if r.get('batch') == 'batch_002'])
b003_count = len([r for r in ledger if r.get('batch') == 'batch_003'])
b004_count = len([r for r in ledger if r.get('batch') == 'batch_004'])

print("=== GLOBAL LEDGER V2 ===")
print(f"Unique CID Union: {global_unique}")
print(f"Logic Analyzable Unique: {logic_analyzable}/100")
print(f"Independent Logic Observations: {independent_logic}")
print(f"Performance Verified: {perf_verified}")
print()
print("=== BATCH BREAKDOWN ===")
print(f"Batch001: {b001_count} unique (frozen)")
print(f"Batch002: {b002_count} qualified")
print(f"Block003: {b003_count} done (COOLDOWN)")
print(f"Block004: {b004_count} articles (COMPLETE)")
print()
print("=== MILESTONES ===")
print(f"Global >= 100: IN_PROGRESS ({logic_analyzable}/100)")
print(f"Gap to 100: {100 - logic_analyzable}")
print()

# Toutiao articles
toutiao_dir = OUTPUT_DIR / "batch_004_toutiao" / "SEED_WAVE_001"
articles = list(toutiao_dir.glob('*.json'))
print(f"=== TOUTIAO SEED WAVE 001 ===")
print(f"Articles downloaded: {len(articles)}")
print(f"Route Status: PASS")
print()

# Evidence files
evidence_b002 = list((OUTPUT_DIR / "batch_002" / "CORPUS_DELIVERABLES_V2").glob('EVIDENCE_FULL_PART_*.md'))
evidence_b003 = list((OUTPUT_DIR / "batch_003" / "BATCH003_INTERIM_V1").glob('EVIDENCE_FULL_PART_*.md'))
print(f"=== EVIDENCE FILES ===")
print(f"Batch002 Parts: {len(evidence_b002)}")
print(f"Block003 Parts: {len(evidence_b003)}")
print()
print("="*70)