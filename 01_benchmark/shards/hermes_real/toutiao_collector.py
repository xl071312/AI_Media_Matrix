#!/usr/bin/env python3
"""
Toutiao User Content Collector
"""
import json
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")

def collect_toutiao_user(user_id):
    """Collect user content from Toutiao"""
    # API endpoints to try
    endpoints = [
        f"https://www.toutiao.com/api/pc/user/article/list/?user_id={user_id}&cursor=0&count=20",
        f"https://www.toutiao.com/api/pc/feed/user/content/?user_id={user_id}&cursor=0&count=20",
        f"https://www.toutiao.com/api/pc/feed/by_channel/?channel=news_article&user_id={user_id}&max_behot_time=0&count=20",
    ]
    
    cookies = ""  # Will be provided by user
    
    results = []
    for endpoint in endpoints:
        try:
            url = endpoint
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Cookie': cookies,
                'Referer': 'https://www.toutiao.com/'
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if data.get('data'):
                    results.extend(data['data'])
        except Exception as e:
            print(f"Error: {e}")
    
    return results

if __name__ == "__main__":
    print("Toutiao User Collector v1.0")
    print("=" * 60)
    print("\n需要用户提供Cookie才能访问用户数据")
    print("请提供头条Cookie或完成登录后重试")
