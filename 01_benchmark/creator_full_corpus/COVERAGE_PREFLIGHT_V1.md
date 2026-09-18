# COVERAGE_PREFLIGHT_V1 — Issue #6 Phase B0

> 状态：完成预检，待 Lan / ChatGPT 决定是否替换后进入正式 Phase B  
> 执行：HERMES 页面实读证据 + 库内索引对照  
> 证据：`01_benchmark/creator_full_corpus/coverage_evidence_b0.jsonl` 与 `shards/hermes/issue6_b0/coverage_evidence.jsonl`  
> 禁止项遵守：未做风格定型 / 语言指纹 / Voice Profile / 新口播稿

## 门槛
- READY：完整有效预计 ≥30
- READY_WITH_LIMITATIONS：20–29
- REPLACE_RECOMMENDED：<20 或 PRIMARY 平台本轮不可达

完整有效 = 视频可播且可做完整逐字稿，或图文完整正文可读。标题/摘要/首30秒/搜索片段/AI总结 **不计**。

## 六人结论

### 银行小姐姐 (`dy_银行小姐姐`)
- PRIMARY：`douyin`
- homepage_access：OK
- visible_total：518
- indexed_work_count：2
- full_video_available（本轮实样）：3
- full_article_available（本轮实样）：0
- complete_effective_estimate：518
- performance_metrics_available（本轮）：1
- access_limit：login_qr_modal_on_load; feed_cards_not_scrollable_this_session
- **coverage_status：`READY`**
- notes：Douyin homepage UI showed 作品518; 3 seeds playable with caption. Full corpus scrape still needs login-stable feed crawl.

### 直男财经 (`zhinan_caijing`)
- PRIMARY：`douyin`
- homepage_access：LOGIN_WALL
- visible_total：NULL
- indexed_work_count：8
- full_video_available（本轮实样）：0
- full_article_available（本轮实样）：0
- complete_effective_estimate：0
- performance_metrics_available（本轮）：0
- access_limit：douyin_search_login_wall; seed_video_unavailable
- **coverage_status：`REPLACE_RECOMMENDED`**
- replace_reason：PRIMARY抖音本轮无法打开主页/作品；种子视频不存在；已索引8条亦缺互动指标
- notes：Suggest light-check alternates: 巫师财经 / 一鸣财经

### 温义飞的急救财经 (`wenyifei_jijiu`)
- PRIMARY：`toutiao`
- homepage_access：OK_TOUTIAO_DOUYIN_BLOCKED
- visible_total：12
- indexed_work_count：9
- full_video_available（本轮实样）：0
- full_article_available（本轮实样）：1
- complete_effective_estimate：12
- performance_metrics_available（本轮）：1
- access_limit：douyin_login_wall; douyin_seed_author_mismatch; toutiao_feed_12_cards_no_total
- **coverage_status：`REPLACE_RECOMMENDED`**
- replace_reason：PRIMARY抖音不可用；头条可见卡片仅约12，完整有效预计<20
- notes：B站AUX另有索引3条，不得主导 Voice Profile。备选轻查：巫师财经、夏鹏

### 韩秀云讲经济 (`hanxiuyun_jingji`)
- PRIMARY：`douyin`
- homepage_access：OK
- visible_total：1588
- indexed_work_count：10
- full_video_available（本轮实样）：4
- full_article_available（本轮实样）：0
- complete_effective_estimate：1588
- performance_metrics_available（本轮）：0
- access_limit：login_qr_modal; feed_not_scrollable; toutiao_seed_author_mismatch
- **coverage_status：`READY`**
- notes：Douyin header 作品1588; 4 videos playable with caption. Metrics often hidden behind modal.

### 小Lin说 (`xiaolin_shuo`)
- PRIMARY：`toutiao`
- homepage_access：OK_TOUTIAO_DOUYIN_BLOCKED
- visible_total：12
- indexed_work_count：31
- full_video_available（本轮实样）：0
- full_article_available（本轮实样）：2
- complete_effective_estimate：20
- performance_metrics_available（本轮）：2
- access_limit：douyin_login_wall; toutiao_feed_12_cards_visible_no_total; bilibili_AUX_indexed_9_not_primary
- **coverage_status：`READY_WITH_LIMITATIONS`**
- notes：PRIMARY完整有效预计约20（边界）；抖音本轮不可采；B站库内更多但仅AUX。建议Phase B先清头条全文再攻抖音登录。

