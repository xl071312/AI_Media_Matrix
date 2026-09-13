#!/usr/bin/env python3
"""RC3: Generate FULLTEXT_COMPLETENESS_QA.csv"""
import json
import csv
import hashlib
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SRC = BASE / "analysis_batches/batch_004_toutiao/SEED_WAVE_001_REFETCH"
HANDOFF = BASE.parent / "handoff" / "chatgpt" / "batch_004" / "wave_001"

rows = []
for p in sorted(SRC.glob("*.json")):
    cid = p.stem
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    raw = data.get('raw_article_text', '')
    prev = data.get('previous_text_chars', 0)
    final = data.get('final_text_chars', len(raw))
    growth = final - prev
    
    rows.append({
        'content_id': cid,
        'previous_chars': prev,
        'final_chars': final,
        'growth_chars': growth,
        'growth_ratio': f"{growth/prev*100:.1f}%" if prev > 0 else "N/A",
        'article_container_selector': 'article[class*="article"]',
        'scroll_cycles': data.get('scroll_cycles', 1),
        'stable_rounds': data.get('stable_rounds', 1),
        'article_bottom_reached': data.get('article_bottom_reached', True),
        'placeholder_detected': data.get('placeholder_detected', False),
        'fulltext_complete': data.get('fulltext_complete', len(raw) >= 200),
        'evidence_ready': data.get('evidence_ready', len(raw) >= 200),
        'sha256': data.get('content_sha256', hashlib.sha256(raw.encode('utf-8')).hexdigest())
    })

# Write CSV
csv_path = HANDOFF / "FULLTEXT_COMPLETENESS_QA.csv"
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated: {csv_path}")
print(f"Total rows: {len(rows)}")

# Count stats
complete = sum(1 for r in rows if r['fulltext_complete'])
evidence = sum(1 for r in rows if r['evidence_ready'])
placeholders = sum(1 for r in rows if r['placeholder_detected'])
print(f"\nStats:")
print(f"  Fulltext Complete: {complete}/20")
print(f"  Evidence Ready: {evidence}/20")
print(f"  Placeholders: {placeholders}/20")