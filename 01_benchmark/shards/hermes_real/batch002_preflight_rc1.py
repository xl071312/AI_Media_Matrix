#!/usr/bin/env python3
"""Batch002 Preflight RC1 - Fix Cross-Batch Dedupe"""
import csv
import json
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"

# Topic keywords
TOPIC_KEYWORDS = ["赚钱", "变现", "信息差", "副业", "创业", "职场", "中产", "焦虑", 
                  "消费", "陷阱", "AI", "搞钱", "翻身", "财富", "认知", "思维", 
                  "商业", "加盟", "避坑", "投资", "黄金", "回收", "降级", "收入",
                  "劳动", "打工", "老板", "生意", "财务", "自由", "存钱", "理财",
                  "贫穷", "富贵", "资本", "经济", "金融", "知识", "付费", "课程"]
OFF_TOPIC_MARKERS = ["游戏", "攻略", "三角洲", "原神", "王者荣耀", "动漫", "二次元",
                     "短剧", "剧情", "美食", "烹饪", "健身", "宠物", "旅游", "美妆",
                     "穿搭", "数码", "汽车", "音乐", "舞蹈", "搞笑", "综艺"]

def is_on_topic(title, desc=""):
    text = f"{title} {desc}".lower()
    for m in OFF_TOPIC_MARKERS:
        if m in text:
            return False
    matches = sum(1 for kw in TOPIC_KEYWORDS if kw in text)
    return matches >= 2

def normalize_cid(raw):
    """Normalize content_id: remove DY_REAL_ prefix, strip whitespace"""
    if not raw:
        return ""
    raw = str(raw).strip()
    # Remove BOM
    raw = raw.lstrip('\ufeff')
    # Remove DY_REAL_ prefix
    if raw.startswith('DY_REAL_'):
        raw = raw[8:]
    # Ensure string format
    return str(raw).strip()

def main():
    print("=== BATCH 002 PREFLIGHT RC1 ===\n")
    
    # Load Registry
    reg_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
    registry = set()
    with open(reg_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = normalize_cid(row.get('content_id', ''))
            if cid:
                registry.add(cid)
    
    print(f"Registry entries: {len(registry)}")
    
    # Load Selection
    sel_path = SHARDS / "douyin_benchmark_selection.csv"
    selections = []
    with open(sel_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_cid = row.get('content_id', row.get('aweme_id', ''))
            cid = normalize_cid(raw_cid)
            if cid:
                selections.append({
                    'raw_cid': raw_cid,
                    'cid': cid,
                    'title': row.get('desc', '')[:100],
                    'source_keyword': row.get('source_keyword', ''),
                    'performance_score': float(row.get('performance_score', 0)),
                    'sample_role': row.get('sample_role', ''),
                    'viral_type': row.get('viral_type', ''),
                    'liked_count': int(row.get('liked_count', 0)),
                    'comment_count': int(row.get('comment_count', 0)),
                    'collected_count': int(row.get('collected_count', 0)),
                    'share_count': int(row.get('share_count', 0))
                })
    
    print(f"Selection entries: {len(selections)}")
    
    # Check target CID
    target = '7525683513706810682'
    print(f"\nTarget CID {target}:")
    print(f"  In Registry: {target in registry}")
    
    # Classify selections
    existing_in_registry = []
    new_unique = []
    invalid = []
    
    for s in selections:
        cid = s['cid']
        if cid in registry:
            existing_in_registry.append(s)
        elif is_on_topic(s['title'], s['source_keyword']):
            new_unique.append({**s, 'on_topic': True})
        else:
            new_unique.append({**s, 'on_topic': False})
    
    # Split new unique by topic
    on_topic_new = [s for s in new_unique if s.get('on_topic')]
    off_topic_new = [s for s in new_unique if not s.get('on_topic')]
    
    print(f"\n=== CLASSIFICATION ===")
    print(f"Selection Total: {len(selections)}")
    print(f"Existing in Registry: {len(existing_in_registry)}")
    print(f"New Unique (ON_TOPIC): {len(on_topic_new)}")
    print(f"New Unique (OFF_TOPIC): {len(off_topic_new)}")
    print(f"Invalid: {len(invalid)}")
    
    # Verify math
    total = len(existing_in_registry) + len(on_topic_new) + len(off_topic_new) + len(invalid)
    print(f"Sum check: {total} == {len(selections)}: {total == len(selections)}")
    
    # Show top on_topic new unique
    on_topic_new.sort(key=lambda x: x['performance_score'], reverse=True)
    
    print(f"\n=== TOP 20 ON_TOPIC NEW UNIQUE ===")
    for i, s in enumerate(on_topic_new[:20], 1):
        print(f"{i}. {s['cid']} | perf={s['performance_score']:.1f} | {s['viral_type']}")
        print(f"   {s['title'][:60]}")
        print(f"   Keyword: {s['source_keyword']}")
    
    # Check for any registry violations in top 20
    violations = [s for s in on_topic_new[:20] if s['cid'] in registry]
    print(f"\nTOP20 Registry Violations: {len(violations)}")
    for v in violations:
        print(f"  VIOLATION: {v['cid']}")
    
    # Save results
    result = {
        'timestamp': datetime.now().isoformat(),
        'registry_size': len(registry),
        'selection_total': len(selections),
        'existing_in_registry': len(existing_in_registry),
        'new_unique_on_topic': len(on_topic_new),
        'new_unique_off_topic': len(off_topic_new),
        'invalid': len(invalid),
        'top_on_topic_new': on_topic_new[:20],
        'violations': violations
    }
    
    output_path = SHARDS / "batch002_preflight_rc1.json"
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\nSaved to: {output_path}")
    
    # Preflight verdict
    preflight_pass = len(violations) == 0 and len(on_topic_new) >= 30
    print(f"\nPREFLIGHT_QA: {'PASS' if preflight_pass else 'FAIL'}")
    if not preflight_pass:
        if len(violations) > 0:
            print(f"  FAIL: {len(violations)} registry violations in TOP20")
        if len(on_topic_new) < 30:
            print(f"  FAIL: Only {len(on_topic_new)} ON_TOPIC new unique (need 30)")
    
    return preflight_pass, on_topic_new

if __name__ == "__main__":
    preflight_pass, candidates = main()
