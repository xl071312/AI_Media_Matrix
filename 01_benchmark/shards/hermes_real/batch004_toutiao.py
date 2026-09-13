#!/usr/bin/env python3
"""Batch 004 Toutiao - Production Pipeline"""
import csv
import json
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright
from faster_whisper import WhisperModel
import subprocess
import urllib.request
import ssl

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH4_DIR = BASE / "analysis_batches" / "batch_004_toutiao"
MEDIA_DIR = BASE / "media" / "batch_004_toutiao"
TRANSCRIPT_DIR = SHARDS / "transcripts_v2"

# Create dirs
BATCH4_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Load registry with global keys
reg_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
registry = {}
with open(reg_path, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        cid = row.get('content_id', '').strip().lstrip('\ufeff')
        if cid:
            registry[cid] = row

print(f"=== BATCH 004 TOUTIAO PRODUCTION ===")
print(f"Registry entries: {len(registry)}")
print()

# Load existing progress
existing_path = BATCH4_DIR / "batch004_progress.json"
existing_results = []
if existing_path.exists():
    with open(existing_path, 'r', encoding='utf-8') as f:
        existing_results = json.load(f)
done_cids = set(r.get('content_id', '') for r in existing_results)

print(f"Already done: {len(done_cids)}")
print()

# Topic keywords for Batch004
PRIORITY_TOPICS = {
    '赚钱逻辑': ['赚钱', '搞钱', '财富', '收入', '金钱', '资本', '暴富'],
    '能力变现': ['变现', '副业', '技能', '个人成长', '时间管理'],
    '普通人收入': ['收入', '工资', '月薪', '年薪', '普通人', '翻身', '逆袭'],
    '职场收入': ['职场', '打工', '升职', '加薪', '跳槽', '面试'],
    '信息差': ['信息差', '认知', '思维', '知识', '茧房', '差距'],
    'AI赚钱': ['AI', '人工智能', '豆包', 'ChatGPT', '大模型'],
    '商业思维': ['商业', '生意', '模式', '盈利', '赛道'],
    '创业失败': ['失败', '踩坑', '避坑', '教训', '反思'],
    '消费认知': ['消费观', '理性消费', '省钱', '存钱', '财务自由'],
    '中产焦虑': ['中产', '焦虑', '返贫', '房贷'],
}
OFF_MARKERS = ['游戏', '攻略', '三角洲', '原神', '动漫', '短剧', '美食', '健身', 
               '宠物', '旅游', '美妆', '穿搭', '数码', '汽车', '音乐', '搞笑', '电影', '明星',
               '体育', '娱乐', '八卦', '明星']

def is_toutiao_article(title, keyword=""):
    """Check if content is on-topic for Toutiao"""
    text = f"{title} {keyword}".lower()
    # Filter off-topic
    for m in OFF_MARKERS:
        if m in text:
            return False
    # Check for topic markers
    for topic_keywords in PRIORITY_TOPICS.values():
        if any(kw in text for kw in topic_keywords):
            return True
    return False

def classify_toutiao_topic(title, keyword=""):
    """Classify topic for Toutiao content"""
    text = f"{title} {keyword}".lower()
    for topic, keywords in PRIORITY_TOPICS.items():
        if any(kw in text for kw in keywords):
            return topic
    return 'GENERAL'

# Try to get Toutiao candidates from existing data
# Since we don't have direct Toutiao API, we'll search for topics via browser

# Load model
model = WhisperModel('Systran/faster-whisper-tiny', device='cpu', compute_type='int8')
print("Model loaded\n")

results = list(existing_results)
processed = 0

# Search strategies for Toutiao
search_queries = [
    # 赚钱逻辑
    "赚钱思维 认知",
    "副业赚钱方法",
    "普通人如何赚钱",
    # 能力变现
    "技能变现教程",
    "副业收入分享",
    # 职场收入
    "职场升职加薪",
    "打工人的出路",
    # AI赚钱
    "AI赚钱方法",
    "ChatGPT副业",
    # 创业失败
    "创业失败教训",
    "避坑指南",
    # 信息差
    "信息差赚钱",
    "认知提升",
    # 消费认知
    "消费主义陷阱",
    "理性消费",
]

print("Starting Toutiao search and collection...")
print()

for i, query in enumerate(search_queries, 1):
    print(f"[{i}] Searching: {query}")
    
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    context = browser.contexts[0]
    page = context.new_page()
    
    try:
        # Navigate to Toutiao search
        search_url = f'https://www.toutiao.com/search?keyword={query}'
        page.goto(search_url, timeout=20000)
        time.sleep(3)
        
        # Get page content
        content = page.content()
        
        # Extract article links
        articles = page.evaluate('''() => {
            const links = document.querySelectorAll('a[href*="toutiao.com/a"]');
            return Array.from(links).map(a => ({
                href: a.href,
                text: a.textContent.trim().substring(0, 100)
            }));
        }''')
        
        # Filter unique and valid
        unique_links = set()
        for art in articles:
            if art['href'] and 'toutiao.com' in art['href']:
                # Extract content_id from URL
                cid_match = art['href'].split('/')[-1].replace('.html', '')
                if cid_match.isdigit() and cid_match not in unique_links and cid_match not in done_cids:
                    unique_links.add(cid_match)
        
        print(f"  Found {len(unique_links)} unique articles")
        
        # Process first 2 articles per query
        for cid in list(unique_links)[:2]:
            if cid in done_cids:
                continue
            
            print(f"    Processing: {cid}")
            
            # Get article details
            article_url = f'https://www.toutiao.com/article/{cid}/'
            page.goto(article_url, timeout=20000)
            time.sleep(2)
            
            # Extract metadata
            meta = page.evaluate('''() => {
                const titleEl = document.querySelector('.article-title, h1, .title');
                const authorEl = document.querySelector('.author-name, .source a');
                const contentEl = document.querySelector('.article-content, .content, [class*="article"]');
                
                return {
                    title: titleEl ? titleEl.textContent.trim() : '',
                    author: authorEl ? authorEl.textContent.trim() : '',
                    content: contentEl ? contentEl.textContent.trim().substring(0, 5000) : ''
                };
            }''')
            
            if not meta['title']:
                print(f"    ✗ No title found")
                continue
            
            # Check topic
            if not is_toutiao_article(meta['title']):
                print(f"    ✗ Off-topic")
                continue
            
            topic = classify_toutiao_topic(meta['title'])
            print(f"    ✓ Topic: {topic}")
            
            # Save article data
            article_data = {
                'content_id': cid,
                'platform': 'toutiao',
                'content_type': 'ARTICLE',
                'title': meta['title'],
                'author': meta['author'],
                'primary_topic': topic,
                'full_text': meta['content'],
                'text_chars': len(meta['content']),
                'status': 'DOWNLOADED'
            }
            
            # Save to file
            article_path = MEDIA_DIR / f'{cid}.json'
            article_path.write_text(json.dumps(article_data, ensure_ascii=False, indent=2))
            
            results.append({
                'content_id': cid,
                'platform': 'toutiao',
                'content_type': 'ARTICLE',
                'title': meta['title'],
                'primary_topic': topic,
                'status': 'DOWNLOADED',
                'text_chars': len(meta['content'])
            })
            
            done_cids.add(cid)
            processed += 1
        
        # Update registry
        for cid in unique_links:
            if cid not in registry:
                registry[cid] = {'content_id': cid, 'platform': 'toutiao'}
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
    finally:
        try: page.close()
        except: pass
        try: browser.close()
        except: pass
        try: p.stop()
        except: pass
    
    time.sleep(random.uniform(2, 4))
    
    # Save progress periodically
    if processed % 5 == 0:
        output = BATCH4_DIR / "batch004_progress.json"
        output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"  Progress saved ({len(results)} total, {processed} new)")

# Summary
articles_done = len([r for r in results if r.get('status') == 'DOWNLOADED'])
print(f"\n{'='*50}")
print(f"BATCH 004 TOUTIAO RESULTS:")
print(f"  Total processed: {len(results)}")
print(f"  Articles downloaded: {articles_done}")
print(f"  Target: 30 articles + 10 videos")

output = BATCH4_DIR / "batch004_progress.json"
output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"Saved to: {output}")