# ChatGPT -> HERMES Mechanical Task: Pilot001 TTS Check

Status: ACTION_REQUIRED
Owner: HERMES (mechanical only)
Semantic/script authority: ChatGPT

## Input

Read exactly:
- `04_content/pilots/guanyu_pilot_001_ability_monetization/02_script_v0_1.md`
- `04_content/pilots/guanyu_pilot_001_ability_monetization/04_qa_v0_1.md`

Do NOT rewrite, summarize, improve, shorten, expand, or semantically edit the script.

## Goal

Perform the deterministic TTS-duration gate for Pilot001.
This is a draft production check only. `publish_authorized=false` remains locked.

## Steps

1. Extract only the text under `## Script` from `02_script_v0_1.md`.
2. Calculate deterministic metrics:
   - Chinese/non-whitespace character count
   - punctuation count
   - paragraph count
3. Find and use the project's existing TTS configuration/voice if one is already configured.
4. If no existing project TTS voice/config exists, STOP and report `TTS_CONFIG_REQUIRED`. Do not choose a new voice yourself.
5. If configuration exists, synthesize a draft audio file without changing script wording.
6. Measure actual audio duration in seconds.
7. Do not change speaking speed solely to force the target duration unless the existing project config already specifies the speed.

## Duration gate

Target: 240–300 seconds.
Review band: 230–310 seconds.

Labels:
- `TTS_DURATION_PASS` = 240–300s
- `TTS_DURATION_REVIEW_SHORT` = 230–239s
- `TTS_DURATION_REVIEW_LONG` = 301–310s
- `TTS_DURATION_FAIL_SHORT` = <230s
- `TTS_DURATION_FAIL_LONG` = >310s

Do not edit the script after assigning the label. ChatGPT owns any semantic compression/expansion.

## Outputs

Under:
`04_content/pilots/guanyu_pilot_001_ability_monetization/`

Create if TTS runs:
- `05_tts_metrics.json`
- `05_tts_draft.<existing project audio extension>`

`05_tts_metrics.json` must contain:
- script_sha256
- tts_config_source
- voice_id/name if already configured
- speed if configured
- char_count
- punctuation_count
- paragraph_count
- duration_seconds
- duration_gate_label
- generated_at
- publish_authorized: false

If TTS cannot run, create:
- `05_tts_metrics.json` with status `TTS_CONFIG_REQUIRED` or the exact mechanical blocker.

## Hard boundaries

- No script editing.
- No semantic analysis.
- No Voice Profile inference.
- No new voice selection.
- No publishing.
- No video rendering yet.
- Do not modify personal-case facts/numbers.

## Final report only

- TTS: PASS / CONFIG_REQUIRED / FAIL
- Duration: <seconds or N/A>
- Gate: <label>
- Audio: <path or N/A>
- Push: PASS / FAIL
- Commit SHA: <sha>
