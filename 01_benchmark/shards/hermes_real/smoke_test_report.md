# 【HERMES MediaCrawler Smoke Test Report】

**时间**: 2026-09-06 23:26:03
**关键词**: 赚钱逻辑

---

## 运行环境

| 项目 | 值 |
|------|-----|
| 运行Host | Windows (真实Chrome) |
| Chrome版本 | 152.0.7977.76 |
| CDP端口 | 9222 |
| CDP状态 | 已连接 |
| 登录状态 | 已登录抖音 |

---

## Smoke Test结果

| 指标 | 数量 |
|------|------|
| 采集作品 | 28 |
| 有点赞数 | 28 |
| 有评论数 | 28 |
| 有收藏数 | 28 |
| 有分享数 | 28 |
| performance_verified | 28 |
| 验证码触发 | 0次 |

---

## 通过标准

- [x] 采集到5-10条真实作品 ✅
- [x] 包含真实liked_count ✅
- [x] 包含真实comment_count ✅
- [x] 包含真实aweme_url ✅
- [x] 无验证码阻塞 ✅

**结果**: PASS

---

## 输出文件

- 原始数据: `data/douyin/search_contents_2026-09-06.jsonl`
- 转换数据: `C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real\douyin_real_batch_001.csv`
- 本报告: `C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real\smoke_test_report.md`

---

*Hermes Benchmark Collector v3.0 - MediaCrawler Smoke Test*
