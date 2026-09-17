# Guanyu Writing Engine V1

Date: 2026-09-16
Owner: ChatGPT
Status: V1 / usable for production testing; Voice Profile still not frozen

## 0. Evidence boundary

This version combines three evidence layers:

1. **RC6I PRIMARY 28** — usable for title/opening/market-response study only. The recovery pack contains no full transcripts; these samples must not be used to infer mid-video logic, ending structure, or phrase-level voice.
2. **Batch 001 / Batch 002 full timed transcripts** — usable for long-form logic architecture and explanation-order study. ASR is often noisy, so structure is more reliable than exact wording.
3. **Plain-Language Engine v0.5 evidence** — usable for concrete-to-abstract explanation rules and negative controls.

Hard rule: **do not promote a rule from one evidence layer beyond what that layer can support.**

---

# 1. Core production thesis

Guanyu should not be written as `hook + 3 points + conclusion`.

The working formula is:

`familiar high-stakes entry -> unresolved question -> one reasoning spine -> concrete proof -> constraint -> decision rule -> memory model -> loopback`

The job of the opening is not to be clever. The job is to make the viewer immediately know:

- this is about me / my money / my work / my risk / my decision;
- something I currently believe may be incomplete;
- there is a concrete question worth staying for.

The job of the middle is not to keep throwing conclusions. It must progressively reduce uncertainty.

The job of the ending is not encouragement. It must leave a rule, model, or distinction the viewer can reuse.

---

# 2. Opening Engine V1

## 2.1 Four preferred entry families

### O1 — Self-location

Use when the topic naturally contains a ladder, threshold, rank, or coordinate.

Forms:
- `你现在的收入，大概在哪一档？`
- `30岁之前存到多少钱，才算真的有安全垫？`
- `月薪5000，到底处在什么位置？`

Why it works structurally:
- viewer can immediately insert themselves;
- creates a prediction gap;
- often supports data ladder later.

Best paired with: `X2 Self-location + E3 Data Ladder + L2 Reframe`.

RC6I evidence includes multiple high-response samples built around income level, savings, and “你在哪一级”的 framing. Treat this as association, not a platform law.

### O2 — Contradiction against a familiar belief

Forms:
- `你工作上最大的问题，可能就是效率太高。`
- `很多人不是赚得少才存不下钱，而是根本没搞清钱去哪了。`
- `真正让能力变现困难的，通常不是能力不够。`

Why it works:
- uses familiar language;
- creates immediate Question Debt;
- naturally hands off to mechanism.

Best paired with: `X1 Contradiction -> L1 Mechanism or L2 Reframe`.

Batch 002 sample `B002-025` opens with “你工作的最大问题就是效率太高了” and immediately follows with a contrary explanation; this is strong structural evidence for the pattern.

### O3 — Concrete outcome before explanation

Forms:
- `一个职高生，靠兼职先把8000块的电脑挣出来了。`
- `我接手前半年亏了6万，接手第一个月就转正。真正改变的不是销售额。`

Why it works:
- outcome is already visible;
- viewer asks “怎么做到的？” before the creator asks them to;
- case can carry the reasoning instead of decorating it.

Best paired with: `X4 Real Case -> L6 Case-to-Principle`.

Batch 002 sample `B002-015` starts with a concrete identity + result + price anchor, then moves into the method. This supports outcome-first case openings.

### O4 — Familiar problem + cost

Forms:
- `很多人副业做不起来，不是没项目，是第一步就把成本压错地方了。`
- `你以为租店是创业第一步，其实租店可能是你最早犯的错。`

Why it works:
- viewer already owns the mental picture;
- stakes are explicit;
- creates a choice/constraint question.

Best paired with: `L5 Constraint Optimization`.

---

## 2.2 Openings to reject

Reject by default:

- `在这个快速变化的时代……`
- `很多人都知道……`
- `今天我们来聊一个非常重要的话题……`
- forced metaphor before the viewer knows the problem;
- abstract noun stacks: `认知差、结构化能力、商业闭环、价值杠杆` in the first sentence;
- generic pain before specific stake: `很多人活得很累，很迷茫……`.

Reason: these delay payload and force interpretation cost before the viewer has a concrete reason to care.

---

# 3. Question Debt V1

A hook is incomplete until it creates the next mental move.

Valid Question Debt must force one of these operations:

1. **Compare** — `为什么A反而比B差？`
2. **Locate** — `我属于哪一档？`
3. **Predict** — `如果继续这样，会发生什么？`
4. **Identify payer** — `这件事到底谁会付钱？`
5. **Explain mechanism** — `为什么会这样？`
6. **Choose under constraint** — `条件有限时，哪条路最可行？`

