#!/usr/bin/env python3
"""
尝试访问抖音特定视频页面（不走搜索）
"""
import json
import time
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

def try_video_url(url):
    """Try to access a specific video URL"""
    cookies = load_cookies()
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.douyin.com/',
    })
    
    for name, value in cookies.items():
        session.cookies.set(name, value)
    
    try:
        resp = session.get(url, timeout=10, allow_redirects=True)
        print(f"URL: {url}")
        print(f"Status: {resp.status_code}")
        print(f"Final URL: {resp.url}")
        
        # Check if we got captcha page
        if 'captcha' in resp.text.lower() or '验证' in resp.text or 'verify' in resp.text.lower():
            print("✗ CAPTCHA detected")
            return None
        
        # Try to extract video data from page
        import re
        # Look for aweme detail data
        match = re.search(r'window\._ROUTER_DATA\s*=\s*(\{.*?\});', resp.text, re.DOTALL)
        if match:
            print("✓ Found ROUTER_DATA")
            return match.group(1)
        
        match = re.search(r'window\.__INIT_STATE__\s*=\s*(\{.*?\});', resp.text, re.DOTALL)
        if match:
            print("✓ Found INIT_STATE")
            return match.group(1)
        
        print(f"Response length: {len(resp.text)}")
        return resp.text[:500]
    except Exception as e:
        print(f"Error: {e}")
        return None

# Try some common Douyin video URL patterns
# Note: These are example IDs, we need real ones from user
test_urls = [
    "https://www.douyin.com/video/7345678901234567890",
    "https://www.douyin.com/note/7345678901234567890",
]

print("Testing Douyin video access...")
print("=" * 60)

for url in test_urls:
    result = try_video_url(url)
    if result:
        print(f"Success for {url}")
    print()
    time.sleep(1)

print("\nTo get real videos, I need:")
print("1. You to visit douyin.com in your browser")
print("2. Search for '赚钱逻辑' manually")
print("3. Copy 3-5 video URLs from the results")
print("4. Send them to me")
