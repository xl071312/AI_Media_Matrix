# Issue #6 Phase B0.1 覆盖率短报（FINAL）

## 目的与验收门

B0.1 目标：**检索实读证明（retrieval proof）+ hard-collect 留证**。确认 Phase A 六名候选是否有足够可采样作品，区分唯一 URL、已核验页面与 COMPLETE（作者 UI 匹配；页面可打开；视频可完整播放且可行转写/字幕，或文章正文完整可读）。

**本阶段不做 Phase B 全量采集、不做 Phase C、不做 Voice Profile。** 本稿供 **Lan 验收**；Lan 验收通过前，不进入 Phase B。

状态枚举：
- `READY` = 已有足够 COMPLETE（≥20，且主平台检索证明充分）
- `HARD_COLLECT_OK` = 按 Lan ruling（keep_all_three）保留并允许 hard-collect
- `BELOW_20_DOCUMENTED` = COMPLETE <20 且已留证说明原因，**不得自我替换**

## 六人覆盖表

| creator_id | 创作者 | 主平台 | 主页 | 作品数/可见量 | 粉丝（主页） | unique collected | verified | COMPLETE | 状态 |
|---|---|---|---|---:|---|---:|---:|---:|---|
| `dy_银行小姐姐` | 银行小姐姐 | Douyin | [主页](https://www.douyin.com/user/MS4wLjABAAAAPZgqlIO2MpT0SBcAjLaFbL_c6LvEojAXy1udEgzugQg) | 518 | 186.5万 | 30 | 30 | 30 | **READY** |
| `hanxiuyun_jingji` | 韩秀云讲经济 | Douyin | [主页](https://www.douyin.com/user/MS4wLjABAAAAlbkNTw3vjBlQx6pzhzRnFX1YLHlpCoU8nMpnSKiL6-S0WquIQngezW4Ydt_0DXdk) | 1,588 | 1,295.5万 | 30 | 30 | 30 | **READY** |
| `xiaolin_shuo` | 小Lin说 | Toutiao | [主页](https://www.toutiao.com/c/user/token/MS4wLjABAAAApzhfBgBWoQDePHbhmxcZNZQzTggHQPLBnsl5nzjsrTA/) | 可见卡片12；总数未显示 | 184.0万 | 40 | 40 | 37 | **READY** |
| `zhinan_caijing` | 直男财经 | Douyin | [主页](https://www.douyin.com/user/MS4wLjABAAAADUObyc_aoKXnXnV01JEcZMdvU0_ZFvFnVQAU-weztOgHubCQont1aDrDASxWu8B6) | 1,422 | 2,310.7万 | 57 | 30 | 30 | **HARD_COLLECT_OK** |
| `wenyifei_jijiu` | 温义飞的急救财经 | Toutiao（兼 Douyin） | [Toutiao](https://www.toutiao.com/c/user/token/MS4wLjABAAAA92PXnGCa5PoJxO09OYd14kXBGpRWWHrXJWrmRbiAPXd1RDV10NIzqJlpiPXsv3_j/)；[Douyin](https://www.douyin.com/user/MS4wLjABAAAAPc9V-v4o3BdxwccbI5sPhAF-UPPk86Pkql0L9mHAJDY) | Douyin 517；Toutiao 深滚约40卡 | Toutiao 224.6万；Douyin 1,228.8万 | 95（TT41+DY54） | 24 | 18（TT4+DY14） | **BELOW_20_DOCUMENTED** |
| `banfo_xianren` | 硬核的半佛仙人 | Toutiao | [主页](https://www.toutiao.com/c/user/token/MS4wLjABAAAA5X0VBPDBZMEMapObds7t3Z_5K6V61i3zNDYgSd6uPlM/) | 总数未显示 | 58.4万 | 25 | 25 | 23 | **HARD_COLLECT_OK** |

数字来源：各 `retrieval_summary_*.json` 的 `complete_count` / `complete_confirmed_count` / `complete_total` 字段；温义飞另拆 `complete_toutiao`/`complete_douyin`。

## 口径与 caveats

- **温义飞的急救财经 <20（已留证）**：`complete_total=18`（Douyin 14 + Toutiao 4）。Douyin 主页深滚采集 54 条唯一 `/video/` URL；深化核验中登录弹窗出现后按指令停止，故未能冲到 20。**keep_all_three — 不得自我替换。**
- **硬核的半佛仙人 oral口播 caveat**：23 COMPLETE 全部为 Toutiao **文章**，`full_video_count=0`。文章覆盖 ≠ 视频口播覆盖；后续 Phase B/Voice 需显式处理。
- **Douyin 登录脆弱性**：直男财经本轮依赖 logged-in search（B0 曾 LOGIN_WALL，本轮翻转为可搜）；温义飞深化时再次撞上 login modal。银行小姐姐/韩秀云亦存在 feed/弹窗限制风险。后续采集需预留登录态与重试。
- **小Lin说**：40 核验 / 37 COMPLETE（19 全文 + 18 完整视频）；部分视频核验时黑屏/未缓冲，不可把 40 直接当 COMPLETE。
- **直男财经**：57 唯一 URL，按请求停核验于 30 COMPLETE；互动计数未稳定归一化；状态 `HARD_COLLECT_OK`。

## 对照备选（非替换）

巫师财经 / 夏鹏 / 一鸣财经 / 柏年说政经 = **对照 light-check only**，**不是**替换候选。Lan ruling：**keep_all_three**（直男财经、温义飞、半佛）不得被上述备选顶替。

## 拟定 final 6（Phase A 原六人 + 实读 COMPLETE）

| # | 创作者 | COMPLETE | 状态 |
|---|---|---:|---|
| 1 | 银行小姐姐 | 30 | READY |
| 2 | 韩秀云讲经济 | 30 | READY |
| 3 | 小Lin说 | 37 | READY |
| 4 | 直男财经 | 30 | HARD_COLLECT_OK |
| 5 | 温义飞的急救财经 | 18 | BELOW_20_DOCUMENTED |
| 6 | 硬核的半佛仙人 | 23 | HARD_COLLECT_OK |

**Gate：Lan 验收本包及最终六人后，才能进入 Phase B。当前明确不启动 Phase B、Phase C 或 Voice Profile。**
