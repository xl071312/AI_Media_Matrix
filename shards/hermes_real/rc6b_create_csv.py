#!/usr/bin/env python3
"""RC6B: Create CSV files for Wave003"""
import json
import csv
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")
HANDOFF = BASE / "handoff/chatgpt/batch_004/wave_003"
SRC = BASE / "01_benchmark/analysis_batches/batch_004_toutiao/SEED_WAVE_003"

# Read all articles
articles = []
for p in SRC.glob("*.json"):
    with open(p, 'r', encoding='utf-8') as f:
        articles.append(json.load(f))

# Create TOPIC_GATE.csv
topic_gate_path = HANDOFF / "TOPIC_GATE.csv"
with open(topic_gate_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['content_id', 'title', 'gate_status', 'topic_category', 'theme', 'search_seed'])
    for art in articles:
        writer.writerow([
            art['content_id'],
            art['title'][:100],
            art.get('topic_gate', 'UNKNOWN'),
            art.get('topic_category', ''),
            art.get('theme', ''),
            art.get('search_seed', '')
        ])

# Create FULLTEXT_QA.csv
qa_path = HANDOFF / "FULLTEXT_QA.csv"
with open(qa_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['content_id', 'title', 'text_chars', 'placeholder_detected', 'evidence_ready', 'logic_analyzable', 'sha256'])
    for art in articles:
        writer.writerow([
            art['content_id'],
            art['title'][:100],
            art.get('text_chars', 0),
            art.get('placeholder_detected', False),
            art.get('evidence_ready', False),
            art.get('logic_analyzable', ''),
            art.get('sha256', '')
        ])

# Create DISCOVERY_LOG.csv
discovery_path = HANDOFF / "DISCOVERY_LOG.csv"
with open(discovery_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['content_id', 'title', 'discovery_mode', 'search_seed', 'source_url', 'gate_status'])
    for art in articles:
        writer.writerow([
            art['content_id'],
            art.get('title', '')[:100],
            art.get('discovery_mode', 'QUERY_FIRST'),
            art.get('search_seed', ''),
            art.get('url', ''),
            art.get('topic_gate', '')
        ])

print(f"Created TOPIC_GATE.csv with {len(articles)} rows")
print(f"Created FULLTEXT_QA.csv with {len(articles)} rows")
print(f"Created DISCOVERY_LOG.csv with {len(articles)} rows")

# Summary
passed = sum(1 for a in articles if a.get('topic_gate') == 'TOPIC_PASS_MECHANICAL')
review = sum(1 for a in articles if a.get('topic_gate') == 'TOPIC_REVIEW_REQUIRED')
off = sum(1 for a in articles if a.get('topic_gate') == 'OFF_TOPIC_MECHANICAL')
print(f"\nSummary: PASS={passed}, REVIEW={review}, OFF={off}")