#!/usr/bin/env python3
"""RC6F: Run ASR on all RC6F samples"""
import json
import csv
import subprocess
from pathlib import Path
from datetime import datetime
import faster_whisper

BASE = Path(r"F:\workspace\AI_Media_Matrix")
CORPUS = BASE / "01_benchmark/plain_language_corpus_v1"

print(f"=== Running ASR on RC6F samples ===\n")

# Load Whisper model
print("Loading Whisper model...")
model = faster_whisper.WhisperModel("base", device="cpu", compute_type="int8")
print("Model loaded.\n")

# Get RC6F samples
samples = sorted([d for d in CORPUS.glob("RC6F_*") if d.is_dir()])
print(f"Samples to process: {len(samples)}\n")

asr_complete = 0
asr_failed = 0

for sample_dir in samples:
    sample_id = sample_dir.name
    audio_path = sample_dir / "audio.m4a"
    
    if not audio_path.exists():
        print(f"[{sample_id}] No audio - skipping")
        asr_failed += 1
        continue
    
    print(f"[{sample_id}] Processing...")
    
    try:
        # Run ASR
        segments, info = model.transcribe(str(audio_path), beam_size=5, language="zh")
        
        # Collect segments
        transcript_segments = []
        full_text = []
        
        for seg in segments:
            segment = {
                "start": round(seg.start, 1),
                "end": round(seg.end, 1),
                "text": seg.text.strip(),
                "segment_id": f"S{len(transcript_segments)+1:04d}"
            }
            transcript_segments.append(segment)
            full_text.append(seg.text.strip())
        
        full_text_str = "\n".join(full_text)
        transcript_chars = len(full_text_str.replace(" ", "").replace("\n", ""))
        
        # Get first 30s text
        first30s_text = "".join([s["text"] for s in transcript_segments if s["end"] <= 30])
        
        # Save transcript JSON
        transcript_json = {
            "status": "COMPLETE",
            "segments": transcript_segments,
            "full_text": full_text_str,
            "transcript_chars": transcript_chars,
            "first30s_text": first30s_text,
            "source": "faster_whisper_base_model",
            "generated_at": datetime.now().isoformat()
        }
        
        (sample_dir / "03_transcript_raw.json").write_text(
            json.dumps(transcript_json, ensure_ascii=False, indent=2), encoding='utf-8')
        
        # Save transcript markdown
        md_content = f"# Transcript: {sample_id}\n\n"
        md_content += f"**Full text** ({transcript_chars} chars):\n\n{full_text_str}\n\n"
        md_content += f"**Segments**: {len(transcript_segments)}\n\n"
        md_content += "## Segments\n\n"
        for seg in transcript_segments:
            md_content += f"- **{seg['start']:.1f}s - {seg['end']:.1f}s**: {seg['text']}\n"
        
        (sample_dir / "04_transcript_raw.md").write_text(md_content, encoding='utf-8')
        
        # Update metadata
        meta_path = sample_dir / "01_metadata.json"
        if meta_path.exists():
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            meta['transcript_chars'] = transcript_chars
            meta['transcript_usable'] = transcript_chars > 50
            meta['first30s_available'] = len(first30s_text) > 20
            meta['segment_count'] = len(transcript_segments)
            meta['asr_status'] = 'COMPLETE'
            meta['asr_model'] = 'faster_whisper_base'
            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
        
        asr_complete += 1
        print(f"  ✓ {transcript_chars} chars, {len(transcript_segments)} segments")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        asr_failed += 1

print(f"\n=== ASR Complete ===")
print(f"Successful: {asr_complete}/{len(samples)}")
print(f"Failed: {asr_failed}")