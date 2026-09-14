# Topic-to-Audience Fit Gate v0.1

Date: 2026-09-13
Owner: ChatGPT
Status: CANDIDATE / required before Hook Engine

## Why this gate exists

External-news test #2 showed that a weak audience fit cannot be repaired reliably by adding an everyday analogy. The Anthropic slowdown story required a bridge from `AI safety / IPO / geopolitical competition` to `加班 / 鸡娃 / 价格战`. The bridge itself became the content, so the viewer had to decode the analogy before knowing what the video was about.

Therefore the pipeline must reject some news topics before hook writing.

New order:

`News Pool -> Topic-to-Audience Fit Gate -> Hook Engine -> Logic Engine -> Evidence -> Script`

## Core principle

A topic is not selected because it is important, intelligent, or globally significant.

A topic is selected when the target viewer can understand **why it touches their money, work, risk, choices, status, time, or opportunity without a forced metaphor**.

## Mandatory gate

A news topic may proceed only if all five conditions pass.

### G1 Direct stake
Within one plain sentence, we can name what the viewer may gain, lose, misunderstand, or need to decide.

Examples:
- `普通人最容易接到的那批副业，正在先被AI自动化。`
- `月薪5000的人，在全国到底处在什么位置？`
- `你以为订单多就是生意好，但有些老板订单越多越缺现金。`

FAIL example:
- `Anthropic提出减速，这其实像你不敢第一个下班。`
The viewer must first accept an analogy before relevance exists.

### G2 Natural audience link
The topic must connect to the target audience directly or through one obvious bridge only.

PASS domains for Guanyu include:
- income / earning
- jobs / career survival
- side hustles / freelancing
- business survival / margins / cashflow
- consumer traps / household economics
- AI changing work or monetization
- decisions ordinary people or small business owners actually face

If two or more analogies are required to make the topic feel relevant, reject.

### G3 First-line payload
Before background, the topic must support at least one of:
- a concrete result
- a concrete loss
- a self-location question
- a strong but supportable reframe
- a visible demonstration
- a specific choice/error

If the first useful sentence must begin with a company name + executive + meeting + policy context, the topic is usually too far from the audience for Guanyu.

### G4 Evidence availability
There must be enough source evidence to support the hook and the core mechanism without inventing a composite story.

Minimum for current-news content:
- at least one high-authority current source for the event;
- enough detail to distinguish FACT from INFERENCE;
- no unsupported number used only for shock.

### G5 Cognitive yield
After the news facts are removed, the viewer should still leave with a reusable model, distinction, or decision rule.

Examples:
- task decomposition can make freelance work easier to automate;
- revenue growth and cashflow health can move in opposite directions;
- a skill label is not the same as a purchasable result.

If the episode collapses into `今天发生了什么`, reject.

## Scoring

Score each 0–2:
- direct stake
- natural audience link
- first-line payload
- evidence strength
- cognitive yield

Proceed target: >=8/10.
Mandatory: direct stake >=1, natural audience link =2, evidence strength >=1.

## Anti-force rule

Do not rescue a weak topic by stacking familiar-life analogies.

Bad rescue pattern:
`AI company -> office overtime -> parenting -> price war -> back to AI`

This creates semantic switching and AI-written symmetry.

Prefer either:
1. choose a news item already inside the audience's economic life; or
2. state the universal mechanism directly in one concrete sentence and use the news immediately as proof.

## Current decision

The Anthropic slowdown / IPO story is **REJECTED as the primary Guanyu pilot-news topic for this round**. It may be useful later as supporting evidence inside a broader competition-mechanism episode, but it should not be forced into an ordinary-person hook.
