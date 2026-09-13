#!/usr/bin/env python3
"""Test Douyin API with different approaches"""
import json
import sys
import urllib.request
import urllib.parse
from pathlib import Path

WORKSPACE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
COOKIES_FILE = WORKSPACE / "douyin_cookies.txt"

def load_cookies():
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

def test_api(url, method="GET"):
    cookies = load_cookies()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
        'Cookie': cookies,
        'Referer': 'https://www.douyin.com/',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    
    req = urllib.request.Request(url, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            print(f"URL: {url}")
            print(f"Status: {resp.status}")
            print(f"Response length: {len(content)}")
            print(f"Response preview: {content[:500]}")
            return content
    except Exception as e:
        print(f"Error: {e}")
        return None

# Test 1: Homefeed
print("=" * 60)
print("Test 1: Homefeed API")
test_api("https://www.douyin.com/aweme/v1/web/homefeed/?feed_type=0&category_id=0&pull_type=0&last_replace_time=0&count=10")

# Test 2: Search with different endpoint
print("\n" + "=" * 60)
print("Test 2: Search API v2")
encoded_kw = urllib.parse.quote("赚钱逻辑".encode('utf-8'))
test_api(f"https://www.douyin.com/aweme/v1/web/discover/search/text/?keyword={encoded_kw}&search_channel=aweme_video_web&sort_type=0&publish_time=0&filter_duration=0&cursor=0&count=10&aid=6383")

# Test 3: Check cookie validity
print("\n" + "=" * 60)
print("Test 3: User info API")
test_api("https://www.douyin.com/aweme/v1/web/user/info/?sec_user_id=&uid=")
