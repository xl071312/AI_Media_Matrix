# Task 5 — Government sites collection log

- **scrape_date (PT):** 2026-09-16
- **local ISO:** 2026-09-16T00:00:00-07:00
- **method:** WebSearch + WebFetch + curl only（无 box browser、无登录绕过）
- **output root:** `/workspace/AI_Media_Matrix/research/jinan_tuoguan_2026/07_gov/`

## 1. 校外托管机构证照齐全名单（重点）

| 目标 | 结果 |
|------|------|
| 济南市市场监管局 / 槐荫区政府 托管名单 | **未找到**公开 Excel/PDF |
| 传闻槐荫 Excel ~2026-03 | **未证实**；公开索引无附件 |
| 同市参照 | **莱芜区**市场监管局公示《证照齐全校外托管机构名单》109家（83供餐/26不供餐），见 `raw/laiwu_163_roster.html`（网易转载，**无原 Excel 下载**） |
| `07_gov/downloads/` | 空（无原始 Excel/PDF 可下） |

## 2. 槐荫区教体局 2026 校外培训机构白/黑名单

| 文件 | 状态 |
|------|------|
| 2026-05 白名单 | **已存** `raw/huaiyin_whitelist_202605.html`（解析约 222 行 / 最大序号 165） |
| 2026-04 白名单 | **已存** `raw/huaiyin_whitelist_202604.html` |
| 2026-03 白名单 | **已存** `raw/huaiyin_whitelist_202603.html` |
| 2025-12 黑名单 | URL 公开可检索；**curl 多次失败(000)**；13家名单写入 `findings.jsonl`（来自搜索摘要） |
| 市局 2026-03 汇总 | 槐荫：白165 / 重点监督7 / 黑13；jnedu 页 curl/WebFetch **404/000** |

**重要区分：** 培训机构黑白名单 ≠ 校外托管（小饭桌）证照名单。

## 3. 鲁政办发〔2026〕8号 落地情况

- **省级意见全文：** 已存 `raw/luzhengbanfa_2026_8_zibo.html`（+舜网新闻稿）
- **施行：** 2026-09-16 → 2031-09-15；省市场监管局牵头
- **济南市 / 槐荫区实施细则、通知、Q&A：** **公开检索未发现**
- 舜网观察稿：`raw/e23_xiaofanzhuo_policy.html`

## 4. 12345 / 爱济南

- 专项“校外托管/午休”答复全文：**未找到**
- 已存：`raw/jinan_12345_huaiyin_edu.html`（教育领域12345沟通报道）
- 已存：`raw/huaiyin_afterschool_thirdparty.html`（第三方课后服务规范，2025-06-20）

## 5. 目标学校

见 `schools_public_info.csv`。关键命中：
- 营市东街小学 2025 在校生 **2169**、教职工 **131**、东西校区
- 2026 小学招生计划班数/学位：营东 8/360；实验 4/180；杨柳春风 6/270；泉新 12/540；医学中心 7/315
- 泉新 2026 学区小区：**绿地泉景园、绿地国际花都、绿地泉景嘉园**
- 普遍缺失：放学时间、午休、食堂/配餐校级细则

## Raw HTML inventory

- `e23_luzheng_news.html` (42823 bytes)
- `e23_policy_mass.html` (26822 bytes)
- `e23_xiaofanzhuo_policy.html` (36817 bytes)
- `huaiyin_afterschool_thirdparty.html` (50400 bytes)
- `huaiyin_enroll_plan_2026.html` (166950 bytes)
- `huaiyin_whitelist_202603.html` (992888 bytes)
- `huaiyin_whitelist_202604.html` (978500 bytes)
- `huaiyin_whitelist_202605.html` (1029836 bytes)
- `huaiyin_zhifei_table.html` (75048 bytes)
- `jinan_12345_huaiyin_edu.html` (211697 bytes)
- `jinantimes_enroll_2026.html` (18304 bytes)
- `laiwu_163_roster.html` (182185 bytes)
- `luzhengbanfa_2026_8_zibo.html` (29651 bytes)
- `quanhai_enroll_2025.html` (33116 bytes)
- `quanxin_enroll_2026.html` (36731 bytes)
- `school_directory_2025.html` (155705 bytes)
- `yangliu_plan_2024.html` (48055 bytes)
- `yangliuchunfeng_plan.html` (105777 bytes)
- `yingshi_stats_2025.html` (25276 bytes)
- `yixuezhongxin_workpoints.html` (106963 bytes)

## Blocked / failed fetches

| URL / target | Issue |
|--------------|-------|
| jnedu.jinan.gov.cn 黑白名单汇总 | WebFetch 404；curl 000 |
| 槐荫 2025-12 黑名单 HTML | curl 000（反复） |
| 营市东街收费举报公告 | curl 000 |
| jnedu 2023 托管提案答复 | curl 000 |
| 槐荫站内搜索 校外托管 | curl 000 |
| 爱企查/天眼查全文 | 未付费爬取（见 Task4 lite） |

## Deliverables

- `collection_log.md`（本文件）
- `findings.jsonl`
- `schools_public_info.csv`（UTF-8-SIG）
- `raw/*.html`
- `downloads/`（无 Excel/PDF）
