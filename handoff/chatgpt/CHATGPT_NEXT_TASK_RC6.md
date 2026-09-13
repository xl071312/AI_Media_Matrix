# ChatGPT → HERMES Next Task RC6

Status: ACTION_REQUIRED
Owner: HERMES (mechanical/data work only)
Semantic authority: ChatGPT

Read first:
- `handoff/chatgpt/CHATGPT_SEMANTIC_REVIEW_RC5.md`

## Goal

Move from **Verified Logic Corpus 85/100** to >=100 by collecting a targeted Wave003 with enough on-topic, real-fulltext candidates for model review.

Do not count new samples as Verified Logic yourself.

## 1. Freeze previous waves

- Wave001: FROZEN, accepted by ChatGPT 20/20.
- Wave002: FROZEN with semantic statuses from `CHATGPT_SEMANTIC_REVIEW_RC5.md`.
- Do not re-extract or mutate accepted Wave001/Wave002 bodies unless corruption is detected.

## 2. Create targeted Wave003

Directory:
`handoff/chatgpt/batch_004/wave_003/`

Target:
- discover >=30 NEW UNIQUE candidates
- persist >=20 real-fulltext, on-topic candidates
- expect ChatGPT to accept at least 15

Use the working Toutiao browser route only.

## 3. PRE-EXTRACTION Topic Gate (mandatory)

Before opening/extracting a full article, use title/snippet/page metadata mechanically.

### PASS keywords / domains

Prioritize candidates matching one or more of:

- 赚钱 / 搞钱 / 收入 / 副业 / 变现
- 商业 / 商业模式 / 创业 / 生意 / 客户 / 需求
- 市场验证 / 定价 / 价值 / 交易 / 复购
- AI赚钱 / AI接单 / AI商业 / AI创业
- 职场收入 / 能力 / 人效 / 价值交换
- 信息差 / 财富认知 / 消费认知 / 中产
- 品牌定位 / 供应链 / 渠道 / 用户 / 增长 / 成本 / 利润

Business-case articles may pass even without the literal word “赚钱” when title/snippet clearly concerns reusable business mechanisms.

### AUTO REJECT

Reject before full extraction if obviously about:

- politics / leaders / diplomacy / general current affairs
- sports / running / fitness
- health / illness / medical diary
- relationships / marriage / emotional diary
- travel diary / daily-life diary
- construction / engineering technical content unrelated to business logic
- entertainment gossip
- generic lifestyle news

### REVIEW_REQUIRED

If metadata is ambiguous, add to review queue and continue; do not spend full extraction budget until PASS candidates are exhausted.

## 4. Fulltext requirements

For Topic-PASS candidates only:

- use real article container
- persist actual body in JSON
- no placeholder
- `text_chars_actual >= 200`
- scroll until article-body text is stable / bottom confirmed using the current robust method
- save SHA256
- `logic_analyzable = PENDING_MODEL_REVIEW`

## 5. Evidence categories

HERMES may mechanically label only:

- `TOPIC_PASS_MECHANICAL`
- `TOPIC_REVIEW_REQUIRED`
- `OFF_TOPIC_MECHANICAL`
- `FULLTEXT_READY`
- `SHORT_OR_INCOMPLETE`
- `ACCESS_FAILED`

Do not generate reasoning engine, hook, viral reason, cognitive gain, Guanyu fit, or semantic conclusions.

## 6. Diversity constraints

Wave003 should avoid becoming another AI副业-only batch.

Try to obtain at least:

- 3 能力变现 / 副业
- 3 商业模式 / business case
- 3 普通人收入 / 职场 / 中产
- 3 消费 / 财富认知
- 3 AI赚钱 / AI商业

Remaining slots can be any allowed topic.

No single topic >40% if enough candidates exist.

## 7. Creator / control opportunity

When metadata exposes real creator identity, save it.

If the same creator has both a strong on-topic article and a normal on-topic article, record a candidate pair. Do not analyze why they differ.

## 8. Git handoff

Push only after deterministic QA.

Required files:

- `handoff/chatgpt/batch_004/wave_003/*.json`
- `handoff/chatgpt/batch_004/wave_003/TOPIC_GATE.csv`
- `handoff/chatgpt/batch_004/wave_003/FULLTEXT_QA.csv`
- updated `handoff/chatgpt/CURRENT_STATUS.md`

CURRENT_STATUS must show separately:

- `Verified Logic Corpus = 85/100` (until ChatGPT reviews Wave003)
- `Wave003 Fulltext Ready Pending Review = x`

Do not add pending items into Verified Logic.

## 9. Optional Douyin smoke

If Douyin cooldown has fully cleared, one NEW UNIQUE smoke is allowed in parallel. If rate limited again, set `DOUYIN_DEFERRED_FOR_DAY` and stop. Do not let Douyin block Wave003.

## 10. Stop condition

Stop Wave003 expansion when:

- >=20 NEW UNIQUE Topic-PASS + real-fulltext candidates are pushed to Git

Then wait for ChatGPT semantic review. Do not auto-start Wave004.

## Final report only

- Wave003 Candidates: x
- Topic Pass Mechanical: x
- Fulltext Ready: x
- Review Required: x
- Off Topic: x
- Douyin Smoke: PASS/FAIL/DEFERRED/NOT_RUN
- Push: PASS/FAIL
- Commit SHA: <sha>

No semantic analysis.
