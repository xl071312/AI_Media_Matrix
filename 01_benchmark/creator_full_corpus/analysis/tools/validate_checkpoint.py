#!/usr/bin/env python3
import csv, json, sys
from pathlib import Path
from collections import Counter, defaultdict

FIELDS_25 = json.loads(Path('/workspace/AI_Media_Matrix/01_benchmark/creator_full_corpus/analysis/tools/FIELDS_25.json').read_text())
analysis = Path('/workspace/AI_Media_Matrix/01_benchmark/creator_full_corpus/analysis')
deep = analysis/'deep_items'

def load_done():
    files=list(deep.glob('*/*.json'))
    recs=[]
    for f in files:
        try:
            recs.append(json.loads(f.read_text()))
        except Exception as e:
            recs.append({'_path':str(f),'_error':str(e)})
    return recs

def validate_one(rec):
    errs=[]
    if rec.get('_error'):
        return False, [rec['_error']]
    if rec.get('analysis_status')!='OK':
        errs.append('status!='+str(rec.get('analysis_status')))
    fields=rec.get('fields') or {}
    for k in FIELDS_25:
        if k not in fields:
            errs.append('missing:'+k); continue
        v=fields[k]
        if not isinstance(v, dict):
            errs.append('not_dict:'+k); continue
        if k=='spoken_markers':
            st=v.get('status')
            sme=rec.get('spoken_marker_eligible')
            mod=rec.get('modality')
            if mod=='COMPLETE_TEXT' and st not in ('N/A_TEXT_MODALITY','NA_TEXT'):
                errs.append('text_spoken_markers_bad')
            if sme=='NO' and st not in ('SKIPPED_INELIGIBLE','N/A_TEXT_MODALITY') and v.get('markers'):
                # markers list nonempty while ineligible is FAIL for freq use; allow empty skip
                if st=='COUNTED':
                    errs.append('ineligible_counted')
            continue
        if k=='logic_units':
            if not v.get('units'): errs.append('empty_logic_units')
            continue
        if k=='guanyu_transfer_value':
            if v.get('decision') not in ('KEEP','ADAPT','REJECT'):
                errs.append('bad_transfer')
            continue
        if not (v.get('summary') or v.get('patterns') or v.get('evidence')):
            errs.append('empty:'+k)
        for e in (v.get('evidence') or []):
            if not e.get('sentence_id'):
                errs.append('no_sid:'+k); break
    return len(errs)==0, errs

def main(n_target:int):
    sample=list(csv.DictReader((analysis/'PHASE_C_SAMPLE.csv').open()))[:n_target]
    want={r['work_id']:r for r in sample}
    recs=load_done()
    by_id={r.get('work_id'):r for r in recs if r.get('work_id')}
    present=[by_id[w] for w in want if w in by_id]
    missing=[w for w in want if w not in by_id]
    ok_list=[]; fail_list=[]
    for r in present:
        ok,errs=validate_one(r)
        (ok_list if ok else fail_list).append((r.get('work_id'), errs))
    # structural checks
    creators=Counter((by_id[w].get('creator_id') if w in by_id else want[w]['creator_id']) for w in want if w in by_id)
    mods=Counter(by_id[w].get('modality') for w in want if w in by_id)
    tiers=Counter(by_id[w].get('performance_tier') for w in want if w in by_id)
    # template-hash crude: identical summaries across creators
    template_risk=0
    summaries=defaultdict(list)
    for w,r in by_id.items():
        if w not in want: continue
        s=(r.get('fields') or {}).get('opening_move',{}).get('summary')
        if s: summaries[s].append(r.get('creator_id'))
    for s,cids in summaries.items():
        if len(set(cids))>=3: template_risk+=1

    structural_fail=False
    reasons=[]
    if missing:
        structural_fail=True; reasons.append(f'missing_json:{len(missing)}')
    if fail_list:
        structural_fail=True; reasons.append(f'schema_fail:{len(fail_list)}')
    if n_target>=120 and template_risk>=5:
        structural_fail=True; reasons.append(f'template_risk:{template_risk}')
    if n_target>=240:
        # imbalance: each creator in sample should appear; tier not all HIGH
        if len(creators)<4:
            structural_fail=True; reasons.append('creator_coverage_low')
        if tiers.get('HIGH',0)>0 and tiers.get('CONTROL',0)==0 and tiers.get('MEDIAN',0)==0:
            structural_fail=True; reasons.append('tier_collapse')

    report={
        'checkpoint': n_target,
        'present': len(present),
        'missing': len(missing),
        'schema_ok': len(ok_list),
        'schema_fail': len(fail_list),
        'creators': dict(creators),
        'modalities': dict(mods),
        'tiers': dict(tiers),
        'template_risk': template_risk,
        'structural_pass': not structural_fail,
        'reasons': reasons,
        'fail_examples': fail_list[:10],
        'missing_ids': missing[:20],
    }
    out=analysis/f'PHASE_C_CHECKPOINT_{n_target}.json'
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if not structural_fail else 2

if __name__=='__main__':
    sys.exit(main(int(sys.argv[1]) if len(sys.argv)>1 else 30))
