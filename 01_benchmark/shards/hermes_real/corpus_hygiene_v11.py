#!/usr/bin/env python3
"""
Corpus Hygiene V1.1 - Final Patch & Freeze
Only field corrections, no new ASR/data collection
"""
import json
import csv
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
BATCH = BASE / "analysis_batches" / "batch_001"
INPUT = BATCH / "CORPUS_CANONICAL_MANIFEST_V1.csv"
OUTPUT = BATCH / "CORPUS_CANONICAL_MANIFEST_V1_1.csv"
FREEZE = BATCH / "BATCH_001_CORPUS_STATUS.txt"

def main():
    print("=== CORPUS HYGIENE V1.1 - FINAL PATCH ===\n")
    
    with open(INPUT, encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    
    print(f"Input rows: {len(rows)}")
    
    # Fixes
    RELATIVE_BREAKOUT_CID = '7647797848847439706'
    UNKNOWN_PERF_CID = '7302348364815928612'
    NEAR_DUP_GROUP = ['7599692006406786358', '7680857899472843515']
    
    fixes = 0
    
    for row in rows:
        cid = row['content_id']
        
        # Fix 1: RELATIVE_BREAKOUT → RELATIVE_BREAKOUT_CANDIDATE
        if cid == RELATIVE_BREAKOUT_CID:
            row['sample_role'] = 'RELATIVE_BREAKOUT_CANDIDATE'
            if row.get('notes'):
                row['notes'] += ' | RELATIVE_BREAKOUT_CANDIDATE'
            else:
                row['notes'] = 'RELATIVE_BREAKOUT_CANDIDATE - No creator baseline yet'
            fixes += 1
        
        # Fix 2: likes=0 → likes=NULL for external data
        if cid == UNKNOWN_PERF_CID:
            row['likes'] = 'NULL'
            row['performance_verified'] = 'FALSE'
            fixes += 1
        
        # Fix 3: Split logic_analyzable into boolean + reason
        la = row['logic_analyzable']
        if la == 'TRUE':
            row['logic_analyzable'] = 'TRUE'
            row['logic_exclusion_reason'] = 'NULL'
        elif la == 'FALSE_TRANSCRIPT_EMPTY':
            row['logic_analyzable'] = 'FALSE'
            row['logic_exclusion_reason'] = 'TRANSCRIPT_EMPTY'
        elif la == 'FALSE_ASR_CORRUPTED':
            row['logic_analyzable'] = 'FALSE'
            row['logic_exclusion_reason'] = 'ASR_CORRUPTED'
        elif la == 'FALSE_ASR_UNUSABLE':
            row['logic_analyzable'] = 'FALSE'
            row['logic_exclusion_reason'] = 'ASR_UNUSABLE'
        elif la == 'FALSE_INSUFFICIENT_CONTENT':
            row['logic_analyzable'] = 'FALSE'
            row['logic_exclusion_reason'] = 'INSUFFICIENT_CONTENT'
        elif la == 'FALSE_INCOMPLETE':
            row['logic_analyzable'] = 'FALSE'
            row['logic_exclusion_reason'] = 'TRANSCRIPT_INCOMPLETE'
        else:
            row['logic_exclusion_reason'] = 'NULL'
        
        # Fix 4: Add metadata_complete
        title = row.get('viral_type', '')
        author = row.get('sample_role', '')
        if title and title != 'NULL' and author and author != 'NULL':
            row['metadata_complete'] = 'TRUE'
        else:
            row['metadata_complete'] = 'FALSE'
        
        # Fix 5: Near duplicate group
        if cid in NEAR_DUP_GROUP:
            row['near_duplicate'] = 'TRUE'
            row['near_duplicate_group'] = 'NDG001'
        else:
            row['near_duplicate_group'] = 'NULL'
    
    # Collect all unique fieldnames from all rows
    all_fields = set()
    for row in rows:
        all_fields.update(row.keys())
    all_fields = sorted(all_fields)
    
    # Write V1.1
    with open(OUTPUT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=all_fields)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Fixes applied: {fixes}")
    print(f"Output: {OUTPUT} ({OUTPUT.stat().st_size} bytes)")
    
    # Freeze status
    ANALYZABLE = sum(1 for r in rows if r['logic_analyzable'] == 'TRUE')
    INDEP_OBS = ANALYZABLE - 1  # Subtract near-dup group count
    VERIFIED = sum(1 for r in rows if r['performance_verified'] == 'TRUE')
    META_COMPLETE = sum(1 for r in rows if r.get('metadata_complete') == 'TRUE')
    NEAR_DUP_GROUPS = sum(1 for r in rows if r.get('near_duplicate_group') == 'NDG001') // 2
    EXCLUDED = sum(1 for r in rows if r['logic_analyzable'] == 'FALSE')
    
    from datetime import datetime
    FREEZE.write_text(f"""BATCH_001_CORPUS_STATUS = FROZEN_FOR_LOGIC_RESEARCH
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} GMT+8
Manifest: CORPUS_CANONICAL_MANIFEST_V1_1.csv

Unique Content IDs: {len(rows)}
Logic Analyzable: {ANALYZABLE}
Independent Logic Observations: {INDEP_OBS}
Verified Performance: {VERIFIED}
Metadata Complete: {META_COMPLETE}
Near Duplicate Groups: {NEAR_DUP_GROUPS}
Excluded Samples: {EXCLUDED}

Status: FROZEN
No further ASR, collection, or analysis permitted.
""", encoding='utf-8')
    
    print(f"\n=== CORPUS HYGIENE V1.1 REPORT ===")
    print(f"Unique Content IDs: {len(rows)}")
    print(f"Logic Analyzable: {ANALYZABLE}")
    print(f"Independent Logic Observations: {INDEP_OBS}")
    print(f"Verified Performance: {VERIFIED}")
    print(f"Metadata Complete: {META_COMPLETE}")
    print(f"Near Duplicate Groups: {NEAR_DUP_GROUPS}")
    print(f"Excluded Samples: {EXCLUDED}")
    print(f"\nStatus: FROZEN_FOR_LOGIC_RESEARCH")

if __name__ == "__main__":
    main()
