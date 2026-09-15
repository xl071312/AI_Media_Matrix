# Guanyu Plain-Language Engine v0.6 — CANDIDATE

Date: 2026-09-14
Owner: ChatGPT
Status: CANDIDATE / not frozen
Basis: prior verified spoken corpus + RC6F semantic review. RC6G produced no new semantic evidence because its source route was exhausted.

## Why v0.6 exists

v0.5 correctly moved Guanyu away from `abstract conclusion -> explanation` toward `concrete carrier -> contrast -> question -> conclusion`.

RC6F adds an important correction: **plain language is not the absence of abstract words. It is the absence of unnecessary translation work for the viewer.**

Some words are abstract but already lived and instantly understood: `工资、汇报、消费、加班、老板、客户、辞职、房租`. These can appear early.

Other words require decoding before the audience can even enter the argument: `结构性、边际、范式、非结构化、协同、标准化执行能力、价值权重`. These should normally appear only after the scene is understood.

The better rule is therefore:

**先用观众脑子里已经有画面的词，再用他能看见的动作把关系讲明白，最后才给陌生概念贴标签。**

## Upgrade 1 — Familiar abstraction may lead; unfamiliar abstraction may not

Do not ban all concepts from the opening.

Allowed early if ordinary audience already has a concrete mental image:
- 工资
- 上班
- 汇报
- 消费
- 存钱
- 加班
- 副业
- 老板
- 客户
- 辞职

Delay terms that require a definition before the conflict is visible.

The test is not “is this word abstract?”

The test is:
`普通人听到这个词，脑子里会不会马上出现一个具体场景？`

If yes, it may lead. If no, earn it later.

## Upgrade 2 — Double conversion: number -> lived consequence

A number alone is not yet plain language.

Good explanation often converts twice:

`模糊描述 -> 可比较的数字 -> 普通人能感到的后果`

Example shape:
- not `性能明显提高`;
- first `从2秒变成0.1秒`;
- then explain what that change means for a real user/action.

Likewise, a price becomes easier to judge when converted into something familiar:
`48元咖啡 -> 两斤排骨`

This is stronger than merely stating `48元很贵` because the viewer performs the judgment himself.

## Upgrade 3 — Equivalence Converter is a first-class device

When explaining money, time, effort, or probability, ask whether the abstract amount can be converted into a familiar equivalent.

Useful forms:
- `X块钱 = 另一种常见消费`
- `X小时 = 多少次日常动作`
- `X人 × Y元 = 一个目标金额`
- `一个月存X = 一年是多少 = 能顶多久生活费`

The point is not decoration. It gives the audience a ruler already available in memory.

## Upgrade 4 — One stable micro-world can carry a difficult mechanism

For genuinely difficult topics, a single persistent story-world is often better than several disconnected examples.

Pattern:
1. choose one familiar world;
2. introduce one actor and one goal;
3. change one variable;
4. show what the actor does;
5. show the next consequence;
6. only after the chain is visible, name the mechanism.

This is especially useful for economics, AI/job mechanisms, pricing, debt, incentives, platform rules, and business systems.

Do not jump between programmer -> parent -> shop owner -> foreign company if one micro-world can demonstrate the whole causal chain.

## Upgrade 5 — Human explanation often uses contrast pairs, not definitions

Instead of defining a concept formally, contrast two familiar cases.

Examples of shapes:
- `直接领导更关心进度和风险；更高层更关心结果和收益。`
- `说“买了很多水果”没感觉；说“10斤，一个人吃10天”马上有感觉。`
- `今天20块买一个，明天20块买两个，人可能先不买而是等。`

A contrast pair reduces explanation length and lets the viewer infer the distinction.

## Upgrade 6 — Ask from inside the scene

Questions should sound as if the viewer is standing inside the example.

Better:
- `那老板为什么还要请你？`
- `他最关心什么？`
- `没人买怎么办？`
- `如果明天更便宜，你今天还买吗？`

Worse:
- `这背后反映了怎样的价值迁移？`
- `其核心结构性原因是什么？`

The first type creates real Question Debt. The second type sounds like an essay prompt.

## Upgrade 7 — Dialogue simulation is an allowed carrier

RC6F shows that some complex workplace mechanisms are easier to understand when enacted as a tiny exchange rather than narrated as theory.

