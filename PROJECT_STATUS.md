# PROJECT STATUS

**Last Updated**: 2026-09-08 02:15 GMT+8

---

## PROJECT ROOT

**Current**: `F:\workspace\AI_Media_Matrix`
**Legacy**: `C:\workspace\AI_Media_Matrix` (LEGACY_READ_ONLY)

---

## MIGRATION STATUS

| 项目 | 状态 |
|------|------|
| 文件复制 | ✅ 完成 |
| 环境变量 | ✅ 已设置 |
| 硬编码路径扫描 | ⏸️ 待完成 |
| Smoke Test | ⏸️ 待运行 |

---

## WRITE POLICY

**新数据必须写入**: `F:\workspace\AI_Media_Matrix`
**禁止写入**: `C:\workspace\AI_Media_Matrix`

---

## CURRENT PHASE

**Phase 3.1**: METHOD_VALIDATION_FAIL_REWORK_REQUIRED

- 3条真实Deep Analysis已生成但QA FAIL
- 需要重新生成真实Timed Transcript
- Cross Sample Comparison使用估算值需修正
- Timeline时间轴与实际视频时长不匹配

### 失败原因记录
详见: `09_logs/user_feedback/phase3_1_lan_qa_fail_001.md`

### 阻塞项
- Creator Baseline: BLOCKED_BY_ARGUS (持续)
- ASR质量: 需要人工校验修正
- Timeline: 需要基于真实segment重新生成

---

## DATA ASSETS

| 类型 | 数量 | 路径 |
|------|------|------|
| Raw Pool | 424条 | `01_benchmark/shards/hermes_real/douyin_raw/` |
| Selection | 106条 | `01_benchmark/shards/hermes_real/douyin_benchmark_selection.csv` |
| Deep Batch | 32条 | `01_benchmark/shards/hermes_real/deep_analysis_batch_001.csv` |
| Videos | 24个 | `10_automation/benchmark_collector/MediaCrawler/data/douyin/videos/` |
| Transcripts | 3条 | `01_benchmark/shards/hermes_real/transcripts/` |
| QA Package | 31 files | `01_benchmark/shards/hermes_real/qa_batch_001/` |

---

## HARDWARE NOTES

- GPU: GTX750 (2GB, sm_50) - 无法运行Whisper本地GPU
- Chrome CDP: Port 9223 (douyin_benchmark_v3 profile)
- ASR: faster-whisper base model downloaded

---

*Project migrated from C: to F: on 2026-09-08*
