#!/usr/bin/env python3
"""Process remaining ASR jobs - runs one at a time with checkpoint"""
import json
import csv
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
OUTPUT_DIR = BASE / "analysis_batches" / "batch_001"
CHECKPOINT_FILE = OUTPUT_DIR / ".asr_checkpoint.json"

def load_checkpoint():
    if CHECKPOINT_FILE.exists():
        return json.load(open(CHECKPOINT_FILE))
    return {"completed": [], "failed": []}

def save_checkpoint(cp):
    CHECKPOINT_FILE.write_text(json.dumps(cp, indent=2, ensure_ascii=False))

def get_duration(path):
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                           capture_output=True, text=True, timeout=10)
        return float(r.stdout.strip())
    except:
        return None

def calc_metrics(transcript, duration):
    import re
    full_text = ''.join([s['text'] for s in transcript])
    return {
        "duration_sec": round(duration, 2),
        "asr_segment_count": len(transcript),
        "total_chars": len(full_text),
        "chars_per_sec": round(len(full_text) / max(duration, 1), 2),
        "first_person_count": len(re.findall(r'[我咱俺]', full_text)),
        "second_person_count": len(re.findall(r'[你您]', full_text)),
        "number_count": len(re.findall(r'\d+', full_text)),
        "question_marker_count": full_text.count('？') + full_text.count('?'),
        "transcript_sha256": hashlib.sha256(full_text.encode('utf-8')).hexdigest()[:16]
    }

