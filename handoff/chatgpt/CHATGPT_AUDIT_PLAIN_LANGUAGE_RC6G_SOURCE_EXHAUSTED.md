# ChatGPT Audit — Plain Language RC6G SOURCE_EXHAUSTED

Date: 2026-09-14
Owner: ChatGPT
Status: ACCEPTED AS A STOP CONDITION / NOT A CORPUS PASS
Audited commit: `c208b7e5a3b8a5a2f773052dcfb73b36421271ff`

## Decision

RC6G is accepted as a **correct stopping result for the existing raw-pool route**.

It is **not** accepted as completion of Plain Language Corpus V1, because the route produced no new candidates.

The important result is mechanical:

- historical canonical-ID universe: 480 unique IDs;
- existing raw pool: 414 candidates;
- all 414 are contained in the historical universe;
- new candidate IDs from that route: 0.

Therefore the existing `raw_pool_all.jsonl -> dedupe -> ASR` route is exhausted and must not be retried.

## Governance consequence

Same-route retry is prohibited here. The next collection task must change **discovery source**, not merely rerun dedupe or ASR.

The 414-record raw pool remains useful as historical evidence, but it is no longer a discovery source.

Verified Logic Corpus remains `85/100`; no status change is authorized by RC6G.

## New route principle

The next route will be **live discovery**, with three independent candidate generators:

1. Topic-first Douyin search using a new plain-language query bank;
2. related/adjacent-video discovery from selected anchor videos;
3. limited creator-neighbor discovery, capped so creator-first material does not dominate.

HERMES remains mechanical only. It may search, enumerate results, collect metadata, dedupe IDs, download media, run ASR, compute deterministic metrics, and write evidence. It must not decide why wording is effective or whether a transcript is semantically good.

## Acceptance target for the next route

The next route should first prove that it can produce genuinely new IDs outside the 480-ID historical universe. If it cannot, it must stop with route-specific evidence instead of fabricating a completed corpus.
