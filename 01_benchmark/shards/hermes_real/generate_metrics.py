#!/usr/bin/env python3
"""Generate metrics from real transcripts"""
import json
import re
from pathlib import Path
import statistics

BASE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
TRANSCRIPT_DIR = BASE / "transcripts"
VIDEO_DIR = Path(r"C:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler\data\douyin\videos")

def calculate_metrics(content_id, transcript_file):
    """Calculate language metrics from transcript"""
    with open(transcript_file, 'r', encoding='utf-8') as f:
        segments = json.load(f)
    
    # Combine all text
    full_text = ' '.join([s['text'] for s in segments])
    
    # Basic metrics
    total_chars = len(full_text)
    duration_sec = segments[-1]['end'] if segments else 0
    chars_per_sec = total_chars / max(duration_sec, 1)
    
    # Sentence metrics
    sentences = re.split(r'[。！？；]', full_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = len(sentences)
    avg_sentence_chars = total_chars / max(sentence_count, 1)
    sentence_lengths = [len(s) for s in sentences]
    median_sentence_chars = statistics.median(sentence_lengths) if sentence_lengths else 0
    
    # Ratio metrics
    short_sentences = [s for s in sentences if len(s) <= 10]
    long_sentences = [s for s in sentences if len(s) > 30]
    short_sentence_ratio = len(short_sentences) / max(sentence_count, 1)
    long_sentence_ratio = len(long_sentences) / max(sentence_count, 1)
    
    # Question metrics
    question_count = full_text.count('？') + full_text.count('?')
    question_rate = question_count / max(sentence_count, 1)
    
    # Person metrics
    first_person = len(re.findall(r'[我咱俺]', full_text))
    second_person = len(re.findall(r'[你您]', full_text))
    
    # Transition and contrast markers
    transitions = ['但是', '所以', '其实', '然而', '不过', '因此', '于是']
    contrasts = ['不是', '而是', '相反', '反而', '却']
    examples = ['比如', '例如', '像', '就像', '比如说']
    
    transition_count = sum(full_text.count(t) for t in transitions)
    contrast_count = sum(full_text.count(c) for c in contrasts)
    example_count = sum(full_text.count(e) for e in examples)
    
    # Numbers
    number_count = len(re.findall(r'\d+', full_text))
    
    # Spoken fillers
    fillers = ['嗯', '啊', '那个', '就是', '然后', '就是说', '对吧']
    filler_count = sum(full_text.count(f) for f in fillers)
    
    # Repetition detection
    words = full_text.split()
    repetition_count = 0
    for i in range(len(words) - 1):
        if words[i] == words[i+1]:
            repetition_count += 1
    
    # Hook extraction (first few seconds)
    hook_3s = ''.join([s['text'] for s in segments if s['end'] <= 3])
    hook_5s = ''.join([s['text'] for s in segments if s['end'] <= 5])
    hook_15s = ''.join([s['text'] for s in segments if s['end'] <= 15])
    
    metrics = {
        "content_id": content_id,
        "duration_sec": round(duration_sec, 2),
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
        "contrast_marker_count": contrast_count,
        "example_marker_count": example_count,
        "number_count": number_count,
        "spoken_filler_count": filler_count,
        "repetition_count": repetition_count,
        "hook_chars_3s": hook_3s[:50],
        "hook_chars_5s": hook_5s[:80],
        "hook_chars_15s": hook_15s[:200]
    }
    
    return metrics

def main():
    print("=== GENERATING METRICS ===\n")
    
    # Find processed transcripts
    json_files = list(TRANSCRIPT_DIR.glob("*_raw.json"))
    print(f"Found {len(json_files)} transcripts\n")
    
    results = []
    for json_file in json_files:
        content_id = json_file.stem.replace('_raw', '')
        
        # Skip placeholder files
        if content_id.startswith('DY_REAL_'):
            continue
        
        print(f"Processing {content_id}...")
        
        # Calculate metrics
        metrics = calculate_metrics(content_id, json_file)
        
        # Save
        metrics_file = BASE / "analysis" / f"{content_id}_metrics.json"
        metrics_file.parent.mkdir(parents=True, exist_ok=True)
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)
        
        results.append({
            "content_id": content_id,
            "status": "PASS",
            "duration_sec": metrics['duration_sec'],
            "total_chars": metrics['total_chars'],
            "sentence_count": metrics['sentence_count']
        })
        
        print(f"  ✓ Duration: {metrics['duration_sec']}s, Chars: {metrics['total_chars']}, Sentences: {metrics['sentence_count']}")
    
    print(f"\n=== SUMMARY ===")
    print(f"Metrics generated: {len(results)}")
    
    # Save summary
    with open(BASE / "metrics_results.json", 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
