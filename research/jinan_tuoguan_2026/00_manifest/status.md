# 济南托管调研 v1 状态

更新时间：2026-09-15 23:12 PDT（仅整理已有文件，未启动新网页抓取）

## 本次更新

- `comments.csv`：从 `01_douyin_target/comments/*.json` 重建；10 个 JSON、77 条抖音评论/回复，连同原有 2 条百度引文共 79 行数据；UTF-8-SIG。
- `posts.csv`：改为仅从 `01_douyin_target/videos_meta/works_detail_partial.jsonl` 刷新，18 行数据。
- `济南托管调研_v1.xlsx`：`任务1_抖音竞品` 更新为 18 行，并加入已采集评论行数及价格/地址/名额/负面标记；新增 `任务1_抽取字段`，其他工作表保留。
- `任务8_场地租金`：从 `10_rent/rent.csv` 填入 17 行；其中 5 行有明确月租并计算单位租金，12 行保留“面议”。来源链接、楼层、餐饮/燃气、近校提示和数据质量写入备注。
- `任务9_人工成本`：从 `11_labor/labor.csv` 填入 16 行；保留岗位、薪资区间、区域、来源链接，以及公司、要求、工作时间和数据质量。
- 根目录 `manifest.json` 与 `00_manifest/manifest.json`：新增 rent/labor 进度记录并更新更新时间。

## 当前阻塞/缺口

- 大众点评、美团：登录/验证墙、403/404，未取得可读店铺/评论数据。
- 政府：济南/槐荫校外托管证照齐全名单及专门实施细则未找到；学校放学时间、午休、校级配餐细则普遍未公开。
- 学一家：精确品牌未公开命中；官网遇 JS challenge/跳转壳，价格、加盟与济南门店未能官方核验。
- 场地租金：主表中 12/17 条为“面议”，未公开可计算的月租；另有 2 条 JSONL 候选因不完整或面积低于主分析筛选条件未纳入主表。
- 人工成本：部分岗位为搜索摘要，详情页存在验证/JS 墙，需线下或公开详情进一步核验。


## Task7 Douyin competitors (2026-09-16T06:22:14.463824+00:00)
- accounts: 62 unique
- posts sampled: 79
- keywords: 11
- 同城 web entry: unavailable; search used
- blocker: 泉海托管 user page login popup (saved)
