#!/usr/bin/env python3
"""RC6D Pilot001 TTS Check - Mechanical only"""
import asyncio
import json
import hashlib
import re
from pathlib import Path
from datetime import datetime
import edge_tts

BASE = Path(r"F:\workspace\AI_Media_Matrix")
PILOT_DIR = BASE / "04_content/pilots/guanyu_pilot_001_ability_monetization"
SCRIPT_PATH = PILOT_DIR / "02_script_v0_1.md"
OUTPUT_JSON = PILOT_DIR / "05_tts_metrics.json"
OUTPUT_AUDIO = PILOT_DIR / "05_tts_draft.mp3"

async def get_chinese_voice():
    """Find a suitable Chinese voice"""
    voices = await edge_tts.list_voices()
    zh_voices = [v for v in voices if 'zh' in v['Locale'].lower()]
    # Prefer female voices for narration
    for v in zh_voices:
        if v['Gender'] == 'Female':
            return v['ShortName']
    if zh_voices:
        return zh_voices[0]['ShortName']
    return None

async def main():
    # Read and extract script
    content = SCRIPT_PATH.read_text(encoding='utf-8')
    match = re.search(r'^## Script\s*\n(.*?)(?:\n##|\Z)', content, re.DOTALL | re.MULTILINE)
    if not match:
        print("ERROR: Script section not found")
        return
    
    script_text = match.group(1).strip()
    
    # Calculate metrics
    non_ws = re.sub(r'\s+', '', script_text)
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', script_text))
    punct_count = len(re.findall(r'[,.!?，。！？、；：""''（）【】《》…—～]', script_text))
    paragraphs = [p.strip() for p in script_text.split('\n') if p.strip()]
    para_count = len(paragraphs)
    char_count = len(non_ws)
    
    # SHA256 of script
    script_sha = hashlib.sha256(script_text.encode('utf-8')).hexdigest()
    
    # Get voice
    voice = await get_chinese_voice()
    if not voice:
        print("ERROR: No Chinese voice found")
        return
    
    print(f"Voice: {voice}")
    print(f"Chinese chars: {chinese_chars}")
    print(f"Non-whitespace chars: {char_count}")
    print(f"Punctuation: {punct_count}")
    print(f"Paragraphs: {para_count}")
    
    # Generate TTS
    comm = edge_tts.Communicate(script_text, voice)
    await comm.save(str(OUTPUT_AUDIO))
    print(f"Audio saved: {OUTPUT_AUDIO}")
    
    # Measure duration (approximate: 4-5 chars per second for Chinese)
    import subprocess
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 
                           'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
                           str(OUTPUT_AUDIO)], capture_output=True, text=True)
    duration = float(result.stdout.strip()) if result.stdout.strip() else 0
    
    print(f"Duration: {duration:.1f}s")
    
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
    
    print(f"Gate: {gate}")
    
    # Create metrics JSON
    metrics = {
        "script_sha256": script_sha,
        "tts_config_source": "edge-tts (system default)",
        "voice_id": voice,
        "speed": None,  # Not explicitly configured
        "char_count": char_count,
        "punctuation_count": punct_count,
        "paragraph_count": para_count,
        "duration_seconds": round(duration, 1),
        "duration_gate_label": gate,
        "generated_at": datetime.now().isoformat(),
        "publish_authorized": False
    }
    
    OUTPUT_JSON.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\nMetrics saved: {OUTPUT_JSON}")
    print("DONE")

if __name__ == "__main__":
    asyncio.run(main())