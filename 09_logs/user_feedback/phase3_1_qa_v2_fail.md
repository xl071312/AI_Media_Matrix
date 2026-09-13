# Phase 3.1 QA V2 Fail Report

**提交时间**: 2026-09-08 04:30 GMT+8
**验收结果**: FAIL
**原因**: 分析链问题（非采集链）

---

## 失败项清单

### FAIL-01: Sample 03不存在于Review Bundle
**问题**: LAN_REVIEW_BUNDLE_V2.md只包含Sample 01和02
**影响**: 无法验收第三条样本
**修正**: 重新生成完整Bundle包含3条样本

### FAIL-02: Sample 01 Timeline与真实ASR segment错位
**问题**: Timeline引用错误segment
- 真实: 02.04–05.32 "普通人该怎么赚到自己的第一桶"
- Timeline却使用: "这个视频你吸收的越多"
**影响**: Timeline与Transcript不一致
**修正**: 每个Timeline节点必须绑定source_segment_ids

### FAIL-03: Sample 02 Timeline同样segment错位
**问题**: 
- 真实: 02.92–05.72 "一边找一个靠谱的产品去卖"
- Timeline却引用: "只要是开始卖东西"
**影响**: Timeline错误引用transcript内容
**修正**: 程序直接拼接source_segment_ids对应text

### FAIL-04: Sample 02 Logic Map复制Sample 01
**问题**: Sample 02真实主题"打工→卖货→商业社会→确定性"，但Logic Map写"从1到100万→三条路→第一桶金→伪创业→轻资产"
**影响**: 跨样本污染
**修正**: 每个Logic Map必须独立基于自身Transcript生成

### FAIL-05: Sample 01 Metrics sentence_count=1错误
**问题**: sentence_count=1, avg_sentence_chars=863
**影响**: 无研究意义
**修正**: 废除标点分割句子算法，改用spoken_unit（口语意群）

### FAIL-06: Sample 02 Metrics同样错误
**问题**: sentence_count=1, avg_sentence_chars=864
**修正**: 同FAIL-05

### FAIL-07: Question检测错误
**问题**: Sample 02存在明显问句"那为什么不建议打工呢""客户为什么会离去"，但question_count=0
**修正**: Question Detector检测关键词+语义判断

### FAIL-08: Normalized Transcript存在ASR错误
**问题**: 大量识别错误未修正
**修正**: 建立normalized_corrections.csv记录每次修改

### FAIL-09: Cross Sample Comparison数据不一致
**问题**: 
- Sample 1 Metrics: 863 chars，Comparison写~973
- Sample 2 Metrics: 864 chars，Comparison写~4670
**修正**: 程序直接读取metrics_v2.json生成表格

### FAIL-10: Cross Sample Comparison使用估算值
**问题**: 使用"~""大约""估计值"
**修正**: 全部使用真实计算数值

### FAIL-11: Review Bundle未嵌入完整内容
**问题**: 只用路径引用，未直接嵌入
**修正**: Bundle必须包含完整Transcript/Timeline/Logic/Evidence

### FAIL-12: Sample 02 RELATIVE_BREAKOUT无Baseline证据
**问题**: 未展示baseline_sample_n/creator_median_likes/relative_like_ratio
**修正**: 补充Creator Baseline或降级为RELATIVE_BREAKOUT_CANDIDATE

---

## 根本原因

1. **Timeline生成器bug**: 使用了错误的segment索引
2. **Metrics计算错误**: 把整个transcript当成一个句子
3. **Question检测不完整**: 只找问号，未检测语义问句
4. **Cross-contamination**: Sample 02 Logic Map复制Sample 01
5. **Bundle生成不完整**: 未包含Sample 03和完整内容

---

## 修复方案

1. 为每个ASR Segment建立永久ID (segment_id)
2. Timeline每个节点绑定source_segment_ids
3. 废除sentence算法，改用spoken_unit
4. 增强Question Detector（关键词+语义）
5. 程序生成所有Metrics和Cross Comparison
6. 建立cross-sample污染检测
7. 重新生成完整LAN_REVIEW_BUNDLE_V3

---

*Phase 3.1 QA V2: FAIL → REPAIRING_PIPELINE*
