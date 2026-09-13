#!/usr/bin/env python3
"""Douyin Search API Collector using real cookies - Fixed encoding"""
import json
import sys
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime
import csv

# Paths
WORKSPACE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
COOKIES_FILE = WORKSPACE / "douyin_cookies.txt"
OUTPUT_FILE = WORKSPACE / "douyin_real_batch_001.csv"

def load_cookies():
    """Load cookies from Netscape format file"""
    cookies = []
    with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('\t')
            if len(parts) >= 7:
                cookies.append(f"{parts[5]}={parts[6]}")
    return "; ".join(cookies)

def collect_douyin_search(keyword, count=10):
    """Search douyin and extract video data"""
    cookies = load_cookies()
    
    # URL encode keyword properly
    encoded_keyword = urllib.parse.quote(keyword.encode('utf-8'))
    
    url = f"https://www.douyin.com/aweme/v1/web/search/item/?keyword={encoded_keyword}&search_channel=aweme_video_web&sort_type=0&publish_time=0&filter_duration=0&cursor=0&count={count}&aid=6383"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
        'Cookie': cookies,
        'Referer': 'https://www.douyin.com/',
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8')
            data = json.loads(content)
            return data.get('data', [])
    except Exception as e:
        print(f"Error searching '{keyword}': {e}", file=sys.stderr)
        return []

def main():
    keywords = ["赚钱逻辑", "副业", "创业", "信息差"]
    all_videos = []
    
    for keyword in keywords:
        print(f"Searching: {keyword}")
        videos = collect_douyin_search(keyword, count=10)
        print(f"  Found {len(videos)} videos")
        
        for item in videos:
            aweme_id = item.get('aweme_id', '')
            desc = item.get('desc', '')
            author = item.get('author', {}).get('nickname', '')
            stats = item.get('statistics', {})
            
            video_data = {
                'content_id': f'DY_REAL_{aweme_id}',
                'platform': 'Douyin',
                'content_format': 'video',
                'url': f'https://www.douyin.com/video/{aweme_id}',
                'creator_name': author,
                'title': desc[:100] if desc else '',
                'topic_cluster': keyword,
                'discovery_query': keyword,
                'discovery_mode': 'search',
                'publish_date': '',
                'duration_sec': str(item.get('duration', 0) // 1000),
                'followers': '',
                'views': str(stats.get('play_count', '')),
                'likes': str(stats.get('digg_count', '')),
                'comments': str(stats.get('comment_count', '')),
                'favorites': str(stats.get('collect_count', '')),
                'shares': str(stats.get('share_count', '')),
                'performance_verified': 'False',
                'transcript_status': 'pending',
                'evidence_url': f'https://www.douyin.com/video/{aweme_id}',
                'evidence_type': 'api_response',
                'evidence_capture_time': datetime.now().isoformat(),
                'notes': 'Real data from API'
            }
            all_videos.append(video_data)
    
    # Write CSV
    fieldnames = ['content_id', 'platform', 'content_format', 'url', 'creator_name',
                  'title', 'topic_cluster', 'discovery_query', 'discovery_mode',
                  'publish_date', 'duration_sec', 'followers', 'views', 'likes',
                  'comments', 'favorites', 'shares', 'performance_verified',
                  'transcript_status', 'evidence_url', 'evidence_type',
                  'evidence_capture_time', 'notes']
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_videos)
    
    print(f"\nTotal collected: {len(all_videos)} videos")
    print(f"Output: {OUTPUT_FILE}")
    
    # Print sample
    if all_videos:
        print("\nSample records:")
        for v in all_videos[:3]:
            print(f"  {v['content_id']}: {v['title'][:50]}... | likes={v['likes']}")

if __name__ == "__main__":
    main()
