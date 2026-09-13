#!/usr/bin/env python3
"""
Phase 3 Alternative: Use search results to build creator baseline
Since detail/creator mode is blocked by ArgusSecurityPlugin,
we'll use the search data we already have to estimate creator baselines.
"""
import json
import csv
from pathlib import Path
from collections import defaultdict
import statistics

BASE_DIR = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
RAW_POOL = BASE_DIR / "douyin_raw" / "raw_pool_all.jsonl"
DEEP_BATCH = BASE_DIR / "deep_analysis_batch_001.csv"
BASELINE_OUTPUT = BASE_DIR / "creator_baselines_estimated.json"

def load_raw_pool():
    records = []
    with open(RAW_POOL, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    records.append(json.loads(line))
                except:
                    pass
    return records

def load_deep_batch():
    records = []
    with open(DEEP_BATCH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.lstrip('\ufeff'): v for k, v in row.items()}
            records.append(clean_row)
    return records

def estimate_creator_baseline(raw_records, target_creators):
    """Estimate creator baselines from raw pool data"""
    # Group by creator
    creator_videos = defaultdict(list)
    
    for r in raw_records:
        nickname = r.get('nickname', '')
        if nickname in target_creators:
            likes = int(r.get('liked_count', 0) or 0)
            comments = int(r.get('comment_count', 0) or 0)
            favorites = int(r.get('collected_count', 0) or 0)
            shares = int(r.get('share_count', 0) or 0)
            
            if likes > 0:  # Only include videos with engagement
                creator_videos[nickname].append({
                    'aweme_id': r.get('aweme_id', ''),
                    'likes': likes,
                    'comments': comments,
                    'favorites': favorites,
                    'shares': shares
                })
    
    # Calculate baselines
    baselines = {}
    for creator, videos in creator_videos.items():
        if len(videos) >= 3:  # Minimum sample size
            likes_list = [v['likes'] for v in videos]
            comments_list = [v['comments'] for v in videos]
            favorites_list = [v['favorites'] for v in videos]
            shares_list = [v['shares'] for v in videos]
            
            baselines[creator] = {
                'baseline_sample_n': len(videos),
                'median_likes': statistics.median(likes_list),
                'mean_likes': statistics.mean(likes_list),
                'median_comments': statistics.median(comments_list),
                'median_favorites': statistics.median(favorites_list),
                'median_shares': statistics.median(shares_list),
                'min_likes': min(likes_list),
                'max_likes': max(likes_list),
                'videos': videos[:10]  # Store first 10 for reference
            }
    
    return baselines

def calculate_relative_ratios(deep_batch, baselines):
    """Calculate relative performance ratios"""
    results = []
    
    for record in deep_batch:
        creator = record.get('nickname', '')
        target_likes = int(record.get('liked_count', 0) or 0)
        
        if creator in baselines:
            baseline = baselines[creator]
            sample_n = baseline['baseline_sample_n']
            
            if sample_n >= 5:  # Reliable baseline
                median_likes = baseline['median_likes']
                if median_likes > 0:
                    relative_ratio = target_likes / median_likes
                    
                    # Classify
                    if relative_ratio >= 20:
                        breakout_level = 'EXTREME_BREAKOUT'
                    elif relative_ratio >= 10:
                        breakout_level = 'STRONG_BREAKOUT'
                    elif relative_ratio >= 5:
                        breakout_level = 'BREAKOUT'
                    elif relative_ratio >= 3:
                        breakout_level = 'ABOVE_BASELINE'
                    else:
                        breakout_level = 'NORMAL'
                    
                    results.append({
                        'aweme_id': record.get('aweme_id', ''),
                        'creator': creator,
                        'target_likes': target_likes,
                        'median_likes': median_likes,
                        'relative_ratio': round(relative_ratio, 2),
                        'breakout_level': breakout_level,
                        'baseline_sample_n': sample_n,
                        'verified': True
                    })
                else:
                    results.append({
                        'aweme_id': record.get('aweme_id', ''),
                        'creator': creator,
                        'target_likes': target_likes,
                        'median_likes': 0,
                        'relative_ratio': 0,
                        'breakout_level': 'UNKNOWN',
                        'baseline_sample_n': sample_n,
                        'verified': False
                    })
            else:
                results.append({
                    'aweme_id': record.get('aweme_id', ''),
                    'creator': creator,
                    'target_likes': target_likes,
                    'median_likes': baseline['median_likes'],
                    'relative_ratio': 0,
                    'breakout_level': 'INSUFFICIENT_DATA',
                    'baseline_sample_n': sample_n,
                    'verified': False
                })
        else:
            results.append({
                'aweme_id': record.get('aweme_id', ''),
                'creator': creator,
                'target_likes': target_likes,
                'median_likes': 0,
                'relative_ratio': 0,
                'breakout_level': 'NO_BASELINE',
                'baseline_sample_n': 0,
                'verified': False
            })
    
    return results

def main():
    print("=== ESTIMATED CREATOR BASELINE ===\n")
    
    # Load data
    raw_records = load_raw_pool()
    deep_batch = load_deep_batch()
    
    print(f"Raw pool: {len(raw_records)} records")
    print(f"Deep batch: {len(deep_batch)} records\n")
    
    # Get target creators from deep batch
    target_creators = set(r.get('nickname', '') for r in deep_batch)
    print(f"Target creators: {len(target_creators)}\n")
    
    # Estimate baselines
    baselines = estimate_creator_baseline(raw_records, target_creators)
    print(f"Baselines estimated: {len(baselines)}")
    
    # Calculate ratios
    results = calculate_relative_ratios(deep_batch, baselines)
    
    # Save
    output = {
        'baselines': baselines,
        'results': results,
        'generated_at': str(__import__('datetime').datetime.now().isoformat()),
        'method': 'ESTIMATED_FROM_SEARCH_DATA'
    }
    
    with open(BASELINE_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved to: {BASELINE_OUTPUT}")
    
    # Summary
    verified = sum(1 for r in results if r.get('verified'))
    extreme = sum(1 for r in results if r.get('breakout_level') == 'EXTREME_BREAKOUT')
    strong = sum(1 for r in results if r.get('breakout_level') == 'STRONG_BREAKOUT')
    breakout = sum(1 for r in results if r.get('breakout_level') == 'BREAKOUT')
    
    print(f"\n=== SUMMARY ===")
    print(f"Verified baselines: {verified}/{len(results)}")
    print(f"Extreme Breakout: {extreme}")
    print(f"Strong Breakout: {strong}")
    print(f"Breakout: {breakout}")

if __name__ == "__main__":
    main()
