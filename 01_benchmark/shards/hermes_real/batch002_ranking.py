#!/usr/bin/env python3
"""Batch 002 Production - Create Candidate Ranking"""
import csv
import json
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"

# Load preflight results
preflight_path = SHARDS / "batch002_preflight_rc1.json"
with open(preflight_path, 'r', encoding='utf-8') as f:
    preflight = json.load(f)

candidates = preflight['top_on_topic_new']
print(f"Loaded {len(candidates)} ON_TOPIC candidates")

# Topic keywords for categorization
TOPIC_MAP = {
    '赚钱逻辑': ['赚钱', '搞钱', '财富', '收入', '金钱'],
    '能力变现': ['变现', '副业', '技能', '个人成长'],
    '信息差': ['信息差', '认知', '思维', '知识'],
    '职场': ['职场', '打工', '老板', '工作'],
    '消费陷阱': ['消费', '陷阱', '降级', '省钱'],
    '创业': ['创业', '商业', '生意', '加盟'],
    '普通人翻身': ['翻身', '普通人', '逆袭'],
    'AI赚钱': ['AI', '人工智能', '大模型'],
    '投资认知': ['投资', '理财', '黄金', '金融'],
    '中产焦虑': ['中产', '焦虑', '返贫']
}

def classify_topic(title, keyword):
    """Classify topic based on title and source keyword"""
    text = f"{title} {keyword}".lower()
    
    # Check OFF_TOPIC markers
    off_markers = ['游戏', '攻略', '三角洲', '原神', '动漫', '短剧', '剧情', 
                   '美食', '健身', '宠物', '旅游', '美妆', '穿搭', '数码', 
                   '汽车', '音乐', '舞蹈', '搞笑', '综艺', '电影', '明星']
    for m in off_markers:
        if m in text:
            return 'OFF_TOPIC'
    
    # Check topic categories
    for topic, keywords in TOPIC_MAP.items():
        matches = sum(1 for kw in keywords if kw in text)
        if matches >= 2:
            return topic
    
    return keyword if keyword else 'GENERAL'

def main():
    print("=== BATCH 002 CANDIDATE RANKING ===\n")
    
    rows = []
    for i, c in enumerate(candidates, 1):
        cid = c['cid']
        title = c['title']
        keyword = c.get('source_keyword', '')
        
        # Classify topic
        topic = classify_topic(title, keyword)
        
        # Parse metrics
        likes = c.get('liked_count', 0)
        comments = c.get('comment_count', 0)
        favorites = c.get('collected_count', 0)
        shares = c.get('share_count', 0)
        
        # Check if performance verified (all > 0)
        perf_verified = likes > 0 and comments > 0 and favorites > 0 and shares > 0
        
        row = {
            'content_id': cid,
            'title': title[:100],
            'author': '',  # To be filled from page
            'topic': topic,
            'duration': '',  # To be filled from page
            'likes': likes,
            'comments': comments,
            'favorites': favorites,
            'shares': shares,
            'performance_verified': perf_verified,
            'sample_role': c.get('sample_role', ''),
            'viral_type': c.get('viral_type', ''),
            'creator_id': '',
            'cross_batch_duplicate': 'FALSE',
            'topic_pass': 'TRUE',
            'spoken_content_candidate': 'PENDING',
            'selection_score': c.get('performance_score', 0),
            'queue_priority': i
        }
        rows.append(row)
    
    # Sort by performance score
    rows.sort(key=lambda x: x['selection_score'], reverse=True)
    for i, r in enumerate(rows, 1):
        r['queue_priority'] = i
    
    # Save CSV
    csv_path = SHARDS / "BATCH002_CANDIDATE_RANKING.csv"
    fieldnames = list(rows[0].keys())
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Saved: {csv_path}")
    print(f"Total candidates: {len(rows)}")
    
    # Summary by topic
    topic_counts = {}
    for r in rows:
        t = r['topic']
        topic_counts[t] = topic_counts.get(t, 0) + 1
    
    print("\nTopic Distribution:")
    for t, c in sorted(topic_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")
    
    # Show top 30 priorities
    print("\nTOP 30 Queue Priority:")
    for i, r in enumerate(rows[:30], 1):
        print(f"{i}. {r['content_id']} | {r['topic']} | perf={r['selection_score']:.1f} | verified={r['performance_verified']}")
        print(f"   {r['title'][:60]}")
    
    return rows[:30]

if __name__ == "__main__":
    top30 = main()
