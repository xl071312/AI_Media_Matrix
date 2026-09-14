#!/usr/bin/env python3
"""Plain Language Corpus V1: Collection and processing pipeline"""
import json
import csv
import hashlib
import subprocess
import asyncio
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE = Path(r"F:\workspace\AI_Media_Matrix")
CORPUS = BASE / "01_benchmark/plain_language_corpus_v1"
MEDIA_DIR = BASE / "01_benchmark/media/plain_language_v1"
EXISTING_CANDIDATES = BASE / "01_benchmark/shards/hermes_real/douyin_raw/raw_pool_all.jsonl"

# Create directories
CORPUS.mkdir(parents=True, exist_ok=True)
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

# Load existing candidates if available
candidates = []
if EXISTING_CANDIDATES.exists():
    with open(EXISTING_CANDIDATES, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    cand = json.loads(line)
                    if cand.get('content_id') not in existing_ids:
                        candidates.append(cand)
                except:
                    pass

print(f"New candidates from raw pool: {len(candidates)}")

# Define target keywords for plain language content
TARGET_KEYWORDS = [
    "普通人赚钱", "副业赚钱", "打工人的出路", "工资上涨", 
    "职场认知", "存钱方法", "消费降级", "搞钱思路",
    "小生意", "创业故事", "收入提升", "副业项目",
    "AI影响工作", "普通人翻身", "认知升级", "商业思维"
]

# Sample selection criteria (mechanical only)
def is_good_candidate(cand):
    """Check if candidate meets mechanical criteria"""
    duration = cand.get('duration_sec', 0)
    likes = cand.get('likes', 0)
    title = cand.get('title', '')
    content_id = cand.get('content_id', '')
    
    # Duration check (60-360s preferred)
    if not (60 <= duration <= 360):
        return False
    
    # Has meaningful engagement
    if likes < 100:
        return False
    
    # Not already in corpus
    if str(content_id) in existing_ids:
        return False
    
    return True

# Filter candidates
filtered = [c for c in candidates if is_good_candidate(c)]
print(f"Filtered candidates: {len(filtered)}")

# Sort by engagement (mechanical ranking)
filtered.sort(key=lambda x: x.get('likes', 0) + x.get('comments', 0) * 2, reverse=True)

# Select top 40 as reserve pool
reserve_pool = filtered[:40]
print(f"Reserve pool: {len(reserve_pool)}")

# Create candidate manifest
with open(CORPUS / "PLAIN_LANGUAGE_CANDIDATES.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['content_id', 'platform', 'title', 'author', 'duration_sec', 
                     'likes', 'comments', 'favorites', 'shares', 'selection_rank'])
    for i, c in enumerate(reserve_pool, 1):
        writer.writerow([
            c.get('content_id', ''),
            c.get('platform', 'douyin'),
            (c.get('title', '') or '')[:100],
            (c.get('creator_name', '') or '')[:50],
            c.get('duration_sec', 0),
            c.get('likes', 0),
            c.get('comments', 0),
            c.get('favorites', 0),
            c.get('shares', 0),
            i
        ])

print(f"Candidate manifest created: {CORPUS / 'PLAIN_LANGUAGE_CANDIDATES.csv'}")

# Initialize status
status = {
    "target": 30,
    "collected": 0,
    "failed": 0,
    "reservoir_size": len(reserve_pool),
    "started_at": datetime.now().isoformat(),
    "status": "COLLECTION_IN_PROGRESS"
}

with open(CORPUS / "PLAIN_LANGUAGE_CORPUS_V1_STATUS.md", 'w', encoding='utf-8') as f:
    f.write(f"# Plain Language Corpus V1 Status\n\n")
    f.write(f"Started: {status['started_at']}\n")
    f.write(f"Target: {status['target']} videos\n")
    f.write(f"Reserve pool: {status['reservoir_size']} candidates\n")
    f.write(f"Collected: {status['collected']}\n")
    f.write(f"Status: {status['status']}\n")

print(f"\nCorpus V1 initialized:")
print(f"  Target: 30 videos")
print(f"  Reserve pool: {len(reserve_pool)} candidates")
print(f"  Directory: {CORPUS}")
print(f"  Media: {MEDIA_DIR}")