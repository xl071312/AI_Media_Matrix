#!/usr/bin/env python3
"""Batch 002 - Final Admission QA for 12 existing transcripts"""
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

# Topic keywords
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

# Process 12 existing batch002 transcripts
batch002_cids = ['7441108716197301519', '7477191872570477839', '7511664213547519243',
                 '7559914938827803950', '7564348993203948810', '7584407684042165541',
                 '7592567871297932582', '7599188562650734516', '7600369823520073126',
                 '7647446230122356665', '7666798588350065338', '7673172635974421760']

results = []

for cid in batch002_cids:
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
    if transcript_path.exists():
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = json.load(f)
        
        if isinstance(transcript, list) and len(transcript) > 0:
            segments = len(transcript)
            chars = sum(len(s.get('text', '')) for s in transcript)
            first_start = transcript[0].get('start', 0)
            last_end = transcript[-1].get('end', 0)
            
            # Check audio duration
            audio_duration = 0
            if audio_path.exists():
                try:
                    import subprocess
                    result = subprocess.run(
                        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                         '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)],
                        capture_output=True, text=True, timeout=10
                    )
                    audio_duration = float(result.stdout.strip())
                except:
                    pass
            
            # Coverage ratio
            coverage_ratio = (last_end - first_start) / audio_duration if audio_duration > 0 else 0
            
            # Check speech present (chars > 0, reasonable coverage)
            speech_present = chars > 100 and coverage_ratio >= 0.5
            
            # Check topic borderline
            topic_final_pass = primary_topic not in ['OFF_TOPIC', 'GENERAL']
            
            # Longform check
            longform_status = 'NORMAL'
            if audio_duration > 900:  # 15 minutes
                longform_status = 'LONGFORM_DEFERRED'
                # Check if it's high value
                if primary_topic in ['赚钱逻辑', '创业', '能力变现']:
                    longform_status = 'HIGH_VALUE_LONGFORM'
            
            # Performance verified
            likes = int(meta.get('liked_count', 0))
            comments = int(meta.get('comment_count', 0))
            favorites = int(meta.get('collected_count', 0))
            shares = int(meta.get('share_count', 0))
            performance_verified = likes > 0 and comments > 0 and favorites > 0 and shares > 0
            
            # Corpus eligible
            corpus_eligible = (new_unique and topic_final_pass and 
                             speech_present and segments > 0 and chars > 0)
            
            results.append({
                'content_id': cid,
                'title': title,
                'primary_topic': primary_topic,
                'secondary_topics': secondary_topics,
                'new_unique': new_unique,
                'topic_final_pass': topic_final_pass,
                'speech_present': speech_present,
                'asr_complete': True,
                'transcript_usable': segments > 0 and chars > 0,
                'performance_verified': performance_verified,
                'longform_status': longform_status,
                'coverage_ratio': round(coverage_ratio, 2),
                'corpus_eligible': corpus_eligible,
                'exclusion_reason': '' if corpus_eligible else 'TOPIC_BORDERLINE' if not topic_final_pass else 'OFF_TOPIC',
                'segments': segments,
                'chars': chars,
                'audio_duration': audio_duration,
                'status': 'QUALIFIED' if corpus_eligible else 'EXCLUDED'
            })
        else:
            results.append({
                'content_id': cid,
                'status': 'EMPTY_TRANSCRIPT'
            })
    else:
        results.append({
            'content_id': cid,
            'status': 'NO_TRANSCRIPT'
        })

# Save results
output = SHARDS / "batch002_admission_qa.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))

# Summary
qualified = len([r for r in results if r.get('status') == 'QUALIFIED'])
excluded = len([r for r in results if r.get('status') == 'EXCLUDED'])
print(f"=== BATCH002 ADMISSION QA ===")
print(f"Total: {len(results)}")
print(f"Qualified: {qualified}")
print(f"Excluded: {excluded}")
print()

for r in results:
    if r.get('status') == 'QUALIFIED':
        print(f"✓ {r['content_id']}: {r['primary_topic']} ({r['segments']} segs, {r['chars']} chars)")
    else:
        print(f"✗ {r['content_id']}: {r.get('status', 'UNKNOWN')} - {r.get('exclusion_reason', '')}")

print(f"\nSaved to: {output}")

# Save CSV
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

print(f"Saved CSV to: {csv_path}")