# HERMES Task — Plain-Language Spoken Corpus v1

Owner: HERMES mechanical/data only.
Semantic analysis owner: ChatGPT.

## Goal
Collect a new targeted Mandarin spoken-video corpus whose value is not merely topic coverage, but **how creators explain nontrivial ideas in ordinary language that ordinary Chinese viewers can understand immediately**.

This is not a general benchmark expansion. Do not collect randomly.

## Platforms
PRIMARY:
- Douyin
- Toutiao video

Do not use foreign platforms as primary sources.

## Target size
Collect **30 new unique videos** after dedupe.
Preferred reserve pool: 40–50 candidates before final filtering.

## Topic mix
Prioritize Chinese ordinary-person contexts:
- 职场 / 上班 / 工资 / 跳槽 / 老板
- 普通人赚钱 / 副业 / 小生意 / 创业
- 消费 / 买东西 / 存钱 / 中产 / 家庭支出
- AI 对普通工作的影响
- 普通人商业认知

Avoid highly technical finance, legal, medical, academic, geopolitical, or foreign-company-specific explainers unless the language is still clearly ordinary-person accessible.

## Mechanical selection criteria
Each final sample should satisfy as many as possible:
1. Mandarin spoken content with usable audio.
2. Duration preferably 60–360 seconds; longer allowed only if strongly relevant.
3. Real performance metadata available; no simulated values.
4. Prefer videos with substantial likes/favorites/shares/comments, but do not impose one universal threshold if platform data scale differs.
5. The first 30 seconds must be recoverable from actual audio/captions.
6. Full transcript must be recoverable with timestamps.
7. New content_id not already present in the existing global registry/corpus.
8. Prefer China-native examples, RMB amounts, Chinese workplace/business/consumer scenes.
9. Avoid foreign platform/product names in the first 30 seconds unless globally familiar in China.

## Required outputs per video
Create a new corpus root:
`01_benchmark/plain_language_corpus_v1/`

For each sample create:
- `01_metadata.json`
- `02_performance.json`
- `03_transcript_raw.json`
- `04_transcript_raw.md`
- `05_top_comments.csv` when obtainable
- `06_evidence_manifest.json`

Transcript must be actual ASR/captions only. Do not rewrite, summarize, normalize semantically, or improve wording.

## Master tables
Create:
- `PLAIN_LANGUAGE_CORPUS_V1_MANIFEST.csv`
- `PLAIN_LANGUAGE_CORPUS_V1_PERFORMANCE.csv`
- `PLAIN_LANGUAGE_CORPUS_V1_DUPLICATE_AUDIT.csv`
- `PLAIN_LANGUAGE_CORPUS_V1_STATUS.md`

Manifest fields at minimum:
- sample_id
- content_id
- platform
- title
- author
- duration_sec
- likes
- comments
- favorites
- shares
- transcript_chars
- transcript_usable
- first30s_available
- duplicate_status
- source_url_or_source_key

## Strongly preferred sample shapes
These are mechanical search targets only, not semantic labels to assign:
- specific money/result in first sentence
- direct ordinary-person question
- daily-life example used to explain a concept
- creator uses concrete numbers or actions instead of abstract terms
- case/story first, conclusion later
- visible contrast such as `普通人怎么做 / 高手怎么做`
- `你想想 / 为什么 / 我给你算一下 / 说白了 / 比如` type naturally spoken explanation

Do not score or infer why these work. ChatGPT will do that.

## Hard prohibitions
HERMES must NOT produce:
- Hook analysis
- Plain-language rules
- Logic map
- Cognitive gain
- Viral reason
- Why this performed
- Audience psychology
- Voice Profile
- Style judgment
- Semantic categories beyond basic factual metadata already visible in source

## Quality controls
- Dedupe against existing corpus by content_id/source URL/title+author where needed.
- No synthetic transcript.
- Missing fields = NULL, not guessed.
- Keep raw ASR imperfections.
- If a video cannot produce a usable transcript, mark unusable and replace it so final usable target remains 30.
- If the same route fails twice, stop that route and use another legal/available collection route.

## Completion condition
PASS only when:
- 30 unique new videos
- 30 usable full transcripts
- 30 first-30-second sections available
- real metadata captured where source exposes it
- duplicate audit complete
- no semantic analysis performed

Commit and push all outputs to `chatgpt-handoff`.
Return only the final Commit SHA to the user.
