#!/usr/bin/env python3
"""
Phase 3: Deep Analysis Batch Selection
- Add content_style, guanyu_fit_score, viral_type
- Calculate creator baseline
- Select balanced 30-candidate batch
"""
import json
import csv
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE_DIR = Path(r"C:\workspace\AI_Media_Matrix\01_benchmark\shards\hermes_real")
SELECTION_FILE = BASE_DIR / "douyin_benchmark_selection.csv"
DEEP_BATCH_FILE = BASE_DIR / "deep_analysis_batch_001.csv"
MEDIA_DIR = BASE_DIR / "media"
TRANS_DIR = BASE_DIR / "transcripts"
ANALYSIS_DIR = BASE_DIR / "analysis"
CREATOR_PANEL_DIR = BASE_DIR / "creator_panels"
TOPIC_COMP_DIR = BASE_DIR / "topic_comparisons"
REPORTS_DIR = BASE_DIR / "reports"

# Create output dirs
for d in [MEDIA_DIR, TRANS_DIR, ANALYSIS_DIR, CREATOR_PANEL_DIR, TOPIC_COMP_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def load_selection():
    """Load the 100-selection benchmark"""
    records = []
    with open(SELECTION_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Fix BOM issue
            clean_row = {k.lstrip('\ufeff'): v for k, v in row.items()}
            records.append(clean_row)
    return records

def analyze_content_style(desc, title=""):
    """Analyze content style based on description/title"""
    text = f"{desc} {title}".lower()
    
    styles = []
    
    # KNOWLEDGE_EXPLAINER - educational content
    if any(k in text for k in ['原理', '逻辑', '本质', '为什么', '如何', '方法', '知识', '认知', '思维']):
        styles.append('KNOWLEDGE_EXPLAINER')
    
    # TALKING_HEAD - direct address
    if any(k in text for k in ['我', '你', '我们', '说说', '讲讲', '今天']):
        styles.append('TALKING_HEAD')
    
    # VOICEOVER_EXPLAINER - narration style
    if any(k in text for k in ['带你', '教你', '告诉你', '科普', '揭秘']):
        styles.append('VOICEOVER_EXPLAINER')
    
    # STORY_EXPLAINER - narrative
    if any(k in text for k in ['故事', '经历', '创业', '经验', '分享', '经历']):
        styles.append('STORY_EXPLAINER')
    
    # If no specific style detected, default to KNOWLEDGE_EXPLAINER for cognitive content
    if not styles:
        styles.append('KNOWLEDGE_EXPLAINER')
    
    return styles[0] if styles else 'OTHER'

def calculate_guanyu_fit(record):
    """Calculate guanyu_fit_score (0-100)"""
    desc = record.get('desc', '')
    likes = int(record.get('liked_count', 0) or 0)
    comments = int(record.get('comment_count', 0) or 0)
    favorites = int(record.get('collected_count', 0) or 0)
    shares = int(record.get('share_count', 0) or 0)
    
    # Topic relevance (25) - knowledge/business topics score higher
    topic_keywords = ['赚钱', '商业', '思维', '认知', '创业', '职场', '财富', '副业', '搞钱', '变现']
    topic_score = min(25, sum(25 for k in topic_keywords if k in desc) // max(1, len(topic_keywords)))
    
    # Cognitive value (25) - based on favorite/like ratio
    fav_like_ratio = favorites / max(likes, 1)
    cognitive_score = min(25, int(fav_like_ratio * 100))
    
    # Spoken content value (20) - questions, explanations indicate spoken content
    question_mark = desc.count('？') + desc.count('?')
    explanation_markers = len([k for k in ['因为', '所以', '但是', '其实', '其实'] if k in desc])
    spoken_score = min(20, question_mark * 5 + explanation_markers * 3)
    
    # Logic depth (20) - numbered lists, structured content
    number_patterns = len(re.findall(r'[一二三四五六七八九十billionillion][个条种方法]', desc))
    structure_markers = len([k for k in ['第一', '第二', '首先', '其次', '最后', '总结'] if k in desc])
    logic_score = min(20, number_patterns * 5 + structure_markers * 4)
    
    # Format transferability (10) - suitable for different platforms
    format_score = 10 if any(k in desc for k in ['干货', '教程', '攻略', '指南']) else 5
    
    total = topic_score + cognitive_score + spoken_score + logic_score + format_score
    return min(100, max(0, total))

def classify_viral_type(record):
    """Classify viral type based on engagement patterns"""
    likes = int(record.get('liked_count', 0) or 0)
    comments = int(record.get('comment_count', 0) or 0)
    favorites = int(record.get('collected_count', 0) or 0)
    shares = int(record.get('share_count', 0) or 0)
    
    types = []
    
    # Calculate ratios
    like_base = max(likes, 1)
    comment_ratio = comments / like_base
    fav_ratio = favorites / like_base
    share_ratio = shares / like_base
    
    # Classify
    if comment_ratio > 0.02:
        types.append('COMMENT_HEAVY')
    if fav_ratio > 0.3:
        types.append('SAVE_HEAVY')
    if share_ratio > 0.1:
        types.append('SHARE_HEAVY')
    
    # Get base role
    role = record.get('sample_role', '')
    if role == 'ABSOLUTE_VIRAL':
        types.append('ABSOLUTE_VIRAL')
    elif role == 'RELATIVE_BREAKOUT':
        types.append('RELATIVE_BREAKOUT')
    elif role == 'CONTROL':
        types.append('CONTROL')
    
    return ';'.join(types) if types else 'NORMAL_REFERENCE'

def analyze_records(records):
    """Add analysis fields to records"""
    for r in records:
        # Content style
        r['content_style'] = analyze_content_style(r.get('desc', ''), r.get('title', ''))
        
        # Guanyu fit score
        r['guanyu_fit_score'] = calculate_guanyu_fit(r)
        
        # Viral type
        r['viral_type'] = classify_viral_type(r)
        
        # Ratios
        likes = int(r.get('liked_count', 0) or 0)
        favs = int(r.get('collected_count', 0) or 0)
        shares = int(r.get('share_count', 0) or 0)
        comments = int(r.get('comment_count', 0) or 0)
        
        r['favorite_like_ratio'] = round(favs / max(likes, 1), 3)
        r['share_like_ratio'] = round(shares / max(likes, 1), 3)
        r['comment_like_ratio'] = round(comments / max(likes, 1), 3)
    
    return records

def select_deep_batch(records, target=30):
    """Select balanced 30-candidate deep analysis batch"""
    
    # Filter by guanyu_fit_score >= 60 for core
    core_candidates = [r for r in records if int(r.get('guanyu_fit_score', 0)) >= 60]
    other_candidates = [r for r in records if int(r.get('guanyu_fit_score', 0)) < 60]
    
    # Sort by performance_score within each group
    core_candidates.sort(key=lambda x: float(x.get('performance_score', 0)), reverse=True)
    other_candidates.sort(key=lambda x: float(x.get('performance_score', 0)), reverse=True)
    
    selected = []
    seen_ids = set()
    
    # Target: ABSOLUTE_VIRAL 8, RELATIVE_BREAKOUT 8, SAVE/SHARE 6, CONTROL 8
    targets = {
        'ABSOLUTE_VIRAL': 8,
        'RELATIVE_BREAKOUT': 8,
        'SAVE_HEAVY': 3,
        'SHARE_HEAVY': 3,
        'CONTROL': 8,
        'COMMENT_HEAVY': 3
    }
    
    # First pass: select by target distribution
    for vtype, count in targets.items():
        for r in core_candidates + other_candidates:
            if len(selected) >= target:
                break
            if r.get('aweme_id') in seen_ids:
                continue
            
            viral_types = r.get('viral_type', '').split(';')
            if vtype in viral_types:
                selected.append(r)
                seen_ids.add(r.get('aweme_id'))
                if len([s for s in selected if vtype in s.get('viral_type', '')]) >= count:
                    break
    
    # Fill remaining with top performers
    for r in core_candidates + other_candidates:
        if len(selected) >= target:
            break
        if r.get('aweme_id') not in seen_ids:
            selected.append(r)
            seen_ids.add(r.get('aweme_id'))
    
    # Ensure diversity: limit per creator
    creator_counts = defaultdict(int)
    final_selected = []
    for r in selected:
        creator = r.get('nickname', '')
        if creator_counts[creator] >= 2:  # Max 2 per creator
            continue
        creator_counts[creator] += 1
        final_selected.append(r)
        if len(final_selected) >= target:
            break
    
    return final_selected[:target]

def main():
    print("=== PHASE 3: DEEP ANALYSIS BATCH SELECTION ===\n")
    
    # Load selection
    records = load_selection()
    print(f"Loaded {len(records)} records from selection")
    
    # Analyze
    records = analyze_records(records)
    
    # Save updated selection
    fieldnames = ['aweme_id', 'content_id', 'url', 'nickname', 'desc', 'source_keyword',
                  'liked_count', 'comment_count', 'collected_count', 'share_count',
                  'liked_count_percentile', 'performance_score', 'sample_role', 
                  'metadata_source', 'content_style', 'guanyu_fit_score', 'viral_type',
                  'favorite_like_ratio', 'share_like_ratio', 'comment_like_ratio']
    
    with open(SELECTION_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            writer.writerow({k: r.get(k, '') for k in fieldnames})
    
    print(f"Updated selection saved")
    
    # Select deep batch
    deep_batch = select_deep_batch(records, target=30)
    print(f"Selected {len(deep_batch)} for deep analysis")
    
    # Stats
    viral_count = sum(1 for r in deep_batch if 'ABSOLUTE_VIRAL' in r.get('viral_type', ''))
    breakout_count = sum(1 for r in deep_batch if 'RELATIVE_BREAKOUT' in r.get('viral_type', ''))
    save_count = sum(1 for r in deep_batch if 'SAVE_HEAVY' in r.get('viral_type', ''))
    share_count = sum(1 for r in deep_batch if 'SHARE_HEAVY' in r.get('viral_type', ''))
    control_count = sum(1 for r in deep_batch if 'CONTROL' in r.get('viral_type', ''))
    
    creators = len(set(r.get('nickname', '') for r in deep_batch))
    topics = len(set(r.get('source_keyword', '') for r in deep_batch))
    core_count = sum(1 for r in deep_batch if int(r.get('guanyu_fit_score', 0)) >= 60)
    
    print(f"\n=== DEEP BATCH STATS ===")
    print(f"ABSOLUTE_VIRAL: {viral_count}")
    print(f"RELATIVE_BREAKOUT: {breakout_count}")
    print(f"SAVE_HEAVY: {save_count}")
    print(f"SHARE_HEAVY: {share_count}")
    print(f"CONTROL: {control_count}")
    print(f"Creators: {creators}")
    print(f"Topics: {topics}")
    print(f"Core (guanyu_fit>=60): {core_count}")
    
    # Save deep batch
    deep_fieldnames = fieldnames + ['relative_like_ratio', 'baseline_sample_n']
    with open(DEEP_BATCH_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=deep_fieldnames)
        writer.writeheader()
        for r in deep_batch:
            writer.writerow({k: r.get(k, '') for k in deep_fieldnames})
    
    print(f"\nSaved to: {DEEP_BATCH_FILE}")
    
    return deep_batch

if __name__ == "__main__":
    main()