### 硬核的半佛仙人 (`banfo_xianren`)
- PRIMARY：`toutiao`
- homepage_access：OK
- visible_total：12
- indexed_work_count：28
- full_video_available（本轮实样）：0
- full_article_available（本轮实样）：2
- complete_effective_estimate：13
- performance_metrics_available（本轮）：2
- access_limit：toutiao_display_name=半佛仙人本仙人; feed_12_no_total; bilibili_AUX_has_more
- **coverage_status：`REPLACE_RECOMMENDED`**
- replace_reason：PRIMARY头条本轮可见约12、库内约13，完整有效预计<20；B站AUX虽多但不得主导
- notes：备选轻查：巫师财经（库内头条约20）。是否换人交 Lan 决定。

## 建议替换
有
- 原人：直男财经 → 建议备选见下；原因：PRIMARY抖音本轮无法打开主页/作品；种子视频不存在；已索引8条亦缺互动指标
- 原人：温义飞的急救财经 → 建议备选见下；原因：PRIMARY抖音不可用；头条可见卡片仅约12，完整有效预计<20
- 原人：硬核的半佛仙人 → 建议备选见下；原因：PRIMARY头条本轮可见约12、库内约13，完整有效预计<20；B站AUX虽多但不得主导

## 备选轻量检查（仅库内索引，未新开全页）
- 巫师财经: index_hit_names=['巫师财经']; indexed≈23; plats={'bilibili': 2, 'douyin': 1, 'toutiao': 20} (LIGHT INDEX ONLY, no fresh page crawl)
- 夏鹏: index_hit_names=['夏鹏']; indexed≈2; plats={'douyin': 1, 'toutiao': 1} (LIGHT INDEX ONLY, no fresh page crawl)
- 一鸣财经: index_hit_names=['一鸣财经']; indexed≈1; plats={'douyin': 1} (LIGHT INDEX ONLY, no fresh page crawl)
- 柏年说政经: index_hit_names=['柏年说政经']; indexed≈5; plats={'douyin': 4, 'toutiao': 1} (LIGHT INDEX ONLY, no fresh page crawl)

## 需要 HERMES 继续协助的 creator/platform
- 银行小姐姐 / douyin：登录稳态下滚动抓取作品 URL 清单（目标≥30 完整）
- 韩秀云讲经济 / douyin：同上，作品清单与指标实读
- 小Lin说 / toutiao：滚动补全文章/视频清单与全文；douyin 需登录后补 PRIMARY
- 若 Lan 保留温义飞：toutiao 深滚 + 找回正确抖音主页
- 若 Lan 保留半佛：toutiao 深滚；B站仅 AUX
- 直男财经：除非获得抖音登录会话，否则不投入全量采集

## 是否可进入正式 Phase B（全 6 人）
**NO** — 3 人 REPLACE_RECOMMENDED（直男财经、温义飞、半佛），需 Lan 决定换人后再开全员 Phase B。

可先行（可选）：对 READY 二人（银行小姐姐、韩秀云）启动有限 Phase B 采集；小Lin说按 READY_WITH_LIMITATIONS 谨慎开头条全文采集。

## 原始证据摘要
- 银行小姐姐 | Douyin | access=OK | visible=518 | samples=3
- 直男财经 / 胡彬讲财经 | Douyin | access=LOGIN_WALL | visible=None | samples=1
- 温义飞的急救财经 | Douyin | access=ACCESS_LIMITED | visible=None | samples=1
- 温义飞的急救财经 | Toutiao | access=OK | visible=None | samples=1
- 韩秀云讲经济 | Douyin | access=OK | visible=1588 | samples=4
- 韩秀云讲经济 | Toutiao | access=ACCESS_LIMITED | visible=None | samples=1
- 小Lin说 | Douyin | access=LOGIN_WALL | visible=None | samples=0
- 小Lin说 | Toutiao | access=OK | visible=None | samples=2
- 硬核的半佛仙人 | Toutiao | access=OK | visible=None | samples=2