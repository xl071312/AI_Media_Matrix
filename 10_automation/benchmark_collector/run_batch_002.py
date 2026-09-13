#!/usr/bin/env python3
"""
Batch 002 - New Data Collection via MediaCrawler
HERMES Role: DATA ENGINEER ONLY
Target: 30 NEW UNIQUE content IDs
"""
import asyncio
import sys
import os
from pathlib import Path

# Add MediaCrawler to path
MC_PATH = Path(r"F:\workspace\AI_Media_Matrix\10_automation\benchmark_collector\MediaCrawler")
sys.path.insert(0, str(MC_PATH))

async def main():
    print("=== BATCH 002 - NEW DATA COLLECTION ===\n")
    
    # Import MediaCrawler
    import cmd_arg
    import config
    from var import crawler_type_var
    
    # Configure for new unique topics
    config.PLATFORM = "dy"
    config.CRAWLER_TYPE = "search"
    
    # Use different keywords to avoid duplicates
    config.KEYWORDS = """赚钱逻辑,能力变现,信息差,副业,创业,职场,中产焦虑,消费陷阱,AI赚钱,普通人收入,财富认知,搞钱,赚钱思维,普通人翻身,商业思维,加盟避坑,创业失败,投资认知,黄金回收,消费降级,知识付费,个人品牌,自由职业,远程工作,数字游民,副业刚需,斜杠青年,轻资产创业,小成本创业,实体转型,线上创业,内容创业,IP打造,流量变现,私域流量,直播带货,短视频带货,电商创业,跨境电商,自媒体创业,社群运营,社群变现,付费社群,知识星球,在线咨询,企业服务,SaaS创业,工具开发,小程序开发,APP开发,游戏开发,游戏测试,游戏代练,游戏交易,虚拟物品,数字产品,虚拟商品,教育资源,在线课程,教育资讯,升学规划,职业规划,职场技能,软技能,硬技能,沟通技巧,谈判技巧,领导力,团队管理,项目管理,时间管理,效率提升,生产力工具,AI工具,自动化工具,无代码工具,低代码平台,数据分析,数据可视化,商业分析,市场分析,用户研究,产品思维,设计思维,用户体验,产品设计,产品管理,产品经理,运营思维,内容运营,用户运营,活动运营,增长黑客,裂变营销,渠道推广,SEO优化,SEM投放,社交媒体,内容营销,品牌营销,公关传播,事件营销,热点营销,危机公关,舆论引导,舆情监控,舆情分析,舆情报告,公关策略"""
    
    config.START_TIME = "2024-01-01"
    config.END_TIME = "2026-09-01"
    config.PROXY = ""
    config.ITERATION_INTERVAL = 5
    config.CRAWL_TYPE = "search"
    config.ENABLE_GET_COMMENTS = True
    config.COMMENT_START_TYPE = "hot"
    config.MAX_COMMENT_COUNT = 50
    
    # Load existing CIDs to exclude
    EXISTING_CIDS = set()
    BATCH_DIR = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark\analysis_batches")
    for batch in BATCH_DIR.glob("batch_*"):
        for s in batch.glob("sample_*"):
            try:
                import json
                meta = json.load(open(s / "01_metadata.json"))
                EXISTING_CIDS.add(meta.get('content_id', ''))
            except:
                pass
    
    print(f"Existing CIDs to exclude: {len(EXISTING_CIDS)}")
    
    # Run crawler
    from main import CrawlerFactory
    crawler = CrawlerFactory.create_crawler(config.PLATFORM)
    crawler_type_var.set(config.CRAWLER_TYPE)
    
    print(f"\nStarting crawler for platform: {config.PLATFORM}")
    print(f"Crawler type: {config.CRAWLER_TYPE}")
    
    try:
        await crawler.run()
        print("\n✓ Crawler completed")
    except Exception as e:
        print(f"\n✗ Crawler error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
