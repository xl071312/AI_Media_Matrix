# Guanyu Plain Language Engine v0.2 — CANDIDATE

Date: 2026-09-13
Owner: ChatGPT
Status: CANDIDATE / continue external validation
Purpose: stop AI-style abstract prose and force scripts into ordinary spoken Chinese before production.

## Why v0.1 was not enough

Previous drafts were logically coherent but still sounded generated: complete sentence symmetry, abstract nouns, multi-clause explanations, and early use of terms like `标准化`, `权重`, `结构`, `机制`, `价值`, `约束`.

The corpus shows a different surface pattern: viral speakers often deliver the result first, use short concrete clauses, repeat themselves, ask crude/direct questions, use money/work examples, and only later name an abstraction if needed.

## Corpus-derived sentence behavior

### 1. One sentence, one thing

Common spoken pattern:
- `你工作上最大的问题，就是效率太高了。`
- `为什么？`
- `真正厉害的人，从来不看我觉得，他们只看反馈。`
- `你会的，别人不会的，你就能从中间赚到钱。`

Do not compress three claims into one elegant sentence.

### 2. Result first, explanation later

Observed forms:
- `8000块，半年赚到130万。`
- `你工作上最大的问题，就是效率太高了。`
- `想赚100万，99%的人第一步就选错了。`
- `我说真的，我现在看到满地都是商机。`

Rule: opening sentence should already contain the payload, not only introduce the topic.

### 3. Use words people already use at work/home

Preferred noun/verb inventory:
- 钱、工资、老板、客户、订单、亏、赚、买、卖、做、改、等、问、试、错、看、花、拿、跑、加班、返工、客户、店、货、成本、时间

Delay or replace abstract labels:
- `标准化任务` -> `别人能一条一条告诉你怎么做的活`
- `价值权重下降` -> `这种活以后没那么值钱了`
- `决策风险` -> `他为什么敢先把钱给你`
- `市场反馈` -> `先看看有没有人真愿意买`
- `需求验证` -> `先问十个人，看看有几个真要`
- `商业闭环` -> `有人愿意付钱，而且还能重复做`

### 4. Explain with action, not definition

Corpus example pattern from B002-026:
Instead of defining `验证需求`, the speaker says: spend 100 yuan, print flyers/buy fruit, sit at the community entrance, ask whether people would add WeChat; five out of ten means demand may exist, nobody wants it means stop.

Rule:
`abstract claim -> visible action -> observed result -> plain conclusion`

### 5. Use the viewer's next question as the transition

Corpus transitions:
- `为什么？`
- `普通人怎么干？`
- `但是高手不是这样。`
- `你现在想想，什么东西是你会的别人不会的。`
- `你看，就这么一句话。`
- `那你到底在怕什么？`

Avoid essay transitions:
- `从更深层次来看`
- `这背后反映的是`
- `进一步而言`
- `从结构上看`

### 6. Spoken imperfection is allowed

Human speech includes:
- repetitions
- `你看`
- `我就这么跟你说吧`
- `说白了`
- `为什么呢`
- `但是`
- short self-corrections
- incomplete but obvious clauses

Do not over-polish these into balanced written prose.

### 7. Numbers need a job

Good numbers either:
- shock: `8000 -> 130万`
- locate: `5000块在全国什么水平`
- compare: `100个人×1万 / 1000个人×1000`
- test: `先花100块试`
- price: `9块9你都愿意花`

Do not add percentages just to sound authoritative.

### 8. Use examples before theory

Default sequence for difficult ideas:
`先讲一个人/一笔钱/一件事 -> 观众看懂 -> 再说这说明什么`

Do not begin:
`AI正在重构职业价值分配机制。`

Prefer:
`有一种活，以后会越来越便宜：别人把步骤写给你，你照着做完。`

Then show a real case/source.

## Hard anti-AI language gate

Reject a script sentence before production when any of these are true:
1. listener must hold more than two abstract concepts in one sentence;
2. sentence has three or more parallel abstract clauses;
3. writer uses a term that a non-specialist needs explained before understanding the sentence;
4. sentence could appear unchanged in a consultancy report or policy memo;
5. sentence says `本质上/底层逻辑/结构性/系统性/价值重构/能力权重` without an immediately preceding concrete example;
6. three consecutive sentences contain no person, money, action, object, number, or visible event.

## Plain-language rewrite protocol

For every important sentence:
1. underline the concrete person;
2. identify what they want/lose/pay/do;
3. replace abstract noun with an action;
4. split one long claim into 2–4 short clauses;
5. add one ordinary example if still unclear;
6. read once aloud: if a listener needs rewind, fail.

## Example transformation

AI-style:
`AI最先压低价值的，可能不是某一个职业，而是一个职业里最容易标准化、最容易被交代清楚、最容易重复执行的那部分工作。`

Plain-language candidate:
`有一种活，以后会越来越不值钱。别人把步骤写给你，你照着做完。这样的活，AI最容易接过去。`

AI-style:
`需求验证能够降低创业中的决策风险。`

Plain-language candidate:
`别一上来就砸十万。先花一百块试试，看看到底有没有人愿意掏钱。`

AI-style:
`未来更重要的是需求理解与结果校验能力。`

Plain-language candidate:
`以后光会把活做完不够。你得先听懂老板到底要什么，做完以后还得看它到底对不对。`

## Writing order change

Old:
`research -> logic map -> polished script`

New:
`research -> logic map -> rough human speech -> remove abstract words -> oral read-through -> only then tighten logic`

Do not polish first and "口语化" afterward. That tends to preserve AI syntax under casual filler words.

## Status

Not frozen. Must pass multiple China-context external-topic tests and user listening approval before merging into canonical Script Rules.