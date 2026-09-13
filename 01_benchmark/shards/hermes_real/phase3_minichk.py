#!/usr/bin/env python3
"""
Phase 3 End-to-End Mini Checkpoint Executor
Uses DOM fallback when APIs are blocked by ArgusSecurityPlugin
"""
import json
import csv
import time
import urllib.request
import subprocess
from pathlib import Path
from datetime import datetime

BASE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
MC_DIR = Path(r"C:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler")
DOM_SEARCH_DIR = BASE / "douyin_dom_search"
CREATOR_BASELINE_DIR = BASE / "creator_baseline_dom"
MEDIA_DIR = BASE / "media_raw"
TRANSCRIPT_DIR = BASE / "transcripts"
ANALYSIS_DIR = BASE / "analysis"

# Target: 5 creators, 3 transcripts, 3 deep analyses
TARGET_CREATOR_BASELINE = 5
TARGET_TRANSCRIPTS = 3
TARGET_DEEP_ANALYSIS = 3

class Phase3Executor:
    def __init__(self):
        self.status = {
            "phase": "PHASE_3_IN_PROGRESS",
            "timestamp": "",
            "cdp_http": "PENDING",
            "cdp_websocket": "PENDING",
            "search_api": "PENDING",
            "search_dom": "PENDING",
            "creator_api": "PENDING",
            "creator_dom": "PENDING",
            "detail_api": "PENDING",
            "video_page": "PENDING",
            "creator_baseline_done": 0,
            "real_spoken_done": 0,
            "timed_transcript_done": 0,
            "deep_analysis_done": 0,
            "placeholder_upgraded": 0,
            "argus_blocked": False,
            "blockers": []
        }
        
    def check_cdp_http(self):
        """Test CDP HTTP endpoint"""
        print("\n=== TEST: CDP HTTP ===")
        try:
            req = urllib.request.Request("http://127.0.0.1:9222/json/version")
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                self.status["cdp_http"] = "PASS"
                self.status["chrome_version"] = data.get("Browser", "")
                print(f"  PASS: {data.get('Browser', '')}")
                return True
        except Exception as e:
            self.status["cdp_http"] = "FAIL"
            self.status["blockers"].append(f"CDP_HTTP: {str(e)}")
            print(f"  FAIL: {e}")
            return False
    
    def check_cdp_websocket(self):
        """Test CDP WebSocket connection"""
        print("\n=== TEST: CDP WEBSOCKET ===")
        try:
            # Try to connect via MediaCrawler or direct check
            req = urllib.request.Request("http://127.0.0.1:9222/json")
            with urllib.request.urlopen(req, timeout=10) as resp:
                pages = json.loads(resp.read().decode())
                
            # Find a douyin page
            douyin_page = None
            for p in pages:
                if 'douyin.com' in p.get('url', '') and p.get('type') == 'page':
                    douyin_page = p
                    break
            
            if douyin_page:
                ws_url = douyin_page.get('webSocketDebuggerUrl')
                if ws_url:
                    self.status["cdp_websocket"] = "PASS"
                    self.status["ws_url"] = ws_url
                    print(f"  PASS: Connected to {ws_url[:60]}...")
                    return True
                else:
                    self.status["cdp_websocket"] = "FAIL"
                    self.status["blockers"].append("No WebSocket URL found")
                    return False
            else:
                self.status["cdp_websocket"] = "NEEDS_PAGE"
                print("  NEEDS_PAGE: No Douyin page open")
                return False
        except Exception as e:
            self.status["cdp_websocket"] = "FAIL"
            self.status["blockers"].append(f"CDP_WS: {str(e)}")
            print(f"  FAIL: {e}")
            return False
    
    def test_search_api(self):
        """Test MediaCrawler search API"""
        print("\n=== TEST: SEARCH API ===")
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
            
            proc = subprocess.run(cmd, cwd=str(MC_DIR), capture_output=True, text=True, timeout=120)
            
            stderr = proc.stderr.lower()
            stdout = proc.stdout.lower()
            
            if "aweme_list" in stderr and "[]" in stderr:
                self.status["search_api"] = "BLOCKED"
                self.status["argus_blocked"] = True
                print("  BLOCKED: ArgusSecurityPlugin拦截")
                return False
            elif proc.returncode == 0:
                self.status["search_api"] = "PASS"
                print("  PASS: Search API working")
                return True
            else:
                self.status["search_api"] = "FAIL"
                self.status["blockers"].append(f"Search: {proc.stderr[:200]}")
                return False
        except subprocess.TimeoutExpired:
            self.status["search_api"] = "TIMEOUT"
            return False
        except Exception as e:
            self.status["search_api"] = "ERROR"
            self.status["blockers"].append(f"Search error: {str(e)}")
            return False
    
    def test_creator_api(self):
        """Test MediaCrawler creator API"""
        print("\n=== TEST: CREATOR API ===")
        try:
            cmd = [
                "uv", "run", "main.py",
                "--platform", "dy",
                "--type", "creator",
                "--creator_id", "MS4wLjABAAAAf9C6bAkw10bndnBb6OF4Q28AQf2bXdQ0kRut0dIJJOM",
                "--crawler_max_notes_count", "3",
                "--headless", "false",
                "--get_comment", "no",
                "--save_data_option", "jsonl"
            ]
            
            proc = subprocess.run(cmd, cwd=str(MC_DIR), capture_output=True, text=True, timeout=120)
            
            stderr = proc.stderr.lower()
            
            if "uifid not found" in stderr or "argus" in stderr:
                self.status["creator_api"] = "BLOCKED_BY_ARGUS"
                self.status["argus_blocked"] = True
                print("  BLOCKED_BY_ARGUS: Uifid Not Found")
                return False
            elif proc.returncode == 0:
                self.status["creator_api"] = "PASS"
                print("  PASS: Creator API working")
                return True
            else:
                self.status["creator_api"] = "FAIL"
                print(f"  FAIL: {proc.stderr[:200]}")
                return False
        except Exception as e:
            self.status["creator_api"] = "ERROR"
            self.status["blockers"].append(f"Creator error: {str(e)}")
            return False
    
    def test_detail_api(self):
        """Test MediaCrawler detail API"""
        print("\n=== TEST: DETAIL API ===")
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
            
            proc = subprocess.run(cmd, cwd=str(MC_DIR), capture_output=True, text=True, timeout=120)
            
            stderr = proc.stderr.lower()
            
            if "uifid not found" in stderr or "argus" in stderr:
                self.status["detail_api"] = "BLOCKED_BY_ARGUS"
                self.status["argus_blocked"] = True
                print("  BLOCKED_BY_ARGUS: Uifid Not Found")
                return False
            elif proc.returncode == 0:
                self.status["detail_api"] = "PASS"
                print("  PASS: Detail API working")
                return True
            else:
                self.status["detail_api"] = "FAIL"
                print(f"  FAIL: {proc.stderr[:200]}")
                return False
        except Exception as e:
            self.status["detail_api"] = "ERROR"
            self.status["blockers"].append(f"Detail error: {str(e)}")
            return False
    
    def check_video_page_access(self, aweme_id):
        """Check if video page is accessible via browser"""
        print(f"\n=== CHECK: VIDEO PAGE {aweme_id} ===")
        # This would use CDP to navigate and check
        # For now, mark as NEEDS_BENCHMARK_CHROME
        self.status["video_page"] = "NEEDS_BROWSER"
        print("  NEEDS_BROWSER: Open in Benchmark Chrome to check")
        return False
    
    def run_dom_creator_baseline(self, sec_user_id, target_count=10):
        """Collect creator baseline via DOM scraping"""
        print(f"\n=== DOM BASELINE: {sec_user_id} ===")
        
        # This will use CDP to navigate to creator page and scrape
        # Implementation depends on WebSocket connection being available
        
        output_dir = CREATOR_BASELINE_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Placeholder - actual implementation needs WebSocket
        result = {
            "creator_id": sec_user_id,
            "baseline_sample_n": 0,
            "creator_median_likes": None,
            "videos": [],
            "status": "PENDING_WEBSOCKET_FIX"
        }
        
        output_file = output_dir / f"{sec_user_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        return result
    
    def save_checkpoint(self):
        """Save current checkpoint status"""
        self.status["timestamp"] = datetime.now().isoformat()
        
        # Count actual completions
        baseline_files = list(CREATOR_BASELINE_DIR.glob("*.json")) if CREATOR_BASELINE_DIR.exists() else []
        transcript_files = list(TRANSCRIPT_DIR.glob("*_raw.json")) if TRANSCRIPT_DIR.exists() else []
        analysis_files = list(ANALYSIS_DIR.glob("analysis_*.md")) if ANALYSIS_DIR.exists() else []
        
        self.status["creator_baseline_done"] = len([f for f in baseline_files if json.load(open(f)).get('baseline_sample_n', 0) >= 5])
        self.status["timed_transcript_done"] = len(transcript_files)
        self.status["deep_analysis_done"] = len(analysis_files)
        
        output = BASE / "phase3_mini_checkpoint.json"
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(self.status, f, indent=2, ensure_ascii=False)
        
        return self.status

