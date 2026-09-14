# Abstract-to-Spoken Transform Matrix v0.1

Date: 2026-09-13
Owner: ChatGPT
Status: CANDIDATE
Purpose: prevent correct logic from turning into academic/AI-sounding narration.

This matrix is derived from repeated sentence mechanics in the current Douyin spoken corpus. The right column is not copied creator text; it is a Guanyu generation pattern built from corpus behavior.

| Abstract formulation | Spoken transformation | Why it lowers decoding cost |
|---|---|---|
| 需求验证 | `先别租店。先拿一点东西去问十个人，有人愿意买吗？` | turns a business term into an action anyone can picture |
| 低成本试错 | `先花小钱试一下。没人理你，就别继续砸钱。` | gives stop rule instead of label |
| 信息差 | `你会的东西，别人不会；他又正好需要，这中间就可能有钱。` | replaces category with buyer/seller relation |
| 单位经济 | `一个人赚100，得找一万人；一个人赚1万，只要100个人。` | arithmetic carries the model |
| 感知价值 | `15分钟给你剪完，你可能还觉得他不认真；聊半天、改两次，你反而觉得这钱花得值。` | everyday service scene shows the mechanism |
| 支付无感 | `现金一张张掏，你会心疼；手机一扫，35块一下就没了。` | bodily action before concept |
| AI替代风险 | `别人把步骤都写好了，你只管照着做，这种活机器最容易学。` | converts job taxonomy into visible workflow |
| 非标准化工作 | `每家情况都不一样，到了现场你得自己判断。` | describes variability without jargon |
| 物理世界复杂性 | `同样是修水管，两家漏的位置都不一样。你不上门看，根本不知道该怎么修。` | real object and different houses carry complexity |
| 决策权与付款人分离 | `觉得麻烦的人，不一定是掏钱的人。你得找到那个真能批钱的人。` | replaces organization theory with two roles |
| 信任成本 | `你说你很厉害没用。先做一小单，让他看到结果。` | action and transaction instead of abstraction |
| 可重复交付 | `第一次靠你自己硬扛，第二次还得从头来，这就不叫生意。能留下清单、模板、流程，下一次还能照着做，才开始像系统。` | shows repeatability through next occurrence |
| 供需不平衡 | `要的人越来越多，愿意干的人越来越少，价格能不涨吗？` | two crowds + one question replaces economics label |
| 职业价值重构 | `以前老板给钱买你的手，现在越来越要买你的脑子。` | compact familiar contrast; use only after evidence |
| 高判断密度 | `没人告诉你下一步怎么办，你得自己拿主意。` | turns abstract capability into situation |
| 标准化任务 | `第一步、第二步、第三步都写得清清楚楚。` | procedural picture |
| 规模化 | `一个人能做10单，十个人能不能做100单，而且质量别掉？` | capacity question instead of noun |
| 流量变现 | `有人看还不算钱。得有人愿意买，钱才真的进来。` | separates attention from transaction in ordinary terms |
| 机会成本 | `你把三个月都压在这件事上，就等于另外三件事都没机会试。` | uses lost alternatives instead of term |
| 风险集中 | `你所有收入都靠一个老板，他一裁员，你这边直接归零。` | one-basket outcome made personal |
| 分散收入来源 | `别只收一份工资。能不能有第二个、第三个给你钱的人？` | buyer count instead of finance language |

## Sentence conversion procedure

When a draft contains an abstract sentence:

1. Ask `谁在干什么？`
2. Ask `具体要花多少钱/多少时间/做几步？`
3. Ask `普通人在哪见过这件事？`
4. Ask `能不能把判断变成一个选择题？`
5. Ask `能不能先让观众自己得出结论，再说那句话？`

If none can be answered, the sentence is probably too abstract for spoken narration.

## Three anti-patterns

### A. Label substitution
Bad:
`这就是典型的交易摩擦。`

Still bad:
`说白了，这就是交易摩擦。`

Adding `说白了` does not make an abstract label plain language.

Better:
`你有本事是一回事，他敢不敢先给你钱，是另一回事。`

### B. Multi-concept sentence
Bad:
`AI正在通过标准化复制和边际成本下降重塑知识工作的价值分配。`

Better sequence:
`AI为什么先抢一部分白领的活？`
`因为有些活，步骤已经写得太清楚了。`
`你照着做，它也能照着做。`
`而且它做第二遍，几乎不用再学一次。`

### C. Fake ordinary language
Bad:
`你想一下，标准化任务的边际价值是不是正在下降？`

The words remain academic despite `你想一下`.

Better:
`你想一下，如果这件事每次都是同样三步，老板为什么一定要再找一个人做？`

## Corpus-derived rhythm notes

Observed spoken pieces often use:
- claim
- one immediate question
- one tiny example
- short calculation or consequence
- another question
- conclusion

They do not necessarily build grammatically perfect paragraphs. They build a chain the listener can follow in real time.

## Guanyu use rule

The logic layer may stay sophisticated. The narration layer should hide that sophistication inside simple objects, actions, amounts and choices.

Target experience:
`听的时候觉得很简单 -> 听完发现自己多懂了一层`.

Not:
`听的时候觉得很深 -> 听完记不住他说了什么`.