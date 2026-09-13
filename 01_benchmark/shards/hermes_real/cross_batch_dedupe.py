#!/usr/bin/env python3
"""
Cross-Batch Deduplication - Build Global Registry
HERMES Role: DATA ENGINEER ONLY
"""
import json
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
BATCH_DIR = BASE / "analysis_batches"

def main():
    print("=== CROSS-BATCH DEDUPLICATION ===\n")
    
    # Collect all samples from all batches
    all_entries = []
    batch_info = {}
    
    for batch in sorted(BATCH_DIR.glob("batch_*")):
        batch_name = batch.name
        batch_info[batch_name] = {'samples': 0, 'unique_cids': set()}
        
        for s in sorted(batch.glob("sample_*")):
            try:
                meta = json.load(open(s / "01_metadata.json"))
                cid = meta.get('content_id', '')
                if not cid:
                    continue
                
                entry = {
                    'content_id': cid,
                    'batch': batch_name,
                    'sample_id': s.name,
                    'viral_type': meta.get('viral_type', 'NULL'),
                    'sample_role': meta.get('sample_role', 'NULL'),
                    'duration_sec': meta.get('duration_sec', 0),
                    'segment_count': json.load(open(s / "08_evidence_manifest.json")).get('segment_count', 0),
                    'transcript_complete': json.load(open(s / "08_evidence_manifest.json")).get('segment_count', 0) > 0
                }
                all_entries.append(entry)
                batch_info[batch_name]['samples'] += 1
                batch_info[batch_name]['unique_cids'].add(cid)
            except Exception as e:
                print(f"  Error in {batch_name}/{s.name}: {e}")
    
    # Find duplicates across batches
    cid_to_batches = {}
    for entry in all_entries:
        cid = entry['content_id']
        if cid not in cid_to_batches:
            cid_to_batches[cid] = []
        cid_to_batches[cid].append(entry)
    
    # Mark duplicates
    duplicates = []
    for cid, entries in cid_to_batches.items():
        if len(entries) > 1:
            # First occurrence is canonical
            entries[0]['canonical_status'] = 'CANONICAL'
            entries[0]['first_seen_batch'] = entries[0]['batch']
            for e in entries[1:]:
                e['canonical_status'] = 'CARRYOVER_REFERENCE'
                e['duplicate_across_batch'] = True
                duplicates.append(e)
    
    print(f"Total entries: {len(all_entries)}")
    print(f"Unique CIDs: {len(cid_to_batches)}")
    print(f"Cross-batch duplicates: {len(duplicates)}")
    
    # Generate GLOBAL_CONTENT_ID_REGISTRY.csv
    output_rows = []
    for cid, entries in cid_to_batches.items():
        canonical = entries[0]
        output_rows.append({
            'content_id': cid,
            'first_seen_batch': canonical['first_seen_batch'],
            'current_batch': canonical['batch'],
            'platform': 'douyin',
            'duplicate_across_batch': 'TRUE' if len(entries) > 1 else 'FALSE',
            'canonical_status': 'CANONICAL',
            'viral_type': canonical['viral_type'],
            'sample_role': canonical['sample_role'],
            'total_appearances': len(entries),
            'all_batches': '|'.join(e['batch'] for e in entries)
        })
    
    registry_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
    with open(registry_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'content_id', 'first_seen_batch', 'current_batch', 'platform',
            'duplicate_across_batch', 'canonical_status', 'viral_type',
            'sample_role', 'total_appearances', 'all_batches'
        ])
        writer.writeheader()
        writer.writerows(output_rows)
    
    print(f"\nRegistry: {registry_path}")
    
    # Summary
    print(f"\n=== BUDGET ANALYSIS ===")
    print(f"Batch 001 unique: {len(batch_info.get('batch_001', {}).get('unique_cids', set()))}")
    print(f"New unique needed for Batch 002: 30")
    print(f"Total unique available: {len(cid_to_batches)}")
    
    # Generate control groups detection
    print(f"\n=== CONTROL GROUP DETECTION ===")
    creator_to_cids = {}
    for entry in all_entries:
        # Use viral_type as proxy for creator grouping (need better creator_id)
        vt = entry['viral_type']
        if vt not in creator_to_cids:
            creator_to_cids[vt] = []
        creator_to_cids[vt].append(entry['content_id'])
    
    for vt, cids in creator_to_cids.items():
        if len(cids) > 1:
            print(f"  {vt}: {len(cids)} samples")
    
    return cid_to_batches

if __name__ == "__main__":
    main()
