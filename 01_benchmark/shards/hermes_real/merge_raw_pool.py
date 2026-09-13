#!/usr/bin/env python3
"""
Merge all MediaCrawler data into unified Raw Pool
"""
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

RAW_DIR = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real\douyin_raw")
MC_DATA = Path(r"C:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\jsonl")

def main():
    # Read all data
    all_records = []
    seen_ids = set()
    
    # Process the latest merged file
    latest_file = sorted(MC_DATA.glob("*.jsonl"))[-1]
    print(f"Reading: {latest_file}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    record = json.loads(line)
                    aweme_id = record.get('aweme_id', '')
                    if aweme_id and aweme_id not in seen_ids:
                        seen_ids.add(aweme_id)
                        record['metadata_source'] = 'MEDIACRAWLER_REAL_CDP'
                        record['capture_time'] = datetime.now().isoformat()
                        all_records.append(record)
                except:
                    pass
    
    print(f"Total unique records: {len(all_records)}")
    
    # Save merged raw pool
    raw_pool_file = RAW_DIR / "raw_pool_all.jsonl"
    with open(raw_pool_file, 'w', encoding='utf-8') as f:
        for r in all_records:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    
    print(f"Saved to: {raw_pool_file}")
    
    # Generate ranking
    ranking_file = RAW_DIR / "performance_ranking.csv"
    import csv
    
    # Sort by likes
    sorted_records = sorted(all_records, key=lambda x: int(x.get('liked_count', 0)), reverse=True)
    
    with open(ranking_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['rank', 'aweme_id', 'nickname', 'desc', 'liked_count', 'comment_count', 
                        'collected_count', 'share_count', 'aweme_url', 'source_keyword'])
        
        for i, r in enumerate(sorted_records[:100], 1):
            writer.writerow([
                i,
                r.get('aweme_id', ''),
                r.get('nickname', ''),
                r.get('desc', '')[:80],
                r.get('liked_count', ''),
                r.get('comment_count', ''),
                r.get('collected_count', ''),
                r.get('share_count', ''),
                r.get('aweme_url', ''),
                r.get('source_keyword', '')
            ])
    
    print(f"Ranking saved to: {ranking_file}")
    
    # Stats
    with_likes = sum(1 for r in all_records if r.get('liked_count'))
    top_10_pct = sorted_records[:len(sorted_records)//10] if len(sorted_records) > 10 else []
    
    print(f"\n=== SUMMARY ===")
    print(f"Total raw pool: {len(all_records)}")
    print(f"With likes data: {with_likes}")
    print(f"TOP 10% count: {len(top_10_pct)}")
    if top_10_pct:
        print(f"TOP 10% avg likes: {sum(int(r.get('liked_count', 0)) for r in top_10_pct) // len(top_10_pct)}")

if __name__ == "__main__":
    main()