For Guanyu, this does **not** mean producing comedy skits. It means a narrator may briefly simulate two sides:

`老板：这活你按步骤做。`
`员工：那如果步骤AI也会呢？`

or

`客户：我为什么要多花这笔钱？`
`你：因为我能把这个结果交出来。`

Use only when the dialogue compresses a real mechanism. Do not manufacture theatrical dialogue for decoration.

## Upgrade 8 — A human voice is allowed to take a position

AI-like scripts often sound artificially balanced:
`一方面...另一方面...因此需要辩证看待...`

Strong spoken content often gives the viewer a clear provisional judgment first, then adds constraints.

Guanyu may say:
- `这事先别急着干。`
- `这钱我觉得不该先花。`
- `如果你只会照着做，这部分确实危险。`

Then immediately explain **why** and **where the boundary is**.

Do not confuse a clear stance with unsupported certainty.

## Upgrade 9 — Spoken paragraphs should climb, not summarize repeatedly

Bad AI rhythm:
`观点 -> 解释 -> 总结 -> 下一观点 -> 解释 -> 总结`

Preferred rhythm:
`具体事实 -> 问题 -> 推进一步 -> 新后果 -> 再问 -> 最后收一句`

Do not conclude every 10 seconds. Too many mini-summaries create synthetic cadence.

A 45–60 second reasoning block may need only one real compression sentence at the end.

## Upgrade 10 — Plain language must still contain a cognitive payload

RC6F negative samples show an important counterexample: short sentences, direct address, lucky-person rhetoric, emotional promises, or colloquial wording can still be cognitively empty.

Therefore plain-language quality requires both:

`低理解成本 × 真正的信息/判断增量`

A script fails if it is easy to understand but says almost nothing testable, useful, or transferable.

## Upgrade 11 — Concrete does not mean “many examples”

AI often overcompensates for abstraction by adding four examples.

That increases cognitive switching cost.

Default for a reasoning block:
- one primary carrier;
- one contrast;
- one consequence;
- optional second carrier only if it performs a genuinely different proof function.

## Upgrade 12 — Friend-at-dinner test

In addition to the retell test, apply:

`这句话如果我坐在饭桌上跟一个不懂行业的朋友说，会不会自然这么说？`

Warning signs:
- perfect parallelism for three sentences in a row;
- several abstract nouns in one sentence;
- transition words that exist only to make prose polished;
- “我们需要从三个维度理解” before the viewer knows why he cares;
- repeated `本质上 / 核心是 / 归根结底` without new evidence;
- a question whose answer is already obvious from the wording.

## Default 60-second explanation architecture

Use as a scaffold, not a rigid template:

`一句直接判断`
→ `一个熟悉场景`
→ `一个对比或数字`
→ `观众自然会问的问题`
→ `把后果往前推一步`
→ `必要时再换算一次`
→ `最后一句才压成一个道理`

## 4–5 minute integration rule

Plain Language Engine does not replace Logic Architecture.

Recommended composition:

`Hook / ordinary-person stake`
→ `one stable carrier introduces conflict`
→ `Logic Engine explains why`
→ `evidence / number / contrast`
→ `constraint or counterexample`
→ `decision rule`
→ `memory model`

The language layer's job is to keep every reasoning step understandable on first hearing.

## What v0.6 explicitly rejects

- opening with unfamiliar institutions or foreign platform names when they are not already known to the Chinese target audience;
- defining an abstract term with another abstract term;
- jumping across unrelated examples to prove one point;
- using technical vocabulary as proof of sophistication;
- converting every paragraph into perfectly balanced written prose;
- colloquial filler with no reasoning job;
- easy-to-understand but cognitively empty motivational claims.

## Next falsification

v0.6 is still not frozen.

Next required test:
1. RC6H must produce genuinely new live-discovered spoken samples;
2. ChatGPT semantically reviews those samples without changing their wording;
3. counterexamples are used to attack v0.6;
4. only then run an unseen China-native current-topic script test;
5. user judges whether the opening is immediately clear, whether the body sounds like a real person explaining, and whether the content gives a new useful model.

If the live script still sounds AI-like, return to dismantling. Do not enter production just because the logic is technically correct.
