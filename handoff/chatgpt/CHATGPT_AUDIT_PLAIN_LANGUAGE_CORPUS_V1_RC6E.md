# ChatGPT Audit — Plain Language Corpus V1 RC6E

Date: 2026-09-14
Owner: ChatGPT
Audit target: HERMES commit `3098ced289c460b0b159ce479dd68ca2641fbd2c`
Status: **FAIL AS COMPLETED CORPUS / REPAIR REQUIRED**

## Executive verdict

The user-facing verification claimed `30/30` unique, complete, transcribed samples. The repository state does not support that claim.

The commit is still useful as a candidate pool, but it must **not** be treated as a finished 30-new-video plain-language corpus and must not be used to freeze semantic language rules until repaired.

## Finding 1 — status and manifest contradict the PASS report

`PLAIN_LANGUAGE_CORPUS_V1_STATUS.md` says:
- `Status: PARTIAL - Audio download in progress`
- ASR processing pending
- transcript availability pending

`PLAIN_LANGUAGE_CORPUS_V1_MANIFEST.csv` marks all 30 rows:
- `transcript_usable=False`
- `first30s_available=False`

Therefore the repository does not currently contain a canonical machine-readable state matching the claimed `30/30 complete` result.

## Finding 2 — duplicate audit has an ID-normalization defect

The duplicate audit contains registry IDs in more than one form, including raw numeric Douyin IDs and IDs prefixed with `DY_REAL_`.

The selected candidate manifest uses raw numeric IDs. A candidate can therefore be marked `NEW` even when the same Douyin work already exists in the registry as `DY_REAL_<numeric_id>`.

Confirmed selected candidates that collide with existing-registry rows under prefix normalization include at least:

- `7533123064641506579`
- `7351254246710463755`
- `7439645541958552844`
- `7590019669398932763`
- `7666798588350065338`
- `7293036400465726783`
- `7559914938827803950`
- `7577322313134132520`
- `7540234540556619058`
- `7600369823520073126`
- `7479008308989316361`
- `7450364063030267151`
- `7673172635974421760`
- `7513092150196702476`
- `7564348993203948810`
- `7473417086673440012`

These 16 rows cannot count as new samples unless the registry itself is proven wrong. They may remain useful as corroborative language evidence, but not as new-corpus additions.

## Finding 3 — confirmed empty transcript artifacts

At least the following `04_transcript_raw.md` files contain only a heading/title and no actual transcript text or timestamped segments:

- `SAMPLE_013` / `7636452871718385906`
- `SAMPLE_016` / `7672955716349099387`
- `SAMPLE_019` / `7607833383963622309`
- `SAMPLE_021` / `7559367421950610739`
- `SAMPLE_026` / `7043715937320635663`
- `SAMPLE_027` / `7668735500266072425`
- `SAMPLE_028` / `7599226104158676914`

This is a lower bound, not a complete empty-file count. The repair must scan all 30 mechanically rather than relying on file existence.

## Finding 4 — file existence is not transcript completeness

Some samples do contain real ASR. Example: `SAMPLE_001` has 720 characters and 94 segments. But even there, content suitability is mixed: the video turns into a detergent native advertisement in the middle. This can be retained as raw evidence, but semantic inclusion must be decided by ChatGPT, not by the mechanical collector.

`SAMPLE_006` also contains a short real transcript with timestamped segments and ordinary workplace phrasing. It is potentially useful language evidence even though it does not by itself repair corpus completeness.

## Corpus accounting rule after this audit

Until repair passes, authoritative state is:

- candidate rows indexed: 30
- completed-new-unique plain-language corpus: **NOT ESTABLISHED**
- verified Logic Corpus: unchanged at 85
- semantic engine work may use individually audited usable transcripts, but must label old-registry overlaps as corroborative rather than new evidence.

## Required repair gates

A repaired V1 passes only if all are true:

1. 30 final samples are unique after canonical ID normalization.
2. Every final sample is absent from the pre-existing global registry after normalization.
3. Every final sample has a non-empty actual transcript with timestamped segments.
4. First 30 seconds are recoverable for every final sample.
5. Manifest fields are regenerated from actual final artifacts and show truthful status.
6. Duplicate audit compares canonicalized candidate IDs against canonicalized registry IDs and against the final set itself.
7. STATUS is regenerated last and agrees with all master tables.
8. HERMES performs no semantic analysis.

## Semantic-use policy during repair

ChatGPT may continue dismantling language from:
- the already verified historical corpus;
- individually checked usable RC6E transcripts;
- duplicated RC6E rows only as corroboration of previously seen behavior.

Do not freeze Hook / Plain-Language / Voice rules from the invalid `30/30` completion claim.
