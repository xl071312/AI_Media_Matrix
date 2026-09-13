#!/usr/bin/env python3
"""RC8C: Generate Research Handoff V2 Markdown Files"""
import json
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
OUTPUT_DIR = BASE / "analysis_batches"
REFETCH_DIR = OUTPUT_DIR / "batch_004_toutiao" / "SEED_WAVE_001_REFETCH"
HANDOFF_DIR = OUTPUT_DIR / "batch_004_toutiao" / "BATCH004_RESEARCH_HANDOFF_V2"

HANDOFF_DIR.mkdir(parents=True, exist_ok=True)

# Load saved articles
articles = []
for f in sorted(REFETCH_DIR.glob('*.json')):
    with open(f, 'r', encoding='utf-8') as fh:
        try:
            data = json.load(fh)
            if data.get('content_id') and data.get('fulltext_available'):
                articles.append(data)
        except:
            pass

print(f"Loaded {len(articles)} articles for handoff")
print()

# Generate 4 parts
part_size = 5
for part_num in range(1, 5):
    start_idx = (part_num - 1) * part_size
    end_idx = min(start_idx + part_size, len(articles))
    
    if start_idx >= len(articles):
        break
    
    part_content = f"""# Batch004 Research Handoff V2 - Part {part_num}

**Generated**: 2026-09-12
**Source**: Toutiao Wave001 Refetch
**Articles**: {end_idx - start_idx}

---

"""
    
    for idx in range(start_idx, end_idx):
        art = articles[idx]
        body_text = art.get('full_text', '')
        
        part_content += f"""## Article {idx + 1}: {art['content_id']}

**Title**: {art['title']}
**Author**: {art['author']}
**Publish Time**: {art['publish_time']}
**URL**: {art['url']}
**Text Chars**: {art['text_chars']}
**Paragraphs**: {art['paragraph_count']}

---

### Full Article Text

{body_text}

---

"""
    
    part_path = HANDOFF_DIR / f"BATCH004_RESEARCH_HANDOFF_V2_PART_{part_num:02d}.md"
    with open(part_path, 'w', encoding='utf-8') as f:
        f.write(part_content)
    
    print(f"✓ Generated: {part_path.name} ({end_idx - start_idx} articles)")

print()
print("="*70)
print("RC8C Research Handoff V2 Generation Complete")
print("="*70)