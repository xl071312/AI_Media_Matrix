# 济南校外托管线上竞争情报采集包（Issue #2 验收布局）

> **角色边界：** GROK BOT 仅负责采集与结构化。本包**不做**竞品最终排名、**不做**开店结论。请 **ChatGPT / Sol** 基于原始 CSV、截图与 transcript 做商业分析。

- 生成时间（PT）：2026-09-16 00:20 PT
- 仓库：`xl071312/AI_Media_Matrix`
- 目录：`research/jinan_tuoguan_2026/`

## 调研范围

- 地理焦点：济南市槐荫区（兼及市中区泉海参照）
- 学校/片区：营东/营市东街、槐荫实验、杨柳春风、泉新、泉景
- 平台：抖音（指定壹心 + 关键词竞品）、小红书、地图/本地宝/好位置、大众点评（部分）、招聘、政府公开页
- 约束：仅公开可见；不绕过登录/验证码；不发明字段

## 目录映射（新布局）

| 新目录 | 含义 | 旧目录（保留） |
|--------|------|----------------|
| `00_manifest/` | 清单、迁移说明、状态 | 同名 |
| `01_official_registry/` | 官方母表缺口说明 + 莱芜参照 | （新建） |
| `02_institutions_master/` | 机构主档副本 | （新建） |
| `03_douyin_target/` | 指定抖音壹心 | `01_douyin_target/` |
| `04_douyin_competitors/` | 抖音竞品搜索 | `02_douyin_competitors/` |
| `05_xiaohongshu/` | 小红书 | `03_xiaohongshu/` |
| `06_maps_reviews/` | 地图/点评 | `04_maps_reviews/` |
| `07_recruitment/` | 招聘 | `11_labor/` |
| `08_raw_screenshots/` | 截图汇总 | `05_raw_screenshots/` |
| `09_transcripts/` | ASR/文本 | `06_transcripts/` |
| `10_evidence/` | 证据索引 | （新建） |

旧目录 `07_gov` `08_xueyijia` `09_enterprise` `10_rent` `11_labor` `12_ai_eval_pack` 仍保留，供溯源。

## 根目录必交付 CSV / JSON

- `institutions.csv` — 机构主档（仅 A/B；C 级见 unresolved）
- `institution_accounts.csv` — 机构↔社媒账号匹配
- `accounts.csv` / `posts.csv` / `comments.csv`
- `prices.csv` / `services.csv` / `poi.csv`
- `recruitment.csv` / `school_competition.csv`
- `evidence_index.csv` / `unresolved_matches.csv` / `failures.csv`
- `manifest.json` / `README.md`

编码：UTF-8-SIG。

## 完成度 vs 失败项（摘要）

### 已完成（可分析）

- 抖音目标号「壹心托管济南校区」公开主页与部分作品/评论/ASR
- 抖音关键词竞品账号与作品合并表
- 小红书笔记与评论（公开可见）
- POI 种子（本地宝/好位置等）+ 片区密度启发式
- 大众点评部分商户列表/少量详情与评价（验证墙限制）
- 招聘公开岗位样本
- 政府侧：省级托管意见、槐荫培训白名单、目标校公开招生信息
- Issue #2 验收目录与主表主键/匹配置信度字段

### 失败 / 缺口（详见 failures.csv）

- **槐荫证照齐全托管名单 Excel：未找到**（莱芜名单仅作参照模拟）
- 济南/槐荫实施细则未找到
- 大众点评登录/验证墙；美团 404
- 高德/百度详情 SPA 壳
- 抖音同城入口不可用
- 壹心公开电话/标价未展示；部分 ASR/评论不完整
- 校级放学/午休/配餐细则普遍未公开

## 给 ChatGPT / Sol 的使用提示

1. 以 `institutions.csv` + `institution_accounts.csv` 为实体骨架；`match_confidence=A/B` 才可当较实事实，`C` 只在 `unresolved_matches.csv`。
2. 价格/服务必须回溯 `evidence_path` / `source_url` / `screenshot_path`；广告自述 ≠ 已验证。
3. `school_competition.csv` 是启发式计数，不是实地或 API 围栏普查。
4. **请你们输出排名/开店结论**；本包作者不输出。

## 统计快照

```json
{
  "institutions_total": 87,
  "confirmed_social_accounts": 33,
  "douyin_posts": 85,
  "xhs_notes": 15,
  "map_reviews": 7,
  "unresolved_entities": 37,
  "failures": 8,
  "poi_rows": 61,
  "recruitment_rows": 16,
  "evidence_rows": 84,
  "comments_total": 181,
  "accounts_total": 62,
  "school_areas": 5
}
```

## Claude / 自动化工具直链

完整 raw 链接清单见 [`CLAUDE_RAW_LINKS.md`](./CLAUDE_RAW_LINKS.md) / [`CLAUDE_RAW_LINKS.txt`](./CLAUDE_RAW_LINKS.txt)。
