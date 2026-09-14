# Guanyu Hook Engine v0.2 — CANDIDATE

Date: 2026-09-13
Owner: ChatGPT
Status: CANDIDATE / supersedes v0.1 for testing
Scope: first 5–30 seconds

## Why v0.1 failed

v0.1 over-corrected toward `Audience Mirror`. It forced an ordinary-life setup before the topic, which produced a polished but vague structure:

`common scene -> analogy -> another analogy -> news reveal -> question`

The result was understandable only after several sentences and sounded generated.

The new principle is **Payload First**.

The first sentence should already contain something worth hearing: a result, loss, danger, self-location, contradiction, or strong reframe.

## Evidence from the current corpus

Observed openings include:
- `关于我用8000块，在半年内赚到130万...` — concrete outcome first.
- `你们知道对钱没有概念有多可怕吗` — personal threat first.
- `想赚100万，99%的人第一步就选错了` — goal + error first.
- `世界上所有的赚钱行为都可以用这一个公式去解决` — compressed promise first.
- `上班是为了早日赎身，而不是为了当头牌` — identity reframe first.
- `你的收入到底什么水平？每月5000放全国排第几？` — self-location first.

These are not one formula. Their common property is that the viewer knows the semantic payload immediately.

## New opening law

**First sentence = topic + personal consequence or unresolved tension.**

Do not warm up the viewer before saying the thing.

By the end of sentence 1, the viewer should be able to answer:
- `这条视频大概在说什么？`
- `为什么可能跟我有关？`

If either answer is unclear, Hook FAIL.

## Preferred cold-open families

### H1 Concrete Outcome
`投入/动作 -> 结果`
Example structure: `8000块，半年130万。`
Use when proof exists.

### H2 Concrete Threat / Loss
`你正在做的X -> 可能让你损失Y`
Use for spending, career, hidden cost, risk.

### H3 Goal + Hidden Error
`想要X的人，大多数第一步错在Y`
Use for earning, career, business decisions.

### H4 Self-Location
`你现在在哪一级 / 哪一类 / 哪个阶段？`
Use when a credible ladder or comparison exists.

### H5 Strong Reframe
`你以为A，真正决定结果的是B`
B must be specific and explainable, not a slogan.

### H6 Contradiction With Named Object
`最应该做A的人，反而在做B。`
The object and contradiction must be concrete in sentence 1.

### H7 Live Proof
Show the artifact/result first, then explain.

### H8 Identity + Immediate Utility
`如果你是X，现在最该知道的是Y。`
Must contain utility, not generic identity flattery.

## First 15-second rules

1. **One semantic field only.**
Do not jump `加班 -> 鸡娃 -> 价格战 -> AI` inside 15 seconds.

2. **No setup sentence.**
Avoid openings whose only job is to prepare another sentence.
Examples to reject unless immediately concrete:
- `很多人都遇到过...`
- `你有没有想过一个问题...`
- `今天有一条新闻...`
- `最近发生了一件很有意思的事...`
- `这里有一个很反常的地方...`

3. **No abstract noun before concrete object.**
Avoid `博弈、底层逻辑、集体行动困境、宏观趋势` before the viewer has a specific object/result/loss.

4. **No forced symmetry.**
AI-smell patterns include:
- three parallel examples from unrelated domains;
- `一边A，另一边B` repeated mechanically;
- `不是A，而是B` stacked several times;
- polished three-part lists before the topic is clear.

5. **No explanatory announcement.**
Avoid `今天我们就来聊聊...`, `接下来我给你解释...`, `这背后其实是一套...` in the hook.
The explanation should begin, not be announced.

6. **Use proper nouns only when they add payload.**
`Fiverr/Upwork` can appear after `普通人副业正在被AI先吃掉`.
Do not ask the viewer to care about an unfamiliar executive before the stake is clear.

## Hook density test

For the first 8 seconds, count only sentences that deliver one of:
- result
- loss
- identity/stage
- contradiction
- proof
- open loop

Setup-only sentences count as zero.

Target: every sentence in first 8 seconds has payload.

## AI-smell rejection test

Reject and rewrite if the opening contains two or more of:
- generic `很多人`
- generic `你有没有想过`
- meta phrase `今天/这期/接下来我们聊`
- 3-item analogy chain
- abstract term before a concrete noun
- polished rhetorical symmetry
- multiple `其实/所以/那问题来了` used as scaffolding
- viewer cannot name the topic after sentence 1

## Relationship to Topic Fit Gate

Hook Engine v0.2 runs only after `TOPIC_TO_AUDIENCE_FIT_GATE_V0_1` passes.

If natural relevance is weak, reject the topic instead of manufacturing a relatable intro.

## External validation rule

Do not draft the full 4–5 minute script until the first 15–30 seconds pass user review.

Failure diagnosis categories:
- TOPIC_FIT_FAIL
- FIRST_LINE_CLARITY_FAIL
- STAKE_FAIL
- SPECIFICITY_FAIL
- AI_SMELL_FAIL
- QUESTION_DEBT_FAIL
- BAIT_PAYOFF_MISMATCH

A failed hook updates the engine before another full script is written.
