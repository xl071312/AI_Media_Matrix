# Guanyu Spoken Voice v0.1 — CANDIDATE

Date: 2026-09-17
Owner: ChatGPT
Status: CANDIDATE / user-validation required

## Basis

This candidate is built from two different evidence layers:

1. Market high-performance spoken transcripts: used to learn conversational mechanics, not to copy a creator.
2. User's own long-form spoken material (`吾剑.docx`): used to identify the user's natural discourse habits, sequencing, stance, and rhythm.

Important: raw live-speech disfluency is evidence of natural speech, but should not be copied mechanically into a script. We preserve the function, not every stutter/filler.

## Core correction

The prior Guanyu drafts were structurally sound but still GPT-like because they overused:

- one-line short sentences;
- consecutive punchlines;
- polished parallel structures;
- abstract summary language;
- every sentence behaving like a subtitle card.

New rule:

**A spoken script should feel like one person thinking aloud to another person, not like 30 title cards stitched together.**

## 1. Sentence rhythm

Default paragraph: 2–4 sentences.
Default sentence: allow one complete thought to run naturally through cause, contrast, example, and qualification.
Single short sentence is reserved for true emphasis, not used as the base rhythm.

Preferred rhythm:

`medium/long spoken sentence -> short clarification -> medium sentence -> occasional punchline`

Avoid:

`short -> short -> short -> short -> slogan`.

## 2. Conversational glue

The following are not decoration. Each has a specific job.

### Listener alignment

- `你想想`
- `你看`
- `你说`
- `对吧`
- `你可能会觉得`

Use when asking the listener to perform one mental operation: compare, imagine, locate, judge.
Do not place one in every paragraph.

### Stance / honesty markers

- `说实话`
- `我觉得`
- `我反而觉得`
- `我一开始也以为`
- `我后来越想越觉得`
- `我最不理解的是`

These give the voice an owner. Guanyu should not sound like an anonymous textbook.

### Reframing markers

- `其实`
- `说白了`
- `换句话说`
- `这么说可能没感觉`
- `问题就在这儿`

Use to lower abstraction after evidence, not to announce fake depth.

### Narrative continuation

- `然后`
- `后来`
- `后面呢`
- `结果`
- `那时候`
- `再往后`

These are useful because real speech often advances through time and causality rather than perfect essay transitions.

### Soft modal particles

- `啊`
- `呢`
- `吧`
- `嘛`
- `呀`

Use lightly to soften, invite agreement, or carry emotion.
Examples:
- `你说这事怪不怪？`
- `这钱贵吗？其实也不算贵。`
- `不可能的嘛。`
- `那接下来呢，问题就来了。`

Do not sprinkle particles randomly. Every particle should change tone.

## 3. Useful imperfection

Real speech contains self-correction and local repetition.
Guanyu may deliberately keep a small amount of this:

- `我一开始以为……后来发现不是。`
- `这事我第一次看也觉得挺正常，后来越想越不对。`
- `肯定不行，真的不行。`
- `这个东西说复杂也复杂，说简单其实也简单。`

Allowed: local repetition for emotion or emphasis.
Not allowed: fake stammering, excessive `呃`, duplicated words, ASR-like broken grammar.

## 4. Deictic language

Use human pointing words:

- `这事`
- `这个东西`
- `那一步`
- `这里面`
- `这一下`
- `那时候`

These reduce essay distance and make the explanation feel situated.

Prefer:
`这事真正麻烦的地方，是……`

Over:
`该事件所反映出的核心问题在于……`

## 5. Opinion ownership

Guanyu must show a point of view, not just a conclusion.

Preferred:
`我现在越来越不相信只拿模型跑分讲AI未来这件事了，因为一个AI如果连你最常用的三个App都进不去，它再聪明，很多时候也只是站在门外给你出主意。`

Avoid:
`AI行业的竞争正在从模型能力转向生态权限。`

The second sentence may be analytically correct, but it has no person inside it.

## 6. Emotion without melodrama

Emotion comes from reaction to a concrete fact:

- 荒唐：`这就有点离谱了。`
- 怀疑：`我看到这里第一反应其实是不太信。`
- 惋惜：`你说可惜不可惜？`
- 反感：`我最烦的就是这种……`
- 惊讶：`这一下我是真没想到。`

Do not manufacture emotion with generic exclamation or stacked adjectives.

## 7. Paragraph logic

Each paragraph should sound like a spoken turn, not an outline item.

Good pattern:

`事实 -> 我的反应 -> 你可能的反应 -> 再解释一步`

or

`先说一个判断 -> 举个熟悉例子 -> 再把判断收回来`

or

`我一开始怎么看 -> 后来发现哪里不对 -> 现在我怎么看`

This produces a human thinking process instead of a polished lecture.

## 8. User-native traits worth preserving

From the user's own long-form speech, the useful tendencies are:

- likes to reason through `因为 -> 所以 -> 然后 -> 再去看`; 
- frequently uses `我觉得` to own a judgment;
- naturally uses `对吧` to check alignment;
- often explains by telling the path of how a conclusion was reached;
- uses examples from personal experience rather than only abstract claims;
- allows a thought to unfold in a longer sentence instead of chopping it into slogans;
- often restates one key point in slightly different words when it matters.

Do not copy the raw density of `就是/然后/呃` from live interviews. Scripted Guanyu should be cleaner, but keep the same reasoning motion.

## 9. Market-spoken traits worth borrowing

Across usable high-performance transcripts, the valuable spoken devices include:

- `我说真的`
- `我直接用大白话跟你讲`
- `我就这么跟你说吧`
- `你现在想想`
- `然后结果你们看呢`
- `你不要觉得说啊`
- `其实说白了`
- `你还担心……啊`
- `这么说可能没感觉，我给你打个比方`
- `你可能会觉得……其实……`

These work because they manage listener attention and turn abstract reasoning into conversation.
They are functions, not signature phrases to repeat mechanically.

## 10. Anti-GPT blacklist

Rewrite when a draft shows three or more of the following:

- 3 consecutive one-line punch sentences;
- repeated `真正的……是……`;
- repeated `这才是……`;
- fake profundity through `底层逻辑`;
- every paragraph ending with a quotable slogan;
- rigid `第一/第二/第三` when the content is really a story or argument;
- `你想一下` inserted without a real mental task;
- perfectly symmetrical parallelism;
- abstract nouns stacked before the listener has a picture;
- no visible `我` or personal stance in an opinion piece.

## 11. Current Guanyu target voice

**像一个逻辑很强、见过事、愿意把自己的真实判断讲出来的人，坐在你对面聊天。**

不是主播腔。
不是知识付费老师腔。
不是连续金句。
不是故意装粗口。
不是把逐字稿写成书面文章。

Desired feeling:

`有观点，但不端着；有逻辑，但不像上课；有情绪，但不煽；能说长句，也知道什么时候突然停一下。`

## 12. Test paragraph

`5999块买一台AI手机，我一开始觉得这个价格也不算离谱——如果它真能把手机里那些破事接过去，值不值另说，至少这逻辑是成立的。可真机一出来有个地方特别逗：微信能打开，美团能打开，淘宝也能打开，可你真让它替你往下办，它又停了。你说这像不像你花钱请了个很聪明的助理，人到了，公司门禁卡没给他？所以我后来越想越觉得，AI接下来拼的可能真不是谁脑子更聪明，而是谁手里的钥匙更多。`

This paragraph is the current style benchmark for future testing.
