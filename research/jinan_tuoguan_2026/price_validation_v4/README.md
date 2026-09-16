# Issue #5 真实收费核验 v4

更新：2026-09-16T05:38:46-07:00

## 硬结论
三片区公开渠道 **正式月费样本 = 0**。
现有 23 条价格行：口述 13、历史旧价 10、体验/团购 0。
因此 `area_price_summary` 全部 `insufficient_for_market_median=1`，禁止写「市场平均价」。

## 固定店模型
`fixed_store_sensitivity.csv`：280 个场景；面积固定 320/350/380/400㎡，不随学生缩小；assumption_flag=model_assumption。
因缺真实正式月费，ARPU 仅为情景假设，不能称为已核验市场价。

## 片区
泉新/绿地泉景园、营市东街（东/西校区线索）、杨柳春风。
