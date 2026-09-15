#!/usr/bin/env python3
"""RC6H: Initialize discovery infrastructure"""
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix")
RC6H_DIR = BASE / "01_benchmark/plain_language_discovery_rc6h"
RC6H_DIR.mkdir(parents=True, exist_ok=True)

# Query bank from task spec
QUERY_BANK = [
    # Money / ordinary-person framing
    "普通人赚钱", "普通人收入", "工资到底", "一个月工资", "攒钱",
    "花钱值不值", "消费降级", "消费陷阱", "赚钱思维", "搞钱",
    "副业避坑", "副业怎么选", "开店亏钱", "小生意", "普通人翻身",
    # Work / boss / employee framing
    "打工人", "上班真相", "老板为什么", "职场真相", "汇报工作",
    "工资涨不上去", "为什么升职", "工作值不值", "职场避坑", "被裁员怎么办",
    # Explain-it-simply framing
    "大白话讲", "我给你算一笔账", "给你算一下", "到底什么意思",
    "举个例子", "一看就懂", "普通人能听懂", "说白了", "你想一下", "为什么呢",
    # AI + ordinary Chinese work/life
    "AI 普通人", "AI 工作", "AI 上班", "AI 副业", "AI 赚钱", "AI 打工人",
]

# Save query bank
with open(RC6H_DIR / "DISCOVERY_QUERY_BANK.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['query', 'category', 'order'])
    categories = {
        '普通人赚钱': 'money', '普通人收入': 'money', '工资到底': 'money',
        '一个月工资': 'money', '攒钱': 'money', '花钱值不值': 'money',
        '消费降级': 'money', '消费陷阱': 'money', '赚钱思维': 'money', '搞钱': 'money',
        '副业避坑': 'money', '副业怎么选': 'money', '开店亏钱': 'money',
        '小生意': 'money', '普通人翻身': 'money',
        '打工人': 'work', '上班真相': 'work', '老板为什么': 'work',
        '职场真相': 'work', '汇报工作': 'work', '工资涨不上去': 'work',
        '为什么升职': 'work', '工作值不值': 'work', '职场避坑': 'work',
        '被裁员怎么办': 'work',
        '大白话讲': 'explain', '我给你算一笔账': 'explain', '给你算一下': 'explain',
        '到底什么意思': 'explain', '举个例子': 'explain', '一看就懂': 'explain',
        '普通人能听懂': 'explain', '说白了': 'explain', '你想一下': 'explain',
        '为什么呢': 'explain',
        'AI 普通人': 'ai', 'AI 工作': 'ai', 'AI 上班': 'ai',
        'AI 副业': 'ai', 'AI 赚钱': 'ai', 'AI 打工人': 'ai',
    }
    for i, q in enumerate(QUERY_BANK, 1):
        cat = categories.get(q, 'other')
        writer.writerow([q, cat, i])

print(f"Query bank saved: {len(QUERY_BANK)} queries")
print(f"RC6H directory: {RC6H_DIR}")

# Initialize result tracking
results = []
with open(RC6H_DIR / "DISCOVERY_RESULTS_RAW.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['query', 'rank', 'content_id', 'title', 'author', 'duration_sec', 
                     'likes', 'comments', 'favorites', 'shares', 'url', 'discovery_timestamp', 'route'])
    # Will populate during discovery

# Route counts
route_counts = {'route_a_douyin': 0, 'route_b_related': 0, 'route_c_creator': 0, 'route_d_toutiao': 0}
with open(RC6H_DIR / "DISCOVERY_ROUTE_COUNTS.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['route', 'count', 'description'])
    writer.writerow(['route_a_douyin', 0, 'Live Douyin topic search'])
    writer.writerow(['route_b_related', 0, 'Related/adjacent videos'])
    writer.writerow(['route_c_creator', 0, 'Creator-neighbor expansion'])
    writer.writerow(['route_d_toutiao', 0, 'Toutiao video search (fallback)'])

print("Infrastructure initialized")