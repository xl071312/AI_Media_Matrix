#!/usr/bin/env python3
"""RC1: Generate Git Handoff Files"""
import json
import csv
import shutil
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix")
BENCHMARK = BASE / "01_benchmark"
OUTPUT_DIR = BASE / "analysis_batches"
HANDOFF_DIR = BASE / "handoff" / "chatgpt"

# Create directory structure
HANDOFF_DIR.mkdir(parents=True, exist_ok=True)
(HANDOFF_DIR / "global").mkdir(exist_ok=True)
(HANDOFF_DIR / "batch_003").mkdir(exist_ok=True)
(HANDOFF_DIR / "batch_004" / "wave_001").mkdir(parents=True, exist_ok=True)
(HANDOFF_DIR / "batch_004" / "wave_002").mkdir(parents=True, exist_ok=True)
(HANDOFF_DIR / "manifests").mkdir(exist_ok=True)

print("="*70)
print("RC1: Generating Git Handoff Files")
print("="*70)
print()

# ============================================================
# 1. Copy Batch003 files
# ============================================================
print("=== Step 1: Batch003 Files ===")
print()

b003_sources = [
    ("BATCH003_INTERIM_STATUS.md", "FINAL_B003_STATUS.md"),
    ("CORPUS_CANONICAL_MANIFEST_INTERIM.csv", "CORPUS_CANONICAL_MANIFEST_B003.csv"),
    ("PERFORMANCE_METRICS_INTERIM.csv", "PERFORMANCE_METRICS_B003.csv"),
    ("EVIDENCE_FULL_PART_01.md", "EVIDENCE_FULL_PART_01.md"),
]

for src_name, dst_name in b003_sources:
    src = OUTPUT_DIR / "batch_003" / src_name
    dst = HANDOFF_DIR / "batch_003" / dst_name
    if src.exists():
        shutil.copy2(src, dst)
        print(f"✓ {src_name} -> {dst_name}")
    else:
        print(f"✗ MISSING: {src_name}")

print()

# ============================================================
# 2. Copy Batch004 Wave001 files
# ============================================================
print("=== Step 2: Batch004 Wave001 Files ===")
print()

wave001_src_dir = OUTPUT_DIR / "batch_004_toutiao" / "SEED_WAVE_001_REFETCH"
wave001_dst_dir = HANDOFF_DIR / "batch_004" / "wave_001"

# Copy JSON files
json_count = 0
for f in wave001_src_dir.glob('*.json'):
    shutil.copy2(f, wave001_dst_dir / f.name)
    json_count += 1

print(f"✓ Copied {json_count} JSON files to wave_001/")

# Copy manifest
manifest_src = OUTPUT_DIR / "batch_004_toutiao" / "CORPUS_CANONICAL_MANIFEST_V4.csv"
manifest_dst = wave001_dst_dir / "CORPUS_CANONICAL_MANIFEST_V4.csv"
if manifest_src.exists():
    shutil.copy2(manifest_src, manifest_dst)
    print(f"✓ CORPUS_CANONICAL_MANIFEST_V4.csv")

# Copy QA file
qa_src = OUTPUT_DIR / "batch_004_toutiao" / "BATCH004_WAVE001_FULLTEXT_QA.csv"
qa_dst = wave001_dst_dir / "BATCH004_WAVE001_FULLTEXT_QA.csv"
if qa_src.exists():
    shutil.copy2(qa_src, qa_dst)
    print(f"✓ BATCH004_WAVE001_FULLTEXT_QA.csv")

print()

# ============================================================
# 3. Copy Batch004 Wave002 files
# ============================================================
print("=== Step 3: Batch004 Wave002 Files ===")
print()

wave002_src_dir = OUTPUT_DIR / "batch_004_toutiao" / "SEED_WAVE_002"
wave002_dst_dir = HANDOFF_DIR / "batch_004" / "wave_002"

# Copy JSON files
json_count = 0
for f in wave002_src_dir.glob('*.json'):
    shutil.copy2(f, wave002_dst_dir / f.name)
    json_count += 1

print(f"✓ Copied {json_count} JSON files to wave_002/")

# Copy candidates file
candidates_src = OUTPUT_DIR / "batch_004_toutiao" / "TOUTIAO_WAVE002_CANDIDATES.csv"
candidates_dst = wave002_dst_dir / "TOUTIAO_WAVE002_CANDIDATES.csv"
if candidates_src.exists():
    shutil.copy2(candidates_src, candidates_dst)
    print(f"✓ TOUTIAO_WAVE002_CANDIDATES.csv")

