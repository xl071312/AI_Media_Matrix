# ASR log — 壹心托管 Douyin videos

- finished_at: 2026-09-16 00:04:17 PT
- asr_engine: faster-whisper medium (CPU int8)
- download: public `aweme/v1/web/aweme/detail` + music/video CDN (anonymous ttwid; no login)
- priority: likes desc → pinned → all 18 `works_detail_partial` videos

## Blockers
1. **yt-dlp** on `https://www.douyin.com/video/{id}`: blocked — “Fresh cookies needed”; bare HTML is 验证码中间页.
2. **ComputerUse / box browser**: not used (busy on Xiaohongshu), per instruction.
3. **OCR of hard-coded captions**: not used as ASR substitute.
4. Multiple clips are **BGM / visual montages** with little or no spoken narration → recorded as `no_speech` (empty `text`).

## Summary
- targeted detail videos: **18**
- spoken transcripts completed: **10**
- no_speech / unusable audio: **8**
- hard download failures: **0** (media reachable via public detail API for all 18)
- `posts.csv` `asr_path` filled: **10**

## Per-video (likes order)
### `7677935290225392369` — **ok** (likes=226, pinned=False)
- url: https://www.douyin.com/video/7677935290225392369
- files: `7677935290225392369.txt`, `7677935290225392369.json`
- chars: 176
- preview: 省级领导一行,历龄壹心托管 视察指导。领导先后查看了校区住宿管理和食品安全工作。住宿方面,仔细查看了

### `7575856001335147953` — **ok** (likes=166, pinned=False)
- url: https://www.douyin.com/video/7575856001335147953
- files: `7575856001335147953.txt`, `7575856001335147953.json`
- chars: 75
- preview: 济南壹壹托管界的天花板来了,三棵三树,酒店式四树,全透明厨房,看着见得干净,太空舱宿舍独立又私密,大

### `7637491112080667633` — **ok** (likes=94, pinned=False)
- url: https://www.douyin.com/video/7637491112080667633
- files: `7637491112080667633.txt`, `7637491112080667633.json`
- chars: 46
- preview: 这是我们的水池，这是咱们的灶台、工作台。咱们的立下全部都分为别类签到标签了，冷冻区、冷藏区。

### `7664065982533590181` — **no_speech** (likes=90, pinned=False)
- url: https://www.douyin.com/video/7664065982533590181
- files: `7664065982533590181.txt`, `7664065982533590181.json`
- note: no reliable spoken audio; empty transcript kept for schema

### `7525763465560313146` — **ok** (likes=48, pinned=False)
- url: https://www.douyin.com/video/7525763465560313146
- files: `7525763465560313146.txt`, `7525763465560313146.json`
- chars: 181
- preview: 我们是壹心托管，济南店。我们的位置在中海国际A5地块九曲便利市场内。我们几名全海学校,步行一分钟即可

### `7520469530099993914` — **no_speech** (likes=37, pinned=False)
- url: https://www.douyin.com/video/7520469530099993914
- files: `7520469530099993914.txt`, `7520469530099993914.json`
- note: no reliable spoken audio; empty transcript kept for schema

### `7653846998802236337` — **ok** (likes=31, pinned=True)
- url: https://www.douyin.com/video/7653846998802236337
- files: `7653846998802236337.txt`, `7653846998802236337.json`
- chars: 15
- preview: 壹心只做一件事，用心做好一件事

### `7674214245349730545` — **no_speech** (likes=31, pinned=False)
- url: https://www.douyin.com/video/7674214245349730545
- files: `7674214245349730545.txt`, `7674214245349730545.json`
- note: no reliable spoken audio; empty transcript kept for schema

### `7678673116122259579` — **ok** (likes=30, pinned=False)
- url: https://www.douyin.com/video/7678673116122259579
- files: `7678673116122259579.txt`, `7678673116122259579.json`
- chars: 261
- preview: 我们开托管,但不是所有孩子都收。各位家长,说句实在话,在我们壹心,不是所有的孩子我们都收。我们挑学生

### `7527685990393400634` — **ok** (likes=30, pinned=False)
- url: https://www.douyin.com/video/7527685990393400634
- files: `7527685990393400634.txt`, `7527685990393400634.json`
- chars: 229
- preview: 什麽托管，壹心托管，这里是我们的家长休息区，温馨舒适，让等待变得不再粗糙，什麽托管，壹心托管，这里是

### `7676858717410167473` — **no_speech** (likes=29, pinned=False)
- url: https://www.douyin.com/video/7676858717410167473
- files: `7676858717410167473.txt`, `7676858717410167473.json`
- note: no reliable spoken audio; empty transcript kept for schema

### `7684511595175017209` — **no_speech** (likes=19, pinned=False)
- url: https://www.douyin.com/video/7684511595175017209
- files: `7684511595175017209.txt`, `7684511595175017209.json`
- note: no reliable spoken audio; empty transcript kept for schema

### `7682957097429101681` — **ok** (likes=18, pinned=False)
- url: https://www.douyin.com/video/7682957097429101681
- files: `7682957097429101681.txt`, `7682957097429101681.json`
- chars: 94
- preview: 爸爸﹑妈妈﹑我们自己都可以哦。开学第二周了﹑一切井然有序﹑排队扫脸﹑自助取餐﹑就餐﹑光盘是我们对厨师

### `7675698430941783409` — **ok** (likes=14, pinned=False)
- url: https://www.douyin.com/video/7675698430941783409
- files: `7675698430941783409.txt`, `7675698430941783409.json`
- chars: 222
- preview: 怎麽样让孩子从被动到主动,很多家长说靠管,在我们壹心靠的是用心赞美三步法。陪伴的真相是孩子不是被管出

### `7675336617532168185` — **ok** (likes=14, pinned=False)
- url: https://www.douyin.com/video/7675336617532168185
- files: `7675336617532168185.txt`, `7675336617532168185.json`
- chars: 99
- preview: 妈妈，我想来壹心,你看餐厅这么大,大家可以在这里取餐,在大餐厅吃,教室也宽敞,还有个读书宝地,这么些

### `7682957063013705841` — **no_speech** (likes=13, pinned=False)
- url: https://www.douyin.com/video/7682957063013705841
- files: `7682957063013705841.txt`, `7682957063013705841.json`
- note: no reliable spoken audio; empty transcript kept for schema

### `7677898834409175729` — **no_speech** (likes=12, pinned=False)
- url: https://www.douyin.com/video/7677898834409175729
- files: `7677898834409175729.txt`, `7677898834409175729.json`
- note: no reliable spoken audio; empty transcript kept for schema

### `7683668880833902757` — **no_speech** (likes=6, pinned=False)
- url: https://www.douyin.com/video/7683668880833902757
- files: `7683668880833902757.txt`, `7683668880833902757.json`
- note: no reliable spoken audio; empty transcript kept for schema

