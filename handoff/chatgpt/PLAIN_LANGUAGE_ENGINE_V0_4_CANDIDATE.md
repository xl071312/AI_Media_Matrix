# Guanyu Plain-Language Engine v0.4 — CANDIDATE

Date: 2026-09-14
Owner: ChatGPT
Status: CANDIDATE / not frozen
Basis: verified historical spoken corpus + individually audited usable RC6E material. RC6E as a 30-new-sample corpus is currently under repair and is not treated as complete evidence.

## Core correction

The main problem in failed live drafts was not merely 'too many professional words'. It was **explanation order**.

AI-like default often does this:

`abstract conclusion -> framework term -> multiple examples -> summary`

Observed strong spoken explainers more often do this:

`one concrete thing -> one obvious change -> simple question -> next concrete change -> viewer notices pattern -> only then name the idea`

For Guanyu, the default must be:

**先让人看见，再让人想明白，最后才告诉他这个道理叫什么。**

## Rule 1 — No abstraction from abstraction

A new abstract idea cannot be explained primarily with another abstract idea.

Bad:
`标准化任务价值下降，因为AI提高了自动化替代率。`

Required bridge types before abstraction:
- a visible action;
- a familiar object;
- a small money calculation;
- a role sequence;
- a before/after contrast;
- a concrete everyday decision.

Only after the audience can picture the situation may the script compress it into a concept.

## Rule 2 — Action before noun

Prefer verbs before labels.

Bad:
`先做低成本需求验证。`

Better structure:
`先别租店。拿点样品去问十个人。有人愿意买吗？没人理你，就先别往里砸钱。`

Only later, if useful:
`这其实就是先验证需求。`

The term is a label attached after comprehension, not the vehicle of comprehension.

## Rule 3 — One sentence, one mental move

A spoken sentence should normally do only one of:
- state one fact;
- make one comparison;
- ask one question;
- show one consequence;
- give one action;
- name one conclusion.

If a sentence contains two or more new abstract nouns, split or rewrite.

Typical AI failure:
`随着AI提升，标准化执行能力的权重下降，而需求理解、系统设计和复杂判断能力的重要性持续上升。`

Human-order rewrite pattern:
`以前老板把步骤告诉你，你照着做，也能把活干完。现在这部分AI也会了。那老板还为什么要多花钱请你？`

The audience should never have to hold four new ideas in working memory before the sentence ends.

## Rule 4 — Use mentally computable numbers

Numbers should help the viewer reason, not decorate authority.

Strong shapes:
- `100个人 × 1万`
- `1000个人 × 1000`
- `10个人问一遍，5个人愿意加微信`
- `5块 × 100个人 = 500块`
- familiar prices placed side by side

Weak shape:
- several large statistics with no calculation or decision attached.

After a number, ask or state what the viewer can immediately infer from it.

## Rule 5 — Keep one cognitive carrier stable

Within one 30–60 second reasoning block, default to one familiar carrier.

Good carriers:
- one bottle of water;
- one shop;
- one boss assigning one job;
- one customer;
- one monthly salary;
- one household bill;
- one target amount of money.

Change one variable at a time.

Do not jump programmer -> parent -> small business -> overseas company just to prove the same point. Each jump creates a new comprehension cost and makes the prose feel synthetic.

A 4–5 minute video may change carriers at section boundaries, but each change must earn a new reasoning function.

## Rule 6 — Question debt must sound like a real person's next question

Avoid essay questions such as:
`这背后反映了怎样的结构性变化？`

Prefer the question a viewer would actually ask:
- `那为什么还有人能卖这么贵？`
- `没人买怎么办？`
- `那老板为什么还要请你？`
- `这钱到底是谁在付？`
- `哪条路更容易？`
- `那我怎么办？`

Each answer should naturally create the next simple question. Do not announce a four-layer framework upfront.

## Rule 7 — Evidence grammar: thing first, conclusion second

Default factual paragraph order:

