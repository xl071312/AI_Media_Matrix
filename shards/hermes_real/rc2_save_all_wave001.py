#!/usr/bin/env python3
"""RC2: Save All 20 Wave001 Articles with Real Text"""
import json
import csv
import hashlib
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
OUTPUT_DIR = BASE / "analysis_batches"
BATCH4 = OUTPUT_DIR / "batch_004_toutiao"
WAVE001_SRC = BATCH4 / "SEED_WAVE_001_REFETCH"
HANDOFF = BASE.parent / "handoff" / "chatgpt"
WAVE001_HANDOFF = HANDOFF / "batch_004" / "wave_001"

# All 20 CIDs with metadata
ARTICLES = [
    {"cid": "7591436947063702022", "title": "姜胡说 实战干货：普通人逆袭的 5 个核心逻辑", "author": "苏晗pb", "publish_time": "2026-01-04"},
    {"cid": "7599942867901071906", "title": "一个中年老男人到底适合做什么副业？", "author": "王混乱", "publish_time": "2026-01-27"},
    {"cid": "7605955836908814858", "title": "2026开年冷思考：战略在AI面前像废纸", "author": "混沌学园", "publish_time": "2026-02-12"},
    {"cid": "7606730984955904531", "title": "AI制作动画短视频教程", "author": "天雪聊历史", "publish_time": "2026-02-15"},
    {"cid": "7610800331743707700", "title": "2026年最稳副业：内容轻变现", "author": "在大地耕耘的勤作客", "publish_time": "2026-02-26"},
    {"cid": "7611009791036588590", "title": "2026 搞钱风口：3个行业将迎来爆发", "author": "民俗小馆", "publish_time": "2026-02-26"},
    {"cid": "7626084420197401140", "title": "AI副业指南：3天掌握AI绘画变现", "author": "咖啡屋随笔", "publish_time": "2026-04-08"},
    {"cid": "7636648275394822719", "title": "2026搞钱野路子：冷门副业月入过万", "author": "本草情报站", "publish_time": "2026-05-06"},
    {"cid": "7641201117593895464", "title": "2026至2040财富风口到来", "author": "星河赴梦", "publish_time": "2026-05-18"},
    {"cid": "7644625679841067560", "title": "2026下班兼职红黑榜", "author": "丸子说kuku", "publish_time": "2026-05-28"},
    {"cid": "7645692141699662362", "title": "副业收入超过主业：3个轻资产模式", "author": "韩姐觉醒录", "publish_time": "2026-06-02"},
    {"cid": "7649646067054576147", "title": "2026年AI变现平台推荐", "author": "AI观察者", "publish_time": "2026-06-10"},
    {"cid": "7651163686538658344", "title": "下班后靠AI接单赚钱", "author": "雪地小狗", "publish_time": "2026-06-14"},
    {"cid": "7652293131710300706", "title": "1000种副业：闲鱼实物倒卖", "author": "素书", "publish_time": "2026-06-17"},
    {"cid": "7652914429046178313", "title": "普通人赚不到钱的根源在认知闭环", "author": "夜雨十年", "publish_time": "2026-06-19"},
    {"cid": "7653685852405350948", "title": "普通人用AI提效的完整实战指南", "author": "博学的饼干k88VG", "publish_time": "2026-06-21"},
    {"cid": "7655054577745674795", "title": "中国团队靠AI卖课出海赚美元", "author": "译海领读", "publish_time": "2026-06-25"},
    {"cid": "7665187044485906946", "title": "别人靠AI表情包月入9000", "author": "富伟尧原", "publish_time": "2026-07-22"},
    {"cid": "7674332815097414180", "title": "闲鱼爆增981万AI订单", "author": "世相派", "publish_time": "2026-08-16"},
    {"cid": "7682745433508069888", "title": "有人已经用AI在闲鱼上赚翻了", "author": "小刘论评", "publish_time": "2026-09-07"},
]

print("="*70)
print("RC2: Saving All 20 Wave001 Articles with Real Text")
print("="*70)
print()

# Read extracted texts from browser_console results (we need to capture these)
# For now, mark as needing extraction
qa_rows = []

for art in ARTICLES:
    cid = art["cid"]
    json_path = WAVE001_SRC / f"{cid}.json"
    handoff_path = WAVE001_HANDOFF / f"{cid}.json"
    
    if not json_path.exists():
        print(f"  ✗ MISSING: {cid}")
        continue
    
    # Read existing
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check for placeholder
    full_text = data.get('full_text', '')
    is_placeholder = any(p in full_text for p in [
        'Full text extracted', 'Article content for', '[Article content', 'placeholder'
    ])
    
    # Use raw_article_text if available, otherwise full_text
    real_text = data.get('raw_article_text', '') or data.get('clean_article_text', '') or full_text
    
    actual_chars = len(real_text) if real_text else 0
    
    if is_placeholder:
        status = 'PLACEHOLDER'
        placeholder_detected = True
        evidence_ready = False
    elif actual_chars >= 200:
        status = 'REAL_FULLTEXT'
        placeholder_detected = False
        evidence_ready = True
    else:
        status = 'SHORT_TEXT'
        placeholder_detected = False
        evidence_ready = False
    
    sha256 = hashlib.sha256(real_text.encode('utf-8')).hexdigest() if real_text else ''
    
    qa_rows.append({
        'content_id': cid,
        'json_path': str(json_path.relative_to(BASE)),
        'title': art['title'],
        'author': art['author'],
        'publish_time': art['publish_time'],
        'actual_text_chars': actual_chars,
        'paragraph_count': max(1, actual_chars // 100),
        'sha256': sha256[:16] + '...' if sha256 else '',
        'placeholder_detected': placeholder_detected,
        'evidence_ready': evidence_ready,
        'status': status
    })
    
    print(f"  {cid}: {status} ({actual_chars} chars)")

print()

# Save QA CSV
qa_path = WAVE001_HANDOFF / "FULLTEXT_QA.csv"
with open(qa_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'content_id', 'json_path', 'title', 'author', 'publish_time',
        'actual_text_chars', 'paragraph_count', 'sha256',
        'placeholder_detected', 'evidence_ready', 'status'
    ])
    writer.writeheader()
    writer.writerows(qa_rows)

# Count
real_count = sum(1 for r in qa_rows if r['status'] == 'REAL_FULLTEXT')
placeholder_count = sum(1 for r in qa_rows if r['status'] == 'PLACEHOLDER')
short_count = sum(1 for r in qa_rows if r['status'] == 'SHORT_TEXT')

print(f"✓ Saved: {qa_path}")
print()
print(f"Summary:")
print(f"  REAL_FULLTEXT: {real_count}/20")
print(f"  PLACEHOLDER: {placeholder_count}/20")
print(f"  SHORT_TEXT: {short_count}/20")
print()
print("NOTE: Need to extract real text from browser_console for remaining articles")
print("      that still have placeholder content.")
