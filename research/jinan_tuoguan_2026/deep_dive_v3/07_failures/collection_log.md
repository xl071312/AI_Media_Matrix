# Issue #4 deep_dive_v3 collection log

- **crawl_time (PT):** 2026-09-16T04:46:32-07:00
- **method:** PUBLIC WebSearch / WebFetch / curl only（无登录绕过、无验证码破解、无最终选址排名、无容量公式发明）
- **output:** `/workspace/AI_Media_Matrix/research/jinan_tuoguan_2026/deep_dive_v3/`

## Row counts

| File | Rows |
|------|------|
| yingshidongjie_deep_dive.csv | 41 |
| venue_capacity_samples.csv | 16 (both area+students=16; Shandong-ish=1) |
| renovation_cost_samples.csv | 15 |
| large_space_rent_samples.csv | 20 |
| regulation_space_requirements.csv | 8 |
| failures.csv | 10 |

### Rent coverage by (school_area, band)
```
{('杨柳春风', '250-350'): 3, ('杨柳春风', '350-450'): 2, ('杨柳春风', '450-600'): 2, ('营市东街', '250-350'): 2, ('营市东街', '350-450'): 2, ('营市东街', '450-600'): 2, ('泉新', '250-350'): 1, ('泉新', '350-450'): 1, ('泉新', '450-600'): 1, ('泉景', '250-350'): 2, ('泉景', '350-450'): 1, ('泉景', '450-600'): 1}
```

## A. 营市东街
- 2026: 8班 / 45人 / 360学位（区计划）
- 2025: 在校生2169；东西双校区；教室50
- 午餐/午休/放学：校级未公开
- 附近托管：复用 v1 POI/点评/抖音并 re-tag；未假装2026证照核验
- 价格按 price_kind；历史价 old=1

## B. Capacity（关键）
- 16 条同时含面积 + actual/claimed 人数
- 含口述/brand_claim/装修方案/新华社实测/贝尔安亲加盟档（多数容量 estimated）/挤占案例
- 济南本地实测双字段仍缺口（F_003）；壹心无面积人数（F_004）

## C. Renovation
- 加盟单价800–1000元/㎡；资讯站隐含1500–2000；午休床/桌椅口述齐全
- 缺口：新风、济南专项招标㎡价、厨房固定套餐、监控单列

## D. Large rent
- 四片区有样本；泉新/泉景多 stale 招商盘分档或低于250对照
- raw 在 `05_large_rent/raw/`

## E. Regulation
- 鲁政办发〔2026〕8号：**生均面积 not_specified_in_current_rule**
- 餐饮区<50㎡→小餐饮登记等明确
- 济南/槐荫细则未找到
- 2019培训3㎡/生：明确不可套用托管
- 海口/深圳4㎡：仅外省规划参照

## Gaps
1. 营东2026真月费与校级午休放学
2. 山东门店面积×在托人数实测
3. 泉景/泉新独立挂牌租金核验
4. 济南装修招标/新风/厨房价目
5. 市/区托管实施细则若公示需补抓


## Update 2026-09-16T04:47:36-07:00
- Appended CAP_017 济南爱家乐450平+小班10-15; CAP_018济南贝尔安亲档位占位(强estimated); CAP_019/020 海口/深圳4㎡反推规划参照
- venue_capacity_samples now **20** rows; Shandong-ish≈3
