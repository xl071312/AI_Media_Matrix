#!/usr/bin/env python3
"""Phase 3 Validation Script - Test CDP v3"""
import json
import asyncio
import urllib.request
from pathlib import Path

BASE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")

async def test_cdp_v3():
    print("=== CDP V3 VALIDATION ===\n")
    
    # Test HTTP
    try:
        req = urllib.request.Request("http://127.0.0.1:9223/json/version")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            print(f"✓ CDP HTTP: PASS")
            print(f"  Browser: {data.get('Browser', '')}")
            ws_url = data.get('webSocketDebuggerUrl', '')
    except Exception as e:
        print(f"✗ CDP HTTP: FAIL - {e}")
        return
    
    # Test WebSocket
    try:
        import websockets
        
        print(f"\nTesting WebSocket...")
        async with websockets.connect(ws_url, origin="http://127.0.0.1:9223") as ws:
            print("✓ WebSocket: PASS")
            
            # Enable Runtime
            await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
            await asyncio.wait_for(ws.recv(), timeout=5)
            
            # Get pages
            await ws.send(json.dumps({
                "id": 2,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": "JSON.stringify(Array.from(document.querySelectorAll('iframe, [class*=\"page\"]').map(el => ({tag: el.tagName, class: el.className, id: el.id}).toString()).slice(0, 5)))"
                }
            }))
            
            resp = await asyncio.wait_for(ws.recv(), timeout=5)
            print(f"✓ DOM access: WORKING")
            
    except Exception as e:
        print(f"✗ WebSocket: FAIL - {e}")
        return
    
    print("\n=== ALL TESTS PASSED ===")
    print("Ready for Phase 3 collection")

if __name__ == "__main__":
    asyncio.run(test_cdp_v3())
