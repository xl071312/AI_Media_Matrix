#!/usr/bin/env python3
"""
使用requests库访问抖音，需要处理签名验证
"""
import json
import time
import requests
from pathlib import Path

WORKSPACE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
COOKIES_FILE = WORKSPACE / "douyin_cookies.txt"

def load_cookies():
    """Load cookies from Netscape format file"""
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

def test_douyin_access():
    """Test if we can access Douyin with cookies"""
    cookies = load_cookies()
    
    # Create session
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    })
    
    # Add cookies
    for name, value in cookies.items():
        session.cookies.set(name, value, domain='.douyin.com')
        session.cookies.set(name, value, domain='www.douyin.com')
    
    # Test homepage
    print("Testing homepage access...")
    try:
        resp = session.get('https://www.douyin.com/', timeout=10)
        print(f"Homepage status: {resp.status_code}")
        print(f"Response length: {len(resp.text)}")
        if 'captcha' in resp.text.lower() or '验证' in resp.text:
            print("CAPTCHA detected!")
        elif 'login' in resp.text.lower():
            print("Login required!")
        else:
            print("Homepage accessible!")
    except Exception as e:
        print(f"Homepage error: {e}")
    
    # Test search API
    print("\nTesting search API...")
    try:
        resp = session.get(
            'https://www.douyin.com/aweme/v1/web/search/item/',
            params={
                'keyword': '赚钱逻辑',
                'search_channel': 'aweme_video_web',
                'sort_type': '0',
                'publish_time': '0',
                'filter_duration': '0',
                'cursor': '0',
                'count': '10',
                'aid': '6383'
            },
            timeout=10
        )
        print(f"Search API status: {resp.status_code}")
        print(f"Response: {resp.text[:500]}")
    except Exception as e:
        print(f"Search API error: {e}")

if __name__ == "__main__":
    test_douyin_access()
