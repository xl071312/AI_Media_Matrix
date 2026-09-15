#!/usr/bin/env python3
"""RC6H: Process available search data for new candidates"""
import json
import csv
import subprocess
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix")
RC6H_DIR = BASE / "01_benchmark/plain_language_discovery_rc6h"
SEARCH_DATA = BASE / "10_automation/benchmark_collector/MediaCrawler/data/douyin/jsonl"
HIST_FILE = BASE / "01_benchmark/plain_language_corpus_v1/HISTORICAL_CONTENT_IDS_CANONICAL.txt"

# Load historical IDs
historical_ids = set()
if HIST_FILE.exists():
    with open(HIST_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            cid = line.strip()
            if cid and cid.isdigit():
                historical_ids.add(cid)

print(f"Historical IDs: {len(historical_ids)}")

# Load all search data candidates
all_candidates = []
for jsonl_file in sorted(SEARCH_DATA.glob("search_*.jsonl")):
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    cand = json.loads(line)
                    aweme_id = str(cand.get('aweme_id', ''))
                    if aweme_id and aweme_id.isdigit():
                        cand['_source_file'] = jsonl_file.name
                        all_candidates.append(cand)
                except:
                    pass

print(f"Total search candidates: {len(all_candidates)}")

# Deduplicate and filter
seen_ids = set()
unique_candidates = []
for cand in all_candidates:
    cid = str(cand.get('aweme_id', ''))
    if cid not in seen_ids:
        seen_ids.add(cid)
        unique_candidates.append(cand)

print(f"Unique candidates: {len(unique_candidates)}")

# Filter: exclude historical IDs
new_candidates = [c for c in unique_candidates if str(c.get('aweme_id', '')) not in historical_ids]
print(f"New candidates (not historical): {len(new_candidates)}")

# Filter by engagement (mechanical)
engaged_candidates = [c for c in new_candidates if int(c.get('liked_count', 0)) >= 100]
print(f"With engagement >= 100: {len(engaged_candidates)}")

# Sort by engagement
def engagement_score(c):
    try:
        liked = int(c.get('liked_count', 0))
        comments = int(c.get('comment_count', 0))
        return liked + comments * 2
    except:
        return 0

engaged_candidates.sort(key=engagement_score, reverse=True)

# Take top candidates
shortlist = engaged_candidates[:50]
print(f"Shortlist: {len(shortlist)}")

# Save results
print("\n=== Saving RC6H Discovery Results ===")

# DISCOVERY_RESULTS_RAW.csv
with open(RC6H_DIR / "DISCOVERY_RESULTS_RAW.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['query', 'rank', 'content_id', 'title', 'author', 'duration_sec',
                     'likes', 'comments', 'favorites', 'shares', 'url', 'discovery_timestamp', 'route'])
    for i, c in enumerate(shortlist, 1):
        writer.writerow([
            c.get('_source_file', ''),
            i,
            c.get('aweme_id', ''),
            (c.get('title', '') or '')[:100],
            (c.get('nickname', '') or '')[:50],
            '',  # duration - will measure after download
            c.get('liked_count', 0),
            c.get('comment_count', 0),
            c.get('collected_count', 0),
            c.get('share_count', 0),
            c.get('aweme_url', ''),
            datetime.now().isoformat(),
            'route_a_douyin_search_data'
        ])

# HISTORICAL_DEDUPE_AUDIT.csv
with open(RC6H_DIR / "HISTORICAL_DEDUPE_AUDIT.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['content_id', 'in_historical_universe', 'duplicate_status'])
    for c in unique_candidates[:100]:  # First 100 for audit
        cid = str(c.get('aweme_id', ''))
        in_hist = cid in historical_ids
        writer.writerow([cid, in_hist, 'DUPLICATE' if in_hist else 'NEW'])

# NEW_CANDIDATES.csv
with open(RC6H_DIR / "NEW_CANDIDATES.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['content_id', 'title', 'author', 'likes', 'comments', 'source_file'])
    for c in new_candidates[:50]:
        writer.writerow([
            c.get('aweme_id', ''),
            (c.get('title', '') or '')[:100],
            (c.get('nickname', '') or '')[:50],
            c.get('liked_count', 0),
            c.get('comment_count', 0),
            c.get('_source_file', '')
        ])

# SHORTLIST.csv
with open(RC6H_DIR / "SHORTLIST.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['content_id', 'title', 'author', 'likes', 'comments', 'engagement_score', 'rank'])
    for i, c in enumerate(shortlist, 1):
        score = engagement_score(c)
        writer.writerow([
            c.get('aweme_id', ''),
            (c.get('title', '') or '')[:100],
            (c.get('nickname', '') or '')[:50],
            c.get('liked_count', 0),
            c.get('comment_count', 0),
            score,
            i
        ])

# PERFORMANCE.csv
with open(RC6H_DIR / "PERFORMANCE.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['content_id', 'likes', 'comments', 'favorites', 'shares', 'engagement_score'])
    for c in shortlist:
        score = engagement_score(c)
        writer.writerow([
            c.get('aweme_id', ''),
            c.get('liked_count', 0),
            c.get('comment_count', 0),
            c.get('collected_count', 0),
            c.get('share_count', 0),
            score
        ])

# Route counts
with open(RC6H_DIR / "DISCOVERY_ROUTE_COUNTS.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['route', 'count', 'description'])
    writer.writerow(['route_a_douyin_search_data', len(shortlist), 'Existing search data (new candidates)'])
    writer.writerow(['route_b_related', 0, 'Related videos (unavailable)'])
    writer.writerow(['route_c_creator', 0, 'Creator expansion (unavailable)'])
    writer.writerow(['route_d_toutiao', 0, 'Toutiao fallback (unavailable)'])

print(f"\nDiscovered raw: {len(unique_candidates)}")
print(f"New after dedupe: {len(new_candidates)}")
print(f"Shortlisted: {len(shortlist)}")
print(f"\nFiles saved to: {RC6H_DIR}")