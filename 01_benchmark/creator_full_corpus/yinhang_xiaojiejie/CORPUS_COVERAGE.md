# CORPUS_COVERAGE — 银行小姐姐 (`yinhang_xiaojiejie`)

- homepage: https://www.douyin.com/user/MS4wLjABAAAAPZgqlIO2MpT0SBcAjLaFbL_c6LvEojAXy1udEgzugQg
- primary_platform: douyin
- homepage UI stats: works_count=518; followers=186.5万; likes_received=2651.6万
- visible_works: 518 (homepage UI)
- homepage-scroll inventory collected: 61 unique `/video/` URLs (initial loadable grid; repeated deep-scroll/PageDown produced no additional links)
- inventory_count: 61
- B0.1 seeded URLs: 30
- opened this session: 15 (first 15 B0.1 seeds; author UI matched 银行小姐姐)
- complete_fulltext: 0
- excluded: 0
- failed: 16 logged entries (15 UI no-full-caption-panel checks + 1 ASR/audio-download blocker); metadata pages themselves saved
- transcript_status: NONE for all 15; no full transcript text obtained
- raw_source_status: SAVED for all 15 opened pages
- blockers: UI review completed for all 15 opened seed pages with author 银行小姐姐 confirmed. No full 文案/字幕/caption panel or copy-text control was exposed. Some player captions and AI-generated 章节要点 were visible, but only partial/summary text, not complete speech, so no transcript files or COMPLETE rows were created. Douyin yt-dlp audio extraction returned HTTP 403 Forbidden and “Fresh cookies ... are needed”; no credentials/cookies used.
- note: do not equate visible_works with obtainable full corpus; homepage list was only partially loadable in this session. UI transcript review did not produce a complete spoken transcript for any of the 15 seeds.

Updated: 2026-09-19T01:40:00Z

## ASR retry log
- 2026-09-19T01:41:18.448934+00:00: exported Chromium cookies (410) via yt-dlp --cookies-from-browser; Douyin web detail JSON still HTTP 403. Cookie DB values empty when copied (OS-encrypted). Blocker remains: need browser-side 文案/字幕全文 capture or alternative media intercept — not inventable.


## UI transcript review
- Reviewed: 15/15 opened seed pages; author UI matched 银行小姐姐.
- Full transcripts obtained: 0.
- Result: all 15 remain NONE/INCOMPLETE; failed.csv records stage=ui_transcript, reason=no_full_caption_panel for each.

Updated: 2026-09-19T01:50:32.185749+00:00

## UI 文案 pass (2026-09-19T01:55:06.600951+00:00)
- Reviewed all 15 seed pages; author matched.
- No full 文案/字幕 copy panel; only partial on-screen captions / AI chapter summaries.
- Full transcripts obtained: 0. transcripts/ empty.
- yt-dlp still blocked (403). Next: media-stream intercept OR accept Douyin transcript gap for this batch while harvesting Toutiao fulltext creators.