`具体场景/数字 -> 发生了什么 -> 你能看出什么 -> 一句结论`

Not:

`结论 -> 专业框架 -> 数据堆 -> 再重复结论`

The evidence must let the viewer partly discover the conclusion before the narrator names it.

## Rule 8 — Vocabulary ceiling

First 30–60 seconds should use vocabulary common in ordinary Chinese conversation whenever possible.

Preferred noun families:
`钱、工资、老板、同事、客户、店、货、时间、订单、房租、成本、买、卖、亏、赚、做完、返工、没人买、有人问`

High-friction words are delayed unless unavoidable:
`标准化、结构性、权重、协同、范式、机制、非结构化、认知框架、边际、供需错配、系统性风险`

If a word needs a parenthetical explanation to be understood, do not use it as the opening vehicle.

## Rule 9 — Human speech is allowed to be imperfect

Do not optimize every sentence into polished written symmetry.

Natural spoken texture may include:
- short fragments;
- a repeated word for emphasis;
- `你想想` / `为什么` / `你看` / `说白了` / `比如` / `我给你算一下` when they actually move the reasoning;
- a quick self-correction;
- one-line questions and answers.

But do not manufacture fillers mechanically. Oral glue must have a reasoning job.

## Rule 10 — Repeatability test

After hearing a sentence once, an ordinary viewer should be able to repeat its meaning in roughly the same words.

If not, the sentence fails even when technically correct.

Use this QA prompt internally:
`一个没有行业背景的人听完这一句，能不能马上告诉别人我刚才说了什么？`

If no, simplify the sentence or move the concept later.

## Rule 11 — Concrete anchor density

During explanation, do not allow more than roughly two consecutive abstract sentences without returning to a concrete carrier, action, number, or scene.

This is a production heuristic, not a platform law.

## Rule 12 — Simple is not enough

Plain language cannot become low-quality certainty.

Do not copy from high-performing samples:
- unsupported percentages;
- conspiracy framing presented as fact;
- guaranteed-income claims;
- fake anecdotes;
- universal claims without constraints.

Learn the **language mechanics**, not their factual weaknesses.

Guanyu must keep its evidence and constraint standards while lowering comprehension cost.

## First-30-second sentence test

Before a script advances, the first 30 seconds should pass all:

1. First sentence says something concrete, not a warm-up.
2. Viewer knows what the video is about within one or two sentences.
3. At least one ordinary-person stake is visible: money, work, time, risk, choice, status, household life.
4. No string of unfamiliar proper nouns.
5. No professional concept is required to understand the basic conflict.
6. At least one question remains that sounds natural in everyday speech.
7. A viewer can retell the opening without translating it into simpler Chinese first.

## Paragraph build template

For most cognition blocks, prefer:

`一句人话判断`
→ `一个具体场景/动作`
→ `一个数字或对比（if useful）`
→ `问一句“为什么/那怎么办”`
→ `再推进一步`
→ `最后一句把道理收住`

Do not mechanically force every block into the exact same rhythm; this is a default anti-AI scaffold.

## Example: AI and work — explanation order only

Do not start:
`AI正在降低标准化执行工作的价值。`

Start from something the viewer can picture:

`老板把第一步、第二步、第三步都写好了，你照着做就行。`
`以前这种活也得找个人。`
`现在很多步骤AI也能照着做。`
`那问题就来了：如果你最值钱的地方只是“照着做”，老板为什么一定要多花钱请你？`

Only after the viewer understands the scene may the script name the distinction between execution and judgment.

This example is a transformation demonstration, not a factual claim that all such jobs will be replaced.

## Status

v0.4 is a stronger candidate than v0.1–v0.3 for script-generation tests, but **not frozen**.

Next validation:
1. repair RC6E corpus integrity;
2. analyze repaired new samples for counterexamples;
3. test on an unseen China-native topic;
4. user judges only whether they naturally want to keep listening and can understand each step;
5. failure returns to dismantling, not cosmetic rewriting.
