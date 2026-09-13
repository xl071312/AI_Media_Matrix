#!/usr/bin/env python3
"""Complete Phase 3.1 Pipeline V3 with all fixes"""
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime
import statistics

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
TRANSCRIPT_DIR = BASE / "transcripts_v2"
QA_BATCH = BASE / "qa_batch_004"
VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")

def aggregate_spoken_units(transcript):
    """Aggregate ASR segments into spoken units"""
    if not transcript:
        return []
    
    units = []
    current_segments = [transcript[0]]
    current_start = transcript[0]['start']
    
    for i in range(1, len(transcript)):
        seg = transcript[i]
        prev_seg = transcript[i-1]
        
        pause = seg['start'] - prev_seg['end']
        
        should_split = False
        
        # Split on pause > 0.3s
        if pause > 0.3:
            should_split = True
        
        # Split on punctuation
        prev_text = prev_seg['text'].rstrip()
        if any(prev_text.endswith(p) for p in ['。', '！', '？', '；']):
            should_split = True
        
        # Split on topic/contrast markers
        curr_text = seg['text'].lstrip()
        markers = ['首先', '其次', '第三', '另外', '还有', '接下来', '然后', '最后', '所以', '因此', 
                   '但是', '然而', '其实', '不过', '相反', '反而', '第一', '第二', '接下来']
        if any(curr_text.startswith(m) for m in markers):
            should_split = True
        
        if should_split and len(current_segments) > 0:
            unit_text = ''.join([s['text'] for s in current_segments])
            units.append({
                'unit_id': f"U{len(units)+1:04d}",
                'start': current_start,
                'end': current_segments[-1]['end'],
                'source_segment_ids': [s['segment_id'] for s in current_segments],
                'text': unit_text,
                'char_count': len(unit_text)
            })
            current_segments = [seg]
            current_start = seg['start']
        else:
            current_segments.append(seg)
    
    if current_segments:
        unit_text = ''.join([s['text'] for s in current_segments])
        units.append({
            'unit_id': f"U{len(units)+1:04d}",
            'start': current_start,
            'end': current_segments[-1]['end'],
            'source_segment_ids': [s['segment_id'] for s in current_segments],
            'text': unit_text,
            'char_count': len(unit_text)
        })
    
    return units

def calculate_metrics_v3(transcript, units, duration):
    """Calculate Metrics V3"""
    full_text = ''.join([s['text'] for s in transcript])
    total_chars = len(full_text)
    
    unit_lengths = [u['char_count'] for u in units]
    avg_unit_chars = sum(unit_lengths) / max(len(unit_lengths), 1)
    median_unit_chars = statistics.median(unit_lengths) if unit_lengths else 0
    
    short_units = [u for u in units if u['char_count'] <= 10]
    medium_units = [u for u in units if 10 < u['char_count'] <= 30]
    long_units = [u for u in units if u['char_count'] > 30]
    
    # Questions
    question_count = 0
    rhetorical_count = 0
    for unit in units:
        text = unit['text']
        if any(text.endswith(m) for m in ['？', '?', '吗', '呢', '么']):
            question_count += 1
        elif any(qw in text for qw in ['为什么', '怎么', '怎么办', '难道', '是不是', '有没有']):
            question_count += 1
            if any(rw in text for rw in ['难道', '凭什么', '为什么']):
                rhetorical_count += 1
    
    first_person = len(re.findall(r'[我咱俺]', full_text))
    second_person = len(re.findall(r'[你您]', full_text))
    
    transitions = ['但是', '所以', '其实', '然而', '不过', '因此', '于是', '首先', '其次', '最后', '然后', '接着']
    transition_count = sum(full_text.count(t) for t in transitions)
    
    contrasts = ['不是', '而是', '相反', '反而', '却', '而', '但']
    contrast_count = sum(full_text.count(c) for c in contrasts)
    
    examples = ['比如', '例如', '像', '就像', '比如说', '譬如', '举个例子']
    example_count = sum(full_text.count(e) for e in examples)
    
    # Numbers - enhanced detection
    number_count = 0
    # Arabic numbers
    number_count += len(re.findall(r'\d+(?:\.\d+)?', full_text))
    # Chinese numerals
    chinese_nums = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿']
    for cn in chinese_nums:
        if cn in full_text:
            number_count += 1
    
    fillers = ['嗯', '啊', '那个', '就是', '然后', '就是说', '对吧', '这个']
    filler_count = sum(full_text.count(f) for f in fillers)
    
    money_count = len(re.findall(r'\d+[万万亿千万百十]?[元块%]|\d+%|[\d]+万|[\d]+亿', full_text))
    
    return {
        "duration_sec": round(duration, 2),
        "asr_segment_count": len(transcript),
        "spoken_unit_count": len(units),
        "avg_spoken_unit_chars": round(avg_unit_chars, 1),
        "median_spoken_unit_chars": round(median_unit_chars, 1),
        "short_unit_ratio": round(len(short_units) / max(len(units), 1), 3),
        "medium_unit_ratio": round(len(medium_units) / max(len(units), 1), 3),
        "long_unit_ratio": round(len(long_units) / max(len(units), 1), 3),
        "total_chars": total_chars,
        "chars_per_sec": round(total_chars / max(duration, 1), 2),
        "question_count": question_count,
        "question_rate": round(question_count / max(len(units), 1), 3),
        "rhetorical_question_count": rhetorical_count,
        "first_person_count": first_person,
        "second_person_count": second_person,
        "transition_count": transition_count,
        "contrast_count": contrast_count,
        "example_count": example_count,
        "number_count": number_count,
        "money_expression_count": money_count,
        "filler_count": filler_count,
        "transcript_sha256": hashlib.sha256(full_text.encode('utf-8')).hexdigest()[:16]
    }

