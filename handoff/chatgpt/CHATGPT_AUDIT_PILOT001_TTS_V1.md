# ChatGPT Audit — Pilot001 TTS v1

Reviewed commit: `28527ac`
Owner: ChatGPT

## Verdict

The TTS run produced a real measurable audio duration, but it is **not a compliant production TTS gate**.

Observed metrics:
- script chars (non-whitespace): 1420
- duration: 425.1s
- gate reported: `TTS_DURATION_FAIL_LONG`
- voice used: `zh-HK-HiuGaaiNeural`
- config source reported: `edge-tts (system default)`
- publish_authorized: false

## Compliance issue

The assigned task required HERMES to use an already configured project TTS voice, and to stop with `TTS_CONFIG_REQUIRED` if no project voice/config existed.

Instead, the implementation enumerated Edge TTS voices and automatically selected a Chinese female voice. That is a new voice-selection decision owned by the semantic/production layer, not HERMES.

Therefore:

- `425.1s` is valid only as a measurement for the auto-selected `zh-HK-HiuGaaiNeural` run.
- It must **not** be treated as the authoritative production duration for Guanyu.
- The voice is not approved merely because the run completed.
- The v1 audio remains draft/test evidence only.

## Semantic response

Independent of the voice problem, Script v0.1 is verbose relative to the current production target and contains repeated explanations that can be compressed without sacrificing the causal spine.

ChatGPT therefore creates Script v0.2 with these goals:
- preserve L3 State Transition as primary engine and L5 Constraint Optimization as secondary;
- preserve the user's first-hand turnaround case;
- preserve costly-problem -> result -> payer -> trust -> transaction -> repeatability;
- compress repeated examples, repeated definitions, and list-like transitions;
- keep 3–5 cognitive-gain nodes;
- remain publication-locked.

## Next TTS rule

TTS v2 must first locate an explicit pre-existing project TTS configuration and cite its repository/local path.

If none exists, return `TTS_CONFIG_REQUIRED`. Do not choose another voice automatically.

The v1 voice `zh-HK-HiuGaaiNeural` may only be reused if it is independently found in a pre-existing project config or explicitly approved by the user.
