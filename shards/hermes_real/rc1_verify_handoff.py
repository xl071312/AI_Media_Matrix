#!/usr/bin/env python3
"""RC1: Generate Handoff Verification Report"""
from pathlib import Path

HANDOFF = Path(r"F:\workspace\AI_Media_Matrix\handoff\chatgpt")
BASE = Path(r"F:\workspace\AI_Media_Matrix")

print("="*70)
print("RC1: Git Handoff Verification Report")
print("="*70)
print()

# Count files
files = list(HANDOFF.rglob('*'))
files = [f for f in files if f.is_file()]

b003_files = list((HANDOFF / "batch_003").rglob('*'))
b003_files = [f for f in b003_files if f.is_file()]

b004_w1_files = list((HANDOFF / "batch_004" / "wave_001").rglob('*'))
b004_w1_files = [f for f in b004_w1_files if f.is_file()]

b004_w2_files = list((HANDOFF / "batch_004" / "wave_002").rglob('*'))
b004_w2_files = [f for f in b004_w2_files if f.is_file()]

global_files = list((HANDOFF / "global").rglob('*'))
global_files = [f for f in global_files if f.is_file()]

print(f"Total handoff files: {len(files)}")
print()
print(f"Batch003: {len(b003_files)} files")
for f in sorted(b003_files):
    print(f"  - {f.relative_to(HANDOFF)}")
print()
print(f"Batch004 Wave001: {len(b004_w1_files)} files")
for f in sorted(b004_w1_files):
    print(f"  - {f.relative_to(HANDOFF)}")
print()
print(f"Batch004 Wave002: {len(b004_w2_files)} files")
for f in sorted(b004_w2_files):
    print(f"  - {f.relative_to(HANDOFF)}")
print()
print(f"Global: {len(global_files)} files")
for f in sorted(global_files):
    print(f"  - {f.relative_to(HANDOFF)}")
print()

# Check ZIP
zip_path = BASE / "handoff" / "CHATGPT_HANDOFF_LATEST.zip"
print(f"ZIP fallback: {zip_path} ({zip_path.stat().st_size} bytes)")
print()
print("="*70)