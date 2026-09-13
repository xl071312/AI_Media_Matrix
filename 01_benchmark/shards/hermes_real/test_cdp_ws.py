#!/usr/bin/env python3
"""Test CDP WebSocket with correct websockets library"""
import asyncio
import json
import urllib.request

async def test_cdp_websocket():
    """Test WebSocket connection using websockets library"""
    print("=== CDP WEBSOCKET TEST ===\n")
    
    try:
        # Get browser WebSocket URL
        req = urllib.request.Request("http://127.0.0.1:9222/json/version")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            print(f"CDP HTTP: PASS")
            print(f"Browser: {data.get('Browser', '')}")
        
        # Get pages
        req = urllib.request.Request("http://127.0.0.1:9222/json")
        with urllib.request.urlopen(req, timeout=10) as resp:
            pages = json.loads(resp.read().decode())
            print(f"\nOpen pages: {len(pages)}")
            
            # Find main page
            main_page = None
            for p in pages:
                if p.get('type') == 'page' and 'douyin.com' in p.get('url', ''):
                    main_page = p
                    break
            
            if main_page:
                ws_url = main_page.get('webSocketDebuggerUrl')
                print(f"Main page: {main_page.get('title')}")
                print(f"WebSocket URL: {ws_url}")
                
                # Test connection with origin header
                import websockets
                
                print(f"\nTesting WebSocket connection...")
                
                try:
                    async with websockets.connect(
                        ws_url,
                        origin="http://127.0.0.1:9222",
                        max_size=10*1024*1024
                    ) as ws:
                        print("✓ WebSocket connected!")
                        
                        # Enable Runtime
                        await ws.send(json.dumps({
                            "id": 1,
                            "method": "Runtime.enable"
                        }))
                        
                        # Read response
                        resp = await asyncio.wait_for(ws.recv(), timeout=5)
                        print(f"Runtime.enable: {resp[:50]}...")
                        
                        # Execute simple JS
                        await ws.send(json.dumps({
                            "id": 2,
                            "method": "Runtime.evaluate",
                            "params": {
                                "expression": "document.title",
                                "returnByValue": True
                            }
                        }))
                        
                        resp = await asyncio.wait_for(ws.recv(), timeout=5)
                        data = json.loads(resp)
                        if 'result' in data and 'result' in data['result']:
                            print(f"✓ document.title: {data['result']['result'].get('value', '')}")
                        
                        return True
                        
                except Exception as e:
                    print(f"✗ WebSocket error: {e}")
                    return False
            else:
                print("No Douyin page found")
                return False
                
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_cdp_websocket())
    print(f"\nResult: {'PASS' if result else 'FAIL'}")
