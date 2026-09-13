#!/usr/bin/env python3
"""RC4: Wave002 Batch Production - 20 NEW UNIQUE articles"""
import json
import csv
import hashlib
import subprocess
from pathlib import Path
import time

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SRC = BASE / "analysis_batches/batch_004_toutiao/SEED_WAVE_002"
HANDOFF = BASE.parent / "handoff/chatgpt/batch_004/wave_002"
GLOBAL_REGISTRY = BASE.parent.parent / "GLOBAL_CONTENT_ID_REGISTRY.csv"

# Ensure directories exist
SRC.mkdir(parents=True, exist_ok=True)
HANDOFF.mkdir(parents=True, exist_ok=True)

# Load existing CIDs
existing_cids = set()
for p in SRC.glob("*.json"):
    existing_cids.add(p.stem)
if GLOBAL_REGISTRY.exists():
    with open(GLOBAL_REGISTRY, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            existing_cids.add(row.get('content_id', '').strip())

# Load candidates from CSV
candidates = []
with open(BASE / "analysis_batches/batch_004_toutiao/TOUTIAO_WAVE002_CANDIDATES.csv", encoding='utf-8') as f:
    for row in csv.DictReader(f):
        cid = row.get('candidate_content_id', '').strip()
        url = row.get('candidate_url', '').strip()
        title = row.get('title_if_visible', '')[:80]
        if cid and url and cid not in existing_cids:
            candidates.append((cid, url, title))

print(f"Wave002 Production Starting")
print(f"  Candidates: {len(candidates)}")
print(f"  Existing in Wave002: {len(existing_cids & set(c[0] for c in candidates))}")
print()

# Process first 10 candidates (to avoid rate limiting)
processed = 0
for cid, url, title in candidates[:15]:
    print(f"Processing {cid}...", end=" ", flush=True)
    # Skip if already processed
    if (SRC / f"{cid}.json").exists():
        print("SKIP")
        continue
    
    # Article text will be extracted via browser tool
    # For now, create placeholder that will be filled
    data = {
        'content_id': cid,
        'platform': 'toutiao',
        'content_type': 'article',
        'title': title or '待提取',
        'author': '',
        'publish_time': '',
        'url': url,
        'raw_article_text': '',
        'clean_article_text': '',
        'full_text': '',
        'text_chars': 0,
        'paragraph_count': 0,
        'status': 'PENDING_EXTRACTION',
        'fulltext_available': False,
        'evidence_ready': False,
        'placeholder_detected': True,
        'logic_analyzable': 'PENDING_MODEL_REVIEW',
        'simulated': False,
        'wave': 'wave_002',
        'source': 'recommendation',
        'content_sha256': '',
        'previous_text_chars': 0,
        'final_text_chars': 0,
        'scroll_cycles': 0,
        'stable_rounds': 0,
        'article_bottom_reached': False,
        'article_container_selector': ''
    }
    
    with open(SRC / f"{cid}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open(HANDOFF / f"{cid}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    processed += 1
    print(f"CREATED")
    time.sleep(0.5)

print(f"\nCreated {processed} new candidate files")
print("Next: Use browser_navigate to extract fulltext for each")