print()

# ============================================================
# 4. Copy Global files
# ============================================================
print("=== Step 4: Global Files ===")
print()

global_files = [
    ("GLOBAL_CORPUS_LEDGER_V5.csv", None),
    ("GLOBAL_COMPARISON_FEATURES_V4.csv", None),
]

for filename, _ in global_files:
    src = OUTPUT_DIR / filename
    dst = HANDOFF_DIR / "global" / filename
    if src.exists():
        shutil.copy2(src, dst)
        print(f"✓ {filename}")
    else:
        print(f"✗ MISSING: {filename}")

print()

# ============================================================
# 5. Generate CURRENT_STATUS.md
# ============================================================
print("=== Step 5: Generate CURRENT_STATUS.md ===")
print()

status_content = f"""# ChatGPT Handoff - Current Status

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source**: AI_Media_Matrix Benchmark Project

---

## Verified Logic Corpus

| Metric | Value |
|--------|-------|
| **Verified Logic Corpus** | **60/100** |
| Independent Logic Observations | 59 |
| Evidence Ready Pending Review | **23** |
| Performance Verified | 46 |

---

## Batch Status

| Batch | Unique CID | Logic Analyzable | Evidence Ready | Status |
|-------|------------|------------------|----------------|--------|
| Block001 | 24 | **20** | - | FROZEN |
| Block002 | 32 | **32** | 32 | COMPLETE |
| Block003 | 9 | **8** | 8 | COOLDOWN |
| Block004 Wave001 | 20 | **0** (pending) | **20** | COMPLETE |
| Block004 Wave002 | 4 | **0** (pending) | **3** | IN_PROGRESS |
| **TOTAL** | **89** | **60** | **63** | - |

---

## Current Collection Status

### Douyin (Batch003)
- **Status**: COOLDOWN (rate-limited)
- **Qualified**: 9/30
- **Blocked**: 47 (captcha/login wall)
- **Cooldown Remaining**: ~2 hours

### Toutiao (Batch004)
- **Status**: Wave002 IN_PROGRESS
- **Wave001**: 20/20 articles recovered
- **Wave002**: 4/27 candidates processed
- **Route**: browser_navigate (confirmed working)

---

## Current Blockers

1. **Douyin Rate Limiting**: 4hr cooldown required, resume with smoke test
2. **Wave002 Candidate Quality**: Many candidates are old articles (>2024) or LOGIN_WALL
3. **Browser Tool**: Primary route confirmed, Playwright CDP retired

---

## Next Actions

1. Continue Wave002 production via browser_navigate
2. After 4hr cooldown, resume Batch003 with smoke test
3. Target: Wave002 reach 20 Evidence Ready
4. Then await main analysis model review

---

## File Inventory

### Global
- GLOBAL_CORPUS_LEDGER_V5.csv (89 rows)
- GLOBAL_COMPARISON_FEATURES_V4.csv (89 rows)

### Batch003
- FINAL_B003_STATUS.md
- CORPUS_CANONICAL_MANIFEST_B003.csv
- PERFORMANCE_METRICS_B003.csv
- EVIDENCE_FULL_PART_01.md

### Batch004 Wave001
- 20 JSON files (full text)
- CORPUS_CANONICAL_MANIFEST_V4.csv
- BATCH004_WAVE001_FULLTEXT_QA.csv

### Batch004 Wave002
- 4 JSON files (full text)
- TOUTIAO_WAVE002_CANDIDATES.csv

---

**Handoff Complete**. Awaiting Git commit and push.
"""

status_path = HANDOFF_DIR / "CURRENT_STATUS.md"
with open(status_path, 'w', encoding='utf-8') as f:
    f.write(status_content)

print(f"✓ CURRENT_STATUS.md generated")
print()

# ============================================================
# 6. Print Summary
# ============================================================
print("="*70)
print("Handoff File Generation Complete")
print("="*70)
print()
print(f"Handoff Directory: {HANDOFF_DIR}")
print()
print("Files Generated:")
for f in sorted(HANDOFF_DIR.rglob('*')):
    if f.is_file():
        print(f"  {f.relative_to(HANDOFF_DIR)}")
print()
print("Next: Git initialization and commit")