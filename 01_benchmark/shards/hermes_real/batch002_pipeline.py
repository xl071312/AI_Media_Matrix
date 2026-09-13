#!/usr/bin/env python3
"""Batch 002 Pipeline with Topic Gate - From Selection"""
import csv
import json
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
SELECTION_PATH = SHARDS / "douyin_benchmark_selection.csv"
REGISTRY_PATH = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
BATCH2_DIR = BASE / "analysis_batches" / "batch_002"
MEDIA_DIR = BASE / "media" / "batch_002_smoke"

# Topic keywords for relevance check
TOPIC_KEYWORDS = [
    "赚钱", "赚钱逻辑", "变现", "信息差", "副业", "创业", "职场", 
    "中产", "焦虑", "消费", "陷阱", "AI", "搞钱", "翻身", "财富",
    "认知", "思维", "商业", "加盟", "避坑", "投资", "黄金", "回收",
    "降级", "收入", "劳动", "打工", "老板", "生意", "成本", "利润",
    "财务", "自由", "存钱", "理财", "贫穷", "富贵", "资本", "经济",
    "金融", "知识", "付费", "课程", "变现"
]

OFF_TOPIC_MARKERS = [
    "游戏", "游戏攻略", "三角洲", "原神", "王者荣耀", "和平精英",
    "动漫", "二次元", "COS", "漫画", "动画",
    "短剧", "剧情", "电视剧", "电影", "娱乐",
    "美食", "烹饪", "食谱", "吃货",
    "健身", "减肥", "瑜伽", "运动",
    "宠物", "猫", "狗", "萌宠",
    "旅游", "景点", "攻略",
    "美妆", "化妆", "护肤",
    "穿搭", "时尚", "衣服",
    "数码", "手机", "科技",
    "汽车", "车", "驾驶",
    "音乐", "歌曲", "演唱会",
    "舞蹈", "跳舞",
    "搞笑", "段子", "综艺"
]

def is_on_topic(title, desc=""):
    """Check if content is on-topic for Batch002"""
    text = f"{title} {desc}".lower()
    
    # Check for off-topic markers
    for marker in OFF_TOPIC_MARKERS:
        if marker in text:
            return False, f"OFF_TOPIC: {marker}"
    
    # Check for on-topic keywords
    topic_matches = sum(1 for kw in TOPIC_KEYWORDS if kw in text)
    if topic_matches >= 2:
        return True, f"ON_TOPIC ({topic_matches} keywords)"
    
    # Check source_keyword from selection
    return False, "NO_TOPIC_SIGNALS"

def load_registry():
    """Load global content ID registry"""
    registry = set()
    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row.get('content_id', '').strip()
            if cid:
                registry.add(cid)
    return registry

def load_selection():
    """Load selection CSV"""
    selections = []
    with open(SELECTION_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Clean up column names (remove BOM)
            cleaned = {k.strip(): v for k, v in row.items()}
            selections.append(cleaned)
    return selections

def main():
    print("=== BATCH 002 PIPELINE WITH TOPIC GATE ===\n")
    
    # Load data
    registry = load_registry()
    selections = load_selection()
    
    print(f"Registry entries: {len(registry)}")
    print(f"Selection entries: {len(selections)}")
    
    # Filter: NOT in registry (NEW)
    new_candidates = []
    for s in selections:
        # Get content_id (may be aweme_id or content_id column)
        cid = s.get('content_id', '').strip()
        if not cid:
            cid = s.get('aweme_id', '').strip()
        if not cid:
            continue
        
        # Skip if in registry
        if cid in registry:
            continue
        
        # Get metadata
        title = s.get('desc', '')[:100]
        source_kw = s.get('source_keyword', '')
        
        # Apply topic gate
        on_topic, reason = is_on_topic(title, source_kw)
        
        new_candidates.append({
            'cid': cid,
            'title': title,
            'source_keyword': source_kw,
            'on_topic': on_topic,
            'topic_reason': reason,
            'performance_score': float(s.get('performance_score', 0)),
            'sample_role': s.get('sample_role', ''),
            'viral_type': s.get('viral_type', '')
        })
    
    # Split by topic
    on_topic = [c for c in new_candidates if c['on_topic']]
    off_topic = [c for c in new_candidates if not c['on_topic']]
    
    print(f"\nNew candidates (not in registry): {len(new_candidates)}")
    print(f"  ON_TOPIC: {len(on_topic)}")
    print(f"  OFF_TOPIC: {len(off_topic)}")
    
    # Show ON_TOPIC candidates sorted by performance
    on_topic.sort(key=lambda x: x['performance_score'], reverse=True)
    
    print("\n--- ON_TOPIC Candidates (top 20) ---")
    for i, c in enumerate(on_topic[:20], 1):
        print(f"{i}. {c['cid']} | perf={c['performance_score']:.1f} | role={c['sample_role']}")
        print(f"   {c['title'][:60]}")
        print(f"   Keyword: {c['source_keyword']} | {c['topic_reason']}")
    
    # Save candidates list
    candidates_path = SHARDS / "batch002_candidates.json"
    candidates_path.write_text(json.dumps({
        'timestamp': datetime.now().isoformat(),
        'total_new': len(new_candidates),
        'on_topic_count': len(on_topic),
        'off_topic_count': len(off_topic),
        'on_topic': on_topic,
        'off_topic': off_topic
    }, indent=2, ensure_ascii=False))
    
    print(f"\nSaved to: {candidates_path}")
    
    # Return top candidates for processing
    return on_topic[:30]  # Target 30

if __name__ == "__main__":
    candidates = main()
    print(f"\nReady to process: {len(candidates)} candidates")
