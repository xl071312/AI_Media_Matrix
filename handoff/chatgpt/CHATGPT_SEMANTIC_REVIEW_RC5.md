# ChatGPT Semantic Review RC5

Date: 2026-09-12
Owner: ChatGPT (semantic/model review)
Source branch: `chatgpt-handoff`
Reviewed through commit: `96048c1`

## 1. Corpus decision

### Wave001

Wave001 is accepted into the Logic Corpus as **20/20 logic-analyzable**.

Reason: all 20 are in-domain for the benchmark (赚钱/副业/AI变现/商业逻辑/普通人收入/财富认知 or closely related business cases), have real persisted article bodies, and RC5 repaired the truncation issue. Low evidence quality or promotional tone does not automatically exclude a sample; such items remain useful as structural controls.

### Wave002 semantic review

The mechanical gate is not the final semantic gate. ChatGPT reviewed the Wave002 candidates and assigns the following final research roles.

#### LOGIC_ANALYZABLE — include in primary logic corpus

- `7677915384284037651` — 龙牙：冷门品类、定位、用户身份认同、破圈与品牌扩张；商业案例。
- `7683168637653598759` — 普通人阶层跨越：时间/精力约束→低质量恢复→能力不增长→循环；职场/普通人收入机制。
- `7684223864338924073` — 琳朝珠宝：稀缺、手艺、价值锚点、品牌信任与规模约束；商业/消费机制案例。
- `7680513034233676323` — DeepSeek：愿景约束资源分配、基础模型定位、低价工程与商业取舍；AI/商业战略案例。
- `7683110588213363240` — 源氏木语：用户痛点、品牌信任迁移、供应链复用、品类扩张与规模循环；商业机制案例。

Wave002 final semantic logic pass = **5**.

#### AUXILIARY_EXPRESSION — keep for expression/style comparison, do not count toward logic milestone

- `7618185265378640403` — 写作素材/踩坑/口语化表达，主要是创作经验，不是当前核心赚钱/商业逻辑。
- `7618556274149491219` — “不硬写”创作经验，适合作为自然口语/叙事表达参考，不进入核心逻辑语料。

#### REJECT_SHORT_OR_INCOMPLETE

- `7671488207304868404` — 仅94字，只到“第一”条，结构明显不完整。
- `7678657654369141289` — 165字AI并购快讯，信息短且缺乏可分析论证链。

#### NO_EVIDENCE

- `6930801562751435267`
- `6979123251842957831`

#### OFF_TOPIC — do not count

- `7048926434592555558` — 疫情隔离日记
- `7049600535418143270` — 疫情隔离后续
- `7187298184346206754` — 外墙保温技术
- `7618573005362332196` — 人际关系/合群
- `7681510302478942759` — 跑步伤病
- `7683548929375339037` — 跑步人生感悟
- `7684096740282171948` — 家庭/夫妻叙事
- `7684362605640647222` — 服贸会新闻
- `7684447381258666559` — 政治新闻

## 2. Updated verified research count

Previous model-verified logic corpus: **60**

+ Wave001 model review: **20**

+ Wave002 semantic logic pass: **5**

= **Verified Logic Corpus = 85/100**

Independent logic observations should be recomputed from the accepted content set after exact duplicate/near-duplicate check; do not assume it equals 85.

## 3. Important methodological finding

Recommendation-page discovery drifts strongly off-topic. Therefore future Toutiao collection must perform a cheap title/snippet/metadata topic gate **before** full-body extraction. Generic recommendation adjacency is not sufficient evidence of topical relevance.

The following categories are allowed as PRIMARY logic candidates:

- 赚钱逻辑 / 搞钱 / 普通人收入
- 能力变现 / 副业 / AI赚钱
- 商业思维 / 商业模式 / 创业
- 职场收入 / 人效 / 价值交换
- 信息差 / 市场验证 / 需求
- 财富认知 / 消费认知 / 中产焦虑
- business cases that expose a reusable mechanism (positioning, supply chain, pricing, customer value, trust, distribution, constraints)

Pure lifestyle, sports, politics, general news, relationships, health, construction/engineering technical content, or unrelated personal diary content is OFF_TOPIC for this corpus.

## 4. Current research state

- Verified Logic Corpus: **85/100**
- Remaining milestone gap: **15**
- Wave001: FROZEN / ACCEPTED 20
- Wave002: FROZEN for semantic status above
- Next collection should deliberately oversample ~20 new on-topic candidates to obtain >=15 model-usable samples.

No Voice Profile conclusion is authorized from Toutiao articles; article text can inform logic and written expression only, not spoken Voice Corpus.
