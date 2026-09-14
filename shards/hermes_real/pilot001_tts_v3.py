#!/usr/bin/env python3
"""RC6D Pilot001 TTS v3 - Exact config from tts_config_v0_1.yaml"""
import asyncio
import json
import hashlib
import re
import subprocess
from pathlib import Path
from datetime import datetime
import edge_tts
import yaml

BASE = Path(r"F:\workspace\AI_Media_Matrix")
PILOT_DIR = BASE / "04_content/pilots/guanyu_pilot_001_ability_monetization"
CONFIG_PATH = BASE / "02_style_system/tts_config_v0_1.yaml"
SCRIPT_PATH = PILOT_DIR / "02_script_v0_2.md"
METRICS_V3 = PILOT_DIR / "05_tts_metrics_v3.json"
AUDIO_V3 = PILOT_DIR / "05_tts_draft_v3.mp3"

# Expected values
EXPECTED_SHA = "db1c7fc61dd38088d1990dfd37c50086ca210fc3aff5a5db334d6eb46d0fe903"
EXPECTED_CHARS = 888

async def main():
    # Load config
    print("=== Pilot001 TTS v3 ===\n")
    if not CONFIG_PATH.exists():
        print(f"ERROR: Config not found: {CONFIG_PATH}")
        return
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    voice_id = config.get('voice_id')
    rate = config.get('rate', '+0%')
    pitch = config.get('pitch', '+0Hz')
    volume = config.get('volume', '+0%')
    provider = config.get('provider')
    locale = config.get('locale')
    
    print(f"Config: {CONFIG_PATH}")
    print(f"Voice: {voice_id}")
    print(f"Rate: {rate}")
    
    # Step 1: Check voice availability
    voices = await edge_tts.list_voices()
    zh_voices = [v for v in voices if v['Locale'] == locale]
    voice_exists = any(v['ShortName'] == voice_id for v in zh_voices)
    
    print(f"\nStep 1 - Voice check:")
    print(f"  Locale: {locale}")
    print(f"  Target voice: {voice_id}")
    print(f"  Available voices in locale: {len(zh_voices)}")
    print(f"  Voice exists: {'✓' if voice_exists else '✗'}")
    
    if not voice_exists:
        print("\nVOICE_UNAVAILABLE - stopping")
        metrics = {
            "status": "VOICE_UNAVAILABLE",
            "script_version": "v0.2",
            "script_sha256": None,
            "config_version": config.get('version'),
            "tts_config_source_path": str(CONFIG_PATH),
            "provider": provider,
            "voice_id": voice_id,
            "locale": locale,
            "rate": rate,
            "pitch": pitch,
            "volume": volume,
            "char_count": None,
            "chinese_char_count": None,
            "punctuation_count": None,
            "paragraph_count": None,
            "compression_ratio_vs_v01": None,
            "duration_seconds": None,
            "duration_gate_label": "VOICE_UNAVAILABLE",
            "audio_path": None,
            "generated_at": datetime.now().isoformat(),
            "publish_authorized": False,
            "brand_voice_frozen": False
        }
        METRICS_V3.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')
        return
    
    # Step 2: Script integrity check
    print(f"\nStep 2 - Script integrity:")
    content = SCRIPT_PATH.read_text(encoding='utf-8')
    match = re.search(r'^## Script\s*\n(.*?)(?:\n##|\Z)', content, re.DOTALL | re.MULTILINE)
    if not match:
        print("  ERROR: Script section not found")
        return
    
    script_text = match.group(1).strip()
    
    # Calculate metrics
    non_ws = re.sub(r'\s+', '', script_text)
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', script_text))
    punct_count = len(re.findall(r'[,.!?，。！？、；：""''（）【】《》…—～]', script_text))
    paragraphs = [p.strip() for p in script_text.split('\n') if p.strip()]
    para_count = len(paragraphs)
    char_count = len(non_ws)
    script_sha = hashlib.sha256(script_text.encode('utf-8')).hexdigest()
    
    # Compression ratio vs v0.1 (1420 chars)
    compression_ratio = round(char_count / 1420, 2)
    
    print(f"  Script SHA256: {script_sha[:16]}...")
    print(f"  Expected SHA: {EXPECTED_SHA[:16]}...")
    print(f"  SHA match: {'✓' if script_sha == EXPECTED_SHA else '✗'}")
    print(f"  Char count: {char_count}")
    print(f"  Expected chars: {EXPECTED_CHARS}")
    print(f"  Chars match: {'✓' if char_count == EXPECTED_CHARS else '✗'}")
    print(f"  Chinese chars: {chinese_chars}")
    print(f"  Punctuation: {punct_count}")
    print(f"  Paragraphs: {para_count}")
    print(f"  Compression ratio: {compression_ratio}")
    
    if script_sha != EXPECTED_SHA or char_count != EXPECTED_CHARS:
        print("\nSCRIPT_INTEGRITY_FAIL - stopping")
        metrics = {
            "status": "SCRIPT_INTEGRITY_FAIL",
            "script_version": "v0.2",
            "script_sha256": script_sha,
            "config_version": config.get('version'),
            "tts_config_source_path": str(CONFIG_PATH),
            "provider": provider,
            "voice_id": voice_id,
            "locale": locale,
            "rate": rate,
            "pitch": pitch,
            "volume": volume,
            "char_count": char_count,
            "chinese_char_count": chinese_chars,
            "punctuation_count": punct_count,
            "paragraph_count": para_count,
            "compression_ratio_vs_v01": compression_ratio,
            "duration_seconds": None,
            "duration_gate_label": "SCRIPT_INTEGRITY_FAIL",
            "audio_path": None,
            "generated_at": datetime.now().isoformat(),
            "publish_authorized": False,
            "brand_voice_frozen": False
        }
        METRICS_V3.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')
        return
    
    # Step 3: Synthesize
    print(f"\nStep 3 - Synthesizing...")
    comm = edge_tts.Communicate(script_text, voice_id, rate=rate, pitch=pitch)
    await comm.save(str(AUDIO_V3))
    print(f"  Audio saved: {AUDIO_V3}")
    
    # Measure duration
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 
                           'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
                           str(AUDIO_V3)], capture_output=True, text=True)
    duration = float(result.stdout.strip()) if result.stdout.strip() else 0
    print(f"  Duration: {duration:.1f}s")
    
    # Determine gate
    if 240 <= duration <= 300:
        gate = "TTS_DURATION_PASS"
    elif 230 <= duration < 240:
        gate = "TTS_DURATION_REVIEW_SHORT"
    elif 300 < duration <= 310:
        gate = "TTS_DURATION_REVIEW_LONG"
    elif duration < 230:
        gate = "TTS_DURATION_FAIL_SHORT"
    else:
        gate = "TTS_DURATION_FAIL_LONG"
    
    print(f"  Gate: {gate}")
    
    # Create metrics
    metrics = {
        "status": gate,
        "script_version": "v0.2",
        "script_sha256": script_sha,
        "config_version": config.get('version'),
        "tts_config_source_path": str(CONFIG_PATH),
        "provider": provider,
        "voice_id": voice_id,
        "locale": locale,
        "rate": rate,
        "pitch": pitch,
        "volume": volume,
        "char_count": char_count,
        "chinese_char_count": chinese_chars,
        "punctuation_count": punct_count,
        "paragraph_count": para_count,
        "compression_ratio_vs_v01": compression_ratio,
        "duration_seconds": round(duration, 1),
        "duration_gate_label": gate,
        "audio_path": str(AUDIO_V3),
        "generated_at": datetime.now().isoformat(),
        "publish_authorized": False,
        "brand_voice_frozen": False
    }
    
    METRICS_V3.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\nMetrics saved: {METRICS_V3}")
    print(f"\nTTS Result: {gate}")
    print(f"Publish authorized: False (locked)")

if __name__ == "__main__":
    asyncio.run(main())