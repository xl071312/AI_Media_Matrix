# RC6J Primary 28 Transcript Report

**Generated**: 2026-09-16T20:11:20.144439
**Source Commit**: b599197
**Status**: MEDIA_UNAVAILABLE

## Input

PRIMARY = 28

## Media & ASR Stats

MEDIA_AVAILABLE = 0
ASR_ATTEMPTED = 0
ASR_SUCCESS = 0

## Transcript Levels

FULL_TRANSCRIPT = 0
PARTIAL_TRANSCRIPT = 0
FIRST30_ONLY = 0
TRANSCRIPT_MISSING = 28
Total = 28

## Analysis Readiness

FULL_ANALYSIS_READY = 0
PARTIAL_ANALYSIS_READY = 0
HOOK_ONLY_READY = 0
NOT_READY = 28

## Failure Reason

所有28条PRIMARY样本均无法获取媒体文件，原因：
1. CDP端口9223不可用
2. yt-dlp需要有效的Douyin登录Cookie
3. 现有Cookie可能已过期或格式不匹配

## Required Action

需要以下任一条件才能继续：
1. 启动Chrome CDP: chrome --remote-debugging-port=9223
2. 提供有效的Netscape格式Douyin Cookie文件
3. 手动下载28个视频并放入对应目录

## Output

- `01_benchmark/analysis_batches/rc6j_full_transcripts/RC6J_PRIMARY_28_TRANSCRIPT_MANIFEST.csv`
- `01_benchmark/analysis_batches/rc6j_full_transcripts/RC6J_PRIMARY_28_TRANSCRIPT_REPORT.md`
- 28个样本目录（含元数据）

---
*本任务受限于媒体访问。等待CDP或Cookie问题解决后重试。*
