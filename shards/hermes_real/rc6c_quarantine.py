#!/usr/bin/env python3
"""RC6C: Quarantine invalid RC6B Wave003 items"""
import shutil
import csv
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")
SRC = BASE / "01_benchmark/analysis_batches/batch_004_toutiao/SEED_WAVE_003"
HANDOFF = BASE / "handoff/chatgpt/batch_004/wave_003"
INVALID_DIR = BASE / "handoff/chatgpt/batch_004/wave_003_invalid_rc6b"
REAL_DIR = BASE / "handoff/chatgpt/batch_004/wave_003_real"

# Create quarantine directory
INVALID_DIR.mkdir(parents=True, exist_ok=True)
REAL_DIR.mkdir(parents=True, exist_ok=True)

# Items to quarantine (synthetic IDs and duplicates)
QUARANTINE = [
    # Synthetic IDs
    "7682293131710300706",
    "7682446926645559860",
    "7682745433508069888",
    "7682800000000000001",
    "7682900000000000002",
    "7683000000000000003",
    "7683110588213363240",
    "7683200000000000004",
    "7683300000000000005",
    "7683400000000000006",
    "7683600000000000007",
    "7683700000000000008",
    "7683800000000000009",
    # Duplicates from earlier batches
    "7671488207304868404",
    "7683168637653598759",
    "7684223864338924073",
    "7680513034233676323",
]

manifest_rows = []
for cid in QUARANTINE:
    src_path = HANDOFF / f"{cid}.json"
    if src_path.exists():
        import json
        with open(src_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Move to invalid dir
        dest_path = INVALID_DIR / f"{cid}.json"
        shutil.move(str(src_path), str(dest_path))
        # Also move from source if exists
        src_src = SRC / f"{cid}.json"
        if src_src.exists():
            shutil.move(str(src_src), str(INVALID_DIR.parent / f"{cid}.json"))
        manifest_rows.append({
            "content_id": cid,
            "title": data.get("title", "")[:80],
            "reason": "synthetic_id_or_duplicate_or_short_text",
            "text_chars": len(data.get("raw_article_text", ""))
        })
        print(f"Quarantined: {cid} ({len(data.get('raw_article_text', ''))} chars)")

# Create manifest CSV
manifest_path = INVALID_DIR / "INVALID_MANIFEST.csv"
with open(manifest_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['content_id', 'title', 'reason', 'text_chars'])
    writer.writeheader()
    writer.writerows(manifest_rows)

print(f"\nQuarantined {len(manifest_rows)} items")
print(f"Manifest: {manifest_path}")