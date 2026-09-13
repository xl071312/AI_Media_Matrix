# 【Batch002 Preflight RC1】- Final Report

**Date**: 2026-09-10
**Status**: PREFLIGHT_QA = PASS

---

## Executive Summary

| Metric | Value | Status |
|--------|-------|--------|
| Selection Total | 100 | ✓ |
| Existing in Registry | 5 | ✓ |
| New Unique (ON_TOPIC) | 75 | ✓ |
| New Unique (OFF_TOPIC) | 20 | ✓ |
| Invalid | 0 | ✓ |
| TOP20 Registry Violations | 0 | ✓ |
| **PREFLIGHT_QA** | **PASS** | ✓ |

---

## Cross-Batch Dedupe Fix

**Problem Identified**: Previous script incorrectly treated `DY_REAL_7525683513706810682` as NEW when it exists in Registry.

**Root Cause**: CID format mismatch - Selection uses `DY_REAL_xxx` prefix while Registry stores plain numeric IDs.

**Fix Applied**: 
```python
def normalize_cid(raw):
    """Remove DY_REAL_ prefix, strip whitespace, ensure string"""
    raw = str(raw).strip().lstrip('\ufeff')
    if raw.startswith('DY_REAL_'):
        raw = raw[8:]
    return str(raw).strip()
```

**Verification**:
- `7525683513706810682 IN Registry: TRUE` ✓
- Registry has 24 entries (all from Batch001)
- Selection has 100 entries
- After normalization: 5 existing, 95 new

---

## Topic Gate Results

**ON_TOPIC Keywords**: 赚钱, 变现, 信息差, 副业, 创业, 职场, 中产焦虑, 消费陷阱, AI赚钱, 普通人收入, 财富认知, 搞钱, 翻身, 商业思维, 加盟避坑, 投资认知, 黄金回收, 消费降级

**OFF_TOPIC Markers**: 游戏, 动漫, 短剧, 美食, 健身, 宠物, 旅游, 美妆, 穿搭, 数码, 汽车, 音乐, 舞蹈, 搞笑

**Result**:
- ON_TOPIC: 75 candidates
- OFF_TOPIC: 20 candidates
- Filtered out: 5 already in registry

---

## TOP 20 ON_TOPIC NEW UNIQUE

| # | Content ID | Performance | Role | Title |
|---|------------|-------------|------|-------|
| 1 | 7351254246710463755 | 99.5 | ABSOLUTE_VIRAL | 醍醐灌顶！本打工人已经将这段话刻进脑子里了 |
| 2 | 7439645541958552844 | 98.5 | ABSOLUTE_VIRAL | 00后大学生勇闯社会第一年 |
| 3 | 7293036400465726783 | 97.6 | ABSOLUTE_VIRAL | 四个阶段：对钱有概念 花钱有概念 攒钱有概念 搞钱有概念 |
| 4 | 7577322313134132520 | 97.4 | ABSOLUTE_VIRAL | 年轻人一定不要超前消费 |
| 5 | 7600369823520073126 | 97.1 | ABSOLUTE_VIRAL | 悟了#如何花钱 #消费观 |
| 6 | 7450364063030267151 | 96.5 | ABSOLUTE_VIRAL | 理想冰箱杯架创业过程分享 |
| 7 | 7540234540556619058 | 96.2 | ABSOLUTE_VIRAL | 对钱没概念这件事，真的会摧毁一个人的人生 |
| 8 | 7479008308989316361 | 95.2 | ABSOLUTE_VIRAL | 年轻人如何赚到一笔大钱呢 |
| 9 | 7673172635974421760 | 95.0 | ABSOLUTE_VIRAL | 被人怼时一秒回击 |
| 10 | 7564348993203948810 | 92.7 | ABSOLUTE_VIRAL | 人一旦掌握了赚钱思维 |
| 11 | 7473417086673440012 | 91.5 | ABSOLUTE_VIRAL | 2025年，最应该提升的是赚钱能力 |
| 12 | 7636452871718385906 | 91.5 | ABSOLUTE_VIRAL | 让我们打破短视频信息茧房 |
| 13 | 7664587315726338697 | 90.9 | ABSOLUTE_VIRAL | 来了义乌才知道，原来自己生活在巨大的信息差里 |
| 14 | 7513092150196702476 | 90.8 | ABSOLUTE_VIRAL | 同志们，警惕消费主义陷阱 |
| 15 | 7583723020817124662 | 90.5 | ABSOLUTE_VIRAL | 查理芒格：慢富即永恒 |
| 16 | 7477191872570477839 | 89.8 | ABSOLUTE_VIRAL | 消费陷阱来自资本的阴谋 |
| 17 | 7218880148861390118 | 77.3 | RELATIVE_BREAKOUT | 普通人需要多久才能赚够100万 |
| 18 | 7647446230122356665 | 77.3 | RELATIVE_BREAKOUT | 创业首先是思维问题 |
| 19 | 7000743196867267871 | 77.2 | RELATIVE_BREAKOUT | 拆掉消费主义陷阱 |
| 20 | 7599188562650734516 | 77.1 | RELATIVE_BREAKOUT | 金价暴涨，最大的受益者是谁 |

---

## Batch002 Targets

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| NEW UNIQUE | >= 30 | 75 available | ✓ |
| ON_TOPIC | 30 | 75 available | ✓ |
| Qualified Transcript | 30 | 0 | Pending |
| Verified Performance | >= 24 | N/A | Pending |
| simulated | 0 | 0 | ✓ |

---

## Pipeline Status

```
✓ DOM Discovery: PASS
✓ Cross-Batch Dedupe: FIXED
✓ Topic Gate: IMPLEMENTED
✓ Preflight QA: PASS
⏳ Page Verification: READY
⏳ Media Download: READY
⏳ ASR: READY
```

---

## Files Generated

```
F:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real\
├── batch002_preflight_rc1.json
├── batch002_preflight_rc1.py
└── PREFLIGHT_RC1_REPORT.md
```

---

## Verdict

**PREFLIGHT_QA = PASS**

Ready to execute Batch002 production run with 30 ON_TOPIC candidates.

Next phase: PAGE VERIFY → AUDIBLE SPEECH CHECK → PERFORMANCE → DOWNLOAD → ASR → TRANSCRIPT QA