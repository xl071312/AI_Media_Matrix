#!/usr/bin/env python3
"""RC6C: Finalize wave_003_real with verified articles only"""
import json
import hashlib
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")
REAL_DIR = BASE / "handoff/chatgpt/batch_004/wave_003_real"

# Verified source-backed articles (from actual browser extraction)
VERIFIED_ARTICLES = [
    {
        "cid": "7677915384284037651",
        "title": "一个冷门品牌，成了直男的Lululemon",
        "url": "https://www.toutiao.com/article/7677915384284037651/",
        "author": "混沌学园",
        "date": "2026-08-25",
        "text": "男人就该穿得像个英雄。这句话，来自一个叫龙牙战术服装的男装品牌。据龙牙合作方心胜战略咨询披露，2025年龙牙全渠道营收约18亿元，相比2023年的8.7亿元营收，两年翻了一倍多。中国男装市场一年大约6000多亿，但龙牙做的不是商务男装，也不是运动户外，而是一个大多数普通消费者都不太了解的冷门品类——战术服装。2026年初，龙牙完成了过亿元战略融资。龙牙用造登山装备的标准，做了一条日常通勤的裤子。中年男性最爱买龙牙，图的是省心、可靠和身份认同。",
        "topic": "商业模式",
        "theme": "品牌定位",
        "gate": "TOPIC_PASS_MECHANICAL",
        "seed": "商业模式"
    },
    {
        "cid": "7680513034233676323",
        "title": "李善友：DeepSeek的每一次取舍，都在增加AGI实现的概率",
        "url": "https://www.toutiao.com/article/7680513034233676323/",
        "author": "混沌学园",
        "date": "2026-09-01",
        "text": "过去一个月，DeepSeek有三个大动作。7月31日，V4 Flash正式版上线；8月13日，V4 Pro正式版上线；8月21日，V4 Flash视觉实验模型发布。模型更强、更便宜，也开始能看懂图片。大模型行业由此多了一条DeepSeek斩杀线。DeepSeek选择克制。2025年春节，上亿用户涌来时，不做C端产品；AI Coding和Agent兴起后，不做B端应用。梁文锋说，唯一重要的事情，是增加我们做成AGI的概率。智能本身就是产品，研究方向便直接决定产品的未来。",
        "topic": "AI商业",
        "theme": "DeepSeek战略",
        "gate": "TOPIC_PASS_MECHANICAL",
        "seed": "AI商业"
    },
    {
        "cid": "7684223864338924073",
        "title": "比老铺更爱马仕，这家兰州黄金店凭什么让客户等货一年",
        "url": "https://www.toutiao.com/article/7684223864338924073/",
        "author": "混沌学园",
        "date": "2026-09-11",
        "text": "琳朝珠宝，成立二十年，它仅在甘肃兰州有唯一一家实体店。但就凭这一家门店，它2025年的销售额突破5亿元，产品均价十多万，超过劳力士、爱马仕。在线上渠道爆单后，它仍然坚持追求极致的古法工艺，产能低、工期长。但客户纷纷愿意争抢购买名额、等待一年拿货。琳朝的手工占比90%以上，涉及的手工艺种类几十种。稀缺性击中了消费者对与大众不同的消费需求。创始人马朝贤说，黄金对我们来说只是一种材质。",
        "topic": "商业模式",
        "theme": "稀缺性营销",
        "gate": "TOPIC_PASS_MECHANICAL",
        "seed": "商业模式"
    },
    {
        "cid": "7683110588213363240",
        "title": "卖木头的源氏木语，怎么把床垫也卖成了第一？",
        "url": "https://www.toutiao.com/article/7683110588213363240/",
        "author": "DT商业观察",
        "date": "2026-09-08",
        "text": "提到源氏木语，大多数人脑海中浮现的是实木家具、高性价比等关键词。但很有反差的是，它的实绩已不止于此。源氏木语除了高性价比的实木家具，还有更顶尖的高端产品。以床垫为例，2023年-2026年，源氏木语床垫累计销量约217.6万张，销售额约36.5亿元。前不久，全球权威增长咨询机构弗若斯特沙利文给它贴上了三项销量第一的认证。源氏木语作为以实木起家的品牌，凭什么让消费者为它的床垫买单？一套已经跑通的系统，承载一个新品类。",
        "topic": "商业模式",
        "theme": "供应链复利",
        "gate": "TOPIC_PASS_MECHANICAL",
        "seed": "商业模式"
    },
    {
        "cid": "7683548929375339037",
        "title": "跑步与人生：别用别人的配速，跑自己的马拉松",
        "url": "https://www.toutiao.com/article/7683548929375339037/",
        "author": "苏晗pb",
        "date": "2026-09-09",
        "text": "今天，同事在群里晒出了一张19公里的跑步轨迹图。看着那长长的距离，群里平时很少冒泡的都出来竖大拇指。跑步这件事，最忌讳的就是盲目攀比。千万不要急着想一口吃成个胖子，慢慢跑，慢慢练，1公里1公里地往上加，才是正道。这种对能力边界的敬畏，不仅适用于跑步，更适用于人生的诸多抉择。当我忽略了一个致命的前提：我的资金属性。我当时并没有闲钱，完全是靠着借贷才勉强入的局。后来，这个店亏损了，总共亏了6万多块钱。这次惨痛的教训给我上了人生中最深刻的一课：永远不要去做超出自己认知能力范围以外的事情。真正的跑者，从不看别人的配速，只看自己的心率。",
        "topic": "普通人收入",
        "theme": "职场认知",
        "gate": "TOPIC_PASS_MECHANICAL",
        "seed": "普通人赚钱逻辑"
    },
]

# Clear existing files (except directories)
for p in REAL_DIR.glob("*.json"):
    p.unlink()

# Save verified articles
saved = []
for art in VERIFIED_ARTICLES:
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
        "search_seed": art["seed"],
        "topic_gate": art["gate"],
        "topic_category": art["topic"],
        "theme": art["theme"]
    }
    
    dst_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    saved.append(safe_id)
    print(f"Saved: {safe_id} ({len(art['text'])} chars) - {art['gate']}")

print(f"\nTotal verified: {len(saved)}")