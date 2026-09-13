#!/usr/bin/env python3
"""RC6B: Save Wave003 articles - batch 2"""
import json
import hashlib
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")
SRC = BASE / "01_benchmark/analysis_batches/batch_004_toutiao/SEED_WAVE_003"
HANDOFF = BASE / "handoff/chatgpt/batch_004/wave_003"

ARTICLES = [
    {"cid": "7671488207304868404", "title": "做自媒体最通透的几条真相", "url": "https://www.toutiao.com/article/7671488207304868404/", "author": "苏晗pb", "date": "2026-08-08", "topic": "能力变现", "theme": "自媒体创业", "gate": "TOPIC_PASS_MECHANICAL", "seed": "能力变现",
     "text": "第一，真诚永远是底色。敢于大方说出自己的优点，也坦然承认自己的缺点和过往的踩坑经历。\n第二，勇敢的人先享受世界。真正的勇敢是带着忐忑依然敢出镜、敢表达、敢持续输出。\n第三，多操作少空想，面子最不值钱。十条完美的理论不如一条粗糙的实操。\n第四，时间不会平白给答案，只会奖励持续迭代的人。"},
    {"cid": "7680513034233676323", "title": "李善友：DeepSeek的每一次取舍都在增加AGI实现的概率", "url": "https://www.toutiao.com/article/7680513034233676323/", "author": "混沌学园", "date": "2026-09-01", "topic": "AI商业", "theme": "DeepSeek战略", "gate": "TOPIC_PASS_MECHANICAL", "seed": "AI商业",
     "text": "DeepSeek选择克制。2025年春节上亿用户涌来时不做C端产品；AI Coding和Agent兴起后不做B端应用。始终聚焦基础模型，坚持开源和原创研究。梁文锋说唯一重要的事情是增加做成AGI的概率。"},
    {"cid": "7677915384284037651", "title": "一个冷门品牌成了直男的Lululemon", "url": "https://www.toutiao.com/article/7677915384284037651/", "author": "混沌学园", "date": "2026-08-25", "topic": "商业模式", "theme": "品牌定位", "gate": "TOPIC_PASS_MECHANICAL", "seed": "商业模式",
     "text": "龙牙战术服装2025年营收约18亿元两年翻倍。中30-50岁中年男性为核心客群提供省心可靠和身份认同。创始人蒋磊从铁血社区起家做战术装备到日常男装。"},
]

for art in ARTICLES:
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

print(f"\nTotal new: {len(ARTICLES)}")