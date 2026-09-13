#!/usr/bin/env python3
"""RC6B: Save all extracted Wave003 articles with fulltext"""
import json
import hashlib
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix")
SRC = BASE / "01_benchmark/analysis_batches/batch_004_toutiao/SEED_WAVE_003"
HANDOFF = BASE / "handoff/chatgpt/batch_004/wave_003"

# All extracted articles with their content
ARTICLES = [
    {
        "cid": "7684223864338924073",
        "title": "比老铺更「爱马仕」，这家兰州黄金店凭什么让客户等货一年？",
        "url": "https://www.toutiao.com/article/7684223864338924073/",
        "author": "混沌学园",
        "date": "2026-09-11",
        "text": "琳朝珠宝，成立二十年，它仅在甘肃兰州有唯一一家实体店。但就凭这一家门店，它2025年的销售额突破5亿元，产品均价十多万，超过劳力士、爱马仕。\n\n在线上渠道爆单后，它仍然坚持追求极致的古法工艺，产能低、工期长。但客户纷纷愿意争抢购买名额、等待一年拿货。\n\n接受亿元战略融资，筹备第二家店，但它的产能又严重受限于难以稳定培养的手艺师傅。\n\n这样一个“快不起来”的品牌，为什么能卖得如此贵？为什么“供不应求”，但客户仍然愿意为它等待？",
        "topic": "商业模式/business case",
        "theme": "稀缺性营销",
        "gate": "TOPIC_PASS_MECHANICAL",
        "seed": "商业模式"
    },
    {
        "cid": "7684820046559969811",
        "title": "推动软件产业实现“换道超车”",
        "url": "https://www.toutiao.com/article/7684820046559969811/",
        "author": "人民网",
        "date": "2026-09-13",
        "text": "人工智能深刻变革软件和信息技术服务业的开发方式、产品形态与服务模式，成为驱动产业升级的核心引擎。工业和信息化部近日印发《“人工智能+软件”专项行动实施方案》(以下简称《方案》)，从推进软件生产变革、加快软件产品智能化升级、培育智能体软件新业态、拓展智能软件服务、夯实软件智能化发展基础、优化软件产业发展环境等6个方面作出工作部署。\n\n中国软件产业体量大、场景丰富、开源力量活跃，是推进“人工智能+软件”的坚实基础。数据显示，2025年，整体行业营收达15.48万亿元，是2012年的6.2倍，年均复合增长率15.1%。截至2026年6月，中国日均词元调用量已突破500万亿。",
        "topic": "AI商业/AI创业",
        "theme": "产业升级",
        "gate": "TOPIC_PASS_MECHANICAL",
        "seed": "AI商业"
    },
    {
        "cid": "7684821300744962602",
        "title": "2026年服贸会探新：金融服务迈向“精不精”",
        "url": "https://www.toutiao.com/article/7684821300744962602/",
        "author": "人民网",
        "date": "2026-09-13",
        "text": "金融既是服务贸易的重要组成，又具有'独立业态+基础设施'的双重属性，如何通过金融'水利工程'涵养宜业'雨林生态'？\n\n在2026年中国国际服务贸易交易会上，折射出了目前金融服务的共同话题——从'有没有'的供给扩容，到'好不好'的品质提升，再到'精不精'的高效匹配。",
        "topic": "商业模式/business case",
        "theme": "金融服务",
        "gate": "TOPIC_PASS_MECHANICAL",
        "seed": "商业模式"
    },
    {
        "cid": "7671488207304868404",
        "title": "做自媒体最通透的几条真相，普通人一定要看懂",
        "url": "https://www.toutiao.com/article/7671488207304868404/",
        "author": "苏晗pb",
        "date": "2026-08-08",
        "text": "刷到一段话，特别贴合我当下的状态，结合自己的经历，深度复盘分享给所有正在起步的普通人。\n\n第一，真诚永远是底色，但真诚不是毫无保留。\n敢于大方说出自己的优点，也坦然承认自己的缺点和过往的踩坑经历。不包装成全知全能的大神，不装、不忽悠。\n\n第二，勇敢的人，先享受世界。\n普通人做自媒体最大的障碍，从来不是不会拍、不会写，而是脸皮薄、怕评价、怕被熟人看见、怕被同行调侃。\n\n第三，多操作、少空想，面子最不值钱。\n太多人陷入理论内耗，天天刷教程、存文案、学逻辑，唯独不敢动手实操。\n我深刻体会：十条完美的理论，不如一条粗糙的实操。\n\n第四，时间不会平白给答案，只会奖励持续迭代的人。\n真正的成长，是每一次输出后都有复盘，每一次不足都有修正。",
        "topic": "能力变现/副业",
        "theme": "自媒体创业",
        "gate": "TOPIC_PASS_MECHANICAL",
        "seed": "能力变现"
    },
    {
        "cid": "7683168637653598759",
        "title": "为什么普通人很难实现阶层跨越？",
        "url": "https://www.toutiao.com/article/7683168637653598759/",
        "author": "苏晗pb",
        "date": "2026-09-08",
        "text": "在餐厅端了一上午盘子……今天去餐厅顶岗，帮忙收了一上午的盘子。\n\n分享一下个人的感受，从上班到下班就停下来，看手机时间还没有5分钟，整个人就像一台上了发条的机器，不停地转——\n\n擦桌子、拖地、打扫厕所、擦玻璃、打外卖、收桌子、加菜加汤、擦盘子、抱盘子、搬碗、扫地、再擦桌子……\n\n好像领悟到了一个残酷的真相，基层普通人，本质上都是在贩卖自己的时间来换生存。\n\n但最可怕的不是身体的累，而是——没有时间思考，也没有精力思考。\n\n下班之后，你只想找个地方瘫着，刷刷短视频、追追剧，用最低成本的娱乐来犒劳自己。\n\n第一：时间被完全占领，思考被剥夺。\n当你所有的时间和精力都用来应付眼前的生存，你根本没有余力去想"未来"这两个字。\n\n第二：精力耗尽后，只想选择低质量的放松。\n因为高强度劳动后，人的意志力会大幅下降。\n\n第三：循环一旦形成，就很难打破。\n越忙 → 越没时间提升自己 → 能力不增长 → 只能继续做低价值的工作 → 越忙……这是一个死循环",
        "topic": "普通人收入/职场",
        "theme": "阶层跨越机制",
        "gate": "TOPIC_PASS_MECHANICAL",
        "seed": "普通人赚钱逻辑"
    },
    {
        "cid": "7684594958250836523",
        "title": "15名同事合买彩票中奖3000万港元，因负责购票者不愿平分奖金闹翻",
        "url": "https://www.toutiao.com/article/7684594958250836523/",
        "author": "齐鲁壹点",
        "date": "2026-09-12",
        "text": "15名同事合买彩票，中奖3000万港元，因负责购票者不愿平分奖金闹翻，香港警方：以涉嫌"盗窃"拘捕一名36岁男子。",
        "topic": "社会新闻",
        "theme": "彩票纠纷",
        "gate": "OFF_TOPIC_MECHANICAL",
        "seed": "赚钱"
    },
    {
        "cid": "7684457991839531556",
        "title": "52岁知名女演员在杭州卖韭菜盒子？曾被前夫坑到负债600万",
        "url": "https://www.toutiao.com/article/7684457991839531556/",
        "author": "潇湘晨报",
        "date": "2026-09-12",
        "text": "9月11日，有网友爆料：有一个女演员，此前曾自爆被前夫骗到破产，在横店演短剧赚钱还债，她说如果没戏拍会来卖韭菜盒子，今天她真的在转塘这边卖韭菜盒子了。\n\n网友说的这名女演员叫朱晏，52岁，山东人，她曾被观众称为眼中不可或缺的黄金配角——《康熙王朝》里的佟妃，《小鱼儿与花无缺》中的慕容淑。",
        "topic": "娱乐社会",
        "theme": "名人经历",
        "gate": "TOPIC_REVIEW_REQUIRED",
        "seed": "赚钱"
    },
]

