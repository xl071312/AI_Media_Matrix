#!/usr/bin/env python3
"""RC2: Wave001 Fulltext Status Check"""
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

WAVE001_CIDS = [
    "7591436947063702022", "7599942867901071906", "7605955836908814858",
    "7606730984955904531", "7610800331743707700", "7611009791036588590",
    "7626084420197401140", "7636648275394822719", "7641201117593895464",
    "7644625679841067560", "7645692141699662362", "7649646067054576147",
    "7651163686538658344", "7652293131710300706", "7652914429046178313",
    "7653685852405350948", "7655054577745674795", "7665187044485906946",
    "7674332815097414180", "7682745433508069888",
]

METADATA = {
    "7591436947063702022": {"title": "姜胡说 实战干货：普通人逆袭的 5 个核心逻辑", "author": "苏晗pb", "publish_time": "2026-01-04"},
    "7599942867901071906": {"title": "一个中年老男人到底适合做什么副业？", "author": "王混乱", "publish_time": "2026-01-27"},
    "7605955836908814858": {"title": "2026开年冷思考：战略在AI面前像废纸", "author": "混沌学园", "publish_time": "2026-02-12"},
    "7606730984955904531": {"title": "AI制作动画短视频教程", "author": "天雪聊历史", "publish_time": "2026-02-15"},
    "7610800331743707700": {"title": "2026年最稳副业：内容轻变现", "author": "在大地耕耘的勤作客", "publish_time": "2026-02-26"},
    "7611009791036588590": {"title": "2026 搞钱风口：3个行业将迎来爆发", "author": "民俗小馆", "publish_time": "2026-02-26"},
    "7626084420197401140": {"title": "AI副业指南：3天掌握AI绘画变现", "author": "咖啡屋随笔", "publish_time": "2026-04-08"},
    "7636648275394822719": {"title": "2026搞钱野路子：冷门副业月入过万", "author": "本草情报站", "publish_time": "2026-05-06"},
    "7641201117593895464": {"title": "2026至2040财富风口到来", "author": "星河赴梦", "publish_time": "2026-05-18"},
    "7644625679841067560": {"title": "2026下班兼职红黑榜", "author": "丸子说kuku", "publish_time": "2026-05-28"},
    "7645692141699662362": {"title": "副业收入超过主业：3个轻资产模式", "author": "韩姐觉醒录", "publish_time": "2026-06-02"},
    "7649646067054576147": {"title": "2026年AI变现平台推荐", "author": "AI观察者", "publish_time": "2026-06-10"},
    "7651163686538658344": {"title": "下班后靠AI接单赚钱", "author": "", "publish_time": "2026-06-16"},
    "7652293131710300706": {"title": "1000种副业：闲鱼实物倒卖", "author": "素书", "publish_time": "2026-06-17"},
    "7652914429046178313": {"title": "普通人赚不到钱的根源在认知闭环", "author": "夜雨十年", "publish_time": "2026-06-19"},
    "7653685852405350948": {"title": "普通人用AI提效的完整实战指南", "author": "博学的饼干k88VG", "publish_time": "2026-06-21"},
    "7655054577745674795": {"title": "中国团队靠AI卖课出海赚美元", "author": "译海领读", "publish_time": "2026-06-25"},
    "7665187044485906946": {"title": "别人靠AI表情包月入9000", "author": "富伟尧原", "publish_time": "2026-07-22"},
    "7674332815097414180": {"title": "闲鱼爆增981万AI订单", "author": "世相派", "publish_time": "2026-08-16"},
    "7682745433508069888": {"title": "有人已经用AI在闲鱼上赚翻了", "author": "小刘论评", "publish_time": "2026-09-07"},
}

print("="*70)
print("RC2: Wave001 Fulltext Status Check")
print("="*70)
print()

qa_rows = []
extracted_count = 0
placeholder_count = 0
missing_count = 0

for cid in WAVE001_CIDS:
    json_path = WAVE001_SRC / f"{cid}.json"
    
    if not json_path.exists():
        missing_count += 1
        print(f"  MISSING: {cid}")
        continue
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    full_text = data.get('full_text', '')
    real_text = data.get('raw_article_text', '') or data.get('clean_article_text', '')
    
    is_placeholder = any(p in full_text for p in [
        'Full text extracted', 'Article content for', '[Article content', 'placeholder'
    ])
    
    actual_text = real_text if real_text else full_text
    actual_chars = len(actual_text) if actual_text else 0
    
    if actual_text and not is_placeholder and actual_chars >= 200:
        sha256 = hashlib.sha256(actual_text.encode('utf-8')).hexdigest()
        status = 'REAL_FULLTEXT'
        extracted_count += 1
    elif is_placeholder:
        sha256 = hashlib.sha256(full_text.encode('utf-8')).hexdigest() if full_text else ''
        status = 'PLACEHOLDER'
        placeholder_count += 1
    else:
        sha256 = hashlib.sha256(actual_text.encode('utf-8')).hexdigest() if actual_text else ''
        status = 'UNKNOWN'
    
    meta = METADATA.get(cid, {})
    
    qa_rows.append({
        'content_id': cid,
        'json_path': str(json_path.relative_to(BASE)),
        'title': meta.get('title', 'UNKNOWN'),
        'author': meta.get('author', 'UNKNOWN'),
        'actual_text_chars': actual_chars,
        'paragraph_count': max(1, actual_chars // 100),
        'sha256': sha256[:16] + '...' if sha256 else '',
        'placeholder_detected': is_placeholder,
        'evidence_ready': not is_placeholder and actual_chars >= 200,
        'status': status
    })
    
    print(f"  {cid}: {status} ({actual_chars} chars)")

print()
print(f"Summary:")
print(f"  Real Fulltext: {extracted_count}/20")
print(f"  Placeholder: {placeholder_count}/20")
print(f"  Missing: {missing_count}/20")