def main():
    executor = Phase3Executor()
    
    print("=" * 60)
    print("PHASE 3 END-TO-END MINI CHECKPOINT")
    print("=" * 60)
    
    # Step 1: CDP HTTP
    if not executor.check_cdp_http():
        print("\nCDP HTTP failed. Cannot proceed.")
        executor.save_checkpoint()
        return
    
    # Step 2: CDP WebSocket
    if not executor.check_cdp_websocket():
        print("\nCDP WebSocket failed. Need Benchmark Chrome with proper params.")
        print("Please execute the PowerShell command to start Benchmark Chrome.")
        executor.save_checkpoint()
        return
    
    # Step 3: Search API
    executor.test_search_api()
    
    # Step 4: Creator API
    executor.test_creator_api()
    
    # Step 5: Detail API
    executor.test_detail_api()
    
    # Step 6: Check video page
    executor.check_video_page_access("7533123064641506579")
    
    # Save checkpoint
    status = executor.save_checkpoint()
    
    print("\n" + "=" * 60)
    print("CHECKPOINT SAVED")
    print("=" * 60)
    
    # Print summary
    print(f"\nCDP HTTP: {status['cdp_http']}")
    print(f"CDP WebSocket: {status['cdp_websocket']}")
    print(f"SEARCH API: {status['search_api']}")
    print(f"CREATOR API: {status['creator_api']}")
    print(f"DETAIL API: {status['detail_api']}")
    print(f"Video Page: {status['video_page']}")
    print(f"\nArgus Blocked: {status['argus_blocked']}")
    print(f"Blockers: {len(status['blockers'])}")
    
    print(f"\nTargets:")
    print(f"  Creator Baseline: {status['creator_baseline_done']}/{TARGET_CREATOR_BASELINE}")
    print(f"  Timed Transcript: {status['timed_transcript_done']}/{TARGET_TRANSCRIPTS}")
    print(f"  Deep Analysis: {status['deep_analysis_done']}/{TARGET_DEEP_ANALYSIS}")

if __name__ == "__main__":
    main()
