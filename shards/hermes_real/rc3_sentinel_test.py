#!/usr/bin/env python3
"""RC3: Scroll-based article body extraction for Wave001 (Sentinel 3)"""
import json
import time
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SRC = BASE / "analysis_batches/batch_004_toutiao/SEED_WAVE_001_REFETCH"

# Sentinel articles to test scroll extraction
SENTINELS = ["7591436947063702022", "7599942867901071906", "7610800331743707700"]

print("RC3 Sentinel Validation - Testing scroll extraction")
print("=" * 60)

results = []
for cid in SENTINELS:
    p = SRC / f"{cid}.json"
    if not p.exists():
        print(f"MISSING: {cid}")
        continue
    
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    previous_chars = len(data.get('raw_article_text', ''))
    print(f"\n{cid}: previous={previous_chars} chars")
    print(f"  Title: {data.get('title', '')[:50]}...")
    
    # Will be updated by browser tool after scroll extraction
    results.append({
        'cid': cid,
        'previous_chars': previous_chars,
        'final_chars': previous_chars,  # placeholder until browser confirms
        'growth': 0
    })

print("\n" + "=" * 60)
print("Sentinel test initiated. Proceeding to browser extraction...")