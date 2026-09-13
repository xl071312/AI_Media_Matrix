#!/usr/bin/env python3
"""RC5 Task C: Wave003 - Discovery and Topic Gate"""
import json
import csv
import hashlib
import subprocess
from pathlib import Path
import re
import time

BASE = Path(r"F:\workspace\AI_Media_Matrix")
SRC = BASE / "01_benchmark/analysis_batches/batch_004_toutiao/SEED_WAVE_003"
HANDOFF = BASE / "handoff/chatgpt/batch_004/wave_003"
HANDOFF.parent.mkdir(parents=True, exist_ok=True)
SRC.mkdir(parents=True, exist_ok=True)

# Keywords for topic classification
POSITIVE_KEYWORDS = [
    "赚钱", "搞钱", "收入", "副业", "变现", "商业", "创业", "信息差", 
    "财富", "职场", "AI赚钱", "AI变现", "普通人收入", "消费", "中产", 
    "投资认知", "能力变现", "兼职", "赚钱方法", "赚钱途径", "网上赚钱",
    "自媒体", "内容创作", "流量", "变现路径", "轻资产", "低成本",
    "商业模式", "生意", "客户", "需求", "市场验证", "定价", "价值",
    "交易", "复购", "AI商业", "AI创业", "人效", "价值交换",
    "品牌定位", "供应链", "渠道", "用户", "增长", "成本", "利润",
    "财富认知", "消费认知"
]

NEGATIVE_INDICATORS = [
    "疫情", "隔离", "核酸", "新冠", "新冠病例",  # epidemic
    "外墙保温", "保温层", "EPS板", "保温板",  # construction
    "习近平", "李克强", "政治局", "两会",  # politics
    "足球", "篮球", "奥运会", "NBA", "世界杯",  # sports
    "离婚", "结婚", "恋爱", "婚姻", "出轨",  # relationships
    "旅游景点", "旅游攻略", "旅行",  # travel
    "做菜", "菜谱", "美食", "烹饪",  # food
    "发烧", "医院", "医生", "治疗",  # health
]

def classify_by_title(title):
    """Classify article by title/snippet keywords"""
    if not title:
        return "OFF_TOPIC_MECHANICAL"
    
    title_lower = title.lower()
    
    # Check positive
    positive_hits = [kw for kw in POSITIVE_KEYWORDS if kw in title]
    
    # Check negative
    negative_hits = [neg for neg in NEGATIVE_INDICATORS if neg in title]
    
    if negative_hits and not positive_hits:
        return "OFF_TOPIC_MECHANICAL"
    elif positive_hits:
        return "TOPIC_PASS_MECHANICAL"
    else:
        return "TOPIC_REVIEW_REQUIRED"

def get_category_from_title(title):
    """Categorize article for diversity tracking"""
    if not title:
        return "UNKNOWN"
    
    if any(kw in title for kw in ["赚钱", "搞钱", "副业", "AI赚钱", "AI变现", "变现", "收入"]):
        return "能力变现/副业"
    elif any(kw in title for kw in ["商业", "创业", "商业模式", "生意", "品牌"]):
        return "商业模式/business case"
    elif any(kw in title for kw in ["职场", "普通人", "中产", "打工人"]):
        return "普通人收入/职场"
    elif any(kw in title for kw in ["消费", "财富", "认知", "中产焦虑"]):
        return "消费/财富认知"
    elif any(kw in title for kw in ["AI", "人工智能"]):
        return "AI赚钱/AI商业"
    else:
        return "其他"

# Existing CIDs to avoid duplicates
existing_cids = set()
for w in ["SEED_WAVE_001_REFETCH", "SEED_WAVE_002"]:
    src_path = BASE / f"01_benchmark/analysis_batches/batch_004_toutiao/{w}"
    if src_path.exists():
        for p in src_path.glob("*.json"):
            existing_cids.add(p.stem)

print(f"Existing CIDs to avoid: {len(existing_cids)}")

# Generate candidate CIDs in the right range (newer articles)
candidates = []
import random
random.seed(20260913)

# Try CIDs from 7685000000000000000 to 7695000000000000000 (newer articles)
for i in range(100):
    cid = 7685000000000000000 + random.randint(0, 5000000000)
    cid = int(str(cid)[:19])  # Ensure 19 digits
    if str(cid) not in existing_cids:
        candidates.append(str(cid))

print(f"Generated {len(candidates)} candidate CIDs for discovery")

# Save candidates for batch processing
with open(SRC / "CANDIDATES.txt", 'w', encoding='utf-8') as f:
    f.write('\n'.join(candidates[:50]))

print("Candidates saved to CANDIDATES.txt")
print(f"Will discover: {min(50, len(candidates))} candidates")