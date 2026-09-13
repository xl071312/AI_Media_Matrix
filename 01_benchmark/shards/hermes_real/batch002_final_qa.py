#!/usr/bin/env python3
"""Batch 002 - Final Admission QA and Status Report"""
import json
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
MEDIA_DIR = BASE / "media" / "batch_002_smoke"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"

# Load registry
reg_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
registry = set()
with open(reg_path, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        cid = row.get('content_id', '').strip().lstrip('\ufeff')
        if cid:
            registry.add(cid)

# Load selection for metadata
sel_path = SHARDS / "douyin_benchmark_selection.csv"
selection_meta = {}
with open(sel_path, 'r', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        raw_cid = row.get('content_id', row.get('aweme_id', '')).strip().lstrip('\ufeff')
        if raw_cid.startswith('DY_REAL_'):
            raw_cid = raw_cid[8:]
        raw_cid = raw_cid.strip()
        if raw_cid:
            selection_meta[raw_cid] = row

# Topic classification
TOPIC_MAP = {
    '赚钱逻辑': ['赚钱', '搞钱', '财富', '收入', '金钱', '资本'],
    '消费陷阱': ['消费', '陷阱', '省钱', '存钱', '负债', '超前'],
    '能力变现': ['变现', '副业', '技能', '个人成长'],
    '信息差': ['信息差', '认知', '思维', '知识', '茧房'],
    '职场': ['职场', '打工', '老板', '工作', '上班'],
    '创业': ['创业', '商业', '生意', '加盟', '开店'],
    '普通人翻身': ['翻身', '普通人', '逆袭'],
    'AI赚钱': ['AI', '人工智能', '豆包'],
    '投资认知': ['投资', '理财', '黄金', '金融', '芒格'],
    '中产焦虑': ['中产', '焦虑', '返贫'],
}
OFF_MARKERS = ['游戏', '攻略', '三角洲', '原神', '动漫', '短剧', '美食', '健身', 
               '宠物', '旅游', '美妆', '穿搭', '数码', '汽车', '音乐', '搞笑', 
               '电影', '明星', '剧情', '明星']

def classify_topic(title, keyword=""):
    text = f"{title} {keyword}".lower()
    for m in OFF_MARKERS:
        if m in text:
            return 'OFF_TOPIC', []
    
    matches = []
    for topic, keywords in TOPIC_MAP.items():
        if any(kw in text for kw in keywords):
            matches.append(topic)
    
    if not matches:
        return 'GENERAL', []
    
    return matches[0], matches[1:]

# Process all audio files
all_audio = sorted([p.stem.replace('.audio', '') for p in MEDIA_DIR.glob('*.m4a') 
                    if not any(x in p.name for x in ['76827', '76828', '76832'])])

print(f"=== BATCH 002 FINAL ADMISSION QA ===")
print(f"Total audio files: {len(all_audio)}")
print()

results = []
qualified_count = 0

for cid in all_audio:
    transcript_path = TRANSCRIPT_DIR / f'{cid}_raw.json'
    audio_path = MEDIA_DIR / f'{cid}.audio.m4a'
    
    # Get metadata
    meta = selection_meta.get(cid, {})
    title = meta.get('desc', '')[:100]
    keyword = meta.get('source_keyword', '')
    
    # Classify topic
    primary_topic, secondary_topics = classify_topic(title, keyword)
    
    # Check NEW_UNIQUE
    new_unique = cid not in registry
    
    # Load transcript
    segments = 0
    chars = 0
    coverage_ratio = 0
    speech_present = False
    audio_duration = 0
    
    if transcript_path.exists():
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = json.load(f)
        
        if isinstance(transcript, list) and len(transcript) > 0:
            segments = len(transcript)
            chars = sum(len(s.get('text', '')) for s in transcript)
            first_start = transcript[0].get('start', 0)
            last_end = transcript[-1].get('end', 0)
            
            # Get audio duration
            try:
                import subprocess
                result = subprocess.run(
                    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                     '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)],
                    capture_output=True, text=True, timeout=10
                )
                audio_duration = float(result.stdout.strip())
                coverage_ratio = (last_end - first_start) / audio_duration if audio_duration > 0 else 0
            except:
                pass
            
            speech_present = chars > 100 and coverage_ratio >= 0.5
    
    # Performance verified
    likes = int(meta.get('liked_count', 0))
    comments = int(meta.get('comment_count', 0))
    favorites = int(meta.get('collected_count', 0))
    shares = int(meta.get('share_count', 0))
    performance_verified = likes > 0 and comments > 0 and favorites > 0 and shares > 0
    
    # Topic final pass
    topic_final_pass = primary_topic not in ['OFF_TOPIC', 'GENERAL']
    
    # Longform check
    longform_status = 'NORMAL'
    if audio_duration > 900:
        longform_status = 'LONGFORM_DEFERRED'
        if primary_topic in ['赚钱逻辑', '创业', '能力变现']:
            longform_status = 'HIGH_VALUE_LONGFORM'
    
    # Corpus eligible
    corpus_eligible = (new_unique and topic_final_pass and 
                       speech_present and segments > 0 and chars > 0)
    
    if corpus_eligible:
        qualified_count += 1
    
    status = 'QUALIFIED' if corpus_eligible else 'EXCLUDED'
    exclusion_reason = '' if corpus_eligible else ('TOPIC_BORDERLINE' if not topic_final_pass else 
                              'NO_SPEECH' if not speech_present else 'OFF_TOPIC')
    
    results.append({
        'content_id': cid,
        'title': title,
        'primary_topic': primary_topic,
        'new_unique': new_unique,
        'topic_final_pass': topic_final_pass,
        'speech_present': speech_present,
        'asr_complete': segments > 0,
        'transcript_usable': segments > 0 and chars > 0,
        'performance_verified': performance_verified,
        'longform_status': longform_status,
        'coverage_ratio': round(coverage_ratio, 2),
        'corpus_eligible': corpus_eligible,
        'exclusion_reason': exclusion_reason,
        'segments': segments,
        'chars': chars,
        'audio_duration': round(audio_duration, 1),
        'status': status
    })
    
    print(f"{'✓' if corpus_eligible else '✗'} {cid}: {primary_topic} ({segments} segs, {chars} chars)")

print(f"\n{'='*60}")
print(f"QUALIFIED: {qualified_count}/{len(results)}")
print(f"Target: 30")
print(f"Status: {'COMPLETE' if qualified_count >= 30 else 'IN_PROGRESS'}")

# Save JSON
output = SHARDS / "batch002_final_qa.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))

# Update CSV
csv_path = SHARDS / "BATCH002_CANONICAL_WORKING.csv"
fieldnames = ['content_id', 'title', 'primary_topic', 'new_unique', 'topic_final_pass',
              'speech_present', 'asr_complete', 'transcript_usable', 'performance_verified',
              'longform_status', 'coverage_ratio', 'corpus_eligible', 'exclusion_reason',
              'segments', 'chars', 'audio_duration', 'status']

with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in results:
        writer.writerow({k: r.get(k, '') for k in fieldnames})

print(f"\nSaved to: {output}")
print(f"CSV updated: {csv_path}")

# Generate final status
status_report = {
    'timestamp': datetime.now().isoformat(),
    'total_audio': len(results),
    'qualified': qualified_count,
    'target': 30,
    'status': 'COMPLETE' if qualified_count >= 30 else 'IN_PROGRESS',
    'by_topic': {}
}

for r in results:
    t = r.get('primary_topic', 'UNKNOWN')
    status_report['by_topic'][t] = status_report['by_topic'].get(t, 0) + 1

status_output = BASE / "analysis_batches" / "batch_002" / "BATCH002_FINAL_STATUS.json"
status_output.parent.mkdir(parents=True, exist_ok=True)
status_output.write_text(json.dumps(status_report, indent=2, ensure_ascii=False))
print(f"Status saved to: {status_output}")