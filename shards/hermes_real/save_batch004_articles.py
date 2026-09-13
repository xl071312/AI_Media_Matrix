#!/usr/bin/env python3
"""Save Batch 004 Articles from Progress Data"""
import json
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
BATCH4_DIR = BASE / "analysis_batches" / "batch_004_toutiao"
SEED_DIR = BATCH4_DIR / "SEED_WAVE_001"

# Load progress data
progress_path = BATCH4_DIR / "batch004_progress.json"
with open(progress_path, 'r', encoding='utf-8') as f:
    progress_data = json.load(f)

# Filter for downloaded articles
articles = [r for r in progress_data if r.get('status') == 'DOWNLOADED']

print(f"Found {len(articles)} downloaded articles")

# Save each article as JSON
for art in articles:
    cid = art.get('content_id', '')
    article_path = SEED_DIR / f'{cid}.json'
    
    article_data = {
        'content_id': cid,
        'platform': 'toutiao',
        'content_type': 'ARTICLE',
        'url': f'https://www.toutiao.com/article/{cid}/',
        'title': art.get('title', ''),
        'author': art.get('author', ''),
        'publish_time': art.get('publish_time', ''),
        'text_chars': art.get('text_chars', 0),
        'status': 'DOWNLOADED',
        'fulltext_available': True,
        'notes': 'SEED_WAVE_001'
    }
    
    article_path.write_text(json.dumps(article_data, ensure_ascii=False, indent=2))
    print(f"  Saved: {article_path.name}")

print(f"\nTotal saved: {len(articles)} articles")