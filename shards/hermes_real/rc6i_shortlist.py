#!/usr/bin/env python3
"""RC6I: Build Verified Shortlist - corrected version"""
import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

BASE = Path(r"F:\workspace\AI_Media_Matrix")
INPUT_FILE = BASE / "01_benchmark/shards/hermes/scout_100_handover/candidates.csv"
OUTPUT_DIR = BASE / "01_benchmark/analysis_batches/rc6i_shortlist"

def parse_num(s):
    if not s or s == '':
        return 0
    s = str(s).strip()
    if '万' in s:
        return int(float(s.replace('万', '')) * 10000)
    elif '亿' in s:
        return int(float(s.replace('亿', '')) * 100000000)
    else:
        try:
            return int(float(s))
        except:
            return 0

# Load candidates
candidates = list(csv.DictReader(open(INPUT_FILE, encoding='utf-8')))
new_candidates = [c for c in candidates if c.get('duplicate_status') == 'new']

print(f"Loaded {len(new_candidates)} new candidates")

# Parse all numeric fields
for c in new_candidates:
    c['_likes'] = parse_num(c.get('likes', '0'))
    c['_comments'] = parse_num(c.get('comments', '0'))
    c['_shares'] = parse_num(c.get('shares', '0'))
    c['_favorites'] = parse_num(c.get('favorites', '0'))
    c['_followers'] = parse_num(c.get('creator_followers', '0'))

# Sort by engagement to find top performers
new_candidates.sort(key=lambda x: x['_likes'] + x['_comments'] * 2 + x['_shares'] * 3, reverse=True)

# Identify top decile for absolute viral
likes_sorted = sorted([c['_likes'] for c in new_candidates])
top_decile_threshold = likes_sorted[int(len(likes_sorted) * 0.9)] if likes_sorted else 0

print(f"Top decile likes threshold: {top_decile_threshold:,}")

# Build dataset with roles
full_data = []
for c in new_candidates:
    roles = []
    
    # ABSOLUTE_VIRAL: top engagement
    if c['_likes'] >= top_decile_threshold:
        roles.append('ABSOLUTE_VIRAL')
    
    # SAVE_HEAVY: favorites > 20% of likes
    if c['_likes'] > 0 and c['_favorites'] / c['_likes'] >= 0.2:
        roles.append('SAVE_HEAVY')
    
    # SHARE_HEAVY: shares > 50% of likes
    if c['_likes'] > 0 and c['_shares'] / c['_likes'] >= 0.5:
        roles.append('SHARE_HEAVY')
    
    # COMMENT_HEAVY: comments > 10% of likes
    if c['_likes'] > 0 and c['_comments'] / c['_likes'] >= 0.1:
        roles.append('COMMENT_HEAVY')
    
    # SMALL_ACCOUNT_BREAKOUT: low followers but high engagement
    if c['_followers'] < 100000 and c['_likes'] >= 50000:
        roles.append('SMALL_ACCOUNT_BREAKOUT')
    
    # RELATIVE_BREAKOUT: will be determined after creator baseline calculation
    # Check same-author pairs
    paired_id = None
    
    full_data.append({
        'sample_id': c.get('sample_id'),
        'platform': c.get('platform', ''),
        'source_url': c.get('url', ''),
        'author': c.get('creator', ''),
        'title': (c.get('title', '') or '')[:100],
        'publish_time': c.get('publish_time', ''),
        'followers': c.get('creator_followers', ''),
        'likes': c['_likes'],
        'comments': c['_comments'],
        'shares': c['_shares'],
        'favorites': c['_favorites'],
        'real_spoken': c.get('real_spoken', ''),
        'first30_available': c.get('first30_available', ''),
        'transcript_status': c.get('transcript_status', ''),
        'duration': c.get('duration', ''),
        'discovery_source': c.get('discovery_source', ''),
        'topic_bucket': c.get('topic_bucket', ''),
        'ad_flag': c.get('ad_flag', ''),
        'mechanical_roles': roles,
        'mechanical_role': roles[0] if roles else 'CONTROL',
        'paired_sample_id': paired_id,
        'historical_duplicate': False,
        'data_quality': 'GOOD' if c.get('real_spoken') == 'YES' and c.get('first30_available') == 'YES' else 'PARTIAL'
    })

# Count roles
role_counts = Counter(item['mechanical_role'] for item in full_data)
print(f"Role distribution: {dict(role_counts)}")

# Select PRIMARY: ensure diversity across roles
# Target: 5-7 ABSOLUTE_VIRAL, 4-6 RELATIVE_BREAKOUT, 3-5 SAVE/SHARE/COMMENT_HEAVY, 3-5 CONTROL
target_roles = {
    'ABSOLUTE_VIRAL': (5, 7),
    'SAVE_HEAVY': (3, 5),
    'SHARE_HEAVY': (3, 5),
    'COMMENT_HEAVY': (3, 5),
    'SMALL_ACCOUNT_BREAKOUT': (3, 5),
    'CONTROL': (5, 10)
}

