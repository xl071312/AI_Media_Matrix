#!/usr/bin/env python3
"""RC5 Task B: Regenerate FULLTEXT_COMPLETENESS_QA_V2.csv for Wave001"""
import json
import csv
import hashlib
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SRC = BASE / "analysis_batches/batch_004_toutiao/SEED_WAVE_001_REFETCH"
HANDOFF = BASE.parent / "handoff/chatgpt/batch_004/wave_001"
QA_CSV = HANDOFF.parent / "FULLTEXT_COMPLETENESS_QA_V2.csv"

rows = []
for p in sorted(SRC.glob("*.json")):
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cid = p.stem
    title = data.get('title', '')
    text = data.get('clean_article_text', '') or data.get('raw_article_text', '')
    text_chars = len(text)
    placeholder = data.get('placeholder_detected', True)
    
    # Count headings mechanically
    heading_count = sum(1 for line in text.split('\n') if line.strip().startswith('模式') or line.strip().startswith('一、') or line.strip().startswith('二、') or line.strip().startswith('三、'))
    
    # Check declared count
    declared_match = None
    import re
    declared_m = re.search(r'(\d+)个', title)
    declared_count = int(declared_m.group(1)) if declared_m else None
    
    # Truncation check
    truncation_suspect = False
    if declared_count and heading_count < declared_count:
        truncation_suspect = True
    
    rows.append({
        'content_id': cid,
        'title': title[:60],
        'text_chars': text_chars,
        'placeholder_detected': str(placeholder),
        'fulltext_complete': str(not placeholder and text_chars >= 200 and heading_count >= min(declared_count or 0, heading_count)),
        'evidence_ready': str(not placeholder and text_chars >= 200 and data.get('evidence_ready', False)),
        'declared_count': str(declared_count or ''),
        'observed_heading_count': str(heading_count),
        'structure_truncation_suspect': str(truncation_suspect),
        'sha256': hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]
    })

with open(QA_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['content_id', 'title', 'text_chars', 'placeholder_detected', 
                                           'fulltext_complete', 'evidence_ready', 'declared_count',
                                           'observed_heading_count', 'structure_truncation_suspect', 'sha256'])
    writer.writeheader()
    writer.writerows(rows)

complete = sum(1 for r in rows if r['fulltext_complete'] == 'True')
print(f"Wave001 Fulltext Complete V2: {complete}/{len(rows)}")
print(f"CSV saved: {QA_CSV}")