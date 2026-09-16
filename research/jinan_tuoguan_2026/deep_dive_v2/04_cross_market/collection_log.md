# deep_dive_v2 collection_log

collected_at: 2026-09-16T01:58:17-07:00 (PT)
method: WebSearch / WebFetch / curl only. No ComputerUse. No login bypass. No symlinks.

## Row counts
| file | rows |
|------|------|
| current_prices_2026.csv | 23 |
| core_competitors.csv | 25 |
| school_facts.csv | 7 |
| local_rent_2026.csv | 11 |
| labor_cost_2026.csv | 16 |
| parent_demand_signals.csv | 5 |
| unresolved_matches.csv | 4 |
| failures.csv | 9 |

## Area tag discipline applied
- 绿地泉景园门店 (金苹果/新星/博乐) ≠ 泉新学校社交账号
- 阳光100住址门店 → 阳光100参照
- 壹心 → 泉海参照 only
- 贝尔安亲(泉景校区) → unresolved_matches (店名/地址冲突)

## Price_kind mix
月费/体验价/首月优惠/团购价/评论口述价/历史旧价 已分列；2016-2018价一律 历史旧价。

## Still missing (honest)
1. **泉新学校 / 绿地泉景园 / 杨柳春风** 现行可比月费仍远低于「≥5/区」目标（公开站无店家2026价目）
2. **泉景小学/中学** 具名在营机构+月费不足
3. **dismissal_time / afterschool_end** 官方未公开 → status_flag=not_publicly_found
4. 泉新校门 **100-300㎡带明确月租** 商铺样本不足
5. screenshot_path 大多为空（无浏览器）；raw HTML 已落盘

## Parallel batch2_premium
See ../batch2_premium/collection_log.md (壹心/贝尔/小火竹等 + 学区房价 + 合规 + 成本)。
