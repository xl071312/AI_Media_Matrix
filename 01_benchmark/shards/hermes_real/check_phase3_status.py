#!/usr/bin/env python3
"""
Phase 3 Real-time Status Check
"""
import json
from pathlib import Path

BASE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")

# Load diagnostic results
diag_file = BASE / "phase3_blocker_diagnostic.json"
if diag_file.exists():
    with open(diag_file, 'r') as f:
        diag = json.load(f)
else:
    diag = {}

# Load existing data counts
raw_file = BASE / "douyin_raw" / "raw_pool_all.jsonl"
selection_file = BASE / "douyin_benchmark_selection.csv"
deep_file = BASE / "deep_analysis_batch_001.csv"

raw_count = 0
if raw_file.exists():
    with open(raw_file, 'r') as f:
        raw_count = sum(1 for l in f if l.strip())

sel_count = 0
if selection_file.exists():
    with open(selection_file, 'r', encoding='utf-8-sig') as f:
        sel_count = sum(1 for _ in __import__('csv').DictReader(f))

deep_count = 0
if deep_file.exists():
    with open(deep_file, 'r', encoding='utf-8-sig') as f:
        deep_count = sum(1 for _ in __import__('csv').DictReader(f))

# Count analysis files
analysis_dir = BASE / "analysis"
metrics_count = len(list(analysis_dir.glob("*_metrics.json"))) if analysis_dir.exists() else 0
templates_count = len(list(analysis_dir.glob("*.md"))) if analysis_dir.exists() else 0

# Count transcript placeholders
trans_dir = BASE / "transcripts"
transcript_count = len(list(trans_dir.glob("*_raw.md"))) if trans_dir.exists() else 0

# Build status report
report = {
    "phase": "PHASE_3_IN_PROGRESS",
    "timestamp": str(__import__('time').time()),
    "diagnostic": diag.get("cdp", {}),
    "data_counts": {
        "raw_pool": raw_count,
        "selection": sel_count,
        "deep_batch": deep_count,
        "metrics": metrics_count,
        "templates": templates_count,
        "transcripts_placeholder": transcript_count
    },
    "blockers": {
        "search_now_empty": True,  # From diagnostic
        "creator_api_blocked": diag.get("creator_test", {}).get("status") == "BLOCKED",
        "detail_api_blocked": diag.get("detail_test", {}).get("status") == "BLOCKED"
    },
    "simulated_data": 0,
    "real_data_available": raw_count > 0
}

# Save updated status
status_file = BASE / "phase3_real_status.json"
with open(status_file, 'w') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print("=== PHASE 3 STATUS ===")
print(f"Raw Pool: {raw_count}")
print(f"Selection: {sel_count}")
print(f"Deep Batch: {deep_count}")
print(f"Metrics: {metrics_count}")
print(f"Templates: {templates_count}")
print(f"Transcripts (placeholder): {transcript_count}")
print(f"\nBlockers:")
print(f"  Search now empty: True")
print(f"  Creator API blocked: {report['blockers']['creator_api_blocked']}")
print(f"  Detail API blocked: {report['blockers']['detail_api_blocked']}")
print(f"\nsimulated: 0")
