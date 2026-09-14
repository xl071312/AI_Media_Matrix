# Guanyu Plain-Language Engine v0.3 — CANDIDATE

Date: 2026-09-13
Owner: ChatGPT
Status: CANDIDATE / continue validation with new HERMES corpus
Scope: sentence/block generation for Chinese cognition videos

## Why v0.2 was still insufficient

The previous rule `use ordinary words` was too weak. A script can use simple vocabulary and still sound like AI if the explanation order is academic: define concept -> classify -> summarize mechanism -> give example.

The better-performing spoken samples repeatedly reverse that order:

`concrete thing -> concrete action/result -> obvious contrast/question -> only then compress the lesson`

The viewer is allowed to understand the idea before hearing its name.

## Corpus observations used in this revision

High-confidence examples from current corpus:

- `7647446230122356665`: instead of saying `low-cost demand validation`, the speaker describes spending about 100 RMB on leaflets/sample fruit, asking people whether they would add WeChat, and deciding whether to continue from the response.
- `7666798588350065338`: instead of defining `information asymmetry`, the speaker says in plain terms that if you know something another person does not know, there may be money in the gap; then uses a five-RMB tutorial / 100 buyers / 500 RMB example.
- `7639944588144250138`: instead of starting with `perceived value`, it starts with the counterintuitive claim that a person's work problem may be being too efficient, then uses haircut/service situations to make the feeling concrete.
- `7682791681556548883`: instead of opening with `AI substitution boundary`, it first compares cheap mass-produced goods with increasingly expensive human services, then names cooking help, installers, caregivers and plumbing repairs.
- `7540234540556619058`: instead of `payment friction reduces spending salience`, the speaker contrasts handing out physical cash with a phone swipe and then immediately converts 35 RMB into everyday buying power.
- `7672991243072616697`: instead of `customer segmentation and unit economics`, the speaker reduces one-million-RMB revenue to three simple routes: fewer people paying more vs more people paying less.

These are working corpus observations, not universal platform laws.

## Core generation order

Default block order:

`Thing -> Action -> Result -> Question -> Difference -> One-line lesson`

Not:

`Concept -> Definition -> Framework -> Example -> Summary`

### Example

Reject:
`AI会优先替代标准化、重复执行、低判断密度的工作。`

Preferred generation process:
1. What does the person actually do?
2. Can I show the instruction they receive?
3. Can I show what AI would copy?
4. Can I ask one concrete question?
5. Only then state the lesson.

Possible spoken result:
`有一种活最危险：别人把一二三都告诉你，你照着做完。为什么？因为你能照着做，AI也能照着做。`

The example wording is a ChatGPT test sentence, not a corpus quote.

## 1. Verb-before-noun rule

Prefer actions people can picture:
- 租店
- 装修
- 进货
- 加微信
- 报价
- 跟单
- 返工
- 写代码
- 做表
- 改图
- 上门修
- 帮老人洗澡
- 花35块
- 赚500块

Delay abstract nouns:
- 验证
- 定位
- 价值
- 标准化
- 供需
- 交易摩擦
- 感知价值
- 能力结构

If an abstract noun can be replaced by a visible action without losing meaning, replace it.

## 2. Numbers must do work

A number is useful when the listener can mentally calculate with it.

Good jobs for numbers:
- compare two choices
- convert a vague cost into a daily-life cost
- show unit economics
- show how many people must buy
- show how small a test can be
- show before/after

Weak number use:
- stacking percentages for authority
- unsupported precision
- statistics with no decision implication

Preferred form:
`5块一个教程，100个人买，就是500块。`

The sentence structure matters: known amount -> simple multiplication -> obvious result.

## 3. Explain with a familiar object before a model

Before introducing a model, find a carrier from ordinary Chinese life:
- 工资
- 奶茶
- 火锅
- 理发
- 租店
- 小区
- 微信
- 老板
- 客户
- 返工
- 家电
- 护工
- 修水管
- 快递/外卖 where relevant

The carrier should reduce mental load, not create a second topic.

Hard rule: if explaining the example requires another explanation, the carrier is bad.

## 4. One sentence, one mental move

Avoid sentences that simultaneously contain cause, exception, classification and conclusion.

Reject:
`随着AI能力快速提升，标准化知识工作因可复制性增强而面临价值重估。`

Break it into moves:
`AI先抢哪种活？`
`就是那种步骤已经写得很清楚的活。`
`第一步干什么，第二步干什么，第三步交什么。`
`你只是照着做。`
`这种活，机器学得最快。`

Each line advances one thought.

## 5. Question = next step, not decoration

Corpus questions often push the reasoning one step forward:
- 为什么？
- 你想想。
- 哪条路更容易？
- 你会怎么办？
- 这35块到底是什么概念？
- 如果没人愿意加微信呢？

Avoid decorative questions whose answer is already obvious and adds no reasoning.

