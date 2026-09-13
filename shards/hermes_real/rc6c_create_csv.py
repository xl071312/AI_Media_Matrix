#!/usr/bin/env python3
"""RC6C: Create proper CSV files for wave_003_real"""
import json
import csv
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")
REAL_DIR = BASE / "handoff/chatgpt/batch_004/wave_003_real"

# Read all articles
articles = []
for p in REAL_DIR.glob("*.json"):
    with open(p, 'r', encoding='utf-8') as f:
        articles.append(json.load(f))

# Create TOPIC_GATE.csv
topic_gate_path = REAL_DIR / "TOPIC_GATE.csv"
with open(topic_gate_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['content_id', 'title', 'gate_status', 'topic_category', 'theme', 'search_seed'])
    for art in articles:
        writer.writerow([
            art.get('content_id', ''),
            art.get('title', '')[:100],
            art.get('topic_gate', 'UNKNOWN'),
            art.get('topic_category', ''),
            art.get('theme', ''),
            art.get('search_seed', '')
        ])

# Create FULLTEXT_QA.csv
qa_path = REAL_DIR / "FULLTEXT_QA.csv"
with open(qa_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['content_id', 'title', 'text_chars', 'placeholder_detected', 'evidence_ready', 'logic_analyzable', 'sha256'])
    for art in articles:
        writer.writerow([
            art.get('content_id', ''),
            art.get('title', '')[:100],
            art.get('text_chars', 0),
            art.get('placeholder_detected', False),
            art.get('evidence_ready', False),
            art.get('logic_analyzable', ''),
            art.get('sha256', '')
        ])

# Create DISCOVERY_LOG.csv
discovery_path = REAL_DIR / "DISCOVERY_LOG.csv"
with open(discovery_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['discovered_at', 'discovery_mode', 'search_seed', 'source_search_url_or_parent_url', 'candidate_url', 'content_id', 'title', 'fetch_status'])
    for art in articles:
        writer.writerow([
            art.get('publish_date', ''),
            art.get('discovery_mode', 'UNKNOWN'),
            art.get('search_seed', ''),
            art.get('url', ''),
            art.get('url', ''),
            art.get('content_id', ''),
            art.get('title', '')[:100],
            'FETCHED' if art.get('placeholder_detected') == False else 'FAILED'
        ])

# Create CROSS_BATCH_DEDUPE.csv
dedupe_path = REAL_DIR / "CROSS_BATCH_DEDUPE.csv"
with open(dedupe_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['content_id', 'found_in', 'status'])
    # Check against Wave001 and Wave002
    w1_ids = set((BASE / "01_benchmark/analysis_batches/batch_004_toutiao/SEED_WAVE_001_REFETCH").glob("*.json"))
    w2_ids = set((BASE / "01_benchmark/analysis_batches/batch_004_toutiao/SEED_WAVE_002").glob("*.json"))
    for art in articles:
        cid = art.get('content_id', '')
        in_w1 = any(p.stem == cid for p in w1_ids)
        in_w2 = any(p.stem == cid for p in w2_ids)
        if in_w1 or in_w2:
            writer.writerow([cid, 'WAVE001/WAVE002', 'DUPLICATE_REJECTED'])
        else:
            writer.writerow([cid, '', 'NEW_UNIQUE'])

print(f"Created CSV files in {REAL_DIR}")
print(f"  TOPIC_GATE.csv: {len(articles)} rows")
print(f"  FULLTEXT_QA.csv: {len(articles)} rows")
print(f"  DISCOVERY_LOG.csv: {len(articles)} rows")
print(f"  CROSS_BATCH_DEDUPE.csv: {len(articles)} rows")