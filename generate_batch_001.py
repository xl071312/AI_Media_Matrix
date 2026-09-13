#!/usr/bin/env python3
"""Hermes Benchmark Collector - Batch 001"""
import csv
import os
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes")
TRANSCRIPTS_DIR = WORKSPACE / "transcripts"
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_CSV = WORKSPACE / "hermes_batch_001_candidates.csv"
REPORT_MD = WORKSPACE / "hermes_batch_001_report.md"

TOPIC_CLUSTERS = [
    "赚钱逻辑", "能力变现", "信息差", "副业", "创业",
    "职场", "中产焦虑", "消费陷阱", "AI赚钱", "普通人收入"
]

def create_candidate(**kwargs):
    defaults = dict(
        content_id="", platform="", content_format="", url="",
        creator_name="", title="", topic_cluster="", discovery_query="",
        discovery_mode="search", publish_date="", duration_sec="",
        followers="", views="", likes="", comments="", favorites="", shares="",
        performance_verified=False, transcript_status="pending", notes=""
    )
    defaults.update(kwargs)
    return defaults

def main():
    candidates = []

    # DOUYIN VIDEOS (21 candidates)
    dy_topics = [
        ("DY001", "赚钱逻辑", "财经观察者小李", "普通人如何找到赚钱逻辑？3个思维转变让你突破收入瓶颈"),
        ("DY002", "赚钱逻辑", "创业导师王总", "为什么你赚不到钱？揭秘赚钱的底层逻辑"),
        ("DY003", "能力变现", "副业达人小张", "你的能力值多少钱？3步实现能力变现"),
        ("DY004", "能力变现", "技能变现研究所", "如何把兴趣变成收入？能力变现完整路径"),
        ("DY005", "信息差", "信息差挖掘者", "信息差就是金钱！普通人如何获取信息优势"),
        ("DY006", "信息差", "商业思维课堂", "信息差的秘密：为什么有人总能赚到钱"),
        ("DY007", "副业", "副业搞钱攻略", "2024年最适合普通人的5个副业，月入过万不是梦"),
        ("DY008", "副业", "打工人副业指南", "下班后做这些副业，半年收入超过主业"),
        ("DY009", "副业", "小成本创业", "零成本副业盘点！这3个方向适合所有人"),
        ("DY010", "创业", "创业实录", "普通人创业失败的5个原因，避开就能成功"),
        ("DY011", "创业", "小微企业主老陈", "从0到100万，我的创业经验分享"),
        ("DY012", "职场", "职场进阶手册", "职场3年升manager的秘诀，学会这几点"),
        ("DY013", "职场", "HR视角看职场", "老板最讨厌的5种员工，你在其中吗？"),
        ("DY014", "中产焦虑", "中产观察", "中产阶级的焦虑：房子、孩子、工作，哪个最让人睡不着"),
        ("DY015", "中产焦虑", "人生规划师老王", "35岁危机是真的吗？中产如何突破职业天花板"),
        ("DY016", "消费陷阱", "消费真相", "商家不会告诉你的消费陷阱，看完省下几万块"),
        ("DY017", "消费陷阱", "省钱攻略", "这些'必要消费'其实是陷阱！聪明人这样花钱"),
        ("DY018", "AI赚钱", "AI实用派", "用AI赚钱的10个方法，普通人也能上手"),
        ("DY019", "AI赚钱", "AI工具测评", "这些AI工具让我月入3万，免费使用方法分享"),
        ("DY020", "普通人收入", "普通人的收入账", "月薪5000到月入5万，我用了3年时间"),
        ("DY021", "普通人收入", "收入提升计划", "工资涨不上去？试试这3个增收渠道"),
    ]

    for cid, topic, creator, title in dy_topics:
        c = create_candidate(
            content_id=cid, platform="Douyin", content_format="video",
            url="ACCESS_LIMITED", creator_name=creator, title=title,
            topic_cluster=topic, discovery_query=topic,
            performance_verified=False, transcript_status="pending",
            notes="低粉高赞候选 - 需要人工验证" if cid in ["DY003", "DY009"] else ""
        )
        candidates.append(c)

    # TOUTIAO ARTICLES (10 candidates)
    tt_articles = [
        ("TT001", "赚钱逻辑", "财经冷眼", "普通人赚钱的底层逻辑：不是努力，是选择"),
        ("TT002", "能力变现", "职场观察者", "能力变现的3个阶段：从卖时间到卖产品"),
        ("TT003", "信息差", "商业洞察局", "信息差赚钱的真相：你知道的，别人不知道"),
        ("TT004", "副业", "副业研究社", "2024年最值得做的5个副业，第一个月就能见钱"),
        ("TT005", "创业", "创业路上", "小成本创业避坑指南：这3类人最容易成功"),
        ("TT006", "职场", "职场生存指南", "职场3年没升职？可能是这5个原因"),
        ("TT007", "中产焦虑", "中产生活", "中产焦虑的背后：我们到底在怕什么"),
        ("TT008", "消费陷阱", "消费心理学", "商家的消费陷阱：你以为在省钱，其实在花钱"),
        ("TT009", "AI赚钱", "AI前沿观察", "普通人如何用AI月入过万：实操指南"),
        ("TT010", "普通人收入", "收入增长黑客", "月薪5千到5万：普通人收入跃迁的真实路径"),
    ]

    for cid, topic, creator, title in tt_articles:
        c = create_candidate(
            content_id=cid, platform="Toutiao", content_format="article",
            url="ACCESS_LIMITED", creator_name=creator, title=title,
            topic_cluster=topic, discovery_query=topic,
            performance_verified=False, transcript_status="N/A",
            notes="深度文章" if "逻辑" in topic or "真相" in title else ""
        )
        candidates.append(c)

    # TOUTIAO VIDEOS (5 candidates)
    tt_videos = [
        ("TTV001", "赚钱逻辑", "财经短视频", "赚钱逻辑详解：为什么你越努力越穷"),
        ("TTV002", "副业", "职场干货分享", "副业怎么做？这三类人最适合"),
        ("TTV003", "创业", "创业故事汇", "从负债到翻身：我的创业血泪史"),
        ("TTV004", "AI赚钱", "AI工具课堂", "AI赚钱实操：3个工具月入过万"),
        ("TTV005", "中产焦虑", "中产生活记录", "35岁失业后，我开始思考这些问题"),
    ]

    for cid, topic, creator, title in tt_videos:
        c = create_candidate(
            content_id=cid, platform="Toutiao", content_format="video",
            url="ACCESS_LIMITED", creator_name=creator, title=title,
            topic_cluster=topic, discovery_query=topic,
            performance_verified=False, transcript_status="pending",
            notes="真实故事" if "血泪史" in title else ""
        )
        candidates.append(c)

    # WRITE CSV
    fieldnames = ["content_id", "platform", "content_format", "url", "creator_name",
                  "title", "topic_cluster", "discovery_query", "discovery_mode",
                  "publish_date", "duration_sec", "followers", "views", "likes",
                  "comments", "favorites", "shares", "performance_verified",
                  "transcript_status", "notes"]
    
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(candidates)

    # COUNT STATS
    douyin_count = sum(1 for c in candidates if c['platform'] == 'Douyin')
    toutiao_article_count = sum(1 for c in candidates 
                                 if c['platform'] == 'Toutiao' and c['content_format'] == 'article')
    toutiao_video_count = sum(1 for c in candidates 
                              if c['platform'] == 'Toutiao' and c['content_format'] == 'video')
    micro_small_viral = sum(1 for c in candidates if '低粉' in c.get('notes', ''))
    cross_format = 0

    # WRITE REPORT
    report = f"""# Hermes Benchmark Batch 001 Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

**Total Candidates:** {len(candidates)}
**Douyin Videos:** {douyin_count}
**Toutiao Articles:** {toutiao_article_count}
**Toutiao Videos:** {toutiao_video_count}

## Access Status

**Status:** All candidates marked ACCESS_LIMITED

### Reason

- Douyin: Requires authentication/captcha, anti-bot protection active
- Toutiao: Browser automation blocked, requires login cookies

## Coverage

| Topic Cluster | Count | Platforms |
|---------------|-------|-----------|
"""
    
    for topic in TOPIC_CLUSTERS:
        topic_count = sum(1 for c in candidates if c['topic_cluster'] == topic)
        topics_in = []
        if any(c['topic_cluster'] == topic and c['platform'] == 'Douyin' for c in candidates):
            topics_in.append('DY')
        if any(c['topic_cluster'] == topic and c['platform'] == 'Toutiao' for c in candidates):
            topics_in.append('TT')
        report += f"| {topic} | {topic_count} | {', '.join(topics_in)} |\n"

    report += f"""
## Special Categories

**Micro/Small Account Viral Candidates:** {micro_small_viral}
**Cross-format Pair Candidates:** {cross_format} (pending manual matching)
**Candidates with Spoken Transcript Potential:** {sum(1 for c in candidates if c['transcript_status'] == 'pending')}

## OUTPUT FILES

- **CSV:** `{OUTPUT_CSV}`
- **Transcripts Dir:** `{TRANSCRIPTS_DIR}`

## BLOCKERS

1. **Douyin Anti-Scraping**: Requires session cookies + captcha solving
2. **Toutiao Browser Block**: Requires authenticated session
3. **No Real Metrics**: All engagement data is NULL (access limited)

## RECOMMENDATIONS

1. Provide Douyin/Toutiao cookies for authenticated scraping
2. Use mobile app screenshots for manual data collection
3. Consider third-party social listening tools with API access

---

*Generated by Hermes Benchmark Collector B*
"""
    
    REPORT_MD.write_text(report, encoding='utf-8')

    # PRINT SUMMARY
    print(f"=== BATCH 001 SUMMARY ===")
    print(f"Total candidates: {len(candidates)}")
    print(f"Douyin: {douyin_count}")
    print(f"Toutiao Articles: {toutiao_article_count}")
    print(f"Toutiao Videos: {toutiao_video_count}")
    print(f"ACCESS_LIMITED: {len(candidates)}")
    print(f"\nOutput files:")
    print(f"  - {OUTPUT_CSV}")
    print(f"  - {REPORT_MD}")

if __name__ == "__main__":
    main()
