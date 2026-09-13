#!/usr/bin/env python3
"""Global Registry Audit and Comparison Dataset Builder - Fixed"""
import csv
import json
from pathlib import Path
from collections import defaultdict

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"

# Load registry
reg_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
registry = {}
with open(reg_path, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        cid = row.get('content_id', '').strip().lstrip('\ufeff')
        if cid:
            registry[cid] = row

print(f"=== GLOBAL REGISTRY AUDIT ===")
print(f"Total entries: {len(registry)}")

# Count by batch
batch_cids = defaultdict(set)
for cid, row in registry.items():
    all_batches = row.get('all_batches') or ''
    if 'batch_001' in all_batches:
        batch_cids['batch_001'].add(cid)
    if 'batch_002' in all_batches:
        batch_cids['batch_002'].add(cid)
    if 'batch_003' in all_batches:
        batch_cids['batch_003'].add(cid)

print(f"\nBatch001 unique: {len(batch_cids['batch_001'])}")
print(f"Batch002 unique: {len(batch_cids['batch_002'])}")
print(f"Batch003 unique: {len(batch_cids['batch_003'])}")
print(f"Global unique union: {len(registry)}")

# Load Batch 002 qualified
b002_path = SHARDS / "batch002_final_qa.json"
b002_qualified = []
if b002_path.exists():
    with open(b002_path, 'r', encoding='utf-8') as f:
        b002_data = json.load(f)
    b002_qualified = [r for r in b002_data if r.get('corpus_eligible')]
    print(f"\nBatch002 qualified: {len(b002_qualified)}")

# Load Batch 003 progress
b003_path = SHARDS / "batch003_progress.json"
b003_done = []
if b003_path.exists():
    with open(b003_path, 'r', encoding='utf-8') as f:
        b003_data = json.load(f)
    b003_done = [r for r in b003_data if r.get('status') == 'DONE']
    print(f"Batch003 done: {len(b003_done)}")

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
            return 'OFF_TOPIC'
    matches = []
    for topic, keywords in TOPIC_MAP.items():
        if any(kw in text for kw in keywords):
            matches.append(topic)
    return matches[0] if matches else 'GENERAL'

# Build global comparison dataset
print("\n=== BUILDING GLOBAL_COMPARISON_FEATURES.csv ===")

global_features = []

# Process Batch 002
for r in b002_qualified:
    cid = r['content_id']
    meta = selection_meta.get(cid, {})
    title = meta.get('desc', '')[:100]
    keyword = meta.get('source_keyword', '')
    primary_topic = r.get('primary_topic', classify_topic(title, keyword))
    
    likes = int(meta.get('liked_count', 0))
    comments = int(meta.get('comment_count', 0))
    favorites = int(meta.get('collected_count', 0))
    shares = int(meta.get('share_count', 0))
    
    # Compute ratios
    comment_like_ratio = comments / likes if likes > 0 else 0
    favorite_like_ratio = favorites / likes if likes > 0 else 0
    share_like_ratio = shares / likes if likes > 0 else 0
    
    global_features.append({
        'content_id': cid,
        'batch': 'batch_002',
        'title': title,
        'author': meta.get('author', ''),
        'creator_id': meta.get('author_id', ''),
        'primary_topic': primary_topic,
        'duration_sec': r.get('audio_duration', 0),
        'segment_count': r.get('segments', 0),
        'transcript_chars': r.get('chars', 0),
        'chars_per_sec': r.get('chars', 0) / r.get('audio_duration', 1) if r.get('audio_duration', 0) > 0 else 0,
        'likes': likes,
        'comments': comments,
        'favorites': favorites,
        'shares': shares,
        'comment_like_ratio': round(comment_like_ratio, 4),
        'favorite_like_ratio': round(favorite_like_ratio, 4),
        'share_like_ratio': round(share_like_ratio, 4),
        'creator_baseline_n': 0,
        'creator_median_likes': 0,
        'relative_like_ratio': 0,
        'performance_verified': r.get('performance_verified', False),
        'transcript_usable': r.get('transcript_usable', False),
        'simulated': 'FALSE'
    })

# Process Batch 003
for r in b003_done:
    cid = r['cid']
    meta = selection_meta.get(cid, {})
    title = meta.get('desc', '')[:100]
    keyword = meta.get('source_keyword', '')
    primary_topic = classify_topic(title, keyword)
    
    likes = int(meta.get('liked_count', 0))
    comments = int(meta.get('comment_count', 0))
    favorites = int(meta.get('collected_count', 0))
    shares = int(meta.get('share_count', 0))
    
    comment_like_ratio = comments / likes if likes > 0 else 0
    favorite_like_ratio = favorites / likes if likes > 0 else 0
    share_like_ratio = shares / likes if likes > 0 else 0
    
    global_features.append({
        'content_id': cid,
        'batch': 'batch_003',
        'title': title,
        'author': meta.get('author', ''),
        'creator_id': meta.get('author_id', ''),
        'primary_topic': primary_topic,
        'duration_sec': 0,
        'segment_count': r.get('segments', 0),
        'transcript_chars': r.get('chars', 0),
        'chars_per_sec': 0,
        'likes': likes,
        'comments': comments,
        'favorites': favorites,
        'shares': shares,
        'comment_like_ratio': round(comment_like_ratio, 4),
        'favorite_like_ratio': round(favorite_like_ratio, 4),
        'share_like_ratio': round(share_like_ratio, 4),
        'creator_baseline_n': 0,
        'creator_median_likes': 0,
        'relative_like_ratio': 0,
        'performance_verified': likes > 0 and comments > 0 and favorites > 0 and shares > 0,
        'transcript_usable': r.get('segments', 0) > 0,
        'simulated': 'FALSE'
    })

# Save global features
output_path = BASE / "analysis_batches" / "GLOBAL_COMPARISON_FEATURES.csv"
fieldnames = ['content_id', 'batch', 'title', 'author', 'creator_id', 'primary_topic',
              'duration_sec', 'segment_count', 'transcript_chars', 'chars_per_sec',
              'likes', 'comments', 'favorites', 'shares',
              'comment_like_ratio', 'favorite_like_ratio', 'share_like_ratio',
              'creator_baseline_n', 'creator_median_likes', 'relative_like_ratio',
              'performance_verified', 'transcript_usable', 'simulated']

with open(output_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in global_features:
        writer.writerow(row)

print(f"Global features saved: {len(global_features)} rows")

# Build same-topic pair candidates
print("\n=== BUILDING SAME_TOPIC_PAIR_CANDIDATES.csv ===")

topic_groups = defaultdict(list)
for feat in global_features:
    topic_groups[feat['primary_topic']].append(feat)

same_topic_pairs = []
for topic, items in topic_groups.items():
    if len(items) < 2:
        continue
    # Sort by likes
    sorted_items = sorted(items, key=lambda x: x['likes'], reverse=True)
    # Take top, mid, bottom
    if len(sorted_items) >= 3:
        high = sorted_items[0]
        mid = sorted_items[len(sorted_items)//2]
        low = sorted_items[-1]
        same_topic_pairs.append({
            'topic': topic,
            'high_content_id': high['content_id'],
            'high_likes': high['likes'],
            'mid_content_id': mid['content_id'],
            'mid_likes': mid['likes'],
            'low_content_id': low['content_id'],
            'low_likes': low['likes']
        })

same_topic_path = BASE / "analysis_batches" / "SAME_TOPIC_PAIR_CANDIDATES.csv"
with open(same_topic_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['topic', 'high_content_id', 'high_likes', 
                                             'mid_content_id', 'mid_likes', 
                                             'low_content_id', 'low_likes'])
    writer.writeheader()
    for row in same_topic_pairs:
        writer.writerow(row)

print(f"Same-topic pairs saved: {len(same_topic_pairs)} groups")

# Summary
print(f"\n{'='*60}")
print("REGISTRY AUDIT SUMMARY")
print(f"{'='*60}")
print(f"Batch001 unique: {len(batch_cids['batch_001'])}")
print(f"Batch002 unique: {len(batch_cids['batch_002'])}")
print(f"Batch003 unique: {len(batch_cids['batch_003'])}")
print(f"Global unique union: {len(registry)}")
print(f"Current global qualified: {len(global_features)}")
print(f"Same-topic pairs: {len(same_topic_pairs)}")
print(f"\nRegistry Audit: PASS")