# ChatGPT → HERMES Next Task RC6B

Status: ACTION_REQUIRED
Owner: HERMES (mechanical/data only)
Semantic authority: ChatGPT

## Status correction
RC6 is NOT complete.
Current verified state:
- Verified Logic Corpus = 85/100
- Wave003 discovered = 5
- Topic-PASS mechanical = 0
- Fulltext Ready = 0

Keep the existing 5 Wave003 items as discovery audit evidence. Do not count them toward the RC6 stop condition.

## Root cause
The generic Toutiao recommendation/home feed is dominated by political/current-affairs content. Stop using that feed as the primary discovery route.

## Switch to QUERY-FIRST discovery
Priority:
1. Toutiao internal search in the authenticated browser session.
2. Search-engine discovery restricted to Toutiao article URLs: `site:toutiao.com/article/` + target keyword.
3. Author pages / related articles from accepted on-topic Wave001/Wave002 creators, with title/snippet topic gate before extraction.
4. Recommendation links only when the source page is strongly on-topic and the candidate passes the pre-extraction gate.

Search seeds:
能力变现; 普通人赚钱逻辑; 普通人收入; 职场收入; 副业变现; 商业模式; 生意逻辑; 创业失败; 市场验证; 需求验证; 定价逻辑; 价值交换; 信息差; 财富认知; 中产焦虑; 消费认知; 品牌定位; 供应链; 渠道增长; 成本利润; AI接单; AI赚钱; AI商业; AI创业.

## Hard targets
Continue Wave003 until ALL are met:
- >=30 NEW UNIQUE discovered candidates after cross-batch dedupe
- >=20 Topic-PASS mechanical candidates
- >=20 REAL FULLTEXT READY candidates pushed to Git

Do not stop at 5/10/15 discovered candidates.
Global key: `TOUTIAO:<content_id>`.

## Pre-extraction topic gate
PASS: earning/income/monetization/side business; business model/entrepreneurship/customer/demand; pricing/transaction/repeat purchase/market validation; work income/ability monetization/efficiency/value exchange; wealth/consumer behavior/middle-class pressure; AI commercial use/AI monetization/AI services; reusable business cases involving positioning, supply chain, pricing, trust, distribution, constraints, growth, cost, profit.

AUTO REJECT: politics/diplomacy/leaders/general news; sports/running/fitness; health/illness; relationships/marriage/family diary; travel/generic lifestyle diary; construction/engineering technical content unrelated to business; entertainment gossip; lottery/pure windfall stories.

Ambiguous metadata => `TOPIC_REVIEW_REQUIRED`; do not spend fulltext budget while PASS candidates remain.

## Diversity target among >=20 fulltext-ready
At least 3 each:
- 能力变现/副业
- 商业模式/business case
- 普通人收入/职场/中产
- 消费/财富认知
- AI赚钱/AI商业
No one topic >40% when alternatives exist.

## Fulltext QA
For Topic-PASS only:
- persist real article body, no placeholder
- actual body >=200 Chinese chars; shorter complete items => `SHORT_REVIEW`, not Evidence Ready
- confirm article-body bottom using the robust extraction route
- if title says N points/modes but body lacks expected structure, flag `TRUNCATION_SUSPECT`
- save SHA256
- `logic_analyzable = PENDING_MODEL_REVIEW`

Allowed HERMES labels only:
TOPIC_PASS_MECHANICAL, TOPIC_REVIEW_REQUIRED, OFF_TOPIC_MECHANICAL, FULLTEXT_READY, SHORT_REVIEW, TRUNCATION_SUSPECT, ACCESS_FAILED.
No semantic analysis.

## Git outputs
Continue under `handoff/chatgpt/batch_004/wave_003/` and maintain:
- `*.json`
- `TOPIC_GATE.csv`
- `FULLTEXT_QA.csv`
- `DISCOVERY_LOG.csv` with discovery_mode, search_seed, source_url, content_id, title
- updated `handoff/chatgpt/CURRENT_STATUS.md`

CURRENT_STATUS must keep separate:
- Verified Logic Corpus = 85/100
- Wave003 Discovered = x
- Wave003 Topic Pass Mechanical = x
- Wave003 Fulltext Ready Pending Model Review = x

Do not add pending to Verified Logic.

## Stop condition
Stop only when >=20 NEW UNIQUE Topic-PASS + REAL FULLTEXT READY candidates are pushed to Git. Then wait for ChatGPT semantic review. Do not auto-start Wave004.

Final report only:
Discovery Mode: QUERY_FIRST
Wave003 Discovered: x
Topic Pass Mechanical: x
Fulltext Ready: x
Review Required: x
Off Topic: x
Truncation Suspect: x
Push: PASS/FAIL
Commit SHA: <sha>

No Logic Architecture, no Voice Profile, no Guanyu fit.
