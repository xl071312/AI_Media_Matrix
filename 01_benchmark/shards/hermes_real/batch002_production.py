#!/usr/bin/env python3
"""Batch 002 Production - Full 75 Candidates Processing"""
import csv
import json
import time
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SHARDS = BASE / "shards" / "hermes_real"
BATCH2_DIR = BASE / "analysis_batches" / "batch_002"
MEDIA_DIR = BASE / "media" / "batch_002_smoke"
TRANSCRIPT_DIR = BASE / "shards" / "hermes_real" / "transcripts_v2"

BATCH2_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

# Topic keywords
TOPIC_KEYWORDS = ["赚钱", "变现", "信息差", "副业", "创业", "职场", "中产", "焦虑", 
                  "消费", "陷阱", "AI", "搞钱", "翻身", "财富", "认知", "思维", 
                  "商业", "加盟", "避坑", "投资", "黄金", "回收", "降级", "收入",
                  "劳动", "打工", "老板", "生意", "财务", "自由", "存钱", "理财",
                  "贫穷", "富贵", "资本", "经济", "金融", "知识", "付费", "课程"]
OFF_TOPIC_MARKERS = ["游戏", "攻略", "三角洲", "原神", "王者荣耀", "动漫", "二次元",
                     "短剧", "剧情", "美食", "烹饪", "健身", "宠物", "旅游", "美妆",
                     "穿搭", "数码", "汽车", "音乐", "舞蹈", "搞笑", "综艺", "电影", "明星"]

def is_on_topic(title, keyword=""):
    text = f"{title} {keyword}".lower()
    for m in OFF_TOPIC_MARKERS:
        if m in text:
            return False
    matches = sum(1 for kw in TOPIC_KEYWORDS if kw in text)
    return matches >= 2

def normalize_cid(raw):
    if not raw:
        return ""
    raw = str(raw).strip().lstrip('\ufeff')
    if raw.startswith('DY_REAL_'):
        raw = raw[8:]
    return str(raw).strip()

def load_candidates():
    """Load all ON_TOPIC new unique candidates"""
    # Load registry
    reg_path = BASE / "GLOBAL_CONTENT_ID_REGISTRY.csv"
    registry = set()
    with open(reg_path, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            cid = normalize_cid(row.get('content_id', ''))
            if cid:
                registry.add(cid)
    
    # Load selection
    sel_path = SHARDS / "douyin_benchmark_selection.csv"
    candidates = []
    with open(sel_path, 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            raw_cid = row.get('content_id', row.get('aweme_id', ''))
            cid = normalize_cid(raw_cid)
            if not cid or cid in registry:
                continue
            
            title = row.get('desc', '')[:100]
            keyword = row.get('source_keyword', '')
            
            if not is_on_topic(title, keyword):
                continue
            
            candidates.append({
                'cid': cid,
                'title': title,
                'keyword': keyword,
                'perf_score': float(row.get('performance_score', 0)),
                'sample_role': row.get('sample_role', ''),
                'viral_type': row.get('viral_type', ''),
                'likes': int(row.get('liked_count', 0)),
                'comments': int(row.get('comment_count', 0)),
                'favorites': int(row.get('collected_count', 0)),
                'shares': int(row.get('share_count', 0))
            })
    
    # Sort by performance
    candidates.sort(key=lambda x: x['perf_score'], reverse=True)
    return candidates

def get_page_data(cid):
    """Get page metadata and URLs via CDP"""
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9223')
    context = browser.contexts[0]
    
    page = context.new_page()
    url = f'https://www.douyin.com/video/{cid}'
    
    try:
        page.goto(url, timeout=25000)
        time.sleep(3)
        
        # Check blocked
        content = page.content()
        blocked = any(x in content for x in ['安全验证', '登录', '二维码'])
        
        if blocked:
            return {'cid': cid, 'status': 'BLOCKED'}
        
        # Get performance URLs
        perf_urls = page.evaluate('''() => {
            const entries = performance.getEntriesByType('resource');
            return entries.filter(e => e.name.includes('douyinvod'))
                .map(e => ({url: e.name.substring(0, 600), type: e.initiatorType}));
        }''')
        
        video_url = next((u['url'] for u in perf_urls if 'media-video' in u['url']), None)
        audio_url = next((u['url'] for u in perf_urls if 'media-audio' in u['url']), None)
        
        # Get metadata
        title = page.title().replace(' - 抖音', '').strip()
        
        # Get author
        author_links = page.query_selector_all('a[href*="/user/"]')
        author = author_links[0].text_content().strip() if author_links else 'N/A'
        
        # Get duration
        duration_text = page.evaluate('''() => {
            const spans = document.querySelectorAll('[class*="duration"], [class*="time"]');
            for (const s of spans) {
                const t = s.textContent.trim();
                if (t.match(/\\d{1,2}:\\d{2}/)) return t;
            }
            return null;
        }''')
        
        result = {
            'cid': cid,
            'status': 'OK',
            'title': title,
            'author': author,
            'video_url': video_url,
            'audio_url': audio_url,
            'duration_text': duration_text,
            'page_loaded': True
        }
        
    except Exception as e:
        result = {'cid': cid, 'status': f'ERROR: {str(e)[:50]}'}
    finally:
        try: page.close()
        except: pass
        try: browser.close()
        except: pass
        try: p.stop()
        except: pass
    
    return result

def main():
    print("=== BATCH 002 PRODUCTION ===\n")
    
    # Load candidates
    candidates = load_candidates()
    print(f"Total ON_TOPIC candidates: {len(candidates)}")
    
    # Process first 30
    results = []
    for i, c in enumerate(candidates[:30], 1):
        cid = c['cid']
        print(f"\n[{i}/30] {cid}")
        print(f"  Title: {c['title'][:60]}")
        
        data = get_page_data(cid)
        data.update({
            'likes': c['likes'],
            'comments': c['comments'],
            'favorites': c['favorites'],
            'shares': c['shares'],
            'perf_score': c['perf_score'],
            'viral_type': c['viral_type'],
            'sample_role': c['sample_role']
        })
        
        if data.get('status') == 'OK':
            print(f"  ✓ Loaded: {data.get('title', 'N/A')[:50]}")
            print(f"    Author: {data.get('author', 'N/A')}")
            print(f"    Video: {bool(data.get('video_url'))}, Audio: {bool(data.get('audio_url'))}")
        else:
            print(f"  ✗ {data.get('status')}")
        
        results.append(data)
        time.sleep(0.5)
    
    # Save results
    output_path = SHARDS / "batch002_production_progress.json"
    output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    
    # Summary
    ok = sum(1 for r in results if r.get('status') == 'OK')
    with_audio = sum(1 for r in results if r.get('audio_url'))
    print(f"\nSummary: {ok}/{len(results)} loaded, {with_audio}/{len(results)} with audio")
    print(f"Saved to: {output_path}")
    
    return results

if __name__ == "__main__":
    main()