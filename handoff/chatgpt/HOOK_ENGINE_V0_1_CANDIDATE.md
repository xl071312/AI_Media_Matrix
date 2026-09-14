# Guanyu Hook Engine v0.1 — CANDIDATE

Date: 2026-09-13
Owner: ChatGPT
Status: CANDIDATE / requires external-topic validation
Scope: first 30 seconds of 4–5 minute cognition/knowledge videos

## Why this layer exists

External validation exposed a gap in Logic Architecture v0.3: `conflict/anomaly` is not automatically a hook. A conflict may be real inside the news event but still feel irrelevant to the viewer.

The missing layer is **Audience Relevance before Topic Context**.

A Guanyu opening should not begin by proving the topic is important. It should first make the viewer feel that the unresolved problem is already about their money, work, status, risk, choices, identity, or everyday experience.

## Evidence patterns from the current spoken corpus

Observed high-performing openings include:

- **Outcome shock** — B002-003 opens with `8000块 -> 半年130万` before background.
- **Direct personal threat** — B002-010 opens with `你们知道对钱没有概念有多可怕吗` before explanation. This sample has 859,506 likes and 638,381 shares in the verified performance table.
- **Identity + reframe** — B002-007 opens by addressing entrepreneurs and immediately says their biggest problem is not the obvious one.
- **Self-location** — B002-012 immediately asks what level an ordinary person's monthly income is at, then places `5000元` on a national ladder.
- **Specific desire + error** — 7672991243072616697 opens approximately as `想赚100万，99%的人第一步就选错了`, then offers three concrete routes.
- **Compression promise** — 7680569771779521482 opens by claiming a single formula can explain earning behavior, then immediately introduces A→B.
- **Role-play contradiction** — 7600957703851148773 opens by putting the viewer in the role of a financial giant facing a contradictory incentive. This can work, but it has a higher comprehension burden than direct ordinary-person relevance.
- **Identity + utility inventory** — B002-011 opens by speaking to `普通女生想搞钱` and immediately promises 20 routes.
- **Belief challenge + proof** — B002-009 questions whether self-media can still change income, then immediately uses creator experience/proof.

These examples do not prove platform-wide causal laws. They are working structural patterns for Guanyu testing.

## Core correction to the script engine

Old default:

`Conflict/Anomaly -> Question Debt -> Mechanism -> Evidence ...`

Candidate new default:

`Audience Mirror -> Personal Stakes -> Contradiction -> Question Debt -> Topic/News Reveal -> Mechanism -> Evidence ...`

News is usually **evidence of a mechanism**, not the first object the audience should be asked to care about.

## Opening time architecture

### 0–3s — Audience Mirror
The first sentence must connect to something the target viewer already recognizes.

Preferred entry objects:
- money lost / money desired
- income / price / cost
- work pressure / job risk
- business survival
- status / self-location
- time wasted
- a common contradiction in ordinary life

Do not lead with company background, executive names, conference names, dates, or abstract macro framing unless the viewer is already directly affected by them.

### 3–8s — Stakes
Show why the problem costs the viewer something or threatens something they care about.

Useful stake types:
- `你先停，别人不停，先吃亏的可能是你`
- lost money
- lost time
- missed opportunity
- loss of certainty
- social/status disadvantage

### 8–15s — Contradiction / Open Loop
Create a tension the intuitive explanation cannot fully resolve.

Examples of structures:
- everyone wants X, but behavior produces not-X
- the person with the strongest reason to do A instead does B
- the apparently safer choice creates a larger risk
- the apparently richer/higher-income person has less real freedom
- the obvious cause is not the main cause

### 15–30s — Reveal + Promise
Only now reveal the external event, company, case, or news as a large real-world example.
Then state the precise unresolved question the video will explain.

By 30 seconds the viewer should know:
1. why this matters to them;
2. what is strange about it;
3. what they will understand if they continue.

## Eight hook families for testing

### K1 Outcome Shock
`small input / unusual action -> large concrete result`
Best for: business cases, earning, AI execution, experiments.

### K2 Loss / Threat
`something you do normally may be costing you much more than you think`
Best for: consumption, middle class, work, hidden costs.

### K3 Self-Location
`where are you on this ladder / which group are you in?`
Best for: income, consumption, career stage, capability stage.

### K4 Identity Mirror
`普通人 / 打工人 / 小老板 / 中产 / 某类具体人群 -> 你正在遇到的问题`
Best for: group-specific pain and proxy speech.

### K5 Counterintuitive Reframe
`真正的问题不是A，而是B`
Best for: cognition pieces. Must not reveal B as an empty slogan; a question debt must remain.

### K6 Constraint Choice
`goal -> only a few routes -> most people choose the wrong one because of a hidden constraint`
Best for: earning, business models, decisions.

### K7 Everyday Paradox
`everyone wants X, but everyone together creates not-X`
Best for: news translation, competition, workplace, pricing, education, AI races.

### K8 Live Proof / Demonstration
Show the result or artifact before explanation.
Best for: AI tools, practical workflows, visible transformations.

## News Translation Protocol

For a news story, do not ask first: `what happened?`
Ask first:

1. **What ordinary-person mechanism is this news a giant example of?**
2. **Where does the viewer already experience that mechanism?**
3. **What does it cost them?**
4. **What contradiction does the news make visible?**
5. **What reusable model can the viewer take away?**

Transform:

`Entity A said X; Entity B did Y`

into:

`You already live inside mechanism M -> here is the surprising cost -> today's event is a huge real-world proof of M -> why does M force people into behavior they themselves dislike?`

## Hard Fail Gate for first 15 seconds

Any mandatory failure below rejects the opening before full-script drafting:

1. **Viewer relevance FAIL** — first sentence has no recognizable viewer situation, desire, loss, identity, or decision.
2. **Stake FAIL** — by 8s there is no concrete reason to care.
3. **Question-debt FAIL** — by 15s there is no unresolved contradiction or question.
4. **Context-first FAIL** — opening begins with `今天有一条新闻`, `最近某公司`, `某CEO表示`, or equivalent background summary without a viewer mirror.
5. **Proper-noun overload FAIL** — more than one unfamiliar proper noun appears before relevance is established.
6. **Abstract-first FAIL** — an abstract term such as `集体行动困境`, `博弈论`, `底层逻辑`, `宏观趋势` appears before a concrete scene or tension.

Secondary review checks:
- proof/credibility appears by ~30s when factual;
- hook promise matches the actual reasoning spine;
- no fake urgency, fake statistics, or bait-and-switch.

## Hook QA score

Score 1 point each:
- viewer mirror
- personal stakes
- concrete language
- contradiction
- question debt
- low comprehension burden
- topic reveal serves the hook rather than replacing it
- promise can be paid off by the ending

Target: **>=7/8**.
Mandatory: viewer mirror + stakes + question debt.

## Important limitation

This is a candidate engine, not a frozen platform law. It was created because the first external-news test failed at the opening. It must now survive external-topic tests before being merged into the canonical Guanyu Script Rules.
