# Task 9 人工成本 — collection_log

- scrape_date (ISO PT): `2026-09-15T23:09:10-07:00`
- method: WebSearch + WebFetch + curl only (no box browser, no login bypass)
- queries: 济南 托管老师 / 生活老师 / 托管厨师 / 课后辅导老师
- target platforms: BOSS直聘, 58同城（智联等公开索引作补充并标注）

## Platform blockers

| Platform | Result |
|----------|--------|
| BOSS直聘 zhipin.com | **JS/security wall** (`请稍候 - BOSS直聘`) on list URLs — no job body via curl; kept WebSearch index snippets |
| 智联招聘 zhaopin.com | **Tencent EdgeOne Security Verification** captcha on jobdetail curls — kept search-index snippets (incl. 槐荫岗位) |
| 58同城招聘 m.58.com | **Partial success** — 5 job detail pages returned parseable JSON fields (title/salary/address/company) |

## Salary band summary (from captured rows)

- 托管/辅导老师全职常见：**2000–6000 元/月**；槐荫索引样本约 **3000–6000**
- 督学/晚辅综合偏高：**6000–9000+**（部分综合至 12K）
- 生活老师：**约 3000–4000**
- 托管厨师：**约 4000–5500**（样本至 5000–6000 标题区间）
- 兼职辅导向：**80–140 元/天** 或按时薪

## Counts

- jobs.jsonl / labor.csv records: 16
- raw HTML samples: `11_labor/raw_html/` (11 files)
