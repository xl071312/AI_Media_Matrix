# HERMES Task — Plain Language Corpus V1 RC6G Reserve Build

Owner: HERMES
Authority: ChatGPT
Mode: **MECHANICAL COLLECTION / ASR / DEDUPE ONLY**
Do not perform semantic analysis.
Do not modify Verified Logic Corpus.
Do not declare Plain Language Corpus complete.

## Objective

Build a **large historically-unique, speech-dense reserve pool** so ChatGPT can perform the semantic selection for the final 30-sample Plain Language Corpus.

RC6F is not accepted as 30 usable samples. Preserve it unchanged as evidence.

Target for RC6G:

- at least **60 historically unique candidates** attempted;
- at least **40 MECHANICAL_PASS** candidates if available;
- every retained candidate must have real audio and real ASR output;
- ChatGPT, not HERMES, decides final semantic usability.

## 1. Read before work

Read:

- `handoff/chatgpt/CHATGPT_AUDIT_PLAIN_LANGUAGE_CORPUS_V1_RC6F.md`
- `01_benchmark/plain_language_corpus_v1/PLAIN_LANGUAGE_CORPUS_V1_MANIFEST.csv`
- `01_benchmark/GLOBAL_CONTENT_ID_REGISTRY.csv`

Also recover the pre-repair historical-ID evidence mechanically with:

`git show 3098ced289c460b0b159ce479dd68ca2641fbd2c:01_benchmark/plain_language_corpus_v1/PLAIN_LANGUAGE_CORPUS_V1_DUPLICATE_AUDIT.csv`

Do not reinterpret the audit semantically.

## 2. Historical ID universe — mandatory

The prior error came from comparing against only one incomplete registry representation.

Build `HISTORICAL_CONTENT_IDS_CANONICAL.txt` from the union of all mechanically discoverable Douyin IDs already present in benchmark history.

Sources must include at minimum:

1. `01_benchmark/GLOBAL_CONTENT_ID_REGISTRY.csv`;
2. the RC6E duplicate audit recovered from commit `3098ced...`;
3. existing Plain Language RC6F manifest;
4. structured ID fields under `01_benchmark` where the field name is one of:
   - `content_id`
   - `canonical_content_id`
   - `raw_content_id`
   - `aweme_id`
   - `video_id`
5. Douyin URLs matching `/video/<numeric_id>` in benchmark metadata files.

Canonicalization rule:

- strip `DY_REAL_` prefix;
- extract the numeric Douyin video ID;
- store as plain decimal string;
- deduplicate exactly.

Do **not** treat likes, timestamps, prices, durations or arbitrary long numbers as content IDs unless they appear in one of the explicit structured ID fields or `/video/<id>` URL position.

## 3. Candidate source

Use the existing real Douyin raw pool / verified discovery data already available in the project.

No simulated metadata.
No invented URLs.
No semantic topic judgments.
No web essay/search substitution.

Exclude every candidate whose canonical ID exists in `HISTORICAL_CONTENT_IDS_CANONICAL.txt`.

Also deduplicate internally before audio work.

## 4. Mechanical collection preference

To improve ASR yield without semantic judgment, prefer candidates with these purely mechanical properties when metadata permits:

- duration: **20–600 seconds**;
- nonzero likes/comments/favorites/shares where available;
- downloadable audio;
- stable media URL/source evidence.

Do not rank by any semantic quality such as “good explanation”, “clear logic”, “human language”, “viral reason”, or “Guanyu fit”. Those belong to ChatGPT.

## 5. ASR processing

For each attempted candidate:

- download/derive audio using the existing project route;
- run the existing ASR stack;
- save timestamped segments;
- save raw transcript;
- do not rewrite transcript prose;
- do not repair meaning manually;
- do not create semantic summaries.

Required per candidate files:

- `01_metadata.json`
- `02_performance.json`
- `03_audio_info.json`
- `04_transcript_raw.md`
- `05_segments.json`
- `06_mechanical_metrics.json`

## 6. Mechanical speech-density gate

A candidate may receive `MECHANICAL_PASS=true` only if all applicable conditions pass:

- `transcript_chars >= 120`;
- `segment_count >= 10`;
- at least 10 non-empty ASR segments;
- if duration >=30s, there is ASR speech within the first 30s;
- total ASR speech-span coverage / media duration >= 0.30 when computable;
- no single identical normalized segment accounts for >20% of all non-empty segments;
- transcript is not merely a title copied into the body;
- audio file exists and ffprobe duration is valid.

This gate is **not semantic usability**. Label it only `MECHANICAL_PASS` / `MECHANICAL_FAIL`.

Do not use `transcript_usable=true` as a semantic claim.

## 7. Output location

Create:

`01_benchmark/plain_language_corpus_v1/rc6g_reserve/`

Required top-level outputs:

- `RC6G_RESERVE_MANIFEST.csv`
- `RC6G_RESERVE_PERFORMANCE.csv`
- `RC6G_HISTORICAL_DUPLICATE_AUDIT.csv`
- `HISTORICAL_CONTENT_IDS_CANONICAL.txt`
- `RC6G_STATUS.md`

Manifest columns at minimum:

- candidate_id
- raw_content_id
- canonical_content_id
- platform
- title
- author
- duration_sec
- likes
- comments
- favorites
- shares
- transcript_chars
- segment_count
- nonempty_segment_count
- first30s_has_speech
- speech_coverage_ratio
- repeated_segment_max_ratio
- historical_duplicate
- internal_duplicate
- mechanical_pass
- source_url

## 8. Hard verification before commit

Before committing, assert mechanically:

1. zero `mechanical_pass=true` rows are historical duplicates;
2. zero `mechanical_pass=true` rows are internal duplicates;
3. every `mechanical_pass=true` row has `transcript_chars >=120`;
4. every `mechanical_pass=true` row has `segment_count >=10`;
5. every retained sample path exists;
6. audio/ASR source fields are not placeholders;
7. no semantic labels or conclusions were generated.

If fewer than 40 candidates pass after 60 attempts, continue through the available reserve pool up to **100 attempts**. If still below 40, STOP with truthful counts; do not lower gates and do not fabricate completion.

## 9. Do not do

HERMES must not:

- decide which samples are good examples of plain language;
- extract spoken-language rules;
- label logic engines;
- infer why a video performed;
- create Voice Profile hypotheses;
- rewrite ASR into polished Chinese;
- change `PLAIN_LANGUAGE_ENGINE_V0_4/V0_5`;
- update Verified Logic Corpus count;
- mark final corpus complete.

## 10. Completion response

Commit all RC6G reserve evidence to `chatgpt-handoff`.

Return **only the final commit SHA**.
