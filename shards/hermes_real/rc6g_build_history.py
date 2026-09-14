#!/usr/bin/env python3
"""RC6G: Build historical ID universe from all sources"""
import json
import csv
import re
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")

print("=== Building Historical ID Universe ===\n")

all_ids = set()

# Source 1: GLOBAL_CONTENT_ID_REGISTRY.csv
registry = BASE / "01_benchmark/GLOBAL_CONTENT_ID_REGISTRY.csv"
if registry.exists():
    with open(registry, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            cid = row.get('content_id', '')
            if cid:
                canonical = cid.replace('DY_REAL_', '').strip()
                if canonical and canonical.isdigit():
                    all_ids.add(canonical)
    print(f"Registry: {len([x for x in all_ids if x.isdigit()])} IDs")

# Source 2: RC6E duplicate audit from git
try:
    import subprocess
    result = subprocess.run(
        ['git', 'show', '3098ced289c460b0b159ce479dd68ca2641fbd2c:01_benchmark/plain_language_corpus_v1/PLAIN_LANGUAGE_CORPUS_V1_DUPLICATE_AUDIT.csv'],
        cwd=BASE, capture_output=True, text=True
    )
    if result.returncode == 0:
        for line in result.stdout.split('\n')[1:]:  # Skip header
            if line.strip():
                parts = line.split(',')
                if len(parts) >= 1 and parts[0].isdigit():
                    all_ids.add(parts[0].strip())
        print(f"RC6E audit: parsed")
except:
    pass

# Source 3: RC6F manifest
rc6f_manifest = BASE / "01_benchmark/plain_language_corpus_v1/PLAIN_LANGUAGE_CORPUS_V1_MANIFEST.csv"
if rc6f_manifest.exists():
    with open(rc6f_manifest, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            cid = row.get('raw_content_id', '') or row.get('canonical_content_id', '')
            if cid and cid.isdigit():
                all_ids.add(cid)
    print(f"RC6F manifest: parsed")

# Source 4: Scan all JSON files for content_id fields
print("\nScanning benchmark data for IDs...")
id_pattern = re.compile(r'"(?:content_id|canonical_content_id|raw_content_id|aweme_id|video_id)"\s*:\s*"(\d+)"')
url_pattern = re.compile(r'/video/(\d{15,20})')

for json_file in BASE.rglob("*.json"):
    if 'plain_language_corpus_v1' in str(json_file) and 'rc6g' not in str(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Find content IDs
                for match in id_pattern.finditer(content):
                    cid = match.group(1)
                    if cid.isdigit() and len(cid) >= 15:
                        all_ids.add(cid)
                # Find video URLs
                for match in url_pattern.finditer(content):
                    cid = match.group(1)
                    if cid.isdigit():
                        all_ids.add(cid)
        except:
            pass

# Source 5: Scan JSONL files
for jsonl_file in BASE.rglob("*.jsonl"):
    if 'plain_language_corpus_v1' in str(jsonl_file):
        continue
    try:
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        for field in ['aweme_id', 'content_id', 'video_id']:
                            cid = str(data.get(field, ''))
                            if cid.isdigit() and len(cid) >= 15:
                                all_ids.add(cid)
                    except:
                        pass
    except:
        pass

# Sort and save
sorted_ids = sorted([x for x in all_ids if x.isdigit()], key=int)
print(f"\nTotal unique historical IDs: {len(sorted_ids)}")

# Save to file
hist_file = BASE / "01_benchmark/plain_language_corpus_v1/HISTORICAL_CONTENT_IDS_CANONICAL.txt"
hist_file.write_text('\n'.join(sorted_ids), encoding='utf-8')
print(f"Saved to: {hist_file}")