Question rule:
`current fact -> unresolved next fact`

## 6. Contrast must compare actions/results

Weak:
`低价值工作 vs 高价值工作`

Stronger:
`别人告诉你怎么做，你负责做完` vs `别人只告诉你结果，你得自己想办法`

Weak:
`普通人思维 vs 高手思维`

Stronger:
`先租店装修再等客户` vs `先花100块试试看有没有人要`

The contrast should be observable.

## 7. Compression comes after proof

Do not begin with the polished line if the listener has not earned it.

Preferred sequence:
`scene -> calculation/example -> listener can see the difference -> one short compression sentence`

Examples of compression-function language from corpus style:
- `说白了……`
- `你看……`
- `所以问题就在这儿……`
- `我就这么跟你说……`
- `你记住一句话……`

Use sparingly. The phrase itself is not the insight.

## 8. Concrete pronouns and roles

Prefer:
- 你
- 老板
- 客户
- 员工
- 买家
- 店主
- 上班的人
- 一个小公司

Avoid opening with:
- 市场主体
- 从业者
- 个体
- 组织
- 需求侧
- 供给侧

A role is good when a viewer can imagine the person immediately.

## 9. Allow spoken imperfection

Do not polish every sentence into written prose.

Natural spoken properties allowed:
- short repetition
- sentence fragments
- `你看`
- `为什么呢`
- `比如说`
- `我给你算一下`
- `你想想`
- `那就很简单了`
- restart/rephrase when useful

But do not mechanically insert fillers. Their function is pacing and reasoning.

## 10. The retell test

After each 20–40 second block, ask:

`一个普通观众听一遍后，能不能用自己的话复述这段？`

If not, locate the failure:
- too many abstract nouns
- too many unfamiliar entities
- more than one idea per sentence
- no visible action
- no number/object/scene
- conclusion arrives before evidence
- analogy itself requires explanation

Block FAIL if the central idea cannot be retold in one ordinary sentence.

## 11. The middle-school paraphrase gate

Before script approval, translate every key sentence into language a middle-school student could understand without specialist background.

This does NOT mean making the idea childish. It means removing unnecessary decoding cost.

If meaning materially degrades when simplified, retain the precise term but explain it immediately with a concrete scene.

## 12. AI-smell blacklist

Review or reject when several appear together:
- `本质上`
- `从某种意义上说`
- `结构性`
- `标准化`
- `价值重估`
- `能力边界`
- `底层逻辑`
- `认知框架`
- `供给侧/需求侧`
- `变量`
- `路径依赖`
- `范式`
- `权重下降/提升`

These terms are not forbidden. They are forbidden as the listener's first required representation of the idea.

## 13. Block template library

### B1 Calculation block
`一个具体目标 -> 两三个可算方案 -> 直接算 -> 问哪个更现实 -> conclusion`

### B2 Small-test block
`想干一件事 -> 普通做法先砸钱 -> 改成极小测试 -> 看真实反馈 -> 决定继续/停止`

### B3 Everyday-price block
`一个金额 -> 换成日常物品/天数 -> 重新感受金额 -> conclusion`

### B4 Role block
`假设你是老板/客户 -> 现在发生一件事 -> 你会怎么选 -> reveal incentive`

### B5 Before/after-action block
`A怎么做 -> 结果 -> B怎么做 -> 结果 -> difference`

### B6 Physical-world block
`AI看起来什么都能做 -> 选一个真实上门/照护动作 -> 展开现场变化 -> show why judgment/flexibility matters`

### B7 Personal-mistake block
`我原来怎么做 -> 吃了什么亏 -> 后来改一个动作 -> result -> lesson`

## 14. Required block carriers

Every important cognitive block must contain at least one:
- amount/number
- concrete action
- ordinary object
- familiar role
- real case
- simple comparison

Two consecutive important blocks with none of the above = LANGUAGE FAIL.

## 15. Drafting sequence for ChatGPT

For each cognitive node:
1. Write the exact insight privately.
2. Circle every abstract noun.
3. Find the real action behind each noun.
4. Find one China-native familiar carrier.
5. Build the example/calculation first.
6. Add the one-line lesson last.
7. Run retell test.
8. Run read-aloud test.

Do not expose the private abstract formulation in the final narration unless necessary.

## 16. Current confidence

HIGH:
- example/action before abstraction reduces decoding burden in this corpus.
- specific money/actions/roles are repeatedly used to carry reasoning.
- simple contrast and arithmetic are strong reusable explanation devices.

MEDIUM:
- exact frequency and placement of oral glue phrases.
- whether every topic benefits from numbers.
- ideal sentence length.

DEFER:
- frozen Guanyu Voice Profile.
- creator-specific catchphrases.
- platform-wide causal claims.

Next validation: apply these rules to the incoming 30-video plain-language corpus and attempt an external-topic script only after the corpus challenge.