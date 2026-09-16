# 任务7 Douyin competitors — slow public crawl / 2026-09-16

- Scope: public Douyin web search/profile/video pages only; no login bypass, no private data. Parent handles are not collected; if comments appear later, label 家长A/B… . No child face close-ups saved.
- Search paths: 济南托管 (user), 济南汇智托管中心 (user), 槐荫托管 (user), 泉海托管 (user), 医学中心托管 (user), 托管 济南 市中区 (user), 晚托 济南 (user), 学生托管 济南 (user), 济南历山学校贝尔安亲托管 (general/video cards).
- New/expanded accounts in this run: 15 candidates processed; 13 net-new account names appended after dedupe, plus 2 existing accounts (泉海托管、乐恩托管) refreshed (see accounts_raw.jsonl). Key local additions: 济南汇智托管中心、济南槐荫知信教育信息咨询中心、泉海托管、济南市中大朗托管、书香致远托管中心、济南托管艳子老师、幼小衔接苗苗老师、济南历山学校贝尔安亲托管、状元楼校外托管、济南暖芽课后托辅中心（华山校区）、济南托管姜老师、济南悦童课后成长中心、济南市中区悦童年课后成长中心；品牌扩展：壹心托管官方号；区外但济南区县：阳阳小饭桌（仲宫）。
- Existing-account refresh: 泉海托管 and 乐恩托管 now have public IDs, follower/like counts, bio/location and profile URLs from the泉海托管 user-search page.
- Posts: 1 key video with stable ID (7675336617532168185) plus 11 exact full-caption search cards for 历山贝尔安亲; metrics/captions saved. Search cards did not expose stable post IDs in public DOM, so they are marked search_card_index rather than guessed IDs.
- Comments: key video page showed 全部评论 / 暂无评论 (0); no image replies or merchant replies. Search-card-only records are explicitly marked not expanded; no bypass.
- Covers/screens: 任务7_历山贝尔安亲_01.png and 任务7_壹心托管_post_7675336617532168185_cover.png (also mirrored to 02_douyin_competitors).
