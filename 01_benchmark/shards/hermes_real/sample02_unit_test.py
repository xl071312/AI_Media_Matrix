#!/usr/bin/env python3
"""
Phase 3.1 Sample 02 Method Unit Test
- Re-implement Spoken Unit Builder V2
- Process ONLY Sample 02 (7647797848847439706)
- Generate complete analysis
"""
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
TRANSCRIPT_DIR = BASE / "transcripts_v2"
OUTPUT_DIR = BASE / "qa_sample02_v5"

# Target: ONLY Sample 02
TARGET_ID = "7647797848847439706"

def load_transcript(content_id):
    """Load original transcript"""
    trans_file = TRANSCRIPT_DIR / f"{content_id}_raw.json"
    if not trans_file.exists():
        return None
    with open(trans_file, 'r', encoding='utf-8') as f:
        transcript = json.load(f)
    # Assign segment IDs
    for i, seg in enumerate(transcript):
        seg['segment_id'] = f"S{i+1:04d}"
    return transcript

def build_spoken_units_v2(transcript):
    """
    Re-implement Spoken Unit Builder V2
    
    Rules:
    1. Each ASR segment belongs to exactly one unit
    2. Merge segments into natural speech units
    3. Max unit duration: 15 seconds (REVIEW_REQUIRED), 25 seconds (FAIL)
    4. Split at: punctuation, topic markers, contrast markers
    """
    if not transcript:
        return []
    
    units = []
    current_segments = [transcript[0]]
    current_start = transcript[0]['start']
    
    for i in range(1, len(transcript)):
        seg = transcript[i]
        prev_seg = transcript[i-1]
        
        # Calculate pause
        pause = seg['start'] - prev_seg['end']
        
        # Get texts
        prev_text = prev_seg['text'].rstrip()
        curr_text = seg['text'].lstrip()
        
        # Check if should start new unit
        should_split = False
        
        # Rule 1: ANY punctuation in previous segment
        all_punctuation = ['。', '！', '？', '；', '，', '、', '. ', '! ', '? ', ', ', '...']
        if any(prev_text.endswith(p) for p in all_punctuation):
            should_split = True
        
        # Rule 2: Long pause (> 0.3s)
        if pause > 0.3:
            should_split = True
        
        # Rule 3: Current starts with topic/contrast/new idea marker
        split_markers = [
            '首先', '其次', '第三', '另外', '还有', '接下来', '然后', '最后',
            '所以', '因此', '于是', '接着',
            '但是', '然而', '其实', '不过', '相反', '反而',
            '第一', '第二', '第三', '第四',
            '那么', '这时候', '也就是说', '就是说'
        ]
        if any(curr_text.startswith(m) for m in split_markers):
            should_split = True
        
        # Rule 4: Significant content shift (very short prev + long curr)
        if len(prev_text) < 5 and len(curr_text) > 15:
            should_split = True
        
        # Rule 5: Force split if unit is getting too long (> 10s)
        current_duration = seg['start'] - current_start
        if current_duration > 10:
            should_split = True
        
        if should_split and len(current_segments) > 0:
            # Close current unit
            unit_text = ''.join([s['text'] for s in current_segments])
            unit_duration = current_segments[-1]['end'] - current_start
            
            units.append({
                'unit_id': f"U{len(units)+1:04d}",
                'start': current_start,
                'end': current_segments[-1]['end'],
                'duration': round(unit_duration, 2),
                'source_segment_ids': [s['segment_id'] for s in current_segments],
                'text': unit_text,
                'char_count': len(unit_text)
            })
            
            current_segments = [seg]
            current_start = seg['start']
        else:
            current_segments.append(seg)
    
    # Last unit
    if current_segments:
        unit_text = ''.join([s['text'] for s in current_segments])
        unit_duration = current_segments[-1]['end'] - current_start
        units.append({
            'unit_id': f"U{len(units)+1:04d}",
            'start': current_start,
            'end': current_segments[-1]['end'],
            'duration': round(unit_duration, 2),
            'source_segment_ids': [s['segment_id'] for s in current_segments],
            'text': unit_text,
            'char_count': len(unit_text)
        })
    
    return units

def validate_spoken_units(units, transcript):
    """Validate spoken units"""
    checks = {
        'unit_count': len(units),
        'segment_coverage': 0,
        'max_duration': 0,
        'units_over_15s': 0,
        'units_over_25s': 0,
        'all_segments_covered': False,
        'no_duplicates': True
    }
    
    # Check segment coverage
    all_seg_ids = set(s['segment_id'] for s in transcript)
    covered_seg_ids = set()
    duplicate_found = False
    
    for unit in units:
        seg_ids = set(unit['source_segment_ids'])
        checks['max_duration'] = max(checks['max_duration'], unit['duration'])
        
        if unit['duration'] > 15:
            checks['units_over_15s'] += 1
        if unit['duration'] > 25:
            checks['units_over_25s'] += 1
        
        # Check for duplicates
        overlap = covered_seg_ids & seg_ids
        if overlap:
            duplicate_found = True
        
        covered_seg_ids.update(seg_ids)
    
    checks['segment_coverage'] = len(covered_seg_ids)
    checks['all_segments_covered'] = covered_seg_ids == all_seg_ids
    checks['no_duplicates'] = not duplicate_found
    
    return checks

