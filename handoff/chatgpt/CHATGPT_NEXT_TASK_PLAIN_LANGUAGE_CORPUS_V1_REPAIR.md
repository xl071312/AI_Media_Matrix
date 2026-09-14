# HERMES Task — Plain Language Corpus V1 Repair

Owner: HERMES mechanical/data only.
Semantic analysis owner: ChatGPT.
Input audit: `handoff/chatgpt/CHATGPT_AUDIT_PLAIN_LANGUAGE_CORPUS_V1_RC6E.md`
Target branch: `chatgpt-handoff`

## Goal
Repair `01_benchmark/plain_language_corpus_v1/` so that it contains **30 truly new, unique, mechanically complete spoken-video samples** suitable for later ChatGPT semantic analysis.

Do not preserve a candidate merely because its files already exist. The final corpus must satisfy the gates below.

## 1. Canonical ID normalization — mandatory before dedupe

For Douyin content IDs, compare canonical numeric work IDs, not raw registry strings.

Mechanical normalization rules:
- trim whitespace;
- if an ID starts with `DY_REAL_`, remove that prefix before comparison;
- treat remaining numeric Douyin work ID as the canonical comparison key;
- preserve original/raw ID separately when useful for evidence;
- do not infer or rewrite a numeric ID.

Run dedupe against:
1. `01_benchmark/GLOBAL_CONTENT_ID_REGISTRY.csv`;
2. all existing benchmark manifests/registries needed to cover the historical corpus;
3. the 30 final candidates themselves.

Any candidate whose normalized content ID already exists historically is **not new** and must be replaced.

Known collision candidates identified by ChatGPT audit include at least:
`7533123064641506579, 7351254246710463755, 7439645541958552844, 7590019669398932763, 7666798588350065338, 7293036400465726783, 7559914938827803950, 7577322313134132520, 7540234540556619058, 7600369823520073126, 7479008308989316361, 7450364063030267151, 7673172635974421760, 7513092150196702476, 7564348993203948810, 7473417086673440012`.

Do not rely only on this list. Recompute the full audit mechanically.

## 2. Transcript-content validation — mandatory

For every final sample, inspect actual transcript content, not file existence.

A usable sample must have:
- actual spoken transcript text beyond headings/metadata;
- timestamped segments from real audio/captions;
- at least one segment intersecting the first 30 seconds;
- non-zero transcript character count based on spoken text only.

Files that contain only a title/header are unusable and must be replaced or reprocessed.

Known empty/unusable examples found by ChatGPT include at least SAMPLE_013, SAMPLE_016, SAMPLE_019, SAMPLE_021, SAMPLE_026, SAMPLE_027, SAMPLE_028 in the current RC6E state. Re-scan all 30; do not assume this is the complete list.

## 3. Collection target

Final corpus target remains 30.

Preferred source mix:
- Douyin primary;
- Toutiao video allowed;
- China-native scenes preferred;
- spoken Mandarin;
- ordinary-person topics: work, salary, boss/customer, side income, small business, consumption, household spending, AI impact on ordinary work, practical business cognition.

Preferred duration: 60–360s. Longer may be retained if highly relevant and mechanically usable.

Do not choose foreign-company/platform-specific explainers as the main sample shape.

## 4. Per-sample required artifacts

For every final sample directory:
- `01_metadata.json`
- `02_performance.json`
- `03_transcript_raw.json`
- `04_transcript_raw.md`
- `05_top_comments.csv` when obtainable
- `06_evidence_manifest.json`

Transcript must remain raw actual ASR/captions. No semantic rewrite, normalization, summarization, or style cleanup.

## 5. Regenerate master tables from final artifacts

Rebuild, do not patch around stale rows:
- `PLAIN_LANGUAGE_CORPUS_V1_MANIFEST.csv`
- `PLAIN_LANGUAGE_CORPUS_V1_PERFORMANCE.csv`
- `PLAIN_LANGUAGE_CORPUS_V1_DUPLICATE_AUDIT.csv`
- `PLAIN_LANGUAGE_CORPUS_V1_STATUS.md`

Manifest must derive fields from actual files and include at minimum:
- sample_id
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
- transcript_usable
- first30s_available
- historical_duplicate
- internal_duplicate
- source_url_or_source_key

Duplicate audit must include both raw and canonical IDs and clearly show comparison result against historical registry.

## 6. Status-generation order

Generate `PLAIN_LANGUAGE_CORPUS_V1_STATUS.md` **last**, after every other artifact is complete.

PASS status is allowed only if all of these equal 30:
- final unique samples
- historically new samples
- non-empty usable transcripts
- first-30-second availability

If any count is below 30, status must be PARTIAL/FAIL and state exact blockers.

## 7. Hard prohibitions

HERMES must NOT produce:
- hook analysis
- spoken-language rules
- semantic categories
- logic maps
- cognitive gain
- viral explanations
- audience psychology
- style judgments
- Voice Profile
- Guanyu script text

Do not decide whether a transcript is 'good language'; only validate mechanical usability.

## 8. Route-failure rule

If the same acquisition route fails twice for a replacement sample, stop that route and switch to another available legal route. Do not loop indefinitely.

## Completion response

Commit and push the repaired corpus and regenerated master tables.
Return only the final Commit SHA to the user.
