# CORPUS_COVERAGE — `zhinan_caijing` (直男财经)

> Phase B HERMES collection update: 2026-09-18 PT.

## Identity
- creator_id: `zhinan_caijing`
- display_name: 直男财经
- primary_platform: douyin
- homepage: https://www.douyin.com/user/MS4wLjABAAAADUObyc_aoKXnXnV01JEcZMdvU0_ZFvFnVQAU-weztOgHubCQont1aDrDASxWu8B6
- author verification: opened pages exposed the 直男财经 verified profile and `粉丝2311.0万获赞4.3亿`; no author mismatch observed.

## Homepage UI snapshot
- Works: **1422**
- Following: **199**
- Followers: **2311.0万**
- Likes received: **4.3亿**
- Homepage works grid was opened and deep-scrolled. The visible grid is not a complete history.

## Collection counts
| artifact | count | status |
|---|---:|---|
| url_inventory.jsonl unique URLs | 57 | 30 B01 seeds + 27 deep-scroll URLs |
| corpus_index rows | 30 | 30 seed rows retained |
| opened seed pages | 15 | author verified; raw JSON saved |
| COMPLETE transcripts | 0 | no full 文案/字幕 text exposed |
| INCOMPLETE opened pages | 15 | transcript_status=NONE |
| excluded | 0 | no exclusions made |
| failed | 0 | no failed captures logged |

## Raw and transcript status
- `raw/<id>.json` exists for each of the 15 opened seed pages. `playback_ok=true` records rendered/playing video UI.
- No `transcripts/<id>.txt` files were created: only embedded on-video Chinese captions were visible; the UI did not expose a complete 文案/字幕 text panel. No transcript text was invented.
- yt-dlp was not used. No media download/ASR attempt was made because the user-required UI metadata/transcript blocker was already established and no safe full-text panel was available.

## Seeds and visible-history caveat
- 30 B0.1 seeds remain in the index; first 15 were opened in this run. The remaining 15 are still `PENDING` and were not counted as opened.
- Deep-scroll inventory reached 57 unique video URLs. This is only the loadable visible grid segment, not full creator history.
