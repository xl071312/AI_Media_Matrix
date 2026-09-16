#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Issue #2 acceptance layout + master tables. Collect/structure only; no ranking."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW_PT = "2026-09-16 00:20 PT"
NOW_ISO = "2026-09-16T00:20:00-07:00"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def utf8_sig_writer(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in fieldnames})


def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def norm_name(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[\s\-_/\\|·•（）()【】\[\]「」『』“”\"'`,.，。、！!？?：:；;]", "", s)
    for tok in ["托管中心", "托管服务中心", "校外托管", "托辅中心", "托教中心", "小饭桌", "托管", "托教", "托辅", "济南市", "济南", "槐荫区", "市中区"]:
        s = s.replace(tok.lower() if tok.isascii() else tok, "")
        s = s.replace(tok, "")
    # re-run after Chinese removals (norm is mixed)
    for tok in ["托管中心", "托管服务中心", "校外托管", "托辅中心", "托教中心", "小饭桌", "托管", "托教", "托辅", "济南市", "济南", "槐荫区", "市中区"]:
        s = s.replace(tok, "")
    return s


def stable_id(prefix: str, *parts: str) -> str:
    raw = "|".join((p or "").strip() for p in parts)
    h = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}_{h}"


def brand_core(name: str) -> str:
    n = (name or "").strip()
    n = re.sub(r"[（(].*?[）)]", "", n)
    for tok in ["托管中心", "校外托管服务中心", "托辅中心", "托教中心", "小饭桌", "托管", "托教", "托辅"]:
        n = n.replace(tok, "")
    return n.strip()


SCHOOL_AREAS = [
    {
        "school_area_id": "area_yingdong",
        "school_area_name": "营东/营市东街片区",
        "school_aliases": ["营东小学", "营市东街小学", "济南市营市东街小学", "营市街"],
        "near_school_keys": ["济南市营市东街小学"],
    },
    {
        "school_area_id": "area_huaiyin_shiyan",
        "school_area_name": "槐荫实验片区",
        "school_aliases": ["槐荫实验", "槐荫区实验学校", "济南市槐荫区实验学校", "保利实验"],
        "near_school_keys": ["济南市槐荫区实验学校"],
    },
    {
        "school_area_id": "area_yangliu",
        "school_area_name": "杨柳春风片区",
        "school_aliases": ["杨柳春风", "杨柳春风学校", "济南市槐荫区杨柳春风学校", "绿城育华杨柳春风"],
        "near_school_keys": ["济南市槐荫区杨柳春风学校"],
    },
    {
        "school_area_id": "area_quanxin",
        "school_area_name": "泉新学校片区",
        "school_aliases": ["泉新", "泉新学校", "济南市槐荫区泉新学校"],
        "near_school_keys": ["济南市槐荫区泉新学校"],
    },
    {
        "school_area_id": "area_quanjing",
        "school_area_name": "泉景片区",
        "school_aliases": ["泉景", "泉景园", "绿地泉景园", "泉景中学", "泉景小学"],
        # 泉景 overlaps 泉新 catchment; count POIs whose address/near_school mentions 泉景
        "near_school_keys": ["济南市槐荫区泉新学校"],
        "address_hint": "泉景",
    },
]


def map_school_area(near_school: str, address: str = "", text: str = "") -> str:
    blob = " ".join([near_school or "", address or "", text or ""])
    if any(k in blob for k in ["营市东街", "营东", "营市街"]):
        return "area_yingdong"
    if any(k in blob for k in ["槐荫区实验", "槐荫实验", "保利实验"]):
        return "area_huaiyin_shiyan"
    if "杨柳春风" in blob:
        return "area_yangliu"
    if "泉新" in blob:
        return "area_quanxin"
    if "泉景" in blob:
        return "area_quanjing"
    if "医学中心" in blob:
        return "area_yixue"  # extra bucket, not in required 5
    if "泉海" in blob:
        return "area_quanhai"
    return ""


# ---------------------------------------------------------------------------
# 1) Directory layout
# ---------------------------------------------------------------------------

NEW_DIRS = [
    "00_manifest",
    "01_official_registry",
    "02_institutions_master",
    "03_douyin_target",
    "04_douyin_competitors",
    "05_xiaohongshu",
    "06_maps_reviews",
    "07_recruitment",
    "08_raw_screenshots",
    "09_transcripts",
    "10_evidence",
]

MIGRATIONS = [
    # (new_name, old_name) — copy/symlink content; keep old
    ("03_douyin_target", "01_douyin_target"),
    ("04_douyin_competitors", "02_douyin_competitors"),
    ("05_xiaohongshu", "03_xiaohongshu"),
    ("06_maps_reviews", "04_maps_reviews"),
    ("07_recruitment", "11_labor"),
    ("08_raw_screenshots", "05_raw_screenshots"),
    ("09_transcripts", "06_transcripts"),
]


def ensure_layout():
    for d in NEW_DIRS:
        (ROOT / d).mkdir(parents=True, exist_ok=True)

    for new, old in MIGRATIONS:
        src = ROOT / old
        dst = ROOT / new
        dst.mkdir(parents=True, exist_ok=True)
        if not src.exists():
            continue
        # Mirror: for each top-level entry in old, ensure present in new via symlink if absent
        for item in src.iterdir():
            target = dst / item.name
            if target.exists() or target.is_symlink():
                continue
            try:
                os.symlink(os.path.relpath(item, dst), target)
            except OSError:
                if item.is_dir():
                    shutil.copytree(item, target, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, target)

    # Also symlink whole-folder markers for clarity
    readme_map = ROOT / "00_manifest" / "directory_migration.md"
    lines = [
        "# Directory migration (Issue #2)",
        "",
        f"- generated_at_pt: {NOW_PT}",
        "- old folders retained for continuity",
        "- new folders contain symlinks (or copies) into old content",
        "",
        "| New | Old |",
        "|-----|-----|",
    ]
    for new, old in MIGRATIONS:
        lines.append(f"| `{new}/` | `{old}/` |")
    lines += [
        "",
        "| New | Notes |",
        "|-----|-------|",
        "| `01_official_registry/` | Laiwu roster analog + Huaiyin gap note |",
        "| `02_institutions_master/` | institutions.csv seed + match notes |",
        "| `10_evidence/` | evidence_index.csv + key pointer files |",
    ]
    readme_map.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# 2) Official registry
