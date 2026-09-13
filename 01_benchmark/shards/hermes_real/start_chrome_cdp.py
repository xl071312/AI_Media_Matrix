#!/usr/bin/env python3
"""Start Chrome CDP for MediaCrawler"""
import subprocess
import time
import socket
import urllib.request
import json
from pathlib import Path

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE_DIR = r"F:\workspace\AI_Media_Matrix\browser_profiles\douyin_benchmark_v3"
CDP_PORT = 9223

def start_chrome_cdp():
    """Start Chrome with CDP enabled"""
    print("=== STARTING CHROME CDP ===\n")
    
    # Check if already running
    s = socket.socket()
    s.settimeout(3)
    r = s.connect_ex(('127.0.0.1', CDP_PORT))
    s.close()
    
    if r == 0:
        print(f"CDP port {CDP_PORT} already listening")
        return True
    
    # Start Chrome
    print(f"Starting Chrome...")
    print(f"  Path: {CHROME_PATH}")
    print(f"  Profile: {PROFILE_DIR}")
    print(f"  Port: {CDP_PORT}")
    
    try:
        subprocess.Popen([
            CHROME_PATH,
            f"--remote-debugging-port={CDP_PORT}",
            f"--user-data-dir={PROFILE_DIR}",
            "--no-first-run",
            "--no-default-browser-check"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for CDP to be ready
        print("Waiting for CDP...")
        for i in range(15):
            time.sleep(2)
            s = socket.socket()
            s.settimeout(3)
            r = s.connect_ex(('127.0.0.1', CDP_PORT))
            s.close()
            if r == 0:
                print(f"  ✓ CDP port OPEN after {i*2+2}s")
                break
        else:
            print("  ✗ CDP port NOT OPEN after 30s")
            return False
        
        # Verify CDP
        try:
            resp = urllib.request.urlopen(f'http://127.0.0.1:{CDP_PORT}/json/version', timeout=5)
            data = json.loads(resp.read().decode())
            print(f"  ✓ CDP Version: {data.get('Browser', '?')}")
            ws_url = data.get('webSocketDebuggerUrl', '')
            print(f"  ✓ WebSocket: {ws_url[:60]}...")
            return True
        except Exception as e:
            print(f"  ✗ CDP Version check failed: {e}")
            return False
            
    except Exception as e:
        print(f"  ✗ Failed to start Chrome: {e}")
        return False

if __name__ == "__main__":
    success = start_chrome_cdp()
    exit(0 if success else 1)
