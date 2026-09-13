#!/usr/bin/env python3
"""
Douyin Benchmark Collector - 20 Topic Batch Pipeline
Phase 1: Raw Pool Collection (600-1000 videos)
"""
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(r"C:\workspace\AI_Media_Matrix")
RAW_DIR = WORKSPACE / "01_benchmark/shards/hermes_real/douyin_raw"
DATA_DIR = WORKSPACE / "10_automation/benchmark_collector/MediaCrawler/data/douyin/jsonl"
MC_DIR = WORKSPACE / "10_automation/benchmark_collector/MediaCrawler"

# 20核心关键词
TOPICS = [
    "赚钱逻辑",
    "能力变现", 
    "信息差",
    "副业",
    "创业",
    "职场",
    "中产焦虑",
    "消费陷阱",
    "AI赚钱",
    "普通人收入",
    "财富认知",
    "搞钱",
    "赚钱思维",
    "普通人翻身",
    "商业思维",
    "加盟避坑",
    "创业失败",
    "投资认知",
    "黄金回收",
    "消费降级"
]

def run_keyword(keyword):
    """Run MediaCrawler for one keyword"""
    print(f"\n{'='*60}")
    print(f"Running: {keyword}")
    print(f"{'='*60}")
    
    cmd = [
        "uv", "run", "main.py",
        "--platform", "dy",
        "--type", "search",
        "--keywords", keyword,
        "--headless", "false",
        "--get_comment", "no",
        "--save_data_option", "jsonl"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(MC_DIR),
            capture_output=True,
            text=True,
            timeout=180
        )
        
        if result.returncode == 0:
            print(f"✓ Success")
            return True
        else:
            print(f"✗ Failed: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    # Create dirs
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=== DOUYIN BENCHMARK COLLECTOR V4.0 ===")
    print(f"Topics: {len(TOPICS)}")
    print(f"Target: 30-50 videos per topic")
    print(f"Start time: {datetime.now().isoformat()}")
    
    results = {}
    
    for i, keyword in enumerate(TOPICS, 1):
        print(f"\n[{i}/{len(TOPICS)}] Collecting: {keyword}")
        
        success = run_keyword(keyword)
        
        if success:
            # Read the collected data
            latest_file = sorted(DATA_DIR.glob("*.jsonl"))[-1] if list(DATA_DIR.glob("*.jsonl")) else None
            if latest_file:
                with open(latest_file, 'r', encoding='utf-8') as f:
                    records = [json.loads(l) for l in f if l.strip()]
                
                # Save to raw pool
                raw_file = RAW_DIR / f"raw_{keyword}.jsonl"
                with open(raw_file, 'w', encoding='utf-8') as f:
                    for r in records:
                        r['source_keyword'] = keyword
                        r['capture_time'] = datetime.now().isoformat()
                        r['metadata_source'] = 'MEDIACRAWLER_REAL_CDP'
                        f.write(json.dumps(r, ensure_ascii=False) + '\n')
                
                results[keyword] = len(records)
                print(f"  ✓ Collected: {len(records)} videos")
        else:
            results[keyword] = 0
            print(f"  ✗ No data collected")
        
        # Rate limiting
        if i < len(TOPICS):
            time.sleep(3)
    
    # Summary
    total = sum(results.values())
    print(f"\n{'='*60}")
    print(f"COLLECTION COMPLETE")
    print(f"{'='*60}")
    print(f"Topics completed: {len([v for v in results.values() if v > 0])}/{len(TOPICS)}")
    print(f"Total videos: {total}")
    print(f"Target: 600-1000")
    
    return total

if __name__ == "__main__":
    main()
