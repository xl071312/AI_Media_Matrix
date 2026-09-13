#!/usr/bin/env python3
"""ASR Transcription for RC3 muxed videos"""
import json
import hashlib
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
MEDIA_DIR = BASE / "media" / "batch_002_smoke"
TRANSCRIPT_DIR = BASE / "shards" / "hermes_real" / "transcripts_v2"
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

CIDS = ['7683219193294114063', '7682806976379620660', '7682728905966423334']

def run_asr(video_path, cid):
    """Run ASR on video"""
    from faster_whisper import WhisperModel
    print(f"    Loading model...")
    model = WhisperModel("Systran/faster-whisper-base", device="cpu", compute_type="int8")
    
    print(f"    Transcribing...")
    segments, info = model.transcribe(str(video_path), beam_size=5, language="zh")
    
    transcript = []
    for seg in segments:
        transcript.append({
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": seg.text.strip()
        })
    
    # Save raw transcript
    out_path = TRANSCRIPT_DIR / f"{cid}_raw.json"
    out_path.write_text(json.dumps(transcript, ensure_ascii=False, indent=2), encoding='utf-8')
    
    # Save markdown
    full_text = ''.join([s['text'] for s in transcript])
    lines = [
        f"# Raw Transcript: {cid}",
        "",
        f"**Source**: ASR Raw Output",
        f"**Status**: UNVERIFIED_RAW_ASR",
        f"**Note**: Complete transcript embedded.",
        "",
        "---",
        ""
    ]
    for j, seg in enumerate(transcript):
        sm, ss = int(seg['start'] // 60), seg['start'] % 60
        em, es = int(seg['end'] // 60), seg['end'] % 60
        lines.append(f"[S{j+1:04d}] [{sm:02d}:{ss:05.2f}-{em:02d}:{es:05.2f}] {seg['text']}")
    
    md_path = TRANSCRIPT_DIR / f"{cid}_transcript.md"
    md_path.write_text('\n'.join(lines), encoding='utf-8')
    
    return transcript

def main():
    print("=== ASR TRANSCRIPTION RC3 ===\n")
    
    results = []
    for cid in CIDS:
        video_path = MEDIA_DIR / f"{cid}.muxed.mp4"
        if not video_path.exists():
            video_path = MEDIA_DIR / f"{cid}.mp4"
        
        print(f"\n--- {cid} ---")
        try:
            transcript = run_asr(video_path, cid)
            if transcript and len(transcript) > 0:
                print(f"  ✓ ASR complete: {len(transcript)} segments")
                results.append({'cid': cid, 'segments': len(transcript), 'status': 'OK'})
            else:
                print(f"  ✗ Empty transcript")
                results.append({'cid': cid, 'status': 'EMPTY'})
        except Exception as e:
            print(f"  ✗ ASR failed: {e}")
            results.append({'cid': cid, 'status': f'ERROR: {e}'})
    
    print("\n" + "="*50)
    print("ASR RESULTS")
    print("="*50)
    ok_count = sum(1 for r in results if r['status'] == 'OK')
    print(f"Completed: {ok_count}/{len(results)}")
    for r in results:
        print(f"  {r['cid']}: {r['status']}" + (f" ({r['segments']} segs)" if r.get('segments') else ""))
    
    return ok_count

if __name__ == "__main__":
    count = main()
    print(f"\nsimulated: 0")
    if count >= 2:
        print("\n✓ ASR PASS")
    else:
        print(f"\n⚠ ASR PARTIAL ({count}/3)")