# ---------------------------------------------------------------------------

def build_official_registry(failures: list):
    reg = ROOT / "01_official_registry"
    note = {
        "topic": "槐荫区证照齐全校外托管机构名单",
        "status": "not_found",
        "failure_reason": "公开检索未发现济南市/槐荫区市场监管《证照齐全校外托管机构名单》Excel/PDF（含传闻2026-03槐荫Excel）。不得用培训机构黑白名单冒充托管名单。",
        "analog_reference": {
            "jurisdiction": "济南市莱芜区",
            "title": "莱芜区证照齐全校外托管机构名单",
            "count_claimed": "109家（供餐83/不供餐26）",
            "note": "仅作同市参照格式/量级，不可当作槐荫母表。",
            "source_url": "https://www.163.com/dy/article/L5L1ALOU0534DDHN.html",
            "local_path": "07_gov/raw/laiwu_163_roster.html",
            "also_mirrored": "01_official_registry/laiwu_roster_analog_note.md",
        },
        "scrape_date_pt": "2026-09-16",
    }
    (reg / "huaiyin_tuoguan_roster_gap.json").write_text(
        json.dumps(note, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (reg / "laiwu_roster_analog_note.md").write_text(
        "\n".join(
            [
                "# 莱芜区证照齐全校外托管机构名单（参照模拟，非槐荫母表）",
                "",
                "- **用途：** Issue #2 要求官方机构母表；槐荫/济南市级托管证照名单未公开找到。",
                "- **参照：** 同市莱芜区市场监管局公示约 109 家（供餐 83 / 不供餐 26）。",
                "- **来源：** https://www.163.com/dy/article/L5L1ALOU0534DDHN.html",
                "- **本地：** `07_gov/raw/laiwu_163_roster.html`（网易转载，无原始 Excel 附件）",
                "- **约束：** 不得把该名单并入槐荫 institutions 确认母表；仅登记为 registry 缺口说明。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    # symlink laiwu html if possible
    src = ROOT / "07_gov" / "raw" / "laiwu_163_roster.html"
    dst = reg / "laiwu_163_roster.html"
    if src.exists() and not dst.exists():
        try:
            os.symlink(os.path.relpath(src, reg), dst)
        except OSError:
            shutil.copy2(src, dst)

    # copy findings excerpt
    findings = ROOT / "07_gov" / "findings.jsonl"
    if findings.exists():
        shutil.copy2(findings, reg / "gov_findings.jsonl")

    failures.append(
        {
            "failure_id": "fail_huaiyin_tuoguan_roster",
            "area": "01_official_registry",
            "target": "槐荫区/济南市证照齐全校外托管机构名单 Excel/PDF",
            "failure_reason": note["failure_reason"],
            "source_attempted": "web_search + huaiyin.gov.cn + jnedu + 163 analog",
            "recorded_at": NOW_ISO,
        }
    )
    return note


# ---------------------------------------------------------------------------
# 3) Institutions master from POI + dianping + douyin candidates
# ---------------------------------------------------------------------------

def build_institutions():
    institutions = {}  # institution_id -> row
    unresolved = []
    name_index = {}  # norm_name -> institution_id

    def upsert_inst(**kwargs):
        name = kwargs.get("brand_name") or kwargs.get("official_name") or ""
        addr = kwargs.get("address") or ""
        # try merge by normalized name (+ soft address)
        key_n = norm_name(name)
        iid = None
        if key_n and key_n in name_index:
            iid = name_index[key_n]
            # merge non-empty fields
            row = institutions[iid]
            for k, v in kwargs.items():
                if v and not row.get(k):
                    row[k] = v
                elif k == "source_urls" and v:
                    existing = set(filter(None, (row.get("source_urls") or "").split("|")))
                    existing.update(filter(None, v.split("|")))
                    row["source_urls"] = "|".join(sorted(existing))
                elif k == "near_schools" and v:
                    existing = set(filter(None, (row.get("near_schools") or "").split("|")))
                    existing.update(filter(None, v.split("|")))
                    row["near_schools"] = "|".join(sorted(existing))
            return iid
        iid = kwargs.get("institution_id") or stable_id("inst", name, addr or kwargs.get("platform_poi_id") or "")
        kwargs["institution_id"] = iid
        institutions[iid] = kwargs
        if key_n:
            name_index[key_n] = iid
        return iid

    # --- POI (baidu/gaode bendibao/haoweizhi seeds) ---
    pois = read_csv(ROOT / "poi.csv")
    poi_out = []
    for p in pois:
        name = (p.get("name") or "").strip()
        if not name:
            continue
        addr = (p.get("address") or "").strip()
        near = (p.get("near_school") or "").strip()
        area = map_school_area(near, addr)
        iid = upsert_inst(
            institution_id=stable_id("inst", name, addr or p.get("poi_id") or ""),
            official_name="",
            brand_name=name,
            brand_short=brand_core(name),
            district="槐荫区" if "槐荫" in (addr + near) else ("市中区" if "市中" in (addr + near) else ""),
            address=addr,
            phone=(p.get("phone") or "").strip(),
            lat=p.get("lat") or "",
            lng=p.get("lng") or "",
            near_schools=near,
            school_area_id=area,
            source_type="map_list",
            source_urls=(p.get("url") or ""),
            screenshot_path="",
            verification_status="unverified_public_list",
            match_confidence="A" if addr else "B",
            notes=f"seeded_from_poi; platform={p.get('platform')}; search_query={p.get('search_query')}",
            platform_poi_id=p.get("poi_id") or "",
            collected_at=p.get("collected_at") or "",
        )
        poi_row = dict(p)
        poi_row["institution_id"] = iid
        poi_row["school_area_id"] = area
        poi_row["match_confidence"] = "A" if addr else "B"
        poi_row["source_type"] = "map_list"
        poi_row["verification_status"] = "unverified_public_list"
        poi_out.append(poi_row)

    # --- Dianping shops ---
    dp_pois = read_csv(ROOT / "04_maps_reviews" / "dianping" / "poi.csv")
    # also under new path
    if not dp_pois:
        dp_pois = read_csv(ROOT / "06_maps_reviews" / "dianping" / "poi.csv")

    TUOGUAN_HINTS = ("托管", "托教", "托辅", "小饭桌", "安亲", "伴学", "托育")
    # tutoring-only brands without托管 keywords stay candidates at B/C carefully
    for d in dp_pois:
        name = (d.get("merchant_name") or "").strip()
        if not name:
            continue
        addr = (d.get("address") or "").strip()
        ctx = (d.get("target_school_context") or "").strip()
        area = map_school_area(ctx, addr, name)
        is_tuoguanish = any(h in name or h in (d.get("service_category") or "") for h in TUOGUAN_HINTS)
        # merge if same brand already from POI
        conf = "A" if (addr and is_tuoguanish) else ("B" if is_tuoguanish else "C")
        if conf == "C":
            unresolved.append(
                {
                    "unresolved_id": stable_id("unres", "dianping", d.get("merchant_id") or name),
                    "candidate_name": name,
                    "platform": "dianping",
                    "platform_id": d.get("merchant_id") or "",
                    "url": d.get("url") or "",
                    "near_context": ctx,
                    "address": addr,
                    "match_confidence": "C",
                    "reason": "大众点评列表命中但主要为课后辅导/非强托管证据，或缺少地址；不并入确认机构",
                    "source_type": "dianping_search_list",
                    "screenshot_path": "",
                    "collected_at": d.get("scrape_date") or "",
                }
            )
            # still add to poi_out as unmatched poi-like row? keep in unresolved only
            continue
        iid = upsert_inst(
            institution_id=stable_id("inst", name, addr or d.get("merchant_id") or ""),
            official_name="",
            brand_name=name,
            brand_short=brand_core(name),
            district="",
            address=addr,
            phone="",
            lat="",
            lng="",
            near_schools=ctx,
            school_area_id=area,
            source_type="dianping",
            source_urls=d.get("url") or "",
            screenshot_path="",
            verification_status="public_listing_only" if "blocked" in (d.get("notes") or "") else "unverified_public_detail",
            match_confidence=conf,
            notes=(d.get("notes") or "")[:500],
            platform_poi_id=d.get("merchant_id") or "",
            rating=d.get("rating") or "",
            review_count=d.get("review_count") or "",
            collected_at=d.get("scrape_date") or "",
        )
        poi_out.append(
            {
                "platform": "dianping",
                "poi_id": d.get("merchant_id") or "",
                "name": name,
                "address": addr,
                "lat": "",
                "lng": "",
                "distance_text": d.get("distance_to_school") or "",
                "phone": "",
                "rating": d.get("rating") or "",
                "review_count": d.get("review_count") or "",
                "price_text": d.get("price_per_person_rmb") or "",
                "open_status": d.get("hours") or "",
                "near_school": ctx,
                "search_query": "dianping 托管/小饭桌 槐荫",
                "url": d.get("url") or "",
                "images_paths": "",
                "collected_at": d.get("scrape_date") or "",
                "institution_id": iid,
                "school_area_id": area,
                "match_confidence": conf,
                "source_type": "dianping",
                "verification_status": "unverified_public_list",
            }
        )

    # --- Douyin target + competitors as candidate institutions ---
    accounts = read_csv(ROOT / "accounts.csv")
    institution_accounts = []
    accounts_out = []

    JINAN_HINTS = ("济南", "槐荫", "营市", "营东", "泉景", "泉新", "杨柳", "西客站", "医学中心", "胜利大街")
    INST_NAME_HINTS = ("托管", "托教", "托辅", "小饭桌", "安亲", "伴学", "壹心")

    for a in accounts:
        nick = (a.get("nickname") or "").strip()
        kw = (a.get("source_keyword") or "").strip()
        bio = (a.get("bio") or "").strip()
        notes = (a.get("notes") or "").strip()
        blob = " ".join([nick, kw, bio, notes, a.get("region") or ""])
        aid = a.get("account_id") or ""
        url = a.get("url") or ""

        is_yixin = "壹心" in nick
        looks_jinan = any(h in blob for h in JINAN_HINTS) or is_yixin
        looks_inst = any(h in nick for h in INST_NAME_HINTS) or is_yixin

        area = map_school_area(kw, "", nick + bio)

        if is_yixin:
            conf = "B"  # strong brand account but address/phone not publicly shown on profile
            reason = "指定目标抖音账号；主页可见昵称/粉丝/作品，但公开电话与精确门店地址未展示，故 match_confidence=B（非官方工商核验）"
            iid = upsert_inst(
                institution_id=stable_id("inst", "壹心托管济南校区", "douyin"),
                official_name="",
                brand_name="壹心托管济南校区",
                brand_short="壹心托管",
                district="济南",
                address="",
                phone="",
                lat="",
                lng="",
                near_schools=kw,
                school_area_id=area or "",
                source_type="douyin_profile",
                source_urls=url,
                screenshot_path="08_raw_screenshots/profile_full_01.png",
                verification_status="public_profile_unverified_address",
                match_confidence=conf,
                notes=reason,
                platform_poi_id="",
                collected_at=a.get("collected_at") or "",
            )
            institution_accounts.append(
                {
                    "institution_id": iid,
                    "platform": "douyin",
                    "account_id": aid,
                    "nickname": nick,
                    "url": url,
                    "match_confidence": conf,
                    "match_reason": reason,
                    "role_guess": "brand_or_campus_account",
                    "source_type": "douyin_profile",
                    "screenshot_path": "08_raw_screenshots/profile_full_01.png",
                    "verification_status": "public_visible",
                    "collected_at": a.get("collected_at") or "",
                }
            )
        elif looks_jinan and looks_inst:
            # try link to existing POI institution by brand overlap
            core = norm_name(nick)
            linked = None
            for nkey, iid0 in name_index.items():
                if not nkey or not core:
                    continue
                if nkey in core or core in nkey or brand_core(nick) and brand_core(nick) in (institutions[iid0].get("brand_name") or ""):
                    # require some overlap length
                    if len(nkey) >= 2 and (nkey in core or core in nkey):
                        linked = iid0
                        break
            if linked:
                conf = "B"
                reason = "抖音昵称与已有 POI/列表品牌弱匹配（名称重叠）；缺电话/地址双强证据，故 B"
                institutions[linked]["source_urls"] = "|".join(
                    sorted(
                        set(filter(None, (institutions[linked].get("source_urls") or "").split("|") + [url]))
                    )
                )
                institution_accounts.append(
                    {
                        "institution_id": linked,
                        "platform": "douyin",
                        "account_id": aid,
                        "nickname": nick,
                        "url": url,
                        "match_confidence": conf,
                        "match_reason": reason,
                        "role_guess": "possible_brand_or_teacher_account",
                        "source_type": "douyin_search",
                        "screenshot_path": "",
                        "verification_status": "unverified",
                        "collected_at": a.get("collected_at") or "",
                    }
                )
            else:
                # create candidate institution at B if nickname clearly 济南+托管 brand-like
                conf = "B"
                reason = "济南相关关键词搜索命中的托管向抖音账号；无门店地址/电话强一致证据，作为候选机构 B"
                iid = upsert_inst(
                    institution_id=stable_id("inst", nick, "douyin", aid),
                    official_name="",
                    brand_name=nick,
                    brand_short=brand_core(nick),
                    district="济南" if "济南" in blob else ("槐荫区" if "槐荫" in blob else ""),
                    address="",
                    phone="",
                    lat="",
                    lng="",
                    near_schools=kw,
                    school_area_id=area,
                    source_type="douyin_search",
                    source_urls=url,
                    screenshot_path="",
                    verification_status="candidate_social_only",
                    match_confidence=conf,
                    notes=reason,
                    platform_poi_id="",
                    collected_at=a.get("collected_at") or "",
                )
                institution_accounts.append(
                    {
                        "institution_id": iid,
                        "platform": "douyin",
                        "account_id": aid,
                        "nickname": nick,
                        "url": url,
                        "match_confidence": conf,
                        "match_reason": reason,
                        "role_guess": "candidate_account",
                        "source_type": "douyin_search",
                        "screenshot_path": "",
                        "verification_status": "unverified",
                        "collected_at": a.get("collected_at") or "",
                    }
                )
        else:
            # C-level or out-of-scope → unresolved only
            unresolved.append(
                {
                    "unresolved_id": stable_id("unres", "douyin", aid or nick),
                    "candidate_name": nick,
                    "platform": "douyin",
                    "platform_id": aid,
                    "url": url,
                    "near_context": kw,
                    "address": "",
                    "match_confidence": "C",
                    "reason": "抖音搜索命中但缺少济南门店强证据，或非托管机构主体；仅名称/内容相关，不并入确认机构",
                    "source_type": "douyin_search",
                    "screenshot_path": "",
                    "collected_at": a.get("collected_at") or "",
                }
            )

        # always keep account row
        a2 = dict(a)
        a2["institution_id"] = ""
        # fill if linked
        for ia in institution_accounts:
            if ia["account_id"] == aid:
                a2["institution_id"] = ia["institution_id"]
                a2["match_confidence"] = ia["match_confidence"]
                break
        else:
            a2["match_confidence"] = "C"
        accounts_out.append(a2)

    # Write institutions master
    inst_fields = [
        "institution_id",
        "official_name",
        "brand_name",
        "brand_short",
        "district",
        "address",
        "phone",
        "lat",
        "lng",
        "near_schools",
        "school_area_id",
        "source_type",
        "source_urls",
        "screenshot_path",
        "verification_status",
        "match_confidence",
        "rating",
        "review_count",
        "platform_poi_id",
        "notes",
        "collected_at",
    ]
    inst_rows = []
    for iid, row in institutions.items():
        if row.get("match_confidence") == "C":
            # should not happen for confirmed table
            unresolved.append(
                {
                    "unresolved_id": stable_id("unres", "inst", iid),
                    "candidate_name": row.get("brand_name") or "",
                    "platform": row.get("source_type") or "",
                    "platform_id": row.get("platform_poi_id") or "",
                    "url": (row.get("source_urls") or "").split("|")[0],
                    "near_context": row.get("near_schools") or "",
                    "address": row.get("address") or "",
                    "match_confidence": "C",
                    "reason": "C级未并入确认表",
                    "source_type": row.get("source_type") or "",
                    "screenshot_path": row.get("screenshot_path") or "",
                    "collected_at": row.get("collected_at") or "",
                }
            )
            continue
        inst_rows.append(row)

    # dedupe unresolved by unresolved_id
    seen_u = set()
    unresolved_dedup = []
    for u in unresolved:
        if u["unresolved_id"] in seen_u:
            continue
        seen_u.add(u["unresolved_id"])
        unresolved_dedup.append(u)

    return {
        "institutions": inst_rows,
        "inst_fields": inst_fields,
        "institution_accounts": institution_accounts,
        "accounts_out": accounts_out,
        "poi_out": poi_out,
        "unresolved": unresolved_dedup,
        "institutions_by_id": {r["institution_id"]: r for r in inst_rows},
    }


# ---------------------------------------------------------------------------
# 4) Other tables
# ---------------------------------------------------------------------------

def build_posts_comments():
    posts = read_csv(ROOT / "posts.csv")
    comments = read_csv(ROOT / "comments.csv")
    # enrich dianping comments into comments.csv if not already
    dp_c = read_csv(ROOT / "04_maps_reviews" / "dianping" / "comments.csv")
    existing_ids = {(c.get("platform"), c.get("comment_id") or c.get("content") or c.get("comment_text")) for c in comments}
    for d in dp_c:
        cid = f"dp_{d.get('merchant_id')}_{hashlib.sha1((d.get('comment_text') or '').encode()).hexdigest()[:8]}"
        key = ("dianping", cid)
        if key in existing_ids:
            continue
        comments.append(
            {
                "platform": "dianping",
                "post_id": d.get("merchant_id") or "",
                "comment_id": cid,
                "author": d.get("parent_nickname") or "",
                "content": d.get("comment_text") or "",
                "likes": "",
                "is_author_reply": "0",
                "parent_id": "",
                "collected_at": d.get("scrape_date") or "",
                "source_url": d.get("url") or "",
                "merchant_name": d.get("merchant_name") or "",
            }
        )
    return posts, comments


def build_prices_services():
    prices = read_csv(ROOT / "prices.csv")
    services = read_csv(ROOT / "services.csv")
    dp_p = read_csv(ROOT / "04_maps_reviews" / "dianping" / "prices.csv")
    dp_s = read_csv(ROOT / "04_maps_reviews" / "dianping" / "services.csv")
    for d in dp_p:
        prices.append(
            {
                "platform": "dianping",
                "source_type": "group_buy_list",
                "source_id": d.get("merchant_id") or "",
                "account_or_poi": d.get("merchant_name") or "",
                "price_text": d.get("offer_text") or "",
                "price_value": d.get("price_rmb") or "",
                "unit": "元",
                "service_item": "团购/体验价(未核验有效期)",
                "grade_range": "",
                "raw_quote": d.get("offer_text") or "",
                "evidence_path": d.get("url") or "",
                "collected_at": d.get("scrape_date") or "",
                "verification_status": "unverified_listing",
                "notes": d.get("notes") or "",
            }
        )
    for d in dp_s:
        services.append(
            {
                "platform": "dianping",
                "source_type": "dianping_category",
                "source_id": d.get("merchant_id") or "",
                "account_or_poi": d.get("merchant_name") or "",
                "service_type": d.get("service_category") or "",
                "time_window": "",
                "lunch": "",
                "nap": "",
                "pickup": "",
                "homework": "",
                "teacher_student_ratio": "",
                "venue": d.get("business_area") or "",
                "promo": "",
                "trial": "",
                "pain_points": "",
                "pitch": "",
                "differentiator": "",
                "raw_quote": d.get("notes") or "",
                "evidence_path": d.get("url") or "",
                "collected_at": d.get("scrape_date") or "",
                "verification_status": "category_label_only",
            }
        )
    return prices, services


def build_recruitment():
    labor = read_csv(ROOT / "11_labor" / "labor.csv")
    rows = []
    for r in labor:
        rows.append(
            {
                "recruitment_id": r.get("id") or stable_id("job", r.get("url") or r.get("title") or ""),
                "source_platform": r.get("source_platform") or "",
                "url": r.get("url") or "",
                "title": r.get("title") or "",
                "salary_range": r.get("salary_range") or "",
                "work_hours": r.get("work_hours") or "",
                "requirements": r.get("requirements") or "",
                "company": r.get("company") or "",
                "company_district": r.get("company_district") or "",
                "institution_id": "",  # no strong match asserted
                "match_confidence": "C",
                "data_quality": r.get("data_quality") or "",
                "source_type": "job_board_public",
                "verification_status": "public_listing",
                "screenshot_path": "",
                "collected_at": r.get("scrape_date") or "",
                "notes": "招聘主体与目标托管机构未做强绑定；保留供人工匹配",
            }
        )
    return rows


def build_school_competition(inst_rows, poi_out, institution_accounts, accounts_out):
    # competitor counts from POI + linked accounts
    rows = []
    for area in SCHOOL_AREAS:
        aid = area["school_area_id"]
        # POI competitors
        if aid == "area_quanjing":
            poi_names = sorted(
                {
                    p.get("name")
                    for p in poi_out
                    if "泉景" in ((p.get("address") or "") + (p.get("near_school") or "") + (p.get("name") or ""))
                }
            )
        else:
            keys = set(area["near_school_keys"])
            poi_names = sorted(
                {
                    p.get("name")
                    for p in poi_out
                    if (p.get("near_school") in keys) or (p.get("school_area_id") == aid)
                }
            )
        # institutions in area
        inst_in = [i for i in inst_rows if i.get("school_area_id") == aid]
        # accounts whose source_keyword mentions aliases
        aliases = area["school_aliases"]
        acc_hits = []
        for a in accounts_out:
            blob = " ".join([a.get("nickname") or "", a.get("source_keyword") or "", a.get("notes") or ""])
            if any(al in blob for al in aliases):
                acc_hits.append(a.get("nickname") or a.get("account_id"))
        # also institution_accounts near
        ia_hits = [
            ia.get("nickname")
            for ia in institution_accounts
            if any(al in ((ia.get("match_reason") or "") + (ia.get("nickname") or "")) for al in aliases)
            or (institutions_area_id(inst_rows, ia.get("institution_id")) == aid)
        ]
        rows.append(
            {
                "school_area_id": aid,
                "school_area_name": area["school_area_name"],
                "school_aliases": "|".join(area["school_aliases"]),
                "poi_competitor_count": len(poi_names),
                "poi_competitor_names": "|".join(poi_names),
                "institution_master_count": len(inst_in),
                "social_account_hit_count": len(set(acc_hits)),
                "social_account_hit_names": "|".join(sorted(set(filter(None, acc_hits)))[:40]),
                "notes": "POI 计数来自 bendibao/地图列表启发式归属，非实时地理围栏；泉景与泉新存在学区重叠。",
                "source_type": "derived_from_poi_and_accounts",
                "verification_status": "heuristic",
                "collected_at": NOW_ISO,
            }
        )
    return rows


def institutions_area_id(inst_rows, iid):
    for i in inst_rows:
        if i.get("institution_id") == iid:
            return i.get("school_area_id") or ""
    return ""


def build_evidence_index(inst_pack):
    rows = []
    eid = 0

    def add(**kw):
        nonlocal eid
        eid += 1
        rows.append({"evidence_id": f"ev_{eid:04d}", **kw})

    # screenshots walk
    patterns = [
        ("08_raw_screenshots", ROOT / "05_raw_screenshots"),
        ("03_douyin_target/screenshots", ROOT / "01_douyin_target" / "screenshots"),
        ("04_douyin_competitors/screenshots", ROOT / "02_douyin_competitors" / "screenshots"),
        ("05_xiaohongshu/screenshots", ROOT / "03_xiaohongshu" / "screenshots"),
        ("06_maps_reviews/dianping/screenshots", ROOT / "04_maps_reviews" / "dianping" / "screenshots"),
    ]
    yixin_id = None
    for i in inst_pack["institutions"]:
        if "壹心" in (i.get("brand_name") or ""):
            yixin_id = i["institution_id"]
            break

    for logical, physical in patterns:
        if not physical.exists():
            continue
        for f in sorted(physical.iterdir()):
            if not f.is_file():
                continue
            if f.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
                continue
            rel = f"{logical}/{f.name}"
            iid = ""
            post_id = ""
            platform = ""
            if "壹心" in f.name or "profile_full" in f.name:
                iid = yixin_id or ""
                platform = "douyin"
            if "cover_" in f.name:
                m = re.search(r"cover_(\d+)", f.name)
                if m:
                    post_id = m.group(1)
                    platform = "douyin"
                    iid = yixin_id or ""
            if "任务6" in f.name or "xiaohongshu" in logical:
                platform = "xiaohongshu"
            if "任务2" in f.name or "dianping" in logical:
                platform = "dianping"
            if "任务7" in f.name:
                platform = "douyin"
            add(
                file_path=rel,
                file_type=f.suffix.lower().lstrip("."),
                platform=platform,
                institution_id=iid or "",
                post_id=post_id,
                account_id="82936373898" if iid == yixin_id and platform == "douyin" else "",
                description=f.name,
                source_type="screenshot",
                verification_status="raw_asset",
                collected_at=NOW_ISO,
            )

    # transcripts
    tdir = ROOT / "06_transcripts"
    if tdir.exists():
        for f in sorted(tdir.glob("*.txt")):
            pid = f.stem
            add(
                file_path=f"09_transcripts/{f.name}",
                file_type="txt",
                platform="douyin",
                institution_id=yixin_id or "",
                post_id=pid if pid.isdigit() else "",
                account_id="82936373898" if (yixin_id and pid.isdigit()) else "",
                description="ASR transcript",
                source_type="asr",
                verification_status="machine_transcript",
                collected_at=NOW_ISO,
            )

    # key raw jsonl
    for rel in [
        "06_maps_reviews/poi_raw.jsonl",
        "04_maps_reviews/poi_raw.jsonl",
        "07_gov/findings.jsonl",
        "11_labor/jobs.jsonl",
        "07_recruitment/jobs.jsonl",
    ]:
        p = ROOT / rel
        # also try without new prefix
        if not p.exists():
            continue
        add(
            file_path=rel,
            file_type="jsonl",
            platform="",
            institution_id="",
            post_id="",
            account_id="",
            description="raw structured dump",
            source_type="raw_dump",
            verification_status="raw_asset",
            collected_at=NOW_ISO,
        )

    return rows


def build_failures(extra):
    failures = list(extra)
    # from existing logs
    known = [
        {
            "failure_id": "fail_dianping_login_wall",
            "area": "06_maps_reviews/dianping",
            "target": "大众点评搜索/详情",
            "failure_reason": "登录墙/验证中心；部分列表可见，详情多数未展开",
            "source_attempted": "public URL + screenshots",
            "recorded_at": "2026-09-15T22:50:00-07:00",
        },
        {
            "failure_id": "fail_meituan_404",
            "area": "06_maps_reviews/meituan",
            "target": "美团公开搜索",
            "failure_reason": "HTTP 404/NoSuchKey；无公开列表卡片",
            "source_attempted": "public search URLs",
            "recorded_at": "2026-09-15T22:50:00-07:00",
        },
        {
            "failure_id": "fail_gaode_baidu_spa",
            "area": "06_maps_reviews",
            "target": "高德/百度地图详情",
            "failure_reason": "主要为 SPA 壳，详情字段不完整；bendibao/好位置列表作 POI 种子",
            "source_attempted": "m_search / pois_raw.json",
            "recorded_at": "2026-09-15T22:40:00-07:00",
        },
        {
            "failure_id": "fail_huaiyin_local_rules",
            "area": "01_official_registry / 07_gov",
            "target": "济南/槐荫《鲁政办发〔2026〕8号》实施细则",
            "failure_reason": "公开检索未见市级/区级专门实施细则/通知/Q&A",
            "source_attempted": "web_search + gov portals",
            "recorded_at": "2026-09-16T00:00:00-07:00",
        },
        {
            "failure_id": "fail_school_ops_details",
            "area": "07_gov",
            "target": "目标校放学/午休/配餐校级细则",
            "failure_reason": "校级细则普遍未公开",
            "source_attempted": "huaiyin.gov.cn school pages",
            "recorded_at": "2026-09-16T00:00:00-07:00",
        },
        {
            "failure_id": "fail_douyin_tongcheng",
            "area": "04_douyin_competitors",
            "target": "抖音同城入口",
            "failure_reason": "同城入口不可用；改用公开综合搜索；未登录绕过",
            "source_attempted": "douyin public search",
            "recorded_at": "2026-09-15T23:07:00-07:00",
        },
        {
            "failure_id": "fail_yixin_contact_price",
            "area": "03_douyin_target",
            "target": "壹心托管公开电话/价格/完整评论ASR",
            "failure_reason": "主页未展示公开电话与价格；评论/ASR/OCR 部分未完整",
            "source_attempted": "public profile + partial works",
            "recorded_at": "2026-09-16T05:36:00Z",
        },
    ]
    failures.extend(known)
    return failures


def write_readme(stats):
    text = f"""# 济南校外托管线上竞争情报采集包（Issue #2 验收布局）

> **角色边界：** GROK BOT 仅负责采集与结构化。本包**不做**竞品最终排名、**不做**开店结论。请 **ChatGPT / Sol** 基于原始 CSV、截图与 transcript 做商业分析。

- 生成时间（PT）：{NOW_PT}
- 仓库：`xl071312/AI_Media_Matrix`
- 目录：`research/jinan_tuoguan_2026/`

## 调研范围

- 地理焦点：济南市槐荫区（兼及市中区泉海参照）
- 学校/片区：营东/营市东街、槐荫实验、杨柳春风、泉新、泉景
- 平台：抖音（指定壹心 + 关键词竞品）、小红书、地图/本地宝/好位置、大众点评（部分）、招聘、政府公开页
- 约束：仅公开可见；不绕过登录/验证码；不发明字段

## 目录映射（新布局）

| 新目录 | 含义 | 旧目录（保留） |
|--------|------|----------------|
| `00_manifest/` | 清单、迁移说明、状态 | 同名 |
| `01_official_registry/` | 官方母表缺口说明 + 莱芜参照 | （新建） |
| `02_institutions_master/` | 机构主档副本 | （新建） |
| `03_douyin_target/` | 指定抖音壹心 | `01_douyin_target/` |
| `04_douyin_competitors/` | 抖音竞品搜索 | `02_douyin_competitors/` |
| `05_xiaohongshu/` | 小红书 | `03_xiaohongshu/` |
| `06_maps_reviews/` | 地图/点评 | `04_maps_reviews/` |
| `07_recruitment/` | 招聘 | `11_labor/` |
| `08_raw_screenshots/` | 截图汇总 | `05_raw_screenshots/` |
| `09_transcripts/` | ASR/文本 | `06_transcripts/` |
| `10_evidence/` | 证据索引 | （新建） |

旧目录 `07_gov` `08_xueyijia` `09_enterprise` `10_rent` `11_labor` `12_ai_eval_pack` 仍保留，供溯源。

## 根目录必交付 CSV / JSON

- `institutions.csv` — 机构主档（仅 A/B；C 级见 unresolved）
- `institution_accounts.csv` — 机构↔社媒账号匹配
- `accounts.csv` / `posts.csv` / `comments.csv`
- `prices.csv` / `services.csv` / `poi.csv`
- `recruitment.csv` / `school_competition.csv`
- `evidence_index.csv` / `unresolved_matches.csv` / `failures.csv`
- `manifest.json` / `README.md`

编码：UTF-8-SIG。

## 完成度 vs 失败项（摘要）

### 已完成（可分析）

- 抖音目标号「壹心托管济南校区」公开主页与部分作品/评论/ASR
- 抖音关键词竞品账号与作品合并表
- 小红书笔记与评论（公开可见）
- POI 种子（本地宝/好位置等）+ 片区密度启发式
- 大众点评部分商户列表/少量详情与评价（验证墙限制）
- 招聘公开岗位样本
- 政府侧：省级托管意见、槐荫培训白名单、目标校公开招生信息
- Issue #2 验收目录与主表主键/匹配置信度字段

### 失败 / 缺口（详见 failures.csv）

- **槐荫证照齐全托管名单 Excel：未找到**（莱芜名单仅作参照模拟）
- 济南/槐荫实施细则未找到
- 大众点评登录/验证墙；美团 404
- 高德/百度详情 SPA 壳
- 抖音同城入口不可用
- 壹心公开电话/标价未展示；部分 ASR/评论不完整
- 校级放学/午休/配餐细则普遍未公开

## 给 ChatGPT / Sol 的使用提示

1. 以 `institutions.csv` + `institution_accounts.csv` 为实体骨架；`match_confidence=A/B` 才可当较实事实，`C` 只在 `unresolved_matches.csv`。
2. 价格/服务必须回溯 `evidence_path` / `source_url` / `screenshot_path`；广告自述 ≠ 已验证。
3. `school_competition.csv` 是启发式计数，不是实地或 API 围栏普查。
4. **请你们输出排名/开店结论**；本包作者不输出。

## 统计快照

```json
{json.dumps(stats, ensure_ascii=False, indent=2)}
```
"""
    (ROOT / "README.md").write_text(text, encoding="utf-8")


def main():
    ensure_layout()
    failures = []
    build_official_registry(failures)

    pack = build_institutions()
    posts, comments = build_posts_comments()
    prices, services = build_prices_services()
    recruitment = build_recruitment()
    school_comp = build_school_competition(
        pack["institutions"], pack["poi_out"], pack["institution_accounts"], pack["accounts_out"]
    )
    evidence = build_evidence_index(pack)
    failures = build_failures(failures)

    # Write CSVs at root
    utf8_sig_writer(ROOT / "institutions.csv", pack["inst_fields"], pack["institutions"])
    utf8_sig_writer(
        ROOT / "02_institutions_master" / "institutions.csv",
        pack["inst_fields"],
        pack["institutions"],
    )

    ia_fields = [
        "institution_id",
        "platform",
        "account_id",
        "nickname",
        "url",
        "match_confidence",
        "match_reason",
        "role_guess",
        "source_type",
        "screenshot_path",
        "verification_status",
        "collected_at",
    ]
    utf8_sig_writer(ROOT / "institution_accounts.csv", ia_fields, pack["institution_accounts"])
    utf8_sig_writer(ROOT / "02_institutions_master" / "institution_accounts.csv", ia_fields, pack["institution_accounts"])

    acc_fields = list(pack["accounts_out"][0].keys()) if pack["accounts_out"] else [
        "platform", "account_id", "nickname", "unique_id", "url", "followers", "likes_total",
        "bio", "region", "contact", "source_keyword", "collected_at", "notes", "institution_id", "match_confidence",
    ]
    utf8_sig_writer(ROOT / "accounts.csv", acc_fields, pack["accounts_out"])

    post_fields = list(posts[0].keys()) if posts else []
    utf8_sig_writer(ROOT / "posts.csv", post_fields, posts)

    # unify comment fields
    c_fields = [
        "platform", "post_id", "comment_id", "author", "content", "likes",
        "is_author_reply", "parent_id", "collected_at", "source_url", "merchant_name",
    ]
    c_norm = []
    for c in comments:
        c_norm.append({
            "platform": c.get("platform") or "",
            "post_id": c.get("post_id") or c.get("note_id") or "",
            "comment_id": c.get("comment_id") or "",
            "author": c.get("author") or "",
            "content": c.get("content") or c.get("comment_text") or "",
            "likes": c.get("likes") or "",
            "is_author_reply": c.get("is_author_reply") or "",
            "parent_id": c.get("parent_id") or "",
            "collected_at": c.get("collected_at") or c.get("scrape_date") or "",
            "source_url": c.get("source_url") or c.get("url") or "",
            "merchant_name": c.get("merchant_name") or "",
        })
    utf8_sig_writer(ROOT / "comments.csv", c_fields, c_norm)

    price_fields = [
        "platform", "source_type", "source_id", "account_or_poi", "price_text", "price_value",
        "unit", "service_item", "grade_range", "raw_quote", "evidence_path", "collected_at",
        "verification_status", "notes",
    ]
    utf8_sig_writer(ROOT / "prices.csv", price_fields, prices)

    svc_fields = [
        "platform", "source_type", "source_id", "account_or_poi", "service_type", "time_window",
        "lunch", "nap", "pickup", "homework", "teacher_student_ratio", "venue", "promo", "trial",
        "pain_points", "pitch", "differentiator", "raw_quote", "evidence_path", "collected_at",
        "verification_status",
    ]
    utf8_sig_writer(ROOT / "services.csv", svc_fields, services)

    poi_fields = [
        "platform", "poi_id", "name", "address", "lat", "lng", "distance_text", "phone",
        "rating", "review_count", "price_text", "open_status", "near_school", "search_query",
        "url", "images_paths", "collected_at", "institution_id", "school_area_id",
        "match_confidence", "source_type", "verification_status",
    ]
    utf8_sig_writer(ROOT / "poi.csv", poi_fields, pack["poi_out"])
    # also under maps
    utf8_sig_writer(ROOT / "06_maps_reviews" / "poi.csv", poi_fields, pack["poi_out"])

    rec_fields = [
        "recruitment_id", "source_platform", "url", "title", "salary_range", "work_hours",
        "requirements", "company", "company_district", "institution_id", "match_confidence",
        "data_quality", "source_type", "verification_status", "screenshot_path", "collected_at", "notes",
    ]
    utf8_sig_writer(ROOT / "recruitment.csv", rec_fields, recruitment)
    utf8_sig_writer(ROOT / "07_recruitment" / "recruitment.csv", rec_fields, recruitment)

    sc_fields = [
        "school_area_id", "school_area_name", "school_aliases", "poi_competitor_count",
        "poi_competitor_names", "institution_master_count", "social_account_hit_count",
        "social_account_hit_names", "notes", "source_type", "verification_status", "collected_at",
    ]
    utf8_sig_writer(ROOT / "school_competition.csv", sc_fields, school_comp)

    un_fields = [
        "unresolved_id", "candidate_name", "platform", "platform_id", "url", "near_context",
        "address", "match_confidence", "reason", "source_type", "screenshot_path", "collected_at",
    ]
    utf8_sig_writer(ROOT / "unresolved_matches.csv", un_fields, pack["unresolved"])
    utf8_sig_writer(ROOT / "02_institutions_master" / "unresolved_matches.csv", un_fields, pack["unresolved"])

    ev_fields = [
        "evidence_id", "file_path", "file_type", "platform", "institution_id", "post_id",
        "account_id", "description", "source_type", "verification_status", "collected_at",
    ]
    utf8_sig_writer(ROOT / "evidence_index.csv", ev_fields, evidence)
    utf8_sig_writer(ROOT / "10_evidence" / "evidence_index.csv", ev_fields, evidence)

    fail_fields = ["failure_id", "area", "target", "failure_reason", "source_attempted", "recorded_at"]
    utf8_sig_writer(ROOT / "failures.csv", fail_fields, failures)
    utf8_sig_writer(ROOT / "00_manifest" / "failures.csv", fail_fields, failures)

    # counts
    douyin_posts = sum(1 for p in posts if p.get("platform") == "douyin")
    xhs_notes = sum(1 for p in posts if p.get("platform") == "xiaohongshu")
    map_reviews = sum(1 for c in c_norm if c.get("platform") in {"baidu", "dianping", "gaode", "meituan"})
    # also dianping review_count sum? Issue says 地图评论数 — count comment rows from maps
    confirmed_social = len({(ia["platform"], ia["account_id"]) for ia in pack["institution_accounts"] if ia.get("match_confidence") in {"A", "B"}})

    stats = {
        "institutions_total": len(pack["institutions"]),
        "confirmed_social_accounts": confirmed_social,
        "douyin_posts": douyin_posts,
        "xhs_notes": xhs_notes,
        "map_reviews": map_reviews,
        "unresolved_entities": len(pack["unresolved"]),
        "failures": len(failures),
        "poi_rows": len(pack["poi_out"]),
        "recruitment_rows": len(recruitment),
        "evidence_rows": len(evidence),
        "comments_total": len(c_norm),
        "accounts_total": len(pack["accounts_out"]),
        "school_areas": len(school_comp),
    }

    manifest = {
        "project": "jinan_tuoguan_2026",
        "issue": 2,
        "version": "v1_issue2_acceptance",
        "role": "GROK_BOT_collect_structure_only",
        "generated_at_pt": NOW_PT,
        "generated_at": NOW_ISO,
        "layout": "issue2_required",
        "dirs": NEW_DIRS,
        "migrations": [{ "new": n, "old": o} for n, o in MIGRATIONS],
        "counts": stats,
        "constraints": [
            "public_only",
            "no_auth_bypass",
            "utf8_sig_csv",
            "raw_assets_retained",
            "no_business_ranking",
            "no_open_store_conclusion",
            "C_matches_unresolved_only",
        ],
        "official_registry": {
            "huaiyin_tuoguan_roster": "not_found",
            "laiwu_analog_only": True,
            "note_path": "01_official_registry/huaiyin_tuoguan_roster_gap.json",
        },
        "handoff": "ChatGPT/Sol analyze; Grok Bot does not rank",
        "failure_reason_file": "failures.csv",
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "00_manifest" / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "10_evidence" / "README.md").write_text(
        "# 10_evidence\n\n见根目录 `evidence_index.csv`（本目录有副本）。\n链接 `institution_id` / `post_id` 尽可能填写；无强证据则留空。\n",
        encoding="utf-8",
    )

    write_readme(stats)

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    print("DONE", ROOT)


if __name__ == "__main__":
    main()