def detect_questions_enhanced(transcript, units):
    """Enhanced question detection"""
    full_text = ''.join([s['text'] for s in transcript])
    
    questions = []
    
    # Check each unit
    for unit in units:
        text = unit['text']
        
        # Direct question markers at end
        if any(text.rstrip().endswith(m) for m in ['？', '?', '吗', '呢', '么']):
            questions.append({
                'unit_id': unit['unit_id'],
                'text': text[:80],
                'type': 'direct'
            })
            continue
        
        # Question words with question structure
        question_words = ['为什么', '怎么', '怎么办', '凭什么', '难道', '是不是', '有没有', 
                          '什么', '谁', '哪', '多少', '几', '如何', '为何', '究竟']
        
        for qw in question_words:
            if qw in text:
                # Check context
                idx = text.find(qw)
                context = text[max(0, idx-5):min(len(text), idx+30)]
                
                # Skip non-question contexts
                if any(x in context for x in ['告诉你为什么', '我知道怎么', '这就是为什么', 
                                               '因为所以', '原因在于', '目的是']):
                    continue
                
                # Check if it has question-like structure
                if any(m in context for m in ['？', '?', '吗', '呢', '么']):
                    questions.append({
                        'unit_id': unit['unit_id'],
                        'text': context[:80],
                        'type': 'implicit'
                    })
                    break
    
    return questions

def main():
    print("=== PHASE 3.1 SAMPLE 02 METHOD UNIT TEST ===\n")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load transcript
    print(f"Loading transcript for {TARGET_ID}...")
    transcript = load_transcript(TARGET_ID)
    if not transcript:
        print("ERROR: Transcript not found")
        return
    
    print(f"  Segments: {len(transcript)}")
    
    # Build spoken units V2
    print("\nBuilding Spoken Units V2...")
    units = build_spoken_units_v2(transcript)
    print(f"  Units: {len(units)}")
    
    # Validate
    print("\nValidating Spoken Units...")
    validation = validate_spoken_units(units, transcript)
    print(f"  Coverage: {validation['segment_coverage']}/{len(transcript)}")
    print(f"  All covered: {validation['all_segments_covered']}")
    print(f"  No duplicates: {validation['no_duplicates']}")
    print(f"  Max duration: {validation['max_duration']}s")
    print(f"  Units > 15s: {validation['units_over_15s']}")
    print(f"  Units > 25s: {validation['units_over_25s']}")
    
    # Detect questions
    print("\nDetecting Questions...")
    questions = detect_questions_enhanced(transcript, units)
    print(f"  Questions found: {len(questions)}")
    for q in questions[:5]:
        print(f"    {q['unit_id']}: {q['text'][:50]}... ({q['type']})")
    
    # Get video duration
    import subprocess
    VIDEO_DIR = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")
    video_path = VIDEO_DIR / TARGET_ID / "video.mp4"
    
    try:
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
               "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        duration = float(result.stdout.strip())
    except:
        duration = transcript[-1]['end'] if transcript else 0
    
    print(f"\n  Duration: {duration:.1f}s")
    
    # Save files
    print("\nSaving files...")
    
    # 01_source_metadata.json
    meta = {
        "content_id": TARGET_ID,
        "aweme_id": TARGET_ID,
        "url": f"https://www.douyin.com/video/{TARGET_ID}",
        "creator_id": "辉***累",
        "creator_name": "辉***累",
        "title": "普通人如何靠卖货翻身",
        "viral_type": "RELATIVE_BREAKOUT",
        "duration_sec": round(duration, 2),
        "likes": 144012,
        "comments": 16989,
        "favorites": 56538,
        "shares": 26515,
        "capture_time": datetime.now().isoformat(),
        "metadata_source": "MEDIACRAWLER_REAL_CDP",
        "asr_segment_count": len(transcript),
        "spoken_unit_count": len(units),
        "question_count": len(questions)
    }
    (OUTPUT_DIR / "01_source_metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    
    # 02_transcript_raw.json
    (OUTPUT_DIR / "02_transcript_raw.json").write_text(json.dumps(transcript, indent=2, ensure_ascii=False))
    
    # 03_spoken_units.json
    (OUTPUT_DIR / "03_spoken_units.json").write_text(json.dumps(units, indent=2, ensure_ascii=False))
    
    # 04_spoken_unit_validation.json
    (OUTPUT_DIR / "04_spoken_unit_validation.json").write_text(json.dumps(validation, indent=2, ensure_ascii=False))
    
    # 05_transcript_normalized.md
    with open(OUTPUT_DIR / "05_transcript_normalized.md", 'w', encoding='utf-8') as f:
        f.write(f"# Normalized Transcript: {TARGET_ID}\n\n")
        f.write(f"**Note**: Awaiting manual quality check.\n\n---\n\n")
        for seg in transcript:
            start_min = int(seg['start'] // 60)
            start_sec = seg['start'] % 60
            end_min = int(seg['end'] // 60)
            end_sec = seg['end'] % 60
            f.write(f"[{seg['segment_id']}] [{start_min:02d}:{start_sec:05.2f} - {end_min:02d}:{end_sec:05.2f}] {seg['text']}\n")
    
    # 06_questions.json
    (OUTPUT_DIR / "06_questions.json").write_text(json.dumps(questions, indent=2, ensure_ascii=False))
    
    print("\n✓ Files saved to:", OUTPUT_DIR)
    
    # Summary
    print("\n=== SUMMARY ===")
    print(f"ASR Segments: {len(transcript)}")
    print(f"Spoken Units: {len(units)}")
    print(f"Questions: {len(questions)}")
    print(f"Max Unit Duration: {validation['max_duration']}s")
    print(f"Unit Count Valid: {'✓' if len(units) > 1 else '✗ FAIL'}")
    print(f"Coverage Valid: {'✓' if validation['all_segments_covered'] else '✗ FAIL'}")
    print(f"Duration Valid: {'✓' if validation['max_duration'] <= 25 else '✗ FAIL'}")

if __name__ == "__main__":
    main()
