#!/usr/bin/env python3
"""
尝试使用不同的API端点访问抖音
"""
import json
import requests
from pathlib import Path

WORKSPACE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
COOKIES_FILE = WORKSPACE / "douyin_cookies.txt"

def load_cookies():
    cookies = {}
    with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('\t')
            if len(parts) >= 7:
                cookies[parts[5]] = parts[6]
    return cookies

def try_endpoint(url, params=None):
    """Try a specific endpoint"""
    cookies = load_cookies()
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.douyin.com/',
    })
    
    for name, value in cookies.items():
        session.cookies.set(name, value)
    
    try:
        resp = session.get(url, params=params, timeout=10)
        data = resp.json()
        return data
    except Exception as e:
        return {"error": str(e)}

# Try different endpoints
endpoints = [
    ("Homefeed", "https://www.douyin.com/aweme/v1/web/home/feed/", {"feed_type": 0, "category_id": 0}),
    ("Discover", "https://www.douyin.com/aweme/v1/web/discover/", None),
    ("Recommend", "https://www.douyin.com/aweme/v1/web/recommend/item/", {"count": 10}),
]

results = {}
for name, url, params in endpoints:
    print(f"Testing {name}...")
    data = try_endpoint(url, params)
    results[name] = data
    
    if 'aweme_list' in data and data['aweme_list']:
        print(f"  ✓ Found {len(data['aweme_list'])} videos!")
        for v in data['aweme_list'][:3]:
            print(f"    - {v.get('desc', 'N/A')[:50]}...")
    elif 'error' in data:
        print(f"  ✗ Error: {data['error']}")
    else:
        print(f"  Response keys: {list(data.keys())[:5]}")
    
    time.sleep(1)

# Save results
output_file = WORKSPACE / "douyin_api_test.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nResults saved to: {output_file}")
