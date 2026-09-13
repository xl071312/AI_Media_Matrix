#!/usr/bin/env python3
"""Download audio tracks and mux with video for ASR - RC3"""
import json
import hashlib
import subprocess
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
MEDIA_DIR = BASE / "media" / "batch_002_smoke"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

CIDS = ['7683219193294114063', '7682806976379620660', '7682728905966423334']

def get_urls(cid):
    """Get video+audio URLs from CDP"""
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    context = browser.contexts[0]
    
    page = context.new_page()
    page.goto(f'https://www.douyin.com/video/{cid}', timeout=30000)
    time.sleep(4)
    
    urls = page.evaluate('''() => {
        const entries = performance.getEntriesByType('resource');
        const result = {video: null, audio: null};
        for (const e of entries) {
            const name = e.name;
            if (name.includes('douyinvod') && name.includes('media-video')) {
                if (!result.video) result.video = name.substring(0, 800);
            }
            if (name.includes('douyinvod') && name.includes('media-audio')) {
                if (!result.audio) result.audio = name.substring(0, 800);
            }
        }
        return result;
    }''')
    
    page.close()
    browser.close()
    p.stop()
    return urls

def download_url(url, path, timeout=300):
    """Download from URL"""
    import urllib.request
    req = urllib.request.Request(url, headers={'Referer': 'https://www.douyin.com/'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        with open(path, 'wb') as f:
            while True:
                chunk = resp.read(8192)
                if not chunk: break
                f.write(chunk)
    return path.stat().st_size

def calc_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''): h.update(chunk)
    return h.hexdigest()

def get_duration(path):
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                           "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                          capture_output=True, text=True, timeout=10)
        return float(r.stdout.strip())
    except: return None

def mux_video_audio(video_path, audio_path, output_path):
    """Mux video and audio using ffmpeg"""
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "copy",
        "-map", "0:v:0",
        "-map", "1:a:0",
        str(output_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return result.returncode == 0

def main():
    print("=== AUDIO DOWNLOAD + MUX SMOKE RC3 ===\n")
    
    results = {}
    
    for cid in CIDS:
        print(f"\n--- {cid} ---")
        
        # Get URLs
        print("  Getting URLs...")
        urls = get_urls(cid)
        if not urls.get('audio'):
            print("  ✗ No audio URL found")
            results[cid] = {'status': 'NO_AUDIO_URL'}
            continue
        
        # Download audio
        audio_path = MEDIA_DIR / f"{cid}.audio.m4a"
        print("  Downloading audio...")
        try:
            size = download_url(urls['audio'], audio_path)
            print(f"  ✓ Audio downloaded: {size/1024:.1f} KB")
        except Exception as e:
            print(f"  ✗ Audio download failed: {e}")
            results[cid] = {'status': 'AUDIO_DOWNLOAD_FAILED'}
            continue
        
        # Check audio
        duration = get_duration(audio_path)
        sha256 = calc_sha256(audio_path)
        print(f"  Duration: {duration}s, SHA256: {sha256[:16]}")
        
        # Mux with existing video
        video_path = MEDIA_DIR / f"{cid}.mp4"
        muxed_path = MEDIA_DIR / f"{cid}.muxed.mp4"
        
        if video_path.exists():
            print("  Muxing video + audio...")
            ok = mux_video_audio(video_path, audio_path, muxed_path)
            if ok and muxed_path.exists():
                size_mb = muxed_path.stat().st_size / 1024 / 1024
                print(f"  ✓ Muxed: {size_mb:.1f} MB")
                results[cid] = {'status': 'OK', 'audio_size_kb': size/1024}
            else:
                print(f"  ✗ Mux failed: {ok}")
                results[cid] = {'status': 'MUX_FAILED'}
        else:
            results[cid] = {'status': 'VIDEO_MISSING'}
    
    # Print summary
    print("\n" + "="*50)
    print("RESULTS")
    print("="*50)
    for cid, r in results.items():
        print(f"  {cid}: {r}")
    
    ok_count = sum(1 for r in results.values() if r.get('status') == 'OK')
    print(f"\nAudio downloads: {ok_count}/{len(CIDS)}")
    return ok_count

if __name__ == "__main__":
    count = main()
    print(f"\nsimulated: 0")
    if count >= 2:
        print("✓ AUDIO PIPELINE PASS")
    else:
        print("✗ AUDIO PIPELINE FAIL")
