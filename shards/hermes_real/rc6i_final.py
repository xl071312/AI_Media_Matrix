#!/usr/bin/env python3
"""RC6I Final Report Generation"""
import csv
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")
INPUT_DIR = BASE / "01_benchmark/analysis_batches/rc6i_deep_input"
MANIFEST = INPUT_DIR / "RC6I_PRIMARY_28_INPUT_MANIFEST.csv"

# Load manifest
rows = list(csv.DictReader(open(MANIFEST, encoding='utf-8')))

# Count stats
full_transcript = sum(1 for r in rows if r.get('transcript_level') == 'FULL_TRANSCRIPT')
partial_transcript = sum(1 for r in rows if r.get('transcript_level') == 'PARTIAL_TRANSCRIPT')
first30_only = sum(1 for r in rows if r.get('transcript_level') == 'FIRST30_ONLY')
transcript_missing = sum(1 for r in rows if r.get('transcript_level') == 'TRANSCRIPT_MISSING')

real_spoken = sum(1 for r in rows if r.get('real_spoken') == 'YES')
first30_available = sum(1 for r in rows if r.get('first30_available') == 'YES')
top_comments = sum(1 for r in rows if r.get('top_comments_available') == 'YES')
evidence = sum(1 for r in rows if r.get('evidence_available') == 'YES')

chatgpt_full = sum(1 for r in rows if r.get('chatgpt_ready') == 'YES' and r.get('analysis_scope') == 'FULL')
chatgpt_partial = sum(1 for r in rows if r.get('chatgpt_ready') == 'YES' and r.get('analysis_scope') == 'PARTIAL')
chatgpt_hook = sum(1 for r in rows if r.get('chatgpt_ready') == 'LIMITED')
chatgpt_not = sum(1 for r in rows if r.get('chatgpt_ready') == 'NO')

print("=" * 60)
print("RC6I PRIMARY INPUT READY")
print("=" * 60)
print(f"\nPRIMARY:\n{len(rows)}")
print(f"\nFULL_TRANSCRIPT:\n{full_transcript}")
print(f"\nPARTIAL_TRANSCRIPT:\n{partial_transcript}")
print(f"\nFIRST30_ONLY:\n{first30_only}")
print(f"\nTRANSCRIPT_MISSING:\n{transcript_missing}")
print(f"\nREAL_SPOKEN:\n{real_spoken}")
print(f"\nFIRST30_AVAILABLE:\n{first30_available}")
print(f"\nTOP_COMMENTS_AVAILABLE:\n{top_comments}")
print(f"\nCHATGPT_FULL_READY:\n{chatgpt_full}")
print(f"\nCHATGPT_PARTIAL_READY:\n{chatgpt_partial}")
print(f"\nCHATGPT_HOOK_ONLY:\n{chatgpt_hook}")
print(f"\nCHATGPT_NOT_READY:\n{chatgpt_not}")
print(f"\nInput:")
print(f"  {INPUT_DIR}/RC6I_PRIMARY_28_INPUT.md")
print(f"  {INPUT_DIR}/RC6I_PRIMARY_28_INPUT_MANIFEST.csv")
print(f"\nReport:")
print(f"  {INPUT_DIR}/RC6I_PRIMARY_28_INPUT_REPORT.md")
print(f"\nCommit:\nb599197")
print(f"\nStatus:\nDEEP_ANALYSIS_INPUT_READY")