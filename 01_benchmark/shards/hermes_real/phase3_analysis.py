#!/usr/bin/env python3
"""
Phase 3 Step 3: Generate Metrics + Deep Analysis Templates
"""
import json
import csv
import re
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
DEEP_BATCH_FILE = BASE_DIR / "deep_analysis_batch_001.csv"
TRANS_DIR = BASE_DIR / "transcripts"
ANALYSIS_DIR = BASE_DIR / "analysis"
CREATOR_PANEL_DIR = BASE_DIR / "creator_panels"
TOPIC_COMP_DIR = BASE_DIR / "topic_comparisons"

# Create dirs
for d in [ANALYSIS_DIR, CREATOR_PANEL_DIR, TOPIC_COMP_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def load_deep_batch():
    records = []
    with open(DEEP_BATCH_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.lstrip('\ufeff'): v for k, v in row.items()}
            records.append(clean_row)
    return records

def generate_metrics(content_id, transcript_file):
    """Generate analysis metrics from transcript"""
    metrics = {
        "content_id": content_id,
        "generated_at": datetime.now().isoformat(),
        "duration_sec": 0,
        "total_chars": 0,
        "chars_per_sec": 0,
        "sentence_count": 0,
        "avg_sentence_chars": 0,
        "median_sentence_chars": 0,
        "short_sentence_ratio": 0,
        "long_sentence_ratio": 0,
        "question_count": 0,
        "question_rate": 0,
        "first_person_count": 0,
        "second_person_count": 0,
        "transition_count": 0,
        "contrast_marker_count": 0,
        "example_marker_count": 0,
        "number_count": 0,
        "spoken_filler_count": 0,
        "repetition_count": 0,
        "hook_chars_3s": "",
        "hook_chars_5s": "",
        "hook_chars_15s": ""
    }
    
    # Try to read transcript if exists
    transcript_path = TRANS_DIR / f"{content_id}_raw.md"
    if transcript_path.exists():
        with open(transcript_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Calculate metrics
        text_only = re.sub(r'[#\[\]-]', ' ', content)
        chars = len(text_only)
        sentences = re.split(r'[。！？；]', text_only)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        metric_dict = {
            "total_chars": chars,
            "sentence_count": len(sentences),
            "avg_sentence_chars": round(chars / max(len(sentences), 1), 1),
            "question_count": content.count('？') + content.count('?'),
            "first_person_count": len(re.findall(r'[我咱俺]', content)),
            "second_person_count": len(re.findall(r'[你您你]', content)),
            "transition_count": len([k for k in ['但是', '所以', '其实', '然而', '不过'] if k in content]),
            "contrast_marker_count": len([k for k in ['不是', '而是', '相反', '反而'] if k in content]),
            "example_marker_count": len([k for k in ['比如', '例如', '像', '就像'] if k in content]),
            "number_count": len(re.findall(r'\d+', content)),
            "spoken_filler_count": len([k for k in ['嗯', '啊', '那个', '就是', '然后'] if k in content])
        }
        
        metrics.update(metric_dict)
        if metrics['total_chars'] > 0 and metrics.get('duration_sec', 0) > 0:
            metrics['chars_per_sec'] = round(metrics['total_chars'] / metrics['duration_sec'], 2)
        
        # Hook extraction (placeholder)
        lines = content.split('\n')
        for line in lines[:10]:
            if line.strip() and not line.startswith('#'):
                metrics['hook_chars_3s'] = line[:30]
                metrics['hook_chars_5s'] = line[:50]
                break
    
    return metrics

def generate_deep_analysis_template(content_id, record):
    """Generate deep analysis markdown template"""
    
    analysis = f"""# Deep Analysis: {content_id}

**Generated**: {datetime.now().isoformat()}
**Source**: {record.get('source_keyword', 'Unknown')}
**URL**: {record.get('url', '')}

---

## A. Performance

| Metric | Value |
|--------|-------|
| Likes | {record.get('liked_count', '')} |
| Comments | {record.get('comment_count', '')} |
| Favorites | {record.get('collected_count', '')} |
| Shares | {record.get('share_count', '')} |
| Performance Score | {record.get('performance_score', '')} |
| Guanyu Fit | {record.get('guanyu_fit_score', '')} |

### Creator Baseline
- Median Likes: NULL (pending baseline collection)
- Relative Like Ratio: NULL

---

## B. Content Type

| Field | Value |
|-------|-------|
| Style | {record.get('content_style', 'UNKNOWN')} |
| Viral Types | {record.get('viral_type', '')} |
| Topic Cluster | {record.get('source_keyword', '')} |

---

## C. Hook Analysis

### First 1 Second
- Text: [Placeholder - needs transcript]
- Visual: [Placeholder]

### First 3 Seconds
- Text: [Placeholder]
- Technique: [Placeholder]

### First 5 Seconds
- Text: [Placeholder]
- Cognitive Hook: [Placeholder]

### First 15 Seconds
- Summary: [Placeholder]
- Key Arguments: [Placeholder]

---

## D. Core Conflict

**Audience Original Cognition**: [To be filled]
**Video Challenge**: [To be filled]

---

## E. Logic Map

```
[Structure to be mapped from transcript]
Step 1 → Step 2 → Step 3 → Conclusion
```

---

## F. Evidence Types

- Cases: [Count]
- Numbers: [Count]
- Stories: [Count]
- Analogies: [Count]

---

## G. Spoken Style

- Avg Sentence Length: [chars]
- Question Rate: [%]
- First Person Rate: [%]
- Transition Words: [Count]
- Filler Words: [Count]

---

## H. Attention Mechanism

- When reset: [Timestamps]
- How: [Technique]

---

## I. Cognitive Gain

1. First insight: [Time, Text]
2. Second insight: [Time, Text]
3. Biggest counter-intuition: [Text]

---

## J. Ending & CTA

- Ending type: [Placeholder]
- CTA: [Placeholder]
- Loop back: [Yes/No]

---

## K. Why It Performed

### FACTS (Verified)
- [List verified facts]

### INFERENCE (Likely)
- [List reasonable inferences]

### HYPOTHESIS (Speculative)
- [List hypotheses to test]

---

## L. Reusable Mechanisms

1. [Mechanism 1]
2. [Mechanism 2]
3. [Mechanism 3]

---

*Analysis template generated. Fill in details after transcript review.*
"""
    
    return analysis

def main():
    print("=== PHASE 3: METRICS + DEEP ANALYSIS ===\n")
    
    batch = load_deep_batch()
    print(f"Processing {len(batch)} videos\n")
    
    metrics_count = 0
    analysis_count = 0
    
    for i, record in enumerate(batch, 1):
        content_id = record.get('content_id', '')
        
        print(f"[{i}/{len(batch)}] Generating for {content_id}...")
        
        # Generate metrics
        metrics = generate_metrics(content_id, TRANS_DIR / f"{content_id}_raw.md")
        metrics_file = ANALYSIS_DIR / f"{content_id}_metrics.json"
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)
        metrics_count += 1
        
        # Generate deep analysis template
        analysis = generate_deep_analysis_template(content_id, record)
        analysis_file = ANALYSIS_DIR / f"{content_id}.md"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            f.write(analysis)
        analysis_count += 1
        
        # Rate limit
        import time
        time.sleep(0.5)
    
    print(f"\n=== RESULTS ===")
    print(f"Metrics generated: {metrics_count}/{len(batch)}")
    print(f"Deep analysis templates: {analysis_count}/{len(batch)}")
    
    # Save progress
    progress = {
        "phase": "PHASE_3_IN_PROGRESS",
        "metrics_done": metrics_count,
        "analysis_done": analysis_count,
        "total_target": len(batch),
        "timestamp": datetime.now().isoformat()
    }
    
    with open(BASE_DIR / "phase3_progress.json", 'w') as f:
        json.dump(progress, f, indent=2)
    
    print(f"\nProgress saved to: {BASE_DIR / 'phase3_progress.json'}")

if __name__ == "__main__":
    main()