def main():
    print("=== ASR QUEUE PROCESSOR ===\n")
    
    # Load selection
    with open(SHARDS / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        selection = {row.get('aweme_id'): row for row in reader}
    
    cp = load_checkpoint()
    completed = set(cp.get('completed', []))
    failed = set(cp.get('failed', []))
    
    # Existing samples
    existing = set()
    for s in OUTPUT_DIR.glob("sample_*"):
        meta_f = s / "01_metadata.json"
        if meta_f.exists():
            existing.add(json.load(open(meta_f)).get('content_id', ''))
    
    # Build pending list
    pending = []
    for d in sorted(VIDEO_DIR.glob("*/")):
        cid = d.name
        if cid in existing or cid in completed or cid in failed:
            continue
        video_path = d / "video.mp4"
        trans_file = TRANSCRIPT_DIR / f"{cid}_raw.json"
        if video_path.exists() and not trans_file.exists():
            pending.append({'id': cid, 'path': video_path, 
                          'row': selection.get(cid), 'from_sel': cid in selection})
    
    print(f"Pending: {len(pending)}, Completed: {len(completed)}, Failed: {len(failed)}")
    
    processed = 0
    for item in pending:
        cid = item['id']
        print(f"\n--- ASR: {cid} ---")
        try:
            from faster_whisper import WhisperModel
            model = WhisperModel("Systran/faster-whisper-base", device="cpu", compute_type="int8")
            segments, info = model.transcribe(str(item['path']), beam_size=5, language="zh")
            
            transcript = []
            for seg in segments:
                transcript.append({"start": seg.start, "end": seg.end, "text": seg.text.strip()})
            
            (TRANSCRIPT_DIR / f"{cid}_raw.json").write_text(json.dumps(transcript, ensure_ascii=False, indent=2))
            print(f"  ✓ Transcribed: {len(transcript)} segments")
            
            completed.add(cid)
            save_checkpoint({"completed": list(completed), "failed": list(failed)})
            
            # Create sample directory
            next_id = len(sorted(OUTPUT_DIR.glob("sample_*"))) + 1
            sample_dir = OUTPUT_DIR / f"sample_{next_id:02d}"
            sample_dir.mkdir(parents=True, exist_ok=True)
            
            duration = get_duration(item['path']) or (transcript[-1]['end'] if transcript else 0)
            metrics = calc_metrics(transcript, duration)
            
            row = item['row']
            if row:
                vt_raw = row.get('viral_type', '')
                vt = vt_raw.split(';')[0] if ';' in vt_raw else vt_raw
                title = row.get('desc', '')[:150] or 'NULL'
                creator = row.get('nickname', '') or 'NULL'
                topic = row.get('source_keyword', '') or 'NULL'
                role = row.get('sample_role', '') or 'NULL'
                likes = int(row.get('liked_count', 0)) if row.get('liked_count') else None
                comments = int(row.get('comment_count', 0)) if row.get('comment_count') else None
                favorites = int(row.get('collected_count', 0)) if row.get('collected_count') else None
                shares = int(row.get('share_count', 0)) if row.get('share_count') else None
                source = "MEDIACRAWLER_REAL_CDP"
            else:
                vt = "UNKNOWN"
                title = "NULL"
                creator = "NULL"
                topic = "NULL"
                role = "EXTERNAL_DATA"
                likes = comments = favorites = shares = None
                source = "EXTERNAL"
            
            meta = {"content_id": cid, "url": f"https://www.douyin.com/video/{cid}",
                    "creator_id": creator, "creator_name": creator, "title": title,
                    "topic": topic, "viral_type": vt, "sample_role": role,
                    "duration_sec": round(duration, 2), "capture_time": datetime.now().isoformat(),
                    "metadata_source": source}
            (sample_dir / "01_metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
            
            perf = {"likes": likes, "comments": comments, "favorites": favorites, "shares": shares}
            if isinstance(likes, int) and isinstance(likes, int):
                perf["favorite_like_ratio"] = round(favorites / max(likes, 1), 3) if likes > 0 else 0
                perf["share_like_ratio"] = round(shares / max(likes, 1), 3) if likes > 0 else 0
                perf["comment_like_ratio"] = round(comments / max(likes, 1), 3) if likes > 0 else 0
            (sample_dir / "02_performance.json").write_text(json.dumps(perf, indent=2, ensure_ascii=False))
            
            (sample_dir / "03_creator_baseline.json").write_text(json.dumps({
                "status": "NOT_COLLECTED", "note": "Requires API access or DOM fallback",
                "creator_id": creator
            }, indent=2, ensure_ascii=False))
            
            (sample_dir / "04_transcript_raw.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
            
            with open(sample_dir / "05_transcript_raw.md", 'w', encoding='utf-8') as f:
                f.write(f"# Raw Transcript: {cid}\n\n**Source**: ASR Raw Output\n**Status**: UNVERIFIED_RAW_ASR\n\n---\n\n")
                for seg in transcript:
                    sm, ss = int(seg['start']//60), seg['start']%60
                    em, es = int(seg['end']//60), seg['end']%60
                    f.write(f"[{seg['segment_id']}] [{sm:02d}:{ss:05.2f}-{em:02d}:{es:05.2f}] {seg['text']}\n")
            
            (sample_dir / "06_metrics_basic.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False))
            
            with open(sample_dir / "07_top_comments.csv", 'w', encoding='utf-8') as f:
                f.write("comment_id,author,text,likes,reply_count,created_time\n")
                f.write("# To be collected\n")
            
            manifest = {"content_id": cid, "media_path": str(item['path']),
                        "media_size_mb": round(item['path'].stat().st_size/1024/1024, 2),
                        "media_sha256": hashlib.sha256(item['path'].read_bytes()).hexdigest()[:16],
                        "transcript_sha256": metrics['transcript_sha256'],
                        "segment_count": len(transcript), "duration_sec": round(duration, 2)}
            (sample_dir / "08_evidence_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
            
            print(f"  ✓ Sample {next_id:02d} created")
            processed += 1
            
            # Stop after 2 per run to avoid timeout
            if processed >= 2:
                print("\n--- Checkpoint saved, processing paused (max 2 per run) ---")
                break
                
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed.add(cid)
            save_checkpoint({"completed": list(completed), "failed": list(failed)})
    
    final_count = len(list(OUTPUT_DIR.glob("sample_*")))
    print(f"\n=== BATCH STATUS ===")
    print(f"Total samples: {final_count}/10")
    print(f"Completed this run: {processed}")

if __name__ == "__main__":
    main()
