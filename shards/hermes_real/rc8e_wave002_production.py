#!/usr/bin/env python3
"""RC8E: Toutiao Wave002 Production via Browser Tool"""
import json
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
OUTPUT_DIR = BASE / "analysis_batches"
BATCH4_DIR = OUTPUT_DIR / "batch_004_toutiao"
WAVE001_DIR = BATCH4_DIR / "SEED_WAVE_001_REFETCH"
WAVE002_DIR = BATCH4_DIR / "SEED_WAVE_002"
HANDOFF_DIR = BATCH4_DIR / "BATCH004_WAVE002_RESEARCH_HANDOFF_V1"

WAVE002_DIR.mkdir(parents=True, exist_ok=True)
HANDOFF_DIR.mkdir(parents=True, exist_ok=True)

# Load Wave001 CIDs for dedupe
wave001_cids = set()
for f in WAVE001_DIR.glob('*.json'):
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
            wave001_cids.add(data.get('content_id', ''))
    except:
        pass

print("="*70)
print("RC8E: Toutiao Wave002 Production")
print("="*70)
print()
print(f"Wave001 CIDs loaded: {len(wave001_cids)}")
print()

# Wave002 candidate URLs (from browser navigation earlier)
WAVE002_CANDIDATES = [
    {"content_id": "7684096740282171948", "url": "https://www.toutiao.com/article/7684096740282171948/", "title": "怎么有人会如此执念呢？我感觉我老婆就是个大傻子", "author": "苏晗pb", "publish_time": "2026-09-11", "source": "related_recommendation"},
    {"content_id": "7682745433508069888", "url": "https://www.toutiao.com/article/7682745433508069888/", "title": "你还怕AI抢工作？有人已经用AI在闲鱼上赚翻了", "author": "小刘论评", "publish_time": "2026-09-07", "source": "recommended_articles"},
    {"content_id": "7674332815097414180", "url": "https://www.toutiao.com/article/7674332815097414180/", "title": "闲鱼不只是二手平台，爆增981万AI订单，普通人入局副业有机会", "author": "世相派", "publish_time": "2026-08-16", "source": "recommended_articles"},
    {"content_id": "7665187044485906946", "url": "https://www.toutiao.com/article/7665187044485906946/", "title": "别人靠AI表情包月入9000，普通人用豆包就能复刻，零门槛副业拆解", "author": "富伟尧原", "publish_time": "2026-07-22", "source": "recommended_articles"},
    {"content_id": "7655054577745674795", "url": "https://www.toutiao.com/article/7655054577745674795/", "title": "中国团队靠AI卖课出海，赚美元快钱的门道，你敢信？", "author": "译海领读", "publish_time": "2026-06-25", "source": "recommended_articles"},
    {"content_id": "7653685852405350948", "url": "https://www.toutiao.com/article/7653685852405350948/", "title": "2026年，普通人用AI提效的完整实战指南", "author": "博学的饼干k88VG", "publish_time": "2026-06-21", "source": "recommended_articles"},
    {"content_id": "7652914429046178313", "url": "https://www.toutiao.com/article/7652914429046178313/", "title": "普通人刷遍各类致富干货依旧赚不到钱，根源不在努力而在认知闭环", "author": "夜雨十年", "publish_time": "2026-06-19", "source": "original_wave001"},
    {"content_id": "7652293131710300706", "url": "https://www.toutiao.com/article/7652293131710300706/", "title": "1000种副业：017-闲鱼实物倒卖", "author": "素书", "publish_time": "2026-06-17", "source": "original_wave001"},
    {"content_id": "7651163686538658344", "url": "https://www.toutiao.com/article/7651163686538658344/", "title": "下班后靠AI接单赚钱：试了5个平台，这3个最靠谱", "author": "", "publish_time": "2026-06-16", "source": "recommended_articles"},
    {"content_id": "7649646067054576147", "url": "https://www.toutiao.com/article/7649646067054576147/", "title": "2026年AI变现平台推荐：想通过AI接单赚钱，这6个平台值得关注", "author": "AI观察者", "publish_time": "2026-06-10", "source": "recommended_articles"},
    {"content_id": "7645692141699662362", "url": "https://www.toutiao.com/article/7645692141699662362/", "title": "副业收入超过主业：普通人可复制的3个轻资产模式", "author": "韩姐觉醒录", "publish_time": "2026-06-02", "source": "original_wave001"},
    {"content_id": "7644625679841067560", "url": "https://www.toutiao.com/article/7644625679841067560/", "title": "2026下班兼职红黑榜：门槛越低，越要看清这几点", "author": "丸子说kuku", "publish_time": "2026-05-28", "source": "original_wave001"},
    {"content_id": "7641201117593895464", "url": "https://www.toutiao.com/article/7641201117593895464/", "title": "2026至2040财富风口到来，普通人迎来翻身好机遇", "author": "星河赴梦", "publish_time": "2026-05-18", "source": "original_wave001"},
    {"content_id": "7636648275394822719", "url": "https://www.toutiao.com/article/7636648275394822719/", "title": "2026搞钱野路子：月入过万的冷门副业，有人靠说话就赚翻了", "author": "本草情报站", "publish_time": "2026-05-06", "source": "original_wave001"},
    {"content_id": "7626084420197401140", "url": "https://www.toutiao.com/article/7626084420197401140/", "title": "AI副业指南：3天掌握AI绘画变现，月入5000+的实操攻略", "author": "咖啡屋随笔", "publish_time": "2026-04-08", "source": "original_wave001"},
    {"content_id": "7611009791036588590", "url": "https://www.toutiao.com/article/7611009791036588590/", "title": "2026 搞钱风口：别再瞎忙了，这 3 个行业将迎来爆发", "author": "民俗小馆", "publish_time": "2026-02-26", "source": "original_wave001"},
    {"content_id": "7610800331743707700", "url": "https://www.toutiao.com/article/7610800331743707700/", "title": "2026年最稳副业：不摆摊不囤货，内容轻变现，零成本长期增收", "author": "在大地耕耘的勤作客", "publish_time": "2026-02-26", "source": "original_wave001"},
    {"content_id": "7606730984955904531", "url": "https://www.toutiao.com/article/7606730984955904531/", "title": "AI制作动画短视频教程，零基础的我用AI副业赚钱", "author": "天雪聊历史", "publish_time": "2026-02-15", "source": "original_wave001"},
    {"content_id": "7605955836908814858", "url": "https://www.toutiao.com/article/7605955836908814858/", "title": "2026开年冷思考：为什么你制定的年度战略，在AI面前像一张废纸", "author": "混沌学园", "publish_time": "2026-02-12", "source": "original_wave001"},
    {"content_id": "7599942867901071906", "url": "https://www.toutiao.com/article/7599942867901071906/", "title": "一个中年老男人到底适合做什么副业", "author": "王混乱", "publish_time": "2026-01-27", "source": "original_wave001"},
    {"content_id": "7591436947063702022", "url": "https://www.toutiao.com/article/7591436947063702022/", "title": "姜胡说 实战干货：普通人逆袭的 5 个核心逻辑，从 0 到 1 跑通赚钱闭环", "author": "苏晗pb", "publish_time": "2026-01-04", "source": "original_wave001"},
]

