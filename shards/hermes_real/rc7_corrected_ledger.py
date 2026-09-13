#!/usr/bin/env python3
"""Generate Corrected Global Ledger V3 with All 20 Articles"""
import json
import csv
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
OUTPUT_DIR = BASE / "analysis_batches"
SEED_DIR = OUTPUT_DIR / "batch_004_toutiao" / "SEED_WAVE_001"

print("="*70)
print("RC7: Corrected Global Ledger V3")
print("="*70)
print()

# Load existing V2 ledger
ledger_v2_path = OUTPUT_DIR / "GLOBAL_CORPUS_LEDGER_V2.csv"
with open(ledger_v2_path, 'r', encoding='utf-8') as f:
    ledger_v2 = list(csv.DictReader(f))

print(f"Loaded V2 ledger: {len(ledger_v2)} rows")

# Load all Batch004 articles
b004_articles = []
for f in SEED_DIR.glob('*.json'):
    with open(f, 'r', encoding='utf-8') as fh:
        try:
            data = json.load(fh)
            if data.get('content_id'):
                b004_articles.append(data)
        except:
            pass

print(f"Loaded Batch004 articles: {len(b004_articles)}")
print()

# Generate V3
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
        # Skip if already in V2
        if any(r.get('content_id') == cid and r.get('batch') == 'batch_004' for r in ledger_v2):
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

print("✓ Generated GLOBAL_CORPUS_LEDGER_V3.csv")
print()

# Compute final stats
with open(OUTPUT_DIR / "GLOBAL_CORPUS_LEDGER_V3.csv", 'r', encoding='utf-8') as f:
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

print("="*70)
print("FINAL STATISTICS")
print("="*70)
print()
print(f"Unique CID Union: {final_unique}")
print(f"Logic Analyzable Unique: {final_logic}/100")
print(f"Independent Logic Observations: {final_independent}")
print(f"Performance Verified: {final_perf}")
print()
print("=== BATCH BREAKDOWN ===")
print(f"Batch001 (Frozen): {b001_count} unique")
print(f"Block002: {b002_count} qualified")
print(f"Block003: {b003_count} done")
print(f"Block004: {b004_count} articles")
print()
print("=== MILESTONES ===")
print(f"Global >= 100: IN_PROGRESS ({final_logic}/100)")
print(f"Gap to 100: {100 - final_logic}")
print()
print("="*70)