A rhetorical question that does not change the next reasoning step is decoration, not Question Debt.

---

# 4. Logic Engine V1

Keep Logic Architecture v0.3 six-engine taxonomy, but production usage is tightened:

## L1 Mechanism Derivation
`现象/判断 -> 为什么 -> 隐藏机制 -> 后果`

Use when the viewer needs causal understanding.

## L2 Cognitive Reframe
`常见理解A -> 实际B -> A为什么失效 -> 新判断`

Use when the main product is a changed mental model.

## L3 State Transition
`现在A -> 想到B -> 过渡成本/约束 -> 桥梁 -> 为什么能持续`

Use for ability monetization, career change, income transitions.

## L4 System Loop
`行动 -> 反馈 -> 信息 -> 判断 -> 调整 -> 重复 -> 放大`

Use when compounding and iteration are central.

## L5 Constraint Optimization
`目标 -> 可选路径 -> 现实约束 -> 排除 -> 可行路径 -> 小测试`

Use for side business, startup, channel, money decisions.

## L6 Case-to-Principle
`真实案例 -> 发生了什么 -> 机制 -> 原则 -> 迁移`

Use when a concrete case is the proof carrier.

### Production rule

One video chooses **one primary L-engine**. A second engine may support it. More than two usually means the script is mixing problems.

---

# 5. Cognitive Gain Engine V1

A 4–5 minute Guanyu script should normally produce 3–5 distinct gains.

A gain is valid only if the viewer can now do at least one thing they could not do before:

- distinguish two things they previously mixed together;
- explain a mechanism;
- predict a consequence;
- locate themselves;
- reject an unsuitable path;
- choose under uncertainty;
- reuse a decision rule.

Facts alone are not gains.

### Recommended sequence

`CG1: 纠正问题定义`
`CG2: 看见隐藏机制`
`CG3: 用案例/数字证明机制`
`CG4: 加入约束，避免过度泛化`
`CG5: 压成一个可复用判断规则`

---

# 6. Explanation Order V1

The strongest current rule from Plain-Language v0.5 remains:

**熟悉的词可以先说；陌生的概念要后命名。**

Preferred micro-sequence:

`熟悉入口 -> 稳定载体 -> 一个变化/对比 -> 普通人会问的问题 -> 数字/动作 -> 后果 -> 最后命名概念`

## 6.1 One stable carrier

Prefer one micro-world through a reasoning block:

- one boss + one employee;
- one shop + one customer;
- one household + one monthly bill;
- one product + one price;
- one ability + one payer.

Do not jump across four unrelated examples to prove one mechanism.

## 6.2 Equivalence Converter

Translate abstraction into familiar units:

`40%成本下降` -> `100块变60块` -> `省下的40块到底意味着什么`

The goal is comprehension, not decoration.

## 6.3 Contrast must change judgment

Good contrast:
- `100个人每人付1万` vs `1000个人每人付1000`
- `直接租店` vs `先花100块测试有没有人愿意加微信`
- `老板关心完成没完成` vs `更高层关心结果有没有价值`

Bad contrast:
- two examples that produce no new decision.

---

# 7. Spoken Expression V1 — structure, not catchphrases

Current evidence is enough to define **spoken construction**, but not enough to freeze a phrase-level Voice Profile.

## 7.1 Sentence construction

Prefer:
- short clauses;
- one new mental move per clause;
- direct subject + verb + consequence;
- natural repetition when it helps orientation;
- occasional self-correction or conversational pivot;
- concrete nouns before abstract labels.

Avoid:
- polished parallelism in every paragraph;
- three abstract causal sentences in a row;
- continuous “金句” mode;
- fake oral fillers inserted by template;
- forcing `你想一下 / 那问题来了 / 换句话说` at fixed frequency.

## 7.2 Spoken transition jobs

A transition should do a reasoning job:

- `为什么？` -> open mechanism
- `你注意这个区别` -> set comparison
- `再往后想一步` -> extend consequence
- `问题就在这儿` -> identify bottleneck
- `换句话说` -> compress, not repeat
- `那如果……` -> introduce constraint/counterexample

If deleting a transition changes nothing, delete it.

---

# 8. Attention Reset V1

Do not try to “reset attention” with random suspense every 15 seconds.

Use reasoning-state changes:

1. new number;
2. new comparison;
3. concrete example;
4. counterexample;
5. role switch;
6. reveal a hidden payer/cost;
7. ask viewer to predict;
8. compress into a rule.

Attention reset should coincide with cognitive movement.

---

# 9. Save / Share / Comment V1

These remain separate behavior hypotheses.

## Save = Deferred Reuse

Give something worth reopening:
- decision rule;
- checklist;
- model;
- comparison table;
- script/template;
- ordered process.