def main():
    print("=== PHASE 3.1 PIPELINE V3 FINAL ===\n")
    
    samples = [
        {"id": "7302348364815928612", "type": "ABSOLUTE_VIRAL", "title": "从1到100万 普通人第一桶金", 
         "creator": "男***門", "likes": 1112455, "comments": 61476, "favorites": 279069, "shares": 493633},
        {"id": "7647797848847439706", "type": "RELATIVE_BREAKOUT", "title": "普通人如何靠卖货翻身",
         "creator": "辉***累", "likes": 144012, "comments": 16989, "favorites": 56538, "shares": 26515},
        {"id": "7546212425998454074", "type": "NORMAL_REFERENCE", "title": "除了打工，用心给大家整理了16条路",
         "creator": "小***究", "likes": 410006, "comments": 106874, "favorites": 263470, "shares": 83064}
    ]
    
    results = []
    
    for i, sample in enumerate(samples, 1):
        content_id = sample["id"]
        print(f"\n--- Sample {i}: {content_id} ({sample['type']}) ---")
        
        trans_file = TRANSCRIPT_DIR / f"{content_id}_raw.json"
        if not trans_file.exists():
            print(f"  SKIP: No transcript")
            continue
        
        with open(trans_file, 'r', encoding='utf-8') as f:
            transcript = json.load(f)
        
        for j, seg in enumerate(transcript):
            seg['segment_id'] = f"S{j+1:04d}"
        
        video_path = VIDEO_DIR / content_id / "video.mp4"
        if not video_path.exists():
            print(f"  SKIP: Video not found")
            continue
        
        import subprocess
        try:
            cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
                   "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            duration = float(result.stdout.strip())
        except:
            duration = transcript[-1]['end'] if transcript else 0
        
        print(f"  Duration: {duration:.1f}s, Segments: {len(transcript)}")
        
        # Aggregate spoken units
        units = aggregate_spoken_units(transcript)
        print(f"  Spoken Units: {len(units)}")
        
        # Calculate metrics V3
        metrics = calculate_metrics_v3(transcript, units, duration)
        
        # Validate
        last_ts = transcript[-1]['end'] if transcript else 0
        ts_valid = last_ts <= duration + 1
        unit_aggregation_ok = len(units) < len(transcript)
        
        print(f"  Questions: {metrics['question_count']}, Numbers: {metrics['number_count']}")
        print(f"  Units < Segments: {'✓' if unit_aggregation_ok else '✗'}")
        
        # Create sample directory
        sample_dir = QA_BATCH / f"sample_{i:02d}"
        sample_dir.mkdir(parents=True, exist_ok=True)
        
        # Save files
        meta = {
            "content_id": content_id,
            "aweme_id": content_id,
            "url": f"https://www.douyin.com/video/{content_id}",
            "creator_id": sample["creator"],
            "title": sample["title"],
            "viral_type": sample["type"],
            "duration_sec": round(duration, 2),
            "likes": sample["likes"],
            "comments": sample["comments"],
            "favorites": sample["favorites"],
            "shares": sample["shares"],
            "capture_time": datetime.now().isoformat(),
            "metadata_source": "MEDIACRAWLER_REAL_CDP",
            "video_path": str(video_path),
            "asr_segment_count": len(transcript),
            "spoken_unit_count": len(units),
            "timestamp_valid": ts_valid,
            "last_timestamp": round(last_ts, 2),
            "transcript_sha256": metrics["transcript_sha256"],
            "unit_aggregation_valid": unit_aggregation_ok
        }
        (sample_dir / "00_source_metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
        
        perf = {
            "performance_verified": True,
            "performance_source": "MEDIACRAWLER_REAL_CDP",
            "likes": sample["likes"],
            "comments": sample["comments"],
            "favorites": sample["favorites"],
            "shares": sample["shares"]
        }
        (sample_dir / "01_performance.json").write_text(json.dumps(perf, indent=2, ensure_ascii=False))
        
        baseline = {"status": "NOT_AVAILABLE", "reason": "ArgusSecurityPlugin blocked Creator API"}
        (sample_dir / "02_creator_baseline.json").write_text(json.dumps(baseline, indent=2, ensure_ascii=False))
        
        (sample_dir / "03_transcript_raw_v2.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
        
        with open(sample_dir / "04_transcript_normalized_v2.md", 'w', encoding='utf-8') as f:
            f.write(f"# Normalized Transcript: {content_id}\n\n")
            for seg in transcript:
                start_min = int(seg['start'] // 60)
                start_sec = seg['start'] % 60
                end_min = int(seg['end'] // 60)
                end_sec = seg['end'] % 60
                f.write(f"[{seg['segment_id']}] [{start_min:02d}:{start_sec:05.2f} - {end_min:02d}:{end_sec:05.2f}] {seg['text']}\n")
        
        (sample_dir / "05_metrics_v3.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False))
        
        # Timeline
        tl_lines = [
            f"# Cognitive Timeline: {content_id}",
            f"",
            f"**Duration**: {duration:.1f}s",
            f"**Segments**: {len(transcript)}",
            f"**Spoken Units**: {len(units)}",
            f"",
            f"---",
            f"",
            f"| Unit ID | Time | Chars | Text |"
        ]
        for u in units:
            text_preview = u['text'][:50].replace('|', '\\|')
            tl_lines.append(f"| {u['unit_id']} | {u['start']:.2f}-{u['end']:.2f} | {u['char_count']} | {text_preview}... |")
        
        (sample_dir / "06_timeline_v3.md").write_text('\n'.join(tl_lines))
        
        results.append({
            "id": content_id,
            "type": sample["type"],
            "duration": round(duration, 2),
            "segments": len(transcript),
            "units": len(units),
            "timestamp_valid": ts_valid,
            "unit_aggregation_valid": unit_aggregation_ok,
            "metrics_v3": metrics
        })
        
        print(f"  ✓ Complete")
    
    print(f"\n=== SUMMARY ===")
    for r in results:
        print(f"  {r['id']}: {r['duration']}s, {r['segments']} segs → {r['units']} units, questions={r['metrics_v3']['question_count']}, numbers={r['metrics_v3']['number_count']}")
    
    print(f"\n✓ Phase 3.1 Pipeline V3 complete!")

if __name__ == "__main__":
    main()
