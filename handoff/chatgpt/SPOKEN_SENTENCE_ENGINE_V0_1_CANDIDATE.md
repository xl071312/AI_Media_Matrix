# Guanyu Spoken Sentence Engine v0.1 — CANDIDATE

Date: 2026-09-13
Owner: ChatGPT
Status: CANDIDATE / corpus-grounded / requires user acceptance
Scope: Chinese spoken openings and sentence-level delivery for 4–5 minute cognition videos

## Why this exists

The previous external-news hook tests still sounded AI-written even when they satisfied relevance and hook structure. The failure was not only topic selection or logic. It was sentence-level language.

The current corpus shows that high-performing spoken openings are usually much simpler, rougher, more concrete and more immediate than the wording produced by the prior script rules.

This file is grounded in actual transcript lines from the benchmark corpus. It is not a free-form style invention.

## Observed opening patterns from the corpus

### 1. Concrete result first

B002-003 opens approximately:
- `关于我用8000块，在半年内，赚到了130万...`

What the sentence does:
- money appears immediately;
- the result is concrete;
- no background explanation before payoff;
- the viewer knows what the story is about in the first breath.

### 2. Direct personal danger first

B002-010 opens approximately:
- `你们知道对钱没有概念有多可怕吗`

What the sentence does:
- starts with `你们`;
- uses ordinary words: 钱 / 可怕;
- creates one simple question;
- no abstract noun is needed.

### 3. Self-location first

B002-012 starts by asking what level an ordinary person's monthly income is at, then immediately uses `5000块` and asks where it ranks nationally.

What the sentence does:
- viewer can immediately place self inside the topic;
- number comes before theory;
- the promise is concrete: `你在哪一级`.

### 4. Goal + mistake first

7672991243072616697 opens approximately:
- `想赚100万，99%的人第一步就选错了`

Then it immediately gives three arithmetic routes.

What the sentence does:
- desire appears first;
- error appears second;
- question debt is automatic: `错在哪？`
- no warm-up.

### 5. Identity + blunt reframe first

B002-007 opens by addressing entrepreneurs and says their biggest problem is not the obvious one.

B002-013 opens with the rough idea:
- `上班是为了早日赎身，而不是为了当头牌`

What these do:
- name the person's current identity/action;
- give a blunt judgment;
- use familiar verbs/nouns instead of analytical vocabulary.

### 6. Belief challenge + proof first

B002-009 opens approximately:
- `这年头还有人相信做自媒体可以月入过万...`

It then quickly moves to the creator's own experience/proof.

What it does:
- sounds like conversation, not a report;
- challenges a belief the viewer already has;
- proof follows before a long explanation.

### 7. Utility inventory first

7546212425998454074 opens approximately:
- `除了打工，至少还有16种赚钱的方法`

What it does:
- ordinary-person problem is named directly;
- concrete number signals utility;
- viewer knows exactly what they will get.

## Sentence-level properties that recur

These are observations, not universal platform laws.

### A. The first sentence carries the payload

The first sentence usually already contains at least one of:
- money;
- result;
- loss;
- job;
- mistake;
- number;
- identity;
- a blunt judgment.

Bad Guanyu pattern:
- `这里有一个很反常的地方...`
- `今天有一组新闻...`
- `真正值得看的其实是...`

Why bad: these sentences announce that an insight is coming but do not contain the insight.

### B. Ordinary nouns beat analytical nouns

Prefer corpus-like words:
- 钱
- 工资
- 上班
- 老板
- 亏
- 赚
- 买
- 卖
- 时间
- 100万
- 5000块
- 你自己

Avoid in the opening unless absolutely necessary:
- 机制
- 结构
- 变量
- 约束
- 系统性
- 认知框架
- 价值权重
- 标准化程度
- 竞争结构

Those concepts may be explained later, but first translate them into a situation a person can picture.

### C. One breath = one idea

Corpus openings often move in short chunks:
- `想赚100万`
- `99%的人第一步就选错了`
- `就三条路`
- `100个人，每人1万`
- `1000个人，每人1000`

Do not combine four functions into one polished sentence.

### D. Concrete question beats conceptual question

Prefer:
- `你猜哪条最容易？`
- `5000块放全国排第几？`
- `35块到底是什么概念？`
- `你会怎么办？`

Avoid:
- `这背后反映了怎样的结构性变化？`
- `为什么这一机制会形成自我强化？`

### E. Spoken roughness is allowed

The corpus is not polished essay prose. It contains:
- repetition;
- short fillers;
- self-correction;
- `你想想` / `为什么呢` / `我给你算一下` / `说白了` / `你看`;
- incomplete-feeling short clauses.

Guanyu should not intentionally insert verbal garbage, but it also should not polish every sentence into symmetrical written prose.

### F. Explanation usually follows an object, not an abstraction

Corpus pattern:
- object/result -> question -> example/calculation -> explanation.

Avoid:
- abstract definition -> framework -> example.

## Oral translation table

Before drafting, translate abstract wording into ordinary speech.

| Abstract draft wording | Spoken translation direction |
|---|---|
| 标准化任务 | `这活是不是照着步骤就能干` |
| 决策风险 | `他凭什么先给你钱` |
| 可交付结果 | `你到底能帮他做成什么` |
| 竞争结构 | `你停了，别人不停，最后谁先吃亏` |
| 价值权重下降 | `光会干这件事，可能越来越不值钱` |
| 认知升级 | `你听完以后能多看懂什么` |
| 系统复制 | `第一次你自己会做，第二次别人照着也能做` |
| 用户需求 | `人家到底为什么愿意掏钱` |

These translations are wording directions, not quotations from one creator.

## Opening hard gate — sentence level

Before a hook can pass, the first sentence must satisfy all of the following:

1. A Chinese viewer with no specialist knowledge understands the literal meaning immediately.
2. It contains a concrete object/action/result, not an announcement of analysis.
3. No unfamiliar company/person/platform name is required to understand it.
4. No abstract professional term is necessary.
5. It sounds plausible if said aloud by a normal person to a friend.
6. Removing the second sentence should not make the first sentence meaningless.

Automatic FAIL phrases at the start unless the specific topic requires them:
- `这里有一个很反常的地方`
- `真正值得关注的是`
- `从本质上看`
- `这背后其实是一套`
- `今天我们来聊聊`
- `随着AI的发展`
- `在当前的环境下`

## Drafting process correction

Old process:
`topic -> logic -> polished hook`

New candidate process:
`topic -> extract one concrete payload -> write 5 corpus-shaped first sentences -> reject abstract/polished ones -> choose one -> then attach logic`

The model must not write a full 30-second opening until the first sentence passes the user-level comprehension test.

## Validation rule

Do not declare this engine frozen yet.

Use the next external-topic test to validate only:
- first sentence;
- first 5 seconds;
- first 15 seconds.

If the user still says `AI味 / 看不懂 / 不像人说话`, return to the corpus again rather than polishing the generated sentence.