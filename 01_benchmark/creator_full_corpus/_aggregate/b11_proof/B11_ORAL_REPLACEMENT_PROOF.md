# B1.1 ORAL REPLACEMENT PROOF

- Written: 2026-09-19T10:46:52.178729+00:00
- Scope: proof only（每人 3 条，≥2/3 PASS）。不进 Phase C / Voice Profile / 新口播稿。
- Backups（罗翔说刑法 / 李永乐老师官方）: **NOT NEEDED** — 三位主候选均 ≥2/3。

## Summary

| creator | pass | gate | method | PRIMARY/AUX | expandable≥40 | replace |
|---|---|---|---|---|---|---|
| 巫师财经 | 3/3 | PASS | 1× B站本地全文ASR + 2× YouTube音频 faster-whisper tiny 全文ASR | AUX | YES_LIKELY | ACCEPT_AS_AUX_ORAL_REPLACEMENT |
| 毕导 | 3/3 | PASS | YouTube 公开音频 + faster-whisper small 全文ASR | AUX | YES_LIKELY | ACCEPT_AS_AUX_ORAL_REPLACEMENT |
| 老师好我叫何同学 | 3/3 | PASS | YouTube 公开自动字幕(zh) → spoken txt | AUX | YES_LIKELY | ACCEPT_AS_AUX_ORAL_REPLACEMENT |

## Per-creator

### 巫师财经
- FULL_SPOKEN success: **3/3** (PASS)
- Method: 1× B站本地全文ASR + 2× YouTube音频 faster-whisper tiny 全文ASR
- PRIMARY/AUX: **AUX_ORAL**
- Expandable to ≥40 FULL_SPOKEN: **YES_LIKELY**（官方片库大；本批管线已证明；B站本环境仍 412）
- Blocker: Bilibili 本环境 412；YT 常无自动字幕 → 音频ASR可行
- Replace recommendation: **ACCEPT_AS_AUX_ORAL_REPLACEMENT**
- Proof URLs:
  - https://www.bilibili.com/video/BV1ViEg6PESR
  - https://www.youtube.com/watch?v=GXd5r1KtW0w
  - https://www.youtube.com/watch?v=pnW6Ilpjc0Q

### 毕导
- FULL_SPOKEN success: **3/3** (PASS)
- Method: YouTube 公开音频 + faster-whisper small 全文ASR
- PRIMARY/AUX: **AUX_ORAL**
- Expandable to ≥40 FULL_SPOKEN: **YES_LIKELY**（官方片库大；本批管线已证明；B站本环境仍 412）
- Blocker: Bilibili 412；YT+ASR 可用
- Replace recommendation: **ACCEPT_AS_AUX_ORAL_REPLACEMENT**
- Proof URLs:
  - https://www.youtube.com/watch?v=zXJ8GGbvJ5w
  - https://www.youtube.com/watch?v=ZdhxyGjU2VU
  - https://www.youtube.com/watch?v=aDGyz9dHrcs

### 老师好我叫何同学
- FULL_SPOKEN success: **3/3** (PASS)
- Method: YouTube 公开自动字幕(zh) → spoken txt
- PRIMARY/AUX: **AUX_ORAL**
- Expandable to ≥40 FULL_SPOKEN: **YES_LIKELY**（官方片库大；本批管线已证明；B站本环境仍 412）
- Blocker: Bilibili 412；改用官方 YT 字幕
- Replace recommendation: **ACCEPT_AS_AUX_ORAL_REPLACEMENT**
- Proof URLs:
  - https://www.youtube.com/watch?v=9vnr69Lg4_I
  - https://www.youtube.com/watch?v=Zoe9FOZRkJY
  - https://www.youtube.com/watch?v=-tHdM8dOeAc

## Global blockers

- Bilibili HTTP/API/yt-dlp 本环境：**412 Precondition Failed**（CAPTION_BLOCKED）。Cookie 未能解除。
- 未使用 Douyin yt-dlp 403 重试（禁止）。
- 采用路径：官方 YouTube 公开字幕，和/或公开音频 + 本地 faster-whisper **全文** ASR（非前30秒、非摘要、非文章当口播）。

## Final replace slate（供 Lan/ChatGPT）

建议接受 **巫师财经 / 毕导 / 老师好我叫何同学** 作为 AUX_ORAL 替换人选（对应口播门失败：银行小姐姐 / 直男财经 / 韩秀云讲经济），待验收。

TEXT 侧 KEEP 不变：温义飞的急救财经 / 小Lin说 / 硬核的半佛仙人。

## Stop

No Phase C. No Voice Profile. No new 口播稿. Waiting Lan/ChatGPT.
