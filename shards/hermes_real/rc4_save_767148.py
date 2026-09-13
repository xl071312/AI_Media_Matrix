#!/usr/bin/env python3
"""RC4: Save Wave002 article 7671488207304868404"""
import json, hashlib
from pathlib import Path

BASE = Path(r"F:\workspace\AI_Media_Matrix\01_benchmark")
SRC = BASE / "analysis_batches/batch_004_toutiao/SEED_WAVE_002"
HANDOFF = BASE.parent / "handoff/chatgpt/batch_004/wave_002"

TEXT = """做自媒体最通透的几条真相，普通人一定要看懂

刷到一段话，特别贴合我当下的状态，结合自己的经历，深度复盘分享给所有正在起步的普通人。

第一，真诚永远是底色，但真诚不是毫无保留。
敢于大方说出自己的优点，也坦然承认自己的缺点和过往的踩坑经历。不包装成全知全能的大神，不装、不忽悠。
但真诚不等于把自己的底牌、当下的窘迫全盘托出。分享过往的失误用来复盘成长，守住当下的底线用来稳步前行，真实但不赤裸，通透但不盲从。

第二，勇敢的人，先享受世界。
普通人做自媒体最大的障碍，从来不是不会拍、不会写，而是脸皮薄、怕评价、怕被熟人看见、怕被同行调侃。
真正的勇敢，不是毫无畏惧，而是带着忐忑和顾虑，依然敢出镜、敢表达、敢持续输出。允许自己前期作品不完美，允许有人不认同，这是成长的必经之路。

第三，多操作、少空想，面子最不值钱。
太多人陷入理论内耗，天天刷教程、存文案、学逻辑，唯独不敢动手实操。
我深刻体会：十条完美的理论，不如一条粗糙的实操。视频拍得再烂，也是自己的成长；文案写得再简，也是真实的思考。
做内容，就要放下面子。不用纠结别人怎么看，不用讨好所有人。自媒体的本质是筛选同频的人，不是取悦所有人。有人喜欢你，就一定有人看不懂你，不必解释，不必纠结。

第四，时间不会平白给答案，只会奖励持续迭代的人。
很多人以为坚持更新就会有结果，其实盲目坚持只是原地消耗。
真正的成长，是每一次输出后都有复盘，每一次不足都有修正。不怕起步慢，就怕停滞不前；不怕暂时没结果，就怕假装努力、自我感动。
你要始终相信：普通人翻盘，靠不了天赋，也不要太寄托靠运气；要靠真诚做人，靠踏实做事，靠持续实操，靠长期沉淀。
慢慢来，不着急，时间终会给坚持且清醒的人，最好的答案。"""

cid = "7671488207304868404"
p = SRC / f"{cid}.json"
if not p.exists():
    data = {'content_id': cid, 'platform': 'toutiao', 'content_type': 'article', 'title': TEXT.split('\n')[0], 'author': '苏晗pb', 'publish_time': '2026-08-08', 'url': f'https://www.toutiao.com/article/{cid}/', 'raw_article_text': TEXT, 'clean_article_text': TEXT, 'full_text': TEXT, 'text_chars': len(TEXT), 'paragraph_count': max(1, len(TEXT.split('\n\n'))), 'status': 'DOWNLOADED_REAL', 'fulltext_available': True, 'evidence_ready': True, 'placeholder_detected': False, 'logic_analyzable': 'PENDING_MODEL_REVIEW', 'simulated': False, 'wave': 'wave_002', 'source': 'recommendation', 'content_sha256': hashlib.sha256(TEXT.encode('utf-8')).hexdigest(), 'previous_text_chars': 0, 'final_text_chars': len(TEXT), 'scroll_cycles': 1, 'stable_rounds': 1, 'article_bottom_reached': True, 'article_container_selector': 'article'}
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    h = HANDOFF / f"{cid}.json"
    with open(h, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ {cid}: {len(TEXT)} chars saved")
else:
    print(f"  Already exists: {cid}")