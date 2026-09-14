#!/usr/bin/env python3
"""Plain Language Corpus V1: Collect samples with available data"""
import json
import csv
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix")
CORPUS = BASE / "01_benchmark/plain_language_corpus_v1"
MEDIA_DIR = BASE / "01_benchmark/media/plain_language_v1"
RAW_POOL = BASE / "01_benchmark/shards/hermes_real/douyin_raw/raw_pool_all.jsonl"

MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Collect existing content IDs for dedupe
existing_ids = set()
for p in BASE.rglob("*.json"):
    if 'plain_language' in str(p):
        continue
    try:
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
            cid = data.get('content_id')
            if cid:
                existing_ids.add(str(cid))
    except:
        pass

print(f"Existing content IDs: {len(existing_ids)}")

# Load raw pool candidates
candidates = []
if RAW_POOL.exists():
    with open(RAW_POOL, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    cand = json.loads(line)
                    aweme_id = str(cand.get('aweme_id', ''))
                    if aweme_id and aweme_id not in existing_ids:
                        candidates.append(cand)
                except:
                    pass

print(f"New candidates: {len(candidates)}")

# Mechanical selection - prioritize engagement
def engagement_score(c):
    try:
        liked = int(c.get('liked_count', 0))
        comments = int(c.get('comment_count', 0))
        shares = int(c.get('share_count', 0))
        return liked + comments * 2 + shares * 3
    except:
        return 0

# Filter by minimum engagement (mechanical)
filtered = [c for c in candidates if int(c.get('liked_count', 0)) >= 1000]
filtered.sort(key=engagement_score, reverse=True)

# Select top 40 as reserve pool
reserve_pool = filtered[:40]
print(f"Reserve pool: {len(reserve_pool)}")

# Save candidate manifest
with open(CORPUS / "PLAIN_LANGUAGE_CANDIDATES.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['content_id', 'platform', 'title', 'author', 'likes', 'comments', 
                     'favorites', 'shares', 'selection_rank', 'aweme_url', 'source_keyword'])
    for i, c in enumerate(reserve_pool, 1):
        writer.writerow([
            c.get('aweme_id', ''),
            'douyin',
            ((c.get('title', '') or '')[:100]),
            (c.get('nickname', '') or '')[:50],
            c.get('liked_count', 0),
            c.get('comment_count', 0),
            c.get('collected_count', 0),
            c.get('share_count', 0),
            i,
            c.get('aweme_url', ''),
            c.get('source_keyword', '')
        ])

print(f"Candidate manifest created: {CORPUS / 'PLAIN_LANGUAGE_CANDIDATES.csv'}")

# Show top candidates
print(f"\nTop 10 candidates:")
for i, c in enumerate(reserve_pool[:10], 1):
    title = (c.get('title', '') or '')[:60]
    print(f"  {i}. {c.get('aweme_id')} - {title}... ({c.get('liked_count')} likes)")

# Initialize status file
status = {
    "target": 30,
    "reservoir_size": len(reserve_pool),
    "collected": 0,
    "failed": 0,
    "started_at": datetime.now().isoformat(),
    "status": "COLLECTION_IN_PROGRESS"
}

with open(CORPUS / "PLAIN_LANGUAGE_CORPUS_V1_STATUS.md", 'w', encoding='utf-8') as f:
    f.write(f"# Plain Language Corpus V1 Status\n\n")
    f.write(f"**Started**: {status['started_at']}\n")
    f.write(f"**Target**: {status['target']} videos\n")
    f.write(f"**Reserve pool**: {status['reservoir_size']} candidates\n")
    f.write(f"**Collected**: {status['collected']}\n")
    f.write(f"**Status**: {status['status']}\n")
    f.write(f"\n## Notes\n\n")
    f.write(f"- Duration not available in raw pool - will need ffprobe measurement\n")
    f.write(f"- Collection in progress...\n")

print(f"\nCorpus V1 initialized:")
print(f"  Target: {status['target']} videos")
print(f"  Reserve pool: {status['reservoir_size']} candidates")
print(f"  Directory: {CORPUS}")