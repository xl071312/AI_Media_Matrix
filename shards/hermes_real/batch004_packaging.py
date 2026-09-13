#!/usr/bin/env python3
"""Generate Batch 004 Manifest and Evidence Files"""
import json
import csv
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
BATCH4_DIR = BASE / "analysis_batches" / "batch_004_toutiao"
SEED_DIR = BATCH4_DIR / "SEED_WAVE_001"
OUTPUT_DIR = BATCH4_DIR

# Create output dirs
(OUTPUT_DIR / "EVIDENCE").mkdir(parents=True, exist_ok=True)

# Load all articles
articles = []
for f in SEED_DIR.glob('*.json'):
    with open(f, 'r', encoding='utf-8') as fh:
        articles.append(json.load(fh))

print(f"Loaded {len(articles)} articles from SEED_WAVE_001")

# Generate Manifest
manifest_path = OUTPUT_DIR / "CORPUS_CANONICAL_MANIFEST.csv"
with open(manifest_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'canonical_id', 'content_id', 'platform', 'content_type', 'url',
        'title', 'author', 'creator_id', 'publish_time',
        'primary_topic', 'secondary_topics',
        'article_chars', 'paragraph_count', 'fulltext_available',
        'likes', 'comments', 'favorites', 'shares', 'views',
        'performance_verified', 'logic_analyzable', 'simulated', 'notes'
    ])
    writer.writeheader()
    
    for i, art in enumerate(articles, 1):
        writer.writerow({
            'canonical_id': f'B004-{i:03d}',
            'content_id': art.get('content_id', ''),
            'platform': 'toutiao',
            'content_type': 'ARTICLE',
            'url': art.get('url', ''),
            'title': art.get('title', '')[:100],
            'author': art.get('author', ''),
            'creator_id': '',
            'publish_time': art.get('publish_time', ''),
            'primary_topic': '',
            'secondary_topics': '',
            'article_chars': art.get('text_chars', 0),
            'paragraph_count': len(art.get('full_text', '').split('\n')) if art.get('full_text') else 0,
            'fulltext_available': True,
            'likes': None,
            'comments': None,
            'favorites': None,
            'shares': None,
            'views': None,
            'performance_verified': False,
            'logic_analyzable': True,
            'simulated': 'FALSE',
            'notes': 'SEED_WAVE_001'
        })

print(f"Generated manifest: {manifest_path}")

# Generate Evidence Parts (2 parts: 10 articles each)
for part_num in range(1, 3):
    part_articles = articles[(part_num-1)*10:part_num*10]
    part_path = OUTPUT_DIR / "EVIDENCE" / f"ARTICLE_EVIDENCE_FULL_PART_{part_num:02d}.md"
    
    with open(part_path, 'w', encoding='utf-8') as f:
        f.write(f"# 【Batch 004 - Article Evidence Part {part_num}】\n\n")
        f.write(f"**Route**: Direct URL (Seed IDs)\n")
        f.write(f"**Date**: 2026-09-10\n")
        f.write(f"**simulated**: 0\n\n")
        f.write("---\n\n")
        
        for art in part_articles:
            cid = art.get('content_id', '')
            title = art.get('title', '')
            author = art.get('author', '')
            publish_time = art.get('publish_time', '')
            full_text = art.get('full_text', '')
            chars = art.get('text_chars', len(full_text))
            
            f.write(f"## Content ID: {cid}\n\n")
            f.write(f"**Title**: {title}\n\n")
            f.write(f"**Author**: {author}\n\n")
            f.write(f"**Publish Time**: {publish_time}\n\n")
            f.write(f"**URL**: {art.get('url', '')}\n\n")
            f.write(f"**Character Count**: {chars}\n\n")
            f.write(f"**Full Text Available**: TRUE\n\n")
            f.write("---\n\n")
            f.write(full_text)
            f.write("\n\n")
    
    print(f"Generated evidence part {part_num}: {part_path}")

print("\nBatch 004 packaging complete!")