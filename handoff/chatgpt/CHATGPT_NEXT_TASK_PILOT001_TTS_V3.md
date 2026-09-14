# ChatGPT -> HERMES Mechanical Task: Pilot001 TTS v3

Status: ACTION_REQUIRED
Owner: HERMES (mechanical only)
Semantic/script authority: ChatGPT
Publish authorization: false

## Read first

- `02_style_system/tts_config_v0_1.yaml`
- `04_content/pilots/guanyu_pilot_001_ability_monetization/02_script_v0_2.md`
- `04_content/pilots/guanyu_pilot_001_ability_monetization/04_qa_v0_2.md`

Do not use v0.1 script and do not use the old auto-selected Hong Kong voice.

## Exact TTS config

Use the exact values from `02_style_system/tts_config_v0_1.yaml`:

- provider: edge-tts
- voice_id: `zh-CN-YunyangNeural`
- locale: `zh-CN`
- rate: `+0%`
- pitch: `+0Hz`
- volume: `+0%`

This config is **PROVISIONAL_PILOT**, not a frozen brand voice.

## Step 1 — Mechanical availability check

Enumerate installed/available edge-tts voices only to verify whether the exact configured `zh-CN-YunyangNeural` exists.

Do not rank, recommend, or substitute voices.

If exact voice is unavailable:
- do not synthesize audio;
- write metrics with `status=VOICE_UNAVAILABLE`;
- `duration_seconds=null`;
- `duration_gate_label=VOICE_UNAVAILABLE`;
- stop.

## Step 2 — Script integrity

Use exactly the text under `## Script` in:

`04_content/pilots/guanyu_pilot_001_ability_monetization/02_script_v0_2.md`

Expected script SHA256 from prior verified run:
`db1c7fc61dd38088d1990dfd37c50086ca210fc3aff5a5db334d6eb46d0fe903`

Expected non-whitespace char count: `888`.

If either differs, STOP with `SCRIPT_INTEGRITY_FAIL`. Do not synthesize.

No rewriting, summarizing, punctuation editing, rate tuning, or semantic changes.

## Step 3 — Synthesize exact draft

If voice and script integrity both pass, synthesize exactly once using the configured voice/rate/pitch/volume.

Outputs:
- `04_content/pilots/guanyu_pilot_001_ability_monetization/05_tts_metrics_v3.json`
- `04_content/pilots/guanyu_pilot_001_ability_monetization/05_tts_draft_v3.mp3`

Measure audio duration with ffprobe or equivalent deterministic media metadata.

Duration gate:
- PASS: 240–300s
- REVIEW_SHORT: 230–239.9s
- REVIEW_LONG: 300.1–310s
- FAIL_SHORT: <230s
- FAIL_LONG: >310s

Do not change speaking rate to force a PASS.

## Metrics JSON required fields

- status
- script_version: `v0.2`
- script_sha256
- config_version: `v0.1`
- tts_config_source_path: `02_style_system/tts_config_v0_1.yaml`
- provider
- voice_id
- locale
- rate
- pitch
- volume
- char_count
- chinese_char_count
- punctuation_count
- paragraph_count
- compression_ratio_vs_v01
- duration_seconds
- duration_gate_label
- audio_path
- generated_at
- publish_authorized: false
- brand_voice_frozen: false

## Hard boundaries

- No voice substitution.
- No rate tuning.
- No script editing.
- No semantic analysis.
- No Voice Profile inference.
- No video rendering.
- No publishing.
- Do not change the user's first-hand business-case numbers.

## Final report only

- TTS: PASS / REVIEW / FAIL / VOICE_UNAVAILABLE / SCRIPT_INTEGRITY_FAIL
- Script chars: <n>
- Voice: <voice>
- Rate: <rate>
- Duration: <seconds or N/A>
- Gate: <label>
- Audio: <path or N/A>
- Push: PASS / FAIL
- Commit SHA: <sha>
