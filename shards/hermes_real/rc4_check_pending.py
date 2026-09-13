#!/usr/bin/env python3
"""RC4: Save Wave002 remaining articles to reach 15/20"""
import json
import hashlib
import subprocess
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SRC = BASE / "analysis_batches/batch_004_toutiao/SEED_WAVE_002"
HANDOFF = BASE.parent / "handoff/chatgpt/batch_004/wave_002"

# Check which are already done
done = {p.stem for p in SRC.glob("*.json") if json.load(open(p, 'r', encoding='utf-8')).get('placeholder_detected') == False}
pending = {p.stem for p in SRC.glob("*.json")} - done

print(f"Already real: {len(done)}")
print(f"Still pending: {len(pending)}")
print(f"CIDs pending: {sorted(pending)}")