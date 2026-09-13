#!/usr/bin/env python3
"""Run Creator Baseline for top creators using MediaCrawler creator mode"""
import subprocess
import json
import time
from pathlib import Path

BASE_DIR = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
MC_DIR = Path(r"C:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler")
TARGETS_FILE = BASE_DIR / "creator_baseline_targets.csv"
OUTPUT_DIR = BASE_DIR / "creator_baselines"

# Create output dir
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_targets():
    import csv
    targets = []
    with open(TARGETS_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.lstrip('\ufeff'): v for k, v in row.items()}
            targets.append(clean_row)
    return targets

def run_creator_baseline(creator_url, creator_name):
    """Run MediaCrawler creator mode for one creator"""
    print(f"  Running creator mode for: {creator_name}")
    
    # Create temp config or use CLI args
    cmd = [
        "uv", "run", "main.py",
        "--platform", "dy",
        "--type", "creator",
        "--creator_id", creator_url,
        "--crawler_max_notes_count", "20",
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
            print(f"    ✓ Success")
            return True, result.stdout[-500:] if len(result.stdout) > 500 else result.stdout
        else:
            print(f"    ✗ Failed: {result.stderr[:200]}")
            return False, result.stderr[:500]
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False, str(e)

def main():
    print("=== CREATOR BASELINE COLLECTION ===\n")
    
    targets = load_targets()
    print(f"Loading {len(targets)} creator targets\n")
    
    # Only process top 10 for now
    top_targets = sorted(targets, key=lambda x: int(x.get('target_likes', 0) or 0), reverse=True)[:10]
    
    results = {}
    
    for i, target in enumerate(top_targets, 1):
        creator_name = target.get('creator_name', '')
        creator_url = target.get('creator_url', '')
        
        print(f"[{i}/{len(top_targets)}] {creator_name}")
        
        success, output = run_creator_baseline(creator_url, creator_name)
        results[creator_name] = {
            'success': success,
            'output': output[:500],
            'timestamp': str(time.time())
        }
        
        # Rate limit
        time.sleep(2)
    
    # Save results
    output_file = OUTPUT_DIR / "baseline_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: {output_file}")
    
    # Summary
    success_count = sum(1 for r in results.values() if r['success'])
    print(f"\nSuccess: {success_count}/{len(results)}")

if __name__ == "__main__":
    main()
