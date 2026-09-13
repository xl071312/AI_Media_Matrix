#!/usr/bin/env python3
"""RC2: Save extracted real text to Wave001 JSONs"""
import json
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SRC = BASE / "analysis_batches/batch_004_toutiao/SEED_WAVE_001_REFETCH"

# Extracted real text from browser_console calls
TEXTS = {
    "7591436947063702022": open("F:/workspace/AI_Media_Matrix/shards/hermes_real/texts/7591436947063702022.txt", "r", encoding="utf-8").read(),
    "7599942867901071906": open("F:/workspace/AI_Media_Matrix/shards/hermes_real/texts/7599942867901071906.txt", "r", encoding="utf-8").read(),
}

print("Loading text files...")
for cid, path in TEXTS.items():
    p = SRC / f"{cid}.json"
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data['raw_article_text'] = path
    data['clean_article_text'] = path
    data['text_chars'] = len(path)
    data['fulltext_available'] = True
    data['evidence_ready'] = True
    data['logic_analyzable'] = 'PENDING_MODEL_REVIEW'
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Updated {cid}: {len(path)} chars")
