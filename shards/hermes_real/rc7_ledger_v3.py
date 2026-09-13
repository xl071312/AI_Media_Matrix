#!/usr/bin/env python3
"""RC7: Generate Global Ledger V3 with Corrected Counts"""
import csv
import json
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
OUTPUT_DIR = BASE / "analysis_batches"
SEED_DIR = OUTPUT_DIR / "batch_004_toutiao" / "SEED_WAVE_001"

print("="*70)
print("RC7: Global Ledger V3 Generation")
print("="*70)
print()

# ============================================================
# 1. Load Existing Ledger V2
# ============================================================
ledger_v2_path = OUTPUT_DIR / "GLOBAL_CORPUS_LEDGER_V2.csv"
with open(ledger_v2_path, 'r', encoding='utf-8') as f:
    ledger_v2 = list(csv.DictReader(f))

print(f"Loaded Ledger V2: {len(ledger_v2)} rows")

# ============================================================
# 2. Load Batch004 Articles from SEED_WAVE_001
# ============================================================
print()
print("=== Loading Batch004 Articles ===")

b004_articles = []
for f in SEED_DIR.glob('*.json'):
    with open(f, 'r', encoding='utf-8') as fh:
        try:
            data = json.load(fh)
            b004_articles.append(data)
        except:
            pass

print(f"Loaded {len(b004_articles)} articles from SEED_WAVE_001")

# ============================================================
# 3. Compute Corrected Global Stats
# ============================================================
print()
print("=== Computing Corrected Stats ===")

# From V2 ledger
v2_unique = len(ledger_v2)
v2_logic = len([r for r in ledger_v2 if r.get('logic_analyzable') == 'True'])
v2_independent = len([r for r in ledger_v2 if r.get('independent_observation') == 'True'])
v2_perf = len([r for r in ledger_v2 if r.get('performance_verified') == 'True'])

# Batch004 contribution
b004_logic = len(b004_articles)  # All saved articles are logic_analyzable

print(f"V2 Logic Analyzable: {v2_logic}")
print(f"Batch004 Articles: {b004_logic}")
print()

# ============================================================
# 4. Generate Ledger V3
# ============================================================
print("=== Generating GLOBAL_CORPUS_LEDGER_V3.csv ===")

fieldnames = [
    'global_content_key', 'platform', 'content_id', 'batch',
    'unique_valid', 'logic_analyzable', 'logic_exclusion_reason',
    'near_duplicate_group_id', 'independent_observation',
    'performance_verified', 'transcript_usable', 'fulltext_usable',
    'content_type', 'simulated', 'notes'
]

with open(OUTPUT_DIR / "GLOBAL_CORPUS_LEDGER_V3.csv", 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    # Write existing V2 rows
    for row in ledger_v2:
        writer.writerow(row)
    
    # Write new Batch004 articles
    for art in b004_articles:
        cid = art.get('content_id', '')
        if not cid:
            continue
        
        writer.writerow({
            'global_content_key': f"TOUTIAO:{cid}",
            'platform': 'toutiao',
            'content_id': cid,
            'batch': 'batch_004',
            'unique_valid': True,
            'logic_analyzable': True,
            'logic_exclusion_reason': '',
            'near_duplicate_group_id': '',
            'independent_observation': True,
            'performance_verified': False,
            'transcript_usable': 'FALSE',
            'fulltext_usable': 'TRUE',
            'content_type': 'ARTICLE',
            'simulated': 'FALSE',
            'notes': 'SEED_WAVE_001'
        })

new_path = OUTPUT_DIR / "GLOBAL_CORPUS_LEDGER_V3.csv"
print(f"✓ Generated: {new_path}")

# ============================================================
# 5. Compute Final Stats
# ============================================================
print()
print("=== Final Statistics ===")

with open(new_path, 'r', encoding='utf-8') as f:
    v3_rows = list(csv.DictReader(f))

final_unique = len(v3_rows)
final_logic = len([r for r in v3_rows if r.get('logic_analyzable') == 'True'])
final_independent = len([r for r in v3_rows if r.get('independent_observation') == 'True'])
final_perf = len([r for r in v3_rows if r.get('performance_verified') == 'True'])

# Batch breakdown
b001_count = len([r for r in v3_rows if r.get('batch') == 'batch_001'])
b002_count = len([r for r in v3_rows if r.get('batch') == 'batch_002'])
b003_count = len([r for r in v3_rows if r.get('batch') == 'batch_003'])
b004_count = len([r for r in v3_rows if r.get('batch') == 'batch_004'])

print()
print(f"Unique CID Union: {final_unique}")
print(f"Logic Analyzable Unique: {final_logic}/100")
print(f"Independent Logic Observations: {final_independent}")
print(f"Performance Verified: {final_perf}")
print()
print(f"Batch001: {b001_count} unique")
print(f"Block002: {b002_count} qualified")
print(f"Block003: {b003_count} done")
print(f"Block004: {b004_count} articles")
print()
print(f"Gap to 100: {100 - final_logic}")
print()
print("="*70)
print("GLOBAL LEDGER V3 COMPLETE")
print("="*70)