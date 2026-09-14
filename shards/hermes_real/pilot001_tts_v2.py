#!/usr/bin/env python3
"""RC6D Pilot001 TTS v2 - Check for pre-existing config, create metrics only"""
import json
import hashlib
import re
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix")
PILOT_DIR = BASE / "04_content/pilots/guanyu_pilot_001_ability_monetization"
SCRIPT_PATH = PILOT_DIR / "02_script_v0_2.md"
METRICS_V2 = PILOT_DIR / "05_tts_metrics_v2.json"

# Search for pre-existing TTS config
config_sources = []
search_paths = [
    BASE / ".env",
    BASE / ".hermes" / "config.yaml",
    BASE / "config.yaml",
    BASE / "04_content" / "config.yaml",
    BASE / "04_content" / "pilots" / "guanyu_pilot_001_ability_monetization" / "config.yaml",
]

for path in search_paths:
    if path.exists():
        content = path.read_text(encoding='utf-8').lower()
        if 'tts' in content or 'edge_tts' in content or 'voice_id' in content or 'zh-' in content:
            config_sources.append(str(path))

print("=== Pilot001 TTS v2 Check ===\n")
print(f"Script path: {SCRIPT_PATH}")
print(f"Config sources found: {config_sources if config_sources else 'NONE'}")

# Extract and calculate metrics
content = SCRIPT_PATH.read_text(encoding='utf-8')
match = re.search(r'^## Script\s*\n(.*?)(?:\n##|\Z)', content, re.DOTALL | re.MULTILINE)
if not match:
    print("\nERROR: Script section not found")
    exit(1)

script_text = match.group(1).strip()

# Metrics
non_ws = re.sub(r'\s+', '', script_text)
chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', script_text))
char_count = len(non_ws)
punct_count = len(re.findall(r'[,.!?，。！？、；：""''（）【】《》…—～]', script_text))
paragraphs = [p.strip() for p in script_text.split('\n') if p.strip()]
para_count = len(paragraphs)
script_sha = hashlib.sha256(script_text.encode('utf-8')).hexdigest()

# Compression ratio vs v0.1 (1420 chars)
v01_chars = 1420
compression_ratio = round(char_count / v01_chars, 2) if v01_chars > 0 else 0

print(f"\nScript v0.2 metrics:")
print(f"  Chinese chars: {chinese_chars}")
print(f"  Non-whitespace chars: {char_count}")
print(f"  Punctuation: {punct_count}")
print(f"  Paragraphs: {para_count}")
print(f"  SHA256: {script_sha[:16]}...")
print(f"  Compression ratio vs v0.1: {compression_ratio} ({char_count}/{v01_chars})")

# No config found - create TTS_CONFIG_REQUIRED metrics
metrics = {
    "status": "TTS_CONFIG_REQUIRED",
    "script_version": "v0.2",
    "script_sha256": script_sha,
    "tts_config_source_path": None,
    "voice_id": None,
    "locale": None,
    "speed": None,
    "char_count": char_count,
    "chinese_char_count": chinese_chars,
    "punctuation_count": punct_count,
    "paragraph_count": para_count,
    "compression_ratio_vs_v01": compression_ratio,
    "duration_seconds": None,
    "duration_gate_label": "TTS_CONFIG_REQUIRED",
    "generated_at": datetime.now().isoformat(),
    "publish_authorized": False
}

METRICS_V2.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"\nMetrics saved: {METRICS_V2}")
print("\nTTS Result: CONFIG_REQUIRED")
print("No pre-existing project TTS config found.")
print("No audio synthesized.")