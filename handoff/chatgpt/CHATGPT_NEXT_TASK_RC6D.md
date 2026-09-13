# ChatGPT → HERMES Next Task RC6D

Status: ACTION_REQUIRED
Owner: HERMES (mechanical/data only)
Semantic authority: ChatGPT

Read first:
- `handoff/chatgpt/CHATGPT_AUDIT_RC6C.md`
- `handoff/chatgpt/CHATGPT_SEMANTIC_REVIEW_RC5.md`

## Authoritative starting state

- Verified Logic Corpus = **85/100**
- Remaining gap = **15**
- RC6C Wave003 net-new = **0** because all 5 source-backed items are cross-batch duplicates.

Do not count RC6C Wave003 duplicates again.

# 1. Stop the failed discovery route

Retire generic Toutiao recommendation/home-feed discovery for milestone gap filling.

Do not continue scrolling BRICS/current-affairs recommendation feeds.

# 2. Create a new gap-fill production area

Use:

`handoff/chatgpt/gapfill_100/`

Create subfolders:

- `toutiao/`
- `douyin/`

Goal: produce **>=20 NEW UNIQUE, real-evidence, on-topic candidates** so ChatGPT can accept at least 15 and reach 100.

# 3. PRE-FETCH cross-batch dedupe is mandatory

Immediately after discovering a candidate URL/CID, BEFORE opening or extracting the body:

check against all known IDs in:
- Batch001
- Batch002
- Batch003
- Batch004 Wave001
- Batch004 Wave002
- RC6C Wave003 audit set

Global keys:
- `TOUTIAO:<content_id>`
- `DOUYIN:<aweme_id>`

If already present:

`DUPLICATE_BEFORE_FETCH`

Do not fetch it. Do not count it as discovered-new. Do not spend extraction budget.

Maintain:

`gapfill_100/PREFETCH_DEDUPE.csv`

# 4. Lane A — Toutiao historical QUERY-FIRST

Primary discovery order:

1. External search-engine result pages restricted to actual Toutiao article URLs, e.g. `site:toutiao.com/article/ <keyword>`.
2. Toutiao internal keyword search in authenticated browser.
3. Author pages of accepted on-topic creators, but max **3 new samples per creator** in this gap-fill set.
4. Related links from strongly on-topic accepted articles only after title/snippet gate.

Do NOT construct article IDs or URLs manually.

A candidate is valid only when the candidate URL/href is observed on a real search/author/result page.

For each discovery record save:

- discovery_timestamp
- discovery_mode
- search_engine_or_source
- search_seed
- source_result_page_url
- observed_anchor_title
- observed_candidate_url
- content_id
- prefetch_dedupe_status

Required file:

`gapfill_100/toutiao/DISCOVERY_LOG.csv`

## Toutiao search seeds

Use a broad, balanced set:

- 能力变现
- 普通人收入
- 职场收入
- 副业变现
- 商业模式
- 生意逻辑
- 创业失败
- 市场验证
- 需求验证
- 定价逻辑
- 价值交换
- 信息差
- 财富认知
- 中产焦虑
- 消费认知
- 品牌定位
- 供应链
- 渠道增长
- 成本利润
- AI接单
- AI赚钱
- AI商业
- AI创业

Prefer historical 2025–2026 content rather than current-news feed dominance.

## Toutiao mechanical topic gate

PASS only when title/snippet clearly concerns:
- earning / income / monetization / side business
- business model / entrepreneurship / customer / demand
- pricing / transaction / repeat purchase / market validation
- work income / ability monetization / efficiency / value exchange
- wealth / consumer behavior / middle-class pressure
- AI commercial use / AI monetization / AI services
- reusable business mechanisms: positioning, supply chain, pricing, trust, distribution, constraints, growth, cost, profit

AUTO REJECT:
- politics / diplomacy / leaders / general current affairs
- sports / running / fitness
- health / illness
- relationships / marriage / family diary
- travel / generic lifestyle diary
- construction/engineering technical content unrelated to business
- entertainment gossip
- lottery / windfall stories

