# Issue #5 price_validation_v4 collection log

- Crawl window: 2026-09-16 PT (~05:26–05:40)
- Scope: 泉新学校 / 绿地泉景园 | 营市东街小学 | 杨柳春风学校 ONLY
- Tag discipline: 泉新/绿地泉景园 NOT merged with 泉景小学/中学
- Rules: no fake phone scripts; no captcha/login bypass; no final ranking; historical only with price_kind=历史旧价 & old=1

## Row counts
- named_current_prices.csv: **23**
- service_scope_comparison.csv: **24**
- failures.csv: **25**
- price_evidence_pack.csv: **12**

## Overall price_kind mix (named_current_prices)
- formal monthly family: **0**
- trial/groupbuy/promo family: **0**
- oral (评论口述价): **13**
- historical (历史旧价/old=1): **10**

## Per-area counts
### 泉新学校
- price rows: 1 | formal: 0 | trial/groupbuy: 0 | oral: 1 | historical: 0
- named institutions in service_scope_comparison: 4 — 金苹果小饭桌, 新星小饭桌, 博乐少儿托管所中心, 槐荫小石头托管中心

### 绿地泉景园
- price rows: 8 | formal: 0 | trial/groupbuy: 0 | oral: 4 | historical: 4
- named institutions in service_scope_comparison: 6 — 金苹果小饭桌, 新星小饭桌, 博乐少儿托管所中心, 槐荫小石头托管中心, 槐荫函函托管中心, 远航教育(绿地泉景园校区)

### 营市东街小学
- price rows: 8 | formal: 0 | trial/groupbuy: 0 | oral: 4 | historical: 4
- named institutions in service_scope_comparison: 10 — 天天小饭桌, 金牌小饭桌, 朵朵小饭桌, 快乐作文小饭桌, 爱心托管, 平平小饭桌, 放心托教, 阳光托教, 花儿朵朵托辅中心, 致远托管

### 杨柳春风学校
- price rows: 6 | formal: 0 | trial/groupbuy: 0 | oral: 4 | historical: 2
- named institutions in service_scope_comparison: 4 — 真爱小饭桌, 锦绣放心小饭桌, 杨柳春风×济南青少年宫暑期托管, 依春然托管

## Key findings
1. **Zero** public **具名门店正式月费** for the three core areas in this pass.
2. Current (2025) signals are mainly **小红书口述**: 槐荫≈900；济南午餐750 / 综合≈1100 / 午托450 — all `评论口述价`, confidence=low (live note 页面不见了; kept via comments.csv + screenshot).
3. Named brands near 绿地泉景园 (金苹果/新星/博乐/小石头/函函): address/list only → failures (no fee).
4. 营东周边 (天天/金牌/朵朵/阳光/花儿朵朵/致远等): presence only; campus_note 东校区/西校区 where address allows.
5. 杨柳 (真爱/锦绣放心/青少年宫/依春然): no public numeric monthly; 17800学期为西客站探店口述弱关联.
6. 贝尔安亲点评团购: login wall + 王官庄/泉景名 mismatch → not retagged into core.
7. 花锦时代880 (槐荫实验附近): excluded from core three.
8. Insufficient for market median of formal monthly; do not invent phone consults.

## Artifacts
- Raw: `01_quanxin/raw`, `02_yingshidongjie/raw`, `03_yangliu/raw`, `06_failures/raw`
- Screenshots: `*/screenshots`
- Required CSVs: UTF-8-SIG
