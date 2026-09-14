# Guanyu Plain-Language Engine v0.5 — CANDIDATE

Date: 2026-09-14
Owner: ChatGPT
Status: CANDIDATE / not frozen
Supersedes: `PLAIN_LANGUAGE_ENGINE_V0_4_CANDIDATE.md` for current testing
Evidence added: semantic audit of RC6F transcript-bearing samples. RC6F as a whole is **not** accepted as a 30-sample corpus.

## Why v0.5 exists

v0.4 made the key correction that Guanyu should usually explain from concrete experience toward abstraction. RC6F adds useful counterexamples and refinements.

The most important correction is:

> **The enemy is not abstraction itself. The enemy is asking the listener to decode an unfamiliar abstraction before they can picture the thing.**

A familiar topic word such as `汇报`, `工资`, `消费`, `存钱`, `房贷` can appear immediately because the listener already owns the mental picture. A term such as `结构性变化`, `边际收益`, `非结构化判断`, `流动性陷阱` usually needs a bridge first.

So the stronger rule is:

**熟悉的词可以先说；陌生的概念要后命名。**

---

## Evidence classes from RC6F

### Strong positive structure evidence

- `RC6F_010`: familiar workplace topic -> audience distinction -> concrete result -> number -> everyday analogy -> process story -> takeaway.
- `RC6F_011`: one concept explained almost entirely by price equivalence and before/after choice.
- `RC6F_012`: intuitive expectation -> contradiction -> behavior -> consequence -> only then concept label; stable fictional carrier throughout.

### Structure-usable but phrase-level noisy

- `RC6F_003`
- `RC6F_008`
- `RC6F_013`

These can support explanation-order hypotheses, but not exact phrase-frequency claims.

### Negative/control

- `RC6F_009`: useful as an example of why easy language alone is not enough; it mixes readable speech with unsupported certainty and engagement bait.

### Reject for expression learning

- `RC6F_006`: character count passes mechanically but speech is not semantically reconstructable.
- `RC6F_007`: too much ASR corruption / scene mixing for reliable phrase learning.

---

# v0.5 Core Rules

## Rule 1 — Familiar abstraction exception

Do not mechanically force every script to begin with a physical object or scene.

Allowed early if instantly understood by a general audience:

- 汇报
- 工资
- 存钱
- 负债
- 消费
- 老板
- 客户
- 买房
- 加班

Usually delay until earned:

- 结构性
- 范式
- 边际
- 系统性风险
- 认知框架
- 非结构化任务
- 供需错配
- 流动性陷阱

Test:

`听到这个词，普通人脑子里马上有没有画面？`

If yes, it may open the topic. If no, build the picture first.

## Rule 2 — One contrast should do real explanatory work

RC6F_011 shows a high-value pattern:

`同一笔钱 -> 两种完全不同的去处`

That lets the audience feel the decision rather than hear a lecture about priorities.

General form:

`X元买A`
vs
`X元可以买B`

or:

`以前要做A`
vs
`现在同样条件下变成B`

or:

`直接领导关心A`
vs
`更高层关心B`

The contrast must change the viewer's judgment, not merely add variety.

## Rule 3 — Equivalence Converter

A number becomes plain language when converted into something already familiar.

Weak:

`成本降低40%。`

Stronger:

`以前100块，现在60块。`

Stronger again when useful:

`省下的40块，刚好等于另一件观众熟悉的东西。`

RC6F_011 and RC6F_010 both support this mechanism in different forms.

Formula:

`abstract number -> familiar unit -> felt meaning`

Use only when the equivalence is real and not misleading.

## Rule 4 — Vague -> number -> lived meaning

RC6F_010 provides a useful three-step ladder.

Do not stop at:

`提升很多。`

Move to:

`从A到B。`

Then, if comprehension still benefits, translate to an everyday consequence:

`这意味着用户/老板/客户实际少等多久、少做多少次、少花多少钱。`

This is different from statistic decoration. The number exists to make the result imaginable.

## Rule 5 — Audience-role fork

A complex topic becomes simpler when the script asks:

`这件事对谁来说，最关心的是什么？`

RC6F_010 uses this effectively with different levels of workplace audience.

General structure:

`同一件事`
-> `角色A最关心什么`
-> `角色B最关心什么`
-> `所以你应该怎么说/怎么做`

This is especially useful for:

- workplace communication;
- business transactions;
- pricing;
- management;
- customer decisions;
- policy explanation.

It prevents one generic abstraction from pretending every stakeholder thinks the same way.

## Rule 6 — Intuition first, contradiction second, label last

RC6F_012 is the strongest current example of the v0.4 thesis.

Pattern:

1. state what a normal person expects;
2. show what actually happens in the example;
3. ask why;
4. walk through the behavior;
5. name the concept only after the listener has already understood it.

Generic form:

`按理说A，应该会B。`
`但现实里却出现C。`
`为什么？`
`因为人先做了D。`
`D继续下去，又导致E。`
`这个现象才叫X。`