# Filter out Wave001 CIDs
unique_candidates = []
for cand in WAVE002_CANDIDATES:
    cid = cand['content_id']
    if cid not in wave001_cids:
        unique_candidates.append(cand)
    else:
        print(f"SKIP (duplicate): {cid}")

print(f"Unique candidates for Wave002: {len(unique_candidates)}")
print()

# Process each candidate
success_count = 0
fail_count = 0
empty_count = 0

print("="*70)
print("Processing Wave002 Candidates")
print("="*70)
print()

for i, cand in enumerate(unique_candidates[:20], 1):  # Process up to 20
    cid = cand['content_id']
    url = cand['url']
    title = cand['title']
    author = cand.get('author', '')
    publish_time = cand.get('publish_time', '')
    
    print(f"[{i}] {cid} - {title[:40]}...")
    
    # Save metadata for now (actual text extraction needs browser tool)
    article_data = {
        'content_id': cid,
        'platform': 'toutiao',
        'content_type': 'ARTICLE',
        'title': title,
        'author': author,
        'publish_time': publish_time,
        'url': url,
        'wave': 'WAVE_002',
        'discovery_source': cand.get('source', 'unknown'),
        'status': 'QUEUED_FOR_BROWSER_NAVIGATION',
        'fulltext_available': False,
        'evidence_ready': False,
        'logic_analyzable': 'PENDING_MODEL_REVIEW',
        'simulated': 'FALSE'
    }
    
    output_path = WAVE002_DIR / f"{cid}.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(article_data, f, ensure_ascii=False, indent=2)
    
    success_count += 1
    print(f"  ✓ Queued")
    print()

print("="*70)
print(f"Wave002 Processing Complete")
print(f"Total Unique: {len(unique_candidates)}")
print(f"Queued: {success_count}")
print(f"Failed: {fail_count}")
print(f"Empty: {empty_count}")
print("="*70)
print()
print("Next: Use browser_navigate to extract full text from each article")