Ambiguous => `TOPIC_REVIEW_REQUIRED` and skip while clear PASS candidates remain.

## Toutiao fulltext hard QA

For NEW UNIQUE Topic-PASS only:

- actual fetched URL must resolve to the same observed CID
- page title must materially match observed anchor title
- persist real article body
- no placeholder
- body >= **400 Chinese chars** for primary gap-fill acceptance
- 250–399 chars => `SHORT_REVIEW`, not counted toward the hard target
- confirm article-body bottom / completeness
- if title promises N points/modes/steps but body lacks them => `TRUNCATION_SUSPECT`
- save SHA256
- `logic_analyzable = PENDING_MODEL_REVIEW`

# 5. Lane B — Douyin recovery in parallel

Perform exactly one NEW UNIQUE Douyin smoke after cooldown.

If smoke PASS:
- resume low-frequency collection
- target **8–12 NEW UNIQUE** on-topic spoken videos
- collect real metadata
- download/obtain audio through the already established legal project route
- ASR mechanically
- persist timed transcript segments
- no semantic analysis

Minimum transcript quality for gap-fill candidate:
- real audio-derived transcript
- transcript >=250 Chinese chars unless clearly complete shorter piece
- not ASR corrupted
- `logic_analyzable = PENDING_MODEL_REVIEW`

If smoke fails with captcha/rate-limit/login wall:

`DOUYIN_DEFERRED_FOR_DAY`

Stop Douyin for the day and let Toutiao Lane A continue. Do not block the gap-fill job.

# 6. Hard anti-fabrication rules

Forbidden:
- manually invented content IDs
- manually invented article URLs
- synthetic titles/authors/text
- summarizing an unseen article and storing the summary as raw/full text
- setting `evidence_ready=true` when actual text is below threshold
- counting duplicates as new discoveries

Every accepted candidate must be traceable:

observed result URL -> fetched canonical page/video -> persisted source body/transcript -> SHA256.

# 7. Diversity targets

Across the >=20 NEW UNIQUE evidence-ready candidates, aim for at least:

- 3 能力变现 / 副业
- 3 商业模式 / business case
- 3 普通人收入 / 职场 / 中产
- 3 消费 / 财富认知
- 3 AI赚钱 / AI商业

No single creator >3 samples.
No single topic >40% when alternatives exist.

# 8. Required outputs

`handoff/chatgpt/gapfill_100/PREFETCH_DEDUPE.csv`

Toutiao:
- `gapfill_100/toutiao/*.json`
- `gapfill_100/toutiao/DISCOVERY_LOG.csv`
- `gapfill_100/toutiao/TOPIC_GATE.csv`
- `gapfill_100/toutiao/FULLTEXT_QA.csv`

Douyin if PASS:
- candidate folders/files with metadata + transcript
- `gapfill_100/douyin/DISCOVERY_LOG.csv`
- `gapfill_100/douyin/ASR_QA.csv`

Also update:
- `handoff/chatgpt/CURRENT_STATUS.md`

CURRENT_STATUS must show separately:

- Verified Logic Corpus = **85/100**
- Gapfill NEW UNIQUE discovered = x
- Gapfill Evidence Ready Pending Model Review = x
- Toutiao = x
- Douyin = x / DEFERRED

Do not add pending candidates to Verified Logic.

# 9. Stop condition

Stop only when one of these is true:

A. **>=20 NEW UNIQUE evidence-ready candidates** have been pushed to Git; or

B. both lanes have hit documented terminal blockers after allowed retries.

Do not start another wave automatically.

# 10. Final HERMES report only

- Toutiao NEW UNIQUE Discovered: x
- Toutiao Evidence Ready: x
- Douyin Smoke: PASS / FAIL / DEFERRED
- Douyin Evidence Ready: x
- Cross-batch Duplicates Rejected Before Fetch: x
- Total NEW UNIQUE Evidence Ready: x
- Terminal Blocker: NONE / <reason>
- Push: PASS / FAIL
- Commit SHA: <sha>

No semantic analysis. No Logic Architecture. No Voice Profile. No Guanyu fit.