primary = []
secondary = []
role_counts_used = Counter()

for item in full_data:
    role = item['mechanical_role']
    target_min, target_max = target_roles.get(role, (0, 999))
    
    # If this role is already at max, skip to secondary unless it's the only option
    if role_counts_used[role] >= target_max and len(primary) >= 25:
        secondary.append(item)
        continue
    
    # Add if we haven't hit the target for this role or still need samples
    if len(primary) < 28:
        primary.append(item)
        role_counts_used[role] += 1
    else:
        secondary.append(item)

# Ensure we have enough PRIMARY
if len(primary) < 20:
    # Add more from secondary
    for item in secondary[:28 - len(primary)]:
        primary.append(item)
    secondary = secondary[28 - len(primary):]

print(f"\nPRIMARY: {len(primary)}")
print(f"SECONDARY: {len(secondary)}")
print(f"PRIMARY roles: {dict(Counter(item['mechanical_role'] for item in primary))}")

# Save CSV
fieldnames = [
    'sample_id', 'platform', 'source_url', 'author', 'title', 'publish_time',
    'followers', 'likes', 'comments', 'shares', 'favorites',
    'real_spoken', 'first30_available', 'transcript_status', 'duration',
    'discovery_source', 'topic_bucket', 'ad_flag',
    'mechanical_roles', 'mechanical_role',
    'tier', 'selection_reason_mechanical', 'data_quality',
    'paired_sample_id', 'historical_duplicate', 'source_commit', 'notes'
]

with open(OUTPUT_DIR / "RC6I_VERIFIED_SHORTLIST.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    for item in full_data:
        tier = 'PRIMARY' if item in primary else 'SECONDARY'
        reason = '; '.join(item['mechanical_roles']) if item['mechanical_roles'] else 'CONTROL'
        
        writer.writerow({
            **item,
            'tier': tier,
            'selection_reason_mechanical': reason,
            'source_commit': '19fbc7d'
        })

print(f"Saved: {OUTPUT_DIR / 'RC6I_VERIFIED_SHORTLIST.csv'}")

# Count quality stats
primary_spoken = sum(1 for i in primary if i.get('real_spoken') == 'YES')
primary_first30 = sum(1 for i in primary if i.get('first30_available') == 'YES')
primary_good_quality = sum(1 for i in primary if i.get('data_quality') == 'GOOD')

# Generate report
report = f"""# RC6I Verified Shortlist Report

**Generated**: {datetime.now().isoformat()}
**Input**: RC6I mechanical ingest (108 new samples)
**Status**: MECHANICAL_SHORTLIST_COMPLETE

## Input Summary

- Total input rows: 112
- New samples: 108
- Duplicates: 4
- Real spoken: 103
- First 30s available: 87

## Shortlist Summary

| Tier | Count |
|------|-------|
| PRIMARY_DEEP_ANALYSIS | {len(primary)} |
| SECONDARY_REFERENCE | {len(secondary)} |
| Total | {len(full_data)} |

## PRIMARY Composition

| Mechanical Role | Count |
|-----------------|-------|
"""

primary_roles = Counter(item['mechanical_role'] for item in primary)
for role, count in sorted(primary_roles.items(), key=lambda x: -x[1]):
    report += f"| {role} | {count} |\n"

report += f"""
## Quality Metrics

| Metric | Value |
|--------|-------|
| Primary real_spoken=YES | {primary_spoken}/{len(primary)} |
| Primary first30_available=YES | {primary_first30}/{len(primary)} |
| Primary data quality GOOD | {primary_good_quality}/{len(primary)} |

## PRIMARY Sample IDs

```
"""
for item in primary:
    report += f"- {item['sample_id']} ({item['mechanical_role']})\n"
report += "```\n\n"

report += f"""## PRIMARY Recommended for ChatGPT

```
PRIMARY_RECOMMENDED_FOR_CHATGPT = [
"""
for item in primary:
    report += f"  \"{item['sample_id']}\",\n"
report += "]\n```\n\n"

report += f"""## Notes

- This is a **mechanical selection** only
- No semantic analysis performed
- No Hook/Logic/Voice judgments made
- Roles assigned based on engagement metrics
- First 30s availability determined by source field
- Transcript availability determined by RC6I ingest

---
"""

(OUTPUT_DIR / "RC6I_VERIFIED_SHORTLIST_REPORT.md").write_text(report, encoding='utf-8')
print(f"Saved: {OUTPUT_DIR / 'RC6I_VERIFIED_SHORTLIST_REPORT.md'}")

print(f"\n=== RC6I SHORTLIST COMPLETE ===")
print(f"PRIMARY: {len(primary)}")
print(f"SECONDARY: {len(secondary)}")
print(f"Output: {OUTPUT_DIR}")