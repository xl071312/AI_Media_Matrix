# ChatGPT Review RC4 — Corpus Admission Fix

Status: ACTION_REQUIRED
Owner: HERMES for data/mechanical work; ChatGPT owns semantic review.

## What ChatGPT verified from commit bda513b

RC4 extraction completed mechanically, but the current Wave002 set is NOT admissible as 18 topic-qualified research samples.

Examples found directly in Git:
- 7187298184346206754 = external-wall insulation engineering article → OFF_TOPIC.
- 7048926434592555558 / 7049600535418143270 = 2022 quarantine/personal diary → OFF_TOPIC.
- 7618573005362332196 = social-relationship essay about being gregarious → OFF_TOPIC for the benchmark core.
- 7684447381258666559 = BRICS political news, only 128 chars, yet evidence_ready=true → OFF_TOPIC and violates >=200-char evidence rule.
- TOUTIAO_WAVE002_CANDIDATES.csv itself contains visible unrelated recommendation titles, showing recommendation discovery drift.

Wave001 also still needs deterministic completeness repair: 7645692141699662362 is titled “3个轻资产模式” but current persisted body ends after 模式二, so mechanical `article_bottom_reached=true` was a false positive.

## Metric definitions — lock

Do not combine verified and pending:
- Verified Logic Corpus = samples already accepted by ChatGPT.
- Evidence Ready Pending Review = ONLY new pending samples, excluding verified corpus.
- Raw Fulltext Recovered = extraction success only; says nothing about topic admission.

Current verified corpus remains 60 until ChatGPT promotes samples.

## Task A — Wave002 quarantine and topic gate

1. Freeze current `wave_002` as RAW_RECOMMENDATION_POOL.
2. Do not count 18 real-body files as Evidence Ready for the target corpus merely because text exists.
3. Add fields to a new `WAVE002_TOPIC_GATE.csv`:
   `content_id,title_or_first_line,text_chars,mechanical_topic_hit,obvious_off_topic,gate_status`
4. Mechanical positive keyword families (metadata/title/first 300 chars only):
   赚钱, 搞钱, 副业, 收入, 变现, 商业, 创业, 信息差, 财富, 职场, AI赚钱, AI变现, 普通人收入, 消费, 中产, 投资认知, 能力变现.
5. Obvious negative/off-topic examples: politics/news, construction engineering, epidemic diary, pure relationship/life essay, unrelated local news.
6. If no positive hit or obvious off-topic → `OFF_TOPIC_MECHANICAL` or `TOPIC_REVIEW_REQUIRED`; do not set evidence_ready=true for benchmark admission.
7. ChatGPT makes final semantic topic decision.

## Task B — Wave001 completeness hard repair

1. Re-run all Wave001 article bodies using browser_navigate.
2. Before extraction, click visible `展开全文`, `阅读全文`, `继续阅读` controls when present.
3. Use the article BODY container only.
4. Scroll article body to bottom and read same container repeatedly.
5. Require `stable_rounds >= 3` for every article. No exceptions based on one-pass height.
6. Persist actual `clean_article_text` after expansion.
7. `fulltext_complete=true` only when:
   - actual_text_chars >= 200
   - placeholder=false
   - article_bottom_reached=true
   - stable_rounds>=3
8. Add `declared_count` / `observed_heading_count` where mechanically detectable for titles/body patterns like `3个/5个/N步/N种/N类`; if observed < declared → `STRUCTURE_TRUNCATION_SUSPECT=true` and fulltext_complete=false.
9. Regenerate `FULLTEXT_COMPLETENESS_QA_V2.csv`.

## Task C — replace bad Wave002 discovery

After A/B:
1. Do NOT discover new corpus articles from unfiltered recommendation links.
2. Candidate must pass mechanical topic gate BEFORE full-body extraction.
3. Prefer already-authenticated browser searches/direct links around the benchmark keywords; recommendation links may be used only after title/first-text topic gate.
4. Target 25 NEW UNIQUE candidates to yield >=20 topic-qualified pending samples.
5. Persist real full text with the same completeness QA as Wave001.

## Git handoff

Update:
- `handoff/chatgpt/CURRENT_STATUS.md`
- `handoff/chatgpt/batch_004/wave_001/FULLTEXT_COMPLETENESS_QA_V2.csv`
- `handoff/chatgpt/batch_004/wave_002/WAVE002_TOPIC_GATE.csv`
- repaired/new JSONs

Commit message:
`benchmark handoff: RC5 corpus topic gate and completeness repair`

Final report only:
- Wave001 Fulltext Complete V2: x/20
- Wave001 Truncation Suspects: x
- Wave002 Raw Real Body: x
- Wave002 Mechanical On-topic: x
- Wave002 Off-topic: x
- New Topic-gated Evidence Pending Review: x
- Verified Logic Corpus: 60/100 (unchanged until ChatGPT review)
- Push: PASS/FAIL
- Commit SHA

No semantic logic/viral/voice analysis by HERMES.
