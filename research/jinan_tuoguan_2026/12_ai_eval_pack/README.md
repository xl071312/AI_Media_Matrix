# 12_ai_eval_pack — 济南托管 · AI 评估选址/竞品数据包

本目录为 **AI 评估选址与 Douyin 竞品分析** 专用只读数据包（v1），由既有调研产物汇总而成，**未启动新抓取**。

目标账号：**壹心托管济南校区**；竞品：关键词公开搜索所得 Douyin 账号与帖子。用途：卖点、价格线索、校区/区位、家长痛点、内容类型分布等评估——**仅基于本包字段与 corpus，禁止编造未见数据**。

整理时间：2026-09-16 00:35 PT（Douyin deepen 合并后刷新）。

---

## 文件一览

| 路径 | 说明 |
|------|------|
| `douyin_accounts_for_eval.csv` | 目标 + 竞品账号合并表（UTF-8-SIG） |
| `douyin_posts_for_eval.csv` | 全部 Douyin 帖子（文案/话题/互动/asr_path） |
| `douyin_comments_for_eval.csv` | Douyin 评论 + 作者回复 |
| `corpus/` | 关键 json/jsonl 与转写、Excel、项目 manifest 的相对符号链接 |
| `manifest_eval.json` | 行数、来源、阻塞摘要、git 分支说明、collected_at |
| `prompts/ai_eval_brief.md` | 给评估用 AI 的简短分析 brief |

---

## 字段说明

### `douyin_accounts_for_eval.csv`（76 行）

| 字段 | 含义 |
|------|------|
| `platform` | 固定 `douyin` |
| `account_id` | 目标为抖音号/unique_id；竞品多为 `douyin_comp_*` 哈希 ID |
| `nickname` | 公开昵称 |
| `unique_id` | 抖音号（竞品搜索卡常为空） |
| `url` | 主页 URL（竞品常为空） |
| `followers` / `likes_total` | 粉丝/获赞（公开可见时） |
| `bio` | 简介；竞品侧多为搜索卡卖点摘要 |
| `region` | IP/地区标签（竞品搜索卡常为空） |
| `contact` | 公开联系方式（多数为空） |
| `source_keyword` | 命中关键词或目标标签 |
| `collected_at` | 采集时间 |
| `notes` | 采集备注/粗估近 30 日发帖等 |
| `eval_role` | `target`（壹心）或 `competitor`（本包派生，非平台字段） |

**来源：** 根目录 `accounts.csv`（已合并 `01_douyin_target/account.json` 与 `02_douyin_competitors/accounts.csv`）。竞品原始行亦见 `corpus/02_douyin_competitors/accounts_raw.jsonl`。

### `douyin_posts_for_eval.csv`（96 行）

| 字段 | 含义 |
|------|------|
| `post_id` / `account_id` / `url` | 帖子与账号标识 |
| `published_at` | 发布时间（公开可见格式，未必 ISO） |
| `title` / `caption_full` / `hashtags` | 标题、全文案、话题 |
| `likes` / `comments_count` / `favorites` / `shares` | 互动指标（公开可见时） |
| `duration_sec` | 时长（秒） |
| `asr_path` | 相对路径至 `06_transcripts/*.txt`（有口播时）；空=无可靠 ASR |
| `ocr_path` / `cover_path` | OCR/封面路径（多数为空） |
| `source_keyword` / `rank_type` / `rank_pos` | 搜索词与排序线索 |
| `collected_at` | 采集时间 |

**来源：** 根目录 `posts.csv` 中 `platform=douyin` 行（含目标详情帖 + 竞品搜索抽样）。ASR 文本见 `corpus/06_transcripts/`。

### `douyin_comments_for_eval.csv`（77 行）

| 字段 | 含义 |
|------|------|
| `post_id` / `comment_id` | 帖子与评论 ID |
| `author` | 作者；非商家句柄已匿名为「家长A/B/C…」 |
| `content` | 评论正文 |
| `likes` | 点赞 |
| `is_author_reply` | `1`=账号作者回复，`0`=其他 |
| `parent_id` | 父评论（回复链） |
| `collected_at` | 采集时间 |

**来源：** 根目录 `comments.csv` 中 `platform=douyin`（主要来自 `01_douyin_target/comments/*.json`）。本包 **不含** 小红书/百度评论。

---

## `corpus/` 内容

相对符号链接（指向上级调研目录，勿当独立副本）：

- `01_douyin_target/`：`account.json`、`collection_summary.json`、`extracted_fields.json`、`works_detail_partial.jsonl`、`works_list_raw.json`
- `02_douyin_competitors/`：`accounts_raw.jsonl`、`README_task7.json`、`blocker_note.txt`
- `search_raw_summaries/`：11 个关键词 `*.json` + `_index.json`
- `06_transcripts/`：18 组 json/txt + `asr_log.md`
- `济南托管调研_v1.xlsx`、`project_manifest.json`

---

## 数据溯源（provenance）

| 层级 | 路径 |
|------|------|
| 目标账号 | `../01_douyin_target/` |
| 竞品搜索 | `../02_douyin_competitors/`（62 账号、79 源帖抽样；合并后 Douyin 帖 85） |
| 转写 | `../06_transcripts/`（10 条有口播写入 posts.asr_path；8 条无可靠人声） |
| 根表 | `../accounts.csv`、`../posts.csv`、`../comments.csv` |
| Excel | `../济南托管调研_v1.xlsx`（任务1/任务7 等） |
| 项目清单 | `../manifest.json` |

约束：公开可见、不登录、不绕过验证；家长昵称已匿名；未主动保存儿童面部特写。

---

## 阻塞与缺口（blockers）

1. **登录墙**：公开网页用户搜索「泉海托管」出现「登录后即可搜索更多精彩视频」；未登录/未绕过。证据：`../02_douyin_competitors/screenshots/任务7_登录拦截_01.png`，说明见 `corpus/02_douyin_competitors/blocker_note.txt`。
2. **同城不可用**：网页未见可用「同城」入口，竞品改用公开「综合」搜索。
3. **目标详情不全**：完整评论/ASR/OCR、电话、公开标价、精确门牌多未展示或未完整采集。
4. **竞品卡字段稀疏**：位置/IP、主页 URL、粉丝数常空；近 30 日发帖为可见结果粗估。
5. **ASR**：18 条转写记录中 8 条无可靠人声（空文本保留）。
6. **本包范围外**：地图点评墙、政府细则缺口、学一家未精确命中等见根 `manifest.json`，不在本 Douyin 评估表内。

---

## 使用注意

- CSV 均为 **UTF-8-SIG**（Excel 可直接打开）。
- `eval_role` 仅便于筛选目标/竞品，分析时仍以 `nickname`/`account_id`/原文为准。
- 价格、校区、联系方式：**只引用 CSV/corpus 中明确出现的公开文本**；未见则标「未公开/未采集」。
- Git：当前 box 上 `AI_Media_Matrix` **不是 git 仓库**（见 `manifest_eval.json` → `git_branch`）。