This is a preferred explanation pattern for economics, technology, workplace incentives and business mechanisms.

## Rule 7 — Stable carrier beats example hopping

RC6F_012 keeps one fictional world/role set while changing only one economic condition at a time.

That lowers working-memory cost.

For Guanyu:

- one boss + one employee;
- one shop + one customer;
- one household + one monthly bill;
- one product + one price;

is usually better than jumping through four unrelated industries to prove one mechanism.

Change the carrier only when the new carrier adds a different reasoning function.

## Rule 8 — Lists need an explanatory spine

A numbered list alone is not reasoning.

RC6F_013 shows why lists are easy to follow, but its claims also show the risk of certainty and overgeneralization.

Guanyu may use a list only when every item answers the same question under the same decision rule.

Good:

`判断一件副业值不值得做，我只看四件事：谁付钱、结果能不能验、第一次交易风险多大、能不能复购。`

Bad:

five unrelated pieces of life advice grouped only because there are five of them.

## Rule 9 — Direct question must create the next mental move

Useful questions are not decoration.

They should force one of four operations:

- compare;
- calculate;
- identify payer;
- predict consequence.

Examples of useful forms:

- `那老板为什么还要请你？`
- `这钱到底是谁付？`
- `如果今天更便宜，你为什么反而不买？`
- `同样1000块，你到底换回了什么？`

Avoid rhetorical questions whose answer changes nothing.

## Rule 10 — Concrete language can still be bad reasoning

RC6F_009 is the warning.

A script can be easy to understand and still fail Guanyu because it relies on:

- guaranteed outcomes;
- destiny/luck framing;
- unsupported certainty;
- engagement bait pretending to be evidence;
- universal claims without constraints.

Therefore Plain Language QA and Evidence QA remain separate gates.

`听得懂` is necessary.
`说得对` is separate.
`值得相信` is separate again.

## Rule 11 — ASR character count is never semantic evidence

RC6F_006 proves that `>50 chars` can still be garbage.

Corpus pipeline must separate:

- mechanical speech presence;
- semantic intelligibility;
- phrase-level transcription reliability;
- positive style suitability.

Only ChatGPT assigns the latter three semantic statuses.

Do not learn exact oral phrases from a transcript merely because it is long.

## Rule 12 — Phrase learning needs higher evidence than structure learning

A noisy transcript may still show:

- one stable carrier;
- list structure;
- question placement;
- contrast placement;
- number/example position.

But it cannot support exact claims such as:

- favorite transition phrase;
- filler frequency;
- sentence-ending habit;
- recurring catchphrase;
- precise lexical rhythm.

Therefore keep two evidence levels:

`STRUCTURE_USABLE`
and
`PHRASE_USABLE`

Voice Profile should use only `PHRASE_USABLE` material.

---

# Recommended 30–60 second explanation block v0.5

Default scaffold:

`一句熟悉的人话题目/判断`
-> `一个稳定角色或场景`
-> `一个对比或变化`
-> `问一句普通人真的会问的问题`
-> `用数字/动作推进一步`
-> `把数字翻译成实际感受`
-> `再推进一个因果`
-> `最后才压缩成概念/规则`

Not every block must contain every element.

The invariant is that each new sentence should reduce uncertainty rather than add terminology.

---

# First-30-second QA v0.5

A draft should normally pass all:

1. viewer knows the topic within 1–2 sentences;
2. opening uses familiar language even if the topic noun itself is abstract;
3. one concrete stake is visible: money/work/time/risk/choice/status;
4. no unexplained high-friction term is required to understand the conflict;
5. one stable carrier is identifiable;
6. at least one contrast/question gives the viewer a reason to continue;
7. no sentence requires holding more than roughly one new mental move;
8. the viewer can retell the conflict after hearing it once;
9. evidence claims are not replaced by certainty rhetoric.

---

# Current v0.5 synthesis

The strongest current production heuristic is now:

> **先用熟悉词把问题说清楚；再让观众看见一个人、一笔钱、一次动作或一个前后变化；让他自己产生下一问；用对比和可感知的数字回答；最后才把这一串压成一个概念。**

A shorter formula:

`熟悉入口 -> 稳定载体 -> 对比/异常 -> 普通人问题 -> 数字/动作 -> 后果 -> 概念`

This is a script-generation candidate, not a platform law.

---

# Status and next validation

v0.5 is **stronger than v0.4 but still not frozen**.

Do not move to Voice Profile freeze yet.

Next:

1. HERMES builds RC6G mechanically clean speech-dense reserve;
2. ChatGPT semantically selects enough genuinely new, intelligible samples;
3. attack v0.5 with counterexamples;
4. only after the rules survive that test, run an unseen China-native topic generation test;
5. user judges whether the result is naturally understandable and worth continuing to hear;
6. failure returns to teardown, not cosmetic rewrite.
