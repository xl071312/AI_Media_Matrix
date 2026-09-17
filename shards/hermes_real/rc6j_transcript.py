#!/usr/bin/env python3
"""RC6J: Download and transcribe using proper subprocess"""
import json
import csv
import hashlib
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix")
SHORTLIST = BASE / "01_benchmark/analysis_batches/rc6i_shortlist/RC6I_VERIFIED_SHORTLIST.csv"
OUTPUT_DIR = BASE / "01_benchmark/analysis_batches/rc6j_full_transcripts"
COOKIES = BASE / "01_benchmark/shards/hermes_real/douyin_cookies.txt"
YT_DLP = Path("/e/hermes/hermes-agent/venv/Scripts/yt-dlp.exe")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load PRIMARY samples
shortlist = list(csv.DictReader(open(SHORTLIST, encoding='utf-8')))
primary = [r for r in shortlist if r.get('tier') == 'PRIMARY']
print(f"PRIMARY samples: {len(primary)}")

# Stats
stats = {'media_available': 0, 'asr_success': 0, 'FULL_TRANSCRIPT': 0, 
         'PARTIAL_TRANSCRIPT': 0, 'FIRST30_ONLY': 0, 'TRANSCRIPT_MISSING': 0}

manifest_rows = []

for i, sample in enumerate(primary, 1):
    sample_id = sample.get('sample_id', '')
    url = sample.get('source_url', '')
    
    print(f"\n[{i}/28] {sample_id}")
    
    sample_dir = OUTPUT_DIR / sample_id
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    audio_file = sample_dir / "audio.m4a"
    media_available = False
    failure_reason = ''
    
    # Try yt-dlp download
    try:
        cmd = [
            str(YT_DLP),
            '--extractor-args', 'douyin:api_hostname=douyin.com',
            '-f', 'bestaudio[ext=m4a]',
            '--no-playlist',
            '--cookies', str(COOKIES),
            '-o', str(audio_file),
            url
        ]
        print(f"  Running: yt-dlp...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0 and audio_file.exists():
            media_available = True
            stats['media_available'] += 1
            print(f"  Downloaded: {audio_file.stat().st_size} bytes")
        else:
            error_msg = result.stderr[:300] if result.stderr else 'Unknown error'
            print(f"  Failed: {error_msg}")
            failure_reason = f'yt-dlp: {error_msg[:100]}'
    except Exception as e:
        print(f"  Error: {e}")
        failure_reason = f'Exception: {str(e)[:100]}'
    
    # Run ASR if media available
    segments = []
    total_chars = 0
    transcript_level = 'TRANSCRIPT_MISSING'
    
    if media_available:
        try:
            import faster_whisper
            print(f"  Running ASR...")
            model = faster_whisper.WhisperModel("base", device="cpu", compute_type="int8")
            segments_obj, info = model.transcribe(str(audio_file), beam_size=5, language="zh")
            
            for seg in segments_obj:
                text = seg.text.strip()
                if not text:
                    continue
                segments.append({
                    'segment_id': f"S{len(segments)+1:04d}",
                    'start': round(seg.start, 2),
                    'end': round(seg.end, 2),
                    'raw_text': text
                })
                total_chars += len(text.replace(' ', '').replace('\n', ''))
            
            if segments:
                # Determine level
                # Get duration
                dur_result = subprocess.run(
                    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                     '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_file)],
                    capture_output=True, text=True
                )
                duration = float(dur_result.stdout.strip()) if dur_result.stdout.strip() else 0
                coverage = total_chars / duration if duration > 0 else 0
                
                if coverage >= 5 and len(segments) >= 10:
                    transcript_level = 'FULL_TRANSCRIPT'
                    stats['FULL_TRANSCRIPT'] += 1
                elif coverage >= 2:
                    transcript_level = 'PARTIAL_TRANSCRIPT'
                    stats['PARTIAL_TRANSCRIPT'] += 1
                else:
                    transcript_level = 'FIRST30_ONLY'
                    stats['FIRST30_ONLY'] += 1
                
                stats['asr_success'] += 1
                print(f"  ASR: {total_chars} chars, {len(segments)} segments -> {transcript_level}")
            else:
                transcript_level = 'TRANSCRIPT_MISSING'
                stats['TRANSCRIPT_MISSING'] += 1
                print(f"  ASR empty")
        except Exception as e:
            print(f"  ASR error: {e}")
            transcript_level = 'TRANSCRIPT_MISSING'
            stats['TRANSCRIPT_MISSING'] += 1
    else:
        stats['TRANSCRIPT_MISSING'] += 1
    
    # Save files
    csv_path = sample_dir / "transcript_raw.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['segment_id', 'start', 'end', 'raw_text'])
        for seg in segments:
            writer.writerow([seg['segment_id'], seg['start'], seg['end'], seg['raw_text']])
    
    # Meta
    meta = {
        'sample_id': sample_id,
        'media_available': media_available,
        'transcript_level': transcript_level,
        'segment_count': len(segments),
        'raw_char_count': total_chars,
        'failure_reason': failure_reason
    }
    (sample_dir / "transcript_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    
    # Manifest row
    manifest_rows.append({
        'sample_id': sample_id,
        'source_url': url,
        'media_available': 'YES' if media_available else 'NO',
        'transcript_level': transcript_level,
        'segment_count': len(segments),
        'raw_char_count': total_chars,
        'failure_reason': failure_reason,
        'source_commit': 'b599197'
    })
    
    print(f"  Done: {transcript_level}")

# Save manifest
with open(OUTPUT_DIR / "RC6J_PRIMARY_28_TRANSCRIPT_MANIFEST.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=manifest_rows[0].keys())
    writer.writeheader()
    writer.writerows(manifest_rows)

# Report
report = f"""# RC6J Primary 28 Transcript Report

**Generated**: {datetime.now().isoformat()}
**Source Commit**: b599197

## Results

MEDIA_AVAILABLE = {stats['media_available']}
ASR_SUCCESS = {stats['asr_success']}

FULL_TRANSCRIPT = {stats['FULL_TRANSCRIPT']}
PARTIAL_TRANSCRIPT = {stats['PARTIAL_TRANSCRIPT']}
FIRST30_ONLY = {stats['FIRST30_ONLY']}
TRANSCRIPT_MISSING = {stats['TRANSCRIPT_MISSING']}

## Status

{"RC6J_RAW_TEXT_READY" if stats['media_available'] > 0 else "MEDIA_DOWNLOAD_FAILED"}

---
*本任务只负责原始文本恢复，不做语义分析。*
"""
(OUTPUT_DIR / "RC6J_PRIMARY_28_TRANSCRIPT_REPORT.md").write_text(report, encoding='utf-8')

print(f"\n=== RC6J COMPLETE ===")
print(f"MEDIA_AVAILABLE: {stats['media_available']}/28")
print(f"TRANSCRIPT levels: FULL={stats['FULL_TRANSCRIPT']}, PARTIAL={stats['PARTIAL_TRANSCRIPT']}, FIRST30={stats['FIRST30_ONLY']}, MISSING={stats['TRANSCRIPT_MISSING']}")
print(f"\nOutput: {OUTPUT_DIR}")