## Share = Proxy Speech + Useful Discovery

Give the viewer something precise they want another person to hear:
- a reframe;
- a useful discovery;
- a sentence that accurately articulates a shared experience.

## Comment = Self Projection + Experience + Conflict

Create a legitimate insertion point:
- self-location;
- lived experience;
- evidence-backed disagreement;
- practical diagnostic question.

Do not treat engagement categories as proven causality. RC6I supports association only because top comments and full transcripts are missing.

---

# 10. 4–5 minute production spine V1

## 0–8s — Payload

Use O1/O2/O3/O4. Viewer must know the stake immediately.

## 8–30s — Question Debt

State the unresolved difference/mechanism/choice.

## 30–90s — Mechanism 1

Explain the first hidden relation. One stable carrier.

## 90–160s — Proof

Case, data ladder, field observation, transaction, or market feedback.

## 160–220s — Mechanism 2 / constraint

Show where the simple explanation breaks or what condition matters.

## 220–270s — Decision rule

Give a compact rule the viewer can apply.

## final 20–30s — Memory model + loopback

Return to the opening and show why the viewer would answer it differently now.

Timing is a production default; actual TTS duration remains final authority.

---

# 11. Guanyu ability-monetization preset V1

Primary spine: `L3 State Transition`
Secondary support: `L5 Constraint Optimization`
Evidence preference: `E5 Market Feedback > E1/E4 > E3`
Action: `A3 Decision Rule`

Canonical chain:

`你会什么`
-> `谁因为这个问题正在付高成本`
-> `你能交付什么可验结果`
-> `谁是付款者`
-> `对方为什么敢第一次付钱`
-> `怎么降低第一次交易风险`
-> `怎么形成重复交付/复购`

Opening should not be “能力很重要”。

Better:

`很多有能力的人赚不到钱，问题根本不在能力。你把一件事做得再好，如果它没有被包装成别人愿意付钱验收的结果，它就还是你的能力，不是生意。`

This is a generated application of the engine, not a copied benchmark phrase.

---

# 12. Anti-AI QA V1

Reject a draft if any of the following is true:

1. opening delays the actual topic for more than two sentences;
2. paragraph contains three abstract nouns before one concrete picture;
3. every paragraph ends with a slogan;
4. five-item list replaces one causal chain;
5. same conclusion is restated three times;
6. analogy changes every paragraph;
7. “底层逻辑” appears without an explicit mechanism;
8. claim certainty exceeds evidence certainty;
9. rhetorical question does not cause a new reasoning step;
10. ending merely encourages instead of compressing a reusable rule.

---

# 13. Evidence confidence table

## HIGH confidence for production testing

- one primary reasoning spine;
- familiar language before unfamiliar abstraction;
- concrete carrier and real consequence;
- contradiction/self-location/concrete-result openings;
- evidence must do reasoning work;
- one stable carrier per explanation block;
- constraint/counterexample before final decision rule;
- memory model + loopback ending.

## MEDIUM confidence

- Save as Deferred Reuse;
- Share as Proxy Speech + Useful Discovery;
- Comment as Self Projection / Experience / Conflict;
- Question Debt as a general retention mechanism.

These are plausible cross-sample associations, not causal platform laws.

## DEFERRED

- exact oral filler frequency;
- creator-independent sentence-ending habits;
- precise lexical rhythm;
- frozen Guanyu Voice Profile.

Reason: existing full transcripts contain significant ASR noise, while RC6I only supplies opening fragments and no comment corpus.

---

# 14. What changed from previous candidate rules

1. Opening guidance is now stricter: **payload first**; generic setup is explicitly rejected.
2. RC6I is formally scoped to opening/market-response evidence only.
3. Full-structure claims are grounded only in full-transcript batches.
4. Plain-language rules are retained but separated from Voice Profile claims.
5. Attention reset is tied to reasoning-state change, not arbitrary suspense frequency.
6. Production engine is now usable for article/script generation even though phrase-level voice remains unfrozen.

---

# 15. Next acceptance test

Use one unseen China-native topic and generate a 4–5 minute script with:

- one O-entry;
- one primary L-engine;
- 3–5 cognitive gains;
- one concrete evidence anchor;
- one meaningful constraint;
- one A3 decision rule;
- one memory model;
- no forced catchphrases.

User acceptance questions:

1. 前10秒会不会继续听？
2. 听完30秒能不能准确说出“问题到底是什么”？
3. 中段有没有新的认知，而不是换句话重复？
4. 有没有明显 AI 腔或刻意金句？
5. 听完后能不能用一句规则重新做判断？

Failure returns to evidence teardown, not cosmetic polishing.
