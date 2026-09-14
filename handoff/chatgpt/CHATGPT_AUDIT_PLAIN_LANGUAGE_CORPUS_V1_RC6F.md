# ChatGPT Audit — Plain Language Corpus V1 RC6F

Date: 2026-09-14
Owner: ChatGPT
Audited commit: `8db686051f59627a301ab1cf24434fbe3efff4bf`
Status: **PARTIAL / NOT ACCEPTED AS 30-USABLE-SAMPLE CORPUS**

## Executive finding

RC6F is materially better than RC6E: canonical numeric IDs are now present, the 30 sample directories exist, and the manifest records transcript/segment counts. However, the reported `30/30 new unique` and `30/30 complete` are not sufficient for acceptance of the Plain Language Corpus.

The correct current interpretation is:

- 30 sample slots exist;
- 12 have more than 50 transcript characters according to the manifest;
- 18 are empty/too short mechanically;
- at least 3 of the 30 are historical duplicates after canonicalizing prior `DY_REAL_` IDs;
- character count alone produces semantic false positives;
- after ChatGPT semantic inspection, only a small subset is currently suitable for positive plain-language pattern extraction.

The Verified Logic Corpus remains **85/100**. RC6F does not change it.

## 1. Internal status contradiction

`PLAIN_LANGUAGE_CORPUS_V1_STATUS.md` says:

- Collected: 30
- New unique: 12
- Duplicate in registry: 0
- Empty transcript: 18
- No first 30s: 17

The external RC6F summary instead says `New unique 30/30` and `12/30 usable transcripts`.

`New unique: 12` in STATUS appears to be a mislabeled usable-transcript count, not a defensible uniqueness count. The status vocabulary must be corrected so uniqueness and transcript usability are never conflated.

## 2. Historical duplicate check still incomplete

RC6F's new duplicate audit checks the current `GLOBAL_CONTENT_ID_REGISTRY.csv`, but the prior RC6E audit had already preserved historical IDs using both numeric and `DY_REAL_` forms.

After canonicalization, at least these RC6F samples are already historical corpus IDs:

- `RC6F_001` — `7533123064641506579` = prior `DY_REAL_7533123064641506579`
- `RC6F_002` — `7351254246710463755` = prior `DY_REAL_7351254246710463755`
- `RC6F_004` — `7293036400465726783` = prior `DY_REAL_7293036400465726783`

Therefore `30/30 new unique` is false under the historical-universe definition already used by the project.

Future duplicate gating must compare against the union of all historical corpus IDs, not only one registry file.

## 3. Mechanical transcript threshold is not semantic usability

The manifest treats `>50 chars` as usable. This is only a mechanical prefilter.

Counterexample:

### RC6F_006

83 characters / 36 segments, but the transcript is dominated by repeated fragments such as `电视台`, `有限内`, `放开`, and repeated `我`. It is not semantically reconstructable and must be **SEMANTIC_FAIL**, despite clearing the character threshold.

### RC6F_007

962 characters / 168 segments, but the ASR mixes severe corruption, dialogue, scene changes and unrelated-sounding spans. It may contain locally recoverable phrases, but it is not reliable enough for exact spoken-expression mining. Classify **STRUCTURE_REVIEW / PHRASE_FAIL** rather than positive plain-language evidence.

### RC6F_009

The opening is partly understandable but later spans degrade strongly and the content relies heavily on fortune/engagement-bait framing. It can serve as a **negative/control example**, not a positive Guanyu voice exemplar.

## 4. Current semantic classification

This is a ChatGPT semantic judgment; HERMES must not reproduce or modify it.

### Positive structure-usable candidates

- `RC6F_003` — concise role/action slots; ASR noisy but core structure recoverable.
- `RC6F_008` — concrete price examples, rhetorical questions, category-by-category contrast; phrase-level ASR noisy.
- `RC6F_010` — strong positive exemplar: familiar topic, audience-role fork, quantified before/after, concrete analogy, process story.
- `RC6F_011` — strong positive exemplar: equivalence converter (`48元咖啡` vs everyday food; `1000元` alternative uses), before/after contrast, short sentences.
- `RC6F_012` — strong positive exemplar: one stable fictional carrier, intuitive contradiction, behavior consequence, then concept label.
- `RC6F_013` — structure usable: personal stake, questions, familiar money units, list progression; factual/advice claims are not transferable without verification.

### Negative / control candidate

- `RC6F_009` — recognizable engagement and certainty mechanics, but too much manipulative/unsupported framing and degraded ASR for positive voice learning.

### Semantic fail / not countable

- `RC6F_006` — ASR semantically unusable.
- `RC6F_007` — too corrupted/scene-mixed for reliable phrase mining.

### Mechanical fail / not countable

- `RC6F_005` and `RC6F_014..030` — insufficient transcript content under the current manifest.

### Historical duplicate / not countable as new independent sample

- `RC6F_001`, `RC6F_002`, `RC6F_004`.

## 5. Acceptance rule going forward

A sample is countable toward the 30-sample Plain Language Corpus only if all are true:

1. canonical content ID is absent from the full historical-ID universe;
2. no internal duplicate;
3. transcript has meaningful speech content, not merely `>50 chars`;
4. enough continuous intelligible speech exists to analyze explanation order;
5. sample is not dominated by unrelated film/drama fragments, music lyrics, or ASR hallucination;
6. exact phrase mining is allowed only when phrase-level ASR is sufficiently reliable;
7. semantic suitability is decided by ChatGPT, not HERMES.

## 6. Operational consequence

Do **not** mark Plain Language Corpus V1 complete.

RC6F should be retained as an evidence attempt. The next mechanical collection should produce a larger reserve pool of speech-dense, historically unique candidates. ChatGPT will then select the final replacements semantically.

No need to touch the Verified Logic Corpus. It remains 85/100.
