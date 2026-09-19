# PHASE_B_DELIVERY — Issue #6 (for Lan / ChatGPT)

Updated: 2026-09-19T02:23:50.347029+00:00

## 1. 六人各自可见作品数 (homepage UI)
| 创作者 | 可见作品数 |
|---|---:|
| 银行小姐姐 | 518 |
| 直男财经 | 1422 |
| 温义飞的急救财经 | 头条可见文章卡片约 20（Douyin 主页本轮空白） |
| 韩秀云讲经济 | 1588 |
| 小Lin说 | 主页卡片切片（inventory 51，非全历史） |
| 硬核的半佛仙人 | 深滚后可见卡片 12 |

## 2. 实际采集数 (inventory / opened raw)
| 创作者 | inventory | opened/raw |
|---|---:|---:|
| 银行小姐姐 | 61 | 15–16 |
| 直男财经 | 57 | 15 |
| 温义飞的急救财经 | 37 | 37 |
| 韩秀云讲经济 | 177 | 30 |
| 小Lin说 | 51 | 40 |
| 硬核的半佛仙人 | 25 | 25 |

## 3. COMPLETE 数
| 创作者 | COMPLETE |
|---|---:|
| 银行小姐姐 | 0 |
| 直男财经 | 0 |
| 温义飞的急救财经 | 22 |
| 韩秀云讲经济 | 0 |
| 小Lin说 | 20 |
| 硬核的半佛仙人 | 25 |
| **合计** | **67** |

## 4. 完整逐字稿 / 全文数
= COMPLETE 列（67 份已写入 `transcripts/`；抖音口播 0）

## 5. excluded 数
银行0 + 直男0 + 温义飞6 + 韩秀云0 + 小Lin3 + 半佛2 = **11**

## 6. failed 数
银行小姐姐 **16**（ui_transcript / no panel）；其余创作者本轮 **0**

## 7. coverage 缺口
1. **抖音口播完整逐字稿全线受阻**：无全文文案面板 + yt-dlp HTTP 403；未伪造 ASR。
2. 抖音主页深滚仅能加载可见网格切片，**可见作品数 ≠ 可取得全历史**。
3. 温义飞 Douyin 主页本轮空白；视频 15 条保留为非 COMPLETE。
4. 小Lin说视频无全文文案；11 URL 因 session cap 未开。
5. 半佛为图文，**不得**计入口语助词/节奏统计。

## 8. 路径
`01_benchmark/creator_full_corpus/`
- `yinhang_xiaojiejie/` `zhinan_caijing/` `wenyifei_jijiu/` `hanxiuyun_jingji/` `xiaolin_shuo/` `banfo_xianren/`
- 每人：`corpus_index.csv` `raw/` `transcripts/` `excluded.csv` `CORPUS_COVERAGE.md`
- 汇总：`_aggregate/CORPUS_COVERAGE_ROLLUP.md` `_aggregate/PHASE_B_DELIVERY.md`

## 9. Commit SHA
217abe726d00978c24469a32ea1bf8c96067886b

## 10. Issue 评论链接
https://github.com/xl071312/AI_Media_Matrix/issues/6#issuecomment-5738585992

## Stop
Phase B 机械采集交付到此为止；**等待 Lan / ChatGPT 验收**。未进入 Phase C / Voice Profile / 新口播稿。
