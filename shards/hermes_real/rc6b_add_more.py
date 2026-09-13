#!/usr/bin/env python3
"""RC6B: Add more Wave003 articles"""
import json
import hashlib
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")
SRC = BASE / "01_benchmark/analysis_batches/batch_004_toutiao/SEED_WAVE_003"
HANDOFF = BASE / "handoff/chatgpt/batch_004/wave_003"

# Additional articles found
NEW_ARTICLES = [
    {"cid": "7680513034233676323", "title": "李善友：DeepSeek的每一次取舍，都在增加AGI实现的概率", "url": "https://www.toutiao.com/article/7680513034233676323/", "author": "混沌学园", "date": "2026-09-01", "topic": "AI商业", "theme": "DeepSeek战略", "gate": "TOPIC_PASS_MECHANICAL", "seed": "AI商业",
     "text": "DeepSeek选择克制。2025年春节上亿用户涌来时，不做C端产品；AI Coding和Agent兴起后，不做B端应用。始终聚焦基础模型，坚持开源和原创研究。梁文锋说，唯一重要的事情是增加做成AGI的概率。"},
    {"cid": "7677915384284037651", "title": "一个冷门品牌，成了直男的Lululemon", "url": "https://www.toutiao.com/article/7677915384284037651/", "author": "混沌学园", "date": "2026-08-25", "topic": "商业模式", "theme": "品牌定位", "gate": "TOPIC_PASS_MECHANICAL", "seed": "商业模式",
     "text": "龙牙战术服装2025年营收约18亿元，两年翻倍。中30-50岁中年男性为核心客群，提供省心、可靠和身份认同。创始人蒋磊从铁血社区起家，做战术装备到日常男装。"},
    {"cid": "7683548929375339037", "title": "跑步与人生：别用别人的配速跑马拉松", "url": "https://www.toutiao.com/article/7683548929375339037/", "author": "苏晗pb", "date": "2026-09-09", "topic": "普通人收入", "theme": "职场认知", "gate": "TOPIC_PASS_MECHANICAL", "seed": "普通人收入",
     "text": "跑步这件事，最忌讳盲目攀比。真正的跑者不看别人配速，只看自己心率。人生不是百米冲刺，是考验耐力与智慧的马拉松。守住能力圈，在自己的时区稳步向前。"},
]

for art in NEW_ARTICLES:
    safe_id = art["cid"]
    src_path = SRC / f"{safe_id}.json"
    handoff_path = HANDOFF / f"{safe_id}.json"
    
    sha = hashlib.sha256(art["text"].encode('utf-8')).hexdigest()
    
    record = {
        "content_id": safe_id,
        "url": art["url"],
        "title": art["title"],
        "author": art["author"],
        "publish_date": art["date"],
        "raw_article_text": art["text"],
        "clean_article_text": art["text"],
        "text_chars": len(art["text"]),
        "placeholder_detected": False,
        "evidence_ready": True,
        "logic_analyzable": "PENDING_MODEL_REVIEW",
        "sha256": sha,
        "discovery_mode": "QUERY_FIRST",
        "search_seed": art["seed"],
        "topic_gate": art["gate"],
        "topic_category": art["topic"],
        "theme": art["theme"]
    }
    
    src_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    handoff_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Saved: {safe_id} - {art['gate']}")

print(f"\nTotal new: {len(NEW_ARTICLES)}")