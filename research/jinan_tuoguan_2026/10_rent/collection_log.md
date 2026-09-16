# Task 8 场地租金 — collection_log

- scrape_date (ISO PT): `2026-09-15T23:09:10-07:00`
- method: WebSearch + WebFetch + curl only (no box browser, no login bypass)
- area intent: ~1km of 营市东街小学 / 槐荫实验·保利华府 / 杨柳春风 / 泉新·泉景园 / 医学中心实验；泉海 reference
- filters: 1–3F 商铺/底商, 80–300㎡, exclude 地下室/半地下室

## Platform blockers

| Platform | Result |
|----------|--------|
| 贝壳 ke.com / beike | **CAPTCHA / 人机验证** on `jn.ke.com/zufang/huaiyin/` — raw sample saved; no listing body |
| 58同城商铺 | **验证码** (`请输入验证码`) on `www.58.com/jn/spcz-*` detail/list curls — kept search-index snippets only |
| 安居客详情多数 | First list page OK; most subsequent detail IDs returned **验证码** after rate limit; one detail (`7538070615`) fully parsed |
| 安居客列表 | `m.anjuke.com/jn/sp/zu/huaiyinqu-huaiyinquqita-yuezujin7/` **200 OK** — primary structured source |
| 指点网 shangpu99 | **200 OK** full detail |
| 济南闪铺网 | **200 OK** full details (supplemental; not in original platform list but public) |

## Counts

- listings.jsonl total records: 19
- rent.csv useful (fit_filter=True): 17
- raw HTML samples: `10_rent/raw_html/` (18 files)

## Notes

- Exact ~1km school-radius matching is approximate from address text (no map geocode API this pass).
- Many “面议” rents; priced samples in 西客站/经十西路 roughly **~23–55 元/㎡/月** when calculable.
- 泉景园拐角 25㎡ listing kept in jsonl as excluded rent-per-sqm reference only.
