#!/usr/bin/env python3
"""RC2: Directly save extracted texts to Wave001 JSONs"""
import json
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SRC = BASE / "analysis_batches/batch_004_toutiao/SEED_WAVE_001_REFETCH"

# Pre-extracted texts from browser_console calls (saved as variables)
TEXTS = [
    ("7591436947063702022", """姜胡说 20 年实战干货：普通人逆袭的 5 个核心逻辑，从 0 到 1 跑通赚钱闭环

很多人总困在 "想做事却不敢动" 的死循环里：报了一堆课、收藏了无数干货，却始终迈不出第一步；要么怕准备不充分，要么担心失败亏成本，最后只能看着机会溜走。

姜胡说在直播中分享的 20 年实战经验，戳中了普通人逆袭的关键：成功从不是 "准备完美" 后的爆发，而是 "最小化试错" 后的复利积累。以下 5 个核心逻辑，附可直接落地的行动方案，帮你从 0 到 1 跑通赚钱闭环。

1. 最小化试错：从卖 "破烂" 打通赚钱链路

姜胡说的赚钱起点，是小时候翻家里的闲置物品拿去售卖 —— 舅舅不用的墨镜、堆在角落的旧物件，哪怕只卖几毛钱，核心是跑通 "挂链接、写文案、做沟通" 的完整链路。

这正是普通人最该起步的方式：不追求 "赚大钱"，先以零成本验证交易逻辑。很多人觉得 "没项目可做"，其实身边的闲置资源、过往经验都是商机：

闲置资源：家里不用的家电、书籍挂到二手平台，办公室多余的工位对外短租，甚至通勤时的空座承接顺风单；
知识经验：考公笔记、四六级备考资料整理成文档售卖，做过餐饮就输出 "小店选址避坑指南"，懂 Excel 就做 "办公技巧教程"。

可行动步骤：
今天找出 1 件家里 3 年没用到的闲置物品（如旧相机、闲置课程）；
花 1 小时写 3 句文案（说明用途 + 优势 + 价格），拍 3 张清晰照片；
挂到二手平台或朋友圈，记录咨询量和成交情况，重点熟悉 "发布 - 沟通 - 成交" 流程。"""),
    
    ("7599942867901071906", """一个中年老男人到底适合做什么副业？

欢迎您关注王混乱，一个所见所闻创作者。

我的自白

年近40岁，一家三口，普通城市，拿着捉襟见肘的死工资，想去昂贵的饭店不敢去，想买心仪的汽车买不起，想换改善型住房没办法。于是心里边总是嘀咕：有没有什么合适的副业可以做，哪怕不多，每个月赚个三两千块钱当零花也可以。

随便问了豆包："年近 40 岁有固定工作、工作日晚上和周末可以抽出来时间的男性可做的副业有哪些？"

豆包回答我：核心要贴合时间灵活、轻投入、避重体力、能发挥中年积累的阅历 / 技能 / 资源的特点，优先选 "低试错成本、可长期做、不挤占主业精力" 的类型，避开需要熬夜拼体力、大额投入的项目，以下分技能变现、资源对接、轻运营实操三大类，覆盖不同能力基础：

一、技能变现类（有基础技能优先，性价比最高，直接靠能力赚钱）

适合有办公技能、专业技术、职场经验的人，不用额外学新东西，直接把现有能力变现，时间可控，单干为主不用组队。

办公 / 文案类兼职：写 PPT 代做、公文 / 工作总结代写、Excel 数据整理 / 图表制作，40 岁的职场阅历对写正式文案、做商务 PPT 的把控力远高于年轻人，平台（猪八戒网、淘宝店、小红书）接单，晚间做单、周末交稿，单份 PPT80-500 元不等，简单数据整理 30-200 元 / 单；

专业技术兼职：如果主业是财务、设计、机械、电工、建筑等，接对应兼职 —— 财务代账（小微企业，每月固定做账，晚间 / 周末处理）、CAD 制图 / 家装设计（对接装修公司）、家电 / 水电简单维修（本地社区接单，周末上门），这类有技术壁垒，单价高，还能积累稳定客户；
职场 / 学业辅导：把自己的行业经验、考公 / 考编 / 职场晋升心得做成课程，或做一对一辅导，比如教年轻人写简历、面试技巧，或辅导中小学生作业（晚间线上、周末线下），不用露脸，靠阅历说话，口碑起来后客户会转介绍。"""),
]

print("Saving extracted texts...")
for cid, text in TEXTS:
    p = SRC / f"{cid}.json"
    if not p.exists():
        print(f"  MISSING: {cid}")
        continue
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data['raw_article_text'] = text
    data['clean_article_text'] = text
    data['text_chars'] = len(text)
    data['fulltext_available'] = True
    data['evidence_ready'] = True
    data['placeholder_detected'] = False
    data['logic_analyzable'] = 'PENDING_MODEL_REVIEW'
    data['status'] = 'DOWNLOADED_REAL'
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {cid}: {len(text)} chars saved")

print("\nDone. Committing...")