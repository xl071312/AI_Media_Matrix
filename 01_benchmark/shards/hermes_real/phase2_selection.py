#!/usr/bin/env python3
"""
Phase 2: Performance Analysis + Selection
- Calculate percentiles for each metric
- Build performance_score
- Identify ABSOLUTE_VIRAL and RELATIVE_BREAKOUT
- Select 80-120 benchmark candidates
"""
import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import numpy as np

RAW_POOL = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real\douyin_raw\raw_pool_all.jsonl")
OUTPUT_DIR = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
SELECTION_FILE = OUTPUT_DIR / "douyin_benchmark_selection.csv"
PERFORMANCE_DIR = OUTPUT_DIR / "performance"

def load_records():
    records = []
    with open(RAW_POOL, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    records.append(json.loads(line))
                except:
                    pass
    return records

def calculate_percentiles(records):
    """Calculate percentile ranks for each metric"""
    metrics = ['liked_count', 'comment_count', 'collected_count', 'share_count']
    
    for metric in metrics:
        values = [int(r.get(metric, 0)) for r in records if r.get(metric)]
        if values:
            for r in records:
                val = int(r.get(metric, 0))
                if val > 0:
                    percentile = (sum(1 for v in values if v <= val) / len(values)) * 100
                    r[f'{metric}_percentile'] = percentile
                else:
                    r[f'{metric}_percentile'] = 0
    
    return records

def calculate_performance_score(records):
    """Calculate composite performance score"""
    for r in records:
        likes_p = r.get('liked_count_percentile', 0)
        comments_p = r.get('comment_count_percentile', 0)
        favorites_p = r.get('collected_count_percentile', 0)
        shares_p = r.get('share_count_percentile', 0)
        
        # Weighted score
        score = likes_p * 0.40 + comments_p * 0.20 + favorites_p * 0.25 + shares_p * 0.15
        r['performance_score'] = round(score, 2)
    
    return records

def classify_records(records):
    """Classify into ABSOLUTE_VIRAL, RELATIVE_BREAKOUT, CONTROL, NORMAL_REFERENCE"""
    for r in records:
        likes_p = r.get('liked_count_percentile', 0)
        score = r.get('performance_score', 0)
        
        if likes_p >= 90 or score >= 85:
            r['sample_role'] = 'ABSOLUTE_VIRAL'
        elif likes_p >= 70 and likes_p < 90:
            r['sample_role'] = 'RELATIVE_BREAKOUT'
        elif likes_p < 30:
            r['sample_role'] = 'CONTROL'
        else:
            r['sample_role'] = 'NORMAL_REFERENCE'
    
    return records

def select_benchmark(records, target_count=100):
    """Select balanced benchmark candidates"""
    # Sort by performance_score
    sorted_records = sorted(records, key=lambda x: x.get('performance_score', 0), reverse=True)
    
    # Select top candidates
    selected = []
    
    # ABSOLUTE_VIRAL: TOP 20%
    viral_threshold = int(len(sorted_records) * 0.2)
    viral = sorted_records[:viral_threshold]
    
    # RELATIVE_BREAKOUT: Next 20%
    breakout = sorted_records[viral_threshold:viral_threshold*2]
    
    # CONTROL: BOTTOM 30%
    control = sorted_records[int(len(sorted_records) * 0.7):]
    
    # Balance selection
    selected.extend(viral[:25])
    selected.extend(breakout[:25])
    selected.extend(control[:20])
    
    # Fill remaining with NORMAL_REFERENCE
    remaining = sorted_records[viral_threshold*2:int(len(sorted_records) * 0.7)]
    selected.extend(remaining[:target_count - len(selected)])
    
    return selected[:target_count]

def main():
    print("=== PHASE 2: PERFORMANCE ANALYSIS ===\n")
    
    # Load data
    records = load_records()
    print(f"Loaded {len(records)} records")
    
    # Calculate percentiles
    records = calculate_percentiles(records)
    
    # Calculate performance scores
    records = calculate_performance_score(records)
    
    # Classify
    records = classify_records(records)
    
    # Select benchmark
    selected = select_benchmark(records, target_count=100)
    
    # Save selection
    fieldnames = ['aweme_id', 'content_id', 'url', 'nickname', 'desc', 'source_keyword',
                  'liked_count', 'comment_count', 'collected_count', 'share_count',
                  'liked_count_percentile', 'comment_count_percentile', 
                  'collected_count_percentile', 'share_count_percentile',
                  'performance_score', 'sample_role', 'metadata_source']
    
    with open(SELECTION_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in selected:
            writer.writerow({
                'aweme_id': r.get('aweme_id', ''),
                'content_id': f"DY_REAL_{r.get('aweme_id', '')}",
                'url': r.get('aweme_url', ''),
                'nickname': r.get('nickname', ''),
                'desc': r.get('desc', '')[:200],
                'source_keyword': r.get('source_keyword', ''),
                'liked_count': r.get('liked_count', ''),
                'comment_count': r.get('comment_count', ''),
                'collected_count': r.get('collected_count', ''),
                'share_count': r.get('share_count', ''),
                'liked_count_percentile': round(r.get('liked_count_percentile', 0), 1),
                'comment_count_percentile': round(r.get('comment_count_percentile', 0), 1),
                'collected_count_percentile': round(r.get('collected_count_percentile', 0), 1),
                'share_count_percentile': round(r.get('share_count_percentile', 0), 1),
                'performance_score': r.get('performance_score', 0),
                'sample_role': r.get('sample_role', ''),
                'metadata_source': r.get('metadata_source', 'MEDIACRAWLER_REAL_CDP')
            })
    
    # Stats
    viral_count = sum(1 for r in selected if r.get('sample_role') == 'ABSOLUTE_VIRAL')
    breakout_count = sum(1 for r in selected if r.get('sample_role') == 'RELATIVE_BREAKOUT')
    control_count = sum(1 for r in selected if r.get('sample_role') == 'CONTROL')
    
    print(f"\n=== SELECTION RESULTS ===")
    print(f"Total selected: {len(selected)}")
    print(f"  ABSOLUTE_VIRAL: {viral_count}")
    print(f"  RELATIVE_BREAKOUT: {breakout_count}")
    print(f"  CONTROL: {control_count}")
    print(f"\nSaved to: {SELECTION_FILE}")
    
    # Save full ranking
    PERFORMANCE_DIR.mkdir(parents=True, exist_ok=True)
    ranking_file = PERFORMANCE_DIR / "full_ranking.csv"
    with open(ranking_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in sorted(records, key=lambda x: x.get('performance_score', 0), reverse=True):
            writer.writerow({k: r.get(k, '') for k in fieldnames})
    
    print(f"Full ranking saved to: {ranking_file}")

if __name__ == "__main__":
    main()
