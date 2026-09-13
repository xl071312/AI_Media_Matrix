#!/usr/bin/env python3
"""RC8B: Batch004 JSON Body Audit - Check 20 articles for actual text content"""
import json
import csv
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
OUTPUT_DIR = BASE / "analysis_batches"
SEED_DIR = OUTPUT_DIR / "batch_004_toutiao" / "SEED_WAVE_001"

print("="*70)
print("RC8B: Batch004 JSON Body Audit")
print("="*70)
print()

# Possible body text field names to check
BODY_FIELDS = [
    'full_article_text',
    'article_text', 
    'text',
    'content',
    'body',
    'content_text',
    'article_content',
    'paragraphs',
    'html',
    'content_html',
    'article_body',
    'main_content',
    'content_body'
]

# All keys we'll check
ALL_KEYS = ['content_id', 'url', 'title', 'author', 'publish_time', 
            'platform', 'content_type', 'status', 'fulltext_available',
            'text_chars', 'wave', 'simulated'] + BODY_FIELDS

# Audit each JSON
audit_results = []

print("=== Auditing 20 Article JSONs ===")
print()

for json_file in sorted(SEED_DIR.glob('*.json')):
    cid = json_file.stem
    print(f"Processing: {cid}")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except:
            audit_results.append({
                'content_id': cid,
                'json_file': json_file.name,
                'body_field_detected': 'PARSE_ERROR',
                'body_raw_chars': 0,
                'body_text_chars': 0,
                'paragraph_count': 0,
                'has_nonempty_body': False,
                'metadata_only': True,
                'needs_reacquisition': True,
                'all_keys': ','.join(data.keys()) if data else ''
            })
            print(f"  PARSE ERROR")
            continue
    
    # Get all keys
    keys = list(data.keys())
    
    # Find body field
    body_field = None
    body_raw = None
    body_text = None
    paragraph_count = 0
    has_nonempty_body = False
    metadata_only = True
    
    for field in BODY_FIELDS:
        if field in data:
            value = data[field]
            if value is None:
                continue
            if isinstance(value, str):
                if len(value.strip()) > 0:
                    body_field = field
                    body_raw = value
                    body_text = value.strip()
                    paragraph_count = len([p for p in value.split('\n') if p.strip()])
                    has_nonempty_body = True
                    metadata_only = False
                    break
            elif isinstance(value, list):
                # Check if list of strings
                combined = '\n'.join([str(v) for v in value if isinstance(v, str)])
                if len(combined.strip()) > 0:
                    body_field = field
                    body_raw = combined
                    body_text = combined.strip()
                    paragraph_count = len([p for p in combined.split('\n') if p.strip()])
                    has_nonempty_body = True
                    metadata_only = False
                    break
    
    status = "HAS_BODY" if has_nonempty_body else "NO_BODY"
    print(f"  Body Field: {body_field or 'NONE'}")
    print(f"  Status: {status}")
    if body_text:
        print(f"  Text Chars: {len(body_text)}")
        print(f"  Paragraphs: {paragraph_count}")
    else:
        print(f"  Keys: {keys}")
    
    audit_results.append({
        'content_id': cid,
        'json_file': json_file.name,
        'body_field_detected': body_field or 'NONE',
        'body_raw_chars': len(body_raw) if body_raw else 0,
        'body_text_chars': len(body_text) if body_text else 0,
        'paragraph_count': paragraph_count,
        'has_nonempty_body': str(has_nonempty_body),
        'metadata_only': str(metadata_only),
        'needs_reacquisition': str(not has_nonempty_body),
        'all_keys': ','.join(keys)
    })
    print()

# ============================================================
# Generate JSON_BODY_AUDIT.csv
# ============================================================
print("=== Generating JSON_BODY_AUDIT.csv ===")
print()

audit_path = OUTPUT_DIR / "batch_004_toutiao" / "JSON_BODY_AUDIT.csv"
with open(audit_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'content_id', 'json_file', 'body_field_detected', 
        'body_raw_chars', 'body_text_chars', 'paragraph_count',
        'has_nonempty_body', 'metadata_only', 'needs_reacquisition',
        'all_keys'
    ])
    writer.writeheader()
    writer.writerows(audit_results)

print(f"✓ Generated: {audit_path.name}")
print()

# ============================================================
# Summary Statistics
# ============================================================
print("=== Summary Statistics ===")
print()

total = len(audit_results)
with_body = len([r for r in audit_results if r['has_nonempty_body'] == 'True'])
metadata_only_count = len([r for r in audit_results if r['metadata_only'] == 'True'])
needs_reacquisition = len([r for r in audit_results if r['needs_reacquisition'] == 'True'])

print(f"Total Articles: {total}")
print(f"JSON With Nonempty Body: {with_body}/{total}")
print(f"Metadata Only: {metadata_only_count}/{total}")
print(f"Reacquisition Required: {needs_reacquisition}/{total}")
print()

if with_body > 0:
    print("Branch A: JSON contains actual text content")
    print("Action: Fix packaging program and regenerate manifest")
else:
    print("Branch B: All JSONs are metadata-only")
    print("Action: Re-fetch articles using authenticated Chrome")
print()

# Show articles with bodies
if with_body > 0:
    print("=== Articles With Body Text ===")
    for r in audit_results:
        if r['has_nonempty_body'] == 'True':
            print(f"  {r['content_id']}: {r['body_text_chars']} chars ({r['body_field_detected']})")
print()

# Show articles without bodies  
if metadata_only_count > 0:
    print("=== Articles Without Body Text (Metadata Only) ===")
    for r in audit_results:
        if r['metadata_only'] == 'True':
            print(f"  {r['content_id']}: Keys={r['all_keys']}")
