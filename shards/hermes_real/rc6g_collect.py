#!/usr/bin/env python3
"""RC6G: Collect and process candidate samples with mechanical gate"""
import json
import csv
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
import urllib.request
import faster_whisper

BASE = Path(r"F:\workspace\AI_Media_Matrix")
CORPUS = BASE / "01_benchmark/plain_language_corpus_v1"
RESERVE_DIR = CORPUS / "rc6g_reserve"
RAW_POOL = BASE / "01_benchmark/shards/hermes_real/douyin_raw/raw_pool_all.jsonl"
HIST_FILE = CORPUS / "HISTORICAL_CONTENT_IDS_CANONICAL.txt"

RESERVE_DIR.mkdir(parents=True, exist_ok=True)

# Load historical IDs
historical_ids = set()
if HIST_FILE.exists():
    with open(HIST_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            cid = line.strip()
            if cid and cid.isdigit():
                historical_ids.add(cid)

print(f"Historical IDs: {len(historical_ids)}")

# Load existing reserve IDs
existing_reserve = set()
for p in RESERVE_DIR.glob("*/01_metadata.json"):
    try:
        with open(p, 'r', encoding='utf-8') as f:
            meta = json.load(f)
            cid = str(meta.get('canonical_content_id', ''))
            if cid:
                existing_reserve.add(cid)
    except:
        pass

print(f"Existing reserve IDs: {len(existing_reserve)}")

# Load raw pool candidates
candidates = []
if RAW_POOL.exists():
    with open(RAW_POOL, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    cand = json.loads(line)
                    aweme_id = str(cand.get('aweme_id', ''))
                    if aweme_id and aweme_id.isdigit():
                        candidates.append(cand)
                except:
                    pass

print(f"Raw pool candidates: {len(candidates)}")

# Filter: exclude historical duplicates and existing
new_candidates = [c for c in candidates 
                  if str(c.get('aweme_id', '')) not in historical_ids
                  and str(c.get('aweme_id', '')) not in existing_reserve]

print(f"New candidates (not historical): {len(new_candidates)}")

# Sort by engagement (mechanical preference)
def engagement_score(c):
    try:
        liked = int(c.get('liked_count', 0))
        comments = int(c.get('comment_count', 0))
        return liked + comments * 2
    except:
        return 0

new_candidates.sort(key=engagement_score, reverse=True)

# Load Whisper model
print("\nLoading Whisper model...")
model = faster_whisper.WhisperModel("base", device="cpu", compute_type="int8")
print("Model loaded.\n")

# Collection targets
TARGET_ATTEMPTS = 60
TARGET_PASS = 40

collected = 0
attempts = 0
passed = 0
failed = 0

manifest_rows = []
performance_rows = []
duplicate_audit_rows = []

for i, cand in enumerate(new_candidates[:TARGET_ATTEMPTS + 50], 1):
    if attempts >= TARGET_ATTEMPTS:
        break
    
    content_id = str(cand.get('aweme_id', ''))
    candidate_id = f"RC6G_{attempts+1:03d}"
    sample_dir = RESERVE_DIR / candidate_id
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[{attempts+1}/{TARGET_ATTEMPTS}] Processing {content_id}...")
    attempts += 1
    
    # Check duration metadata
    # Note: raw pool doesn't have duration, will measure after download
    
    # Download audio
    audio_src = cand.get('music_download_url', '')
    audio_dst = sample_dir / "audio.m4a"
    
    if not audio_src:
        print(f"  No audio URL - skipping")
        failed += 1
        continue
    
    try:
        req = urllib.request.Request(audio_src, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(audio_dst, 'wb') as f:
                import shutil
                shutil.copyfileobj(response, f)
        print(f"  Audio downloaded: {audio_dst.stat().st_size} bytes")
    except Exception as e:
        print(f"  Download failed: {e}")
        failed += 1
        continue
    
    # Measure duration
    duration = None
    if audio_dst.exists():
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_dst)],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            try:
                duration = float(result.stdout.strip())
            except:
                pass
    
    # Run ASR
    print(f"  Running ASR...")
    try:
        segments, info = model.transcribe(str(audio_dst), beam_size=5, language="zh")
        
        transcript_segments = []
        full_text = []
        nonempty_segments = []
        
        for seg in segments:
            text = seg.text.strip()
            if not text:
                continue
            
            segment = {
                "start": round(seg.start, 1),
                "end": round(seg.end, 1),
                "text": text,
                "segment_id": f"S{len(transcript_segments)+1:04d}"
            }
            transcript_segments.append(segment)
            full_text.append(text)
            nonempty_segments.append(text)
        
        full_text_str = "\n".join(full_text)
        transcript_chars = len(full_text_str.replace(" ", "").replace("\n", ""))
        
        # Check first 30s
        first30s_text = "".join([s["text"] for s in transcript_segments if s["end"] <= 30])
        first30s_has_speech = len(first30s_text) > 20
        
        # Speech coverage
        speech_span = sum(s["end"] - s["start"] for s in transcript_segments)
        speech_coverage = speech_span / duration if duration and duration > 0 else 0
        
        # Check for repeated segments
        from collections import Counter
        normalized_segs = [s.lower().strip()[:20] for s in nonempty_segments]
        repeated_ratio = max(Counter(normalized_segs).values()) / len(normalized_segs) if normalized_segs else 0
        
        # Mechanical gate
        mechanical_pass = (
            transcript_chars >= 120 and
            len(transcript_segments) >= 10 and
            len(nonempty_segments) >= 10 and
            (duration is None or duration < 30 or first30s_has_speech) and
            (duration is None or speech_coverage >= 0.30) and
            repeated_ratio <= 0.20
        )
        
        if mechanical_pass:
            passed += 1
            print(f"  ✓ MECHANICAL_PASS: {transcript_chars} chars, {len(transcript_segments)} segments")
        else:
            print(f"  ✗ MECHANICAL_FAIL: {transcript_chars} chars, {len(transcript_segments)} segments")
        
        # Save files
        # 01_metadata.json
        metadata = {
            "candidate_id": candidate_id,
            "raw_content_id": content_id,
            "canonical_content_id": content_id,
            "platform": "douyin",
            "title": (cand.get('title', '') or '')[:200],
            "author": cand.get('nickname', ''),
            "url": cand.get('aweme_url', ''),
            "duration_sec": duration,
            "likes": int(cand.get('liked_count', 0)),
            "comments": int(cand.get('comment_count', 0)),
            "favorites": int(cand.get('collected_count', 0)),
            "shares": int(cand.get('share_count', 0)),
            "source_keyword": cand.get('source_keyword', ''),
            "transcript_chars": transcript_chars,
            "segment_count": len(transcript_segments),
            "nonempty_segment_count": len(nonempty_segments),
            "first30s_has_speech": first30s_has_speech,
            "speech_coverage_ratio": round(speech_coverage, 3),
            "repeated_segment_max_ratio": round(repeated_ratio, 3),
            "mechanical_pass": mechanical_pass,
            "created_at": datetime.now().isoformat()
        }
        (sample_dir / "01_metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
        
        # 02_performance.json
        performance = {
            "likes": metadata['likes'],
            "comments": metadata['comments'],
            "favorites": metadata['favorites'],
            "shares": metadata['shares'],
            "engagement_score": metadata['likes'] + metadata['comments'] * 2 + metadata['shares'] * 3
        }
        (sample_dir / "02_performance.json").write_text(
            json.dumps(performance, ensure_ascii=False, indent=2), encoding='utf-8')
        
        # 03_audio_info.json
        audio_info = {
            "duration_sec": duration,
            "file_size_bytes": audio_dst.stat().st_size if audio_dst.exists() else 0,
            "format": "m4a"
        }
        (sample_dir / "03_audio_info.json").write_text(
            json.dumps(audio_info, ensure_ascii=False, indent=2), encoding='utf-8')
        
        # 04_transcript_raw.md
        md_content = f"# Transcript: {candidate_id}\n\n"
        md_content += f"**Full text** ({transcript_chars} chars):\n\n{full_text_str}\n\n"
        md_content += f"**Segments**: {len(transcript_segments)}\n\n"
        md_content += "## Segments\n\n"
        for seg in transcript_segments:
            md_content += f"- **{seg['start']:.1f}s - {seg['end']:.1f}s**: {seg['text']}\n"
        (sample_dir / "04_transcript_raw.md").write_text(md_content, encoding='utf-8')
        
        # 05_segments.json
        (sample_dir / "05_segments.json").write_text(
            json.dumps(transcript_segments, ensure_ascii=False, indent=2), encoding='utf-8')
        
        # 06_mechanical_metrics.json
        mechanical_metrics = {
            "transcript_chars": transcript_chars,
            "segment_count": len(transcript_segments),
            "nonempty_segment_count": len(nonempty_segments),
            "first30s_has_speech": first30s_has_speech,
            "speech_coverage_ratio": round(speech_coverage, 3),
            "repeated_segment_max_ratio": round(repeated_ratio, 3),
            "mechanical_pass": mechanical_pass
        }
        (sample_dir / "06_mechanical_metrics.json").write_text(
            json.dumps(mechanical_metrics, ensure_ascii=False, indent=2), encoding='utf-8')
        
        collected += 1
        manifest_rows.append(metadata)
        performance_rows.append(performance)
        duplicate_audit_rows.append({
            'raw_content_id': content_id,
            'canonical_content_id': content_id,
            'platform': 'douyin',
            'in_historical_universe': False,  # We filtered these out
            'duplicate_status': 'NEW'
        })
        
    except Exception as e:
        print(f"  ASR failed: {e}")
        failed += 1
        continue
    
    # Stop if we reached target passes
    if passed >= TARGET_PASS:
        print(f"\nReached target of {TARGET_PASS} mechanical passes")
        break

print(f"\n=== RC6G Summary ===")
print(f"Attempts: {attempts}")
print(f"Collected: {collected}")
print(f"Mechanical passes: {passed}")
print(f"Failed: {failed}")
print(f"Reserve directory: {RESERVE_DIR}")