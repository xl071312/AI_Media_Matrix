#!/usr/bin/env python3
"""Batch 002 Production - Full Pipeline: Download + ASR + QA"""
import csv
import json
import subprocess
import hashlib
import time
import random
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH2_DIR = BASE / "analysis_batches" / "batch_002"
MEDIA_DIR = BASE / "media" / "batch_002_smoke"
TRANSCRIPT_DIR = BASE / "shards" / "hermes_real" / "transcripts_v2"

BATCH2_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

# Load registry
reg_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
registry = set()
with open(reg_path, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        cid = row.get('content_id', '').strip().lstrip('\ufeff')
        if cid:
            registry.add(cid)

# Load selection
sel_path = SHARDS / "douyin_benchmark_selection.csv"
candidates = []
with open(sel_path, 'r', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        raw_cid = row.get('content_id', row.get('aweme_id', '')).strip().lstrip('\ufeff')
        if raw_cid.startswith('DY_REAL_'):
            raw_cid = raw_cid[8:]
        raw_cid = raw_cid.strip()
        if raw_cid in registry:
            continue
        candidates.append({
            'cid': raw_cid,
            'title': row.get('desc', '')[:100],
            'keyword': row.get('source_keyword', ''),
            'perf_score': float(row.get('performance_score', 0)),
            'likes': int(row.get('liked_count', 0)),
            'comments': int(row.get('comment_count', 0)),
            'favorites': int(row.get('collected_count', 0)),
            'shares': int(row.get('share_count', 0))
        })

print(f"Total candidates: {len(candidates)}")

# Topic classification with primary_topic field
TOPIC_MAP = [
    ('消费陷阱', ['消费', '陷阱', '省钱', '存钱', '负债', '超前']),
    ('赚钱逻辑', ['赚钱', '搞钱', '财富', '收入', '金钱']),
    ('能力变现', ['变现', '副业', '技能', '个人成长']),
    ('信息差', ['信息差', '认知', '思维', '知识', '茧房']),
    ('职场', ['职场', '打工', '老板', '工作', '上班']),
    ('创业', ['创业', '商业', '生意', '加盟', '开店']),
    ('普通人翻身', ['翻身', '普通人', '逆袭']),
    ('AI赚钱', ['AI', '人工智能', '豆包']),
    ('投资认知', ['投资', '理财', '黄金', '金融', '芒格']),
    ('中产焦虑', ['中产', '焦虑', '返贫']),
]
OFF_MARKERS = ['游戏', '攻略', '三角洲', '原神', '动漫', '短剧', '美食', '健身', 
               '宠物', '旅游', '美妆', '穿搭', '数码', '汽车', '音乐', '搞笑', 
               '电影', '明星', '剧情', '明星']

def classify_topic(title, keyword=""):
    text = f"{title} {keyword}".lower()
    for m in OFF_MARKERS:
        if m in text:
            return 'OFF_TOPIC', []
    
    matches = []
    for topic, keywords in TOPIC_MAP:
        if any(kw in text for kw in keywords):
            matches.append(topic)
    
    if not matches:
        return 'GENERAL', []
    
    return matches[0], matches[1:]

# Filter ON_TOPIC with primary topic
on_topic = []
for c in candidates:
    primary, secondary = classify_topic(c['title'], c['keyword'])
    if primary != 'OFF_TOPIC':
        on_topic.append({**c, 'primary_topic': primary, 'secondary_topics': secondary})

print(f"ON_TOPIC candidates: {len(on_topic)}")

# Sort by performance score
on_topic.sort(key=lambda x: x['perf_score'], reverse=True)

# Save candidate list
output_path = SHARDS / "batch002_candidates_final.json"
output_path.write_text(json.dumps(on_topic[:50], indent=2, ensure_ascii=False))
print(f"Saved top 50 candidates to: {output_path}")

# Show distribution
topic_counts = {}
for c in on_topic:
    t = c['primary_topic']
    topic_counts[t] = topic_counts.get(t, 0) + 1

print("\nTopic Distribution:")
for t, c in sorted(topic_counts.items(), key=lambda x: -x[1]):
    print(f"  {t}: {c}")

print("\nTop 30 Queue:")
for i, c in enumerate(on_topic[:30], 1):
    print(f"{i}. {c['cid']} | {c['primary_topic']} | perf={c['perf_score']:.1f}")
    print(f"   {c['title'][:50]}")