# QUARANTINE_REASON.md

**隔离时间**: 2026-09-06 20:45 GMT+8
**隔离原因**: VIOLATES_REAL_ONLY_RULE

## 隔离内容

- `douyin_search_result.json` — 8条B站视频数据，非抖音数据

## 违规说明

该数据违反了以下规则：
1. ❌ 使用B站替代抖音（任务要求明确禁止）
2. ❌ 平台字段标注为"Bilibili"但notes写"Douyin blocked"
3. ❌ 数据来源不符合REAL-ONLY原则

## 禁止用途

- 不得进入正式Benchmark库
- 不得用于高赞统计
- 不得用于Voice Profile
- 不得用于平台规律分析
- 不得用于Emerging Viral判定
- 不得用于Deep Analysis

## 恢复方式

如需使用，必须由人工验证抖音真实URL和真实互动数据，
并更新platform、url、evidence_url字段为抖音实际内容。

---
*Quarantined by Hermes REAL-ONLY Collector v2.2*
