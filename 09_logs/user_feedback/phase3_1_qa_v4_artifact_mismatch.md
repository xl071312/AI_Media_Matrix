# Phase 3.1 QA V4 Fail Report - Artifact Mismatch

**时间**: 2026-09-08 08:00 GMT+8
**问题类型**: REPORT/ARTIFACT MISMATCH

---

## 错误描述

**汇报声称**:
- Sample 1: units=5
- Sample 2: units=5
- Sample 3: units=10

**实际Artifact显示**:
- Sample 1: Spoken Units=1
- Sample 2: Spoken Units=1
- Sample 3: Spoken Units=1

---

## 根本原因

Pipeline V3的Spoken Unit聚合算法失败：
- 算法将所有ASR segments合并成1个unit
- 阈值设置不当（pause > 0.5s才split）
- 未考虑中文口语的自然边界

---

## 修正措施

1. 废止当前Spoken Unit Aggregator
2. 重新设计三层结构：ASR Segment → Spoken Unit → Cognitive Block
3. 硬保护：任何Unit duration > 25秒自动FAIL
4. 当前只处理Sample 02单样本单元测试
5. 所有汇报数字必须直接从最终artifact解析生成

---

## 状态

PIPELINE_QA = FAIL
METHOD_VALIDATION = FAIL_REWORK
STATUS = SAMPLE_02_UNIT_TEST_ONLY
