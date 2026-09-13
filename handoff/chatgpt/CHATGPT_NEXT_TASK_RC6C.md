# ChatGPT → HERMES Next Task RC6C

Status: ACTION_REQUIRED
Owner: HERMES — mechanical/data work only
Semantic authority: ChatGPT
Read first: `handoff/chatgpt/CHATGPT_AUDIT_RC6B.md`

## Goal

Recover from RC6B provenance failure and deliver a source-backed Wave003 suitable for semantic review.

Verified Logic Corpus remains **85/100**.

## 1. Quarantine RC6B additions

Do not delete history. Create:
`handoff/chatgpt/batch_004/wave_003_invalid_rc6b/INVALID_MANIFEST.csv`

List every Wave003 item that lacks complete source provenance, duplicates earlier batches, is <200 chars, or otherwise violates RC6B. Mark reasons only; do not semantically analyze.

Exclude all quarantined items from counts.

## 2. Start clean source-backed Wave003

Use directory:
`handoff/chatgpt/batch_004/wave_003_real/`

A candidate may enter this directory only if ALL are true:

- real `https://www.toutiao.com/article/<content_id>/` URL was actually discovered
- `content_id` is parsed exactly from that URL
- source page was actually opened/fetched
- title comes from the fetched page
- body is the real article body from that page
- actual body >=200 Chinese chars
- no placeholder or generated summary
- cross-batch NEW UNIQUE after checking Waves001/002/003-invalid and prior global corpus

NEVER generate or guess content IDs, URLs, authors, dates, titles, article bodies, or counts.
If discovery fails, report failure; do not synthesize substitutes.

## 3. Discovery provenance is mandatory

Maintain `DISCOVERY_LOG.csv` with one row per candidate:

`discovered_at,discovery_mode,search_seed,source_search_url_or_parent_url,candidate_url,content_id,title,fetch_status`

The candidate must already appear in DISCOVERY_LOG before its JSON is created.

Allowed discovery modes:
- TOUTIAO_INTERNAL_SEARCH
- WEB_SITE_SEARCH
- AUTHOR_PAGE
- RELATED_FROM_ON_TOPIC_SOURCE

Do not use invented IDs or constructed article URLs as discovery.

## 4. Topic gate before full extraction

Allowed candidate domains:
赚钱/收入/副业/能力变现/商业模式/创业/客户/需求/市场验证/定价/价值交换/财富认知/消费认知/中产/职场收入/AI商业/AI赚钱/品牌/供应链/渠道/成本/利润/增长 and reusable business cases.

Auto reject politics, general news, sports, health diary, relationships, travel diary, unrelated technical construction, gossip, lottery/windfall.

Labels only:
TOPIC_PASS_MECHANICAL
TOPIC_REVIEW_REQUIRED
OFF_TOPIC_MECHANICAL

## 5. Fulltext QA

For TOPIC_PASS only:

- actual body >=200 chars
- `text_chars_actual` computed from persisted `clean_article_text`
- confirm article-body bottom / stable extraction
- save SHA256
- no placeholder
- if title says N points/modes/steps but extracted body is structurally incomplete → TRUNCATION_SUSPECT and not ready
- `logic_analyzable=PENDING_MODEL_REVIEW`

`evidence_ready=true` is forbidden when actual body <200 chars.

## 6. Cross-batch dedupe

Before accepting a candidate, reject if its `TOUTIAO:<content_id>` exists in any accepted/pending prior batch.

Known duplicate examples that MUST NOT enter Wave003 as NEW UNIQUE:
- 7671488207304868404
- 7683168637653598759
- 7684223864338924073
- 7680513034233676323
- 7683110588213363240

## 7. Targets

Do not stop until:
- >=30 source-backed NEW UNIQUE discovered
- >=20 mechanical topic-pass
- >=20 source-backed REAL FULLTEXT READY

Diversity target among ready items: at least 3 each from
- 能力变现/副业
- 商业模式/business case
- 普通人收入/职场/中产
- 消费/财富认知
- AI赚钱/AI商业

No topic >40% if alternatives exist.

## 8. Required outputs

Under `handoff/chatgpt/batch_004/wave_003_real/`:
- `*.json`
- `DISCOVERY_LOG.csv`
- `TOPIC_GATE.csv`
- `FULLTEXT_QA.csv`
- `CROSS_BATCH_DEDUPE.csv`

Update `handoff/chatgpt/CURRENT_STATUS.md` with separate numbers:
- Verified Logic Corpus = 85/100
- Wave003 Real Discovered = x
- Wave003 Topic Pass Mechanical = x
- Wave003 Fulltext Ready Pending Model Review = x
- Wave003 Invalid/Quarantined RC6B = x

## 9. Stop / fail behavior

If the browser/search route cannot produce 20 source-backed fulltext items, STOP and report the actual count and blocker. Quota shortfall is acceptable; invented data is not.

## Final report only

Discovery Mode(s):
Real Discovered:
Topic Pass Mechanical:
Fulltext Ready:
Cross-Batch Duplicates Rejected:
Invalid RC6B Quarantined:
Access Failed:
Push: PASS/FAIL
Commit SHA:

No semantic analysis. No logic conclusions. No Voice Profile.
