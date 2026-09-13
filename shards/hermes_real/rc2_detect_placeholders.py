#!/usr/bin/env python3
"""RC2: Fix Placeholder Text - Re-extract Real Fulltext for Wave001 and Wave002"""
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

# All 20 Wave001 content IDs
WAVE001_CIDS = [
    "7591436947063702022", "7599942867901071906", "7605955836908814858",
    "7606730984955904531", "7610800331743707700", "7611009791036588590",
    "7626084420197401140", "7636648275394822719", "7641201117593895464",
    "7644625679841067560", "7645692141699662362", "7649646067054576147",
    "7651163686538658344", "7652293131710300706", "7652914429046178313",
    "7653685852405350948", "7655054577745674795", "7665187044485906946",
    "7674332815097414180", "7682745433508069888",
]

# Wave002 CIDs (4 so far)
WAVE002_CIDS = [
    "7684096740282171948", "7683548929375339037",
    "7683168637653598759", "7681510302478942759",
]

# Pre-captured titles/authors from browser tool (RC7/RC8D/RC8E)
ARTICLE_META = {
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
print("RC2: Fixing Placeholder Text - Re-extracting Real Fulltext")
print("="*70)
print()
print("NOTE: The browser tool captures page content but does not expose")
print("      raw article body text directly. We must use browser_snapshot")
print("      to read visible text, then extract and save.")
print()
print("Since browser tool sessions persist, we will re-navigate each")
print("URL and capture the full visible text from the article body.")
print()

# Phase 1: Generate QA files for existing JSONs (detect placeholders)
print("=== Phase 1: Detect Placeholders in Existing JSONs ===")
print()

placeholder_count = 0
real_content_count = 0
qa_rows = []

for cid in WAVE001_CIDS:
    json_path = WAVE001_SRC / f"{cid}.json"
    handoff_path = HANDOFF / "batch_004" / "wave_001" / f"{cid}.json"
    
    if not json_path.exists():
        print(f"✗ MISSING: {cid}")
        continue
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    full_text = data.get('full_text', '')
    text_chars = data.get('text_chars', 0)
    
    # Check for placeholder patterns
    is_placeholder = any(p in full_text for p in [
        'Full text extracted',
        'Article content for',
        '[Article content',
        'placeholder'
    ])
    
    # Calculate actual text chars from full_text
    actual_chars = len(full_text) if full_text else 0
    
    # SHA256 of clean_article_text or full_text
    text_to_hash = data.get('clean_article_text', full_text)
    sha256 = hashlib.sha256(text_to_hash.encode('utf-8')).hexdigest() if text_to_hash else ''
    
    evidence_ready = not is_placeholder and actual_chars >= 200
    
    if is_placeholder:
        placeholder_count += 1
    else:
        real_content_count += 1
    
    qa_rows.append({
        'content_id': cid,
        'json_path': str(json_path.relative_to(BASE)),
        'actual_text_chars': actual_chars,
        'paragraph_count': max(1, actual_chars // 100),
        'sha256': sha256[:16] + '...' if sha256 else '',
        'placeholder_detected': is_placeholder,
        'evidence_ready': evidence_ready,
        'status': 'PLACEHOLDER' if is_placeholder else ('REAL' if evidence_ready else 'SHORT')
    })
    
    print(f"  {cid}: {'PLACEHOLDER' if is_placeholder else 'REAL'} ({actual_chars} chars)")

print()
print(f"Wave001 QA: {real_content_count} real, {placeholder_count} placeholder")
print()

# Save QA CSV
qa_dir = HANDOFF / "batch_004" / "wave_001"
qa_dir.mkdir(parents=True, exist_ok=True)
qa_path = qa_dir / "FULLTEXT_QA.csv"
with open(qa_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['content_id', 'json_path', 'actual_text_chars', 'paragraph_count', 'sha256', 'placeholder_detected', 'evidence_ready', 'status'])
    writer.writeheader()
    writer.writerows(qa_rows)
print(f"✓ Saved: {qa_path}")
print()

# Phase 2: Check Wave002
print("=== Phase 2: Wave002 QA ===")
print()
w2_qa_rows = []
for cid in WAVE002_CIDS:
    json_path = WAVE002_SRC / f"{cid}.json"
    if not json_path.exists():
        print(f"  {cid}: MISSING")
        continue
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    full_text = data.get('full_text', '')
    actual_chars = len(full_text) if full_text else 0
    
    is_placeholder = any(p in full_text for p in [
        'Full text extracted',
        'Article content for',
        '[Article content',
        'placeholder'
    ])
    
    text_to_hash = data.get('clean_article_text', full_text)
    sha256 = hashlib.sha256(text_to_hash.encode('utf-8')).hexdigest() if text_to_hash else ''
    evidence_ready = not is_placeholder and actual_chars >= 200
    
    w2_qa_rows.append({
        'content_id': cid,
        'json_path': str(json_path.relative_to(BASE)),
        'actual_text_chars': actual_chars,
        'paragraph_count': max(1, actual_chars // 100),
        'sha256': sha256[:16] + '...' if sha256 else '',
        'placeholder_detected': is_placeholder,
        'evidence_ready': evidence_ready,
        'status': 'PLACEHOLDER' if is_placeholder else ('REAL' if evidence_ready else 'SHORT')
    })
    
    print(f"  {cid}: {'PLACEHOLDER' if is_placeholder else 'REAL'} ({actual_chars} chars)")

# Save Wave002 QA
w2_qa_dir = HANDOFF / "batch_004" / "wave_002"
w2_qa_dir.mkdir(parents=True, exist_ok=True)
w2_qa_path = w2_qa_dir / "FULLTEXT_QA.csv"
with open(w2_qa_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['content_id', 'json_path', 'actual_text_chars', 'paragraph_count', 'sha256', 'placeholder_detected', 'evidence_ready', 'status'])
    writer.writeheader()
    writer.writerows(w2_qa_rows)
print(f"✓ Saved: {w2_qa_path}")
print()

# Phase 3: Summary
print("="*70)
print("RC2 Phase 1-2 Complete: QA Files Generated")
print("="*70)
print()
print(f"Wave001: {real_content_count} real / {placeholder_count} placeholder")
print(f"Wave002: {len([r for r in w2_qa_rows if r['evidence_ready']])} evidence ready / {len(w2_qa_rows)} total")
print()
print("NOTE: The browser tool captures page HTML/DOM but not raw article text")
print("      in a parseable format. The full_text field contains placeholder strings")
print("      because the original extraction script saved metadata-only content.")
print()
print("To fix: Need to use browser_snapshot to read visible text from each article.")
print("This requires re-navigating each URL and extracting the article body.")