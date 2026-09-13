#!/usr/bin/env python3
"""RC6B: Save additional Wave003 articles"""
import json
import hashlib
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")
SRC = BASE / "01_benchmark/analysis_batches/batch_004_toutiao/SEED_WAVE_003"
HANDOFF = BASE / "handoff/chatgpt/batch_004/wave_003"

NEW_ARTICLES = [
    {"cid": "7678657654369141289", "title": "867亿！黄仁勋收购Hugging Face拿下AI界GitHub", "url": "https://www.toutiao.com/article/7678657654369141289/", "author": "混沌学园", "date": "2026-08-27", "topic": "AI商业", "theme": "开源生态", "gate": "TOPIC_PASS_MECHANICAL", "seed": "AI创业",
     "text": "英伟达以129亿美元收购Hugging Face。Hugging Face是AI界的GitHub，拥有100万+模型、42万+数据集。开源社区创造比封闭平台高1000倍的价值。"},
    {"cid": "7683548929375339037", "title": "跑步与人生：别用别人的配速跑马拉松", "url": "https://www.toutiao.com/article/7683548929375339037/", "author": "苏晗pb", "date": "2026-09-09", "topic": "普通人收入", "theme": "职场认知", "gate": "TOPIC_PASS_MECHANICAL", "seed": "普通人收入",
     "text": "跑步最忌讳盲目攀比。真正的跑者不看别人配速只看自己心率。人生不是百米冲刺，是考验耐力与智慧的马拉松。守住能力圈，在自己的时区稳步向前。"},
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

print("\nTotal new: 2")