#!/usr/bin/env python3
"""Phase 3 Blocker Diagnostic - Determine root cause"""
import json
import urllib.request
import urllib.error
from pathlib import Path
import subprocess
import time

BASE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
MC_DIR = Path(r"C:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler")

results = {
    "timestamp": "",
    "cdp": {"status": "UNKNOWN", "error": ""},
    "search_test": {"status": "PENDING", "error": ""},
    "creator_test": {"status": "PENDING", "error": ""},
    "detail_test": {"status": "PENDING", "error": ""},
    "media_test": {"status": "PENDING", "error": ""}
}

def check_cdp():
    """Check if CDP is accessible"""
    try:
        req = urllib.request.Request("http://127.0.0.1:9222/json/version")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            results["cdp"]["status"] = "PASS"
            results["cdp"]["chrome_version"] = data.get("Browser", "")
            results["timestamp"] = str(int(time.time()))
            return True
    except urllib.error.URLError as e:
        results["cdp"]["status"] = "FAIL"
        results["cdp"]["error"] = str(e)
        return False
    except Exception as e:
        results["cdp"]["status"] = "ERROR"
        results["cdp"]["error"] = str(e)
        return False

def run_search_test():
    """Test search mode (known to work before)"""
    try:
        cmd = [
            "uv", "run", "main.py",
            "--platform", "dy",
            "--type", "search",
            "--keywords", "赚钱逻辑",
            "--crawler_max_notes_count", "5",
            "--headless", "false",
            "--get_comment", "no",
            "--save_data_option", "jsonl"
        ]
        
        print("Running SEARCH test...")
        proc = subprocess.run(cmd, cwd=str(MC_DIR), capture_output=True, text=True, timeout=120)
        
        if proc.returncode == 0:
            # Check output files
            data_dir = MC_DIR / "data" / "douyin" / "jsonl"
            latest = sorted(data_dir.glob("*.jsonl"))[-1] if list(data_dir.glob("*.jsonl")) else None
            if latest:
                with open(latest, 'r', encoding='utf-8') as f:
                    lines = [l for l in f if l.strip()]
                if len(lines) >= 3:
                    results["search_test"]["status"] = "PASS"
                    results["search_test"]["records"] = len(lines)
                    print(f"SEARCH PASS: {len(lines)} records")
                    return True
        
        results["search_test"]["status"] = "FAIL"
        results["search_test"]["error"] = proc.stderr[:300] if proc.stderr else "No output"
        print(f"SEARCH FAIL: {results['search_test']['error']}")
        return False
    except Exception as e:
        results["search_test"]["status"] = "ERROR"
        results["search_test"]["error"] = str(e)
        return False

def run_creator_test():
    """Test creator mode"""
    try:
        # Use a known creator from our data
        cmd = [
            "uv", "run", "main.py",
            "--platform", "dy",
            "--type", "creator",
            "--creator_id", "MS4wLjABAAAAf9C6bAkw10bndnBb6OF4Q28AQf2bXdQ0kRut0dIJJOM",
            "--crawler_max_notes_count", "5",
            "--headless", "false",
            "--get_comment", "no",
            "--save_data_option", "jsonl"
        ]
        
        print("Running CREATOR test...")
        proc = subprocess.run(cmd, cwd=str(MC_DIR), capture_output=True, text=True, timeout=120)
        
        # Check for specific error patterns
        stderr = proc.stderr.lower()
        stdout = proc.stdout.lower()
        combined = stderr + stdout
        
        if "account blocked" in combined or "request params incrr" in combined or "uifid not found" in combined:
            results["creator_test"]["status"] = "BLOCKED"
            results["creator_test"]["error"] = "API blocked by Douyin security"
            print("CREATOR BLOCKED: API security block detected")
        elif proc.returncode == 0:
            results["creator_test"]["status"] = "PASS"
            print("CREATOR PASS")
        else:
            results["creator_test"]["status"] = "FAIL"
            results["creator_test"]["error"] = proc.stderr[:300] if proc.stderr else str(proc.returncode)
            print(f"CREATOR FAIL: {results['creator_test']['error']}")
        
        return results["creator_test"]["status"] == "PASS"
    except subprocess.TimeoutExpired:
        results["creator_test"]["status"] = "TIMEOUT"
        results["creator_test"]["error"] = "Command timed out"
        return False
    except Exception as e:
        results["creator_test"]["status"] = "ERROR"
        results["creator_test"]["error"] = str(e)
        return False

def run_detail_test():
    """Test detail mode with media"""
    try:
        cmd = [
            "uv", "run", "main.py",
            "--platform", "dy",
            "--type", "detail",
            "--specified_id", "7533123064641506579",
            "--headless", "false",
            "--get_comment", "no",
            "--save_data_option", "jsonl"
        ]
        
        print("Running DETAIL test...")
        proc = subprocess.run(cmd, cwd=str(MC_DIR), capture_output=True, text=True, timeout=120)
        
        stderr = proc.stderr.lower()
        stdout = proc.stdout.lower()
        combined = stderr + stdout
        
        if "account blocked" in combined or "request params incrr" in combined or "uifid not found" in combined:
            results["detail_test"]["status"] = "BLOCKED"
            results["detail_test"]["error"] = "API blocked by Douyin security"
            print("DETAIL BLOCKED: API security block detected")
        elif proc.returncode == 0:
            results["detail_test"]["status"] = "PASS"
            print("DETAIL PASS")
        else:
            results["detail_test"]["status"] = "FAIL"
            results["detail_test"]["error"] = proc.stderr[:300] if proc.stderr else str(proc.returncode)
            print(f"DETAIL FAIL: {results['detail_test']['error']}")
        
        return results["detail_test"]["status"] == "PASS"
    except Exception as e:
        results["detail_test"]["status"] = "ERROR"
        results["detail_test"]["error"] = str(e)
        return False

def main():
    print("=== PHASE 3 BLOCKER DIAGNOSTIC ===\n")
    
    # Test 1: CDP
    print("TEST 1: CDP Connection")
    cdp_ok = check_cdp()
    print(f"  Status: {results['cdp']['status']}")
    if results['cdp']['error']:
        print(f"  Error: {results['cdp']['error']}")
    print()
    
    if not cdp_ok:
        print("CDP not available. Cannot proceed with other tests.")
        save_results()
        return
    
    # Test 2: Search
    print("TEST 2: SEARCH Mode")
    search_ok = run_search_test()
    print()
    
    if not search_ok:
        print("SEARCH failed - CDP/Session issue. Stopping further tests.")
        save_results()
        return
    
    # Test 3: Creator
    print("TEST 3: CREATOR Mode")
    creator_result = run_creator_test()
    print()
    
    # Test 4: Detail + Media
    print("TEST 4: DETAIL + MEDIA Mode")
    detail_result = run_detail_test()
    print()
    
    save_results()
    print("\n=== RESULTS SAVED ===")
    print(json.dumps(results, indent=2, ensure_ascii=False))

def save_results():
    output = BASE / "phase3_blocker_diagnostic.json"
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
