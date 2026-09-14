# Pilot001 TTS v4

Owner: HERMES mechanical only. Publish remains locked.

Inputs:
- script: `04_content/pilots/guanyu_pilot_001_ability_monetization/02_script_v0_3.md`
- TTS config: `02_style_system/tts_config_v0_1.yaml`

Use exactly the text under `## Script`. Expected non-whitespace char count: **1272**. Use the config unchanged: `zh-CN-YunyangNeural`, rate `+0%`, pitch `+0Hz`, volume `+0%`.

Create `05_tts_draft_v4.mp3` and `05_tts_metrics_v4.json` in the same pilot directory. Measure audio duration with ffprobe.

Duration labels:
- 240–300s: `TTS_DURATION_PASS`
- 230–239s: `TTS_DURATION_REVIEW_SHORT`
- 301–310s: `TTS_DURATION_REVIEW_LONG`
- below 230s: `TTS_DURATION_FAIL_SHORT`
- above 310s: `TTS_DURATION_FAIL_LONG`

Metrics should record script version, char counts, config/voice/rate, duration, gate, audio path, generated time, `publish_authorized=false`, and `brand_voice_frozen=false`.

Do not rewrite the script, alter the TTS settings, perform semantic judgment, or start subtitles/video work. Commit and push the v4 outputs, then stop and return the Commit SHA.