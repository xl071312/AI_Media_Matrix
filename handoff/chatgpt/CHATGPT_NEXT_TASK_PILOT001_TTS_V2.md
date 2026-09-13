# ChatGPT -> HERMES Mechanical Task: Pilot001 TTS v2

Status: ACTION_REQUIRED
Owner: HERMES (mechanical only)
Semantic/script authority: ChatGPT
Publish authorization: false

## Read first

- `handoff/chatgpt/CHATGPT_AUDIT_PILOT001_TTS_V1.md`
- `04_content/pilots/guanyu_pilot_001_ability_monetization/02_script_v0_2.md`
- `04_content/pilots/guanyu_pilot_001_ability_monetization/04_qa_v0_2.md`

Do not use `02_script_v0_1.md` for this run.

## Critical correction from TTS v1

TTS v1 auto-selected `zh-HK-HiuGaaiNeural`. That violated the prior task boundary because HERMES was not authorized to choose a new voice.

For v2, **do not enumerate voices and pick one**.

Before synthesizing anything, search the existing project for a pre-existing explicit TTS config/voice selection. Record the exact source path and exact configured voice/speed.

The search may inspect configuration or production files already inside `F:\workspace\AI_Media_Matrix`, but must not create a new preference.

If no explicit project TTS config exists, STOP with:

`TTS_CONFIG_REQUIRED`

Do not synthesize audio in that case.

The prior `zh-HK-HiuGaaiNeural` is NOT approved unless it is independently present in a pre-existing project configuration or the user has explicitly approved it.

## Script integrity

Use exactly the text under `## Script` in:

`04_content/pilots/guanyu_pilot_001_ability_monetization/02_script_v0_2.md`

No rewriting, summarizing, punctuation editing, speed-forcing, or semantic changes.

## Deterministic metrics

Calculate:
- script SHA256
- non-whitespace character count
- Chinese-character count
- punctuation count
- paragraph count
- compression ratio vs v0.1 char_count=1420

## If valid TTS config exists

Synthesize draft audio with exactly that configured voice and configured speed.

Output:
- `04_content/pilots/guanyu_pilot_001_ability_monetization/05_tts_metrics_v2.json`
- `04_content/pilots/guanyu_pilot_001_ability_monetization/05_tts_draft_v2.<configured extension>`

Measure duration with ffprobe or equivalent deterministic media metadata.

Duration target:
- PASS: 240–300s
- REVIEW_SHORT: 230–239s
- REVIEW_LONG: 301–310s
- FAIL_SHORT: <230s
- FAIL_LONG: >310s

Metrics JSON must include:
- status
- script_version: `v0.2`
- script_sha256
- tts_config_source_path
- voice_id/name
- locale if declared
- speed if declared
- char_count
- chinese_char_count
- punctuation_count
- paragraph_count
- compression_ratio_vs_v01
- duration_seconds
- duration_gate_label
- generated_at
- publish_authorized: false

## If no valid config exists

Create only:

`04_content/pilots/guanyu_pilot_001_ability_monetization/05_tts_metrics_v2.json`

with:
- status: `TTS_CONFIG_REQUIRED`
- script_version: `v0.2`
- script_sha256
- char_count / chinese_char_count / punctuation_count / paragraph_count
- compression_ratio_vs_v01
- tts_config_source_path: null
- voice_id: null
- duration_seconds: null
- duration_gate_label: `TTS_CONFIG_REQUIRED`
- publish_authorized: false

No audio file.

## Hard boundaries

- No voice selection.
- No script editing.
- No semantic analysis.
- No Voice Profile inference.
- No video rendering.
- No publishing.
- Do not modify the user's first-hand business-case numbers.

## Final report only

- TTS: PASS / CONFIG_REQUIRED / FAIL
- Script chars: <n>
- Config source: <path or N/A>
- Voice: <voice or N/A>
- Duration: <seconds or N/A>
- Gate: <label>
- Audio: <path or N/A>
- Push: PASS / FAIL
- Commit SHA: <sha>
