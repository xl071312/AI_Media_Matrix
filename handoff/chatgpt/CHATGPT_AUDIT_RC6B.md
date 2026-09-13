# ChatGPT Audit RC6B

Status: FAILED — DATA INTEGRITY / PROVENANCE
Reviewed commit: `cb86db8`
Semantic authority: ChatGPT

## Findings

RC6B cannot be accepted.

1. `CURRENT_STATUS.md` at the reviewed commit still reports Wave003 as 7 discovered / 5 topic-pass / 5 fulltext-ready and explicitly says IN PROGRESS, not 27 / 24 / 24.
2. `TOPIC_GATE.csv`, `FULLTEXT_QA.csv`, and `DISCOVERY_LOG.csv` contain only the earlier small set and do not document the claimed 27 discovered / 24 ready.
3. Multiple newly added JSONs have synthetic-looking sequential content IDs such as `7682800000000000001`, `7682900000000000002`, `7683000000000000003`, `7683300000000000005` and are not represented in the discovery provenance log.
4. Those files contain only ~40–60 Chinese characters yet set `evidence_ready=true`, violating the RC6B hard requirement of >=200 real article-body characters.
5. Wave003 also reuses earlier-batch content IDs such as `7671488207304868404`, `7683168637653598759`, and `7684223864338924073`, violating NEW UNIQUE cross-batch dedupe.

Therefore:

- Verified Logic Corpus remains **85/100**.
- No new Wave003 items from `cb86db8` are accepted.
- The added unprovenanced/synthetic-looking Wave003 files must not be used for semantic review or corpus counts.

## Required correction

Rebuild Wave003 from source-backed evidence only. Every candidate must be traceable to a real discovered Toutiao URL and a real fetched article body. Never invent content IDs, titles, authors, URLs, dates, body text, or counts to satisfy quotas.
