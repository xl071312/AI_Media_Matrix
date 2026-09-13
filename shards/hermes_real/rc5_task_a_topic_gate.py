#!/usr/bin/env python3
"""RC5 Task A: Wave002 Topic Gate - Classify articles by mechanical keyword hit"""
import json
import csv
import re
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SRC = BASE / "analysis_batches/batch_004_toutiao/SEED_WAVE_002"
HANDOFF = BASE.parent / "handoff/chatgpt/batch_004/wave_002"
QA_CSV = HANDOFF.parent.parent / "WAVE002_TOPIC_GATE.csv"

# Positive keyword families (mechanical hit)
POSITIVE_KEYWORDS = [
    "赚钱", "搞钱", "副业", "收入", "变现", "商业", "创业", "信息差", 
    "财富", "职场", "AI赚钱", "AI变现", "普通人收入", "消费", "中产", 
    "投资认知", "能力变现", "兼职", "赚钱方法", "赚钱途径", "网上赚钱",
    "自媒体", "内容创作", "流量", "变现路径", "轻资产", "低成本"
]

# Negative/off-topic indicators
NEGATIVE_INDICATORS = [
    "疫情", "隔离", "核酸", "新冠", "新冠病例",  # epidemic diary
    "外墙保温", "保温层", "EPS板", "保温板",  # construction engineering
    "政治", "国际", "新闻", "时政", "中美",  # politics/news
    "恋爱", "婚姻", "情感", "朋友", "社交",  # relationship/life essay
    "体育", "足球", "篮球", "奥运会",  # sports
    "美食", "菜谱", "烹饪", "做菜",  # food/cooking
    "旅游", "景点", "旅行",  # travel
]

def classify_article(p):
    """Classify article by mechanical topic gate"""
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cid = p.stem
    title = data.get('title', '')
    first_text = (data.get('clean_article_text', '') or data.get('raw_article_text', ''))[:300]
    
    # Check positive keywords in title + first 300 chars
    positive_hits = []
    for kw in POSITIVE_KEYWORDS:
        if kw in title or kw in first_text:
            positive_hits.append(kw)
    
    # Check negative indicators
    negative_hits = []
    for neg in NEGATIVE_INDICATORS:
        if neg in title or neg in first_text:
            negative_hits.append(neg)
    
    # Determine gate status
    text_chars = len(data.get('clean_article_text', '') or data.get('raw_article_text', ''))
    
    if negative_hits and not positive_hits:
        gate_status = "OFF_TOPIC_MECHANICAL"
    elif positive_hits:
        gate_status = "TOPIC_PASSED_MECHANICAL"
    else:
        gate_status = "TOPIC_REVIEW_REQUIRED"
    
    return {
        'content_id': cid,
        'title_or_first_line': title[:50] if title else first_text[:50],
        'text_chars': text_chars,
        'mechanical_topic_hit': ','.join(positive_hits) if positive_hits else '',
        'obvious_off_topic': ','.join(negative_hits) if negative_hits else '',
        'gate_status': gate_status
    }

# Process all Wave002 articles
results = []
for p in sorted(SRC.glob("*.json")):
    results.append(classify_article(p))

# Write CSV
with open(QA_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['content_id', 'title_or_first_line', 'text_chars', 
                                           'mechanical_topic_hit', 'obvious_off_topic', 'gate_status'])
    writer.writeheader()
    writer.writerows(results)

# Summary
passed = sum(1 for r in results if r['gate_status'] == 'TOPIC_PASSED_MECHANICAL')
off_topic = sum(1 for r in results if r['gate_status'] == 'OFF_TOPIC_MECHANICAL')
review = sum(1 for r in results if r['gate_status'] == 'TOPIC_REVIEW_REQUIRED')

print(f"Wave002 Topic Gate Results:")
print(f"  Total: {len(results)}")
print(f"  PASSED (mechanical): {passed}")
print(f"  OFF_TOPIC (mechanical): {off_topic}")
print(f"  REVIEW_REQUIRED: {review}")
print(f"\nCSV saved: {QA_CSV}")

# Show passed articles
print("\nPassed articles:")
for r in results:
    if r['gate_status'] == 'TOPIC_PASSED_MECHANICAL':
        print(f"  ✓ {r['content_id']}: {r['title_or_first_line'][:40]}...")

print("\nOff-topic articles:")
for r in results:
    if r['gate_status'] == 'OFF_TOPIC_MECHANICAL':
        print(f"  ✗ {r['content_id']}: {r['title_or_first_line'][:40]}... ({r['obvious_off_topic']})")