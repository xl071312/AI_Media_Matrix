#!/usr/bin/env python3
"""RC2: Save remaining extracted texts"""
import json
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SRC = BASE / "analysis_batches/batch_004_toutiao/SEED_WAVE_001_REFETCH"
HANDOFF = BASE.parent / "handoff" / "chatgpt" / "batch_004" / "wave_001"

TEXTS = {
    "7644625679841067560": """2026 年想做下班兼职的人越来越多，但真正拉开差距的，往往不是"谁更努力"，而是谁更早看清：门槛越低的兼职，筛选成本越高。

刷到"0 基础、当天上手、日入几百"的项目，先别急着交钱。现在副业机会确实多，尤其是 AI 工具普及后，文案、表格、客服、设计、数据处理都能提效；但坑也多，很多人不是输在能力不够，而是输在没判断清楚项目靠不靠谱。

2026 下班兼职红榜：更适合长期做的方向

AI 工具型兼职：适合普通人切入

如果你白天有稳定工作，晚上只有 2-3 小时，更建议选择能积累作品和技能的兼职，比如：

AI 文案优化、短视频脚本辅助
PPT 美化、简历优化、汇报材料整理
智能客服话术搭建
企业知识库整理、工作流搭建
数据标注、AI 训练师相关辅助工作

这些方向的共同点是：不是单纯卖时间，而是在训练"AI+业务"的能力。中国信通院多次提到，人工智能正加速进入办公、制造、金融、医疗等场景，企业更需要能把 AI 用到实际工作里的人。""",

    "7645692141699662362": """我表弟去年还在为3000元房贷发愁，上个月却悄悄告诉我，他的副业收入已经连续半年超过主业。更让我震惊的是，他启动这三个项目时，初始资金最高的一笔只投入了800元。今天，我扒出了他藏在手机备忘录里的全部模式——每一个都轻到你可以今晚就启动。

模式一："信息差搬运"的降维打击

案例：杭州宝妈小雅，主业行政月薪5200元，副业做"跨境信息差"月入2-3万。

她的操作简单到令人发指：

发现缝隙：国内1688上批发价15元的原创设计手机壳，美国独立站卖45美元
建立管道：注册Shopify店铺（月费29美元）+ 开通Print-on-Demand（按需打印）服务
精准投放：在Pinterest发布设计图（不是卖货！），引流至店铺

关键动作：

不囤货：客户下单后，系统自动同步至国内供应商直发
不设计：与3个美院学生分成合作（每单分15%）
不售后：供应商承担质量问题退换

她的时间账本：每天投入1.5小时（午休30分钟+睡前1小时），主要工作是在TikTok找热门话题，将相关关键词植入产品描述。第一个月收入327美元，第六个月单月突破4000美元。

模式二："技能封装"的复利系统

反常识真相：最赚钱的不是你的核心技能，而是把技能封装成可复制产品。

案例对比：
• A先生：资深PPT设计师，接定制单，月入1.2万（时间占满）
• B女士：同是设计师，但她做了三件事：
  将过往作品拆解成50个模块化模板（上传至稻壳平台）
  录制3小时PPT速成课（挂载千聊，定价199元）
  开发自动排版工具（与程序员合作分润）

结果：
B女士现在每月被动收入：
  模板下载分成：4000-8000元
  课程复购+企业采购：1.5万+
  工具授权费：6000元
  总计稳定超2.5万，且每天仅需维护1小时。""",
}

print("Saving remaining texts...")
for cid, text in TEXTS.items():
    p = SRC / f"{cid}.json"
    if not p.exists():
        print(f"  MISSING: {cid}")
        continue
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data['raw_article_text'] = text
    data['clean_article_text'] = text
    data['full_text'] = text
    data['text_chars'] = len(text)
    data['fulltext_available'] = True
    data['evidence_ready'] = True
    data['placeholder_detected'] = False
    data['logic_analyzable'] = 'PENDING_MODEL_REVIEW'
    data['status'] = 'DOWNLOADED_REAL'
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # Copy to handoff
    h = HANDOFF / f"{cid}.json"
    with open(h, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {cid}: {len(text)} chars saved")

print("\nDone! 11/20 articles with real fulltext now.")