# CHATGPT NEXT TASK — Plain Language Discovery RC6H

Date: 2026-09-14
Owner: HERMES
Semantic owner: ChatGPT
Status: EXECUTION TASK
Precondition: RC6G accepted as `SOURCE_EXHAUSTED`; do not rescan the existing 414-record raw pool as a discovery route.

## Objective

Build a genuinely new candidate pool for Plain Language Corpus V1 by using **live discovery routes outside the existing raw pool**.

This is a mechanical collection task only. HERMES must not perform semantic analysis, language-style judgment, logic-map work, viral-reason analysis, or Voice Profile conclusions.

## Historical exclusion universe

Use the canonical historical-ID universe produced by RC6G as the exclusion set. Normalize all Douyin IDs before comparison:

- strip `DY_REAL_` and similar internal prefixes;
- extract numeric aweme/video ID from URLs;
- compare canonical numeric IDs;
- exclude anything already in the historical 480-ID universe.

Do not claim `NEW` unless the canonical ID is outside that exclusion universe.

## Discovery Route A — Live Douyin topic search (primary; target >=70% of final candidates)

Use live Douyin search, not `raw_pool_all.jsonl`.

Run the following query bank mechanically. Search both exact phrase and natural variants where the existing collector/browser route supports it:

### Money / ordinary-person framing
- 普通人赚钱
- 普通人收入
- 工资到底
- 一个月工资
- 攒钱
- 花钱值不值
- 消费降级
- 消费陷阱
- 赚钱思维
- 搞钱
- 副业避坑
- 副业怎么选
- 开店亏钱
- 小生意
- 普通人翻身

### Work / boss / employee framing
- 打工人
- 上班真相
- 老板为什么
- 职场真相
- 汇报工作
- 工资涨不上去
- 为什么升职
- 工作值不值
- 职场避坑
- 被裁员怎么办

### Explain-it-simply framing
- 大白话讲
- 我给你算一笔账
- 给你算一下
- 到底什么意思
- 举个例子
- 一看就懂
- 普通人能听懂
- 说白了
- 你想一下
- 为什么呢

### AI + ordinary Chinese work/life
- AI 普通人
- AI 工作
- AI 上班
- AI 副业
- AI 赚钱
- AI 打工人

For each query, collect the first available result pages/scroll window supported by the existing authenticated route. Record query, rank, content ID, title, author, duration, likes, comments, favorites, shares, URL, and discovery timestamp.

Do not stop after the first few high-like results. The purpose is a new candidate universe.

## Discovery Route B — Related / adjacent videos (secondary; target <=15%)

Use these kinds of anchor content only to request mechanically related/adjacent videos if the authenticated route exposes them:

- RC6F_010 type: workplace explanation with concrete examples;
- RC6F_011 type: price/equivalence comparison;
- RC6F_012 type: one stable story-world explaining a hard concept;
- historical strong samples around income, money, small business, ordinary-person decisions.

Collect related-video IDs only. Do not infer why they are related.

Exclude historical IDs immediately.

If the platform route does not expose related videos reliably, mark this route `UNAVAILABLE` and continue. Do not fake adjacency.

## Discovery Route C — Creator-neighbor expansion (tertiary; hard cap <=30% of final shortlist)

For creators attached to strong mechanically usable anchor samples, enumerate other public videos from the same creator where accessible.

Mechanical constraints:
- max 10 candidate videos per creator before dedupe;
- do not let creator-neighbor material exceed 30% of the final shortlist;
- exclude historical IDs;
- record creator source and discovery mode explicitly.

This route is allowed because it is a candidate generator, not a semantic conclusion. Topic-first material must remain dominant.

## Route D fallback — Toutiao video search only if Douyin live discovery is blocked

Use only if Route A cannot produce live results because of access/tooling failure, not merely because some queries are sparse.

Use the same Chinese query bank. Mark all such samples `platform=toutiao` and `role=AUXILIARY_PLAIN_LANGUAGE`.

Do not mix Toutiao written articles into this spoken-language corpus.

## Candidate-pool gate

Before downloading media, prove route viability.

Target:
- >=100 canonical new candidate IDs outside historical universe.

Minimum viable:
- >=50 new candidate IDs.

If fewer than 50 genuinely new IDs remain after all viable routes, stop and return `DISCOVERY_INSUFFICIENT` with per-route counts and evidence. Do not proceed to manufacture a 30-sample corpus.

## Mechanical shortlist

If >=50 new IDs exist, produce a 40–50 item mechanical shortlist for audio/ASR.

Prefer mechanically:
- duration roughly 30s–10min;
- non-zero engagement metadata;
- titles/queries within the requested Chinese topic families;
- mix of very high engagement and mid-level engagement;
- creator-neighbor share <=30%;
- Douyin dominant.

Do not make semantic choices such as “this explains well” or “this sounds human.” ChatGPT will do that later.

## Media + ASR

For shortlisted items:
1. save metadata;
2. download real audio/video using the existing compliant route;
3. run the existing project ASR pipeline;
4. save timestamped segment transcript;
5. compute only deterministic transcript metrics.

Mechanical ASR metrics must include at least:
- transcript character count;
- segment count;
- first-30s segment coverage;
- duration;
- repeated-token ratio or obvious repeated-single-token flag if already supported by project code;
- ASR error/empty status.

A transcript `>50 chars` must **not** be labeled semantically usable. Use a field such as `mechanical_transcript_present=true/false`; leave semantic usability to ChatGPT.

If existing ASR pipeline has an already-configured retry path, one mechanical retry is allowed for empty/failed ASR. Do not invent a new ASR provider or model configuration.

## Required outputs

Create a new route-specific folder, do not overwrite RC6F evidence:

`01_benchmark/plain_language_discovery_rc6h/`

Required files:
- `DISCOVERY_QUERY_BANK.csv`
- `DISCOVERY_RESULTS_RAW.csv`
- `DISCOVERY_ROUTE_COUNTS.csv`
- `HISTORICAL_DEDUPE_AUDIT.csv`
- `NEW_CANDIDATES.csv`
- `SHORTLIST.csv`
- `PERFORMANCE.csv`
- `STATUS.md`

For each downloaded/ASR sample, use a self-contained sample folder with at least:
- metadata JSON/CSV;
- source URL;
- audio/media evidence path where repo policy permits;
- timestamped raw transcript;
- deterministic ASR metrics.

## STATUS values

Use exactly one final status:
- `RC6H_COMPLETE` — >=40 mechanically processed new samples;
- `RC6H_PARTIAL` — >=20 but <40 mechanically processed new samples;
- `DISCOVERY_INSUFFICIENT` — <50 new candidate IDs before media stage;
- `ACCESS_BLOCKED` — authenticated live discovery cannot be performed after one supported recovery attempt.

Do not use `PASSED` for semantic quality.

## Hard prohibitions

HERMES must not write:
- why a video went viral;
- which wording is more human;
- logic maps;
- cognitive-gain analysis;
- plain-language rules;
- Voice Profile conclusions;
- Guanyu script recommendations.

Those belong to ChatGPT.

## Completion response

When finished, return only:
- final status;
- final commit SHA;
- counts: discovered raw / new after historical dedupe / shortlisted / mechanically processed / ASR-present.
