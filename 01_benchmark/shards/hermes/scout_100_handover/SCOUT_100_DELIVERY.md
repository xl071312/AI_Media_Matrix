# 观屿 Scout 100 — 数据交接交付

> 本文件为已有侦察结果的交接导出；**未重新 Discovery**，未编造字段，未做 Hook/Logic/Voice/爆款分析。

## 报告指标

- total_new_samples: **108**
- duplicates: **4** (uncertain_duplicate: 0)
- real_spoken: **103**
- first30_available: **87**
- ordinary_person_bucket: **99**
- small_account_high_performance: **11**

## 文件

- `candidates.csv` — 机器可读主表（英文字段 + 原样事实列）
- `candidates_zh_backup.csv` — 交接前中文表头备份（事实不变）
- `raw_hits.jsonl` — 原始命中日志

## 主题桶（仅 new）

- money_income: 39
- workplace_salary: 19
- side_startup: 17
- consume_life: 14
- ai_ordinary: 10
- other_oral: 9

## discovery_source Top（仅 new）

- 为什么赚不到钱: 37
- AI对普通人: 7
- 副业到底怎么做: 5
- 中产返贫: 5
- 月薪10000什么水平: 5
- 月薪三千: 5
- 存款焦虑: 5
- 工资5000: 4
- 说白了 工资: 4
- 工资低怎么办: 4
- 很多人不知道 赚钱: 4
- 菜市场赚钱: 3
- 房租太贵: 3
- 我给你算一笔账 赚钱: 3
- AI副业普通人: 2

## 一致性

- 与此前交付的有效新样本数一致目标：**108**；本导出 new 行数：**108**
- CSV 数据行数（含 duplicate）：**112**
- sample_id 集合来自既有 scout 结果映射，未新增样本。
