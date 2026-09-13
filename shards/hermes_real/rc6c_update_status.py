#!/usr/bin/env python3
"""RC6C: Update CURRENT_STATUS.md with proper counts"""
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix")
STATUS = BASE / "handoff/chatgpt/CURRENT_STATUS.md"

# Count valid items
REAL = BASE / "handoff/chatgpt/batch_004/wave_003_real"
INVALID = BASE / "handoff/chatgpt/batch_004/wave_003_invalid_rc6b"

import json
import csv

real_articles = [json.load(open(p, 'r', encoding='utf-8')) for p in REAL.glob("*.json") if p.suffix == '.json']
invalid_count = sum(1 for p in INVALID.glob("*.json") if p.suffix == '.json')

passed = sum(1 for a in real_articles if a.get('topic_gate') == 'TOPIC_PASS_MECHANICAL')
fulltext_ready = sum(1 for a in real_articles if a.get('text_chars', 0) >= 200 and not a.get('placeholder_detected') and a.get('topic_gate') == 'TOPIC_PASS_MECHANICAL')

content = f"""# CURRENT_STATUS.md - Updated 2026-09-13 RC6C

## Corpus Status (Pending Model Review)

| Metric | Value |
|--------|-------|
| Verified Logic Corpus | **85/100** (unchanged until ChatGPT review) |
| Wave001 Fulltext Complete V2 | **20/20** (FROZEN) |
| Wave002 Raw Real Body | 18/20 (FROZEN) |
| Wave002 Topic-Passed (Semantic) | **5** |
| Wave003 Real Discovered | **{len(real_articles)}** |
| Wave003 Topic Pass Mechanical | **{passed}** |
| Wave003 Fulltext Ready Pending Review | **{fulltext_ready}** |
| Wave003 Invalid/Quarantined RC6B | **{invalid_count}** |

---

## Wave001 Status (FROZEN - Accepted)

| Item | Value |
|------|-------|
| Total | 20/20 |
| Real Fulltext | 20/20 |
| Fulltext Complete V2 | 20/20 |
| Truncation Suspects | 0 (all repaired) |
| Logic Analyzable | PENDING_MODEL_REVIEW |

---

## Wave002 Status (FROZEN - Semantic Review Applied)

| Item | Value |
|------|-------|
| Total | 20/20 |
| Real Fulltext | 18/20 |
| Placeholder (login) | 2/20 |
| LOGIC_ANALYZABLE | 5 |
| Topic-Passed (Semantic) | **5** |

---

## Wave003 Status (RC6C Rebuild)

### Valid Items (wave_003_real/)
| Item | Value |
|------|-------|
| Discovered | **{len(real_articles)}** |
| Topic PASS Mechanical | **{passed}** |
| Fulltext Ready (>=200 chars) | **{fulltext_ready}** |

### Invalid Items Quarantined (wave_003_invalid_rc6b/)
| Item | Value |
|------|-------|
| Quarantined | **{invalid_count}** |
| Reason | synthetic IDs, duplicates, short text, missing provenance |

---

## Key Findings

1. **RC6B Provenance Failure**: Synthetic content IDs (7682800000000000001, etc.), short text (<200 chars), missing DISCOVERY_LOG entries.
2. **Quarantine Applied**: 17 invalid items moved to wave_003_invalid_rc6b/.
3. **Discovery Limitation**: Current Toutiao feed (2026-09-13) dominated by BRICS political news, limited commercial content available.
4. **Verification Status**: Wave003_Real has {len(real_articles)} source-backed items; targets not fully reached due to content ecosystem constraints.

---

## Discovery Mode: QUERY_FIRST

Search seeds used:
- 赚钱逻辑, 副业变现, 商业模式, AI商业, 能力变现
- 普通人收入, 职场收入, 品牌定位, 供应链, 成本利润

**Blocker**: Toutiao recommendation/search predominantly returns political/diplomatic content during BRICS summit period (2026-09-13). Commercial/business articles scarce in discoverable pool.

---

## Files

- `handoff/chatgpt/batch_004/wave_003_real/*.json` - Valid articles
- `handoff/chatgpt/batch_004/wave_003_real/DISCOVERY_LOG.csv`
- `handoff/chatgpt/batch_004/wave_003_real/TOPIC_GATE.csv`
- `handoff/chatgpt/batch_004/wave_003_real/FULLTEXT_QA.csv`
- `handoff/chatgpt/batch_004/wave_003_real/CROSS_BATCH_DEDUPE.csv`
- `handoff/chatgpt/batch_004/wave_003_invalid_rc6b/INVALID_MANIFEST.csv`
"""

with open(STATUS, 'w', encoding='utf-8') as f:
    f.write(content)

print("CURRENT_STATUS.md updated")
print(f"Real: {len(real_articles)}, Invalid: {invalid_count}")