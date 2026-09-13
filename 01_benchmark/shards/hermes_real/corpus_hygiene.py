#!/usr/bin/env python3
"""
Batch 001 Corpus Hygiene - Data Governance Only
- Fix primary keys
- Deduplicate
- Tag problem samples
- Generate canonical manifest
"""
import json
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
BATCH_DIR = BASE / "analysis_batches" / "batch_001"
REPACK_DIR = BATCH_DIR / "repack"
SHARDS = BASE / "shards" / "hermes_real"

# Load selection data for metadata recovery
with open(SHARDS / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    selection = {row.get('aweme_id'): row for row in reader}

def main():
    print("=== CORPUS HYGIENE - DATA GOVERNANCE ===\n")
    
    # Collect all sample data
    samples = []
    for s in sorted(BATCH_DIR.glob("sample_*")):
        try:
            meta = json.load(open(s / "01_metadata.json"))
            perf = json.load(open(s / "02_performance.json"))
            manifest = json.load(open(s / "08_evidence_manifest.json"))
            
            cid = meta.get('content_id', '')
            if not cid:
                continue
            
            # Check transcript
            trans_file = s / "05_transcript_raw.md"
            transcript_complete = False
            embedded_segs = 0
            if trans_file.exists():
                with open(trans_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    import re
                    embedded_segs = len(re.findall(r'\[S\d{4}\]', content))
                    transcript_complete = embedded_segs == manifest.get('segment_count', 0) and manifest.get('segment_count', 0) > 0
            
            # Recover metadata from selection
            row = selection.get(cid)
            recovered_meta = {}
            if row:
                if meta.get('title') in ['TBD', 'NULL', '']:
                    recovered_meta['title'] = row.get('desc', '')[:150] or None
                if meta.get('creator_name') in ['TBD', 'NULL', '']:
                    recovered_meta['creator_name'] = row.get('nickname', '') or None
                if meta.get('topic') in ['TBD', 'NULL', '']:
                    recovered_meta['topic'] = row.get('source_keyword', '') or None
                if meta.get('viral_type') in ['UNKNOWN', 'NULL', '']:
                    viral_raw = row.get('viral_type', '')
                    recovered_meta['viral_type'] = viral_raw.split(';')[0] if ';' in viral_raw else (viral_raw or None)
                if meta.get('sample_role') in ['EXTERNAL_DATA', 'NULL', '']:
                    recovered_meta['sample_role'] = row.get('sample_role', '') or None
                
                # Recover performance
                likes = int(row.get('liked_count', 0)) if row.get('liked_count') else None
                if isinstance(perf.get('likes'), int) and perf.get('likes', 0) == 0 and likes:
                    perf['likes'] = likes
                    perf['comments'] = int(row.get('comment_count', 0)) if row.get('comment_count') else 0
                    perf['favorites'] = int(row.get('collected_count', 0)) if row.get('collected_count') else 0
                    perf['shares'] = int(row.get('share_count', 0)) if row.get('share_count') else 0
                    if perf['likes'] > 0:
                        perf['favorite_like_ratio'] = round(perf['favorites'] / perf['likes'], 3)
                        perf['share_like_ratio'] = round(perf['shares'] / perf['likes'], 3)
                        perf['comment_like_ratio'] = round(perf['comments'] / perf['likes'], 3)
            
            # Check for exact duplicate
            duplicate_status = 'NONE'
            for existing in samples:
                if existing['manifest'].get('media_sha256') == manifest.get('media_sha256') and existing['cid'] != cid:
                    duplicate_status = 'EXACT_DUPLICATE'
                    break
            
            samples.append({
                'dir': s,
                'cid': cid,
                'meta': meta,
                'perf': perf,
                'manifest': manifest,
                'transcript_complete': transcript_complete,
                'embedded_segs': embedded_segs,
                'recovered_meta': recovered_meta,
                'duplicate_status': duplicate_status
            })
        except Exception as e:
            print(f"  Error processing {s.name}: {e}")
    
    print(f"Total samples collected: {len(samples)}")
    
    # Apply problem tags
    ASR_CORRUPTED = ['7601271873183404410']
    ASR_UNUSABLE = ['7616716621441157861']
    INSUFFICIENT_CONTENT = ['7637328690322049125']
    TRANSCRIPT_EMPTY_IDS = ['7660665426599452089']
    NEAR_DUPLICATE_GROUP = ['7680857899472843515', '7599692006406786358']
    
    for sample in samples:
        cid = sample['cid']
        
        # Set logic_analyzable
        if cid in ASR_CORRUPTED:
            sample['logic_analyzable'] = 'FALSE_ASR_CORRUPTED'
        elif cid in ASR_UNUSABLE:
            sample['logic_analyzable'] = 'FALSE_ASR_UNUSABLE'
        elif cid in INSUFFICIENT_CONTENT:
            sample['logic_analyzable'] = 'FALSE_INSUFFICIENT_CONTENT'
        elif cid in TRANSCRIPT_EMPTY_IDS:
            sample['logic_analyzable'] = 'FALSE_TRANSCRIPT_EMPTY'
        elif sample['transcript_complete']:
            sample['logic_analyzable'] = 'TRUE'
        else:
            sample['logic_analyzable'] = 'FALSE_INCOMPLETE'
        
        # Set near_duplicate
        if cid in NEAR_DUPLICATE_GROUP:
            sample['near_duplicate'] = True
        else:
            sample['near_duplicate'] = False
    
    # Filter out duplicates (keep first occurrence)
    unique_cids = set()
    canonical_samples = []
    duplicate_samples = []
    
    for sample in samples:
        cid = sample['cid']
        if cid in unique_cids:
            sample['duplicate_status'] = 'EXACT_DUPLICATE'
            duplicate_samples.append(sample)
        else:
            unique_cids.add(cid)
            canonical_samples.append(sample)
    
    print(f"Unique content IDs: {len(canonical_samples)}")
    print(f"Exact duplicates removed: {len(duplicate_samples)}")
    
    # Apply recovered metadata
    metadata_recovered = 0
    for sample in canonical_samples:
        if sample['recovered_meta']:
            sample['meta'].update(sample['recovered_meta'])
            metadata_recovered += 1
            # Save updated metadata
            (sample['dir'] / "01_metadata.json").write_text(json.dumps(sample['meta'], indent=2, ensure_ascii=False))
        
        # Save recovered performance
        likes = sample['perf'].get('likes')
        if isinstance(likes, int) and likes > 0:
            (sample['dir'] / "02_performance.json").write_text(json.dumps(sample['perf'], indent=2, ensure_ascii=False))
    
    print(f"Metadata recovered: {metadata_recovered}")
    
    # Count statuses
    logic_analyzable = sum(1 for s in canonical_samples if s['logic_analyzable'] == 'TRUE')
    exact_duplicates = len(duplicate_samples)
    near_duplicate_groups = 1 if any(s['near_duplicate'] for s in canonical_samples) else 0
    transcript_empty = sum(1 for s in canonical_samples if s['logic_analyzable'] == 'FALSE_TRANSCRIPT_EMPTY')
    asr_unusable = sum(1 for s in canonical_samples if s['logic_analyzable'].startswith('FALSE_ASR'))
    verified_perf = sum(1 for s in canonical_samples if isinstance(s['perf'].get('likes'), int) and s['perf'].get('likes', 0) > 0)
    
    # Generate canonical manifest
    print(f"\n=== GENERATING CANONICAL MANIFEST ===")
    
    rows = []
    for i, sample in enumerate(canonical_samples, 1):
        rows.append({
            'canonical_id': f'B001-{i:03d}',
            'content_id': sample['cid'],
            'analysis_id': f'B001-{i:03d}',
            'logic_analyzable': sample['logic_analyzable'],
            'performance_verified': 'TRUE' if isinstance(sample['perf'].get('likes'), int) and sample['perf'].get('likes', 0) > 0 else 'FALSE',
            'transcript_status': 'COMPLETE' if sample['transcript_complete'] else 'INCOMPLETE',
            'duplicate_status': sample['duplicate_status'],
            'near_duplicate': 'TRUE' if sample['near_duplicate'] else 'FALSE',
            'metadata_status': 'RECOVERED' if sample['recovered_meta'] else 'ORIGINAL',
            'media_sha256': sample['manifest'].get('media_sha256', ''),
            'transcript_sha256': sample['manifest'].get('transcript_sha256', ''),
            'segment_count': sample['manifest'].get('segment_count', 0),
            'duration_sec': sample['manifest'].get('duration_sec', 0),
            'viral_type': sample['meta'].get('viral_type', 'NULL'),
            'sample_role': sample['meta'].get('sample_role', 'NULL'),
            'likes': sample['perf'].get('likes', 'NULL'),
            'notes': ''
        })
        
        # Add notes for problem samples
        if sample['cid'] in ASR_CORRUPTED:
            rows[-1]['notes'] = 'ASR_CORRUPTED - Not for Logic Corpus'
        elif sample['cid'] in ASR_UNUSABLE:
            rows[-1]['notes'] = 'ASR_UNUSABLE - Not for Logic Corpus'
        elif sample['cid'] in INSUFFICIENT_CONTENT:
            rows[-1]['notes'] = 'INSUFFICIENT_CONTENT - Not for Logic Corpus'
        elif sample['cid'] in TRANSCRIPT_EMPTY_IDS:
            rows[-1]['notes'] = 'TRANSCRIPT_EMPTY - Not for Logic Corpus'
        elif sample['near_duplicate']:
            rows[-1]['notes'] = 'NEAR_DUPLICATE_CONTENT_PATTERN'
    
    # Write CSV
    csv_path = BATCH_DIR / "CORPUS_CANONICAL_MANIFEST_V1.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'canonical_id', 'content_id', 'analysis_id', 'logic_analyzable',
            'performance_verified', 'transcript_status', 'duplicate_status',
            'near_duplicate', 'metadata_status', 'media_sha256', 'transcript_sha256',
            'segment_count', 'duration_sec', 'viral_type', 'sample_role', 'likes', 'notes'
        ])
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"  ✓ {csv_path}")
    
    # Final report
    print(f"\n=== CORPUS HYGIENE REPORT ===")
    print(f"Unique Content IDs: {len(canonical_samples)}")
    print(f"Logic Analyzable: {logic_analyzable}")
    print(f"Exact Duplicates: {exact_duplicates}")
    print(f"Near Duplicate Groups: {near_duplicate_groups}")
    print(f"Transcript Empty: {transcript_empty}")
    print(f"ASR Unusable: {asr_unusable}")
    print(f"Verified Performance: {verified_perf}")
    print(f"Metadata Recovered: {metadata_recovered}")
    print(f"\nFile: {csv_path}")

if __name__ == "__main__":
    main()
