# Guanyu Spoken Explanation Engine v0.1 — CANDIDATE

Date: 2026-09-13
Owner: ChatGPT
Status: CANDIDATE
Scope: how to explain the middle of a cognition video in ordinary spoken Chinese after the hook.

## Problem

A hook can sound human while the body still turns into AI prose. The corpus suggests that strong spoken explanations repeatedly convert abstractions into one of six concrete carriers.

## E1 — 算一笔账

Use when the idea is about money, scale, tradeoff, price, or business model.

Corpus pattern:
`想赚100万 -> 100个人×1万 / 1000个人×1000 / 10000个人×100`

Why it works: listener solves the same problem with elementary arithmetic instead of learning a business term.

Rule: if a business concept can be turned into a multiplication/division/comparison that a middle-school student understands, do that first.

## E2 — 做一个小动作给你看

Use when the idea is validation, experimentation, workflow, or decision-making.

Corpus pattern from B002-026:
`别先开店砸钱 -> 先花100块 -> 发传单/拿样品 -> 去社区门口问 -> 有人加微信再继续`

Why it works: `需求验证` is understood without saying the term.

Rule: show what a person physically does tomorrow morning.

## E3 — 讲一个自己吃过的亏 / 做成的事

Use when the topic needs trust and lived experience.

Corpus pattern:
- 8000 yuan -> product idea -> search -> no existing product -> rough calculation -> cheap iteration -> presale.
- workplace speaker tells the exact meeting where someone challenged them and their brain went blank before giving the response rule.

Rule: story first, lesson after. Do not open the story with `这说明一个底层逻辑`.

## E4 — 换成一个人人见过的买东西场景

Use when explaining value, service, perceived quality, or transaction behavior.

Corpus pattern from B002-025 uses haircut / photo-service style examples: fast completion may not feel valuable because buyers also pay for communication, attention, confirmation and the feeling of being taken seriously.

Rule: choose a scene that needs no industry knowledge: haircut, food, shopping, rent, delivery, salary, phone, milk tea, traffic, store, WeChat.

## E5 — 让观众站进去

Use when explaining incentives or choices.

Common wording:
- `你想想`
- `如果是你`
- `你会怎么选`
- `你现在想想什么东西是你会的别人不会的`

Rule: one role at a time. Do not stack `假设你是老板、投资者、员工、监管者` in one paragraph.

## E6 — 先说人话结论，再补名字

Example:
First: `先花100块试试，看有没有人真要。`
Later, if useful: `这其实就是先验证需求。`

First: `别人把步骤写给你，你照着做，这种活最容易被AI接走。`
Later, if useful: `因为它更容易被标准化。`

Rule: technical label is optional. Understanding is mandatory.

## Transition language from the corpus

Preferred simple bridges:
- `为什么？`
- `你想想。`
- `比如说。`
- `你看。`
- `说白了。`
- `我就这么跟你说吧。`
- `但是高手不是这样。`
- `那普通人怎么干？`
- `结果呢？`
- `就这么简单。`

Avoid writing-style bridges:
- `进一步来看`
- `从更深层次上说`
- `这背后实际上反映了`
- `从结构性角度分析`
- `基于上述逻辑`

## Paragraph rhythm

A spoken block should usually follow:
`short claim -> question -> concrete example -> one-line takeaway`

Not:
`claim -> explanation -> explanation -> explanation -> abstract summary`

Maximum before a concrete carrier: roughly 2 abstract sentences. Third sentence must show a person, number, object, action, scene, or example.

## Human-repeatability gate

After drafting a cognitive point, ask:
`普通人听一遍，能不能用自己的话复述？`

If not, the explanation is not finished.

A good block often leaves the viewer with a sentence like:
- `别赌，先试。`
- `你会的别人不会，就有机会收费。`
- `不是把活干完，是先搞清楚别人到底要什么。`
- `有人真掏钱，才算需求。`

These are derived candidates, not quotations unless explicitly marked.

## Production rule

For now, every Guanyu script block must declare one carrier: `算账 / 动作 / 故事 / 日常场景 / 角色代入 / 人话结论+术语`.

If a block has none, it cannot enter production.

## Status

Still under拆机. Do not freeze until external-topic tests pass user listening review.