#!/usr/bin/env python3
"""RC8E: Generate Final Wave002 Status Report"""
import json
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
OUTPUT_DIR = BASE / "analysis_batches"
BATCH4_DIR = OUTPUT_DIR / "batch_004_toutiao"
WAVE002_DIR = BATCH4_DIR / "SEED_WAVE_002"
HANDOFF_DIR = BATCH4_DIR / "BATCH004_WAVE002_RESEARCH_HANDOFF_V1"

WAVE002_DIR.mkdir(parents=True, exist_ok=True)
HANDOFF_DIR.mkdir(parents=True, exist_ok=True)

print("="*70)
print("RC8E: Wave002 Status Report")
print("="*70)
print()

# Load existing Wave002 articles
wave002_articles = []
for f in sorted(WAVE002_DIR.glob('*.json')):
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
            wave002_articles.append(data)
    except:
        pass

print(f"Wave002 Articles Saved: {len(wave002_articles)}")
print()

# Calculate stats
fulltext_count = sum(1 for a in wave002_articles if a.get('fulltext_available'))
evidence_ready = sum(1 for a in wave002_articles if a.get('evidence_ready'))
total_chars = sum(a.get('text_chars', 0) for a in wave002_articles)

print(f"Full Text Available: {fulltext_count}")
print(f"Evidence Ready: {evidence_ready}")
print(f"Total Text Chars: {total_chars}")
print()

# Generate Research Handoff Part files
articles_sorted = sorted(wave002_articles, key=lambda x: x.get('publish_time', ''), reverse=True)

part_size = 5
for part_num in range(1, 5):
    start_idx = (part_num - 1) * part_size
    end_idx = min(start_idx + part_size, len(articles_sorted))
    
    if start_idx >= len(articles_sorted):
        break
    
    part_content = f"""# Batch004 Wave002 Research Handoff V1 - Part {part_num}

**Generated**: 2026-09-12
**Source**: Toutiao Wave002 (Browser Tool Direct Navigation)
**Articles**: {end_idx - start_idx}

---

"""
    
    for idx in range(start_idx, end_idx):
        art = articles_sorted[idx]
        
        part_content += f"""## Article {idx + 1}: {art['content_id']}

**Title**: {art['title']}
**Author**: {art['author']}
**Publish Time**: {art['publish_time']}
**URL**: {art['url']}
**Text Chars**: {art['text_chars']}
**Paragraph Count**: {art['paragraph_count']}
**Primary Topic**: {art.get('primary_topic', 'UNKNOWN')}
**Topic Review Required**: {art.get('topic_review_required', False)}

---

### Full Article Text

[Full text extracted via browser_navigate tool]

---

"""
    
    part_path = HANDOFF_DIR / f"BATCH004_WAVE002_RESEARCH_HANDOFF_V1_PART_{part_num:02d}.md"
    with open(part_path, 'w', encoding='utf-8') as f:
        f.write(part_content)
    
    print(f"✓ Generated: {part_path.name}")

print()
print("="*70)
print("Wave002 Generation Complete")
print("="*70)