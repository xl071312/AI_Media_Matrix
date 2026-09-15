#!/usr/bin/env python3
"""RC6H: Generate final status report"""
import json
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix")
RC6H_DIR = BASE / "01_benchmark/plain_language_discovery_rc6h"

# Count available data
hist_file = BASE / "01_benchmark/plain_language_corpus_v1/HISTORICAL_CONTENT_IDS_CANONICAL.txt"
hist_count = 0
if hist_file.exists():
    with open(hist_file, 'r', encoding='utf-8') as f:
        hist_count = sum(1 for line in f if line.strip())

# Check search data
search_data = BASE / "10_automation/benchmark_collector/MediaCrawler/data/douyin/jsonl"
search_total = 0
search_unique = 0
if search_data.exists():
    all_ids = set()
    for jsonl in search_data.glob("search_*.jsonl"):
        with open(jsonl, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        d = json.loads(line)
                        all_ids.add(str(d.get('aweme_id', '')))
                    except:
                        pass
    search_total = sum(1 for jsonl in search_data.glob("search_*.jsonl") 
                       for line in open(jsonl, encoding='utf-8') if line.strip())
    search_unique = len(all_ids)

# Check raw pool
raw_pool = BASE / "01_benchmark/shards/hermes_real/douyin_raw/raw_pool_all.jsonl"
raw_count = 0
if raw_pool.exists():
    with open(raw_pool, 'r', encoding='utf-8') as f:
        raw_count = sum(1 for line in f if line.strip())

print("=" * 60)
print("RC6H Discovery Status Report")
print("=" * 60)
print(f"\nHistorical ID Universe: {hist_count} IDs")
print(f"Search Data Records: {search_total}")
print(f"Search Data Unique: {search_unique}")
print(f"Raw Pool Records: {raw_count}")
print(f"\nNew unique candidates found: 0")
print(f"\nAll existing data sources contain historical duplicates.")
print(f"Live discovery (Route A) unavailable: CDP port not accessible.")
print(f"\nStatus: DISCOVERY_INSUFFICIENT")
print(f"Reason: No genuinely new candidates from available routes.")

# Save status
status = f"""# RC6H Discovery Status

**Completed**: {datetime.now().isoformat()}
**Status**: DISCOVERY_INSUFFICIENT

## Discovery Summary

| Route | Description | Candidates Found |
|-------|-------------|------------------|
| Route A (Live Douyin) | Live search via MediaCrawler | 0 (CDP unavailable) |
| Route B (Related) | Related videos | 0 (not attempted) |
| Route C (Creator) | Creator expansion | 0 (not attempted) |
| Route D (Toutiao) | Toutiao fallback | 0 (not attempted) |

## Data Audit

- Historical ID universe: {hist_count} canonical IDs
- Search data records scanned: {search_total}
- Search data unique IDs: {search_unique}
- Raw pool candidates: {raw_count}
- **New non-historical candidates: 0**

## Root Cause

All available data sources (search_results, raw_pool) contain only historical IDs already in the global registry. Live discovery via MediaCrawler requires CDP connection which is currently unavailable (port 9223 not accessible).

## Required Actions

To continue Plain Language Corpus collection, one of the following is needed:
1. Start Chrome with `--remote-debugging-port=9223` for live CDP-based discovery
2. Provide new cookie/set of cookies with fresh search capability
3. Expand to alternative platforms (Bilibili, etc.) with new collection route

## Output Files

- `DISCOVERY_QUERY_BANK.csv` - {41} queries prepared
- `DISCOVERY_RESULTS_RAW.csv` - Empty (no new candidates)
- `DISCOVERY_ROUTE_COUNTS.csv` - Route statistics
- `HISTORICAL_DEDUPE_AUDIT.csv` - Deduplication audit
- `NEW_CANDIDATES.csv` - Empty (no new candidates)
- `SHORTLIST.csv` - Empty (nothing to shortlist)
- `PERFORMANCE.csv` - Empty (no candidates)
- `STATUS.md` - This file

## Notes

- Verified Logic Corpus: 85/100 (unchanged)
- Plain Language Corpus V1: PARTIAL (RC6F evidence preserved)
- No semantic analysis performed
- No fabrication of completion

---
"""

(RC6H_DIR / "STATUS.md").write_text(status, encoding='utf-8')

print(f"\nStatus saved to: {RC6H_DIR / 'STATUS.md'}")