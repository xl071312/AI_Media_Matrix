# Phase C Analyzer Brief

## Output
`/workspace/AI_Media_Matrix/01_benchmark/creator_full_corpus/analysis/deep_items/<creator_id>/<work_id>.json`

## Required 25 fields (exact names)
1. `opening_move`
2. `claim_chain`
3. `logic_units`
4. `transition_language`
5. `contrast_method`
6. `question_method`
7. `example_method`
8. `abstract_to_concrete`
9. `judgement_language`
10. `self_correction`
11. `rhythm`
12. `spoken_markers`
13. `emotion_curve`
14. `closure_loop`
15. `cta_style`
16. `anti_ai_signals`
17. `weakness`
18. `thought_process_exposure`
19. `listener_positioning`
20. `concrete_anchor`
21. `information_density_curve`
22. `sentence_flow`
23. `viewpoint_personality`
24. `memory_device`
25. `guanyu_transfer_value`

## Record schema
- creator_id, work_id, modality, source_url, source_sha256, performance_tier
- spoken_marker_eligible, analysis_status=`OK`, analyzer_version=`phase_c_v1`
- sentence_count, fields{25}, evidence_sentence_ids, fields_complete_25=true

## Field shapes
- default: `{summary, patterns:[], evidence:[{sentence_id, snippet(<=40 chars), note}]}`
- logic_units: `{units:[{unit_id, sentence_ids, function, note}]}` covering window
- spoken_markers: if COMPLETE_TEXT → status=`N/A_TEXT_MODALITY`; if eligible=NO → `SKIPPED_INELIGIBLE`; else list fillers/repairs with evidence
- guanyu_transfer_value: `{decision: KEEP|ADAPT|REJECT, reason, evidence}`

## Hard rules
1. Not a summary. Bind sentence_id for every claim.
2. Do not invent spoken pauses for TEXT modality.
3. Do not compute filler frequency when spoken_marker_eligible=NO.
4. Snippets <=40 chars; no full-paragraph paste.
5. Patterns must be specific; ban empty labels like 口语化/逻辑强.
6. Create parent dirs as needed.
