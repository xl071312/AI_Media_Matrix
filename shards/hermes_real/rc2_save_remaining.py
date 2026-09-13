#!/usr/bin/env python3
"""RC2: Save all extracted texts and commit"""
import json
from pathlib import Path
import subprocess

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SRC = BASE / "analysis_batches/batch_004_toutiao/SEED_WAVE_001_REFETCH"
HANDOFF = BASE.parent / "handoff" / "chatgpt" / "batch_004" / "wave_001"

# Texts extracted from browser_console calls
TEXTS = {
    "7636648275394822719": """#有什么挣钱的方法介绍一下#

01. 当"搞钱"成为刚需，赚不到钱的你缺的是什么？

最近后台收到很多私信，大家普遍反映："头条的流量主收益降了""工作难找，工资不涨""想做个副业，但除了送外卖、跑网约车，不知道还能干什么"。

大家有没有发现一个现象？以前我们觉得赚钱是靠"出卖体力"，但现在，年轻人赚钱靠的是"信息差"和"情绪价值"。

2026年了，如果你还只想着靠死工资活着，那抵御风险的能力确实太弱了。这一两年，我观察到一个明显的趋势：那些不起眼的、甚至有点"奇葩"的冷门生意，正在让一批年轻人偷偷富起来。

02. 数据背后的真相：你的技能远比你以为的值钱

很多人觉得自己什么都不会，其实这是大错特错。

根据2025年底发布的一份《数字平台中的青年新职业趋势研究》报告显示，仅在"闲鱼"这一个平台上，就有高达1962万人在出售自己的技能服务。

这意味着什么？意味着"卖技能"已经成了一种巨大的风口。

以前我们做生意，得租个店面；现在做生意，一部手机就行。

数据显示，活跃在平台上的副业人群里，00后和95后占了绝大多数。而且这可不是小打小闹，超过41%的从业者，副业收入已经占到了他们总收入的30%以上。

也就是说，对于那些"搞钱野路子"的玩家来说，副业已经不是零花钱了，而是第二根经济支柱。

比如，你可能刷到过"陪诊师"这个职业。说白了就是陪着老人或者异地打工人去医院看病、跑腿。有人觉得这就是"高级保姆"，但你知道吗？因为老龄化加剧，陪诊师的订单量同比暴涨，有人靠周末接单，月入过万很轻松。

再比如"伴宠师"，也就是上门喂猫、遛狗。现在年轻人把宠物当孩子养，出差了不放心放宠物店，就找人上门。这活累吗？不累，就是需要点责任心。但你算算账，一单50-100元，一天跑几家，一个月下来是不是房租就出来了？

搞钱的核心逻辑变了：从"我有力气"变成了"我有耐心"和"我有时间"。

03. 情感经济爆发：靠"说话"也能年入几十万？

除了跑腿和技能，2026年最火的风口其实是——情绪价值。

现在的年轻人，物质丰富了，精神却孤独了。前几天我看到一个极端的案例，杭州一个00后女孩，月薪9000元，竟然愿意花5000元去雇一个"秒回师"。

听到这你可能震惊了，啥是"秒回师"？

其实很简单，就是有人付费给你，你得保证在指定时间段内，微信秒回他，听他吐槽，听他倾诉，当他的"树洞"。这行有时薪高达150元的，甚至有人靠兼职做"情感抚慰"月入过万。

这说明了什么？孤独是一门大生意。""",

    "7641201117593895464": """各位打拼的朋友们，大家好！

我们这代人，活得其实挺不容易。小时候赶上物质匮乏，长大后遇上房价高企、职场内卷，想踏踏实实攒点钱、过好日子，总感觉处处受限。一辈子勤勤恳恳上班，不敢偷懒、不敢任性，到头来发现，辛辛苦苦一年，存不下几个钱，想给家人更好的生活，想给自己留份保障，却总觉得力不从心。

很多人常说："选择大于努力"。这话听着简单，却藏着最实在的生活真相。我们身边总有这样的人：能力不比你强，学历不比你高，人脉也普通，却在某个关键节点抓住了时代机遇，日子越过越红火，实现了阶层跨越。而更多人，一辈子埋头苦干，跟着别人的脚步走，错过了一次又一次财富机会，最后只能感叹"生不逢时"。

其实，时代从来不会抛弃普通人，只是不会提前打招呼。过去几十年，我们经历了改革开放、房地产黄金期、互联网浪潮、移动互联网红利，每一次财富浪潮，都让一批普通人实现了逆袭。而今天，我要跟大家说一个关乎我们每个人未来15年的重磅消息：2026至2040年，新一轮财富风口全面开启，这是普通人最后一次低成本、公平参与、靠认知和执行力翻身改命的黄金窗口期！

这不是空谈，更不是画饼，而是基于国家最新规划、全球产业变革、人口结构变化等多重权威信息，实实在在的时代趋势。接下来，咱们就用大白话，把这15年的财富逻辑、核心风口、普通人可落地的机会，一次性讲透，全程真实靠谱、不夸大、不虚构，看完你就知道，接下来15年，该往哪走、该抓什么机会。

一、时代定调：2026-2040，国家战略护航的15年黄金周期

很多人疑惑：为什么偏偏是2026到2040年？这15年到底特殊在哪？

答案很简单：这15年，是国家发展的关键爬坡期，是产业变革的集中爆发期，更是普通人财富翻身的最后窗口期，每一步都有国家战略保驾护航，确定性极强。

2026年3月，十四届全国人大四次会议正式通过《第十五个五年规划纲要（2026-2030年）》，这份纲领性文件，直接衔接2035年远景目标、2040年现代化建设中期规划，清晰勾勒出未来15年的发展蓝图。国家发改委明确表态，2026-2040年将持续推进七大国家级战略：新质生产力、数字中国、乡村振兴、区域协调、双碳目标、民生保障、人才强国。

简单说：未来15年，国家钱往哪投、政策红利往哪倾斜、资源往哪集中，财富机会就在哪。这15年，和过去靠运气、靠人脉、靠本金的财富时代完全不同，它是普通人最友好的一次财富浪潮——不看学历、不看背景、不看本金，只看你能不能看懂趋势、愿不愿意踏实行动。""",
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

print("\nCommitting...")
subprocess.run(['git', 'add', '-A'], cwd=r'F:\workspace\AI_Media_Matrix')
subprocess.run(['git', 'commit', '-m', 'benchmark handoff: RC2 fix - Wave001 real fulltext extraction (6/20 done)'], cwd=r'F:\workspace\AI_Media_Matrix', capture_output=True)
subprocess.run(['git', 'push', 'origin', 'chatgpt-handoff'], cwd=r'F:\workspace\AI_Media_Matrix', capture_output=True)
print("Done!")