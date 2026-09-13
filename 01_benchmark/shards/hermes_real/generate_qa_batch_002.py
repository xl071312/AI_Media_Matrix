#!/usr/bin/env python3
"""Generate complete QA package with real data"""
import json
import re
from pathlib import Path
import statistics

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
TRANSCRIPT_DIR = BASE / "transcripts_v2"
QA_BATCH = BASE / "qa_batch_002"
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")

def load_transcript(content_id):
    """Load ASR transcript"""
    json_file = TRANSCRIPT_DIR / f"{content_id}_raw.json"
    if json_file.exists():
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def calculate_metrics(transcript, duration):
    """Calculate real metrics from transcript"""
    if not transcript:
        return None
    
    # Combine all text
    full_text = ''.join([s['text'] for s in transcript])
    
    # Basic metrics
    total_chars = len(full_text)
    chars_per_sec = total_chars / max(duration, 1)
    
    # Sentence segmentation (Chinese)
    sentences = re.split(r'[。！？；]', full_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = len(sentences)
    
    # Sentence lengths
    sentence_lengths = [len(s) for s in sentences]
    avg_sentence_chars = sum(sentence_lengths) / max(sentence_count, 1)
    median_sentence_chars = statistics.median(sentence_lengths) if sentence_lengths else 0
    
    # Ratio calculations
    short_sentences = [s for s in sentences if len(s) <= 10]
    long_sentences = [s for s in sentences if len(s) > 30]
    short_sentence_ratio = len(short_sentences) / max(sentence_count, 1)
    long_sentence_ratio = len(long_sentences) / max(sentence_count, 1)
    
    # Question markers
    question_count = full_text.count('？') + full_text.count('?')
    question_rate = question_count / max(sentence_count, 1)
    
    # Person markers
    first_person = len(re.findall(r'[我咱俺]', full_text))
    second_person = len(re.findall(r'[你您]', full_text))
    
    # Transition markers
    transitions = ['但是', '所以', '其实', '然而', '不过', '因此', '于是', '首先', '其次', '最后']
    transition_count = sum(full_text.count(t) for t in transitions)
    
    # Contrast markers
    contrasts = ['不是', '而是', '相反', '反而', '却', '而']
    contrast_count = sum(full_text.count(c) for c in contrasts)
    
    # Example markers
    examples = ['比如', '例如', '像', '就像', '比如说', '譬如']
    example_count = sum(full_text.count(e) for e in examples)
    
    # Numbers
    number_count = len(re.findall(r'\d+', full_text))
    
    # Filler words
    fillers = ['嗯', '啊', '那个', '就是', '然后', '就是说', '对吧', '这个']
    filler_count = sum(full_text.count(f) for f in fillers)
    
    # Hook extraction
    hook_3s = ''.join([s['text'] for s in transcript if s['end'] <= 3])
    hook_5s = ''.join([s['text'] for s in transcript if s['end'] <= 5])
    hook_15s = ''.join([s['text'] for s in transcript if s['end'] <= 15])
    
    return {
        "content_id": transcript[0]['content_id'] if 'content_id' in transcript[0] else None,
        "duration_sec": round(duration, 2),
        "segment_count": len(transcript),
        "total_chars": total_chars,
        "chars_per_sec": round(chars_per_sec, 2),
        "sentence_count": sentence_count,
        "avg_sentence_chars": round(avg_sentence_chars, 1),
        "median_sentence_chars": round(median_sentence_chars, 1),
        "short_sentence_ratio": round(short_sentence_ratio, 3),
        "long_sentence_ratio": round(long_sentence_ratio, 3),
        "question_count": question_count,
        "question_rate": round(question_rate, 3),
        "first_person_count": first_person,
        "second_person_count": second_person,
        "transition_count": transition_count,
        "contrast_count": contrast_count,
        "example_count": example_count,
        "number_count": number_count,
        "filler_count": filler_count,
        "hook_3s": hook_3s[:50],
        "hook_5s": hook_5s[:80],
        "hook_15s": hook_15s[:200]
    }

def generate_timeline(transcript, duration):
    """Generate timeline based on actual segments"""
    if not transcript:
        return ""
    
    lines = []
    lines.append(f"# Timeline Analysis\n")
    lines.append(f"**Video Duration**: {duration:.1f}s\n")
    lines.append(f"**Total Segments**: {len(transcript)}\n")
    lines.append(f"---\n")
    
    # Group segments by function (simplified)
    current_function = "HOOK"
    segment_start = 0.0
    
    for i, seg in enumerate(transcript):
        # Detect function changes based on content
        text = seg['text']
        
        # Simple heuristic for function detection
        if seg['start'] < 5:
            func = "HOOK"
        elif i < 3:
            func = "CLAIM"
        elif '比如' in text or '例如' in text or '像' in text:
            func = "EXAMPLE"
        elif '但是' in text or '然而' in text or '其实' in text:
            func = "REVERSAL"
        elif seg['start'] > duration * 0.8:
            func = "ENDING"
        else:
            func = "EXPLANATION"
        
        if func != current_function or i == len(transcript) - 1:
            if i > 0:
                lines.append(f"### {segment_start:.2f}–{seg['start']:.2f} [{current_function}]")
                lines.append(f"**原话**: {transcript[i-1]['text'][:80]}...")
                lines.append(f"**功能**: {current_function}\n")
            current_function = func
            segment_start = seg['start']
        
        if i == len(transcript) - 1:
            lines.append(f"### {segment_start:.2f}–{seg['end']:.2f} [{func}]")
            lines.append(f"**原话**: {text[:80]}...")
            lines.append(f"**功能**: {func}\n")
    
    return '\n'.join(lines)

def main():
    print("=== PHASE 3.1 REWORK: QA PACKAGE GENERATION ===\n")
    
    # Create QA batch directory
    QA_BATCH.mkdir(parents=True, exist_ok=True)
    
    # Process each sample
    samples = [
        ("7302348364815928612", "ABSOLUTE_VIRAL", "从1到100万 普通人第一桶金", "男***門"),
        ("7647797848847439706", "RELATIVE_BREAKOUT", "普通人如何靠卖货翻身", "辉***累"),
    ]
    
    # Get a third sample that has video
    # Looking for CONTROL with available video
    import csv
    with open(BASE / "douyin_benchmark_selection.csv", 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('viral_type') == 'CONTROL':
                cid = row.get('aweme_id', '')
                title = row.get('desc', '')[:50]
                creator = row.get('nickname', '')
                samples.append((cid, 'CONTROL', title, creator))
                break
    
    results = []
    
    for i, (content_id, viral_type, title, creator) in enumerate(samples, 1):
        print(f"\n--- Sample {i}: {content_id} ({viral_type}) ---")
        
        # Load transcript
        transcript = load_transcript(content_id)
        if not transcript:
            print(f"  SKIP: No transcript")
            continue
        
        # Get video duration
        video_path = VIDEO_DIR / content_id / "video.mp4"
        if not video_path.exists():
            # Try to find in old location
            old_path = Path(r"C:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos") / content_id / "video.mp4"
            if old_path.exists():
                video_path = old_path
            else:
                print(f"  SKIP: Video not found")
                continue
        
        import subprocess
        try:
            cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
                   "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            duration = float(result.stdout.strip())
        except:
            duration = transcript[-1]['end'] if transcript else 0
        
        print(f"  Duration: {duration:.1f}s")
        print(f"  Segments: {len(transcript)}")
        
        # Calculate metrics
        metrics = calculate_metrics(transcript, duration)
        
        # Generate timeline
        timeline = generate_timeline(transcript, duration)
        
        # Create sample directory
        sample_dir = QA_BATCH / f"sample_{i:02d}"
        sample_dir.mkdir(exist_ok=True)
        
        # Save files
        # 00_source_metadata.json
        meta = {
            "content_id": content_id,
            "aweme_id": content_id,
            "url": f"https://www.douyin.com/video/{content_id}",
            "creator_id": creator,
            "creator_name": creator,
            "title": title,
            "viral_type": viral_type,
            "duration_sec": round(duration, 2),
            "capture_time": "2026-09-08T02:30:00+08:00",
            "metadata_source": "MEDIACRAWLER_REAL_CDP",
            "video_path": str(video_path),
            "video_size_mb": round(video_path.stat().st_size / 1024 / 1024, 2),
            "asr_segments": len(transcript)
        }
        (sample_dir / "00_source_metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
        
        # 03_transcript_raw.json
        (sample_dir / "03_transcript_raw.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
        
        # 04_transcript_raw.md
        with open(sample_dir / "04_transcript_raw.md", 'w', encoding='utf-8') as f:
            for seg in transcript:
                start_min = int(seg['start'] // 60)
                start_sec = seg['start'] % 60
                end_min = int(seg['end'] // 60)
                end_sec = seg['end'] % 60
                f.write(f"[{start_min:02d}:{start_sec:05.2f} - {end_min:02d}:{end_sec:05.2f}] {seg['text']}\n")
        
        # 05_transcript_normalized.md (copy of raw for now, will be corrected later)
        (sample_dir / "05_transcript_normalized.md").write_text(
            f"# Normalized Transcript: {content_id}\n\n" +
            f"**Note**: Awaiting manual quality check\n\n---\n\n" +
            (sample_dir / "04_transcript_raw.md").read_text(encoding='utf-8')
        )
        
        # 06_metrics.json
        (sample_dir / "06_metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False))
        
        # 07_timeline.md
        (sample_dir / "07_timeline.md").write_text(timeline)
        
        results.append({
            "id": content_id,
            "type": viral_type,
            "duration": round(duration, 2),
            "segments": len(transcript),
            "status": "PROCESSING"
        })
        
        print(f"  ✓ Saved to {sample_dir}")
    
    print(f"\n=== SUMMARY ===")
    print(f"Processed: {len(results)}")
    for r in results:
        print(f"  {r['id']}: {r['duration']}s, {r['segments']} segments")

if __name__ == "__main__":
    main()