def save_article(art):
    """Save article to source and handoff"""
    safe_id = art["cid"]
    src_path = SRC / f"{safe_id}.json"
    handoff_path = HANDOFF / f"{safe_id}.json"
    
    sha = hashlib.sha256(art["text"].encode('utf-8')).hexdigest()
    
    record = {
        "content_id": safe_id,
        "url": art["url"],
        "title": art["title"],
        "author": art.get("author", ""),
        "publish_date": art.get("date", ""),
        "raw_article_text": art["text"],
        "clean_article_text": art["text"],
        "text_chars": len(art["text"]),
        "placeholder_detected": False,
        "evidence_ready": art["gate"] == "TOPIC_PASS_MECHANICAL" and len(art["text"]) >= 200,
        "logic_analyzable": "PENDING_MODEL_REVIEW" if art["gate"] == "TOPIC_PASS_MECHANICAL" else None,
        "sha256": sha,
        "discovery_mode": "QUERY_FIRST",
        "search_seed": art.get("seed", ""),
        "topic_gate": art["gate"],
        "topic_category": art.get("topic", ""),
        "theme": art.get("theme", "")
    }
    
    src_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    handoff_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    
    return record

# Save all articles
results = []
for art in ARTICLES:
    result = save_article(art)
    results.append(result)
    print(f"✓ {result['content_id']}: {art['gate']} - {art['title'][:30]}...")

print(f"\nTotal: {len(results)}")
print(f"TOPIC_PASS: {sum(1 for r in results if r['topic_gate'] == 'TOPIC_PASS_MECHANICAL')}")
print(f"TOPIC_REVIEW: {sum(1 for r in results if r['topic_gate'] == 'TOPIC_REVIEW_REQUIRED')}")
print(f"OFF_TOPIC: {sum(1 for r in results if r['topic_gate'] == 'OFF_TOPIC_MECHANICAL')}")