#!/usr/bin/env python3
"""Phase C schema helpers: sentence split, skeleton, validate 25 fields."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path

ANALYZER_VERSION = "phase_c_v1"

FIELDS_25 = [
    "opening_move","claim_chain","logic_units","transition_language","contrast_method",
    "question_method","example_method","abstract_to_concrete","judgement_language",
    "self_correction","rhythm","spoken_markers","emotion_curve","closure_loop","cta_style",
    "anti_ai_signals","weakness","thought_process_exposure","listener_positioning",
    "concrete_anchor","information_density_curve","sentence_flow","viewpoint_personality",
    "memory_device","guanyu_transfer_value",
]

def split_sentences(text: str) -> list[dict]:
    text = text.replace("\r\n", "\n").strip()
    # Prefer newline blocks for ASR; also split on Chinese punctuation
    chunks = []
    for para in re.split(r"\n+", text):
        para = para.strip()
        if not para:
            continue
        parts = re.split(r"(?<=[。！？!?；;])\s*", para)
        for p in parts:
            p = p.strip()
            if p:
                chunks.append(p)
    if not chunks and text:
        chunks = [text]
    out = []
    for i, s in enumerate(chunks, 1):
        out.append({"sentence_id": f"s{i}", "char_len": len(s), "snippet": s[:80]})
        # keep full text separately keyed for analyzer use only in sidecar
    return out

def write_sentence_bank(work_id: str, sentences_full: list[str], bank_dir: Path) -> Path:
    bank_dir.mkdir(parents=True, exist_ok=True)
    p = bank_dir / f"{work_id}.sentences.json"
    data = [{"sentence_id": f"s{i}", "text": t} for i, t in enumerate(sentences_full, 1)]
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return p

def full_split(text: str) -> list[str]:
    text = text.replace("\r\n", "\n").strip()
    chunks = []
    for para in re.split(r"\n+", text):
        para = para.strip()
        if not para:
            continue
        parts = re.split(r"(?<=[。！？!?；;])\s*", para)
        for p in parts:
            p = p.strip()
            if p:
                chunks.append(p)
    return chunks or ([text] if text else [])

def empty_field(name: str) -> dict:
    if name == "guanyu_transfer_value":
        return {"decision": None, "reason": None, "evidence": []}
    if name == "logic_units":
        return {"units": []}
    if name == "spoken_markers":
        return {"status": None, "markers": [], "evidence": []}
    return {"summary": None, "patterns": [], "evidence": []}

def make_skeleton(row: dict, sentences_meta: list[dict]) -> dict:
    fields = {k: empty_field(k) for k in FIELDS_25}
    return {
        "creator_id": row["creator_id"],
        "work_id": row["work_id"],
        "modality": row["modality"],
        "source_url": row["source_url"],
        "source_sha256": row["source_sha256"],
        "performance_tier": row["performance_tier"],
        "spoken_marker_eligible": row["spoken_marker_eligible"],
        "analysis_status": "PENDING",
        "analyzer_version": ANALYZER_VERSION,
        "sentence_count": len(sentences_meta),
        "sentences_index": sentences_meta,  # id + snippet only
        "fields": fields,
        "evidence_sentence_ids": [],
        "fields_complete_25": False,
    }

def validate_record(rec: dict) -> tuple[bool, list[str]]:
    errs = []
    if rec.get("analysis_status") not in ("OK", "FAIL_AD", "FAIL_THIN", "FAIL_BAD_TRANSCRIPT"):
        errs.append("bad_status")
    fields = rec.get("fields") or {}
    for k in FIELDS_25:
        if k not in fields:
            errs.append(f"missing_field:{k}")
            continue
        v = fields[k]
        if not isinstance(v, dict):
            errs.append(f"field_not_dict:{k}")
            continue
        if k == "spoken_markers":
            sme = rec.get("spoken_marker_eligible")
            if sme in ("NO", "N/A_TEXT") and v.get("status") not in ("SKIPPED_INELIGIBLE", "N/A_TEXT_MODALITY"):
                # allow analyzed but must not claim frequency stats
                if v.get("status") == "FREQ_COMPUTED":
                    errs.append("spoken_markers_freq_on_ineligible")
            continue
        if k == "guanyu_transfer_value":
            if v.get("decision") not in ("KEEP", "ADAPT", "REJECT", None):
                errs.append("bad_transfer_decision")
            if rec.get("analysis_status") == "OK" and not v.get("decision"):
                errs.append("transfer_empty")
            continue
        if k == "logic_units":
            if rec.get("analysis_status") == "OK" and not v.get("units"):
                errs.append("logic_units_empty")
            continue
        if rec.get("analysis_status") == "OK":
            if not v.get("summary") and not v.get("patterns") and not v.get("evidence"):
                errs.append(f"empty_field:{k}")
            # evidence should cite sentence ids when present
            ev = v.get("evidence") or []
            for e in ev:
                if not e.get("sentence_id"):
                    errs.append(f"evidence_no_sid:{k}")
                    break
    complete = len(errs) == 0 and rec.get("analysis_status") == "OK"
    return complete, errs
