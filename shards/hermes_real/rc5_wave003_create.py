#!/usr/bin/env python3
"""RC5 Task C: Wave003 - Create structure with available candidates"""
import json
import csv
import hashlib
import subprocess
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")
SRC = BASE / "01_benchmark/analysis_batches/batch_004_toutiao/SEED_WAVE_003"
HANDOFF = BASE / "handoff/chatgpt/batch_004/wave_003"
HANDOFF.mkdir(parents=True, exist_ok=True)
SRC.mkdir(parents=True, exist_ok=True)

# Keywords for classification
POSITIVE = ["赚钱", "搞钱", "副业", "变现", "商业", "创业", "AI", "收入", "职场", "赚钱方法"]
NEGATIVE = ["习近平", "金砖", "普京", "莫迪", "政治", "外交", "会议", "领导人"]

def classify(title):
    if any(n in title for n in NEGATIVE):
        return "OFF_TOPIC_MECHANICAL", "时政新闻"
    if any(p in title for p in POSITIVE):
        return "TOPIC_PASS_MECHANICAL", "商业/赚钱"
    return "TOPIC_REVIEW_REQUIRED", "其他"

# Candidates from browser discovery
candidates = [
    ("7684820046559969811", "推动软件产业实现换道超车（锐财经）", "商业模式/AI软件产业", "政经"),
    ("7684821300744962602", "2026年服贸会探新金融服务迈向精不精", "金融服务/商业模式", "政经"),
    ("7684594958250836523", "15名同事合买彩票中奖3000万港元", "彩票/人际关系", "社会新闻"),
    ("7684457991839531556", "52岁女演员卖韭菜盒子负债600万", "人生经历/演艺圈", "娱乐社会"),
    ("7684100593694032399", "武汉大学买商品房当学生公寓", "教育/房地产", "社会新闻"),
]

# Create candidate JSONs
results = []
for cid, title, category, dtype in candidates:
    gate_status, topic_type = classify(title)
    
    data = {
        "content_id": cid,
        "title": title,
        "category": category,
        "dtype": dtype,
        "topic_gate": gate_status,
        "placeholder_detected": True,  # Not extracted yet due to content type
        "evidence_ready": False,
        "logic_analyzable": "PENDING_MODEL_REVIEW",
        "mechanical_topic_hit": "",
        "obvious_off_topic": "" if gate_status == "TOPIC_PASS_MECHANICAL" else "时政/非核心赚钱逻辑",
        "gate_reason": "不符合核心赚钱/副业/AI变现主题" if gate_status != "TOPIC_PASS_MECHANICAL" else ""
    }
    
    # Save to source
    p = SRC / f"{cid}.json"
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Save to handoff
    h = HANDOFF / f"{cid}.json"
    with open(h, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    results.append({
        "content_id": cid,
        "title": title,
        "gate_status": gate_status,
        "topic_type": topic_type
    })

# Write TOPIC_GATE.csv
with open(HANDOFF / "TOPIC_GATE.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['content_id', 'title', 'gate_status', 'topic_type'])
    writer.writeheader()
    writer.writerows(results)

# Summary
passed = sum(1 for r in results if r['gate_status'] == 'TOPIC_PASS_MECHANICAL')
off = sum(1 for r in results if r['gate_status'] == 'OFF_TOPIC_MECHANICAL')
review = sum(1 for r in results if r['gate_status'] == 'TOPIC_REVIEW_REQUIRED')

print(f"Wave003 Created: {len(results)} candidates")
print(f"  PASSED: {passed}")
print(f"  OFF_TOPIC: {off}")
print(f"  REVIEW_REQUIRED: {review}")
print(f"\nNote: Current Toutiao feed dominated by BRICS political news.")
print(f"Core赚钱/副业 content limited. Need to wait for recommendation refresh or search.")

# Write FULLTEXT_QA.csv (empty since no fulltext extracted)
with open(HANDOFF / "FULLTEXT_QA.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['content_id', 'title', 'text_chars', 'fulltext_complete', 'evidence_ready', 'placeholder_detected'])
    writer.writeheader()
    for r in results:
        writer.writerow({
            'content_id': r['content_id'],
            'title': r['title'][:50],
            'text_chars': 0,
            'fulltext_complete': 'False',
            'evidence_ready': 'False',
            'placeholder_detected': 'True'
        })

print(f"\nFiles created:")
print(f"  {HANDOFF}/TOPIC_GATE.csv")
print(f"  {HANDOFF}/FULLTEXT_QA.csv")
print(f"  {HANDOFF}/*.json ({len(results)} files)")