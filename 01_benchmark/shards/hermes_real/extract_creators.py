#!/usr/bin/env python3
"""Extract creator IDs from deep batch and prepare baseline targets"""
import csv
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
DEEP_BATCH_FILE = BASE_DIR / "deep_analysis_batch_001.csv"
CREATOR_TARGETS_FILE = BASE_DIR / "creator_baseline_targets.csv"

def load_deep_batch():
    records = []
    with open(DEEP_BATCH_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.lstrip('\ufeff'): v for k, v in row.items()}
            records.append(clean_row)
    return records

def main():
    batch = load_deep_batch()
    print(f"Loaded {len(batch)} deep batch records\n")
    
    # Extract unique creators
    creators = {}
    for r in batch:
        nickname = r.get('nickname', '')
        aweme_id = r.get('aweme_id', '')
        url = r.get('url', '')
        likes = r.get('liked_count', '')
        
        if nickname not in creators:
            creators[nickname] = {
                'creator_id': nickname,
                'creator_name': nickname,
                'creator_url': url,
                'target_content_id': aweme_id,
                'target_likes': likes,
                'baseline_status': 'PENDING',
                'baseline_sample_n': 0
            }
    
    print(f"Unique creators: {len(creators)}\n")
    
    # Save targets
    fieldnames = ['creator_id', 'creator_name', 'creator_url', 'target_content_id', 
                  'target_likes', 'baseline_status', 'baseline_sample_n']
    
    with open(CREATOR_TARGETS_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for creator in creators.values():
            writer.writerow(creator)
    
    print(f"Saved to: {CREATOR_TARGETS_FILE}")
    
    # Print top creators by likes
    sorted_creators = sorted(creators.items(), key=lambda x: int(x[1]['target_likes'] or 0), reverse=True)
    print("\n=== TOP CREATORS BY LIKES ===")
    for i, (name, data) in enumerate(sorted_creators[:10], 1):
        print(f"{i}. {name}: {data['target_likes']} likes")
    
    return creators

if __name__ == "__main__":
    main()
