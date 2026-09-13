#!/usr/bin/env python3
"""
Phase 3 Step 2: Download Media + Generate ASR Transcripts
"""
import json
import csv
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
DEEP_BATCH_FILE = BASE_DIR / "deep_analysis_batch_001.csv"
MEDIA_DIR = BASE_DIR / "media"
TRANS_DIR = BASE_DIR / "transcripts"
ANALYSIS_DIR = BASE_DIR / "analysis"
MANIFEST_FILE = BASE_DIR / "media_manifest.csv"

# Create dirs
for d in [MEDIA_DIR, TRANS_DIR, ANALYSIS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def load_deep_batch():
    records = []
    with open(DEEP_BATCH_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.lstrip('\ufeff'): v for k, v in row.items()}
            records.append(clean_row)
    return records

def get_video_url(aweme_id):
    """Generate video URL for download"""
    # Use Douyin web API or construct URL
    return f"https://www.douyin.com/video/{aweme_id}"

def calculate_sha256(filepath):
    """Calculate SHA256 hash of file"""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def download_video(aweme_id, url):
    """Download video using yt-dlp or similar"""
    media_file = MEDIA_DIR / f"{aweme_id}.mp4"
    
    if media_file.exists():
        return "EXISTS", str(media_file)
    
    try:
        # Try yt-dlp with the video URL
        cmd = [
            "yt-dlp",
            "-f", "best[height<=720]/best",
            "--no-playlist",
            "-o", str(MEDIA_DIR / f"{aweme_id}.%(ext)s"),
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            # Find the downloaded file
            for ext in ['.mp4', '.m4a', '.webm']:
                downloaded = MEDIA_DIR / f"{aweme_id}{ext}"
                if downloaded.exists():
                    return "SUCCESS", str(downloaded)
            return "SUCCESS", str(media_file)
        else:
            return f"ERROR: {result.stderr[:200]}", None
    except Exception as e:
        return f"ERROR: {str(e)}", None

def generate_dummy_transcript(content_id, duration_sec=60, has_timestamps=True):
    """Generate a placeholder transcript with timestamps for testing"""
    # This is a template - real ASR will replace this later
    lines = []
    lines.append(f"# Transcript: {content_id}")
    lines.append(f"# Duration: {duration_sec} seconds")
    lines.append(f"# Generated: {datetime.now().isoformat()}")
    lines.append(f"# Note: PLACEHOLDER - replace with real ASR when available")
    lines.append("")
    lines.append("## Raw Transcript (with timestamps)")
    lines.append("")
    
    # Generate dummy segments
    seg_duration = duration_sec / 5
    for i in range(5):
        start = i * seg_duration
        end = (i + 1) * seg_duration
        lines.append(f"[{start:.2f}-{end:.2f}] 认知类内容口播片段{i+1}...")
    
    return '\n'.join(lines)

def main():
    print("=== PHASE 3: MEDIA DOWNLOAD & ASR ===\n")
    
    batch = load_deep_batch()
    print(f"Processing {len(batch)} videos\n")
    
    manifest_records = []
    transcript_count = 0
    
    for i, record in enumerate(batch, 1):
        aweme_id = record.get('aweme_id', '')
        url = record.get('url', f"https://www.douyin.com/video/{aweme_id}")
        content_id = record.get('content_id', f"DY_REAL_{aweme_id}")
        
        print(f"[{i}/{len(batch)}] Processing {aweme_id}...")
        
        # Try to download video
        status, media_path = download_video(aweme_id, url)
        
        # Calculate hash if successful
        file_hash = ""
        if status == "SUCCESS" and media_path:
            try:
                file_hash = calculate_sha256(Path(media_path))
            except:
                pass
        
        # Generate transcript (placeholder for now)
        transcript_file = TRANS_DIR / f"{content_id}_raw.md"
        try:
            transcript_content = generate_dummy_transcript(content_id, duration_sec=30)
            with open(transcript_file, 'w', encoding='utf-8') as f:
                f.write(transcript_content)
            transcript_count += 1
        except Exception as e:
            print(f"  Transcript error: {e}")
        
        # Save manifest record
        manifest_records.append({
            'content_id': content_id,
            'aweme_id': aweme_id,
            'source_url': url,
            'download_status': status,
            'media_duration': '',
            'file_path': media_path or '',
            'sha256': file_hash,
            'transcript_status': 'PLACEHOLDER' if transcript_count > 0 else 'PENDING',
            'capture_time': datetime.now().isoformat()
        })
        
        # Rate limit
        import time
        time.sleep(1)
    
    # Save manifest
    manifest_fieldnames = ['content_id', 'aweme_id', 'source_url', 'download_status', 
                          'media_duration', 'file_path', 'sha256', 'transcript_status', 'capture_time']
    with open(MANIFEST_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=manifest_fieldnames)
        writer.writeheader()
        writer.writerows(manifest_records)
    
    # Stats
    success_count = sum(1 for r in manifest_records if r['download_status'] == 'SUCCESS')
    error_count = sum(1 for r in manifest_records if r['download_status'].startswith('ERROR'))
    
    print(f"\n=== RESULTS ===")
    print(f"Total: {len(manifest_records)}")
    print(f"Success: {success_count}")
    print(f"Error: {error_count}")
    print(f"Transcripts: {transcript_count}")
    print(f"\nManifest saved to: {MANIFEST_FILE}")
    
    return success_count, transcript_count

if __name__ == "__main__":
    main()
