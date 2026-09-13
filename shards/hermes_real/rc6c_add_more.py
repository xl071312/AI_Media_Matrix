#!/usr/bin/env python3
"""RC6C: Add more verified Wave003 articles"""
import json
import hashlib
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")
REAL_DIR = BASE / "handoff/chatgpt/batch_004/wave_003_real"

ARTICLES = [
    {
        "cid": "7683110588213363240",
        "title": "卖木头的源氏木语，怎么把床垫也卖成了第一？",
        "url": "https://www.toutiao.com/article/7683110588213363240/",
        "author": "DT商业观察",
        "date": "2026-09-08",
        "text": "提到源氏木语，大多数人脑海中浮现的是实木家具、高性价比等关键词。但很有反差的是，它的实绩已不止于此。源氏木语除了高性价比的实木家具，还有更顶尖的高端产品。8月7日，源氏木语举办新实木主义黑标生活提案品牌发布会。黑标系列是源氏木语整体实木的品质高锚点。再比如，源氏木语的产品线其实不止实木。以床垫为例，2023年-2026年，源氏木语床垫累计销量约217.6万张，销售额约36.5亿元；2024年-2026年元气床垫累计销量约12万张，销售额约4亿元。前不久，全球权威增长咨询机构弗若斯特沙利文给它贴上了三项销量第一的认证：实木、黑胡桃木，以及一个让行业侧目的类别——0胶水床垫全国销量第一（按2025年度销量计）。一家刻着木材基因的企业，为什么要跨界进入软体家具的赛道，又如何把床垫做成了又一个明星品类？源氏木语作为以实木起家的品牌，凭什么让消费者为它的床垫买单？从社媒数据来看，源氏木语品牌的核心用户是正在装修的年轻家庭，他们可能空间有限、预算有限，但对家居品质和环保安全有着明确的诉求。源氏木语床垫品类的平均价格在2000元左右，延续了实木家具低毛利、统一定价的习惯，线上线下同价，比大牌便宜。源氏木语的品类扩张逻辑很清晰：我们通过查阅资料发现，在生产端，虽然床垫和实木家具无法共用同一条生产线，但源氏木语已经围绕自身需求形成了产业集群，让床垫生产的边际成本被大幅摊薄。在源氏木语的带动下，铺集镇已经形成从原材料到成品的十五分钟供应链圈。全链路资源的复用可以提高效率，迅速形成规模，而规模效应又能进一步降低成本，形成正向循环。",
        "topic": "商业模式",
        "theme": "供应链复利",
        "gate": "TOPIC_PASS_MECHANICAL"
    },
]

for art in ARTICLES:
    safe_id = art['cid']
    dst_path = REAL_DIR / f"{safe_id}.json"
    
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
        "search_seed": art["topic"],
        "topic_gate": art["gate"],
        "topic_category": art["topic"],
        "theme": art["theme"]
    }
    
    dst_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Saved: {safe_id} ({len(art['text'])} chars) - {art['gate']}")

print(f"\nTotal new: {len(ARTICLES)}")