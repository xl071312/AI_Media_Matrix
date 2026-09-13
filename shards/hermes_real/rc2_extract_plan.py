#!/usr/bin/env python3
"""RC2: Extract Real Fulltext for Wave001 (20 articles) via browser_console"""
import json
import csv
import hashlib
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
OUTPUT_DIR = BASE / "analysis_batches"
BATCH4 = OUTPUT_DIR / "batch_004_toutiao"
WAVE001_SRC = BATCH4 / "SEED_WAVE_001_REFETCH"
WAVE002_SRC = BATCH4 / "SEED_WAVE_002"
HANDOFF = BASE.parent / "handoff" / "chatgpt"

# All 20 Wave001 CIDs
WAVE001_CIDS = [
    "7591436947063702022", "7599942867901071906", "7605955836908814858",
    "7606730984955904531", "7610800331743707700", "7611009791036588590",
    "7626084420197401140", "7636648275394822719", "7641201117593895464",
    "7644625679841067560", "7645692141699662362", "7649646067054576147",
    "7651163686538658344", "7652293131710300706", "7652914429046178313",
    "7653685852405350948", "7655054577745674795", "7665187044485906946",
    "7674332815097414180", "7682745433508069888",
]

# Wave002 CIDs
WAVE002_CIDS = [
    "7684096740282171948", "7683548929375339037",
    "7683168637653598759", "7681510302478942759",
]

# Metadata (title, author, publish_time) - from browser_navigate results
METADATA = {
    "7591436947063702022": {"title": "姜胡说 实战干货：普通人逆袭的 5 个核心逻辑，从 0 到 1 跑通赚钱闭环", "author": "苏晗pb", "publish_time": "2026-01-04"},
    "7599942867901071906": {"title": "一个中年老男人到底适合做什么副业", "author": "王混乱", "publish_time": "2026-01-27"},
    "7605955836908814858": {"title": "2026开年冷思考：为什么你制定的年度战略，在AI面前像一张废纸", "author": "混沌学园", "publish_time": "2026-02-12"},
    "7606730984955904531": {"title": "AI制作动画短视频教程，零基础的我用AI副业赚钱", "author": "天雪聊历史", "publish_time": "2026-02-15"},
    "7610800331743707700": {"title": "2026年最稳副业：不摆摊不囤货，内容轻变现，零成本长期增收", "author": "在大地耕耘的勤作客", "publish_time": "2026-02-26"},
    "7611009791036588590": {"title": "2026 搞钱风口：别再瞎忙了，这 3 个行业将迎来爆发", "author": "民俗小馆", "publish_time": "2026-02-26"},
    "7626084420197401140": {"title": "AI副业指南：3天掌握AI绘画变现，月入5000+的实操攻略", "author": "咖啡屋随笔", "publish_time": "2026-04-08"},
    "7636648275394822719": {"title": "2026搞钱野路子：月入过万的冷门副业，有人靠说话就赚翻了", "author": "本草情报站", "publish_time": "2026-05-06"},
    "7641201117593895464": {"title": "2026至2040财富风口到来，普通人迎来翻身好机遇", "author": "星河赴梦", "publish_time": "2026-05-18"},
    "7644625679841067560": {"title": "2026下班兼职红黑榜：门槛越低，越要看清这几点", "author": "丸子说kuku", "publish_time": "2026-05-28"},
    "7645692141699662362": {"title": "副业收入超过主业：普通人可复制的3个轻资产模式", "author": "韩姐觉醒录", "publish_time": "2026-06-02"},
    "7649646067054576147": {"title": "2026年AI变现平台推荐：想通过AI接单赚钱，这6个平台值得关注", "author": "AI观察者", "publish_time": "2026-06-10"},
    "7651163686538658344": {"title": "下班后靠AI接单赚钱：试了5个平台，这3个最靠谱", "author": "", "publish_time": "2026-06-16"},
    "7652293131710300706": {"title": "1000种副业：017-闲鱼实物倒卖", "author": "素书", "publish_time": "2026-06-17"},
    "7652914429046178313": {"title": "普通人刷遍各类致富干货依旧赚不到钱，根源不在努力而在认知闭环", "author": "夜雨十年", "publish_time": "2026-06-19"},
    "7653685852405350948": {"title": "2026年，普通人用AI提效的完整实战指南", "author": "博学的饼干k88VG", "publish_time": "2026-06-21"},
    "7655054577745674795": {"title": "中国团队靠AI卖课出海，赚美元快钱的门道，你敢信？", "author": "译海领读", "publish_time": "2026-06-25"},
    "7665187044485906946": {"title": "别人靠AI表情包月入9000，普通人用豆包就能复刻，零门槛副业拆解", "author": "富伟尧原", "publish_time": "2026-07-22"},
    "7674332815097414180": {"title": "闲鱼不只是二手平台，爆增981万AI订单，普通人入局副业有机会", "author": "世相派", "publish_time": "2026-08-16"},
    "7682745433508069888": {"title": "你还怕AI抢工作？有人已经用AI在闲鱼上赚翻了", "author": "小刘论评", "publish_time": "2026-09-07"},
}

print("="*70)
print("RC2: Batch Fulltext Extraction via browser_console")
print("="*70)
print()
print("NOTE: This script generates extraction commands.")
print("      Manual browser_console calls will be made per article.")
print()

# Print extraction JS code
EXTRACT_JS = """(() => { const article = document.querySelector('article') || document.querySelector('[class*="article"]') || document.querySelector('[class*="content"]'); return article ? article.innerText : document.body.innerText.substring(0, 50000); })()"""

for cid in WAVE001_CIDS:
    meta = METADATA.get(cid, {})
    title = meta.get('title', 'UNKNOWN')
    print(f"--- Wave001: {cid}")
    print(f"Title: {title[:50]}...")
    print(f"browser_navigate: https://www.toutiao.com/article/{cid}/")
    print(f"browser_console expression: {EXTRACT_JS[:80]}...")
    print()

print("="*70)
print("After extraction, update JSON with real content")
print("="*70)